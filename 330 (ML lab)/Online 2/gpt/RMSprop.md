# RMSprop

RMSprop (Root Mean Square Propagation) is an adaptive optimization algorithm that fixes [[Adagrad]]'s monotonically decreasing learning rate problem by using an exponential moving average of squared gradients instead of cumulative sums.

## Core Algorithm

At iteration $t$, RMSprop maintains an exponential moving average of squared gradients:

$$\mathbf{v}_t = \beta \mathbf{v}_{t-1} + (1 - \beta) \mathbf{g}_t^2$$

where:
- $\mathbf{g}_t = \nabla \mathcal{L}(\mathbf{w}_t)$ is the gradient
- $\mathbf{g}_t^2$ is element-wise squaring
- $\beta \in [0, 1)$ is the decay rate (typical: 0.9)
- $\mathbf{v}_0 = \mathbf{0}$ (initialized to zero)

Then update parameters:

$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \frac{\mathbf{g}_t}{\sqrt{\mathbf{v}_t} + \epsilon}$$

where:
- $\alpha$ is the [[Learning Rate and Step Size|learning rate]]
- $\epsilon$ is a small constant (typically $10^{-8}$) for numerical stability
- Division and square root are element-wise

## Comparison to Adagrad: Why RMSprop Fixes the Problem

The key difference from [[Adagrad]]:

| Algorithm | Accumulated Squared Gradients |
|---|---|
| Adagrad | $\mathbf{s}_t = \sum_{i=0}^{t} \mathbf{g}_i^2$ (cumulative sum - **grows forever**) |
| RMSprop | $\mathbf{v}_t = \beta \mathbf{v}_{t-1} + (1-\beta) \mathbf{g}_t^2$ (exponential moving average - **stabilizes**) |

### The Adagrad Problem (Concrete Numbers)

Suppose a parameter's gradients are 0.1 for 1000 iterations:

**Adagrad:**
- Iteration 1: s = 0.01, α_eff = 0.1/√0.01 = 1.0 (large step)
- Iteration 100: s = 1.0, α_eff = 0.1/√1.0 = 0.1 (smaller)
- Iteration 500: s = 5.0, α_eff = 0.1/√5.0 ≈ 0.045 (tiny)
- Iteration 1000: s = 10.0, α_eff = 0.1/√10 ≈ 0.032 (microscopic!)

**Problem:** Even with consistent gradients, the learning rate decays to near zero. You can't refine parameters anymore!

