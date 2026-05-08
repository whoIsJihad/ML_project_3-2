# 📝 Gradient Descent Variants - Exam Answers

## Foundation: Understanding the Training Loop & Iterations

### Key Definitions

**Iteration:** One weight update using one batch of data.
**Epoch:** One complete pass through the entire training dataset.
**Batch:** A subset of the dataset used in one iteration.

---

### Calculating Iterations Per Epoch

$$\text{iterations per epoch} = \left\lceil \frac{n}{\text{batch size}} \right\rceil$$

**Concrete examples with $n = 1000$ training samples:**

| Variant | Batch Size | Iterations/Epoch | Weight Updates/Epoch |
|---------|-----------|------------------|----------------------|
| **BGD** | 1000 | 1 | 1 |
| **Mini-batch** | 128 | ~8 | ~8 |
| **Mini-batch** | 32 | ~31 | ~31 |
| **SGD** | 1 | 1000 | 1000 |

---

### The Training Loop: Step-by-Step

**Pseudocode:**
```python
for epoch in range(num_epochs):
    # Shuffle data at start of each epoch
    shuffle_data()
    
    for iteration in range(iterations_per_epoch):
        # Get a batch of samples
        batch = next_batch(batch_size)
        
        # 1. Forward pass: predict on batch
        predictions = model.forward(batch)
        
        # 2. Compute loss on batch
        loss = compute_loss(predictions, batch.labels)
        
        # 3. Backward pass: compute gradient
        gradient = compute_gradient(loss, model.weights)
        
        # 4. Update weights
        model.weights -= learning_rate * gradient
    
    # After each epoch, evaluate on validation set
    val_loss = evaluate(model, validation_data)
    print(f"Epoch {epoch}: val_loss = {val_loss}")
```

---

### Concrete Example: Training with Mini-batch GD

**Setup:**
- Dataset: 100 samples
- Batch size: 20
- Learning rate: 0.01
- Training for 2 epochs

**Execution:**

```
===== EPOCH 1 =====
Iterations per epoch: 100 / 20 = 5

Iteration 1:
  Load batch: samples 1-20
  Forward: ŷ = X[1:20] @ w
  Loss: L = (1/20) Σ(y[1:20] - ŷ)²
  Gradient: ∇L = (1/20) X[1:20]ᵀ(ŷ - y[1:20])
  Update: w ← w - 0.01 × ∇L
  
  → weights have been updated 1 time

Iteration 2:
  Load batch: samples 21-40 (different samples!)
  Compute loss on this batch
  Gradient: ∇L = (1/20) X[21:40]ᵀ(ŷ - y[21:40])
  Update: w ← w - 0.01 × ∇L
  
  → weights have been updated 2 times

Iteration 3: samples 41-60 → update 3
Iteration 4: samples 61-80 → update 4
Iteration 5: samples 81-100 → update 5

End of Epoch 1:
  ✓ All 100 samples seen once
  ✓ Weights updated 5 times
  ✓ Validation loss: say, 0.50

===== EPOCH 2 =====
Shuffle data again (important!)

Iteration 1:
  Load batch: samples in random order (e.g., 50, 23, 88, 12, ..., 99) [20 samples total]
  Update weights
  
  → weights have been updated 6 times total

Iteration 2:
  Different random batch of 20
  
  → weights have been updated 7 times total

... (iterations 3-5)

End of Epoch 2:
  ✓ All 100 samples seen again (2nd time each)
  ✓ Weights updated 10 times total (5 from epoch 1 + 5 from epoch 2)
  ✓ Validation loss: say, 0.35 (improved)

After 2 epochs:
  - Total samples processed: 100 × 2 = 200
  - Total weight updates: 5 × 2 = 10
  - Convergence: loss went from 0.50 to 0.35
```

---

### Wall-Clock Time & Updates Per Second

**Time per iteration depends on:**
1. Batch size: larger batch = more computations per iteration
2. Number of features: more features = more computations
3. Hardware: GPU is much faster than CPU
4. Implementation: optimized code is faster

**Rough estimates (on modern GPU):**

