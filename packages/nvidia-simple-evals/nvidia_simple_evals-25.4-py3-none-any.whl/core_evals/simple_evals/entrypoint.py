import argparse
import logging
import multiprocessing
import os
import sys

import yaml

from .adapters.adapter_config import AdapterConfig

# NOTE(dfridman): will be removed once all benchmarks comply with updated output format
from .api_dataclasses import EvaluationConfig, EvaluationResult, EvaluationTarget
from .evaluate import evaluate_accuracy
from .input import (
    get_available_evaluations,
    load_run_config,
    parse_cli_args,
    validate_cli_args,
    validate_evaluation,
)
from .utils import deep_update

# Note: When using spawn, Python cannot pickle certain objects including:
# - Lambda functions
# - Local functions
# - Functions defined in __main__
# - Functions with closures
# - Objects with unpicklable attributes
# The default start method for multiprocessing on macOS is spawn, which is why we explicitly
# set the start method to "fork" to avoid these limitations when running on macOS.
multiprocessing.set_start_method("fork")

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug", action="store_true", help="Debug the core_evals script"
    )
    subparsers = parser.add_subparsers(help="Functions")
    parser_ls = subparsers.add_parser("ls", help="List available evaluation types")
    parser_ls.set_defaults(command="ls")

    parser_run = subparsers.add_parser("run_eval", help="Run the evaluation")
    parser_run.add_argument("--eval_type", type=str, help="Run config.: task name")
    parser_run.add_argument("--model_id", type=str, help="Run config.: model name")
    parser_run.add_argument(
        "--model_type",
        type=str,
        help="Run config.: endpoint type",
        choices=["chat", "completions", "vlm", "embedding"],
    )
    parser_run.add_argument("--model_url", type=str, help="Run config.: model URI")
    parser_run.add_argument(
        "--output_dir", type=str, help="Run config.: results output dir."
    )
    parser_run.add_argument(
        "--api_key_name",
        type=str,
        help="Run config.: API key env variable name (optional)",
        default=None,
    )
    parser_run.add_argument(
        "--run_config",
        type=str,
        help="Load the run configuration from the YAML file (optional and overridden by the cli arguments)",
        default=None,
    )
    parser_run.add_argument(
        "--overrides",
        type=str,
        help="Comma-separated dot-style parameters to override config values (overriding values from run_config and CLI args)",
        default=None,
    )
    parser_run.add_argument(
        "--dry_run",
        action="store_true",
        help="Shows rendered config and command instead of running",
        default=False,
    )
    parser_run.set_defaults(command="run_eval")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if "command" not in args:
        parser.print_help()
        sys.exit(0)
    return args

def show_available_tasks()-> None:
    _, eval_name_mapping, _ = get_available_evaluations()
    print("Available tasks:")
    for evaluation in sorted(
        eval_name_mapping.values(), key=lambda task: task.config.type
    ):
        print(f"* {evaluation.config.type} (in {evaluation.framework_name})")

def run_evaluation(args) -> None:
    run_config = load_run_config(args.run_config) if args.run_config else {}
    # CLI args take precedence over YAML run config
    run_config = deep_update(run_config, parse_cli_args(args), skip_nones=True)
    validate_cli_args(run_config)
    if args.dry_run:
        evaluation = validate_evaluation(run_config)
        print("Rendered config:\n")
        config = evaluation.model_dump()
        print(
            yaml.dump(config, sort_keys=False, default_flow_style=False, indent=2)
        )
        print("\nRendered command:\n")
        cmd = evaluation.render_command()
        print(cmd)
        exit(0)

    # If adapter is not configured either via yaml or --overrides, it's disabled
    adapter_config: AdapterConfig | None = AdapterConfig.get_validated_config(
        run_config
    )
    adapter = None
    if adapter_config:
        from .adapters.server import AdapterServer
        adapter = AdapterServer(
            api_url=run_config["target"]["api_endpoint"]["url"],
            adapter_config=adapter_config,
        )
        p: multiprocessing.Process | None = multiprocessing.Process(
            target=adapter.run
        )
        # This will be unhooked below
        run_config["target"]["api_endpoint"][
            "url"
        ] = f"http://{adapter.adapter_host}:{adapter.adapter_port}"
        p.start()

    eval_cfg = EvaluationConfig(**run_config["config"])
    target_cfg = EvaluationTarget(**run_config["target"])

    try:
        evaluation_result = evaluate_accuracy(eval_cfg, target_cfg)
    finally:
        # TODO(agronskiy): remove this logic once the streaming based disable works (see jira/COML1KNX-475)
        if adapter_config and p.is_alive():
            p.terminate()

    if isinstance(evaluation_result, EvaluationResult):
        evaluation_result_dict = evaluation_result.model_dump(exclude_none=True)
    else:
        logging.warning("Deprecated output API is used. Will be updated soon.")
        evaluation_result_dict = evaluation_result

    run_command = validate_evaluation(
        {"config": eval_cfg.model_dump(), "target": target_cfg.model_dump()}
    ).render_command()

    # NOTE(agronskiy): for result logging purposes and for keepiing the config intact, we hook the
    # actual upstream api endpoint back, to avoid logging useless `localhost:xxxx`.
    if adapter:
        run_config["target"]["api_endpoint"]["url"] = adapter.api_url

    evaluation_result_dict = {
        "git_hash": os.getenv("CORE_EVALS_GIT_HASH"),
        "command": run_command,
        **run_config,
        "results": evaluation_result_dict,
    }
    with open(os.path.join(eval_cfg.output_dir, "results.yml"), "w") as f:
        yaml.dump(evaluation_result_dict, f)

    print("========== RESULTS ==========")
    print(yaml.dump(evaluation_result_dict))

def run_eval() -> None:
    args = get_args()

    if args.command == "ls":
        show_available_tasks()
    elif args.command == "run_eval":
        run_evaluation(args)

if __name__ == "__main__":
    run_eval()
