import asyncio
import math
import os
import jinja2
from collections import defaultdict
from pathlib import Path
from typing import Any
import numpy as np
from tqdm import tqdm
from tqdm.asyncio import tqdm
import yaml

from simple_evals.simple_evals_types import (EvalResult, Message, SamplerBase,
                                             SingleEvalResult)
from simple_evals.sampler.chat_completion_sampler import OPENAI_SYSTEM_MESSAGE_CHATGPT
from simple_evals.diskcaching import Cache

QUERY_TEMPLATE_MULTICHOICE = """
Answer the following multiple choice question. The last line of your response should be of the following format: 'Answer: $LETTER' (without quotes) where LETTER is one of ABCD. Think step by step before answering.

{Question}

A) {A}
B) {B}
C) {C}
D) {D}
""".strip()

ANSWER_PATTERN_MULTICHOICE = r"(?i)Answer[ \t]*:[ \t]*([A-D])"
ANSWER_PATTERN = r"(?i)Answer\s*:\s*([^\n]+)"
MULTILINGUAL_ANSWER_PATTERN_TEMPLATE = (
    "(?i){}\s*([A-D]|[أ-د]|[অ]|[ব]|[ড]|[ঢ]|[Ａ]|[Ｂ]|[Ｃ]|[Ｄ])"
)
# All the different ways "Answer" is written in different languages
MULTILINGUAL_ANSWER_REGEXES = [
    "Answer\s*:",
    "Answer\s*:​​​​​​",  # Korean invisible character
    "উত্তর\s*:",
    "उत्तर\s*:",
    "উত্তরঃ",
    "উত্তর\s*:",
    "Antwort\s*:",
    "답변\s*:",
    "정답\s*:",
    "답\s*:",
    "答案\s*：",
    "答案\s*:",
    "答\s*：",
    "答\s*:",
    "答复\s*：",
    "答曰\s*：",
    "الإجابة:",
    "الجواب:",
    "إجابة:",
    "الإجابة النهائية:",
    "الإجابة الصحيحة:",
    "الإجابة الصحيحة هي:",
    "الإجابة هي:",
    "Respuesta\s*:",
    "Risposta\s*:",
    "答え\s*:",
    "答え\s*：",
    "回答\s*:",
    "回答\s*：",
    "解答\s*:",
    "Jawaban\s*:",
    "Réponse\s*:",
    "Resposta\s*:",
    "Jibu\s*:",
    "Idahun\s*:",
    "Ìdáhùn\s*:",
    "Idáhùn\s*:",
    "Àmọ̀nà\s*:",
    "Àdáhùn\s*:",
    "Ànúgọ\s*:",
    "Àṣàyàn\s*:",
]


EQUALITY_TEMPLATE = r"""
Look at the following two expressions (answers to a math problem) and judge whether they are equivalent. Only perform trivial simplifications

Examples:

    Expression 1: $2x+3$
    Expression 2: $3+2x$

Yes

    Expression 1: 3/2
    Expression 2: 1.5

Yes

    Expression 1: $x^2+2x+1$
    Expression 2: $y^2+2y+1$

No

    Expression 1: $x^2+2x+1$
    Expression 2: $(x+1)^2$

Yes

    Expression 1: 3245/5
    Expression 2: 649

No
(these are actually equal, don't mark them equivalent if you need to do nontrivial simplifications)

    Expression 1: 2/(-3)
    Expression 2: -2/3

Yes
(trivial simplifications are allowed)

    Expression 1: 72 degrees
    Expression 2: 72

Yes
(give benefit of the doubt to units)

    Expression 1: 64
    Expression 2: 64 square feet

Yes
(give benefit of the doubt to units)

---

YOUR TASK


Respond with only "Yes" or "No" (without quotes). Do not include a rationale.

    Expression 1: %(expression1)s
    Expression 2: %(expression2)s
""".strip()