```
Time per iteration ≈ (batch_size × num_features) / GPU_speed

Example with GPU speed ≈ 10 GFLOPS:
  Batch size = 32, features = 1000
  Time per iteration ≈ (32 × 1000) / (10 Billion) ≈ 0.003 seconds = 3 ms

Updates per second = 1 / time_per_iteration = 1 / 0.003 ≈ 333 updates/second
```

---

### Why Iteration Count Matters

**Training dynamics depend on total iterations, not just epochs:**

```
Scenario A: 1000 samples, batch=1000, train for 100 epochs
  Iterations per epoch: 1
  Total iterations: 100 × 1 = 100
  (each sample seen 100 times, but only 100 weight updates)

Scenario B: 1000 samples, batch=32, train for 3.125 epochs
  Iterations per epoch: ~31
  Total iterations: 100 (same as Scenario A!)
  (each sample seen ~3 times, but 100 weight updates)

Same number of weight updates (100), but:
  - Scenario A: very stable, smooth convergence
  - Scenario B: noisier, may escape local minima better
```

**Key insight:** When comparing variants, compare total iterations, not epochs!

---

### Summary Table

| Metric | BGD | SGD | Mini-batch |
|--------|-----|-----|-----------|
| **Batch size** | $n$ | 1 | 32-256 |
| **Updates per epoch** | 1 | $n$ | $n/B$ |
| **Time per update** | Long | Short | Medium |
| **Updates per second** | Low (~1) | High (~1000s) | Medium (~100s) |
| **Total time per epoch** | Fast (1 slow update) | Slow (many fast updates) | **Balanced** ✓ |
| **Gradient stability** | Stable (full data) | Noisy (1 sample) | Medium (batch data) |

---

---

## Conceptual Q1 Answer

(Wall-clock time vs per-epoch convergence)

**Per-epoch convergence:**
- BGD: 1 epoch = 1 gradient computed on ALL $n$ samples → 1 update
- SGD: 1 epoch = $n$ gradients (one per sample) → $n$ updates

BGD: 1 update with **stable, accurate gradient** (all data)
SGD: $n$ updates with **noisy gradients** (each from 1 sample)

**Why BGD faster per epoch:** One quality update beats many noisy updates.

---

**In wall-clock time (real time):**

BGD per iteration: $O(n \cdot d)$ (process all $n$ samples)
SGD per iteration: $O(d)$ (process 1 sample)

For 1000 samples:
- BGD: 1 update = 1000× computations
- SGD: 1000 updates = 1000× same computations total, but spreads across 1000 iterations

**Practical reality:**
```
BGD:  10 iterations × 1000 ops = 10,000 total ops
SGD:  1000 iterations × 1 op = 1000 total ops per useful update
      But each iteration fast (can parallelize, cache-friendly)
      
Wall-clock: SGD often ~100× faster to reach 95% accuracy
```

**Why?** Early iterations of SGD with noisy gradients still point vaguely toward optimum, and the noise helps escape local minima. Huge speedup outweighs noisiness.

---

## Conceptual Q2 Answer

(Escaping local minima)

**Key insight:** Noise can help escape sharp local minima.

**Sharp local minimum:**
```
L(w)
 ^
 |      BGD gets stuck here
 |    ╱╲
 |   ╱  ╲_____ local minimum (deep, narrow)
 |__╱
   w
```

BGD gradient:
- Smooth, averaged over all samples
- Points directly toward local minimum
- Gets stuck in narrow valley

SGD gradient:
- Noisy (from 1 sample or few samples)
- Points roughly toward local minimum, but **with random jitter**
- Noise can kick it out of narrow valley!

**Mathematical view:**

SGD update: $\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \nabla L_i(\mathbf{w}_t)$

Noise term: $\nabla L_i - \mathbb{E}[\nabla L] = \text{random perturbation}$

This perturbation has nonzero probability of going "uphill" temporarily, allowing escape.

BGD update: $\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \nabla L(\mathbf{w}_t)$ (no noise → stuck)

