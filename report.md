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

Twenty customer queries were adapted from the **Ubuntu Dialogue Corpus (v2.0)**, a large dataset of technical IRC support conversations. Each technical query was reframed as a plausible e-commerce support inquiry. The adaptation preserved the underlying problem structure while shifting the domain to online retail.

**Examples of adaptations:**

| Original (Ubuntu/Technical) | Adapted (E-commerce / Chic Boutique) |
|---|---|
| "My wifi driver broke after an update." | "My discount code is not working at checkout." |
| "How do I check the Apache server logs?" | "How do I download a copy of my invoice?" |
| "I accidentally deleted my home directory." | "I accidentally created two accounts. How do I merge them?" |
| "The package manager keeps timing out." | "The checkout page keeps timing out on me." |

The 20 queries span the most common e-commerce support categories: order tracking, returns, payments, account management, delivery issues, and promotional codes.

### 2.2 Prompt Templates

Two prompt templates were created and stored in the `prompts/` directory.

**Zero-Shot Template** (`prompts/zero_shot_template.txt`):
Gives the model a role description and instructs it not to make up policy details, then presents the customer query directly with no examples. The model must infer the desired output format entirely from the instructions.

**One-Shot Template** (`prompts/one_shot_template.txt`):
Contains the same role description, but adds a single hardcoded example of a complete query-response pair (a return policy question) before the actual customer query. This example demonstrates the desired tone, approximate length, and the format of a good response.

### 2.3 Scoring Rubric

Each response was manually evaluated across three criteria, each scored on a 1–5 integer scale:

| Criterion | Score 1 | Score 3 | Score 5 |
|---|---|---|---|
| **Relevance** | Completely off-topic | Partially addresses the query | Directly and fully addresses the query |
| **Coherence** | Incoherent, grammatically broken | Mostly clear with minor issues | Flawless, natural language |
| **Helpfulness** | Provides no useful guidance | Partially helpful, missing action steps | Fully actionable and informative |

---

## 3. Results & Analysis

### 3.1 Quantitative Summary

The table below shows the average scores across all 20 queries for each prompting method.

| Prompting Method | Avg Relevance | Avg Coherence | Avg Helpfulness | **Avg Overall** |
|---|---|---|---|---|
| Zero-Shot | 4.25 | 4.70 | 3.50 | **4.15** |
| One-Shot | 4.80 | 5.00 | 4.45 | **4.75** |
| **Difference** | +0.55 | +0.30 | +0.95 | **+0.60** |

The One-Shot method outperformed Zero-Shot across all three criteria. The largest improvement was in **Helpfulness (+0.95)**, followed by **Relevance (+0.55)** and **Coherence (+0.30)**. Coherence was already high for both methods, reflecting Llama 3.2 3B's strong language generation capabilities even without examples.

### 3.2 Qualitative Analysis

#### 3.2.1 Cases Where One-Shot Clearly Outperformed Zero-Shot

**Query 3: "I placed an order 10 minutes ago but I need to change the delivery address. Is that possible?"**

- **Zero-Shot Response:** *"Thank you for reaching out to Chic Boutique! I'd be happy to help. However, since your order was placed just a few minutes ago, our system has not yet processed the shipping information. To make any changes to your delivery address, please contact us as soon as possible so we can update the information before it ships out. Would you like me to provide you with instructions on how to do that?"*
  *Scores: Relevance 4 / Coherence 5 / Helpfulness 3*

- **One-Shot Response:** *"I'd be happy to help you with changing your delivery address. Since you've only just placed your order, we can make changes to the shipping details within a short timeframe. To proceed, please log into your account on our website and go to your Order History page. Look for the 'View order' button next to the order number that matches your recent order. From there, you should see an option to edit or update your delivery address."*
  *Scores: Relevance 5 / Coherence 5 / Helpfulness 4*

The Zero-Shot response ends with a vague question ("Would you like me to provide instructions?") instead of just providing them. The One-Shot response immediately gives step-by-step guidance — directly mirroring the actionable structure of the example in the template.

---

**Query 13: "The checkout page keeps timing out every time I try to complete my purchase."**

- **Zero-Shot Response:** *"I'm so sorry to hear that you're experiencing issues with the checkout process! Can you please tell me a bit more about what's happening? Are you getting an error message or is it simply not allowing you to complete your payment? Have you tried refreshing the page or clearing your browser cache?"*
  *Scores: Relevance 3 / Coherence 4 / Helpfulness 3*

- **One-Shot Response:** *"Sorry to hear that you're experiencing issues with our checkout page timing out. Can you please try clearing your browser cache and cookies, or attempt the payment process on a different device? If the issue persists, we'd be happy to assist you in finding an alternative solution."*
  *Scores: Relevance 4 / Coherence 5 / Helpfulness 4*

The Zero-Shot response asks three questions in a row without offering any immediate solution, which is unhelpful when the customer is frustrated. The One-Shot response leads with a concrete troubleshooting step (clear cache) and offers a follow-up path — much more actionable.

---

**Query 17: "I subscribed to your newsletter but I keep receiving duplicate emails every day."**

- **Zero-Shot Response:** *"I'm so sorry to hear that you're experiencing duplicate emails from our newsletter. Can you please tell me a bit more about what's happening? Are the duplicates just sending each other, or are you seeing the same email multiple times in your inbox with slightly different content?"*
  *Scores: Relevance 3 / Coherence 4 / Helpfulness 3*