HTML_JINJA = """
<h3>Prompt conversation</h3>
{% for message in prompt_messages %}
{{ message_to_html(message) | safe }}
{% endfor %}
<h3>Sampled message</h3>
{{ message_to_html(next_message) | safe }}
<h3>Results</h3>
<p>Correct Answer: {{ correct_answer }}</p>
<p>Extracted Answer: {{ extracted_answer }}</p>
<p>Score: {{ score }}</p>
"""


def format_multichoice_question(row):
    return QUERY_TEMPLATE_MULTICHOICE.format(**row)


async def check_equality(sampler, correct_answer: str, extracted_answer: str, use_sympy: bool = False) -> bool:
    if extracted_answer is None:
        return False
        
    # If use_sympy is True, try sympy first
    if use_sympy:
        from simple_evals.evals.math_grading.sympy_grader import grade_answer
        sympy_result = grade_answer(extracted_answer, correct_answer)
        if sympy_result:
            return True
    
    # In all other cases, use the sampler
    messages = [
        dict(
            role="user",
            content=EQUALITY_TEMPLATE % {
                "expression1": correct_answer,
                "expression2": extracted_answer
            }
        ),
    ]
    response = await sampler(messages)
    return response.strip().lower() == "yes"


def mean(arr):
    return sum(arr) / len(arr)


def sample_stddev(arr):
    """Calculate sample standard deviation."""
    # With downsampling, we can end up with a single example in the dataset.
    if len(arr) <= 1:
        return 0.0  # Return 0 for single sample or empty array
    mu = mean(arr)
    return math.sqrt(sum([(x - mu) ** 2 for x in arr]) / (len(arr) - 1))


def mean_stderr(arr):
    """Calculate standard error of the mean."""
    # With downsampling, we can end up with a single example in the dataset.
    if len(arr) <= 1:
        return 0.0  # Return 0 for single sample or empty array
    return sample_stddev(arr) / math.sqrt(len(arr))


def _compute_stat(values: list, stat: str):
    if stat == "mean":
        return np.mean(values)
    elif stat == "std":
        return np.std(values)
    elif stat == "stderr":
        return mean_stderr(values)
    elif stat == "min":
        return np.min(values)
    elif stat == "max":
        return np.max(values)
    else:
        raise ValueError(f"Unknown {stat =}")


def aggregate_results(
    single_eval_results: list[SingleEvalResult],
    task_name: str,
    default_stats: tuple[str] = ("mean", "std", "stderr"),
    name2stats: dict[str, tuple[str]] | None = None,
    add_macro: bool = False
) -> EvalResult:
    """
    Aggregate results from multiple evaluations into a single EvalResult.
    """
    name2stats = name2stats or {}
    name2values = defaultdict(list)
    htmls = []
    convos = []

    # Collect metrics and other data from evaluations
    for single_eval_result in single_eval_results:
        for name, value in single_eval_result.metrics.items():
            name2values[name].append(value)
        if single_eval_result.score is not None:
            name2values["score"].append(single_eval_result.score)
        htmls.append(single_eval_result.html)
        convos.append(single_eval_result.convo)

    # Compute statistics for each metric
    final_metrics = {}
    for name, values in name2values.items():
        stats = name2stats.get(name, default_stats)
        for stat in stats:
            key = name if stat == "mean" else f"{name}:{stat}"
            final_metrics[key] = _compute_stat(values, stat)

    # Add macro statistics if required
    if add_macro:
        macro_values = []
        for name, values in name2values.items():
            # Exclude metrics that start with "score"
            if not name.startswith("score"):
                macro_values.append(_compute_stat(values, "mean"))

        key = "score_macro"
        final_metrics[key] = _compute_stat(macro_values, "mean")

    return EvalResult(
        task_name=task_name,
        score=final_metrics.pop("score", None),
        metrics=final_metrics,
        htmls=htmls,
        convos=convos,
    )


