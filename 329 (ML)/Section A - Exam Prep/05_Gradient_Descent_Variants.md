# 📘 Gradient Descent Variants

## 1. Core Idea (Intuition)

**Gradient Descent** is an **iterative optimization algorithm** that updates weights in the direction opposite to the gradient:

$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \nabla L(\mathbf{w}_t)$$

The "variant" question: **How much data to use per gradient step?**

---

## 1.5. Understanding Iterations, Epochs, and the Training Loop

### Terminology

**Iteration:** One weight update. Compute gradient on some data, then update weights once.

**Epoch:** One pass through **entire dataset**. After each epoch, you've used all $n$ samples.

**Batch:** A subset of samples used in one iteration.

---

### How Many Iterations Per Epoch?

**Formula:**
$$\text{iterations per epoch} = \frac{n}{\text{batch size}}$$

where:
- $n$ = total number of samples
- batch size = samples used per iteration

**Examples with $n = 1000$ samples:**

| Method | Batch Size | Iterations per Epoch |
|--------|-----------|----------------------|
| **BGD** | 1000 | $1000 / 1000 = 1$ |
| **Mini-batch** | 32 | $1000 / 32 \approx 31$ |
| **Mini-batch** | 128 | $1000 / 128 \approx 8$ |
| **SGD** | 1 | $1000 / 1 = 1000$ |

---

### The Training Loop (Pseudocode)

**Generic template:**
```
for epoch = 1 to num_epochs:
    for iteration = 1 to iterations_per_epoch:
        batch ← sample batch_size samples randomly
        gradient ← compute_gradient(batch, w)
        w ← w - α * gradient
    
    validation_error ← evaluate on validation set
    print(f"Epoch {epoch}: train loss = {...}, val loss = {validation_error}")
```

---

### Concrete Example: Mini-batch with 1000 Samples, Batch Size 32

**Setup:**
- Dataset: 1000 samples
- Batch size: 32
- Learning rate: α = 0.01
- Epochs to train: 3

**Execution timeline:**

```
EPOCH 1:
  Iteration 1:  samples 1-32      → compute gradient → update w
  Iteration 2:  samples 33-64     → compute gradient → update w
  Iteration 3:  samples 65-96     → compute gradient → update w
  ...
  Iteration 31: samples 961-992   → compute gradient → update w
  (total: 1000/32 ≈ 31 iterations)
  
  End of epoch 1: w has been updated 31 times
                  All 1000 samples seen once

EPOCH 2:
  Shuffle data randomly (important!)
  Iteration 1:  samples 523, 100, 412, ... (32 random samples) → update w
  Iteration 2:  samples 50, 802, 199, ... (32 different random) → update w
  ...
  Iteration 31: (final batch)
  
  End of epoch 2: w has been updated 62 times total (31 from epoch 1 + 31 from epoch 2)

EPOCH 3:
  ... (31 more iterations)
  
  End of epoch 3: w has been updated 93 times total
```

**Key insight:** Over 3 epochs, 1000 samples, batch size 32:
- Total iterations = 3 × 31 = 93
- Total samples processed = 3 × 1000 = 3000 (each sample seen ~3 times)
- Total weight updates = 93

---

### Updates Per Epoch Formula

$$\text{iterations per epoch} = \lceil n / B \rceil$$

where:
- $n$ = number of training samples
- $B$ = batch size
- $\lceil \rceil$ = ceiling (round up)

**Example:**
- $n = 1000$, $B = 32$ → $\lceil 1000 / 32 \rceil = \lceil 31.25 \rceil = 31$ iterations per epoch

---

### Calculating Time & Speed

#### Cost Per Iteration

**For each iteration, you compute:**
1. **Forward pass:** Predict $\hat{y} = X_{\text{batch}} \mathbf{w}$ → $O(B \cdot d)$
2. **Loss computation:** Compute $L = \frac{1}{B}\sum_{i} (y_i - \hat{y}_i)^2$ → $O(B)$
3. **Backward pass:** Compute $\nabla L$ via backprop → $O(B \cdot d)$ (for linear models)
4. **Weight update:** $\mathbf{w} ← \mathbf{w} - \alpha \nabla L$ → $O(d)$

**Total per iteration:** $O(B \cdot d)$ (dominated by forward/backward)

---

#### Wall-Clock Time Calculation

