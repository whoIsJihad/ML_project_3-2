# 📘 Recurrent Neural Networks (RNN)

## 1. Core Idea (Intuition)

**Problem:** CNNs and MLPs assume **independent samples**; don't handle **sequences** well.

**Sequence:** Text "hello" = [h, e, l, l, o], dependency between consecutive characters.

**RNN solution:** Use **hidden state** that carries information from previous timesteps.

---

## 2. Mathematical Formulation

### Standard RNN

At each timestep $t$:
$$h_t = \sigma(W_{hh} h_{t-1} + W_{xh} x_t + b_h)$$

$$y_t = W_{hy} h_t + b_y$$

where:
- $x_t$: input at timestep $t$
- $h_t$: hidden state at timestep $t$
- $W_{hh}$: recurrent weight (hidden-to-hidden)
- $W_{xh}$: input-to-hidden weight
- $\sigma$: activation (typically $\tanh$)

### Key Insight
**Same weights** $W_{hh}, W_{xh}, W_{hy}$ used at every timestep. This is **weight sharing** across time.

---

## 3. Processing Sequences

### Forward Pass
```
x_1, x_2, x_3, ..., x_T  (input sequence)

h_0 = 0  (initial hidden state)

For t = 1 to T:
  h_t = σ(W_hh * h_{t-1} + W_xh * x_t)
  y_t = W_hy * h_t
```

### Full Sequence
- Input: $X = [x_1, x_2, \ldots, x_T]$
- Output: $Y = [y_1, y_2, \ldots, y_T]$
- Hidden states: $H = [h_1, h_2, \ldots, h_T]$ (computed sequentially)

---

## 4. Training (Backpropagation Through Time - BPTT)

**Challenge:** Gradient flows backward through time.

$$\frac{\partial L}{\partial W_{hh}} = \sum_{t=1}^{T} \frac{\partial L}{\partial y_t} \cdot \text{(chain rule through } T \text{ timesteps)}$$

Long sequences = gradient must flow through many layers (same as very deep network).

**Problem:** Vanishing/exploding gradients (same as deep networks).

---

## 5. Sequence Types

| Type | Example | Output |
|------|---------|--------|
| **Many-to-one** | Text → sentiment | Single output at end |
| **One-to-many** | Image → caption | Multiple outputs |
| **Many-to-many (same length)** | POS tagging | Output per token |
| **Many-to-many (different length)** | Translation | Seq2Seq (see next topic) |

---

## 6. Failure Cases / Limitations

| Problem | Why | Impact |
|---------|-----|--------|
| **Vanishing gradients** | Gradient decays through time | Early timesteps don't learn |
| **Exploding gradients** | Gradient grows unboundedly | Training unstable |
| **Only recent context** | Hidden state size limited | Can't remember far-back info |
| **Slow training** | BPTT is sequential | Cannot parallelize well |

---

## 7. When It Works Well

- **Sequential data:** Text, speech, time series
- **Variable-length inputs:** No padding needed (process one timestep at a time)
- **Simple patterns:** Short-range dependencies
- **Real-world:** Language modeling, sentiment analysis (before Transformers)

---

## 8. Variants & Extensions

| Variant | Purpose |
|---------|---------|
| **Bidirectional RNN** | Process sequence both directions; better context |
| **Multi-layer RNN** | Stack RNNs; learn hierarchical patterns |
| **LSTM/GRU** | Fix vanishing gradients (see next topics) |

---

## 9. Comparison Table

| Method | Strength | Weakness | Best For |
|--------|----------|----------|----------|
| **RNN** | Simple, interpretable | Vanishing gradients, short memory | Simple sequences, baselines |
| **LSTM** | Long-range dependencies | More parameters, slower | Long sequences, text |
| **GRU** | Simpler than LSTM | Less expressive | Lightweight models |
| **Transformer** | Parallel, no vanishing gradient | Attention complexity | Modern NLP (default) |

---

## 10. Exam Questions

### Conceptual
1. Why does RNN have "memory"? How is information passed between timesteps?
2. What is the difference between Recurrent and Feedforward networks?
3. Why does RNN suffer from vanishing gradients while CNNs don't?

### Practical
1. How would you classify a variable-length sentence using RNN? (many-to-one)
2. Design an RNN for machine translation (many-to-many, different lengths).

### Failure Cases
1. You train RNN for 100 epochs. Loss stops decreasing after 50. What might be wrong?
2. A sentence of length 100 words: RNN remembers early words poorly. Why?

---

## 11. Key Takeaways

- **RNN:** Hidden state $h_t$ carries information across time
- **Weight sharing:** Same $W_{hh}, W_{xh}$ used at every timestep
- **BPTT:** Backprop through time; gradient flows backward through timesteps
- **Vanishing gradient:** Long sequences → gradient decay → early timesteps don't learn
- **Many-to-one:** Classify sequences (use $h_T$)
- **Bidirectional RNN:** Better context (both directions)
- **Modern alternative:** Transformers (parallel, no gradient issues)

---