async def map_with_progress(
    func: callable,
    items: list,
    num_threads: int = 10,
    cache_dir: str = "cache.sqlite",
    first_n: int | float | None = None,
):
    """
    Asynchronously apply a function to each element of a list with progress tracking and SqliteDict caching.

    Parameters:
    - func: Callable function to apply to each element.
    - items: List of inputs to process.
    - seed_generator: SeedGenerator instance for deterministic seeding
    - num_threads: Number of concurrent tasks.
    - cache_dir: Path to the SQLite database file for caching.
    - first_n: Limit the number of items to process (None for all). If a float is provided, it will be interpreted as a percentage of the total number of examples.

    Returns:
    - List of results.
    """
    if first_n is not None:
        if isinstance(first_n, float):
            first_n = int(len(items) * first_n)
        items = items[:first_n]

    semaphore = asyncio.Semaphore(num_threads)

    os.makedirs(cache_dir, exist_ok=True)
    cache_file = Path(cache_dir) / "cache.sqlite"
    
    if cache_file.exists():
        print(f"Found existing cache at {cache_file}. Cached predictions will be loaded when available.")
    else:
        print(f"Creating new cache at {cache_file}")

    with Cache(cache_file) as cache:
        async def worker(idx, item):
            cache_key = f"{idx}"
            
            if cache_key in cache:
                return SingleEvalResult.from_dict(cache[cache_key])

            async with semaphore:
                result = await func(item, idx)
            
            cache[cache_key] = SingleEvalResult.to_dict(result)
            return result

        tasks = [worker(idx, item) for idx, item in enumerate(items)]
        results = [await result for result in tqdm(asyncio.as_completed(tasks), total=len(items))]
    return results


jinja_env = jinja2.Environment(
    loader=jinja2.BaseLoader(),
    undefined=jinja2.StrictUndefined,
    autoescape=jinja2.select_autoescape(["html", "xml"]),
)
_message_template = """
<div class="message {{ role }}">
    <div class="role">
    {{ role }} 
    {% if variant %}<span class="variant">({{ variant }})</span>{% endif %}
    </div>
    <div class="content">
    <pre>{{ content }}</pre>
    </div>
</div>
"""


def message_to_html(message: Message) -> str:
    """
    Generate HTML snippet (inside a <div>) for a message.
    """
    return jinja_env.from_string(_message_template).render(
        role=message["role"],
        content=message["content"],
        variant=message.get("variant", None),
    )


jinja_env.globals["message_to_html"] = message_to_html


_report_template = """<!DOCTYPE html>
<html>
    <head>
        <style>
            .message {
                padding: 8px 16px;
                margin-bottom: 8px;
                border-radius: 4px;
            }
            .message.user {
                background-color: #B2DFDB;
                color: #00695C;
            }
            .message.assistant {
                background-color: #B39DDB;
                color: #4527A0;
            }
            .message.system {
                background-color: #EEEEEE;
                color: #212121;
            }
            .role {
                font-weight: bold;
                margin-bottom: 4px;
            }
            .variant {
                color: #795548;
            }
            table, th, td {
                border: 1px solid black;
            }
            pre {
                white-space: pre-wrap;
            }
        </style>
    </head>
    <body>
    {% if metrics %}
    <h1>Metrics</h1>
    <table>
    <tr>
        <th>Metric</th>
        <th>Value</th>
    </tr>
    <tr>
        <td><b>Score</b></td>
        <td>{{ score | float | round(3) }}</td>
    </tr>
    {% for name, value in metrics.items() %}
    <tr>
        <td>{{ name }}</td>
        <td>{{ value }}</td>
    </tr>
    {% endfor %}
    </table>
    {% endif %}
    <h1>Examples</h1>
    {% for html in htmls %}
    {{ html | safe }}
    <hr>
    {% endfor %}
    </body>
</html>
"""


