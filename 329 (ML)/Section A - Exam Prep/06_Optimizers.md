# 📘 Optimizers (Momentum, Nesterov, Adagrad, RMSProp)

## 1. Core Idea (Intuition)

Basic **SGD** $\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \nabla L(\mathbf{w}_t)$ has issues:
- **Slow in flat regions** (small gradient)
- **Oscillates in narrow valleys** (large gradient in one direction)
- **No adaptive learning rates** (same $\alpha$ for all parameters)

**Optimizers fix this by:**
1. **Momentum:** Accumulate velocity to accelerate through flat regions
2. **Adaptive rates:** Different $\alpha$ per parameter based on history

---

## 2. Momentum

### Intuition
Add **inertia** to weight updates. Like a ball rolling downhill: once it gains velocity, it keeps moving even in flat regions.

### Formulation
$$\mathbf{v}_t = \beta \mathbf{v}_{t-1} + \nabla L(\mathbf{w}_t)$$

$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \mathbf{v}_t$$

where:
- $\mathbf{v}_t$: velocity (accumulated gradient)
- $\beta \in [0.9, 0.99]$: momentum coefficient
- $\mathbf{v}_0 = 0$: initialize to zero

### Effect

| Term | Contribution |
|------|--------------|
| Current gradient $\nabla L(\mathbf{w}_t)$ | **1x** (weight 1) |
| Previous velocity $\beta \mathbf{v}_{t-1}$ | Exponential sum of all past gradients |

$$\mathbf{v}_t = \nabla L(\mathbf{w}_t) + \beta \nabla L(\mathbf{w}_{t-1}) + \beta^2 \nabla L(\mathbf{w}_{t-2}) + \cdots$$

**Effect:** Smooth updates; accelerate in consistent directions; dampen oscillations.

### Effective Learning Rate
In a valley with gradient direction oscillating, momentum averages out oscillations, accelerating movement.

---

## 3. Nesterov Momentum

### Problem with Vanilla Momentum
Momentum accumulates old gradients. By the time velocity is high, we may have passed the optimum.

### Solution: Look Ahead
Evaluate gradient at **future position** before committing to update.

$$\mathbf{v}_t = \beta \mathbf{v}_{t-1} + \nabla L(\mathbf{w}_t - \alpha \beta \mathbf{v}_{t-1})$$

$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \mathbf{v}_t$$

**Intuition:** First move according to velocity ($-\alpha \beta \mathbf{v}_{t-1}$), then compute gradient at that "future" position.

### Practical Form (Equivalent)
```
Compute g = ∇L(w - α·β·v)
v ← β·v + g
w ← w - α·v
```

### Convergence Rate
- **Momentum:** $O(1/T)$ (same as BGD, but faster constant)
- **Nesterov:** $O(1/T^2)$ for convex problems (theoretically better!)

---

## 4. Adagrad (Adaptive Gradient)

### Problem
Some parameters have large gradients, others small. Momentum treats all equally.

### Solution: Adaptive Per-Parameter Learning Rates

$$\mathbf{s}_t = \mathbf{s}_{t-1} + (\nabla L(\mathbf{w}_t))^2 \quad \text{(element-wise)}$$

$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \frac{\nabla L(\mathbf{w}_t)}{\sqrt{\mathbf{s}_t + \epsilon}}$$

where:
- $\mathbf{s}_t$: sum of squared gradients (accumulates over time)
- $\epsilon \approx 10^{-8}$: prevent division by zero
- $\sqrt{\mathbf{s}_t}$ is element-wise

### Effect

| Parameter | Large gradients early | Small gradients early |
|-----------|----------------------|----------------------|
| $\mathbf{s}_t$ | Grows fast | Stays small |
| $\frac{\alpha}{\sqrt{\mathbf{s}_t}}$ | Effective $\alpha$ **decreases** | Effective $\alpha$ **increases** |

**Result:** Parameters with large past gradients learn slower; parameters with small past gradients learn faster.

### Problem
$\mathbf{s}_t$ accumulates indefinitely. After many steps, $\sqrt{\mathbf{s}_t}$ becomes huge, and learning effectively stops.

---

## 5. RMSProp (Root Mean Square Propagation)

### Problem with Adagrad
Accumulation of $\mathbf{s}_t$ causes learning rate to decay to zero.

### Solution: Exponential Moving Average
Instead of accumulating all past squared gradients, use **recent history**:

$$\mathbf{s}_t = \rho \mathbf{s}_{t-1} + (1-\rho) (\nabla L(\mathbf{w}_t))^2$$

$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \frac{\nabla L(\mathbf{w}_t)}{\sqrt{\mathbf{s}_t + \epsilon}}$$

where $\rho \in [0.9, 0.99]$ is the decay rate.