**Empirical evidence:**
- SGD often finds better solutions (lower test error)
- SGD trains deep networks that BGD fails on
- SGD + momentum/Adam: standard for modern deep learning

---

## Conceptual Q3 Answer

(Data shuffling effect)

**Without shuffling:**
```
Epoch 1: batches [1-32], [33-64], [65-96], ..., [N-31 to N]
Epoch 2: Same order! (biased)
```

**With shuffling:**
```
Epoch 1: batches [random 32], [random 32], ...
Epoch 2: Different random order (unbiased)
```

**Benefits of shuffling:**
- Each batch is representative (mix of classes/features)
- Gradient estimate unbiased across epochs
- Reduces overfitting to data order
- Helps with variance reduction
- Typically 10-20% faster convergence

**Modern practice:** Always shuffle data between epochs (standard in training loops).

---

## Application/Scenario Q1 Answer

(1M samples, GPU holds 256 samples)

**BGD:** Would need all 1M in memory → impossible
**SGD:** 1M updates per epoch → too noisy, slow convergence
**Mini-batch (best choice!):** 1M / 256 ≈ 4000 updates per epoch
- Fits GPU memory perfectly
- Stable gradient (batch of 256)
- Fast per iteration AND reasonable number of iterations

**Recommended batch size:** 256 (already fits), or try 32-128 if slow

---

## Application/Scenario Q2 Answer

(Loss oscillates wildly every few epochs)

**Diagnosis:** Learning rate too high → overshooting

**Root cause:** Each batch has slightly different gradient. Large α amplifies these differences.

**Solutions (best to worst):**
1. **Use adaptive optimizer (Adam/RMSprop)** - automatically adjusts learning rate
2. **Reduce learning rate** - try α/10
3. **Increase batch size** - larger batch = stabler gradient
4. **Use learning rate schedule** - decay α over epochs

Example: If oscillating with α=0.01, try α=0.001

---

## Application/Scenario Q3 Answer

(Streaming production data)

**Use: SGD (one sample at a time)**

**Why:**
- Process new samples immediately (no waiting for batches)
- Memory efficient (don't store all data)
- Adapts to distribution shift in real-time

**Example:** Recommendation system
- New user action arrives → immediate SGD update
- Model adapts to user preferences instantly

**Not BGD:** Can't collect "all data"—stream never ends
**Not mini-batch:** Would need to buffer samples, unnecessary complexity

---

## Application/Scenario Q4 Answer

(SGD diverges with doubled α, mini-batch works fine)

**Root cause:** Gradient noise scales differently

**Noise in gradient:** ∝ $1/\sqrt{b}$ where $b$ = batch size

SGD (b=1): High noise → large learning rate amplifies → divergence
Mini-batch (b=256): 16× lower noise → can handle large learning rate

**Mathematical:** Max stable α ∝ $1 / \text{noise}$

**Solutions:**
1. Reduce α for SGD
2. Use mini-batch instead (more stable)
3. Use learning rate decay: $\alpha_t = \alpha_0 / \sqrt{t}$
4. Use Adam (automatically adjusts)

---

## Trick/Failure Q1 Answer

(Mini-batch: 10 epochs, BGD: 100 epochs, same α)

**Explanation:** Different effective learning rates

Mini-batch (b=32): 31 updates/epoch × 10 = 310 total updates
BGD (b=1000): 1 update/epoch × 100 = 100 total updates

But mini-batch batches are smaller-scale. With 3× more updates, catches up.

**To fix BGD:** Increase α by ~$\sqrt{b/n} = \sqrt{32/1000} ≈ 0.18$ (heuristic)

---

## Trick/Failure Q2 Answer

(Switch batch size 256 → 1024, maintain same speed)

**Rule of thumb:** Increase learning rate by $\sqrt{b_2/b_1}$

$$\sqrt{\frac{1024}{256}} = \sqrt{4} = 2$$

If old α = 0.01, try new α = 0.02

**Why:** Larger batch = lower gradient noise = can tolerate larger steps

**Caveat:** This is a heuristic. May need tweaking based on actual training dynamics.

