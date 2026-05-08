# 📝 Optimizers - Exam Answers

## Conceptual Q1: Why does momentum help in narrow valleys?

**Answer:**

**Momentum update:**
$$v_t = \beta v_{t-1} + g_t$$
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha v_t$$

where $\beta \approx 0.9$ (accumulation factor).

---

**Narrow valley problem:**

```
Loss L
  ^
  |   ╱╲
  |  ╱  ╲      Narrow valley: steep sides, gentle bottom
  | ╱    ╲___
  |╱________╲______ w
```

With naive gradient descent:
- Gradient perpendicular to contours
- Oscillates left-right (bouncing off steep sides)
- Slowly progresses down the valley

---

**Momentum solution:**

Accumulate velocity:
```
Iteration 1: Move left   (g_t = left)  → v = left
Iteration 2: Gradient right, but v from left → v = mostly left
Iteration 3: Continue left despite oscillating gradient
...
Result: Smooth motion down valley, ignoring noisy gradients
```

**Analogy:** Ball rolling down valley.

Without momentum: Bounces wildly (pure friction, no inertia)
With momentum: Builds up speed, smooths out oscillations (physics!)

---

**Mathematical view:**

Velocity averages past gradients:
$$v_t = \beta v_{t-1} + g_t = g_t + \beta g_{t-1} + \beta^2 g_{t-2} + \ldots$$

Exponentially weighted average of past gradients.

In narrow valleys where gradients oscillate, this averaging cancels noise and amplifies signal (downhill direction).

---

## Conceptual Q2: Why does Nesterov "look ahead"? How is it better than vanilla momentum?

**Answer:**

**Vanilla Momentum:**
$$v_t = \beta v_{t-1} + \nabla L(\mathbf{w}_t)$$
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha v_t$$

Gradient evaluated at **current position** $\mathbf{w}_t$.

---

**Nesterov Momentum:**
$$v_t = \beta v_{t-1} + \nabla L(\mathbf{w}_t - \alpha \beta v_{t-1})$$
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha v_t$$

Gradient evaluated at **"looked ahead" position** $\mathbf{w}_t - \alpha \beta v_{t-1}$.

---

**Why it's better:**

1. **Adaptive correction**
   - If you're about to overshoot (go too far), momentum detects it and corrects
   - Vanilla momentum: too late (already went too far)

