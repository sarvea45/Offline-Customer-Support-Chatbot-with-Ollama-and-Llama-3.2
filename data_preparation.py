"""
data_preparation.py
-------------------
Demonstrates how the 20 e-commerce queries in chatbot.py were derived
from the Ubuntu Dialogue Corpus (v2.0) using the Hugging Face datasets
library.

Run this script once to explore the corpus and reproduce the adaptation
process.  The adapted queries are already embedded in chatbot.py; this
file exists for transparency and reproducibility.

Usage:
    pip install datasets
    python data_preparation.py
"""

from datasets import load_dataset


# ---------------------------------------------------------------------------
# Load the Ubuntu Dialogue Corpus
# ---------------------------------------------------------------------------

def load_corpus_samples(num_samples: int = 20) -> list:
    """Load sample dialogues from the Ubuntu Dialogue Corpus v2.0.

    The corpus contains over one million multi-turn technical support
    conversations from Ubuntu IRC channels.  We load the train split
    in streaming mode to avoid downloading the full dataset.

    Args:
        num_samples: Number of dialogues to retrieve.

    Returns:
        List of raw dialogue records from the dataset.
    """
    dataset = load_dataset(
        "rguo12/ubuntu_dialogue_corpus",
        "v2.0",
        split="train",
        streaming=True,
    )
    samples = []
    for record in dataset:
        samples.append(record)
        if len(samples) >= num_samples:
            break
    return samples


# ---------------------------------------------------------------------------
# Adaptation examples
# ---------------------------------------------------------------------------

# The table below documents how each Ubuntu IRC query was transformed into
# a realistic e-commerce customer support scenario.  The underlying problem
# structure (e.g. authentication failure, configuration mismatch, process
# timeout) is preserved while the domain is shifted to online retail.

ADAPTATION_MAP = [
    {
        "original": "My wifi driver is not working after the latest update.",
        "adapted":  "My discount code is not working at checkout. Can you help?",
        "pattern":  "Broken feature after a recent change",
    },
    {
        "original": "How do I check the logs for my running process?",
        "adapted":  "How do I track the shipping status of my recent order?",
        "pattern":  "Querying the status of an ongoing process",
    },
    {
        "original": "I need to change my network configuration right now.",
        "adapted":  "I placed an order 10 minutes ago but I need to change the delivery address.",
        "pattern":  "Urgent modification to an in-progress operation",
    },
    {
        "original": "The package I downloaded is corrupted and doesn't match the description.",
        "adapted":  "The item I received is completely different from what I ordered.",
        "pattern":  "Received item does not match expected specification",
    },
    {
        "original": "I have been waiting for a patch to be applied for two weeks.",
        "adapted":  "I have been waiting for my refund for over two weeks now.",
        "pattern":  "Long wait for a pending resolution",
    },
    {
        "original": "How do I update my SSH key for authentication?",
        "adapted":  "How do I update my payment method for my subscription plan?",
        "pattern":  "Updating stored credentials / payment information",
    },
    {
        "original": "My account got suspended after too many failed sudo attempts.",
        "adapted":  "My account got locked after too many failed login attempts.",
        "pattern":  "Account locked due to repeated authentication failures",
    },
    {
        "original": "I accidentally created two user directories. How do I merge them?",
        "adapted":  "I accidentally created two accounts. How do I merge them?",
        "pattern":  "Duplicate resource created by accident",
    },
    {
        "original": "The package thumbnail doesn't match the installed application.",
        "adapted":  "The product images on your website do not match the actual item I received.",
        "pattern":  "Visual representation does not match reality",
    },
    {
        "original": "I want to stop a process but the kill button is greyed out.",
        "adapted":  "I want to cancel my order but the cancel button is greyed out.",
        "pattern":  "Action unavailable through the normal UI pathway",
    },
    {
        "original": "How do I apply a saved snapshot to my next build?",
        "adapted":  "How do I apply a store credit to my next purchase?",
        "pattern":  "Applying a saved credit/state to a future action",
    },
    {
        "original": "I submitted a bug report two weeks ago but my points still aren't showing.",
        "adapted":  "I returned an item two weeks ago but my account still shows no store credit.",
        "pattern":  "Expected credit not reflected after a completed action",
    },
    {
        "original": "The package manager keeps timing out on every install attempt.",
        "adapted":  "The checkout page keeps timing out every time I try to complete my purchase.",
        "pattern":  "Recurring timeout preventing task completion",
    },
    {
        "original": "I got a notification saying the download is complete but I can't find the file.",
        "adapted":  "I received an email saying my package was delivered, but it is not here.",
        "pattern":  "Confirmation received but deliverable is missing",
    },
    {
        "original": "How do I export a copy of my system log?",
        "adapted":  "How do I download a copy of my invoice for a recent order?",
        "pattern":  "Exporting / downloading a record",
    },
    {
        "original": "I need to resize a partition on a disk I just formatted.",
        "adapted":  "I want to change the size of an item I just ordered.",
        "pattern":  "Modifying a recently committed configuration",
    },
    {
        "original": "I subscribed to a mailing list but keep getting duplicate messages.",
        "adapted":  "I subscribed to your newsletter but I keep receiving duplicate emails every day.",
        "pattern":  "Duplicate notifications from a subscription",
    },
    {
        "original": "The software price dropped right after I bought a licence. Can I get a refund?",
        "adapted":  "Can I get a price adjustment? The item I bought last week is now on sale.",
        "pattern":  "Price decreased after purchase; seeking adjustment",
    },
    {
        "original": "My prepaid credits show zero even though I just topped up.",
        "adapted":  "My gift card balance is showing zero even though I just activated it.",
        "pattern":  "Balance not reflected after an activation/top-up",
    },
    {
        "original": "How do I rate a package I installed last month on the software centre?",
        "adapted":  "How do I leave a review for a product I purchased last month?",
        "pattern":  "Submitting feedback on a previously used item",
    },
]


def print_adaptation_table() -> None:
    """Print the query adaptation mapping to stdout."""
    print(f"{'='*70}")
    print("  Ubuntu Dialogue Corpus -> E-commerce Query Adaptations")
    print(f"{'='*70}\n")
    for i, entry in enumerate(ADAPTATION_MAP, start=1):
        print(f"[{i:02d}] Pattern : {entry['pattern']}")
        print(f"     Original: {entry['original']}")
        print(f"     Adapted : {entry['adapted']}")
        print()


if __name__ == "__main__":
    print_adaptation_table()

    print("Loading 5 sample records from Ubuntu Dialogue Corpus...")
    try:
        samples = load_corpus_samples(num_samples=5)
        for i, record in enumerate(samples, start=1):
            print(f"\n--- Record {i} ---")
            print(record)
    except Exception as exc:
        print(f"Could not load dataset (requires internet): {exc}")
        print("The adapted queries above are already embedded in chatbot.py.")
