# SGD vs Adam: When to Use Which

This note compares [[Stochastic Gradient Descent (SGD)]] and [[Adam]], the two most commonly used optimizers in deep learning, to help guide selection based on problem characteristics.

## Head-to-Head Comparison

| Aspect | SGD + Momentum | Adam |
|---|---|---|
| **Convergence Speed (iterations)** | Slower | Faster (2-10× fewer) |
| **Wall-clock Time** | Depends on hardware | Often similar |
| **Learning Rate Tuning** | Difficult | Easy |
| **Generalization (test accuracy)** | Often better | Often slightly worse |
| **Memory per Parameter** | 1 buffer | 2 buffers |
| **Hyperparameters** | lr, momentum, schedule | lr, betas (usually default) |
| **Sparse Gradients** | Poor | Good |
| **Large Batch Training** | Excellent | Good |
| **Production Models** | Common | Common |

## Convergence Rate Analysis

### Iteration Complexity

**SGD with momentum:** Requires $O(1/\epsilon^2)$ gradient evaluations to reach $\epsilon$-approximate solution.

**Adam:** Also $O(1/\epsilon^2)$ theoretically, but with **better constants** in practice (often 2-10× faster).

**Practical implication:** On identical hardware with fixed batch sizes:
- SGD: needs 1000 iterations
- Adam: needs 100-500 iterations

### Wall-Clock Time

However, wall-clock time depends on:

1. **GPU utilization:** Both optimizers have similar per-iteration cost
2. **Batch size:** Both benefit from larger batches
3. **Learning rate tuning:** Poor tuning for SGD can waste hours; Adam works quickly with defaults

**In practice:**
- Careful SGD tuning: Often faster overall (fewer iterations, good LR, no wasted steps)
- Default SGD: Often slow (suboptimal LR requires restarts)
- Default Adam: Usually fast (requires minimal tuning)

## Generalization Gap

One of the most important differences:

**Test Accuracy (Generalization):**

| Setup | SGD | Adam |
|---|---|---|
| Standard training | Better (often 1-3% higher) | Worse |
| With regularization (weight decay, dropout) | Still better | Competitive |
| With learning rate schedule | Best | Good |

**Why the difference?**

1. **Noise as Regularization:** SGD's gradient noise helps find flatter minima (better for test data)
2. **Adam's Sharp Minima:** Adam converges to sharper local minima (lower training loss, higher test loss)
3. **Implicit Bias:** [[Saddle Points and Escape Dynamics|SGD explores the loss landscape more thoroughly]]

Modern practice: use SGD when final accuracy is paramount.

## Learning Rate Tuning Difficulty

### SGD

**Sensitive to learning rate choice:**

- Too small (0.001): Training is glacially slow
- Good (0.01): Converges steadily
- Large (0.1): Oscillates but can work
- Too large (1.0): Diverges immediately

**Hyperparameter sensitivity:**

```
SGD with lr=0.001: validation_acc = 87%
SGD with lr=0.01:  validation_acc = 92%
SGD with lr=0.1:   validation_acc = 88%
```

Small change in learning rate → large change in final accuracy.

### Adam

**Robust to learning rate choice:**

- Small (0.0001): Slower but still converges
- Default (0.001): Usually best
- Large (0.01): Still works reasonably
- Very large (0.1): Usually diverges, but even failure is quick to detect

**Hyperparameter robustness:**

```
Adam with lr=0.0001: validation_acc = 89%
Adam with lr=0.001:  validation_acc = 91%
Adam with lr=0.01:   validation_acc = 90%
```

Large range of learning rates work, just with different speeds.

## When to Choose SGD with Momentum

**Use SGD when:**

✅ **Final accuracy is critical** (research papers, production ML)
- Often achieves 1-3% higher test accuracy
- Worth the tuning effort

✅ **Large-scale distributed training**
- Momentum scales predictably with batch size
- Well-studied optimization dynamics
- Industry standard for large models

✅ **You have time to tune learning rate**
- Systematic hyperparameter search
- Grid search or Bayesian optimization
- Access to GPU cluster for experiments

✅ **Stable, clean datasets**
- SGD momentum's advantages shine with consistent gradients
- Sparse, noisy data favors Adam

✅ **You want deterministic, interpretable behavior**
- SGD trajectory is more predictable
- Easier to diagnose divergence or oscillation

### Example: Production CNN for Image Classification

```python
# Training code for competition/production
model = ResNet50(pretrained=False)

optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.1,              # carefully chosen
    momentum=0.9,
    nesterov=True,
    weight_decay=1e-4
)

scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=100
)

for epoch in range(100):
    train()
    validate()
    scheduler.step()
    
# Result: 93.2% test accuracy
```

## When to Choose Adam

**Use Adam when:**

✅ **Fast prototyping and iteration**
- Get results quickly without tuning
- Minimal hyperparameter search

✅ **Limited computational budget**
- Fewer iterations to acceptable performance
- Good for quick feasibility studies

✅ **Sparse or variable-scale gradients**
- NLP with variable sequence lengths
- Recommendation systems with sparse embeddings
- Mixed-precision training

