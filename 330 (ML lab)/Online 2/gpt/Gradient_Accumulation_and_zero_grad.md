# Gradient Accumulation and zero_grad()

This note covers an important but often misunderstood aspect of PyTorch optimization: gradient accumulation and the purpose of `optimizer.zero_grad()`.

## The Gradient Accumulation Issue

By default, PyTorch **accumulates** gradients across `backward()` calls:

```python
model = torch.nn.Linear(10, 5)
loss_fn = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

x = torch.randn(2, 10)
y = torch.randn(2, 5)

# First iteration
output = model(x)
loss1 = loss_fn(output, y)
loss1.backward()  # param.grad = ∇L₁

# Second iteration (forgetting zero_grad)
output = model(x)
loss2 = loss_fn(output, y)
loss2.backward()  # param.grad = ∇L₁ + ∇L₂ (ACCUMULATED!)

# The gradient now contains gradients from TWO losses
# optimizer.step() uses the accumulated gradient
```

This is usually **not desired** for standard mini-batch training.

## Why Accumulation Exists

The accumulation behavior is intentional, designed for **gradient accumulation**—a technique where multiple loss computations are combined before an optimizer step.

## Standard Training: Reset After Each Step

```python
for epoch in range(num_epochs):
    for batch in train_loader:
        x, y = batch
        
        # Forward pass
        output = model(x)
        loss = loss_fn(output, y)
        
        # Backward: compute gradient
        loss.backward()  # param.grad accumulates
        
        # Optimizer step: apply accumulated gradient
        optimizer.step()
        
        # CRITICAL: Reset gradients for next iteration
        optimizer.zero_grad()  # param.grad = 0
```

### What zero_grad() Does

```python
# Pseudocode inside optimizer.zero_grad()
for param_group in optimizer.param_groups:
    for param in param_group['params']:
        if param.grad is not None:
            param.grad.zero_()  # set to 0
```

After `zero_grad()`, all gradients are reset to 0, and the next `backward()` starts fresh.

**Without this reset:**
```
Iteration 1: param.grad = ∇L₁
Iteration 2: param.grad = ∇L₁ + ∇L₂
Iteration 3: param.grad = ∇L₁ + ∇L₂ + ∇L₃
...
Iteration N: param.grad = ∇L₁ + ∇L₂ + ... + ∇Lₙ
```

All past gradients are included → update is completely wrong.

## Proper Training Loop Pattern

```python
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

for epoch in range(num_epochs):
    for batch_idx, (x, y) in enumerate(train_loader):
        # 1. Forward pass
        output = model(x)
        loss = loss_fn(output, y)
        
        # 2. Backward: compute ∇L
        loss.backward()
        
        # 3. Update: w ← w - α∇L
        optimizer.step()
        
        # 4. Reset: ∇L ← 0 for next iteration
        optimizer.zero_grad()
        
        # Order of 3 and 4 can be switched (see below)
```

### Order Variant: zero_grad() First

```python
# Both orderings work:

# Option A: step, then zero (standard)
optimizer.step()
optimizer.zero_grad()

# Option B: zero, then step
optimizer.zero_grad()
optimizer.step()

# Option B allows: zero at start of epoch, no step needed
# Option A is more symmetric with backward
```

In modern PyTorch, using `model.zero_grad()` or `optimizer.zero_grad()` are equivalent for standard optimization.

## Gradient Accumulation: Intentional Use Case

Sometimes you **want** to accumulate gradients across multiple batches:

**Example: Simulating larger batch size**

```python
effective_batch_size = 256
actual_batch_size = 32
accumulation_steps = effective_batch_size // actual_batch_size  # 8

optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

for epoch in range(num_epochs):
    for batch_idx, (x, y) in enumerate(train_loader):
        # Forward and backward: accumulate gradients
        output = model(x)
        loss = loss_fn(output, y) / accumulation_steps
        loss.backward()  # ∇L accumulates
        
        # Update only every accumulation_steps
        if (batch_idx + 1) % accumulation_steps == 0:
            optimizer.step()      # apply accumulated gradient
            optimizer.zero_grad() # reset for next accumulation
```

**Why accumulate?**
- Large batch sizes (e.g., 256) give better gradients but may not fit in GPU memory
- By accumulating 8 batches of 32 samples, we simulate batch size 256
- Effective learning rate scales with accumulated batch size
- Gradient noise is lower (better training)

**Important:** Divide loss by `accumulation_steps` to keep learning rate effective.

## Gradient Accumulation: Memory Efficiency

```python
# Without accumulation (OOM if batch too large):
batch_size = 256
# Trying to load 256 samples → Out of Memory

# With accumulation (memory efficient):
batch_size = 32
accumulation_steps = 8

# Effective batch size = 32 × 8 = 256
# But only 32 samples in GPU memory at once
```

Modern training often uses accumulation to simulate very large batches without OOM.

## Interaction with Learning Rate

When using gradient accumulation, **do not change the learning rate**:

```python
# Correct: same learning rate
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# Accumulating 8 batches of 32
for batch_idx in range(0, 256, 32):
    loss = ...
    loss.backward()
    
    if (batch_idx + 32) % 256 == 0:
        optimizer.step()
        optimizer.zero_grad()
```

The learning rate is applied to the **accumulated gradient**, which already represents a larger batch. The effective learning rate automatically scales.

