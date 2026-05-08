# Adagrad

Adagrad (Adaptive Gradient) is an adaptive optimization algorithm that automatically adjusts [[Learning Rate and Step Size|learning rates]] for each parameter based on accumulated squared gradients. It is particularly effective for sparse gradient problems.

## Core Algorithm

At iteration $t$, Adagrad maintains the sum of squared gradients:

$$\mathbf{s}_t = \mathbf{s}_{t-1} + \mathbf{g}_t^2$$

where:
- $\mathbf{g}_t = \nabla \mathcal{L}(\mathbf{w}_t)$ is the gradient
- $\mathbf{g}_t^2$ is element-wise squaring
- $\mathbf{s}_0 = \mathbf{0}$ (initialized to zero)
- $\mathbf{s}_t$ accumulates over all iterations (never decreases)

Then update parameters:

$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \frac{\mathbf{g}_t}{\sqrt{\mathbf{s}_t} + \epsilon}$$

where:
- $\alpha$ is the [[Learning Rate and Step Size|learning rate]]
- $\epsilon$ is a small constant (typically $10^{-8}$) for numerical stability
- Division and square root are element-wise

## Per-Parameter Learning Rates

The key insight is that each parameter $w_i$ gets its own adaptive learning rate:

$$\alpha_i^{\text{eff}}(t) = \frac{\alpha}{\sqrt{\mathbf{s}_t^{(i)}} + \epsilon}$$

where $\mathbf{s}_t^{(i)}$ is the accumulated squared gradient for parameter $i$.

### Concrete Numerical Example

Let's track two parameters with different gradient patterns:

**Parameter 1: Consistent large gradients**

| Iteration | Gradient | g² | s (accumulate) | √s | α_eff = 0.1/√s |
|-----------|----------|-----|--|---|---|
| 1 | 0.5 | 0.25 | 0.25 | 0.5 | 0.2 |
| 2 | 0.6 | 0.36 | 0.61 | 0.78 | 0.128 |
| 3 | 0.55 | 0.3 | 0.91 | 0.95 | 0.105 |
| 10 | ... | ... | 3.5 | 1.87 | 0.053 |

Learning rate shrinks from 0.2 → 0.128 → 0.105 → ... → 0.053 (well-tuned parameter takes smaller steps)

**Parameter 2: Sparse small gradients**

| Iteration | Gradient | g² | s (accumulate) | √s | α_eff = 0.1/√s |
|-----------|----------|-----|--|---|---|
| 1 | 0.0 | 0.0 | 0.0 | 0.0 | ∞ (clamped to 0.1) |
| 2 | 0.0 | 0.0 | 0.0 | 0.0 | ∞ |
| 5 | 0.1 | 0.01 | 0.01 | 0.1 | 1.0 (huge!) |
| 10 | 0.1 | 0.01 | 0.02 | 0.14 | 0.71 |

Learning rate starts huge (0.1) because parameter is inactive. When it finally updates (iteration 5), it takes a large step to compensate!

**Effect:**
- Parameter 1: well-tuned (small lr because frequent updates)
- Parameter 2: compensated (large lr because rare updates)

This **automatically balances** parameter updates: frequently updated parameters take smaller steps, while rarely updated parameters take larger steps.

## Why This Helps: Sparse Gradients

Consider a sparse feature matrix (common in NLP, recommendation systems):

- Feature A: active in 90% of samples → large cumulative gradient → s grows huge
- Feature B: active in 1% of samples → small cumulative gradient → s barely grows

**Without Adagrad:**
Both features use same learning rate α = 0.01

- Feature A updates: 0.01 × 0.5 = 0.005 (reasonable)
- Feature B updates: 0.01 × 0.05 = 0.0005 (way too small! barely moves)

Feature B updates too slowly because it's rare. When it finally appears, we waste the opportunity.

**With Adagrad:**
Each gets its own learning rate

- Feature A: s_A = 50 (huge! after 100 samples), so α_eff = 0.1/√50 ≈ 0.014 (reasonable)
- Feature B: s_B = 0.1 (tiny! only 1 sample), so α_eff = 0.1/√0.1 ≈ 0.316 (huge!)

When Feature B appears, it takes a large step (0.316 × 0.05 = 0.016) to compensate for rarity.

**Real example:** Embedding table with 1M words

- Common word "the": sees 90% of training data → learns slowly per update (avoid overfitting)
- Rare word "abracadabra": sees 0.001% of training data → learns quickly per update (use the opportunity)

## PyTorch Implementation

```python
optimizer = torch.optim.Adagrad(
    model.parameters(),
    lr=0.01,              # learning rate
    eps=1e-8,             # numerical stability
    weight_decay=0.0      # L2 regularization
)

# Training loop
for epoch in range(num_epochs):
    for batch in train_loader:
        loss = model(batch)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
```

### Inspecting Adagrad State

```python
for param_group in optimizer.param_groups:
    for param in param_group['params']:
        if param in optimizer.state:
            state = optimizer.state[param]
            s = state['sum']  # accumulated squared gradients
            step = state['step']  # iteration count
            
            print(f"Accumulated gradient sum shape: {s.shape}")
```

## Convergence Properties