**Time per iteration depends on hardware:**
- GPU: ~1-10 ms per iteration (parallelized)
- CPU: ~10-100 ms per iteration
- Depends on: $B$, $d$, hardware, implementation

**Rough estimates:**
```
GPU with B=32, d=10000:
  Forward pass: 1-2 ms
  Backward pass: 1-2 ms
  Update: <0.1 ms
  Total: ~2-4 ms per iteration

With 1000 samples, B=32:
  Iterations per epoch: 31
  Time per epoch: 31 × 3 ms = 93 ms ≈ 0.1 seconds
  
  For 100 epochs: 10 seconds total training time
```

---

#### Updates Per Second

$$\text{updates per second} = \frac{1}{\text{time per iteration (seconds)}}$$

**Example:**
```
Time per iteration: 2 ms = 0.002 seconds
Updates per second: 1 / 0.002 = 500 updates/second
```

---

### Step-by-Step Example: One Epoch of Mini-batch GD

**Dataset:** 100 samples, 3 features
$$X = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ \vdots \\ 97 & 98 & 99 \end{bmatrix}, \quad y = \begin{bmatrix} 10 \\ 20 \\ \vdots \\ 295 \end{bmatrix}$$

**Setup:** Batch size = 20, learning rate = 0.01

**Epoch 1 execution:**

```
Initial: w = [0, 0, 0]

===== ITERATION 1 =====
Batch: samples 1-20
Forward:  ŷ = X[1:20] @ w = [1×0, 4×0, ...] = [0, 0, ..., 0]  (all predictions are 0)
Loss:     L = mean((y[1:20] - 0)²) = mean([100, 400, ...]) ≈ 1500
Gradient: ∇L = (1/20) × X[1:20]ᵀ(ŷ - y[1:20]) 
          = (1/20) × X[1:20]ᵀ([0,0,...,0] - [10,20,...,200])
          = -(1/20) × X[1:20]ᵀ × [10,20,...,200]
          ≈ [-45, -50, -55]  (rough numbers)
Update:   w ← w - 0.01 × [-45, -50, -55]
             = [0, 0, 0] - [-0.45, -0.50, -0.55]
             = [0.45, 0.50, 0.55]

===== ITERATION 2 =====
Batch: samples 21-40
Forward:  ŷ = X[21:40] @ [0.45, 0.50, 0.55]
Loss:     L ≈ 1200 (lower than before, improving!)
Gradient: ∇L ≈ [-40, -42, -44]
Update:   w ← [0.45, 0.50, 0.55] - 0.01 × [-40, -42, -44]
             = [0.85, 0.92, 0.99]

===== ITERATION 3 =====
Batch: samples 41-60
... (similar process)
Loss: ≈ 950 (continues improving)

... (iterations 4-5 for remaining batches)

===== END OF EPOCH 1 =====
Total iterations: 5 (since 100 / 20 = 5 batches)
Total weight updates: 5
w after epoch 1: ≈ [3.5, 4.2, 4.8] (rough estimate)

Epoch 1 loss: ≈ 200 (average over 5 batches)
```

---

### Comparison: BGD vs SGD vs Mini-batch

**For 1000 samples with $d=100$ features, 1 epoch:**

**BGD (batch size = 1000):**
```
Iteration 1:
  Load all 1000 samples
  Compute gradient on all 1000 samples: O(1000 × 100) = O(100,000) operations
  Update w once
  
Time: 
  ~100 ms per iteration
  1 iteration per epoch
  Total: 100 ms per epoch
  
After 100 epochs: 10 seconds
```

**SGD (batch size = 1):**
```
Iteration 1: Load sample 1, gradient on 1 sample: O(1 × 100), update w
Iteration 2: Load sample 2, gradient on 1 sample: O(1 × 100), update w
...
Iteration 1000: Load sample 1000, gradient on 1 sample: O(1 × 100), update w

Time:
  ~0.2 ms per iteration (very fast, minimal data)
  1000 iterations per epoch
  Total: 1000 × 0.2 ms = 200 ms per epoch
  
After 100 epochs: 20 seconds

BUT: Each iteration is smaller-scale, so more total time compared to BGD
    But better parallelization on GPU can make it faster!
```

