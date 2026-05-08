# Stochastic Gradient Descent (SGD)

Stochastic Gradient Descent is the foundational optimization algorithm for deep learning. It extends [[Gradient Descent Fundamentals|batch gradient descent]] by using noisy gradient estimates computed on small subsets of data, trading some gradient accuracy for computational efficiency and better generalization.

## Definition and Update Rule

Given training data $\{(\mathbf{x}_i, y_i)\}_{i=1}^N$, at iteration $t$:

1. Sample a batch $\mathcal{B}_t \subset \{1, \ldots, N\}$ of size $B$ uniformly at random
2. Compute batch loss:
$$\mathcal{L}_t(\mathbf{w}) = \frac{1}{B} \sum_{i \in \mathcal{B}_t} \ell(\mathbf{w}, \mathbf{x}_i, y_i)$$

3. Compute batch gradient:
$$\mathbf{g}_t = \nabla \mathcal{L}_t(\mathbf{w}_t)$$

4. Update parameters:
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \mathbf{g}_t$$

where $\alpha$ is the [[Learning Rate and Step Size|learning rate]].

## Why "Stochastic"?

The gradient $\mathbf{g}_t$ is a **random variable** because it depends on the random batch $\mathcal{B}_t$.

**Unbiasedness property:**
$$\mathbb{E}[\mathbf{g}_t] = \nabla \mathcal{L}(\mathbf{w}_t)$$

On average, the batch gradient estimates the true full-dataset gradient correctly. However, on any single iteration, $\mathbf{g}_t$ is noisy:

$$\mathbf{g}_t = \nabla \mathcal{L}(\mathbf{w}_t) + \boldsymbol{\xi}_t$$

where $\mathbf{\xi}_t$ is random noise with $\mathbb{E}[\boldsymbol{\xi}_t] = 0$.

## Variance of Gradient Estimates

The variance of the batch gradient decreases with batch size:

$$\text{Var}[\mathbf{g}_t] \approx \frac{\sigma^2}{B}$$

where $\sigma^2$ is the per-sample gradient variance.

### Concrete Example: Effect of Batch Size

Suppose you have a dataset of 10,000 images and true gradient is ∇L = [1.5, -0.3, 2.1]:

**Batch Size = 1 (one image):**
- Sample 1 image with label "dog"
- Gradient estimate: [1.8, -0.5, 1.9] (noisy!)
- Error from true: [0.3, -0.2, -0.2] (large noise)
- 10,000 iterations to see all data

**Batch Size = 32 (32 images mixed):**
- Average over 32 images
- Gradient estimate: [1.52, -0.29, 2.08] (less noisy)
- Error from true: [0.02, 0.01, -0.02] (smaller noise)
- 312 iterations to see all data

**Batch Size = 256 (256 images):**
- Average over 256 images
- Gradient estimate: [1.503, -0.302, 2.101] (very close)
- Error from true: [0.003, -0.002, 0.001] (tiny noise)
- 39 iterations to see all data

**Batch Size = 10,000 (all data):**
- Average over all data
- Gradient estimate: [1.5, -0.3, 2.1] (exact!)
- Error from true: [0, 0, 0] (no noise)
- 1 iteration to see all data, but very slow per-iteration

| Batch Size | Gradient Noise | Update Speed | Iterations/Epoch | Wall-clock Time |
|---|---|---|---|---|
| $B=1$ (per-sample) | High (±0.3) | Fast | 10,000 | Slow (noisy kills convergence) |
| $B=32$ | Medium (±0.02) | Medium | 312 | Medium |
| $B=256$ | Low (±0.002) | Medium | 39 | Medium |
| Full batch | Zero | Slow | 1 | Slow (few updates per epoch) |

**Trade-off:** Smaller batches update faster but noisily; larger batches update accurately but slowly.

## PyTorch Implementation

```python
# Create optimizer
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.01,           # learning rate α
    momentum=0.0       # can add momentum (see [[SGD with Momentum]])
)

# Training loop
for epoch in range(num_epochs):
    for batch_idx, (x, y) in enumerate(train_loader):
        # Forward pass
        loss = model(x)  # scalar loss
        
        # Backward pass: computes gradients ∇L
        loss.backward()  # populates param.grad for all params
        
        # Update step: w ← w - α∇L
        optimizer.step()
        
        # Clear gradients for next batch
        # (gradients accumulate otherwise)
        optimizer.zero_grad()
```

### What optimizer.step() Does

```python
# Pseudocode inside optimizer.step():
for param in model.parameters():
    if param.grad is not None:
        param.data = param.data - lr * param.grad
```

### What zero_grad() Does

```python
# Pseudocode inside optimizer.zero_grad():
for param in model.parameters():
    if param.grad is not None:
        param.grad = None  # or .zero_()
```

**Why necessary?** By default, PyTorch **accumulates** gradients across iterations. Without zeroing,:

```python
loss1.backward()    # param.grad = ∇L₁
loss2.backward()    # param.grad = ∇L₁ + ∇L₂  (accumulated!)
```

For standard mini-batch training, we zero after each step.

See [[Gradient Accumulation and zero_grad()]] for when **not** to zero.

## Convergence Analysis

### Convex Case

For [[Convex vs Non-Convex Optimization|convex]] loss with Lipschitz-continuous gradients:

$$\mathbb{E}[\mathcal{L}(\mathbf{w}_t)] - \mathcal{L}(\mathbf{w}^*) = O\left(\frac{1}{\sqrt{t}}\right)$$

with a fixed learning rate $\alpha = O(1/\sqrt{t})$ (decaying schedule required).

