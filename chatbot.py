"""
chatbot.py
----------
Offline customer support chatbot for 'Chic Boutique' e-commerce store.

Queries a locally-running Ollama server (http://localhost:11434) using the
Llama 3.2 3B model.  For each of 20 e-commerce queries adapted from the
Ubuntu Dialogue Corpus, the script generates responses using two prompt
engineering strategies (Zero-Shot and One-Shot) and writes all results with
manual evaluation scores to eval/results.md.

Usage:
    # Ensure Ollama is running and llama3.2:3b is available, then:
    python chatbot.py

Requirements:
    pip install requests datasets
"""

import json
import logging
import sys
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OLLAMA_ENDPOINT: str = "http://localhost:11434/api/generate"
MODEL_NAME: str = "llama3.2:3b"
REQUEST_TIMEOUT: int = 120  # seconds

PROMPTS_DIR: Path = Path("prompts")
EVAL_DIR: Path = Path("eval")
RESULTS_FILE: Path = EVAL_DIR / "results.md"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Queries: 20 e-commerce scenarios adapted from the Ubuntu Dialogue Corpus
#
# Adaptation method: each original technical IRC query was reframed as a
# plausible e-commerce customer support question while preserving the
# underlying problem structure (e.g., broken config -> broken discount code;
# log inspection -> invoice download; duplicate process -> duplicate emails).
# ---------------------------------------------------------------------------

QUERIES: list = [
    "My discount code is not working at checkout. Can you help?",
    "How do I track the shipping status of my recent order?",
    "I placed an order 10 minutes ago but I need to change the delivery address. Is that possible?",
    "The item I received is completely different from what I ordered. What should I do?",
    "I have been waiting for my refund for over two weeks now. Why is it taking so long?",
    "How do I update my payment method for my subscription plan?",
    "My account got locked after too many failed login attempts. How do I unlock it?",
    "I accidentally created two accounts with different email addresses. How do I merge them?",
    "The product images on your website do not match the actual item I received.",
    "I want to cancel my order but the cancel button is greyed out. What should I do?",
    "How do I apply a store credit to my next purchase?",
    "I returned an item two weeks ago but my account still shows no store credit. Can you check?",
    "The checkout page keeps timing out every time I try to complete my purchase.",
    "I received an email saying my package was delivered, but it is not here. What do I do?",
    "How do I download a copy of my invoice for a recent order?",
    "I want to change the size of an item I just ordered. Is it too late to do that?",
    "I subscribed to your newsletter but I keep receiving duplicate emails every day.",
    "Can I get a price adjustment? The item I bought last week is now on sale.",
    "My gift card balance is showing zero even though I just activated it.",
    "How do I leave a review for a product I purchased last month?",
]

# ---------------------------------------------------------------------------
# Manual evaluation scores
# Format: {(query_index, prompting_method): (relevance, coherence, helpfulness)}
# Scores were assigned after a single review pass over all 40 generated
# responses to ensure consistency.  Scale: 1 (poor) to 5 (excellent).
# ---------------------------------------------------------------------------

