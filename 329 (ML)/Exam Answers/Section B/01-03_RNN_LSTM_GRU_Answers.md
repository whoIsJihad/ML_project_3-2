# 📝 RNN, LSTM, GRU - Exam Answers

## RNN (Recurrent Neural Networks)

### Q1: Explain vanishing gradients in RNNs

**The problem:**

RNN at time $t$:
$$h_t = \sigma(W_{hh}h_{t-1} + W_{xh}x_t + b_h)$$

To learn long-term dependencies (e.g., word 50 steps ago), gradients must backpropagate through time:

$$\frac{\partial L}{\partial h_1} = \frac{\partial L}{\partial h_T} \cdot \frac{\partial h_T}{\partial h_{T-1}} \cdots \frac{\partial h_2}{\partial h_1}$$

Each factor: $\frac{\partial h_t}{\partial h_{t-1}} = W_{hh}^T \sigma'(z_{t-1})$

**Sigmoid derivative:** $\sigma'(z) \in (0, 0.25]$

Product: $(0.25)^{T-1}$ where $T$ = sequence length.

```
T=10:  (0.25)^9 ≈ 10^-6  (tiny!)
T=50:  (0.25)^49 ≈ 10^-30 (near-zero)
```

**Result:** Early time steps barely update. RNN can't learn long-term dependencies.

---

### Q2: What is backpropagation through time (BPTT)?

**BPTT:** Unroll RNN over time, then apply backprop to the unrolled graph.

```
t=1: h₁ ← f(x₁, h₀)
t=2: h₂ ← f(x₂, h₁)
t=3: h₃ ← f(x₃, h₂)
...
t=T: hₜ ← f(xₜ, hₜ₋₁)

Loss: L = Σ ℓ(yₜ, ŷₜ)

Backprop through entire chain to compute ∂L/∂W
```

**Truncated BPTT:** Backprop only last $\tau$ time steps (reduce memory, prevent vanishing gradients).

---

### Q3: Why is RNN's hidden state called "memory"?

**Definition:** $h_t$ encodes information from past: $h_t = f(x_t, h_{t-1}, h_{t-2}, \ldots)$

**Memory capacity:** Only ~100-200 steps (vanishing gradient limit).

---

## LSTM (Long Short-Term Memory)

### Q1: Explain the LSTM cell

**Components:**
```
Input gate:  i_t = σ(W_i[h_{t-1}, x_t])  — what to remember from input?
Forget gate: f_t = σ(W_f[h_{t-1}, x_t])  — what to forget from past?
Candidate:   C̃_t = tanh(W_c[h_{t-1}, x_t]) — what's new?
Output gate: o_t = σ(W_o[h_{t-1}, x_t])  — what to output?

Cell update: C_t = f_t ⊙ C_{t-1} + i_t ⊙ C̃_t  (additive!)
Output:      h_t = o_t ⊙ tanh(C_t)
```

**Key innovation:** Additive connection for $C_t$.

$$\frac{\partial C_t}{\partial C_{t-1}} = f_t$$

Gradient flows: not exponentially decaying if $f_t ≈ 1$.

---

### Q2: Why does LSTM solve vanishing gradients?

**Reason:** Additive cell state $C_t$ instead of multiplicative hidden state $h_t$.

**Multiplicative (RNN):** $h_t = f(h_{t-1}, x_t)$ → gradient product → vanishes
**Additive (LSTM):** $C_t = C_{t-1} + \Delta_t$ → gradient sum → no vanishing!

$$\frac{\partial C_t}{\partial C_{t-1}} = \frac{\partial}{\partial C_{t-1}}(f_t C_{t-1} + i_t C̃_t) = f_t$$

If forget gate $f_t$ learned to be $≈ 1$, gradients flow unchanged.

---

### Q3: LSTM vs GRU — tradeoffs?

| | LSTM | GRU |
|---|---|---|
| **Parameters** | $4d(d+m)$ | $3d(d+m)$ |
| **Gates** | 3 (input, forget, output) | 2 (reset, update) |
| **Memory** | Long-term $C_t$ + short-term $h_t$ | Single $h_t$ |
| **Training time** | Slower | ~20% faster |
| **Performance** | Slightly better (on large datasets) | Similar (competitive) |

**When to use:**
- LSTM: Large dataset, memory-rich task (translation, long documents)
- GRU: Quick experiments, resource-constrained (mobile, embedded)

---

## GRU (Gated Recurrent Unit)

### Q1: Explain reset and update gates

**Reset gate:** $r_t = \sigma(W_r[h_{t-1}, x_t])$
- Controls how much past to forget
- If $r_t = 0$: ignore all history (reset)

**Update gate:** $u_t = \sigma(W_u[h_{t-1}, x_t])$
- Controls how much past to keep
- If $u_t = 1$: copy past completely
- If $u_t = 0$: use new candidate

**Candidate:** $\tilde{h}_t = \tanh(W[r_t \odot h_{t-1}, x_t])$

**Update:** $h_t = (1-u_t) \odot h_{t-1} + u_t \odot \tilde{h}_t$

---

### Q2: GRU equation breakdown

$$r_t = \sigma(W_r h_{t-1} + U_r x_t)$$
$$u_t = \sigma(W_u h_{t-1} + U_u x_t)$$
$$\tilde{h}_t = \tanh(W_c (r_t \odot h_{t-1}) + U_c x_t)$$
$$h_t = u_t \odot h_{t-1} + (1-u_t) \odot \tilde{h}_t$$

**Why it works:** Gating allows selective memory (like LSTM) with fewer parameters.

---

