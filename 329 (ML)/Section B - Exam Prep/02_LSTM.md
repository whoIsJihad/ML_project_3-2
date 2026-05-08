# 📘 LSTM (Long Short-Term Memory)

## 1. Core Idea (Intuition)

**Problem:** RNN suffers from **vanishing gradients**; cannot learn long-range dependencies.

**Solution:** Add **memory cell** and **gating mechanisms** to control information flow.

**Key insight:** Instead of updating hidden state completely at each step, **selectively add/remove information**.

---

## 2. LSTM Architecture

### Core Components

At timestep $t$:

**Forget gate** (decide what to forget):
$$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$$

**Input gate** (decide what to add):
$$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$$

**Candidate memory**:
$$\tilde{C}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c)$$

**Update memory cell**:
$$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$$

**Output gate** (decide what to output):
$$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$$

**Hidden state**:
$$h_t = o_t \odot \tanh(C_t)$$

where:
- $\odot$: element-wise multiplication
- $\sigma$: sigmoid (outputs 0-1, "on/off" gate)
- $C_t$: memory cell (cumulative information)

---

## 3. How Gating Works

### Forget Gate
- Output $\approx 1$: Keep memory from previous step
- Output $\approx 0$: Forget previous memory

### Input Gate
- Output $\approx 1$: Accept new information
- Output $\approx 0$: Ignore new information

### Output Gate
- Output $\approx 1$: Expose internal memory to next layer
- Output $\approx 0$: Hide internal memory

**Interpretation:** Model learns when to remember, when to forget, when to output.

---

## 4. Gradient Flow Advantage

**Key difference from RNN:**

Memory cell update:
$$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$$

Gradient w.r.t. $C_{t-1}$:
$$\frac{\partial L}{\partial C_{t-1}} = \frac{\partial L}{\partial C_t} \cdot f_t$$

**Important:** If $f_t \approx 1$ (forget gate outputs 1), gradient **flows through unattenuated**!

**vs. RNN:** Gradient $= \text{error} \times \sigma'(h_{t-1}) \times W_{hh}$, which decays if $\sigma'$ or $|W_{hh}| < 1$.

---

## 5. Sequence Processing

```
x_1, x_2, ..., x_T  (input)

C_0 = 0, h_0 = 0  (initial)

For t = 1 to T:
  f_t = σ(W_f[h_{t-1}, x_t])
  i_t = σ(W_i[h_{t-1}, x_t])
  C̃_t = tanh(W_c[h_{t-1}, x_t])
  C_t = f_t ⊙ C_{t-1} + i_t ⊙ C̃_t
  o_t = σ(W_o[h_{t-1}, x_t])
  h_t = o_t ⊙ tanh(C_t)
```

**Output:** Use $h_T$ for many-to-one tasks, or $[h_1, h_2, \ldots, h_T]$ for many-to-many.

---

## 6. Number of Parameters

For hidden size $d$, input size $m$:

- Forget gate: $(d+m) \times d$ weights + $d$ biases
- Input gate: $(d+m) \times d$ weights + $d$ biases
- Candidate: $(d+m) \times d$ weights + $d$ biases
- Output gate: $(d+m) \times d$ weights + $d$ biases

**Total:** $4 \times (d+m) \times d + 4d \approx 4d(d+m)$ (4× more than RNN)

---

## 7. When It Works Well

- **Long sequences:** Text, speech (hundreds to thousands of tokens)
- **Long-range dependencies:** "The bank manager said the customer was rude. He was arrested." (pronoun binding)
- **Real-world:** Language modeling, machine translation, sentiment analysis (before Transformers)

---

## 8. Failure Cases & Limitations

| Problem | Why | Impact |
|---------|-----|--------|
| **Still cannot parallelize** | Sequential nature | Slow for very long sequences |
| **Attention is limited** | Hidden state is bottleneck | For translation, must compress all info into $h_T$ |
| **More parameters** | 4× gates | Requires more data to train |

---

## 9. Comparison: RNN vs. LSTM

| Aspect | RNN | LSTM |
|--------|-----|------|
| **Hidden state update** | Replaced each step: $h_t = \sigma(...)$ | Additive: $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$ |
| **Gradient flow** | Decays (vanishing) | Controlled by forget gate |
| **Long-range dependency** | Poor | Good |
| **Parameters** | $d(d+m)$ | $4d(d+m)$ |
| **Parallelizable** | No | No |
| **Training speed** | Fast | Slower |

---

## 10. Exam Questions

### Conceptual
1. What does the forget gate do? Why is it important for long sequences?
2. How does LSTM solve the vanishing gradient problem?
3. What's the difference between memory cell $C_t$ and hidden state $h_t$?

### Practical
1. Design LSTM for sentiment analysis: many-to-one task.
2. Two sequences of length 10 and 100. Which benefits more from LSTM over RNN?

### Trick Cases
1. Forget gate always outputs 1. What happens to memory over time?
2. Input gate always outputs 0. Can the model learn?

---

## 11. Key Takeaways

- **LSTM:** Uses memory cell $C_t$ + gating to control information flow
- **Forget gate:** $f_t$ controls how much previous memory to keep
- **Input gate:** $i_t$ controls how much new information to add
- **Output gate:** $o_t$ controls what to expose to next layer
- **Gradient advantage:** $\frac{\partial L}{\partial C_{t-1}} = \frac{\partial L}{\partial C_t} \cdot f_t$, no decay if $f_t \approx 1$
- **Cost:** 4× parameters compared to RNN, still sequential (cannot parallelize)
- **Modern alternative:** Transformers (fully parallel, better for long sequences)

---