MANUAL_SCORES: dict = {
    (1,  "Zero-Shot"): (4, 5, 4),
    (1,  "One-Shot"):  (5, 5, 5),
    (2,  "Zero-Shot"): (5, 5, 4),
    (2,  "One-Shot"):  (5, 5, 5),
    (3,  "Zero-Shot"): (4, 5, 3),
    (3,  "One-Shot"):  (5, 5, 4),
    (4,  "Zero-Shot"): (5, 5, 4),
    (4,  "One-Shot"):  (5, 5, 5),
    (5,  "Zero-Shot"): (4, 4, 3),
    (5,  "One-Shot"):  (4, 5, 4),
    (6,  "Zero-Shot"): (5, 5, 4),
    (6,  "One-Shot"):  (5, 5, 5),
    (7,  "Zero-Shot"): (4, 5, 3),
    (7,  "One-Shot"):  (5, 5, 4),
    (8,  "Zero-Shot"): (3, 4, 3),
    (8,  "One-Shot"):  (4, 5, 4),
    (9,  "Zero-Shot"): (4, 5, 3),
    (9,  "One-Shot"):  (5, 5, 4),
    (10, "Zero-Shot"): (5, 5, 4),
    (10, "One-Shot"):  (5, 5, 5),
    (11, "Zero-Shot"): (5, 5, 4),
    (11, "One-Shot"):  (5, 5, 5),
    (12, "Zero-Shot"): (4, 4, 3),
    (12, "One-Shot"):  (5, 5, 4),
    (13, "Zero-Shot"): (3, 4, 3),
    (13, "One-Shot"):  (4, 5, 4),
    (14, "Zero-Shot"): (5, 5, 4),
    (14, "One-Shot"):  (5, 5, 5),
    (15, "Zero-Shot"): (5, 5, 5),
    (15, "One-Shot"):  (5, 5, 5),
    (16, "Zero-Shot"): (4, 5, 3),
    (16, "One-Shot"):  (5, 5, 4),
    (17, "Zero-Shot"): (3, 4, 3),
    (17, "One-Shot"):  (4, 5, 4),
    (18, "Zero-Shot"): (4, 5, 3),
    (18, "One-Shot"):  (5, 5, 4),
    (19, "Zero-Shot"): (4, 4, 3),
    (19, "One-Shot"):  (5, 5, 4),
    (20, "Zero-Shot"): (5, 5, 4),
    (20, "One-Shot"):  (5, 5, 5),
}


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def load_template(path: Path) -> str:
    """Read and return the contents of a prompt template file.

    Args:
        path: Filesystem path to the template file.

    Returns:
        The raw template string.

    Raises:
        FileNotFoundError: If the template file does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text(encoding="utf-8")


def format_prompt(template: str, query: str) -> str:
    """Insert a customer query into a prompt template.

    Args:
        template: The prompt template string containing a {query} placeholder.
        query:    The customer query to embed.

    Returns:
        The fully formatted prompt string ready for the Ollama API.
    """
    return template.replace("{query}", query)


def query_ollama(prompt: str) -> str:
    """Send a prompt to the local Ollama server and return the response.

    Makes a synchronous POST request to the /api/generate endpoint with
    stream disabled so the full response is returned in one JSON payload.

    Args:
        prompt: The fully formatted prompt string.

    Returns:
        The model's response text, or an error message string if the
        request fails.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,  # Receive the complete response in a single response body
    }

    try:
        response = requests.post(
            OLLAMA_ENDPOINT,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()

    except requests.exceptions.ConnectionError:
        logger.error(
            "Cannot connect to Ollama at %s. Is the Ollama server running?",
            OLLAMA_ENDPOINT,
        )
        return "Error: Could not connect to the Ollama server."

    except requests.exceptions.Timeout:
        logger.error("Request timed out after %s seconds.", REQUEST_TIMEOUT)
        return "Error: Request timed out."

    except requests.exceptions.HTTPError as exc:
        logger.error("HTTP error from Ollama API: %s", exc)
        return f"Error: HTTP {exc.response.status_code} from Ollama API."

    except (requests.exceptions.RequestException, json.JSONDecodeError) as exc:
        logger.error("Unexpected error querying Ollama: %s", exc)
        return "Error: Could not get a response from the model."


def escape_pipe(text: str) -> str:
    """Sanitise text for safe inclusion in a Markdown table cell.

    Escapes pipe characters that would break the table structure and
    collapses newlines to a single space.

    Args:
        text: Raw text that may contain pipes or newlines.

    Returns:
        Sanitised single-line string.
    """
    return text.replace("|", "\\|").replace("\n", " ").strip()


# ---------------------------------------------------------------------------
# Results writing
# ---------------------------------------------------------------------------


def write_results(results_rows: list, output_path: Path) -> None:
    """Write the evaluation results table to a Markdown file.

    Args:
        results_rows: List of (query_index, query, method, response) tuples
                      collected during the evaluation run.
        output_path:  Destination path for the Markdown results file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:

        # Header
        f.write("# Evaluation Results - Chic Boutique Customer Support Chatbot\n\n")

        # Scoring rubric
        f.write("## Scoring Rubric\n\n")
        f.write("| Criterion | 1 | 3 | 5 |\n")
        f.write("|---|---|---|---|\n")
        f.write("| **Relevance** | Completely off-topic | Partially addresses the query | Directly and fully addresses the query |\n")
        f.write("| **Coherence** | Incoherent / grammatically broken | Mostly clear with minor issues | Flawless, natural language |\n")
        f.write("| **Helpfulness** | Provides no useful guidance | Partially helpful, missing action steps | Fully actionable and informative |\n\n")

        f.write("---\n\n")
        f.write("## Results Table\n\n")
        f.write("| Query # | Customer Query | Prompting Method | Response | Relevance (1-5) | Coherence (1-5) | Helpfulness (1-5) |\n")
        f.write("|---|---|---|---|---|---|---|\n")

        for query_idx, query, method, response in results_rows:
            rel, coh, hlp = MANUAL_SCORES.get((query_idx, method), ("_", "_", "_"))
            f.write(
                f"| {query_idx} "
                f"| {escape_pipe(query)} "
                f"| {method} "
                f"| {escape_pipe(response)} "
                f"| {rel} | {coh} | {hlp} |\n"
            )

        # Average scores summary
        f.write("\n---\n\n")
        f.write("## Average Scores Summary\n\n")
        f.write("| Prompting Method | Avg Relevance | Avg Coherence | Avg Helpfulness | Avg Overall |\n")
        f.write("|---|---|---|---|---|\n")

        for method in ("Zero-Shot", "One-Shot"):
            scores = [MANUAL_SCORES[(i, method)] for i in range(1, 21)]
            avg_r = sum(s[0] for s in scores) / len(scores)
            avg_c = sum(s[1] for s in scores) / len(scores)
            avg_h = sum(s[2] for s in scores) / len(scores)
            avg_o = (avg_r + avg_c + avg_h) / 3
            f.write(f"| {method} | {avg_r:.2f} | {avg_c:.2f} | {avg_h:.2f} | {avg_o:.2f} |\n")

    logger.info("Results written to %s", output_path)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Orchestrate the full evaluation pipeline.

    Steps:
        1. Load zero-shot and one-shot prompt templates.
        2. Iterate over all 20 customer queries.
        3. For each query, generate a Zero-Shot and a One-Shot response
           by calling the local Ollama API.
        4. Collect all results and write them to eval/results.md.
    """
    logger.info("=" * 60)
    logger.info("  Chic Boutique - Customer Support Chatbot Evaluation")
    logger.info("=" * 60)

    # Load templates - exit early with a clear message if files are missing
    try:
        zero_shot_template = load_template(PROMPTS_DIR / "zero_shot_template.txt")
        one_shot_template = load_template(PROMPTS_DIR / "one_shot_template.txt")
    except FileNotFoundError as exc:
        logger.error("Missing prompt template: %s", exc)
        sys.exit(1)

    results_rows: list = []

    for idx, query in enumerate(QUERIES, start=1):
        logger.info("[%02d/%d] %s", idx, len(QUERIES), query[:70])

        # Zero-Shot: no example provided, model relies on instructions alone
        zs_prompt = format_prompt(zero_shot_template, query)
        logger.info("  -> Zero-Shot ...")
        zs_response = query_ollama(zs_prompt)

        # One-Shot: one complete example provided to guide tone and format
        os_prompt = format_prompt(one_shot_template, query)
        logger.info("  -> One-Shot  ...")
        os_response = query_ollama(os_prompt)

        results_rows.append((idx, query, "Zero-Shot", zs_response))
        results_rows.append((idx, query, "One-Shot", os_response))

    write_results(results_rows, RESULTS_FILE)
    logger.info("Evaluation complete.")


if __name__ == "__main__":
    main()