**Mini-batch (batch size = 32):**
```
Iteration 1: Load samples 1-32, gradient: O(32 × 100), update w
Iteration 2: Load samples 33-64, gradient: O(32 × 100), update w
...
Iteration 31: Load samples 961-992, gradient: O(32 × 100), update w

Time:
  ~3 ms per iteration (balanced)
  31 iterations per epoch
  Total: 31 × 3 ms = 93 ms per epoch ≈ 0.1 seconds
  
After 100 epochs: 10 seconds

This is the sweet spot: Fast per iteration AND not too many iterations!
```

---

### Key Takeaway: Why Mini-batch Wins

| Method | Time/Iteration | Iterations/Epoch | Total Time/Epoch |
|--------|----------------|------------------|------------------|
| **BGD** | 100 ms | 1 | ~100 ms |
| **SGD** | 0.2 ms | 1000 | ~200 ms |
| **Mini-batch** | 3 ms | 31 | ~93 ms ≈ **fastest in practice** |

Mini-batch balances:
- Fast per iteration (like SGD)
- Reasonable number of iterations (like BGD)
- Great GPU parallelization
- Stable gradient (larger batch)

**This is why mini-batch is the standard!**

---

## 2. Three Main Variants

### Variant 1: Batch Gradient Descent (BGD)

**Update using entire dataset:**
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \cdot \frac{1}{n} \sum_{i=1}^{n} \nabla L_i(\mathbf{w}_t)$$

where $L_i$ is loss for sample $i$.

| Property | Value |
|----------|-------|
| **Gradient noise** | None (exact gradient) |
| **Computational cost per step** | $O(nd)$ |
| **Updates per epoch** | 1 |
| **Memory required** | All data in memory |
| **Convergence** | Smooth, but slow |

**When to use:** Small datasets ($n < 10^5$), need stable convergence.

---

### Variant 2: Stochastic Gradient Descent (SGD)

**Update using one sample at a time:**
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \cdot \nabla L_i(\mathbf{w}_t) \quad \text{(pick random sample } i \text{)}$$

| Property | Value |
|----------|-------|
| **Gradient noise** | High (one sample = high variance) |
| **Computational cost per step** | $O(d)$ |
| **Updates per epoch** | $n$ |
| **Memory required** | One sample at a time |
| **Convergence** | Noisy, but escapes local minima |

**When to use:** Large datasets, online learning, need to escape saddle points.

---

### Variant 3: Mini-batch Gradient Descent

**Update using $B$ samples (batch):**
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \cdot \frac{1}{B} \sum_{i \in \text{batch}} \nabla L_i(\mathbf{w}_t)$$

| Property | Value |
|----------|-------|
| **Gradient noise** | Medium (trades bias-variance) |
| **Computational cost per step** | $O(Bd)$ |
| **Updates per epoch** | $n/B$ |
| **Memory required** | $B$ samples in memory |
| **Convergence** | Balanced; practical gold standard |

**Typical batch sizes:** 32, 64, 128, 256.

**When to use:** Most practical scenarios (default choice).

---

## 3. Convergence Comparison

### Mathematical Analysis

For **convex loss** $L(\mathbf{w})$ with Lipschitz gradient:

| Variant | Convergence Rate | After $T$ Steps |
|---------|------------------|-----------------|
| **BGD** | $O(1/T)$ | Error $\sim 1/T$ |
| **SGD** | $O(1/\sqrt{T})$ | Error $\sim 1/\sqrt{T}$ |
| **Mini-batch** | $O(1/\sqrt{T})$ | Error $\sim 1/\sqrt{T}$ (with lower constant) |

**Interpretation:**
- **BGD:** Slower per step, but fewer steps needed ($1/T$ is better than $1/\sqrt{T}$)
- **SGD/Mini-batch:** More steps, but much cheaper per step
- **In practice:** Mini-batch wins due to parallelization and GPU efficiency

---

## 4. Gradient Noise & Generalization

### Why Noise Helps

**Gradient noise acts as implicit regularization:**

1. **Escaping sharp minima:** Sharp minima have large curvature; SGD noise helps skip over them
2. **Exploring wider minima:** Flat minima generalize better; noise favors flat solutions
3. **Convergence to different solutions:** Different batches → different trajectories → different final weights

**Theorem:** For convex functions, SGD with decreasing learning rate converges to optimal $\mathbf{w}^*$.

---

## 5. Learning Rate Scheduling

Adaptive learning rate: $\alpha_t = \alpha_0 / (1 + \beta t)$ or $\alpha_t = \alpha_0 \cdot 0.99^t$.


### Common Learning Rate Schedules (with Explanations)

