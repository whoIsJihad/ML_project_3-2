# 📘 Decoder-Only Architectures (GPT)

## 1. Core Idea (Intuition)

**Transformer variants:**
- **Encoder only (BERT):** Bidirectional; masked language modeling
- **Encoder-Decoder (T5):** Input processing + generation
- **Decoder only (GPT):** Autoregressive generation only

**GPT approach:** Single stack of Transformers; generate left-to-right.

---

## 2. Architecture

### Standard Transformer Decoder
```
Input: Previous tokens (at inference) or full sequence (at training)

For each layer:
  MultiHeadAttention (MASKED - cannot attend to future)
    ↓
  FeedForwardNetwork
    ↓
  LayerNorm + Residual

Output: Logits for next token
```

### Key Difference from Seq2Seq
- **Seq2Seq:** Separate encoder, decoder processes encoder output
- **GPT:** Single decoder; attends to own previous tokens only

---

## 3. Causal Masking

**Constraint:** Token at position $t$ can only attend to positions $< t$ (not future).

$$\text{Attention}_{\text{masked}} = \text{softmax}(\text{mask}(QK^T / \sqrt{d_k})) V$$

where $\text{mask}$ sets future positions to $-\infty$ before softmax.

**Effect:** Cannot "cheat" by looking at future tokens during training.

---

## 4. Training

### Input
Full sequence: $[x_1, x_2, \ldots, x_T]$

### Prediction
At position $t$, predict $x_{t+1}$ from $[x_1, \ldots, x_t]$.

**Loss:** Cross-entropy on predicting next token.

$$L = \sum_{t=1}^{T-1} \text{CrossEntropy}(\hat{y}_{t+1}, y_{t+1})$$

### Efficiency
Parallelize: Compute all positions simultaneously (causal mask prevents cheating).

Unlike RNN (sequential), Transformer decoder can compute all positions in parallel during training.

---

## 5. Inference (Generation)

```
context = [<START>]

For step t:
  logits = model(context)
  next_token = sample/argmax(logits[-1])  [last position]
  context += [next_token]
  
  if next_token == <END>:
    break

return context
```

**Autoregressive:** Generate one token at a time; feed back into model.

---

## 6. Prompt Engineering

**Prompt:** Conditioning text that directs model behavior.

### Few-Shot Prompting
```
Prompt:
"Translate English to French.

English: hello
French: bonjour

English: goodbye
French: ?"

Model: "au revoir"
```

**Effect:** Model learns pattern from examples; generalizes.

### Zero-Shot Prompting
```
Prompt: "Classify sentiment. Text: I love this movie. Sentiment: ?"

Model: "Positive"
```

---

## 7. Comparison: Encoder-Only vs. Decoder-Only vs. Encoder-Decoder

| Architecture | Attention | Use Case | Example |
|-------------|-----------|----------|---------|
| **Encoder-only (BERT)** | Bidirectional | Classification, tagging | Sentiment, NER |
| **Decoder-only (GPT)** | Causal (left-to-right) | Generation | Text completion, chat |
| **Encoder-decoder (T5)** | Bidirectional + causal | Seq2Seq tasks | Translation, summarization |

---

## 8. In-Context Learning

**Large language models (LLMs):** Can "learn" from examples in prompt without gradient updates.

**Example:**
```
Prompt:
"Few-shot learning:
Example 1: Input: cat, Output: animal
Example 2: Input: car, Output: vehicle
Now: Input: apple, Output: ?"

Model: "fruit"
```

**Mechanism:** Attention over examples; weights attend to relevant examples.

---

## 9. Applications

- **Text completion:** GitHub Copilot, T9 keyboard
- **Chatbots:** ChatGPT, Claude, Bard
- **Code generation:** Codex
- **Question answering:** Read context, answer question
- **Summarization:** Generate summary of input

---

## 10. Scaling Laws

**Observation:** Larger models perform better.

$$\text{Loss} \propto N^{-\alpha}$$

where $N$ is number of parameters, $\alpha \approx 0.1$ (slow decay).

**Implication:** Scaling up model/data improves performance; deep learning trend continues.

---

## 11. Failure Cases

| Problem | Why |
|---------|-----|
| **Hallucination** | Generates plausible-sounding but false information |
| **Context length limit** | Cannot process very long documents |
| **No explicit knowledge** | No facts; must be in training data or prompt |

---

## 12. Exam Questions

### Conceptual
1. What is causal masking? Why is it needed?
2. How does GPT differ from BERT (encoder-only)?
3. Explain in-context learning. How does attention enable it?

### Practical
1. Design prompt for sentiment classification (few-shot).
2. Generate text: what hyperparameters control diversity (temperature, top-k)?

### Trick Cases
1. Remove causal mask from GPT. Effect?
2. Model hallucinating. Cause? Fix?

---

## 13. Key Takeaways

- **GPT:** Decoder-only Transformer; left-to-right causal generation
- **Causal masking:** Cannot attend to future; enables autoregressive generation
- **Training:** Predict next token from previous context
- **Inference:** Generate token-by-token; feed back to model
- **Prompt engineering:** Condition behavior via examples (few-shot learning)
- **In-context learning:** Attend to examples in prompt; learn without gradient updates
- **Scaling:** Larger models → better performance (continue scaling trends)
- **Comparison:** Encoder (bidirectional) vs. Decoder (causal) vs. Encoder-Decoder (both)

---
