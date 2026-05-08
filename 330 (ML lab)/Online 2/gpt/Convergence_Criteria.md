# Convergence Criteria

Convergence means training is done—the model has stopped improving significantly. This note explains how to detect it and when to stop training.

## When Is Training "Done"?

In practice, we stop training when one of these happens:

1. **Validation loss stops improving:** Loss hasn't decreased for N epochs
2. **Fixed epoch count:** Train for 100 epochs and stop
3. **Time limit:** Training hits a wall-clock time limit
4. **Gradient becomes tiny:** Gradient is close to zero

The most important is **#1: validation loss stops improving**.

## Strategy 1: Early Stopping (Best)

Stop training when the model stops getting better on validation data.

```python
best_val_loss = float('inf')
patience = 10  # wait 10 epochs without improvement

for epoch in range(1000):
    train_loss = train()
    val_loss = validate()
    
    if val_loss < best_val_loss:
        # Better! Save this model
        best_val_loss = val_loss
        patience_counter = 0
        torch.save(model.state_dict(), 'best_model.pt')
    else:
        # No improvement
        patience_counter += 1
        if patience_counter >= patience:
            print(f"Stopping at epoch {epoch}: no improvement")
            break

# Load the best model found
model.load_state_dict(torch.load('best_model.pt'))
```

**Why this works:**
- Prevents overfitting (validation loss increases when overfitting starts)
- Automatic (doesn't require manual epoch count)
- Finds the sweet spot: good training + good generalization

**Typical patience:** 5-20 epochs (adjust based on your dataset)

## Strategy 2: Fixed Epoch Count

Simple but requires knowing how many epochs to train.

```python
num_epochs = 100

for epoch in range(num_epochs):
    train()
    validate()
    
# Training automatically stops after 100 epochs
```

**Pros:** Simple, reproducible  
**Cons:** Might stop too early or too late; wastes training time

## What Is a "Good" Convergence Point?

Three metrics matter:

### 1. Training Loss

Loss on the data the model trained on. **Should decrease over time.**

```
Training loss |
              |\
              | \___
              |     \___
              |         ~~ (small oscillations)
              |____________ Epoch
```

If training loss is constant or increasing, learning rate is wrong.

### 2. Validation Loss

Loss on data the model **hasn't seen** (test-like data during training). **Should decrease, then plateau.**

```
Validation loss |
                |\
                | \
                |  \___
                |      \___
                |          ~~~~ (plateau)
                |________________ Epoch
```

When validation loss starts increasing while training loss decreases → **overfitting** (stop here).

### 3. Generalization Gap

Difference between training and validation loss.

```
Gap = Validation Loss - Training Loss
```

**Small gap:** Model generalizes well (good)  
**Large gap:** Overfitting (bad)

**What to expect:**
- Start of training: gap is large (model hasn't learned anything)
- Middle: gap decreases (model is learning)
- End: gap increases (model is overfitting)

Early stopping catches you at the minimum gap.

## How to Monitor Training

Print these numbers every epoch to know if training is working:

```python
for epoch in range(num_epochs):
    train_loss = train()
    val_loss = validate()
    
    print(f"Epoch {epoch}: train_loss={train_loss:.4f}, val_loss={val_loss:.4f}")
```

Example output:
```
Epoch 0: train_loss=2.3001, val_loss=2.2998
Epoch 1: train_loss=2.1234, val_loss=2.1256
Epoch 2: train_loss=1.8956, val_loss=1.9123
Epoch 3: train_loss=1.4567, val_loss=1.5234
Epoch 4: train_loss=1.1234, val_loss=1.2567  ← validation starting to increase
Epoch 5: train_loss=0.8901, val_loss=1.3456  ← overfitting! Stop here.
```

**What to look for:**

| Pattern | Meaning | Action |
|---------|---------|--------|
| Both decreasing | Good training | Continue |
| Train decreases, val flat | Nearly converged | Soon will overfit |
| Val increases, train decreases | Overfitting | Stop now (early stopping) |
| Both constant | Converged or stuck | Stop |
| Train increases | Learning rate too high | Reduce lr and restart |

## Common Patterns and Fixes

### Pattern 1: Training Won't Converge

```
Loss |
     |████ (very noisy, doesn't decrease)
     |  ██████
     |██████████
```

**Cause:** Learning rate too high or model is broken  
**Fix:** Reduce learning rate (e.g., 0.1 → 0.01) or check model code

### Pattern 2: Training is Glacially Slow

```
Loss |
     |\
     | \
     |  ________________  (barely decreasing)
```

**Cause:** Learning rate too small  
**Fix:** Increase learning rate (e.g., 0.001 → 0.01)

### Pattern 3: Perfect Training, Overfitting

```
Training loss:   \____
Validation loss:     \____/\/\  ← going up!
```

**Cause:** Model is memorizing training data  
**Fix:** Use early stopping to stop before overfitting

### Pattern 4: Both Losses Plateau Early

```
Loss |
     |\
     | \__________
```

**Cause:** Learning rate too small, or stuck at poor local minimum  
**Fix:** Increase learning rate, or use learning rate schedule (decay)

## Practical Early Stopping Code

```python
from torch.utils.data import DataLoader

best_val_loss = float('inf')
patience = 10
patience_counter = 0

for epoch in range(200):  # max 200 epochs
    # Train
    train_loss = 0
    for batch in train_loader:
        output = model(batch)
        loss = loss_fn(output, batch.y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        train_loss += loss.item()
    
    train_loss /= len(train_loader)
    
    # Validate
    val_loss = 0
    model.eval()
    with torch.no_grad():
        for batch in val_loader:
            output = model(batch)
            loss = loss_fn(output, batch.y)
            val_loss += loss.item()
    model.train()
    
    val_loss /= len(val_loader)
    
    print(f"Epoch {epoch}: train={train_loss:.4f}, val={val_loss:.4f}")
    
    # Early stopping
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        patience_counter = 0
        # Save best model
        torch.save(model.state_dict(), 'best_model.pt')
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print(f"Early stopping at epoch {epoch}")
            break

# Load best model
model.load_state_dict(torch.load('best_model.pt'))
```

## Key Takeaways

1. **Early stopping is best:** Stop when validation loss plateaus
2. **Watch both training and validation loss:** Only train loss → overfitting
3. **Monitor the gap:** Large gap = overfitting
4. **Don't train too long:** Unnecessary computation, worse generalization
5. **Save the best model:** Keep the epoch with lowest validation loss, not the last epoch

## See Also

- [[Stochastic Gradient Descent (SGD)]]: The training algorithm
- [[Learning Rate and Step Size]]: If training won't converge
- [[Gradient Descent Fundamentals]]: Understanding loss landscape