### Effect
- **Recent gradients** weighted heavily (coefficient $1-\rho$)
- **Old gradients** decay exponentially (weight $\rho^k$)
- Learning rate doesn't decay to zero (unlike Adagrad)

---

## 6. Comparison Table (Momentum, Nesterov, Adagrad, RMSProp, Adam)

| Optimizer | Update Rule | Key Insight | Best For |
|-----------|-------------|------------|----------|
| **SGD** | $w_t - \alpha g_t$ | Simple baseline | Theory, interpretability |
| **Momentum** | $v_t = \beta v_{t-1} + g_t$ | Accumulate velocity | Convex, smooth problems |
| **Nesterov** | Gradient at future position | Look-ahead | Theory |
| **Adagrad** | $w_t - \alpha \frac{g_t}{\sqrt{\sum g_\tau^2}}$ | Per-parameter scaling | Sparse data (NLP) |
| **RMSProp** | $w_t - \alpha \frac{g_t}{\sqrt{\rho \mathbf{v}_{t-1} + (1-\rho) g_t^2}}$ | Adaptive, no decay | Pre-Adam method |
| **Adam** ⭐ | $w_t - \alpha \frac{\hat{m}_t}{\sqrt{\hat{v}_t}}$ | **Momentum + adaptive** | **Modern default** |

---

## 7. Adam (Adaptive Moment Estimation)

### Core Idea
Combines **two strategies:**
1. **Momentum:** First moment (mean of gradients)
2. **RMSProp:** Second moment (variance of gradients)

Result: Adaptive learning rates + acceleration through flat regions.

---

### Formulation

**Step 1: Update biased first moment (momentum)**
$$\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1-\beta_1) \nabla L(\mathbf{w}_t)$$

**Step 2: Update biased second moment (adaptive rates)**
$$\mathbf{v}_t = \beta_2 \mathbf{v}_{t-1} + (1-\beta_2) (\nabla L(\mathbf{w}_t))^2$$

**Step 3: Correct bias (crucial early in training)**
$$\hat{\mathbf{m}}_t = \frac{\mathbf{m}_t}{1 - \beta_1^t}$$

$$\hat{\mathbf{v}}_t = \frac{\mathbf{v}_t}{1 - \beta_2^t}$$

**Step 4: Update weights**
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \frac{\hat{\mathbf{m}}_t}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon}$$

---

### Explanation of Each Component

**First moment $\mathbf{m}_t$:**
- Exponential moving average of gradients (like momentum)
- $\beta_1 \approx 0.9$ (default): weight past gradients heavily (retain history)
- Current gradient weight = $1 - \beta_1 = 0.1$ (only 10% of current gradient)
- Accelerates movement in consistent directions

**Second moment $\mathbf{v}_t$:**
- Exponential moving average of squared gradients (like RMSProp)
- $\beta_2 \approx 0.999$ (default): weight past squared gradients heavily (retain history)
- Current squared gradient weight = $1 - \beta_2 = 0.001$ (only 0.1% of current squared gradient)
- Larger squared gradients → smaller effective learning rate (adaptive scaling)

**Bias correction $\hat{\mathbf{m}}_t, \hat{\mathbf{v}}_t$:**
- Initially, $\mathbf{m}_0 = \mathbf{v}_0 = 0$
- At $t=1$: $\mathbf{m}_1 = (1-\beta_1) g_1$ (very small!)
- Denominator $1-\beta_1^t$ corrects this: at $t=1$, divide by $(1-0.9) = 0.1$
- **Effect:** Removes initialization bias; more stable early training

---

### Intuition: Why Combine Both Moments?

| Scenario | Momentum Alone | Adaptive Rates Alone | Adam |
|----------|---|---|---|
| **Flat region** | Velocity builds (past gradients accumulate) → accelerates ✓ | No help; small gradients → slow | **Both:** Builds velocity + adapts rate ✓ |
| **Steep region** | Overshoots (momentum carries through) | Reduces learning rate → stable ✓ | **Both:** Reduces rate + dampens velocity ✓ |
| **Sparse features** | Same learning rate for all | Different rates per parameter ✓ | **Both:** Per-parameter adaptive rates ✓ |
| **Dense features** | Large momentum (high $\beta_1$) | May oscillate | **Both:** Stabilized momentum ✓ |

**Example:**
```
Loss landscape: Flat region → steep valley → flat plateau

With SGD:     crawl → oscillate heavily → crawl
With Momentum: accelerate → overshoot → oscillate
With RMSProp:  crawl → stable descent → crawl
With Adam:     accelerate through flat → stable in valley → accelerate again ✓
```

---

### Default Hyperparameters

**Almost universal settings:**
$$\beta_1 = 0.9, \quad \beta_2 = 0.999, \quad \epsilon = 10^{-8}$$

