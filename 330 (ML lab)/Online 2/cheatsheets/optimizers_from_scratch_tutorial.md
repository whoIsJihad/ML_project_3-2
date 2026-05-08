---

# ⚡ Implementing Adam and SGD from Scratch in PyTorch

This tutorial shows **detailed implementations** of SGD and Adam optimizers. Understand the math and code behind these algorithms!

---

## 📚 SGD (Stochastic Gradient Descent) — The Foundation

SGD updates parameters using only the current batch's gradient.

### **Math Behind SGD:**
```
θ = θ - η * ∇L(θ)
```
Where:
- θ = parameters (weights/biases)
- η = learning rate
- ∇L(θ) = gradient of loss w.r.t. parameters

### **SGD Implementation:**

```python
import torch
import torch.nn as nn

class SGD:
    def __init__(self, parameters, lr=0.01, weight_decay=0.0):
        """
        Args:
            parameters: Model parameters (from model.parameters())
            lr: Learning rate
            weight_decay: L2 regularization (like torch.optim.SGD weight_decay)
        """
        self.parameters = list(parameters)
        self.lr = lr
        self.weight_decay = weight_decay
        
        # Initialize velocity (momentum) if needed
        self.velocity = [torch.zeros_like(p) for p in self.parameters]
    
    def zero_grad(self):
        """Clear gradients for all parameters"""
        for p in self.parameters:
            if p.grad is not None:
                p.grad.zero_()
    
    def step(self):
        """Update parameters using SGD"""
        with torch.no_grad():
            for i, param in enumerate(self.parameters):
                if param.grad is None:
                    continue
                
                # L2 regularization (weight decay)
                if self.weight_decay != 0:
                    param.grad.add_(param, alpha=self.weight_decay)
                
                # SGD update: param = param - lr * grad
                param.sub_(param.grad, alpha=self.lr)

# ================================
# USAGE EXAMPLE
# ================================

# Simple model
model = nn.Linear(10, 1)
optimizer = SGD(model.parameters(), lr=0.01, weight_decay=0.0001)

# Dummy data
x = torch.randn(32, 10)
y = torch.randn(32, 1)

# Training step
for epoch in range(5):
    # Forward pass
    pred = model(x)
    loss = nn.MSELoss()(pred, y)
    
    # Backward pass
    optimizer.zero_grad()
    loss.backward()
    
    # Update parameters
    optimizer.step()
    
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
```

---

## 🚀 SGD with Momentum

Momentum helps SGD escape local minima and speeds up convergence.

### **Math Behind Momentum:**
```
v = β * v + (1-β) * ∇L(θ)
θ = θ - η * v
```
Where:
- v = velocity (accumulated gradient)
- β = momentum coefficient (usually 0.9)

### **Momentum SGD Implementation:**

```python
class SGDMomentum:
    def __init__(self, parameters, lr=0.01, momentum=0.9, weight_decay=0.0):
        self.parameters = list(parameters)
        self.lr = lr
        self.momentum = momentum
        self.weight_decay = weight_decay
        
        # Initialize velocity for each parameter
        self.velocity = [torch.zeros_like(p) for p in self.parameters]
    
    def zero_grad(self):
        for p in self.parameters:
            if p.grad is not None:
                p.grad.zero_()
    
    def step(self):
        with torch.no_grad():
            for i, param in enumerate(self.parameters):
                if param.grad is None:
                    continue
                
                # L2 regularization
                if self.weight_decay != 0:
                    param.grad.add_(param, alpha=self.weight_decay)
                
                # Update velocity: v = momentum * v + (1-momentum) * grad
                self.velocity[i].mul_(self.momentum).add_(param.grad, alpha=1-self.momentum)
                
                # Update parameter: param = param - lr * v
                param.sub_(self.velocity[i], alpha=self.lr)

# ================================
# COMPARISON: SGD vs SGD-Momentum
# ================================

# Without momentum
optimizer_sgd = SGD(model.parameters(), lr=0.01)

# With momentum
optimizer_momentum = SGDMomentum(model.parameters(), lr=0.01, momentum=0.9)

# Momentum helps in:
# 1. Faster convergence in flat areas
# 2. Escape local minima
# 3. Reduce oscillations
```

---

## 🎯 Adam (Adaptive Moment Estimation) — The King

