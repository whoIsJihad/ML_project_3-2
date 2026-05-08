# Optimizer State and Buffers in PyTorch

PyTorch optimizers maintain internal state—buffers that track information between iterations. Understanding this state is essential for proper checkpoint management, distributed training, and debugging.

## What Is Optimizer State?

Each optimizer stores a **state dictionary** per parameter group:

```
Optimizer State:

param_group[0]:
  - params: [param1, param2, ...]  # the actual parameters
  - lr: 0.01
  - momentum: 0.9
  - ... (other hyperparameters)

optimizer.state:  # internal buffers
  param1:
    - momentum_buffer    (for SGD with momentum)
    - step              (iteration counter)
  param2:
    - momentum_buffer
    - step
  ...
```

## Type of Buffers by Optimizer

### SGD (No Momentum)
```python
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
# No internal buffers for vanilla SGD
```

### SGD with Momentum
```python
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Internal state:
optimizer.state[param] = {
    'momentum_buffer': tensor,  # accumulated gradient
    'step': 42                   # iteration number
}
```

### Adam
```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Internal state:
optimizer.state[param] = {
    'step': 42,
    'exp_avg': tensor,      # first moment (momentum)
    'exp_avg_sq': tensor    # second moment (adaptive scaling)
}
```

### RMSprop
```python
optimizer = torch.optim.RMSprop(model.parameters(), lr=0.01)

# Internal state:
optimizer.state[param] = {
    'step': 42,
    'square_avg': tensor    # moving average of squared gradients
}
```

### Adagrad
```python
optimizer = torch.optim.Adagrad(model.parameters(), lr=0.01)

# Internal state:
optimizer.state[param] = {
    'step': 42,
    'sum': tensor           # cumulative sum of squared gradients
}
```

## Accessing Optimizer State

### Inspecting a Specific Parameter

```python
model = torch.nn.Linear(10, 5)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Forward and backward to initialize state
x = torch.randn(2, 10)
loss = model(x).sum()
loss.backward()
optimizer.step()

# Now state is populated
param = list(model.parameters())[0]

if param in optimizer.state:
    state = optimizer.state[param]
    print(f"Keys in state: {state.keys()}")      # dict_keys(['momentum_buffer', 'step'])
    print(f"Momentum buffer shape: {state['momentum_buffer'].shape}")
    print(f"Step: {state['step']}")
```

### Iterating Over All Parameters and State

```python
for param_group in optimizer.param_groups:
    for param in param_group['params']:
        if param in optimizer.state:
            state = optimizer.state[param]
            for key, value in state.items():
                if isinstance(value, torch.Tensor):
                    print(f"  {key}: shape {value.shape}, dtype {value.dtype}")
                else:
                    print(f"  {key}: {value}")
```

## State Persistence: Saving and Loading

### Why Save State?

When you save a checkpoint and resume training later:

1. Parameters themselves are saved and loaded
2. But momentum buffers / adaptive learning rates are **lost**
3. Training effectively restarts from scratch (with different weights but zero buffers)

**Effect of not loading optimizer state:**

```python
# Epoch 50 training:

# Case 1: With saved state
optimizer.load_state_dict(checkpoint['optimizer_state'])
# Momentum buffer loaded: v = [large value]
# Continue training smoothly

# Case 2: Without saved state
# Momentum buffer is zero: v = 0
# Takes several iterations to rebuild momentum
# Training has a "restart" effect
```

### Proper Checkpoint Management

```python
# === SAVING ===
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),  # CRITICAL
    'scheduler_state_dict': scheduler.state_dict(),  # if using scheduler
    'loss': loss
}
torch.save(checkpoint, f'checkpoint_epoch_{epoch}.pt')

# === LOADING ===
checkpoint = torch.load(f'checkpoint_epoch_{epoch}.pt')

model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])  # CRITICAL
if scheduler is not None:
    scheduler.load_state_dict(checkpoint['scheduler_state_dict'])

start_epoch = checkpoint['epoch'] + 1
# Resume training from saved state
```

### What Gets Saved

```python
optimizer_state = optimizer.state_dict()

# Returns:
{
    'state': {
        # param id (memory address) -> state dict
        12345678: {
            'momentum_buffer': tensor([...]),
            'step': 42
        },
        87654321: {
            'momentum_buffer': tensor([...]),
            'step': 42
        }
    },
    'param_groups': [
        {
            'params': [0, 1, ...],  # indices into model.parameters()
            'lr': 0.01,
            'momentum': 0.9,
            ...
        }
    ]
}
```

## Initialization and Growth

### First Iteration: State Not Initialized

```python
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

print(len(optimizer.state))  # 0 (empty)

x = torch.randn(2, 10)
loss = model(x).sum()
loss.backward()
optimizer.step()

print(len(optimizer.state))  # now equals number of parameters
```

