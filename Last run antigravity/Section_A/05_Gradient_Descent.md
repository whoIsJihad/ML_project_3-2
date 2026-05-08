# 📘 Gradient Descent (Batch, SGD, Mini-batch)

## 1. Core Idea (Intuition)

* **Problem it solves:** Given a loss function L(w), find the weights w that minimize it.
* **Why needed:** Most loss functions don't have a closed-form solution (unlike linear regression's Normal Equation). We need an iterative approach.
* **Key insight:** The gradient of the loss points in the direction of steepest increase. Go in the opposite direction → loss decreases. Repeat until convergence.

---

## 2. Mathematical Formulation

**Update rule:**
```
w = w - α · ∇L(w)
```

Where:
- `w` = weight vector
- `α` = learning rate (step size)
- `∇L(w)` = gradient of loss w.r.t. weights

**Three variants differ in HOW they compute the gradient:**

### Batch Gradient Descent (Full-batch)
```
∇L = (1/m) Σᵢ₌₁ᵐ ∇Lᵢ(w)
```
Uses ALL m training examples to compute one gradient update.

### Stochastic Gradient Descent (SGD)
```
∇L ≈ ∇Lᵢ(w)    (for one random example i)
```
Uses ONE random example per update.

### Mini-batch Gradient Descent
```
∇L ≈ (1/B) Σᵢ∈batch ∇Lᵢ(w)
```
Uses a small batch of B examples (typically B = 32, 64, 128, 256).

**Why mini-batch wins in practice:**

| Variant | Gradient Quality | Speed per Update | Convergence | GPU Utilization |
|---|---|---|---|---|
| Batch | Exact (no noise) | Slow (process all data) | Smooth but slow | Good |
| SGD | Very noisy | Very fast | Noisy, oscillates | Poor (1 sample) |
| Mini-batch | Good estimate | Moderate | Good balance | Excellent |

---

## 3. Algorithm / Training Procedure

### Mini-batch GD (the standard):
```
Initialize weights w randomly
Set learning rate α, batch size B, max epochs

For each epoch:
    Shuffle training data
    Split into mini-batches of size B
    For each mini-batch:
        1. Forward pass on batch: compute ŷ for all B examples
        2. Compute batch loss: L = (1/B) Σ loss(yᵢ, ŷᵢ)
        3. Compute gradient: g = (1/B) Σ ∇Lᵢ
        4. Update: w = w - α · g
    
    (Optional) Evaluate on validation set
    (Optional) Decay learning rate
```

**One epoch** = one full pass through training data = m/B weight updates.

**Shuffling matters:** Without shuffling, model sees data in same order every epoch → may learn order-dependent patterns → biased gradients.

---

## 4. Optimization / Learning Dynamics

### Batch GD:
- Follows the true gradient exactly → smooth loss curve
- Guaranteed to converge to a local minimum (global if loss is convex)
- **Problem:** Very slow for large datasets. Computing gradient over millions of examples for one update is wasteful.

### SGD:
- Each update uses gradient from 1 example → high variance (noisy)
- **Advantage of noise:** Can escape shallow local minima! The noise acts as implicit regularization.
- **Problem:** Never truly converges — oscillates around the minimum. Need to decay learning rate.

### Mini-batch:
- Best of both worlds: reasonable gradient estimate + manageable compute
- **Vectorization:** GPUs process matrix operations. A batch of 64 takes almost the same wall-clock time as 1 example on a GPU. So mini-batch is essentially "free" parallelism.

**Learning rate effects:**

| α | Batch GD | SGD | Mini-batch |
|---|---|---|---|
| Too small | Slow but stable | Slow, still noisy | Slow but stable |
| Right | Smooth convergence | Noisy convergence | Good convergence |
| Too large | Diverges | Explodes | Diverges |
| Zero | No update | No update | No update |

**Convergence proof intuition (convex case):**

For convex loss with Lipschitz-continuous gradients:
- Batch GD converges at rate O(1/T) where T = number of iterations
- SGD converges at rate O(1/√T) — slower due to noise
- Mini-batch: O(1/√(T·B)) — √B speedup over SGD

---

## 5. Failure Cases / Limitations

| Failure | Why |
|---|---|
| Saddle points | Gradient = 0 at saddle points. GD gets stuck. (Common in high dimensions.) |
| Plateaus | Very flat regions where gradient ≈ 0. Extremely slow progress. |
| Ravines/valleys | Loss surface is steep in one direction, flat in another. GD oscillates across the steep direction and crawls along the flat one. |
| Poor learning rate | Too high → diverge. Too low → impractically slow. |
| Batch size too large | Reduces noise, loses regularization benefit. Often generalizes worse. |
| Feature scale mismatch | If features have very different scales, gradient is dominated by large-scale features. Loss surface becomes elongated ellipse. |

---

## 6. Where It Works Well

* Mini-batch GD: standard for all neural network training
* Batch GD: small datasets where computing full gradient is cheap
* SGD: online learning (streaming data), when noise is beneficial for exploration
* All variants: any differentiable loss function

---

## 7. Variants / Extensions

| Variant | What it does |
|---|---|
| Learning rate schedules | Step decay, cosine annealing, warmup — adjust α during training |
| Gradient clipping | Cap gradient norm to prevent exploding gradients |
| Learning rate warmup | Start with very small α, gradually increase. Stabilizes early training. |
| Momentum, Adam, etc. | Build on GD with adaptive steps (covered in Optimizers topic) |

---

## 8. Comparison Table

| Variant | Gradient Noise | Speed | Memory | Best For |
|---|---|---|---|---|
| Batch GD | None | Slow per epoch | High (full dataset) | Small datasets, convex problems |
| SGD | High | Fast per update | Low (1 example) | Online learning, exploration |
| Mini-batch GD | Moderate | Fast per epoch | Moderate (batch) | Deep learning (standard) |

---

## 9. Exam Questions

### Conceptual:
1. Why does SGD sometimes find better solutions than batch GD even though its gradients are noisy?
2. Explain why mini-batch GD is preferred over batch and SGD in practice. Mention GPU utilization.
3. What is the effect of batch size on generalization? Why might very large batches generalize poorly?

### Derivation-based:
4. For MSE loss on linear regression, write out the gradient computation for batch GD, SGD, and mini-batch GD. Show how they differ.
5. Prove that the expected value of the SGD gradient equals the full-batch gradient: E[∇Lᵢ] = (1/m)Σ∇Lᵢ = ∇L.

### Trick / Failure-case:
6. Your mini-batch training loss oscillates wildly and doesn't decrease. But when you switch to batch GD, it converges smoothly. What's wrong and how do you fix it without switching to batch GD?
7. Training with batch size 8192 gives much worse test accuracy than batch size 64. Explain why.

---

## 10. Key Takeaways

* Gradient descent = move opposite to gradient, repeat. The three variants differ only in how many examples compute each gradient.
* Mini-batch is the standard. Batch size 32-256 is the sweet spot for most problems.
* SGD noise is a feature, not a bug — helps escape local minima, acts as regularization.
* Large batches need larger learning rates (linear scaling rule) and often generalize worse.
* Always shuffle data between epochs.
* GPU parallelism makes mini-batch almost free compared to SGD — batch of 64 ≈ same wall-clock as batch of 1.
* Learning rate is the most important hyperparameter. Start with 0.001 and adjust.