2. **Faster convergence**
   - Nesterov: $O(1/T^2)$ for convex (faster than vanilla's $O(1/T)$)
   - Looks ahead to avoid bad directions

3. **Intuition: Predictive vs. Reactive**
   ```
   Vanilla:  "I'm here, gradient suggests go left"
   Nesterov: "I would go left next step. What's the gradient there?"
             "Oh no, it's uphill. Better slow down!"
   ```

---

## Conceptual Q3: Adagrad divides by $\sqrt{s_t}$, where $s_t = \sum_{\tau=1}^{t} (g_\tau)^2$. What happens over time? Why is this a problem?

**Answer:**

**Adagrad update:**
$$s_t = s_{t-1} + g_t^2$$
$$\mathbf{w}_t = \mathbf{w}_{t-1} - \frac{\alpha}{\sqrt{s_t + \epsilon}} g_t$$

---

**What happens over time:**

$s_t$ is **cumulative sum of squared gradients**.

As training progresses:
- $t=1$: $s_1 = g_1^2$ (small)
- $t=10$: $s_{10} = g_1^2 + \ldots + g_{10}^2$ (larger)
- $t=1000$: $s_{1000} = \text{huge}$

Denominator $\sqrt{s_t}$ grows **monotonically** and **forever**.

---

**Effect on learning rate:**

Effective learning rate: $\frac{\alpha}{\sqrt{s_t}}$

- Early training: large learning rate (fast)
- Middle: medium learning rate
- Late training: tiny learning rate → **converges to zero!**

$$\lim_{t \to \infty} \frac{\alpha}{\sqrt{s_t}} = 0$$

---

**Why it's a problem:**

1. **Training stops**
   - After enough iterations, learning rate → 0
   - Model stops learning even if not converged
   - Loss plateaus

2. **Can't escape local minima**
   - Too late in training, learning rate too small to make moves
   - Stuck even if minimum is not great

3. **Not suitable for deep learning**
   - Gradient magnitudes vary wildly in neural networks
   - Some weights stop learning while others still learning

---

**Solution:** RMSProp and Adam
- Exponential moving average instead of cumulative sum
- Prevents learning rate decay to zero
- Maintains adaptive per-parameter learning rates

---

## Derivation-Based Q1: Derive the velocity update in momentum: $v_t = \beta v_{t-1} + g_t$. Express $v_t$ as a sum of all past gradients.

**Answer:**

**Momentum recurrence:**
$$v_t = \beta v_{t-1} + g_t$$

---

**Expand recursively:**

$$v_t = \beta v_{t-1} + g_t$$
$$= \beta(\beta v_{t-2} + g_{t-1}) + g_t$$
$$= \beta^2 v_{t-2} + \beta g_{t-1} + g_t$$
$$= \beta^2(\beta v_{t-3} + g_{t-2}) + \beta g_{t-1} + g_t$$
$$= \beta^3 v_{t-3} + \beta^2 g_{t-2} + \beta g_{t-1} + g_t$$

Continuing:
$$v_t = \beta^t v_0 + \sum_{i=0}^{t-1} \beta^i g_{t-i}$$

Assuming $v_0 = 0$:

$$\boxed{v_t = \sum_{i=0}^{t-1} \beta^i g_{t-i} = g_t + \beta g_{t-1} + \beta^2 g_{t-2} + \ldots + \beta^{t-1} g_1}$$

---

**Interpretation:**

Velocity is **exponentially weighted average** of all past gradients.

- Recent gradients $g_t, g_{t-1}$: high weight ($\beta^0, \beta^1$)
- Old gradients $g_1$: low weight ($\beta^{t-1}$)
- With $\beta = 0.9$: effective history ≈ 10 gradients

---

## Derivation-Based Q2: Show that RMSProp with $\rho \to 1$ becomes Adagrad; with $\rho \to 0$ becomes SGD.

**Answer:**

**RMSProp update:**
$$s_t = \rho s_{t-1} + (1-\rho) g_t^2$$
$$\mathbf{w}_t = \mathbf{w}_{t-1} - \frac{\alpha}{\sqrt{s_t + \epsilon}} g_t$$

where $\rho \in (0, 1)$ is decay rate.

---

**Case 1: $\rho \to 1$**

$$s_t = \rho s_{t-1} + (1-\rho) g_t^2 \approx s_{t-1} + \epsilon \cdot g_t^2$$

(small $\epsilon = 1 - \rho$, can ignore)

$$s_t \approx s_{t-1} + g_t^2 = s_{t-2} + g_{t-1}^2 + g_t^2 = \sum_{\tau=1}^{t} g_\tau^2$$

**This is Adagrad!** Cumulative sum of squared gradients.

---

**Case 2: $\rho \to 0$**

$$s_t = \rho s_{t-1} + (1-\rho) g_t^2 \approx 0 + 1 \cdot g_t^2 = g_t^2$$

(only current gradient, ignore past)

$$\mathbf{w}_t = \mathbf{w}_{t-1} - \frac{\alpha}{\sqrt{g_t^2}} g_t = \mathbf{w}_{t-1} - \frac{\alpha}{|g_t|} g_t$$

This is essentially **SGD with normalized gradient** (nearly standard SGD).

---

**Summary:**
- RMSProp is interpolation between Adagrad ($\rho=1$) and SGD ($\rho=0$)
- Typical choice: $\rho = 0.999$ (mostly history, small decay) → good generalization

---

## Trick/Failure Cases

### Q1: You train with Adagrad for 1000 epochs. At epoch 100, accuracy plateaus despite high loss. Why?

**Answer:**

**Diagnosis:** Adagrad's learning rate decayed to near-zero.

By epoch 100:
$$s_t = \sum_{\tau=1}^{100 \times \text{batch_size}} g_\tau^2 = \text{huge number}$$

Effective learning rate:
$$\frac{\alpha}{\sqrt{s_t}} \approx \frac{0.01}{\sqrt{\text{huge}}} \approx \text{tiny}$$

Model can no longer make meaningful weight updates → accuracy stagnates (loss doesn't decrease).

---

**Fix:**

1. **Switch to RMSProp or Adam** (exponential moving average instead)
2. **Reduce Adagrad decay** (less aggressive second moment accumulation)
3. **Checkpoint early** (stop at epoch 50 when still learning)
4. **Learning rate schedule** (reset or anneal learning rate periodically)

**Lesson:** Adagrad good for sparse gradients, but bad for long training. RMSProp/Adam are more robust.

---

### Q2: Momentum with $\beta = 0.95$ vs. $\beta = 0.99$. Which converges faster? Which oscillates less?

**Answer:**

**Recall velocity:**
$$v_t = \sum_{i=0}^{t-1} \beta^i g_{t-i}$$

---

**$\beta = 0.95$ (lower):**
- Weights: $1, 0.95, 0.90, 0.86, \ldots$ (decay fast)
- Effective history: ~20 gradients (more recent-focused)
- **Oscillates more:** Responds quickly to gradient changes
- **Converges faster:** Quick to follow gradients

---

**$\beta = 0.99$ (higher):**
- Weights: $1, 0.99, 0.98, 0.97, \ldots$ (decay slow)
- Effective history: ~100 gradients (long-term memory)
- **Oscillates less:** Smooths out noisy gradients
- **Converges slower:** Takes longer to adjust to new directions

---

**Tradeoff:**
```
β=0.95: Wiggly path, reaches local min quickly
β=0.99: Smooth path, reaches min later but more stable
```

**In practice:**
- $\beta=0.9$ for faster convergence (default for vanilla SGD + momentum)
- $\beta=0.99$ for Adam/RMSProp (more stability, already has other noise reduction)