For [[Convex vs Non-Convex Optimization|convex]] smooth losses:

$$\mathbb{E}[\mathcal{L}(\mathbf{w}_T)] - \mathcal{L}(\mathbf{w}^*) = O\left(\frac{\log T}{\sqrt{T}}\right)$$

Adagrad achieves the **optimal rate for adaptive methods** in convex optimization.

## Advantages

✅ **Automatic per-parameter learning rates:** No manual adjustment needed  
✅ **Excellent for sparse gradients:** Handles variable-activity features well  
✅ **Simple:** Minimal hyperparameter tuning  
✅ **Optimal convergence rate (convex):** $O(\log T / \sqrt{T})$  
✅ **Good for embeddings:** Works well with sparse feature matrices  

## Disadvantages

❌ **Monotonically decreasing learning rates:** Learning rate only shrinks, never increases  
❌ **Learning rate eventually becomes too small:** After many iterations, $\alpha_i^{\text{eff}} \to 0$ (cannot escape local minima)  
❌ **High memory:** Stores accumulated sum for every parameter (like Adam)  
❌ **Non-stationary behavior:** Effective learning rates keep changing  
❌ **Can diverge on non-convex problems:** Accumulated squares can become huge  

## The Core Problem: Monotonic Decay

The critical issue with Adagrad:

$$\mathbf{s}_t = \sum_{i=0}^{t} \mathbf{g}_i^2$$

grows monotonically without bound. Eventually:

$$\alpha_i^{\text{eff}}(t) = \frac{\alpha}{\sqrt{\sum_{i=0}^{t} \mathbf{g}_i^2} + \epsilon} \to 0$$

as $t \to \infty$.

**Practical consequence:** Training stalls after long runs. Parameters stop updating.

This is why Adagrad is rarely used for deep learning (unlike [[Adam]] and [[RMSprop]]).

## Use Cases

**Adagrad is good for:**
- Sparse gradient problems (NLP, recommender systems)
- Small datasets where monotonic decay isn't harmful
- Convex optimization problems

**Don't use for:**
- Deep neural networks (training stalls)
- Long training runs
- Non-convex problems

## Comparison to Modern Alternatives

| Algorithm | Per-Param LR | Sparse Gradients | Monotonic Decay | Deep Learning |
|---|---|---|---|---|
| Adagrad | Yes | Excellent | Yes (bad) | Poor |
| [[RMSprop]] | Yes | Good | No | Good |
| [[Adam]] | Yes (with momentum) | Good | No | Excellent |

[[RMSprop]] and [[Adam]] fix Adagrad's decay problem while maintaining adaptive learning rates.

## Historical Importance

Adagrad was **groundbreaking** when introduced (2011):
- First practical adaptive learning rate algorithm
- Motivated research into better optimizers
- Foundation for RMSprop and Adam

Understanding Adagrad helps understand modern optimizers.

## Practical Hyperparameters

### Learning Rate $\alpha$

Typical range: $0.01$ to $0.1$ (higher than SGD due to adaptive scaling)

Start with $0.01$:

```python
optimizer = torch.optim.Adagrad(model.parameters(), lr=0.01)
```

### Epsilon $\epsilon$

Default: $10^{-8}$ (fine for most problems)

Increase only if division by zero errors occur:

```python
optimizer = torch.optim.Adagrad(model.parameters(), eps=1e-7)
```

### Weight Decay

Can add L2 regularization:

```python
optimizer = torch.optim.Adagrad(
    model.parameters(),
    lr=0.01,
    weight_decay=0.0001
)
```

## When Training Stalls: Early Stopping

Due to monotonic decay, use early stopping with Adagrad:

```python
best_loss = float('inf')
patience = 10

for epoch in range(max_epochs):
    loss = train()
    
    if loss < best_loss:
        best_loss = loss
        patience_reset = 0
    else:
        patience_reset += 1
    
    if patience_reset >= patience:
        print(f"Stopping at epoch {epoch}: learning rate too small")
        break
```

## Modern Alternative: Use RMSprop or Adam

For deep learning, [[RMSprop]] or [[Adam]] are better choices:

```python
# Instead of Adagrad (for deep learning):
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Or RMSprop:
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.001)
```

These fix Adagrad's monotonic decay while keeping sparse gradient benefits.

## Mathematical Details: Intuition

Adagrad's scaling is motivated by the **Hessian** [[Second Derivative Test|diagonal]]:

If a parameter has consistently large gradients, the loss surface is steep in that direction (large second derivative). Gradient-based moves in steep directions overshoot easily, so reduce step size.

If a parameter has small gradients, the loss surface is flat in that direction (small second derivative). Gradient-based moves are safe, so use larger steps.

Accumulated squared gradients approximate this diagonal curvature information.

## See Also

- [[Learning Rate and Step Size]]: Adaptive learning rates concept
- [[Adam]]: Modern adaptive method (fixes Adagrad's decay problem)
- [[RMSprop]]: Alternative adaptive method (exponential moving average instead of accumulation)
- [[Stochastic Gradient Descent (SGD)]]: Alternative optimizer
- [[Convergence Criteria]]: Early stopping with Adagrad
- [[Sparse Gradients]]: Where Adagrad excels
