# Report: Evaluating an Offline LLM for E-commerce Customer Support
### Comparing Zero-Shot vs. One-Shot Prompting with Llama 3.2 3B via Ollama

---

## 1. Introduction

The goal of this project was to evaluate the feasibility of using a locally-hosted Large Language Model (LLM) as a customer support chatbot for a fictional online fashion store, **Chic Boutique**. Operating entirely offline ensures that no sensitive customer data — such as order details, addresses, or account information — is transmitted to third-party cloud servers, making this approach compliant with data privacy regulations like GDPR, CCPA, and India's DPDP Act 2023.

The specific objectives were:

1. Deploy Meta's **Llama 3.2 3B** model locally using **Ollama**.
2. Design two distinct prompt engineering strategies — **Zero-Shot** and **One-Shot** — and compare their effectiveness.
3. Evaluate model responses across 20 realistic e-commerce customer queries on three criteria: **Relevance**, **Coherence**, and **Helpfulness**.
4. Draw conclusions about the practical viability of this approach and its limitations.

---

## 2. Methodology

### 2.1 Query Adaptation

Twenty customer queries were adapted from the **Ubuntu Dialogue Corpus (v2.0)**, a large dataset of technical IRC support conversations. Each technical query was reframed as a plausible e-commerce support inquiry. The adaptation preserved the underlying problem structure (e.g., a broken configuration → a broken discount code; a log-checking request → an invoice download request) to maintain the diversity of question types found in the original corpus.

**Examples of adaptations:**

| Original (Ubuntu/Technical) | Adapted (E-commerce / Chic Boutique) |
|---|---|
| "My wifi driver broke after an update." | "My discount code is not working at checkout." |
| "How do I check the Apache server logs?" | "How do I download a copy of my invoice?" |
| "I accidentally deleted my home directory." | "I accidentally created two accounts. How do I merge them?" |
| "The package manager keeps timing out." | "The checkout page keeps timing out on me." |

The 20 queries were designed to span the most common e-commerce support categories: order tracking, returns, payments, account management, delivery issues, and promotional codes.

### 2.2 Prompt Templates

Two prompt templates were created and stored in the `prompts/` directory.

**Zero-Shot Template** (`prompts/zero_shot_template.txt`):  
This template gives the model a detailed role description and behavioural guidelines (conciseness, tone, honesty about unknown policies), then presents the customer query directly. No example response is provided. The model must infer the desired output format entirely from the instructions.

**One-Shot Template** (`prompts/one_shot_template.txt`):  
This template contains the same role description and guidelines, but adds a single hardcoded example of a complete query-response pair (a return policy question) before the actual customer query. This example demonstrates the desired tone (warm, first-person, actionable), approximate length (~60–80 words), and the closing offer to help further.

### 2.3 Scoring Rubric

Each response was manually evaluated by the project author across three criteria, each scored on a 1–5 integer scale:

| Criterion | Score 1 | Score 3 | Score 5 |
|---|---|---|---|
| **Relevance** | Completely off-topic or addresses a different question | Partially addresses the query but misses key aspects | Directly, fully, and accurately addresses the query |
| **Coherence** | Incoherent, grammatically broken, or repetitive | Mostly clear with some awkward phrasing or minor errors | Flawless, natural, easy-to-read language |
| **Helpfulness** | Provides no useful guidance or actionable steps | Partially helpful but lacks clear next steps | Fully actionable, empowering the customer to resolve their issue |

Scores were assigned after all 40 responses had been generated, in a single review pass, to maintain consistency.

---

## 3. Results & Analysis

### 3.1 Quantitative Summary

The table below shows the average scores across all 20 queries for each prompting method.

| Prompting Method | Avg Relevance | Avg Coherence | Avg Helpfulness | **Avg Overall** |
|---|---|---|---|---|
| Zero-Shot | 4.20 | 4.65 | 3.50 | **4.12** |
| One-Shot | 4.80 | 5.00 | 4.45 | **4.75** |
| **Difference** | +0.60 | +0.35 | +0.95 | **+0.63** |

The One-Shot method outperformed Zero-Shot across all three criteria. The largest improvement was in **Helpfulness (+0.95)**, followed by **Relevance (+0.60)** and **Coherence (+0.35)**. This pattern makes intuitive sense: coherence is relatively easy for Llama 3.2 3B to achieve from instructions alone, but helpfulness — knowing *how* to structure an actionable answer — benefited most from having a concrete example to imitate.

### 3.2 Qualitative Analysis

#### 3.2.1 Cases Where One-Shot Clearly Outperformed Zero-Shot

**Query 8: "I accidentally created two accounts with different email addresses. How do I merge them?"**

- **Zero-Shot Response:** *"I'm sorry to hear that! Unfortunately, merging accounts isn't something I can do directly, but you may want to contact our support team for assistance with this issue."*  
  *Scores: Relevance 3 / Coherence 4 / Helpfulness 3*

- **One-Shot Response:** *"Hi! I completely understand how frustrating that can be. While account merging isn't available as a self-service option, our support team can handle this for you. Please email support@chicboutique.com with both account email addresses and they'll consolidate your order history and store credit. Happy to help with anything else!"*  
  *Scores: Relevance 4 / Coherence 5 / Helpfulness 4*

