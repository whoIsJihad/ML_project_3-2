# SGD with Momentum

Momentum is an enhancement to [[Stochastic Gradient Descent (SGD)|vanilla SGD]] that accelerates convergence by accumulating gradient information over multiple iterations. It introduces "inertia" to the optimization trajectory.

## Motivation: The Oscillation Problem

In [[Stochastic Gradient Descent (SGD)|SGD]] with noisy gradients, parameters oscillate perpendicular to the true descent direction:

```
Loss landscape: narrow valley with steep sides

     ↗ oscillation
    /  ↙
   /  /  true descent direction
  ↙   ↙   (down the valley)
```

Each gradient update points in a slightly different direction due to batch noise. If we naively add them, we get cancellation and slow progress.

**Solution:** Use an exponential moving average of gradients to smooth out noise.

## Definition: Momentum Update

At iteration $t$, maintain a velocity vector $\mathbf{v}_t$:

$$\mathbf{v}_{t+1} = \beta \mathbf{v}_t + \mathbf{g}_t$$

where:
- $\beta \in [0, 1)$ is the **momentum coefficient** (typical: 0.9 or 0.99)
- $\mathbf{g}_t = \nabla \mathcal{L}(\mathbf{w}_t)$ is the gradient at iteration $t$
- Initially $\mathbf{v}_0 = \mathbf{0}$

Then update parameters:

$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \mathbf{v}_{t+1}$$

where $\alpha$ is the [[Learning Rate and Step Size|learning rate]].

## Geometric Interpretation

The velocity is an **exponential moving average** of past gradients:

$$\mathbf{v}_t = \mathbf{g}_{t-1} + \beta \mathbf{g}_{t-2} + \beta^2 \mathbf{g}_{t-3} + \cdots$$

Equivalently:

$$\mathbf{v}_t = \sum_{i=0}^{t-1} \beta^i \mathbf{g}_{t-1-i}$$

**Weight distribution:**
- Recent gradients: high weight ($\approx 1$)
- Old gradients: exponentially decaying weight ($\approx \beta^i$)
- Effective memory: $\approx 1/(1-\beta)$ iterations

### Concrete Numerical Example

Track how momentum accumulates with real numbers (β = 0.9, α = 0.01):

**Iteration 1:**
- Gradient: 0.5, Velocity: 0, Update: 0
- v₁ = 0.9 × 0 + 0.5 = 0.5
- w = w - 0.01 × 0.5 = w - 0.005

**Iteration 2 (gradient changes to 0.4, same direction):**
- Gradient: 0.4, Velocity: 0.5
- v₂ = 0.9 × 0.5 + 0.4 = 0.45 + 0.4 = 0.85
- w = w - 0.01 × 0.85 = w - 0.0085 (bigger step!)

**Iteration 3 (gradient changes to -0.2, opposite direction - noise!):**
- Gradient: -0.2, Velocity: 0.85
- v₃ = 0.9 × 0.85 + (-0.2) = 0.765 - 0.2 = 0.565
- w = w - 0.01 × 0.565 = w - 0.00565 (still moves downhill!)

**Vanilla SGD (no momentum, same gradients):**
- Iteration 1: w = w - 0.01 × 0.5 = w - 0.005
- Iteration 2: w = w - 0.01 × 0.4 = w - 0.004
- Iteration 3: w = w - 0.01 × (-0.2) = w + 0.002 (WRONG DIRECTION!)

**Key insight:** Iteration 3 has noise (gradient flipped sign), but momentum remembers the overall downhill trend and keeps moving downhill. Vanilla SGD gets fooled and moves uphill!

### Effect of $\beta$

| $\beta$ | Memory Depth | Effect |
|---|---|---|
| $0.0$ | 1 | Vanilla SGD (no momentum) |
| $0.5$ | 2 | Light smoothing (weights: [1, 0.5]) |
| $0.9$ | 10 | Standard momentum (weights: [1, 0.9, 0.81, ...]) |
| $0.99$ | 100 | Heavy momentum (very long memory) |
| $0.999$ | 1000 | Very long memory (slow to respond) |

## Convergence Acceleration

In convex [[Convex vs Non-Convex Optimization|optimization]], momentum improves convergence rate:

**Vanilla SGD:**
$$\mathbb{E}[\mathcal{L}(\mathbf{w}_t) - \mathcal{L}(\mathbf{w}^*)] = O\left(\frac{1}{\sqrt{t}}\right)$$

**SGD with momentum ($\beta = 0.9$):**
$$\mathbb{E}[\mathcal{L}(\mathbf{w}_t) - \mathcal{L}(\mathbf{w}^*)] = O\left(\rho^t\right)$$

where $\rho < 1$ is a contraction factor (exponential convergence).

**Practical impact:** Momentum often reduces iterations to convergence by 2-10×.

## Cumulative Effect: Why Momentum Works

Consider a quadratic loss landscape:

$$\mathcal{L}(\mathbf{w}) = \frac{1}{2} \mathbf{w}^T A \mathbf{w}$$

where $A$ is positive definite.

**Without momentum:**
- Steps directly toward optimum (noisy due to batch sampling)
- But orthogonal components make slow lateral progress

**With momentum:**
- Early steps accumulate in the true descent direction
- Lateral noise accumulates to approximately zero (oscillations cancel)
- Effective step size increases in the descent direction
- Parameter updates "build up" velocity toward the optimum

## Physics Analogy

Think of parameters as a ball rolling down a valley:

- Without momentum: ball slides down with friction (hard to move)
- With momentum: ball gains speed, rolling faster (inertia helps)
- High $\beta$: ball is heavy, takes longer to change direction
- Low $\beta$: ball is light, responds quickly to new forces

