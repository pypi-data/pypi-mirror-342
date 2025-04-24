import argparse
import asyncio
import json
import logging
import os
import random
import numpy as np
from pathlib import Path
from typing import Union
import simple_evals.common as common
from simple_evals.constants import GPQA_VARIANTS, MULTILINGUAL_MMLU
from simple_evals.evals.gpqa_eval import GPQAEval
from simple_evals.evals.humaneval_eval import HumanEval
from simple_evals.evals.simpleqa_eval import SimpleQAEval
from simple_evals.evals.math_eval import MathEval
from simple_evals.evals.mgsm_eval import MGSMEval
from simple_evals.evals.mmlu_eval import MMLUEval
from simple_evals.evals.mmlu_pro_eval import MMLUProEval
from simple_evals.sampler.chat_completion_sampler import (
    OPENAI_SYSTEM_MESSAGE_API, ChatCompletionSampler)
from simple_evals.seed_generator import SeedGenerator


def int_or_float(value):
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid number: {value}")


async def run():
    parser = argparse.ArgumentParser(
        description="Run a single evaluation using a specified model and evaluation type."
    )
    parser.add_argument(
        "--model",
        type=str,
        default="meta/llama-3.1-8b-instruct",
        help="Model name to use. Default: meta/llama-3.1-8b-instruct",
    )
    parser.add_argument(
        "--eval_name",
        type=str,
        default="mmlu",
        choices=["math_test_500", "AIME_2024", "AIME_2025",  "AA_math_test_500", "AA_AIME_2024", "mmlu", "mmlu_pro", "mgsm", "humaneval", "humanevalplus", "simpleqa"]
        + MULTILINGUAL_MMLU
        + GPQA_VARIANTS,
        help="Name of the evaluation to run. Default: math",
    )
    parser.add_argument(
        "--url",
        type=str,
        default="https://integrate.api.nvidia.com/v1/chat/completions",
        help="URL for the model API. Default: https://integrate.api.nvidia.com/v1/chat/completions",
    )
    parser.add_argument(
        "--examples", type=int, help="Number of examples to use (overrides default)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0,
        help="Sampling temperature. Default: 0.0.",
    )
    parser.add_argument(
        "--top_p",
        type=float,
        default=1.0,
        help="Top-p sampling parameter. Default: 1.0.",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=4096,
        help="Maximum number of tokens for the model to generate. Default: 512.",
    )
    parser.add_argument(
        "--out_dir",
        type=str,
        default="/tmp",
        help="Directory to save output files. Default: /tmp",
    )
    parser.add_argument(
        "--max_retries", type=int, default=10, help="Server max retries (default: 10)"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Server timeout in seconds (default: None)",
    )
    parser.add_argument("--num_threads", type=int, default=20, help="Number of threads")
    parser.add_argument(
        "--first_n", type=int_or_float, default=None,
        help="Use only first n examples. If a float is provided, it will be interpreted as a percentage of the total number of examples."
    )
    parser.add_argument(
        "--cache_dir", type=str, default="cache", help="Repsonses cache dir"
    )
    parser.add_argument(
        "--num_repeats",
        type=int,
        default=1,
        help="Number of repeats for each sample, available only for math, humaneval and gpqa",
    )
    parser.add_argument("--debug", action="store_true", help="Run in debug mode.")
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)",
    )
    parser.add_argument(
        "--downsampling_ratio",
        type=float,
        default=None,
        help="Ratio of examples to use from the dataset (between 0 and 1)",
    )
    parser.add_argument(
        "--add_system_prompt",
        action="store_true",
        help="Add system prompt for the model",
    )

    args = parser.parse_args()
    
    # Initialize the seed generator
    seed_generator = SeedGenerator(base_seed=args.seed)
    
    random.seed(args.seed)
    np.random.seed(args.seed)
    
    common_eval_args = {
        "num_threads": args.num_threads,
        "cache_dir": args.cache_dir,
        "first_n": args.first_n,
        "seed_generator": seed_generator,  # Pass the seed generator instance
    }
    sampler = ChatCompletionSampler(
        model=args.model,
        system_message=OPENAI_SYSTEM_MESSAGE_API if args.add_system_prompt else None,
        url=args.url,
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens,
        timeout=args.timeout,
        max_retries=args.max_retries,
        api_key=os.environ.get("API_KEY"),
    )

    def get_eval(eval_name):
        if eval_name == "mmlu_pro":
            return MMLUProEval(
                **common_eval_args,
            )
        if eval_name.startswith("mmlu"):
            return MMLUEval(
                language="EN-US" if eval_name == "mmlu" else eval_name.split("_")[1],
                downsampling_ratio=args.downsampling_ratio,
                **common_eval_args,
            )
        if eval_name.startswith("gpqa"):
            return GPQAEval(
                n_repeats=args.num_repeats,
                variant=eval_name.split("_")[1],
                **common_eval_args,
            )

        if eval_name in ["math_test_500", "AIME_2024", "AA_math_test_500", "AA_AIME_2024", "AIME_2025"]:
            if eval_name.startswith("AA_"):
                equality_checker = "llama70b"
            else:
                equality_checker = "gpt4"
                
            return MathEval(
                equality_checker=equality_checker,
                eval_name=eval_name,
                n_repeats=args.num_repeats,
                **common_eval_args,
            )
        match eval_name:
            case "mgsm":
                return MGSMEval(
                    num_examples_per_lang=250,
                    **common_eval_args,
                )
            case "humaneval" | "humanevalplus":
                return HumanEval(
                    eval_name=eval_name,
                    num_samples_per_task=args.num_repeats, **common_eval_args
                )
            case "simpleqa":
                grader_model = "gpt4"
                return SimpleQAEval(
                    n_repeats=args.num_repeats, grader_model=grader_model, **common_eval_args
                )
            case _:
                raise Exception(f"Unrecognized eval type: {eval_name}")

    # Create the evaluation object
    eval_obj = get_eval(args.eval_name)

    # Run the evaluation
    result = await eval_obj(sampler)
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    # Prepare file names
    debug_suffix = "_DEBUG" if args.debug else ""
    file_stem = f"{args.eval_name}"
    # Ensure output directory exists
    out_dir = Path(args.out_dir)
    os.makedirs(out_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Define file paths
    report_filename = out_dir / f"{file_stem}{debug_suffix}.html"
    result_filename = out_dir / f"{file_stem}{debug_suffix}.json"

    print(f"Writing report to {report_filename}")
    with open(report_filename, "w") as fh:
        fh.write(common.make_report(result))

    # Save metrics
    metrics = result.metrics | {"score": result.score} | {"task_name": result.task_name}
    print(metrics)
    print(f"Writing results to {result_filename}")
    with open(result_filename, "w") as f:
        f.write(json.dumps(metrics, indent=2))


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
