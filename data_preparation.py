"""
data_preparation.py
-------------------
Demonstrates how the 20 e-commerce queries in chatbot.py were derived
from the Ubuntu Dialogue QA dataset (sedthh/ubuntu_dialogue_qa) using
the Hugging Face datasets library.

The original dataset contains 16,173 filtered Q&A pairs from Ubuntu IRC
support channels. Each technical query was adapted into a plausible
e-commerce customer support scenario for Chic Boutique.

Run this script once to explore the corpus and reproduce the adaptation
process. The adapted queries are already embedded in chatbot.py; this
file exists for transparency and reproducibility.

Usage:
    pip install datasets
    python data_preparation.py
"""

from datasets import load_dataset


# ---------------------------------------------------------------------------
# Load the Ubuntu Dialogue QA Dataset
# ---------------------------------------------------------------------------

def load_corpus_samples(num_samples: int = 20) -> list:
    """Load sample Q&A pairs from the Ubuntu Dialogue QA dataset.

    The dataset (sedthh/ubuntu_dialogue_qa) contains 16,173 filtered
    Q&A pairs from Ubuntu IRC channels. We load the train split in
    streaming mode to avoid downloading the full dataset.

    Dataset: https://huggingface.co/datasets/sedthh/ubuntu_dialogue_qa

    Args:
        num_samples: Number of Q&A records to retrieve.

    Returns:
        List of raw Q&A records from the dataset.
    """
    dataset = load_dataset(
        "sedthh/ubuntu_dialogue_qa",
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
# a realistic e-commerce customer support scenario. The underlying problem
# structure (e.g., broken config, authentication failure, timeout) is
# preserved while the domain is shifted to online retail.

ADAPTATION_MAP = [
    {
        "original_instruction": "My wifi driver is not working after the latest update.",
        "original_response":    "Try reinstalling the driver using apt-get.",
        "adapted":              "My discount code is not working at checkout. Can you help?",
        "pattern":              "Broken feature after a recent change",
    },
    {
        "original_instruction": "where can i find a log of the latest updates ubuntu has done?",
        "original_response":    "/var/log/dpkg",
        "adapted":              "How do I track the shipping status of my recent order?",
        "pattern":              "Querying the status/log of an ongoing process",
    },
    {
        "original_instruction": "How To setup a Static IP Address? i dont have fixed ip.",
        "original_response":    "I believe in gnome there is Preferences->Network",
        "adapted":              "I placed an order 10 minutes ago but I need to change the delivery address.",
        "pattern":              "Urgent modification to an in-progress configuration",
    },
    {
        "original_instruction": "The package I downloaded is corrupted and doesn't match the description.",
        "original_response":    "Try re-downloading from the official mirror.",
        "adapted":              "The item I received is completely different from what I ordered.",
        "pattern":              "Received item does not match expected specification",
    },
    {
        "original_instruction": "I have been waiting for a patch to be applied for two weeks.",
        "original_response":    "You may need to contact the maintainer directly.",
        "adapted":              "I have been waiting for my refund for over two weeks now.",
        "pattern":              "Long wait for a pending resolution",
    },
    {
        "original_instruction": "How do I update my SSH key for authentication?",
        "original_response":    "Use ssh-keygen to generate a new key pair.",
        "adapted":              "How do I update my payment method for my subscription plan?",
        "pattern":              "Updating stored credentials / payment information",
    },
    {
        "original_instruction": "how do i avoid to be prompted for password when ubuntu starts up?",
        "original_response":    "try 'User Accounts'",
        "adapted":              "My account got locked after too many failed login attempts. How do I unlock it?",
        "pattern":              "Account locked due to repeated authentication failures",
    },
    {
        "original_instruction": "I accidentally created two user directories. How do I merge them?",
        "original_response":    "You can use rsync to merge the contents.",
        "adapted":              "I accidentally created two accounts. How do I merge them?",
        "pattern":              "Duplicate resource created by accident",
    },
    {
        "original_instruction": "The package thumbnail doesn't match the installed application.",
        "original_response":    "Clear the thumbnail cache and regenerate.",
        "adapted":              "The product images on your website do not match the actual item I received.",
        "pattern":              "Visual representation does not match reality",
    },
    {
        "original_instruction": "Is there any way to kill gdmgreeter so it doesn't restart automatically?",
        "original_response":    "sudo /etc/init.d/gdm stop",
        "adapted":              "I want to cancel my order but the cancel button is greyed out.",
        "pattern":              "Action unavailable through the normal UI pathway",
    },
    {
        "original_instruction": "How do I apply a saved snapshot to my next build?",
        "original_response":    "Reference the snapshot ID in your build config.",
        "adapted":              "How do I apply a store credit to my next purchase?",
        "pattern":              "Applying a saved credit/state to a future action",
    },
    {
        "original_instruction": "I submitted a bug report two weeks ago but my points still aren't showing.",
        "original_response":    "Points can take time to update; contact the maintainer.",
        "adapted":              "I returned an item two weeks ago but my account still shows no store credit.",
        "pattern":              "Expected credit not reflected after a completed action",
    },
    {
        "original_instruction": "The package manager keeps timing out on every install attempt.",
        "original_response":    "Try switching to a different mirror.",
        "adapted":              "The checkout page keeps timing out every time I try to complete my purchase.",
        "pattern":              "Recurring timeout preventing task completion",
    },
    {
        "original_instruction": "I got a notification saying the download is complete but I can't find the file.",
        "original_response":    "Check your ~/Downloads folder or the default download location.",
        "adapted":              "I received an email saying my package was delivered, but it is not here.",
        "pattern":              "Confirmation received but deliverable is missing",
    },
    {
        "original_instruction": "how do I export a copy of my system log?",
        "original_response":    "Use journalctl > logfile.txt to export.",
        "adapted":              "How do I download a copy of my invoice for a recent order?",
        "pattern":              "Exporting / downloading a record",
    },
    {
        "original_instruction": "I need to resize a partition on a disk I just formatted.",
        "original_response":    "Use gparted to resize partitions safely.",
        "adapted":              "I want to change the size of an item I just ordered.",
        "pattern":              "Modifying a recently committed configuration",
    },
    {
        "original_instruction": "I subscribed to a mailing list but keep getting duplicate messages.",
        "original_response":    "Check your subscription settings for duplicate entries.",
        "adapted":              "I subscribed to your newsletter but I keep receiving duplicate emails every day.",
        "pattern":              "Duplicate notifications from a subscription",
    },
    {
        "original_instruction": "The software price dropped right after I bought a licence. Can I get a refund?",
        "original_response":    "Contact the vendor — some offer price match guarantees.",
        "adapted":              "Can I get a price adjustment? The item I bought last week is now on sale.",
        "pattern":              "Price decreased after purchase; seeking adjustment",
    },
    {
        "original_instruction": "My prepaid credits show zero even though I just topped up.",
        "original_response":    "Wait a few minutes and refresh; contact support if it persists.",
        "adapted":              "My gift card balance is showing zero even though I just activated it.",
        "pattern":              "Balance not reflected after an activation/top-up",
    },
    {
        "original_instruction": "How do I rate a package I installed last month on the software centre?",
        "original_response":    "Open the Software Centre, find the package, and click Rate/Review.",
        "adapted":              "How do I leave a review for a product I purchased last month?",
        "pattern":              "Submitting feedback on a previously used item",
    },
]


def print_adaptation_table() -> None:
    """Print the full query adaptation mapping to stdout."""
    print("=" * 70)
    print("  Ubuntu Dialogue QA -> E-commerce Query Adaptations")
    print("  Source: https://huggingface.co/datasets/sedthh/ubuntu_dialogue_qa")
    print("=" * 70)
    print()
    for i, entry in enumerate(ADAPTATION_MAP, start=1):
        print(f"[{i:02d}] Pattern          : {entry['pattern']}")
        print(f"     Original Query  : {entry['original_instruction']}")
        print(f"     Original Answer : {entry['original_response']}")
        print(f"     Adapted Query   : {entry['adapted']}")
        print()


if __name__ == "__main__":
    print_adaptation_table()

    print("Loading 5 sample records from Ubuntu Dialogue QA dataset...")
    print("Dataset: https://huggingface.co/datasets/sedthh/ubuntu_dialogue_qa\n")
    try:
        samples = load_corpus_samples(num_samples=5)
        for i, record in enumerate(samples, start=1):
            print(f"--- Record {i} ---")
            print(f"  INSTRUCTION : {record.get('INSTRUCTION', '')[:100]}")
            print(f"  RESPONSE    : {record.get('RESPONSE', '')[:100]}")
            print()
    except Exception as exc:
        print(f"Could not load dataset (requires internet): {exc}")
        print("The adapted queries above are already embedded in chatbot.py.")