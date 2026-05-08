# 📘 Transformers

## 1. Core Idea (Intuition)

**Problem with RNN/LSTM:**
- Sequential: cannot parallelize (slow training)
- Information bottleneck: context vector for Seq2Seq
- Vanishing gradients (though LSTM helps)

**Transformer solution:** Replace recurrence with **self-attention**. Process entire sequence in parallel.

**Key insight:** Attention learns which tokens are relevant to each other; no need for recurrence.

---

## 2. Self-Attention Mechanism

### Query, Key, Value
For each token, compute three vectors:
$$Q = XW^Q, \quad K = XW^K, \quad V = XW^V$$

where $X$ is input (all tokens stacked).

### Attention Scores
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V$$

where:
- $QK^T$: similarity between each pair of tokens (shape: $T \times T$, where $T$ is sequence length)
- $\sqrt{d_k}$: scaling factor ($d_k$ is dimension of keys)
- $\text{softmax}$: attention weights (which tokens matter for each position)
- Result: updated representations incorporating context from all tokens

### Example
For position 1 in "the cat sat":
- Query for "the" attends to all tokens
- Learns "the" is article, might pay attention to noun "cat"
- Low attention to "sat" (verb)

---

## 3. Multi-Head Attention

### Problem
Single attention might focus on one pattern. Use multiple "heads".

$$\text{MultiHead}(Q, K, V) = \text{Concat}(h_1, h_2, \ldots, h_h) W^O$$

where each head:
$$h_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$

**Effect:** Each head learns different attention patterns (e.g., one head focuses on pronouns, another on verbs).

### Common Settings
- **# heads:** 8, 12, 16
- **$d_{model}$:** 512, 768, 1024
- **$d_k = d_{model} / h$:** e.g., 512 / 8 = 64

---

## 4. Transformer Block

### Layer Norm + Residual Connection
$$\text{out} = \text{LayerNorm}(x + \text{SubLayer}(x))$$

Prevents gradient issues; stabilizes training.

### Feed-Forward Network
$$\text{FFN}(x) = \text{ReLU}(xW_1 + b_1)W_2 + b_2$$

Applied to each position independently.

### Full Block
```
Input x
  ↓
LayerNorm
  ↓
MultiHeadAttention
  ↓
+ Residual (skip connection)
  ↓
LayerNorm
  ↓
FeedForwardNetwork
  ↓
+ Residual
  ↓
Output
```

---

## 5. Positional Encoding

**Problem:** Self-attention is position-agnostic. "cat ate food" vs. "food ate cat" looks same without position info.

**Solution:** Add positional encoding to input:
$$PE(t, 2i) = \sin(t / 10000^{2i/d})$$
$$PE(t, 2i+1) = \cos(t / 10000^{2i/d})$$

**Effect:** Position information injected; model can learn order.

---

## 6. Encoder-Decoder Architecture (Seq2Seq Transformer)

### Encoder
Stack of $N$ transformer blocks. Processes input.

### Decoder
Stack of $N$ transformer blocks with **cross-attention**:
- Query: decoder
- Key, Value: encoder output

**Decoding:** Autoregressive (one token at a time).

### Masking
Prevent decoder from attending to **future tokens** (they don't exist yet):
$$\text{Attention}(Q, K, V)_{\text{masked}} = \text{softmax}(\text{mask}(QK^T)) V$$

where mask sets future positions to $-\infty$ before softmax.

---

## 7. Why Transformers Win

| Aspect | RNN/LSTM | Transformer |
|--------|----------|-------------|
| **Parallelization** | Sequential → slow | Parallel → fast |
| **Gradient flow** | Through time → vanishing | Multi-hop attention → stable |
| **Context range** | Hidden state bottleneck | All tokens attended equally |
| **Training time** | Slow | 10-100× faster |
| **Long sequences** | Expensive | Quadratic in sequence length |

---

## 8. Variants & Extensions

| Variant | Purpose |
|---------|---------|
| **BERT** | Bidirectional encoder (two-way attention) |
| **GPT** | Decoder-only (left-to-right generation) |
| **RoBERTa** | Improved BERT (better pretraining) |
| **T5** | Encoder-decoder unified (text-to-text) |
| **Vision Transformer (ViT)** | Transformers for images |
| **Longformer, BigBird** | Efficient attention for long sequences |

---

## 9. Common Issues

| Problem | Why | Fix |
|---------|-----|-----|
| **Quadratic complexity** | Attention is $O(T^2)$ in sequence length | Use sparse attention (local windows) |
| **Slow inference** | Generating token-by-token | Speculative decoding, distillation |
| **Position encoding limits** | Fixed PE only works up to max length | Relative positional bias, ALiBi |

---

## 10. Exam Questions

### Conceptual
1. Why is self-attention better than RNN for parallelization?
2. What does multi-head attention do? Why multiple heads?
3. Explain positional encoding. Why is it needed?

### Practical
1. Design BERT (bidirectional encoder). How differs from GPT?
2. For long document (10K tokens), how would you adapt Transformer?

### Trick Cases
1. Remove positional encoding from Transformer. Effect on performance?
2. Decoder attention to future tokens (no masking). What happens?

---

## 11. Key Takeaways

- **Self-attention:** Query-Key-Value mechanism; $\text{softmax}(\frac{QK^T}{\sqrt{d_k}}) V$
- **Multi-head:** Multiple attention subspaces; each learns different patterns
- **Parallelizable:** Entire sequence processed at once (vs. RNN's sequential)
- **Positional encoding:** Injects position information; essential for order
- **Residual + LayerNorm:** $\text{LayerNorm}(x + \text{SubLayer}(x))$; stabilizes training
- **Encoder-decoder:** Encoder processes input; decoder generates with cross-attention
- **Causal masking:** Decoder cannot attend to future; prevents cheating in autoregressive generation
- **Modern default:** BERT, GPT, T5 variants dominate NLP (Transformers everywhere)

---