The One-Shot response is noticeably more empathetic, provides a concrete action step (contacting support with both emails), and closes with an offer to help — directly mirroring the structure of the example. The Zero-Shot response, while accurate, is vague and passive.

**Query 17: "I subscribed to your newsletter but I keep receiving duplicate emails every day."**

- **Zero-Shot Response:** *"I apologize for the inconvenience. This could be a technical issue on our end. Please unsubscribe and resubscribe to see if that resolves it."*  
  *Scores: Relevance 3 / Coherence 4 / Helpfulness 3*

- **One-Shot Response:** *"So sorry about that — duplicate emails are definitely annoying! It's possible your address was registered twice. Please check your account's Communication Preferences page to remove duplicates. If the issue persists after 24 hours, our support team can manually fix this for you. Is there anything else I can help with today?"*  
  *Scores: Relevance 4 / Coherence 5 / Helpfulness 4*

Again, the One-Shot response provides a specific actionable path and a follow-up escalation route, while the Zero-Shot response offers a generic workaround.

#### 3.2.2 Cases Where Both Methods Performed Well

**Query 15: "How do I download a copy of my invoice for a recent order?"**

Both methods scored 5/5/5. This query is clear and procedural, so even without an example, the model knew to provide step-by-step instructions. Both responses guided the user to the Order History page to download their invoice — a case where the instruction-only approach was sufficient.

#### 3.2.3 Cases Where Both Methods Struggled

**Query 19: "My gift card balance is showing zero even though I just activated it."**

- **Zero-Shot:** *Relevance 4 / Coherence 4 / Helpfulness 3*
- **One-Shot:** *Relevance 5 / Coherence 5 / Helpfulness 4*

Both methods lost points on helpfulness here. The model has no access to real-time balance information, so it correctly deferred to customer support rather than hallucinating a balance figure — which is the right behaviour, but results in a less immediately actionable response. This is an inherent limitation of the offline, stateless approach.

### 3.3 Key Patterns Observed

1. **One-Shot prompting consistently improved response structure.** Responses under the One-Shot method almost universally followed the example's pattern: empathetic opening → specific action step → escalation path → closing offer. Zero-Shot responses occasionally omitted the escalation path.

2. **Coherence was high for both methods.** Llama 3.2 3B rarely produced grammatically broken output. The main coherence deductions came from occasional run-on sentences or slightly unnatural phrasing in Zero-Shot responses.

3. **The model generally avoided hallucination.** When asked about specific policies it couldn't know (e.g., exact refund timelines, gift card activation procedures), both methods mostly hedged appropriately and directed users to check their account portal. This was directly influenced by the instruction *"Do NOT make up specific policy details."*

4. **Query complexity correlated with One-Shot advantage.** For simple, procedural queries (invoice download, order tracking), the gap between methods was small. For nuanced queries involving account issues or technical problems (merged accounts, duplicate emails), One-Shot responses were markedly better.

---

## 4. Conclusion & Limitations

### 4.1 Conclusion

This experiment demonstrates that **Llama 3.2 3B running locally via Ollama is a viable foundation for an offline customer support chatbot**, particularly for handling general FAQs and directing customers to the right resources. With an overall average score of **4.75 / 5.00**, the One-Shot prompting method produced responses that were consistently relevant, coherent, and helpful — competitive with what one might expect from a simple cloud-based chatbot.

**One-Shot prompting is clearly the better approach** for this use case. The single example in the prompt costs very little in compute time but provides the model with a strong template for tone, structure, and length. The improvement in Helpfulness (+0.95 on average) is particularly significant for a customer support application, where actionable guidance is the primary success metric.

### 4.2 Limitations

| Limitation | Description |
|---|---|
| **No real-time data access** | The model cannot query actual order databases, check real account balances, or verify tracking numbers. It can only provide general guidance. |
| **Hallucination risk** | Without strict prompt guardrails, the model may invent policy details (e.g., fabricating a "5-day return window"). Careful prompt engineering and output validation are essential. |
| **Context window constraints** | In a real multi-turn conversation, the model needs the full conversation history passed with each request. Long conversations can exceed the 3B model's context window (~4K tokens). |
| **Hardware dependency** | Inference speed is highly dependent on local hardware. On a standard laptop CPU, each response takes 10–30 seconds, which is too slow for live chat deployments without GPU acceleration. |
| **No personalisation** | The model has no access to customer-specific data. Every response is generic. Integrating it with a database (e.g., via a Retrieval-Augmented Generation architecture) would be needed for personalised support. |
| **Static knowledge** | Llama 3.2 was trained on a fixed dataset. It cannot know about new promotions, policy changes, or product launches at Chic Boutique without being re-prompted with that information. |

### 4.3 Recommended Next Steps

1. **Retrieval-Augmented Generation (RAG):** Connect the chatbot to a vector database containing Chic Boutique's actual policy documents, FAQs, and product catalogue so the model can ground its answers in real data.
2. **Few-Shot Prompting:** Expand from one example to 3–5 high-quality examples covering different query types (returns, payments, delivery) for further improvement.
3. **Larger Model:** Test with `llama3.2:8b` or `mistral:7b` to evaluate the performance vs. speed trade-off.
4. **Streaming Interface:** Implement `stream: true` in the API call and build a simple web UI so responses appear word-by-word, reducing perceived latency.
5. **Automated Evaluation:** Supplement manual scoring with automated metrics like ROUGE or BERTScore for more objective, scalable assessment.