**RMSprop (β = 0.99):**
- Iteration 1: v = 0.01, α_eff = 1.0 (same start)
- Iteration 100: v ≈ 0.01 (doesn't accumulate!), α_eff ≈ 1.0 (stays large)
- Iteration 500: v ≈ 0.01 (steady state), α_eff ≈ 1.0 (stable)
- Iteration 1000: v ≈ 0.01 (stabilized), α_eff ≈ 1.0 (keeps learning)

**Why?** With β = 0.99:
- Old values get weighted 99% (which decays exponentially)
- New values get weighted 1%
- The sum reaches equilibrium instead of growing forever

**Consequence:** Adagrad's learning rate monotonically decays to zero and gets stuck. RMSprop's learning rate stabilizes to a steady-state value and keeps refining.

## Per-Parameter Adaptive Learning Rates

Like Adagrad, RMSprop adjusts each parameter's learning rate:

$$\alpha_i^{\text{eff}}(t) = \frac{\alpha}{\sqrt{\mathbf{v}_t^{(i)}} + \epsilon}$$

But the adaptive scaling is **non-monotonic**: it can increase or decrease based on recent gradient activity, not all-time history.

### Concrete Example: RMSprop Adapts to Recent Trends

Suppose a parameter has changing gradient patterns (β = 0.99):

| Iteration | Gradient | g² | v (moving avg) | √v | α_eff (0.1/√v) | Interpretation |
|---|---|---|---|---|---|---|
| 1 | 0.5 | 0.25 | 0.0025 | 0.05 | 2.0 | Large step (sparse) |
| 10 | 0.5 | 0.25 | 0.025 | 0.158 | 0.632 | Stabilizing |
| 50 | 0.5 | 0.25 | 0.025 | 0.158 | 0.632 | Steady state |
| 51 | 0.05 | 0.0025 | 0.024 | 0.155 | 0.645 | Gradients dropped! Lr goes UP slightly |
| 60 | 0.05 | 0.0025 | 0.024 | 0.155 | 0.645 | Stays stable at new level |
| 100 | 0.5 | 0.25 | 0.025 | 0.158 | 0.632 | Gradients increase again → adapts |

**Key point:** When gradient magnitude changes (0.5 → 0.05), RMSprop adjusts its learning rate. Adagrad would not (s only grows, never shrinks).

## PyTorch Implementation

```python
optimizer = torch.optim.RMSprop(
    model.parameters(),
    lr=0.01,              # learning rate
    alpha=0.99,           # decay rate β (default: 0.99)
    eps=1e-8,             # numerical stability
    weight_decay=0.0,     # L2 regularization
    momentum=0.0          # can add momentum (see below)
)

# Training loop
for epoch in range(num_epochs):
    for batch in train_loader:
        loss = model(batch)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
```

### Inspecting RMSprop State

```python
for param_group in optimizer.param_groups:
    for param in param_group['params']:
        if param in optimizer.state:
            state = optimizer.state[param]
            v = state['square_avg']  # moving average of squared gradients
            step = state['step']
            
            print(f"v shape: {v.shape}, step: {step}")
```

## Decay Rate $\beta$

In PyTorch, the decay rate is called `alpha` (confusing naming, but standard):

$$\mathbf{v}_t = \text{alpha} \cdot \mathbf{v}_{t-1} + (1 - \text{alpha}) \mathbf{g}_t^2$$

Default: $\text{alpha} = 0.99$

### Effect of Different Values

| Decay Rate | Memory Depth | Effect |
|---|---|---|
| 0.5 | 2 iterations | Highly responsive to recent gradients |
| 0.9 | 10 iterations | Balanced (standard) |
| 0.99 | 100 iterations | Smooth, stable |
| 0.999 | 1000 iterations | Very stable, slow adaptation |

- Lower decay (e.g., 0.9): reacts quickly to gradient changes
- Higher decay (e.g., 0.99): averages over longer history (smoother)

**Typical settings:**
```python
# Default (works most of the time)
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.01, alpha=0.99)

# More responsive (noisier data)
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.01, alpha=0.9)

# Smoother (stable data)
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.01, alpha=0.999)
```

## RMSprop with Momentum

RMSprop can be combined with [[SGD with Momentum|momentum]] for faster convergence:

$$\mathbf{v}_t = \beta_2 \mathbf{v}_{t-1} + (1 - \beta_2) \mathbf{g}_t^2$$

$$\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + \mathbf{g}_t$$

$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \frac{\mathbf{m}_t}{\sqrt{\mathbf{v}_t} + \epsilon}$$

```python
optimizer = torch.optim.RMSprop(
    model.parameters(),
    lr=0.01,
    alpha=0.99,
    momentum=0.9  # enables momentum term
)
```

This is essentially a precursor to [[Adam]] (which uses both exponential moving averages).

## Convergence Properties

For [[Convex vs Non-Convex Optimization|smooth convex]] losses:

$$\mathbb{E}[\mathcal{L}(\mathbf{w}_T)] - \mathcal{L}(\mathbf{w}^*) = O\left(\frac{\log T}{\sqrt{T}}\right)$$

Same rate as [[Adam]] (up to log factors). In practice, performance depends heavily on problem structure and hyperparameter tuning.

## Advantages

✅ **Fixes Adagrad's decay problem:** Learning rates don't monotonically shrink to zero  
✅ **Per-parameter adaptation:** Automatically adjusts to gradient magnitudes  
✅ **Works well with sparse gradients:** Good for NLP and recommendation systems  
✅ **Simple conceptually:** Exponential moving average is easy to understand  
✅ **Can add momentum:** Combines with momentum for faster convergence  
✅ **Stable:** Exponential averaging smooths out noise  

## Disadvantages

❌ **More hyperparameters than SGD:** $\alpha$, decay rate $\beta$  
❌ **Less widely adopted than Adam:** Fewer best practices documented  
❌ **No bias correction:** Unlike Adam, early-iteration estimates can be biased (though less severe than Adagrad)  
❌ **Requires careful learning rate tuning:** Not as robust as Adam to learning rate choice  

## When to Use RMSprop

**Good for:**
- Computer vision (sometimes preferred over Adam)
- Recurrent neural networks (more stable than Adam in some cases)
- Sparse gradient problems (NLP, embeddings)
- Situations where Adam's complexity isn't needed

**Avoid in favor of Adam when:**
- Robust hyperparameter selection is important
- Deep networks with many layers
- Time is limited (Adam requires less tuning)

## Comparison to Alternatives

| Aspect | Adagrad | RMSprop | Adam |
|---|---|---|---|
| Per-parameter LR | Yes | Yes | Yes |
| Monotonic decay | Yes (bad) | No (good) | No (good) |
| Momentum optional | No | Yes | Built-in |
| Bias correction | No | No | Yes |
| Complexity | Simple | Simple | Moderate |
| Generalization | N/A | Good | Good |
| Speed | N/A | Very good | Excellent |

## Practical Hyperparameters

### Learning Rate $\alpha$

Typical range: $0.001$ to $0.1$ depending on problem.

Start with $0.01$:

```python
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.01)
```

If loss diverges, reduce by 10×. If convergence is slow, increase by 2-3×.

### Decay Rate (alpha)

Default: 0.99 (works for most cases).

For very noisy data, try 0.9:

```python
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.01, alpha=0.9)
```

For stable data, can try 0.999:

```python
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.01, alpha=0.999)
```

### Momentum

If convergence is slow, add momentum:

```python
optimizer = torch.optim.RMSprop(
    model.parameters(),
    lr=0.01,
    alpha=0.99,
    momentum=0.9
)
```

### Weight Decay

Add L2 regularization if needed:

```python
optimizer = torch.optim.RMSprop(
    model.parameters(),
    lr=0.01,
    weight_decay=0.0001
)
```

See [[Weight Decay vs L2 Regularization]].

## Practical Example: Training a CNN

```python
import torch
import torch.nn as nn
from torch.optim import RMSprop
from torch.optim.lr_scheduler import StepLR

model = nn.Sequential(
    nn.Conv2d(3, 32, 3),
    nn.ReLU(),
    nn.Linear(32 * 30 * 30, 10)
)

optimizer = RMSprop(
    model.parameters(),
    lr=0.01,
    alpha=0.99,
    momentum=0.9
)

scheduler = StepLR(optimizer, step_size=10, gamma=0.1)

for epoch in range(50):
    for batch in train_loader:
        loss = model(batch)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    
    scheduler.step()
    validate()
```

## Historical Context

RMSprop was developed by **Geoffrey Hinton** (informal, not published in a peer-reviewed venue initially) as a fix for Adagrad's decay problem. It became popular in practice, especially for recurrent neural networks.

Key insight: **Use exponential moving average instead of cumulative sum** to balance stability with adaptive learning.

## See Also

- [[Learning Rate and Step Size]]: Adaptive learning rates
- [[Adagrad]]: RMSprop's predecessor (with monotonic decay problem)
- [[Adam]]: Modern successor (combines RMSprop + momentum + bias correction)
- [[SGD with Momentum]]: Momentum mechanism
- [[Stochastic Gradient Descent (SGD)]]: Foundation algorithm
- [[Convergence Criteria]]: Detecting convergence with RMSprop