✅ **Deep networks with many layers**
- Transformer models (standard choice)
- Very deep ResNets
- Where learning rate tuning is difficult

✅ **Unknown problem characteristics**
- First time working on a problem
- Unfamiliar model architectures
- Proof-of-concept stage

### Example: NLP Model (Transformer)

```python
# Quick prototyping of BERT-like model
model = BertModel(config)

optimizer = torch.optim.AdamW(  # Adam with weight decay
    model.parameters(),
    lr=1e-4,             # default, not tuned
    weight_decay=0.01
)

scheduler = torch.optim.lr_scheduler.LinearLR(
    optimizer,
    total_iters=1000
)

for epoch in range(3):
    for batch in train_loader:
        loss = model(batch)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    scheduler.step()

# Result: 87% accuracy on dev set, convergence in hours
```

## Decision Tree

```
START: Choosing an optimizer

1. Is this for research/competition (final accuracy critical)?
   YES → Use SGD with momentum
   NO → Go to 2

2. Do you have sparse gradients (NLP, recommendations)?
   YES → Use Adam
   NO → Go to 3

3. Do you have time to tune learning rate?
   YES → Use SGD with momentum (better final accuracy)
   NO → Use Adam (robust defaults)

4. Is wall-clock time critical?
   YES → Use Adam (fewer iterations)
   NO → Use SGD (often faster overall)
```

## Practical Hybrid Strategy

**Many teams use a two-phase approach:**

### Phase 1: Explore with Adam
```python
# Quick experiments, architecture search
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Train for N epochs, see if promising
for epoch in range(N):
    train()
    if validation_accuracy > threshold:
        proceed_to_phase_2 = True
        break
```

### Phase 2: Fine-tune with SGD
```python
# Once architecture is fixed, optimize accuracy with SGD
# Load best Adam checkpoint and continue with SGD

optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.01,
    momentum=0.9,
    nesterov=True
)

scheduler = torch.optim.lr_scheduler.StepLR(
    optimizer,
    step_size=10,
    gamma=0.1
)

for epoch in range(50):
    train()
    validate()
    scheduler.step()
```

Result: Fast iteration + best final accuracy.

## Adam Variants: Improving Generalization

If you want Adam's speed with better generalization:

### AdamW (Decoupled Weight Decay)

```python
# Better than Adam for generalization
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=0.001,
    weight_decay=0.01
)
```

[[AdamW]] decouples weight decay from gradient scaling, improving final accuracy vs. vanilla Adam.

### [[AMSGrad]]

```python
# Convergence guarantee (but not clearly better in practice)
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001,
    amsgrad=True
)
```

Improves theoretical convergence guarantees.

## Learning Rate Schedule Impact

Both optimizers benefit from schedules, but differently:

### SGD with Schedule

```python
optimizer = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9)

scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=100
)

# Result: Very important for final accuracy
# Without schedule: 90% accuracy
# With schedule: 93% accuracy
```

Schedule is **critical** for SGD (often 3% improvement).

### Adam with Schedule

```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=100
)

# Result: Helpful but less critical than SGD
# Without schedule: 91% accuracy
# With schedule: 92% accuracy
```

Schedule helps (1% improvement) but not essential for Adam.

## Mixed Results: When Both Are Comparable

In some cases (especially modern architectures like Vision Transformers), SGD and Adam achieve similar final accuracy:

- Both: ~91% accuracy
- SGD: more iterations, but reaches there stably
- Adam: fewer iterations, slightly noisier

In these cases, **choose based on other factors:**
- Team preference / codebase standards
- Infrastructure (distributed training optimizations available)
- Simplicity (Adam usually simpler for new projects)

## Practical Recommendations

### For Image Classification (CNN)

```python
# ResNet, VGG, DenseNet, etc.

# Production/competition:
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.1, momentum=0.9, nesterov=True, weight_decay=1e-4
)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)

# Quick experiment:
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=0.001, weight_decay=0.01
)
```

### For NLP (Transformers)

```python
# BERT, GPT, etc.

# Production:
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=1e-4, weight_decay=0.01
)
scheduler = torch.optim.lr_scheduler.LinearLR(optimizer, total_iters=20000)

# Quick experiment:
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
```

### For Computer Vision (ViT, CLIP)

```python
# Vision Transformer

# Production:
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.02, momentum=0.9, nesterov=True, weight_decay=1e-4
)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=300)

# Or Adam (both work well):
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=0.001, weight_decay=0.05
)
```

## Summary

| Goal | Choose |
|---|---|
| Best final accuracy | SGD + schedule |
| Fastest convergence | Adam |
| Sparse gradients | Adam |
| Most robust | Adam |
| Production vision model | SGD |
| Production NLP model | Adam |
| Unknown/experimental | Adam (then switch to SGD) |

## See Also

- [[Stochastic Gradient Descent (SGD)]]: Detailed SGD analysis
- [[Adam]]: Detailed Adam analysis
- [[Learning Rate and Step Size]]: How LR affects both
- [[Learning Rate Schedules]]: Interacting with schedules
- [[AdamW]]: Improved Adam variant
- [[Weight Decay vs L2 Regularization]]: Why Adam often needs AdamW