State buffers are created **lazily** on the first `optimizer.step()` call.

### Memory Growth

State buffers grow with training:

```python
# Before training
model_size = sum(p.numel() for p in model.parameters()) * 4  # bytes (float32)
print(f"Model size: {model_size / 1e6} MB")

# For SGD with momentum, total memory:
# model + momentum buffer = 2x model size
# For Adam: model + m + v = 3x model size

optimizer = torch.optim.Adam(model.parameters())
required_memory = model_size * 3  # rough estimate
```

**Implication:** Optimizer state can be significant. For billion-parameter models, this is a bottleneck.

## Resetting State

### Completely Clear State (Start Fresh)

```python
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# After many iterations, state is large
print(len(optimizer.state))  # large

# To clear it:
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
# OR
optimizer.state.clear()

# Now training restarts with fresh momentum buffers
```

**Use case:** Switching learning rates or optimizers mid-training.

### Partial Reset

Cannot easily reset individual parameter buffers. If you need to, create a new optimizer:

```python
# To reset only certain parameters' state:
new_optimizer = torch.optim.SGD(
    [{'params': [param1, param2], 'lr': 0.001},
     {'params': [param3, param4], 'lr': 0.01}],
    momentum=0.9
)
# Copy non-reset params' state if needed
```

## Distributed Training: State Distribution

In distributed training, optimizer state must be **synchronized** across devices:

```python
# Distributed setting: model replicated across 8 GPUs
model = torch.nn.parallel.DistributedDataParallel(model)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Each GPU has a copy of:
# - model parameters
# - optimizer state (momentum buffers)

# Problem: If gradients differ slightly across GPUs, momentum becomes inconsistent

# Solution: All-reduce gradients before optimizer.step()
for batch in train_loader:
    loss = model(batch)
    loss.backward()
    
    # PyTorch's DDP automatically all-reduces gradients
    # So momentum is computed on synchronized gradients
    
    optimizer.step()
    optimizer.zero_grad()
```

DDP handles synchronization; optimizer state remains consistent across replicas.

## Learning Rate Groups and State

Multiple parameter groups can have different learning rates, **but share optimizer state**:

```python
optimizer = torch.optim.SGD(
    [
        {'params': [param1, param2], 'lr': 0.01},
        {'params': [param3, param4], 'lr': 0.001}  # different lr
    ],
    momentum=0.9
)

# All parameters share the same momentum coefficient (0.9)
# But have different learning rates
# Optimizer state is independent per parameter

print(optimizer.param_groups[0]['lr'])  # 0.01
print(optimizer.param_groups[1]['lr'])  # 0.001

# State is separate:
print(optimizer.state[param1])  # has its own momentum_buffer
print(optimizer.state[param3])  # has its own momentum_buffer
```

## Common Issues and Solutions

### Issue: Nan/Inf in Optimizer State

**Cause:** Gradient explosion or bad learning rate.

**Solution:**
```python
# Check for NaN in state
for param_group in optimizer.param_groups:
    for param in param_group['params']:
        if param in optimizer.state:
            for key, value in optimizer.state[param].items():
                if isinstance(value, torch.Tensor):
                    if torch.isnan(value).any():
                        print(f"NaN in {key}")
```

**Fix:**
1. Reduce learning rate
2. Use gradient clipping
3. Check loss function for invalid operations

### Issue: Memory Exhausted

**Cause:** Optimizer state too large (especially Adam with billions of parameters).

**Solutions:**
```python
# Use SGD instead of Adam (1/3 memory)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Or use sharded optimizer (distributed training)
# or gradient checkpointing (different issue, not optimizer)
```

### Issue: Inconsistent Training After Loading

**Cause:** Forgot to load optimizer state.

**Fix:**
```python
# ALWAYS do this:
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

# NOT just:
model.load_state_dict(checkpoint['model_state_dict'])  # only this
```

## Inspection: Debug Optimizer Behavior

```python
# Log optimizer state for debugging
def log_optimizer_state(optimizer, step):
    total_norm = 0
    for param_group in optimizer.param_groups:
        for param in param_group['params']:
            if param in optimizer.state:
                for key, value in optimizer.state[param].items():
                    if isinstance(value, torch.Tensor):
                        total_norm += value.norm().item() ** 2
    
    print(f"Step {step}: State norm = {total_norm ** 0.5}")

for step in range(num_steps):
    loss.backward()
    optimizer.step()
    log_optimizer_state(optimizer, step)
```

## See Also

- [[Stochastic Gradient Descent (SGD)]]: SGD state structure
- [[SGD with Momentum]]: Momentum buffer details
- [[Adam]]: Two-moment state structure
- [[Gradient Accumulation and zero_grad()]]: Interaction with gradients
- [[Weight Decay vs L2 Regularization]]: State implications
