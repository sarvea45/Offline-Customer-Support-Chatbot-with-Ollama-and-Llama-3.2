# Setup Guide – Chic Boutique Customer Support Chatbot

This guide walks you through installing all dependencies and running the chatbot evaluation script on your local machine. No internet connection is required once setup is complete.

---

## Prerequisites

| Requirement | Minimum Version | Notes |
|---|---|---|
| Operating System | macOS 12 / Ubuntu 20.04 / Windows 10 | 64-bit required |
| RAM | 8 GB | 16 GB recommended for smooth inference |
| Disk Space | ~3 GB free | For the Llama 3.2 3B model weights |
| Python | 3.9+ | Check with `python3 --version` |
| Git | Any recent version | For cloning the repo |

---

## Step 1 – Install Ollama

Ollama is the local LLM runtime that serves the Llama 3.2 model.

**macOS / Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**  
Download the installer from [https://ollama.com/download](https://ollama.com/download) and run it.

Verify the installation:
```bash
ollama --version
```

---

## Step 2 – Pull the Llama 3.2 3B Model

This downloads approximately 2 GB of model weights to your local machine.

```bash
ollama pull llama3.2:3b
```

Confirm the model is available:
```bash
ollama list
```

You should see `llama3.2:3b` in the output.

---

## Step 3 – Start the Ollama Server

On **macOS / Windows**, Ollama starts automatically and appears as an icon in the menu bar / system tray.

On **Linux**, start it manually if it isn't already running:
```bash
ollama serve
```

Verify the server is up by opening your browser and visiting:  
`http://localhost:11434`  
You should see: `Ollama is running`

---

## Step 4 – Clone the Repository

```bash
git clone https://github.com/<your-username>/chic-boutique-chatbot.git
cd chic-boutique-chatbot
```

---

## Step 5 – Set Up the Python Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
# macOS / Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install requests datasets
```

---

## Step 6 – Run the Chatbot Evaluation Script

Make sure the Ollama server is running (Step 3), then execute:

```bash
python chatbot.py
```

The script will:
1. Load both prompt templates from `prompts/`
2. Loop through 20 e-commerce queries
3. Generate a **Zero-Shot** and a **One-Shot** response for each
4. Write all results and scores to `eval/results.md`

Expected runtime: **5–20 minutes** depending on your CPU.

---

## Project Structure

```
chic-boutique-chatbot/
├── chatbot.py               # Main evaluation script
├── data_preparation.py      # Dataset loading & query adaptation documentation
├── setup.md                 # This file
├── report.md                # Analysis report
├── README.md                # Project overview
├── prompts/
│   ├── zero_shot_template.txt
│   └── one_shot_template.txt
└── eval/
    └── results.md           # Generated output + scores
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `Connection refused` on port 11434 | Run `ollama serve` in a separate terminal |
| Responses are very slow | Expected on CPU; each response may take 10–30 seconds |
| `ModuleNotFoundError: requests` | Run `pip install requests datasets` inside your venv |
| Model not found error | Run `ollama pull llama3.2:3b` again |

---

## FAQ

**Q: The Ollama server isn't responding or I'm getting a connection error.**

A: First, ensure the Ollama application is running. On macOS and Windows, it should appear as an icon in your menu bar or system tray. On Linux, it runs as a background service. You can check its status with:

```bash
systemctl --user status ollama
```

Second, confirm that you are sending requests to the correct address, which is `http://localhost:11434` by default.

---

**Q: The model's responses are very slow. Is this normal?**

A: Yes, this is expected when running an LLM on a CPU. Unlike powerful cloud servers with multiple GPUs, your local machine's CPU will take several seconds to generate a response. The performance depends heavily on your computer's hardware. This is one of the key trade-offs of running models locally.

---

**Q: How should I choose a good example for my one-shot prompt?**

A: A good one-shot example should be representative of the ideal output you want. It should be clear, concise, and have the desired tone (e.g., friendly and professional). Choose a common, straightforward query-response pair, like the return policy example provided. Avoid using a complex or ambiguous example, as it might confuse the model.

---

**Q: Can I use a different model, like Mistral 7B or Phi-3 Mini?**

A: Absolutely. Ollama supports a wide range of open-source models. You can explore them on the [Ollama library page](https://ollama.com/library). To use a different model, first run:

```bash
ollama pull <model_name>
```

Then change the `MODEL_NAME` constant at the top of `chatbot.py` to match. Comparing different models would be an excellent extension to this project.