Compare:
```
No accumulation: α × (single batch gradient)
With 8× accumulation: α × (8 × single batch gradient) ≈ scaled effect
```

## Code Pattern: Safer Implementation

```python
# More robust pattern with explicit accumulation handling
def train_with_accumulation(model, optimizer, train_loader, accumulation_steps=8):
    for epoch in range(num_epochs):
        optimizer.zero_grad()  # start clean
        
        for batch_idx, (x, y) in enumerate(train_loader):
            output = model(x)
            loss = loss_fn(output, y) / accumulation_steps
            loss.backward()
            
            # Check if we should do optimizer step
            if (batch_idx + 1) % accumulation_steps == 0:
                optimizer.step()
                optimizer.zero_grad()
        
        # Handle case where final iteration didn't trigger step
        # (if len(train_loader) not divisible by accumulation_steps)
        # Usually okay to skip this edge case
```

## Mixed Precision Training: Special Case

In mixed precision training with `torch.cuda.amp`, gradient accumulation interacts specially:

```python
from torch.cuda.amp import autocast, GradScaler

optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
scaler = GradScaler()
accumulation_steps = 4

for epoch in range(num_epochs):
    for batch_idx, (x, y) in enumerate(train_loader):
        with autocast():
            output = model(x)
            loss = loss_fn(output, y) / accumulation_steps
        
        scaler.scale(loss).backward()  # accumulates scaled gradient
        
        if (batch_idx + 1) % accumulation_steps == 0:
            scaler.step(optimizer)  # apply to unscaled gradient
            scaler.update()
            optimizer.zero_grad()
```

The scaler must be called, not optimizer.step() directly.

## Gradient Accumulation with Multiple Losses

Sometimes you have multiple loss terms to optimize jointly:

```python
# Multi-task learning: combine losses
loss_fn1 = torch.nn.CrossEntropyLoss()  # classification
loss_fn2 = torch.nn.MSELoss()            # regression

optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(num_epochs):
    for batch in train_loader:
        x, y1, y2 = batch
        
        output1, output2 = model(x)
        loss1 = loss_fn1(output1, y1)
        loss2 = loss_fn2(output2, y2)
        
        # Combine losses
        total_loss = loss1 + 0.5 * loss2  # weighted combination
        
        total_loss.backward()  # accumulates ∇(L₁ + 0.5*L₂)
        
        optimizer.step()
        optimizer.zero_grad()
```

Both losses contribute to the same gradient computation.

## Common Mistakes

### Mistake 1: Forgetting zero_grad()

```python
# WRONG: accumulates gradients incorrectly
for epoch in range(num_epochs):
    for batch in train_loader:
        loss = model(batch)
        loss.backward()
        optimizer.step()
        # FORGOT: optimizer.zero_grad()

# Result: training diverges or stalls
```

### Mistake 2: Calling zero_grad() Without backward()

```python
# Odd but harmless:
optimizer.zero_grad()
loss = model(batch)  # no backward!
optimizer.step()     # uses zero gradients

# Result: no parameter updates (gradients are 0)
```

### Mistake 3: Backward Without Step

```python
# WRONG: accumulates gradients forever
for epoch in range(num_epochs):
    for batch in train_loader:
        loss = model(batch)
        loss.backward()
        # FORGOT: optimizer.step()
        optimizer.zero_grad()

# Result: gradients are zeroed before being applied
```

## Debugging: Check Gradient State

```python
# To verify gradients are being computed correctly:
loss = model(batch)
loss.backward()

for name, param in model.named_parameters():
    if param.grad is not None:
        grad_norm = param.grad.norm()
        print(f"{name}: grad norm = {grad_norm:.6f}")
    else:
        print(f"{name}: NO GRADIENT (not used in loss?)")

optimizer.step()
optimizer.zero_grad()  # clear after checking
```

## Gradient Accumulation with Distributed Training

In distributed training, gradients from multiple GPUs are synchronized:

```python
# Each GPU processes a batch, computes gradients
loss.backward()

# DDP automatically all-reduces gradients across GPUs
# BEFORE optimizer.step()

# So with accumulation on 4 GPUs:
# Total effective batch size = batch_size × num_gpus × accumulation_steps
```

The accumulation pattern works as expected; DDP handles synchronization.

## Best Practices

**1. Standard training (no accumulation):**
```python
loss.backward()
optimizer.step()
optimizer.zero_grad()
```

**2. With accumulation:**
```python
loss.backward()
if (batch_idx + 1) % accumulation_steps == 0:
    optimizer.step()
    optimizer.zero_grad()
```

**3. With mixed precision:**
```python
loss.backward()
if (batch_idx + 1) % accumulation_steps == 0:
    scaler.step(optimizer)
    scaler.update()
    optimizer.zero_grad()
```

**4. Always verify gradients are computed:**
```python
loss.backward()
assert param.grad is not None, "Gradient not computed!"
```

## See Also

- [[Stochastic Gradient Descent (SGD)]]: How optimizer.step() uses gradients
- [[Gradient Descent Fundamentals]]: Gradient computation basics
- [[Optimizer State and Buffers in PyTorch]]: State management
- [[Learning Rate and Step Size]]: How learning rate scales with batch size
- [[Batch Normalization]]: Interaction with gradient accumulation
