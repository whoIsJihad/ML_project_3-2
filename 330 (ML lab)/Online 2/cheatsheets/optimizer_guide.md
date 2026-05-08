---

# 🎮 PyTorch Optimizers: What to Tune & How (Beginner Guide)

This guide explains **optimizers** in PyTorch for beginners. Optimizers update your neural network weights during training. Think of them as different "learning strategies."

---

## 📖 Key Terms You'll See (Explained Simply)

Before diving in, let's define terms used throughout this guide:

- **Smoothness**: How steady the training is. Loss decreases without big jumps.
  - **Good smoothness**: Loss goes from 2.0 → 1.8 → 1.6 → 1.4 (steady drop)
  - **Bad smoothness**: Loss goes 2.0 → 1.5 → 2.5 → 1.2 (jumpy)

- **Stability**: Training doesn't crash or go crazy. Loss stays reasonable.
  - **Stable**: Loss decreases from 2.0 to 0.5 over 100 epochs
  - **Unstable**: Loss explodes to 1000 or becomes NaN (not a number)

- **Speed**: How fast the model learns. Measured in epochs to reach good performance.
  - **Fast**: Reaches 90% accuracy in 10 epochs
  - **Slow**: Takes 100 epochs for same accuracy

- **Convergence**: Actually reaching the best possible solution.
  - **Converges**: Loss stops decreasing at a low value (like 0.1)
  - **Doesn't converge**: Loss keeps decreasing very slowly forever

These terms help compare optimizers. No single optimizer is best at all - it depends on your problem!

---

## 📊 SGD (Stochastic Gradient Descent) — The Basic One

## 📊 SGD (Stochastic Gradient Descent) — The Basic One

### What it does:
Updates weights by moving in the direction that reduces loss, using a fixed step size.

### Parameters you can tune:

```python
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=1e-4, dampening=0, nesterov=False)
```

- **`lr` (learning rate)**: How big each step is
  - **How to set**: Start with 0.01 or 0.1. Too high = overshoots. Too low = slow learning.
  - **Range**: 0.001 to 0.1 usually

- **`momentum`**: Helps overcome local minima by adding "speed" from previous steps
  - **How to set**: 0.9 (default good). 0 = no momentum. 0.99 = very smooth.
  - **When to use**: Almost always with SGD. Makes it faster and more stable.

- **`weight_decay`**: L2 regularization (prevents overfitting by shrinking weights)
  - **What is overfitting?** Model memorizes training data too well, performs badly on new data
  - **How it works**: Adds penalty for large weights, forcing model to use smaller, simpler weights
  - **How to set**: 
    - 0 = no penalty (use when no overfitting)
    - 0.0001 or 0.001 (use when model overfits)
  - **Scientific notation reminder**: 
    - 1e-4 = 0.0001, 1e-3 = 0.001 (e means ×10^)
  - **When to use**: If training accuracy high but test accuracy low (overfitting sign)
  - **Think of it as**: A teacher giving extra homework to prevent cheating

- **`dampening`**: Reduces the momentum effect over time
  - **What is momentum?** Like a ball rolling downhill - keeps moving in same direction
  - **How dampening works**: Gradually slows down the "rolling ball" to prevent overshooting
  - **How to set**: Usually 0 (no dampening). Sometimes 0.1-0.5.
  - **When to use**: Rarely. Only if momentum makes training unstable.
  - **Think of it as**: Brakes on the rolling ball
- **`nesterov`**: Advanced momentum variant (set True for better results sometimes)

### When to use SGD:
- **Simple problems**: Linear regression, basic classification
- **When you want control**: You can tune learning rate manually
- **Large datasets**: More stable than Adam
- **Don't use for**: Complex networks (CNNs, RNNs) - too slow

### Example settings:
```python
# Basic SGD
optim.SGD(model.parameters(), lr=0.01)

# With momentum (recommended)
optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# With regularization
optim.SGD(model.parameters(), lr=0.01, momentum=0.9, weight_decay=1e-4)
```

---

## 🚀 Adam (Adaptive Moment Estimation) — The Smart One

### What it does:
Automatically adjusts learning rate for each parameter. "Adaptive" means it learns the best step size for each weight.

### Parameters you can tune:

```python
optimizer = optim.Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999), eps=1e-8, weight_decay=0, amsgrad=False)
```

- **`lr` (learning rate)**: Initial step size (Adam adjusts it automatically)
  - **How to set**: Start with 0.001. Much smaller than SGD!
  - **Range**: 0.0001 to 0.01 usually

- **`betas`**: Two numbers that control Adam's "memory" and "flexibility"
  - **beta1 (0.9)**: How much Adam remembers previous steps (like momentum)
    - **Think**: How long the optimizer "remembers" where it was going
    - **Lower (like 0.8)**: Forgets quickly, changes direction fast (good if stuck)
    - **Higher (like 0.95)**: Remembers longer, moves smoother (good for stable learning)
  - **beta2 (0.999)**: How quickly Adam adjusts to new information
    - **Think**: How fast it learns from mistakes
    - **Lower (like 0.99)**: Learns fast, adapts quickly to changes
    - **Higher (like 0.9999)**: Learns slow, more careful
  - **For beginners**: Just use (0.9, 0.999). Change only if training is really bad.