**Key insight:** Gradient noise prevents convergence to exact zero with fixed learning rate. Convergence is to a neighborhood of size $O(\alpha)$ around the optimum.

### Non-Convex Case (Deep Learning)

For general non-convex losses, SGD converges to a [[Convergence Criteria|stationary point]]:

$$\mathbb{E}\left[\|\nabla \mathcal{L}(\mathbf{w}_T)\|^2\right] \leq \epsilon$$

after $O(1/\epsilon^2)$ gradient evaluations.

**Empirical behavior in practice:**

- SGD often finds [[Local and Global Minima|good local minima]] that generalize well
- The noise from stochasticity may help escape [[Saddle Points and Escape Dynamics|saddle points]]
- Different random seeds often reach different (but similarly performing) solutions

## Implicit Regularization: The Generalization Benefit

One of SGD's most important properties is that it often **implicitly regularizes** the solution, finding parameters that generalize better than batch gradient descent, despite being noisier.

**Why?** Under certain conditions, SGD is biased toward solutions with smaller norm:

$$\text{SGD trajectory tends toward smaller } \|\mathbf{w}\|$$

This acts like implicit L2 regularization. See [[Weight Decay vs L2 Regularization]].

## Noise-Induced Escape from Saddle Points

In neural networks, the loss landscape contains many [[Saddle Points and Escape Dynamics|saddle points]]. The gradient noise in SGD helps escape them:

If at a saddle point:
- Negative curvature direction exists (away from saddle)
- Noise in that direction is amplified
- Escape happens faster than for batch GD

This is one reason SGD generalizes better: it explores the loss landscape more thoroughly.

## Comparison to Alternatives

### vs. Batch Gradient Descent

**SGD advantages:**
- Much faster per-iteration computation
- Better generalization (noise helps)
- Can process datasets that don't fit in memory

**Batch GD advantages:**
- Deterministic trajectory
- Fewer iterations to convergence

### vs. [[Adam|Adam]] and [[Adaptive Methods|adaptive methods]]

**SGD advantages:**
- Simpler, fewer hyperparameters
- Often better final generalization
- More predictable behavior

**Adam advantages:**
- Faster convergence (fewer iterations)
- Robust to learning rate choice
- Better for sparse gradients

See [[SGD vs Adam: When to Use Which]].

## Critical Hyperparameters

### Learning Rate $\alpha$

Most important hyperparameter. See [[Learning Rate and Step Size]].

- Too small: convergence is very slow
- Too large: loss diverges or oscillates

Typical range: $10^{-5}$ to $10^{-1}$ depending on problem.

### Batch Size $B$

Affects gradient noise:

$$\text{larger } B \Rightarrow \text{less noise} \Rightarrow \text{can use larger } \alpha$$

Common values: 32, 64, 128, 256, 512.

Relationship: **learning rate should scale with $\sqrt{B}$** (linear scaling rule).

```python
batch_size_new = 256
batch_size_old = 32
lr_new = lr_old * (batch_size_new / batch_size_old) ** 0.5
```

### Momentum (Optional)

See [[SGD with Momentum]] for momentum version.

Typical values: $\beta = 0.9$ or $0.99$.

```python
optimizer = torch.optim.SGD(
    model.parameters(), 
    lr=0.01, 
    momentum=0.9  # enables momentum
)
```

## Common Failure Modes

| Problem | Symptom | Solution |
|---|---|---|
| Learning rate too large | Loss becomes NaN | Reduce learning rate by 10× |
| Learning rate too small | Loss decreases very slowly | Increase learning rate |
| Batch size too large | Model doesn't converge | Reduce batch size or increase learning rate |
| No zero_grad() | Gradients accumulate | Add optimizer.zero_grad() |
| Divergence on first batch | NaN loss immediately | Check loss function (invalid input?) |

## Advanced: Cyclical Learning Rates and Restarts

Instead of fixed or smoothly decaying learning rate, use cyclical schedules:

```python
scheduler = torch.optim.lr_scheduler.CyclicLR(
    optimizer,
    base_lr=0.001,
    max_lr=0.1,
    step_size_up=100,  # epochs to increase
    cycle_momentum=False
)
```

or [[Warm Restarts|warm restarts]]:

```python
scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
    optimizer,
    T_0=10,  # initial period
    T_mult=2,  # restart period multiplier
    eta_min=0.0001
)
```

These prevent early convergence to poor local minima.

## Modern Variants: SGD with Weight Decay

Use weight decay (decoupled from gradient scaling) for better regularization:

```python
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.01,
    momentum=0.9,
    weight_decay=1e-4,  # L2 regularization coefficient
    nesterov=True       # Nesterov momentum
)
```

See [[Weight Decay vs L2 Regularization]].

## When to Use SGD

✅ **Prefer SGD when:**
- You want the best generalization (lowest test error)
- You can carefully tune learning rate
- Dataset is large (SGD's advantage)
- Training time allows experimentation

❌ **Avoid SGD when:**
- You need fast convergence with minimal tuning
- Sparse gradients (use Adagrad or Adam)
- Hyperparameter tuning time is limited (Adam is easier)

## See Also

- [[Gradient Descent Fundamentals]]: Mathematical foundation
- [[Learning Rate and Step Size]]: Critical hyperparameter
- [[SGD with Momentum]]: Faster convergence variant
- [[Stochastic Gradient Descent (SGD)|Nesterov Momentum]]: Modern momentum variant
- [[Adam]]: Adaptive alternative
- [[Convergence Criteria]]: How to detect convergence
- [[Loss Landscape Geometry]]: Why SGD works on non-convex problems