**Learning rate varies:**
- **General neural networks:** $\alpha = 10^{-3}$ to $10^{-4}$ (start with $10^{-3}$)
- **Fine-tuning pretrained models:** $\alpha = 10^{-5}$ to $10^{-6}$
- **Very large models:** $\alpha = 10^{-4}$ to $10^{-5}$

**Learning rate decay (optional):**
- Many people use constant $\alpha$ (Adam naturally decays effective learning rate)
- Some use: $\alpha_t = \alpha_0 \cdot 0.99^t$ (gentle decay)

---

### Why Keep Beta High in Real Life?

**Yes, we keep $\beta_1 = 0.9$ and $\beta_2 = 0.999$ in practice. Here's why:**

| Beta Value | Effect | Example |
|-----------|--------|---------|
| **$\beta_1 = 0.9$ (high)** | Retain 90% past velocity; current gradient = 10% | Smooth momentum, stable acceleration |
| **$\beta_1 = 0.5$ (low)** | Only 50% past velocity; current gradient = 50% | Noisy, jerky updates; follows gradients too closely |
| **$\beta_1 = 0.99$ (very high)** | Retain 99% past velocity; current gradient = 1% | Can overshoot minima; slow to adapt to direction changes |

**Real-world behavior:**
- **$\beta_1 = 0.9$:** Balances stability (remembers history) + responsiveness (reacts to new gradients)
- **Deviating from 0.9:** Rarely done; empirical testing shows 0.9 works across ~95% of problems
- **Why not lower?** Low $\beta$ = more noisy updates = slower convergence
- **Why not higher?** High $\beta$ = momentum doesn't adapt fast enough = may miss direction changes

**Same logic for $\beta_2 = 0.999$:**
- Keeps adaptive learning rate stable (smooth per-parameter scaling)
- Doesn't overreact to single large gradient
- Prevents premature decay of learning rate

**Practical rule:** Use $\beta_1 = 0.9, \beta_2 = 0.999$ unless you have specific reason to change. Changing these is rare; focus on tuning $\alpha$ instead.

---

### Bias Correction Details

**Why is bias correction important?**

At iteration $t=1$:
```
Without correction:
  m₁ = (1-0.9) × g₁ = 0.1 × g₁ (too small!)
  Update: w ← w - α × 0.1 × g₁ (barely moves)

With correction (β₁ = 0.9):
  m̂₁ = m₁ / (1 - 0.9^1) = (0.1 × g₁) / 0.1 = g₁ (correct!)
  Update: w ← w - α × g₁ (proper step)
```

**When does it matter?**
- **Early training (first ~100 iterations):** Significant difference
- **Later training (t > 1000):** $(1-\beta_1^t) \approx 1$, minimal effect
- **With initialization bias:** Model takes longer to converge without correction

---

### Practical Algorithm (Step-by-Step)

```
Initialize:
  m = 0, v = 0, t = 0

For each batch:
  t += 1
  g = ∇L(w)  // compute gradient
  
  m = 0.9 * m + (1-0.9) * g  // update first moment
  v = 0.999 * v + (1-0.999) * g²  // update second moment
  
  m_hat = m / (1 - 0.9^t)  // bias-corrected first moment
  v_hat = v / (1 - 0.999^t)  // bias-corrected second moment
  
  w = w - 0.001 * m_hat / (√v_hat + 1e-8)  // update weights
```

---

### Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| **Training loss not decreasing** | Learning rate too high | Reduce α (try α/10) |
| **Training extremely slow** | Learning rate too low | Increase α (try α×10) |
| **Loss unstable / spikes** | Learning rate too high OR batch size too small | Reduce α or increase batch size |
| **Doesn't improve after 10 epochs** | Stuck at bad initialization | Use better learning rate or batch normalization |
| **Training diverges (loss → NaN)** | Learning rate way too high | Reduce α significantly |

---

### Adam vs. Other Optimizers

| Optimizer | Pros | Cons | When to Use |
|-----------|------|------|------------|
| **SGD** | Simple, interpretable | Slow, oscillates | Toy problems, theory |
| **Momentum** | Faster than SGD | Still oscillates in valleys | Convex problems |
| **RMSProp** | Adaptive, good for sparse data | Needs tuning | Older method; use Adam instead |
| **Adam** | Works everywhere, adaptive, no decay | More memory (stores m, v) | **Default choice for deep learning** |
| **Nesterov** | Better theory | Slower in practice | Research, convex optimization |

---

### Relationship to RMSProp

**RMSProp:** $\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \frac{g_t}{\sqrt{\mathbf{v}_t + \epsilon}}$