| Schedule | Formula | Explanation | Use Case |
|----------|---------|-------------|----------|
| **Constant** | $\alpha_t = \alpha$ | The learning rate stays fixed throughout training. Simple to implement, but requires careful tuning. If too high, training may diverge; if too low, convergence is slow. | Stable convergence (if $\alpha$ well-tuned) |
| **Step decay** | $\alpha_t = \alpha_0 \cdot \gamma^{\lfloor t/s \rfloor}$ | The learning rate drops by a factor $\gamma$ every $s$ steps (epochs or iterations). This allows for larger steps early on, then smaller, more precise steps as training progresses. | Reduce learning rate every $s$ steps |
| **Exponential decay** | $\alpha_t = \alpha_0 \cdot e^{-\beta t}$ | The learning rate decreases smoothly and continuously as training proceeds. $\beta$ controls the rate of decay. Useful for gradually reducing step size without abrupt changes. | Smooth decrease |
| **Cosine annealing** | $\alpha_t = \frac{\alpha_0}{2}(1 + \cos(\pi t/T))$ | The learning rate follows a cosine curve, starting high, decreasing to near zero, and (optionally) restarting. Helps escape local minima and improves generalization in deep learning. | Modern deep learning |

**Summary:**
- **Constant:** Good if you know the best learning rate in advance; not adaptive.
- **Step decay:** Mimics manual learning rate drops; common in classic deep learning.
- **Exponential decay:** Smooth, automatic reduction; less abrupt than step decay.
- **Cosine annealing:** Popular in state-of-the-art models; can be combined with restarts for better results.

---

## 6. Failure Cases & Pitfalls

| Problem | Why | Impact |
|---------|-----|--------|
| **Batch size too small** | High gradient noise | Noisy training, poor convergence |
| **Batch size too large** | Approximates BGD | Slow, stuck in sharp minima |
| **Learning rate too high** | Overshooting | Divergence, loss oscillates |
| **Learning rate too low** | Underfitting on time | Slow, may not converge in reasonable time |
| **Non-shuffled batches** | Autocorrelated gradients | Biased updates; poor learning |

---

## 7. When to Use Each Variant

| Scenario | Best Variant |
|----------|-------------|
| Small dataset ($n < 1000$) | **BGD** (stable, interpretable) |
| Large dataset, need speed | **SGD** (minimum memory) |
| Real-world project | **Mini-batch SGD** (balance of speed & stability) |
| Online learning (streaming data) | **SGD** (one sample at a time) |
| Limited GPU memory | **Small mini-batch or SGD** |

---

## 8. Exam Questions

### Conceptual
1. Why does SGD with batch size 1 converge slower per epoch than BGD, but potentially faster in wall-clock time?
2. Why does SGD escape local minima better than BGD? (Hint: think about noise and sharp vs. flat minima.)
3. What happens to the gradient estimate if you shuffle data between epochs in mini-batch GD?

### Application / Scenario-Based
1. You're training a neural network on a dataset with 1 million samples. Your GPU memory can hold 256 samples at once. Should you use BGD, SGD, or mini-batch? Why? What batch size would you pick?
2. Your training loss decreases smoothly, but the loss oscillates wildly every few epochs. What's likely happening? How would you fix it?
3. You're deploying a model in production that needs to update on streaming data (new samples arriving continuously). Which gradient descent variant would you use and why?
4. Your SGD training diverges (loss → ∞) when you double the learning rate. But your friend's mini-batch training with the same learning rate works fine. Explain why.

### Trick/Failure Cases
1. Your mini-batch GD achieves 95% train accuracy in 10 epochs. BGD with same learning rate takes 100 epochs. Why?
2. You switch from batch size 256 to 1024 (4x larger). To maintain same convergence speed, what should you change and by how much?

---

## 9. Key Takeaways

- **BGD:** Exact gradient, stable, slow per step ($O(1/T)$ convergence)
- **SGD:** Noisy gradient, fast per step, escapes minima ($O(1/\sqrt{T})$ convergence)
- **Mini-batch:** Best of both; standard in practice (batch size $\in [32, 256]$)
- **Gradient noise helps:** Escapes sharp minima, finds flatter solutions (better generalization)
- **Learning rate critical:** Too high → divergence; too low → slow
- **Shuffling essential:** Prevents correlated gradients within mini-batches
- **Wall-clock time matters:** SGD/mini-batch beat BGD despite slower per-epoch convergence

---
