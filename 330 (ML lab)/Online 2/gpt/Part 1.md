Good. Let’s lock in **Optimization Strategies (SGD vs Adam)** properly — not formula memorization, but **mechanics + intuition + exam usage**.

You already know gradient descent mathematically. We’ll focus on what changes in code and behavior.

---

# ⚙️ Optimization Engine — Mental Model

Think of optimizer as a **stateful machine attached to parameters**.

Each parameter tensor has:

```
value        (weights)
grad         (∂loss/∂value)
optimizer_state   (momentum, moving averages, etc.)
```

Every `step()`:

```
optimizer reads grad
optimizer updates internal state
optimizer mutates parameter value
```

That’s it.

---

# 🟢 SGD — What actually happens

### Vanilla SGD update:

```
w = w - lr * grad
```

That’s literally it.

No memory. No history.

Each step only sees current gradient.

---

### SGD with momentum (common):

Optimizer stores:

```
velocity v
```

Update:

```
v = momentum * v + grad
w = w - lr * v
```

Meaning:

- Gradients accumulate direction over time.
    
- Reduces zig-zag.
    
- Faster convergence.
    

In PyTorch:

```python
torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
```

---

### Properties of SGD

✅ Simple  
✅ Predictable  
❌ Sensitive to learning rate  
❌ Slow on noisy / sparse gradients  
❌ Can get stuck oscillating

Used when:

- You want stability
    
- You tune carefully
    
- Large datasets
    

---

---

# 🔵 Adam — What actually happens

Adam stores **two moving averages per parameter**:

```
m = moving average of gradients (momentum)
v = moving average of squared gradients (scale)
```

Update idea:

```
m ← smooth(grad)
v ← smooth(grad²)
w ← w - lr * m / sqrt(v + eps)
```

Interpretation:

- If gradient is consistently large → step size shrinks
    
- If gradient is small/noisy → step adapts
    
- Each parameter gets its own learning rate
    

Adam is **adaptive SGD + momentum combined**.

In PyTorch:

```python
torch.optim.Adam(model.parameters(), lr=0.001)
```

---

### Properties of Adam

✅ Fast convergence  
✅ Robust to bad scaling  
✅ Minimal tuning  
❌ Sometimes worse generalization  
❌ Can overfit

Used when:

- Prototyping
    
- Deep networks
    
- Messy data
    
- You want fast results
    

---

---

# 🧪 Exam-Level Understanding

You should instantly know:

---

### ✔️ What optimizer.step() uses

```
param.grad
optimizer internal buffers
learning rate
```

---

### ✔️ What zero_grad() does

Clears accumulated gradients:

```
param.grad = 0
```

Because backward accumulates.

---

---

### ✔️ How SGD vs Adam differ in code

Only optimizer line changes:

```python
optimizer = torch.optim.SGD(...)
optimizer = torch.optim.Adam(...)
```

Training loop stays identical.

---

---

### ✔️ What hyperparameters matter

SGD:

```
lr
momentum
```

Adam:

```
lr
betas (usually default)
eps (ignore in exam)
```

---

---

# ⚠️ Common exam traps

❌ Forgetting optimizer.zero_grad()  
→ gradients accumulate

❌ Using too large lr with SGD  
→ loss explodes

❌ Expecting Adam to behave like SGD  
→ wrong intuition

❌ Confusing loss.backward() vs optimizer.step()

Backward computes grads.  
Step applies them.

---

---

# 🧠 Quick sanity test (answer mentally)

1. Which optimizer stores more internal state: SGD or Adam?
    
2. If gradients are noisy and badly scaled, which optimizer is safer?
    
3. Does optimizer know about loss function?
    
4. Does optimizer modify tensors or graphs?
    

If these feel obvious → you’re ready.

---

---

# 👉 Next Phase: Neural Network Building (FNN)

We’ll cover:

✅ What Linear layer actually stores  
✅ How shapes flow  
✅ Where activations live  
✅ What forward really means in PyTorch

This will directly prepare you for code completion.

Say **go** when ready.