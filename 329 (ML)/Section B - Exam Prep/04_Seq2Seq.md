# 📘 Sequence-to-Sequence (Seq2Seq) Models

## 1. Core Idea (Intuition)

**Problem:** LSTM/RNN process variable-length input, but output length may differ.

**Example:** Translation — English "hello" (1 word) → Spanish "hola" (1 word), but "good morning" (2 words) → "buenos días" (2 words).

**Seq2Seq solution:** Two RNNs:
- **Encoder:** Compress input sequence into fixed vector
- **Decoder:** Expand fixed vector into output sequence

---

## 2. Architecture

### Encoder
Takes input sequence $x_1, x_2, \ldots, x_T$:
$$h_t = \text{LSTM}(h_{t-1}, x_t)$$

Final hidden state $h_T$ = **context vector** (summary of input).

### Decoder
Takes context vector $h_T$, generates output sequence:
$$h_t' = \text{LSTM}(h_{t-1}', c) \quad \text{where } c = h_T$$
$$y_t = W_{out} h_t' + b$$

Start with special token `<START>`, end with `<END>`.

### Full Process
```
Input:   x_1, x_2, x_3
Encoder: [LSTM] → h_T (context)

Decoder starts with h_0' = h_T:
  Step 1: y_1 from h_0' 
  Step 2: y_2 from h_1' (previous output fed back)
  Step 3: y_3 from h_2' 
  Until <END> token
Output: y_1, y_2, y_3, ...
```

---

## 3. Inference (Generating Output)

### Greedy Decoding
At each step, pick **most likely token**:
$$y_t = \arg\max_w p(y_t = w | y_1, \ldots, y_{t-1})$$

**Problem:** Locally optimal, not globally optimal. May miss better overall sequences.

### Beam Search
Keep top-$k$ hypotheses (e.g., $k=5$):
1. Start with `<START>`
2. Generate all next tokens, keep top-5 by probability
3. For each, generate all next tokens, keep top-5 by cumulative probability
4. Continue until all reach `<END>`
5. Return best sequence by probability

**Tradeoff:** Better quality than greedy, but slower ($k \times$ slower).

---

## 4. Attention Mechanism (Brief Overview)

**Problem:** Fixed context vector $h_T$ is bottleneck (must compress entire input).

**Solution:** At each decoder step, compute **attention** over all encoder hidden states:

$$\alpha_t = \text{softmax}(q_t^T k_1, q_t^T k_2, \ldots, q_t^T k_T)$$

$$\text{context}_t = \sum_i \alpha_{t,i} v_i$$

where:
- $q_t$: query (decoder state)
- $k_i, v_i$: key, value (encoder hidden states)

**Intuition:** Attention decides which input tokens are relevant to current output step.

**Effect:** Decoder can "look back" at input, not just summary.

---

## 5. Training vs. Inference

### Training (Teacher Forcing)
```
Decoder input: <START>, y_1_true, y_2_true, ...
Compare with: y_1_pred, y_2_pred, ...
Loss = cross_entropy(predictions, true_targets)
```

**Advantage:** Correct history available, faster training.

**Problem:** **Exposure bias** — at inference, wrong predictions used as input, which training never saw.

### Inference
```
Decoder input: <START>, y_1_pred, y_2_pred, ...
(feedback loop; errors compound)
```

---

## 6. Common Issues

| Problem | Why | Fix |
|---------|-----|-----|
| **Exposure bias** | Training uses true labels, inference uses predictions | Scheduled sampling (gradually use predictions) |
| **Short outputs** | Model learns to output early | Penalize short sequences; adjust beam search |
| **Forgetting input** | Context vector bottleneck | Use attention mechanism |
| **Slow inference** | Generating token-by-token | Parallel decoding (see non-autoregressive models) |

---

## 7. Use Cases

- **Machine translation:** English → French
- **Summarization:** Long article → short summary
- **Image captioning:** Image → text description (CNN encoder + RNN decoder)
- **Question answering:** Question → answer
- **Chatbots:** User message → bot response

---

## 8. Comparison: Seq2Seq vs. Single RNN

| Aspect | Single RNN | Seq2Seq |
|--------|-----------|---------|
| **Flexibility** | Fixed output length | Variable output length |
| **Context** | Local (hidden state only) | Global (full input via encoder) |
| **Translation** | Not suitable | Perfect |
| **Complexity** | Simple | More complex |

---

## 9. Exam Questions

### Conceptual
1. Why is Seq2Seq needed for machine translation instead of single RNN?
2. What is "teacher forcing"? Why does it cause problems?
3. Explain attention in Seq2Seq. Why is it better than fixed context vector?

### Practical
1. Design Seq2Seq for summarization (input: article, output: summary).
2. Compare greedy decoding vs. beam search. When use each?

### Trick Cases
1. Encoder outputs context $h_T$. Decoder never sees encoder hidden states $h_1, \ldots, h_{T-1}$. Problem?
2. Training with teacher forcing, but inference fails. Why?

---

## 10. Key Takeaways

- **Seq2Seq:** Encoder (compress input) + Decoder (generate output)
- **Context vector:** Final encoder hidden state $h_T$
- **Teacher forcing:** Train with true labels; faster but causes exposure bias
- **Beam search:** Keep top-$k$ sequences; better than greedy
- **Attention:** Decoder attends to relevant encoder states; solves bottleneck
- **Exposure bias:** Models trained on true labels, tested on predictions → mismatch
- **Modern replacement:** Transformers are default for translation (parallel, faster)

---