The velocity acts like **momentum in physics**:

$$\mathbf{v} = \beta \mathbf{v} + \mathbf{F}$$

is analogous to:

$$m \frac{d\mathbf{v}}{dt} = m \beta \frac{d\mathbf{v}}{dt} + \mathbf{F}$$

## PyTorch Implementation

```python
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.01,
    momentum=0.9  # enables momentum
)

# Training loop remains identical
for epoch in range(num_epochs):
    for batch in train_loader:
        loss = model(batch)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
```

### Internal Optimizer State

The optimizer maintains a velocity buffer for each parameter:

```python
# Inspect momentum buffer
for param_group in optimizer.param_groups:
    for param in param_group['params']:
        if param in optimizer.state:
            state = optimizer.state[param]
            if 'momentum_buffer' in state:
                v = state['momentum_buffer']
                print(f"Momentum buffer shape: {v.shape}")
```

### Saving and Loading with Momentum

Momentum buffers are part of optimizer state:

```python
# Save
checkpoint = {
    'model_state': model.state_dict(),
    'optimizer_state': optimizer.state_dict()
}
torch.save(checkpoint, 'checkpoint.pt')

# Load
checkpoint = torch.load('checkpoint.pt')
model.load_state_dict(checkpoint['model_state'])
optimizer.load_state_dict(checkpoint['optimizer_state'])
```

Without loading optimizer state, momentum buffers are reset to zero (training resumes as if fresh).

## Nesterov Momentum

A variant that looks ahead in the gradient direction for faster convergence:

$$\mathbf{v}_{t+1} = \beta \mathbf{v}_t + \nabla \mathcal{L}(\mathbf{w}_t - \alpha \beta \mathbf{v}_t)$$

$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \mathbf{v}_{t+1}$$

Instead of gradient at current position, use gradient after a lookahead step.

See [[Nesterov Momentum]] for detailed analysis.

**In PyTorch:**

```python
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.01,
    momentum=0.9,
    nesterov=True  # enables Nesterov variant
)
```

Nesterov momentum typically converges slightly faster than standard momentum.

## Interaction with Learning Rate

The effective learning rate includes the momentum coefficient:

$$\text{effective } \alpha = \frac{\alpha}{1 - \beta}$$

If you use momentum $\beta=0.9$, the effective step size is $10\times$ larger.

**When changing momentum, adjust learning rate accordingly:**

| $\beta$ | Effective scaling |
|---|---|
| $0.0$ | $1\times$ |
| $0.9$ | $10\times$ |
| $0.99$ | $100\times$ |

This is why learning rates for momentum-based methods are typically smaller than vanilla SGD.

## Practical Guidance

### When to Use Momentum

✅ **Use when:**
- You want faster convergence (2-10× speedup)
- Training on large datasets
- Dataset is stable (low noise helps momentum)

### Choosing $\beta$

**Default: 0.9** — works for most problems.

**Adjust based on:**
- Sparse/noisy data: use lower $\beta$ (e.g., 0.5)
- Stable data: can use higher $\beta$ (e.g., 0.99)
- High resolution images: try 0.95-0.99

### Common Hyperparameter Sets

**Standard CNN training:**
```python
lr=0.01, momentum=0.9, weight_decay=1e-4
```

**Large-scale distributed training:**
```python
lr=0.1, momentum=0.9, nesterov=True, weight_decay=1e-4
```

**RNN/LSTM training:**
```python
lr=0.001, momentum=0.9
# (lower lr, same momentum)
```

## Interaction with [[Learning Rate and Step Size|Learning Rate Schedules]]

Momentum interacts well with schedules:

```python
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.1,
    momentum=0.9
)

scheduler = torch.optim.lr_scheduler.StepLR(
    optimizer,
    step_size=30,
    gamma=0.1  # reduce lr by 10× every 30 epochs
)

for epoch in range(num_epochs):
    train()
    scheduler.step()  # updates learning rate, but momentum buffer persists
```

The momentum buffer is **not reset** when learning rate changes—it continues accumulating.

## Issues and Troubleshooting

### Issue: Loss Diverges with Momentum

**Cause:** Learning rate is too large (magnified by momentum).

**Solution:** Reduce learning rate or reduce $\beta$.

```python
# Before (diverges)
lr=0.1, momentum=0.9

# After (stable)
lr=0.01, momentum=0.9
# or
lr=0.05, momentum=0.5
```

### Issue: Momentum Buffer Not Helping

**Cause:** Gradients are too noisy (e.g., batch size is 1).

**Solution:** Increase batch size or reduce $\beta$.

### Issue: Slow Convergence Near Optimum

**Cause:** Momentum overshoots the optimum (velocity too high).

**Solution:** Reduce momentum coefficient or use learning rate schedule that decays $\alpha$.

## Comparison to [[Adam|Adam]]

| Aspect | Momentum | Adam |
|---|---|---|
| Parameters | lr, momentum, weight_decay | lr, betas, weight_decay |
| Convergence speed | Slower (more iterations) | Faster (fewer iterations) |
| Tuning difficulty | Moderate | Easy |
| Final generalization | Often better | Often slightly worse |
| Robustness | Sensitive to learning rate | Robust to learning rate |

See [[SGD vs Adam: When to Use Which]].

## See Also

- [[Stochastic Gradient Descent (SGD)]]: Foundation algorithm
- [[Nesterov Momentum]]: Improved momentum variant
- [[Learning Rate and Step Size]]: How momentum affects effective learning rate
- [[Adam]]: Alternative with adaptive per-parameter rates
- [[Weight Decay vs L2 Regularization]]: Using weight decay with momentum
- [[Convergence Criteria]]: How to detect convergence with momentum