**Adam:** $\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \frac{\hat{\mathbf{m}}_t}{\sqrt{\hat{\mathbf{v}}_t} + \epsilon}$

**Difference:** Adam replaces raw gradient $g_t$ with momentum-adjusted $\hat{\mathbf{m}}_t$

This adds acceleration while keeping per-parameter adaptive rates.

---

## 8. Failure Cases / Pitfalls

| Problem | Why | Fix |
|---------|-----|-----|
| **Learning rate too high** | Optimizer amplifies steps further | Reduce $\alpha$ |
| **Learning rate too low** | Even with momentum, slow convergence | Increase $\alpha$ |
| **Momentum too high ($\beta > 0.99$)** | Overshoots minima | Reduce $\beta$ to 0.9-0.95 |
| **Adagrad in long training** | Learning rate decays to zero | Switch to RMSProp or Adam |
| **Different scales per parameter** | Some parameters dominate | Use feature normalization |

---

## 9. Exam Questions

### Conceptual
1. Explain momentum with an analogy. Why is $\beta = 0.9$ better than $\beta = 0.99$ in narrow valleys?
2. Adam combines two moments. What does first moment $\mathbf{m}_t$ do? What does second moment $\mathbf{v}_t$ do?
3. Why does Adam include bias correction? What problem does $\hat{\mathbf{m}}_t = \mathbf{m}_t / (1-\beta_1^t)$ solve?
4. Adagrad divides by $\sqrt{\sum g_\tau^2}$ (sum grows indefinitely). Why is this a problem? How does RMSProp/Adam fix it?

### Application / Scenario-Based
1. You're training a deep neural network. Which optimizer should you use: SGD, Momentum, RMSProp, or Adam? Why?
2. Your training loss decreases smoothly but training is very slow. Would higher $\beta_1$ (more momentum) help or hurt? Why?
3. You trained with Adam and got 90% validation accuracy in 20 epochs. You switch to SGD with the same learning rate and it diverges. Explain why.
4. Adam has $\beta_1 = 0.9$ and $\beta_2 = 0.999$. What would happen if you swapped them ($\beta_1 = 0.999$, $\beta_2 = 0.9$)? Would it still work?

### Trick/Failure Cases
1. You train with Adam and loss goes: [0.5, 0.4, 0.3, NaN]. What happened? How to fix?
2. Two training runs: Run A uses Adam with $\alpha = 10^{-3}$, Run B uses RMSProp with $\alpha = 10^{-2}$. Run A converges in 50 epochs, Run B takes 200. Why?
3. Adam's bias correction factor is $\frac{1}{1-\beta_1^t}$. At $t=100$ with $\beta_1=0.9$, what is this factor approximately? Does it matter?

---

## 10. Practical Recommendations

| Scenario | Recommended Optimizer | Learning Rate |
|----------|----------------------|----------------|
| Convex optimization | **Nesterov** or **RMSProp** | $10^{-2}$ to $10^{-1}$ |
| Neural networks (default) | **Adam** | $10^{-3}$ (start here) |
| Sparse data (NLP) | **Adagrad** | $10^{-2}$ |
| Fine-tuning | **SGD + momentum** ($\beta = 0.9$) | $10^{-4}$ to $10^{-5}$ |
| No clue | **Adam** | $10^{-3}$ (safe default) |

---

## 11. Key Takeaways

**Core Concepts:**
- **Momentum:** $v_t = \beta v_{t-1} + g_t$; accumulates velocity to accelerate through flat regions
- **Adagrad:** Divides by $\sqrt{\sum g_\tau^2}$; adaptive rates but learning rate decays to zero
- **RMSProp:** Uses exponential moving average $\sqrt{\rho v_{t-1} + (1-\rho) g_t^2}$; fixes Adagrad decay
- **Nesterov:** Evaluates gradient at future position; better theoretical convergence rate

**Adam (Most Important for Syllabus):**
- **Combines:** First moment $\mathbf{m}_t$ (momentum) + Second moment $\mathbf{v}_t$ (adaptive rates)
- **Bias correction:** $\hat{\mathbf{m}}_t = \mathbf{m}_t / (1-\beta_1^t)$ ensures stable early training
- **Default hyperparameters:** $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\alpha = 10^{-3}$ to $10^{-4}$
- **Why Adam works:** Accelerates through flat regions + stabilizes steep regions + adapts per-parameter
- **Modern default:** Adam is the recommended optimizer for ~95% of deep learning tasks

**Practical:**
- **For neural networks:** Use Adam (unless explicitly told otherwise)
- **For sparse data (NLP):** Adagrad can work, but Adam is safer
- **For fine-tuning:** SGD with momentum ($\beta=0.9$) with small learning rate
- **Trade-off:** More complex optimizers = better performance but more hyperparameters to tune