Adam combines momentum + adaptive learning rates. Most popular optimizer!

### **Math Behind Adam:**
```
# First moment (mean of gradients):
m_t = β1 * m_{t-1} + (1-β1) * ∇L(θ_t)

# Second moment (variance of gradients):
v_t = β2 * v_{t-1} + (1-β2) * (∇L(θ_t))²

# Bias correction:
m̂_t = m_t / (1 - β1^t)
v̂_t = v_t / (1 - β2^t)

# Parameter update:
θ_{t+1} = θ_t - η * m̂_t / (√v̂_t + ε)
```

Where:
- m_t = first moment (momentum)
- v_t = second moment (adaptive learning rate)
- β1 = 0.9 (first moment decay)
- β2 = 0.999 (second moment decay)
- ε = 1e-8 (numerical stability)

### **Adam Implementation:**

```python
class Adam:
    def __init__(self, parameters, lr=0.001, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0):
        """
        Args:
            parameters: Model parameters
            lr: Learning rate (default: 0.001)
            betas: (β1, β2) coefficients for moments
            eps: Small constant for numerical stability
            weight_decay: L2 regularization
        """
        self.parameters = list(parameters)
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.weight_decay = weight_decay
        
        # Initialize first moment (m) and second moment (v)
        self.m = [torch.zeros_like(p) for p in self.parameters]
        self.v = [torch.zeros_like(p) for p in self.parameters]
        
        # Time step (for bias correction)
        self.t = 0
    
    def zero_grad(self):
        for p in self.parameters:
            if p.grad is not None:
                p.grad.zero_()
    
    def step(self):
        self.t += 1  # Increment time step
        
        with torch.no_grad():
            for i, param in enumerate(self.parameters):
                if param.grad is None:
                    continue
                
                grad = param.grad
                
                # L2 regularization
                if self.weight_decay != 0:
                    grad = grad.add(param, alpha=self.weight_decay)
                
                # Update first moment: m = β1*m + (1-β1)*grad
                self.m[i].mul_(self.beta1).add_(grad, alpha=1-self.beta1)
                
                # Update second moment: v = β2*v + (1-β2)*grad²
                self.v[i].mul_(self.beta2).addcmul_(grad, grad, value=1-self.beta2)
                
                # Bias correction
                m_hat = self.m[i] / (1 - self.beta1 ** self.t)
                v_hat = self.v[i] / (1 - self.beta2 ** self.t)
                
                # Parameter update: θ = θ - lr * m̂ / (√v̂ + ε)
                param.sub_(self.lr * m_hat / (torch.sqrt(v_hat) + self.eps))

# ================================
# ADAM USAGE EXAMPLE
# ================================

# Create model
model = nn.Sequential(
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Linear(128, 10)
)

# Our custom Adam
optimizer = Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999))

# Dummy MNIST-like data
x = torch.randn(64, 784)
y = torch.randint(0, 10, (64,))

# Training loop
criterion = nn.CrossEntropyLoss()

for epoch in range(10):
    # Forward
    outputs = model(x)
    loss = criterion(outputs, y)
    
    # Backward
    optimizer.zero_grad()
    loss.backward()
    
    # Update
    optimizer.step()
    
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
```

---

## 🔬 AdamW (Adam with Weight Decay Fix)

AdamW fixes L2 regularization in Adam. PyTorch's default!

### **The Problem with Adam + Weight Decay:**
Adam's adaptive learning rates interfere with weight decay, making it not true L2 regularization.

### **AdamW Fix:**
Apply weight decay BEFORE the adaptive update.