- **`eps`**: Small number to prevent division by zero
  - **How to set**: Default 1e-8 is fine. Only change for numerical issues.

- **`weight_decay`**: L2 regularization
  - **How to set**: Same as SGD (1e-4 to 1e-3)

- **`amsgrad`**: Improved version of Adam
  - **How to set**: False (default). True for some problems.

### When to use Adam:
- **Most problems**: Default choice for beginners
- **Complex networks**: CNNs, RNNs, Transformers
- **When you don't know**: Just use Adam!
- **Don't use for**: Very simple problems (SGD might be enough)

### Example settings:
```python
# Default Adam (best for beginners)
optim.Adam(model.parameters(), lr=0.001)

# With regularization
optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)

# Smaller learning rate for fine-tuning
optim.Adam(model.parameters(), lr=0.0001)
```

---

## ⚡ RMSprop (Root Mean Square Propagation) — The Middle Ground

### What it does:
Similar to Adam but simpler. Adapts learning rate based on recent gradients.

### Parameters you can tune:

```python
optimizer = optim.RMSprop(model.parameters(), lr=0.001, alpha=0.99, eps=1e-8, weight_decay=0, momentum=0, centered=False)
```

- **`lr` (learning rate)**: Step size
  - **How to set**: 0.001 (same as Adam)

- **`alpha`**: Smoothing factor for gradient history
  - **How to set**: 0.99 (default good). Higher = more smoothing.

- **`eps`**: Prevents division by zero
  - **How to set**: Default 1e-8 fine

- **`weight_decay`**: L2 regularization
  - **How to set**: Same as others

- **`momentum`**: Adds momentum (like SGD)
  - **How to set**: 0 (default) or 0.9

- **`centered`**: Uses centered RMS (better but slower)

### When to use RMSprop:
- **RNNs/LSTMs**: Often better than Adam for sequences
- **When Adam oscillates**: More stable for some problems
- **Online learning**: Adapts well to changing data

### Example settings:
```python
# Default RMSprop
optim.RMSprop(model.parameters(), lr=0.001)

# With momentum
optim.RMSprop(model.parameters(), lr=0.001, momentum=0.9)
```

---

## 📋 Other Optimizers (Less Common)

### Adagrad:
- **What**: Adapts learning rate, but can stop learning too early
- **When**: Rarely used. Good for sparse data.
- **Parameters**: lr=0.01, lr_decay=0, weight_decay=0, eps=1e-10

### Adadelta:
- **What**: Improved Adagrad, doesn't need learning rate
- **When**: When you don't want to tune learning rate
- **Parameters**: lr=1.0 (default), rho=0.9, eps=1e-6, weight_decay=0

### AdamW:
- **What**: Adam with better weight decay
- **When**: If using weight decay with Adam
- **Parameters**: Same as Adam

---

## 🆚 Optimizer Comparison Table

| Optimizer | Speed | Stability | Tuning Needed | Best For |
|-----------|-------|-----------|---------------|----------|
| **SGD** | Slow | Very Stable | High | Simple problems |
| **Adam** | Fast | Stable | Low | Most problems |
| **RMSprop** | Medium | Very Stable | Medium | RNNs, sequences |

---

## 🎯 How to Choose an Optimizer

### For Beginners:
1. **Try Adam first** - It works for almost everything
2. **If slow**: Switch to SGD
3. **If unstable**: Try RMSprop

### By Problem Type:
- **Classification**: Adam or SGD
- **Regression**: Adam or SGD
- **Sequences (RNN)**: RMSprop or Adam
- **Images (CNN)**: Adam
- **Simple math**: SGD

### By Dataset Size:
- **Small dataset**: Adam (learns fast)
- **Large dataset**: SGD (more stable)

---

## ⚙️ Learning Rate Scheduling

Sometimes you want the learning rate to change during training:

```python
from torch.optim import lr_scheduler

# After optimizer creation:
scheduler = lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
# Reduces LR by 10x every 10 epochs

# In training loop:
scheduler.step()  # Call after optimizer.step()
```

- **StepLR**: Reduces LR every N epochs
- **ExponentialLR**: Multiplies LR by gamma each epoch
- **CosineAnnealingLR**: Smoothly decreases LR following cosine curve

---

## 🚨 Common Mistakes

1. **Wrong learning rate scale**: Adam uses 0.001, SGD uses 0.01
2. **Forgetting momentum**: Always add momentum=0.9 to SGD
3. **Using Adam everywhere**: Sometimes SGD is better for simple problems
4. **Not trying different optimizers**: Experiment!
5. **Ignoring weight_decay**: Add it if overfitting

---

## 💡 Pro Tips

- **Start with defaults**: Don't over-tune at first
- **Monitor loss**: If loss explodes, learning rate too high
- **Use validation**: Check performance on unseen data
- **Adam is safe**: Use it if unsure
- **SGD for control**: Use when you want precise tuning
- **Experiment**: Try 2-3 optimizers per problem

---

Remember: The optimizer is like choosing a car:
- **SGD**: Reliable family car (slow but steady)
- **Adam**: Sports car (fast and smart)
- **RMSprop**: SUV (good in rough terrain)

Pick based on your "road conditions" (problem type)! 

---</content>
<parameter name="filePath">/mnt/Data/3-2/330 (ML lab)/Online 2/cheatsheets/optimizer_guide.md