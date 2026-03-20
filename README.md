# Chic Boutique – Offline Customer Support Chatbot

> An offline, privacy-first customer support chatbot powered by **Llama 3.2 3B** running locally via **Ollama**. No data leaves your machine.

---

## Overview

This project builds and evaluates a local LLM-based chatbot for a fictional e-commerce store, **Chic Boutique**. It compares two prompt engineering strategies — **Zero-Shot** and **One-Shot** — across 20 realistic customer support queries adapted from the Ubuntu Dialogue Corpus.

### Why Offline?

Cloud-based LLMs (OpenAI, Gemini, etc.) require sending customer data to third-party servers, creating legal and privacy risks under GDPR, CCPA, and India's DPDP Act 2023. Running the model entirely on local hardware eliminates these risks while retaining the power of modern AI.

---

## Quick Start

```bash
# 1. Install Ollama and pull the model
ollama pull llama3.2:3b

# 2. Clone this repo and set up Python
git clone https://github.com/<your-username>/chic-boutique-chatbot.git
cd chic-boutique-chatbot
python3 -m venv venv && source venv/bin/activate
pip install requests datasets

# 3. Run the evaluation
python chatbot.py
```

Full setup instructions are in [setup.md](setup.md).

---

## Project Structure

```
chic-boutique-chatbot/
├── chatbot.py                  # Main script: generates & logs all responses
├── setup.md                    # Detailed installation guide
├── report.md                   # Full analysis report with results & conclusions
├── README.md                   # This file
├── prompts/
│   ├── zero_shot_template.txt  # Prompt with no examples
│   └── one_shot_template.txt   # Prompt with one example Q&A pair
└── eval/
    └── results.md              # Generated results table with manual scores
```

---

## Key Findings

| Method | Avg Relevance | Avg Coherence | Avg Helpfulness | **Overall** |
|---|---|---|---|---|
| Zero-Shot | 4.20 | 4.65 | 3.50 | **4.12 / 5** |
| One-Shot | 4.80 | 5.00 | 4.45 | **4.75 / 5** |

- **One-Shot prompting outperforms Zero-Shot** across all three criteria, with the largest gain in **Helpfulness (+0.95)**.
- Llama 3.2 3B is capable of producing coherent, professional support responses entirely offline.
- The model generally avoids hallucinating specific policy details when instructed not to.

See [report.md](report.md) for the full analysis.

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM Runtime | [Ollama](https://ollama.com) |
| Model | Meta Llama 3.2 3B (quantized) |
| Language | Python 3.9+ |
| Query Source | [Ubuntu Dialogue Corpus v2.0](https://huggingface.co/datasets/rguo12/ubuntu_dialogue_corpus) |
| HTTP Client | `requests` |
| Dataset Loader | `datasets` (Hugging Face) |

---

## License

MIT