```python
class AdamW:
    def __init__(self, parameters, lr=0.001, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.01):
        self.parameters = list(parameters)
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.weight_decay = weight_decay
        
        self.m = [torch.zeros_like(p) for p in self.parameters]
        self.v = [torch.zeros_like(p) for p in self.parameters]
        self.t = 0
    
    def zero_grad(self):
        for p in self.parameters:
            if p.grad is not None:
                p.grad.zero_()
    
    def step(self):
        self.t += 1
        
        with torch.no_grad():
            for i, param in enumerate(self.parameters):
                if param.grad is None:
                    continue
                
                grad = param.grad
                
                # Weight decay BEFORE adaptive update (AdamW fix)
                if self.weight_decay != 0:
                    param.mul_(1 - self.lr * self.weight_decay)
                
                # Update moments
                self.m[i].mul_(self.beta1).add_(grad, alpha=1-self.beta1)
                self.v[i].mul_(self.beta2).addcmul_(grad, grad, value=1-self.beta2)
                
                # Bias correction
                m_hat = self.m[i] / (1 - self.beta1 ** self.t)
                v_hat = self.v[i] / (1 - self.beta2 ** self.t)
                
                # Update parameter
                param.sub_(self.lr * m_hat / (torch.sqrt(v_hat) + self.eps))

# ================================
# ADAMW VS ADAM COMPARISON
# ================================

# Adam (weight decay applied to gradient)
adam = Adam(model.parameters(), lr=0.001, weight_decay=0.01)

# AdamW (weight decay applied to parameter)
adamw = AdamW(model.parameters(), lr=0.001, weight_decay=0.01)

# AdamW is better for regularization!
```

---

## 🧪 Testing Our Optimizers

```python
import matplotlib.pyplot as plt

# ================================
# COMPARE OPTIMIZERS ON SIMPLE PROBLEM
# ================================

# Simple quadratic function: f(x) = x²
def quadratic(x):
    return x**2

def grad_quadratic(x):
    return 2*x

# Test different optimizers
optimizers = {
    'SGD': SGD([torch.tensor([5.0], requires_grad=True)], lr=0.1),
    'SGD_Momentum': SGDMomentum([torch.tensor([5.0], requires_grad=True)], lr=0.1, momentum=0.9),
    'Adam': Adam([torch.tensor([5.0], requires_grad=True)], lr=0.1)
}

# Track convergence
history = {name: [] for name in optimizers.keys()}

for name, opt in optimizers.items():
    x = torch.tensor([5.0], requires_grad=True)
    
    for step in range(50):
        # Compute gradient
        loss = quadratic(x)
        loss.backward()
        
        # Store current value
        history[name].append(x.item())
        
        # Update
        opt.step()
        opt.zero_grad()

# Plot convergence
plt.figure(figsize=(10, 6))
for name, values in history.items():
    plt.plot(values, label=name)

plt.xlabel('Step')
plt.ylabel('Parameter Value')
plt.title('Optimizer Convergence Comparison')
plt.legend()
plt.grid(True)
plt.show()
```

---

## 📊 Optimizer Comparison Table

| Optimizer | Pros | Cons | Best For |
|-----------|------|------|----------|
| **SGD** | Simple, memory efficient | Slow convergence, can get stuck | Simple problems, large datasets |
| **SGD + Momentum** | Faster convergence, escapes minima | Can overshoot | Most deep learning tasks |
| **Adam** | Adaptive LR, works well out-of-box | Can converge to suboptimal solutions | Complex models, sparse gradients |
| **AdamW** | Better regularization than Adam | Slightly more complex | Modern deep learning |

### **Hyperparameter Recommendations:**

```python
# SGD
optimizer = SGD(model.parameters(), lr=0.01, weight_decay=0.0001)

# SGD + Momentum  
optimizer = SGDMomentum(model.parameters(), lr=0.01, momentum=0.9, weight_decay=0.0001)

# Adam
optimizer = Adam(model.parameters(), lr=0.001, betas=(0.9, 0.999), weight_decay=0.01)

# AdamW (recommended for modern models)
optimizer = AdamW(model.parameters(), lr=0.001, betas=(0.9, 0.999), weight_decay=0.01)
```

---

## 🎯 Key Takeaways

1. **SGD**: Simple but slow. Add momentum for better performance.
2. **Adam**: Combines momentum + adaptive learning rates. Great default choice.
3. **AdamW**: Fixes Adam's weight decay. Use for modern deep learning.
4. **Implementation**: All optimizers follow the same pattern: zero_grad() → step().
5. **Math Matters**: Understanding the algorithms helps you tune hyperparameters better.

**Pro Tip**: Start with Adam (lr=0.001), then experiment with learning rates and weight decay!

---

Now you understand optimizers from the ground up! 🎉</content>
<parameter name="filePath">/mnt/Data/3-2/330 (ML lab)/Online 2/cheatsheets/optimizers_from_scratch_tutorial.md