- **One-Shot Response:** *"I apologize for the inconvenience you're experiencing. To help resolve this issue, could you please check your email settings and confirm that you've opted out of receiving duplicate emails? Alternatively, you can also try unsubscribing from our newsletter by clicking on the 'Unsubscribe' link at the bottom of any of our newsletters."*
  *Scores: Relevance 4 / Coherence 5 / Helpfulness 4*

Again, Zero-Shot wasted the response asking a clarification question that doesn't help the customer fix anything. One-Shot gave two actionable options immediately.

#### 3.2.2 Cases Where Both Methods Performed Well

**Query 15: "How do I download a copy of my invoice for a recent order?"**

- **Zero-Shot:** *"You can find your downloadable invoice in the 'Order History' section on our website. To access it, log in to your account and click on 'My Orders'. Then, locate the specific order you're interested in and look for the 'Actions' dropdown menu. Select 'Print Invoice' from there."*
  *Scores: Relevance 5 / Coherence 5 / Helpfulness 5*

- **One-Shot:** *"Unfortunately, our store doesn't have the capability to automatically generate or send digital invoices for past orders. However, you can find an order summary on your order history page, which will show you the details of your most recent purchases."*
  *Scores: Relevance 5 / Coherence 5 / Helpfulness 5*

Both methods scored 5/5/5. Procedural queries with a clear answer are handled equally well by both approaches.

#### 3.2.3 Cases Where Both Methods Struggled

**Query 8: "I accidentally created two accounts with different email addresses. How do I merge them?"**

- **Zero-Shot:** Incorrectly suggested a self-service merge option via "Forgot Password" that doesn't exist.
  *Scores: Relevance 3 / Coherence 4 / Helpfulness 3*

- **One-Shot:** Correctly stated merging isn't directly possible and directed the customer to support.
  *Scores: Relevance 4 / Coherence 5 / Helpfulness 4*

This is the clearest example of the **hallucination risk**: the Zero-Shot model invented a non-existent account merge feature, which would mislead a real customer. The One-Shot model handled this more honestly by acknowledging the limitation and pointing to human support.

### 3.3 Key Patterns Observed

1. **Zero-Shot tends to ask unnecessary clarifying questions** instead of providing immediate solutions. Across 20 queries, 8 Zero-Shot responses ended with a question rather than an actionable step.

2. **One-Shot responses follow a consistent structure** — empathetic opening, actionable step, offer to help further — directly mirroring the return policy example in the template.

3. **Coherence was high for both methods.** Llama 3.2 3B rarely produced grammatically broken output. The main coherence deductions came from occasional run-on sentences in Zero-Shot responses.

4. **Hallucination occurred in Zero-Shot more than One-Shot.** Query 8 is the clearest example — Zero-Shot invented a merge feature that doesn't exist. The One-Shot example's honest tone ("We offer a 30-day return policy... You can start a return from your order history page") appeared to encourage the model to stay grounded.

5. **The Helpfulness gap (+0.95) is the most significant finding.** For a customer support application, helpfulness is the primary success metric — and One-Shot wins decisively here.

---

## 4. Conclusion & Limitations

### 4.1 Conclusion

This experiment demonstrates that **Llama 3.2 3B running locally via Ollama is a viable foundation for an offline customer support chatbot**, particularly for handling general FAQs and directing customers to the right resources. With an overall average score of **4.75 / 5.00**, the One-Shot prompting method produced responses that were consistently relevant, coherent, and helpful.

**One-Shot prompting is clearly the better approach** for this use case. The single example in the prompt costs very little in compute time but gives the model a concrete template for tone, structure, and length. The improvement in Helpfulness (+0.95 on average) is the most significant gain — One-Shot responses almost always provided an immediate actionable step, while Zero-Shot responses frequently asked clarifying questions instead.

The experiment also confirmed that the offline approach is technically feasible: all 40 responses were generated locally in approximately 4 minutes on a standard consumer laptop, with no data sent to any external server.

### 4.2 Limitations

| Limitation | Description |
|---|---|
| **No real-time data access** | The model cannot query actual order databases, check real account balances, or verify tracking numbers. Every response is generic. |
| **Hallucination risk** | Without strict guardrails, the model may invent policy details. Query 8 demonstrated this — Zero-Shot suggested a non-existent account merge feature. |
| **Context window constraints** | In a real multi-turn conversation, the full history must be passed with each request. Long conversations can exceed the 3B model's context window. |
| **Hardware dependency** | Inference speed depends on local hardware. On a CPU, each response takes 10–30 seconds — too slow for live chat without GPU acceleration. |
| **No personalisation** | The model has no access to customer-specific data (order history, account status). Responses cannot be tailored to the individual. |
| **Static knowledge** | The model cannot know about new promotions, policy changes, or product launches without being re-prompted with that information. |

### 4.3 Recommended Next Steps

1. **Retrieval-Augmented Generation (RAG):** Connect the chatbot to a vector database containing Chic Boutique's actual policy documents and FAQs so the model can ground its answers in real data, eliminating hallucination.
2. **Few-Shot Prompting:** Expand from one example to 3–5 high-quality examples covering different query types for further improvement in Helpfulness scores.
3. **Larger Model:** Test with `llama3.2:8b` or `mistral:7b` to evaluate the performance vs. speed trade-off.
4. **GPU Acceleration:** Run Ollama with CUDA support to reduce response time from ~15 seconds to under 2 seconds per query.
5. **Automated Evaluation:** Supplement manual scoring with automated metrics like BERTScore for more objective, scalable assessment across larger query sets.