def make_report(eval_result: EvalResult) -> str:
    """
    Create a standalone HTML report from an EvalResult.
    """
    return jinja_env.from_string(_report_template).render(
        score=eval_result.score,
        metrics=eval_result.metrics,
        htmls=eval_result.htmls,
    )


def make_report_from_example_htmls(htmls: list[str]):
    """
    Create a standalone HTML report from a list of example htmls
    """
    return jinja_env.from_string(_report_template).render(
        score=None, metrics={}, htmls=htmls
    )


def normalize_response(response: str) -> str:
    """
    Normalize the response by removing markdown and LaTeX formatting that may prevent a match.
    """

    return (
        response.replace("**", "")
        .replace("$\\boxed{", "")
        .replace("}$", "")
        .replace("\\$", "")
        .replace("$\\text{", "")
        .replace("$", "")
        .replace("\\mathrm{", "")
        .replace("\\{", "")
        .replace("\\text", "")
        .replace("\\(", "")
        .replace("\\mathbf{", "")
        .replace("{", "")
        .replace("\\boxed", "")
    )


def normalize_extracted_answer(extracted_answer: str) -> str:
    return (
        # In arabic these are the letters used for A-D in multiple choice questions
        extracted_answer.replace("أ", " A")
        .replace("ب", " B")
        .replace("ج", " C")
        .replace("د", " D")
        # In Bengali these are the letters used for A-D in multiple choice questions
        .replace("অ", " A")
        .replace("ব", " B")
        .replace("ড", " C")
        .replace("ঢ", " D")
        # In Japanese these are the letters sometimes used for A-D in multiple choice questions
        .replace("Ａ", " A")
        .replace("Ｂ", " B")
        .replace("Ｃ", " C")
        .replace("Ｄ", " D")
        .strip()
    )


def load_template(template_name: str) -> str:
    template_path = Path(__file__).parent / "configs" / "templates" / template_name
    with open(template_path, "r") as f:
        return f.read().strip()

def load_regex(regex_name: str) -> str:
    regex_path = Path(__file__).parent / "configs" / "regex" / regex_name
    with open(regex_path, "r") as f:
        return f.read().strip()

def load_task_config(eval_name: str) -> dict | None:
    config_path = Path(__file__).parent / "configs" / "tasks" / f"{eval_name}.yml"
    if config_path.exists():
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return None

def load_judge(judge_name: str) -> SamplerBase:
    """Load a judge configuration and instantiate the appropriate judge class."""
    from simple_evals.sampler.judge.gpt_judge import GPTJudge
    from simple_evals.sampler.chat_completion_sampler import ChatCompletionSampler
    
    print(f"Loading judge configuration for: {judge_name}")
    
    # Change this to look directly in the judge config directory
    config_path = Path(__file__).parent / "configs" / "judge" / f"{judge_name}.yaml"
    if not config_path.exists():
        raise ValueError(f"No configuration found for judge at: {config_path}")
        
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        
    # Extract common parameters
    judge_params = {
        "model": config.get("model", "gpt-4"),
        "timeout": config.get("timeout", 60),
        "max_retries": config.get("max_retries", 16),
        "temperature": config.get("temperature", 0.5),
        "top_p": config.get("top_p", 0.9),
        "max_tokens": config.get("max_tokens", 1024),
    }
    
    # For GPT judges, add rate limiting
    if judge_name.startswith("gpt"):
        return GPTJudge(**judge_params, url=os.environ.get("OPENAI_MODEL_URL", "https://prod.api.nvidia.com/llm/v1/azure/"))
    else:
        # For other judges, use base ChatCompletionSampler
        api_key = os.environ.get("JUDGE_API_KEY")
        if api_key is None:
            raise ValueError("JUDGE_API_KEY environment variable must be set for non-GPT judges")
            
        judge_params["url"] = config.get("url", "https://integrate.api.nvidia.com/v1/chat/completions")
        return ChatCompletionSampler(**judge_params, system_message=None, api_key=api_key)
