# 📘 GRU (Gated Recurrent Unit)

## 1. Core Idea (Intuition)

**Problem with LSTM:** Complex (4 gates, lots of parameters), slower to train.

**GRU solution:** Simplify LSTM while keeping gradient advantages.

**Key difference:** Combine forget and input gates into single **reset gate**.

---

## 2. Mathematical Formulation

### Reset Gate
$$r_t = \sigma(W_r \cdot [h_{t-1}, x_t] + b_r)$$

### Update Gate
$$z_t = \sigma(W_z \cdot [h_{t-1}, x_t] + b_z)$$

### Candidate Hidden State
$$\tilde{h}_t = \tanh(W_h \cdot [r_t \odot h_{t-1}, x_t] + b_h)$$

### Update Hidden State
$$h_t = (1 - z_t) \odot \tilde{h}_t + z_t \odot h_{t-1}$$

where:
- $r_t$: reset gate (control influence of previous hidden state)
- $z_t$: update gate (control how much to update vs. keep)
- No separate memory cell (unlike LSTM)

---

## 3. Interpretation

### Reset Gate
- $r_t \approx 1$: Use full previous hidden state
- $r_t \approx 0$: Ignore previous hidden state (reset)

### Update Gate
- $z_t \approx 1$: Keep previous hidden state (additive)
- $z_t \approx 0$: Completely replace with new candidate

### Candidate
- Computed with reset hidden state: $r_t \odot h_{t-1}$
- Combined multiplicatively with new input

---

## 4. GRU vs. LSTM

| Aspect | LSTM | GRU |
|--------|------|-----|
| **# Gates** | 4 (forget, input, output, tanh) | 2 (reset, update) |
| **Memory cell** | Separate $C_t$ | None (hidden state $h_t$ directly) |
| **Gradient** | Through $C_t$ (additive) | Through $h_t$ (additive) |
| **Parameters** | $4d(d+m)$ | $3d(d+m)$ |
| **Complexity** | Higher | Lower |
| **Performance** | Slightly better on long sequences | Similar for most tasks |
| **Training speed** | Slower | Faster |

---

## 5. Forward Pass

```
For t = 1 to T:
  r_t = σ(W_r[h_{t-1}, x_t])
  z_t = σ(W_z[h_{t-1}, x_t])
  h̃_t = tanh(W_h[r_t ⊙ h_{t-1}, x_t])
  h_t = (1 - z_t) ⊙ h̃_t + z_t ⊙ h_{t-1}
```

**Simpler than LSTM:** Only 2 matrix multiplications per gate (vs. 3 for LSTM).

---

## 6. When to Use GRU vs. LSTM

| Scenario | Choice |
|----------|--------|
| **Large model, lots of data** | LSTM (slightly better) |
| **Resource-constrained** | GRU (faster, fewer params) |
| **Quick experiment** | GRU (trains faster) |
| **Production (real-time)** | GRU (inference speed) |

---

## 7. When It Works Well

- Same as LSTM (sequences, NLP)
- Tasks where LSTM overkill
- Mobile/edge deployment
- Real-world: Google voice search uses GRU variants

---

## 8. Failure Cases

| Problem | Why |
|---------|-----|
| **Moderate sequences only** | Not as powerful as LSTM for very long sequences |
| **Still sequential** | Cannot parallelize like Transformers |

---

## 9. Exam Questions

### Conceptual
1. Explain the reset and update gates in GRU. How do they differ from LSTM's gates?
2. Why is GRU faster than LSTM?
3. When would you choose GRU over LSTM?

### Practical
1. Compare training time: GRU vs. LSTM on same hardware.
2. Sentiment analysis: Does GRU vs. LSTM matter?

---

## 10. Key Takeaways

- **GRU:** Simplified LSTM with 2 gates (reset, update) instead of 4
- **Reset gate:** Controls influence of previous hidden state
- **Update gate:** Controls additive update vs. replacement
- **Efficiency:** $3d(d+m)$ parameters vs. LSTM's $4d(d+m)$
- **Gradient advantage:** Still avoids vanishing through additive connection
- **Tradeoff:** Slightly less expressive than LSTM, but faster
- **Modern usage:** Both GRU and LSTM obsoleted by Transformers in modern NLP

---
