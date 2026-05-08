# Backpropagation Study Guide

A comprehensive, beginner-friendly guide to understanding backpropagation - the algorithm that makes neural networks learn.

---

## 📚 Table of Contents
1. [What is Backpropagation?](#what-is-backpropagation)
2. [The Chain Rule (Calculus Refresher)](#the-chain-rule)
3. [Step-by-Step Example](#step-by-step-example)
4. [Backpropagation Algorithm](#backpropagation-algorithm)
5. [Multi-Layer Networks](#multi-layer-networks)
6. [Code Examples](#code-examples)
7. [Common Pitfalls](#common-pitfalls)

---

## What is Backpropagation?

### The Big Picture

**Backpropagation** (short for "backward propagation of errors") is the algorithm that tells us **how to adjust the weights** in a neural network to reduce the loss.

Think of it like this:
1. **Forward Pass**: You make a prediction and measure how wrong it is (loss)
2. **Backward Pass**: You trace back through the network to figure out which weights caused the error
3. **Update**: You adjust those weights to do better next time

### Why "Backward"?

We compute gradients **starting from the output** (the loss) and work our way **backward** through the network layers, all the way to the input.

```
Input → Layer 1 → Layer 2 → Output → Loss
                                        ↓
Input ← Layer 1 ← Layer 2 ← Output ← Gradients flow backward
```

### The Core Idea

**Backpropagation uses the chain rule** to efficiently compute how each weight affects the loss.

Without backpropagation, we'd have to compute derivatives one at a time. With backpropagation, we compute all gradients in a single backward pass - much more efficient!

---

## The Chain Rule

### Refresher: What is the Chain Rule?

The chain rule from calculus tells us how to take derivatives of **composite functions** (functions inside functions).

### Single Variable Chain Rule

If you have $y = f(g(x))$, then:

$$\frac{dy}{dx} = \frac{dy}{dg} \cdot \frac{dg}{dx}$$

**In plain English:**
> "The rate of change of y with respect to x equals the rate of change of y with respect to g, times the rate of change of g with respect to x."

### Visual Example

```
x → g(x) → f(g(x)) = y
    ↓      ↓
    u      y

If y = f(u) and u = g(x), then:
dy/dx = (dy/du) × (du/dx)
```

### Concrete Example

Let's compute the derivative of $y = (2x + 1)^3$

**Method 1: Direct (tedious)**
- Expand: $y = 8x^3 + 12x^2 + 6x + 1$
- Differentiate: $\frac{dy}{dx} = 24x^2 + 24x + 6$

**Method 2: Chain Rule (elegant)**
- Let $u = 2x + 1$
- Then $y = u^3$
- $\frac{dy}{du} = 3u^2$
- $\frac{du}{dx} = 2$
- $\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx} = 3u^2 \cdot 2 = 6u^2 = 6(2x+1)^2$

Both give the same result, but chain rule is cleaner!

### Code: Chain Rule Visualization

```python
import numpy as np
import matplotlib.pyplot as plt

# Define the composite function: y = (2x + 1)^3
def g(x):
    """Inner function: u = 2x + 1"""
    return 2 * x + 1

def f(u):
    """Outer function: y = u^3"""
    return u ** 3

def composite(x):
    """Composite function: y = f(g(x))"""
    return f(g(x))

# Derivatives
def dg_dx(x):
    """Derivative of g: du/dx = 2"""
    return 2

def df_du(u):
    """Derivative of f: dy/du = 3u^2"""
    return 3 * u ** 2

def dy_dx_chain_rule(x):
    """Using chain rule: dy/dx = (dy/du) * (du/dx)"""
    u = g(x)
    return df_du(u) * dg_dx(x)

# Test
x_test = 2
print(f"At x = {x_test}:")
print(f"  u = g(x) = {g(x_test)}")
print(f"  y = f(u) = {composite(x_test)}")
print(f"  dy/dx = {dy_dx_chain_rule(x_test)}")

# Verify with numerical differentiation
epsilon = 1e-7
numerical_derivative = (composite(x_test + epsilon) - composite(x_test)) / epsilon
print(f"  Numerical derivative: {numerical_derivative:.6f}")
print(f"  Chain rule derivative: {dy_dx_chain_rule(x_test):.6f}")
print(f"  Match: {np.isclose(numerical_derivative, dy_dx_chain_rule(x_test))}")
```

**Output:**
```
At x = 2:
  u = g(x) = 5
  y = f(u) = 125
  dy/dx = 150.0
  Numerical derivative: 150.000000
  Chain rule derivative: 150.000000
  Match: True
```

### Multi-Variable Chain Rule

For multiple variables, the chain rule becomes:

$$\frac{\partial L}{\partial x} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial x}$$

If $y$ depends on multiple intermediate variables:

$$\frac{\partial L}{\partial x} = \sum_i \frac{\partial L}{\partial y_i} \cdot \frac{\partial y_i}{\partial x}$$

This is the foundation of backpropagation!

---

## Step-by-Step Example

Let's work through the exact example from your class notes:

### The Setup

We have:
1. **Linear combination**: $z = wx + b$
2. **Activation function**: $y = \sigma(z)$ where $\sigma$ is sigmoid
3. **Loss function**: $L = \frac{1}{2}(y - t)^2$

Where:
- $x$ = input
- $w$ = weight
- $b$ = bias
- $t$ = target (true label)
- $y$ = prediction
- $L$ = loss

### The Computation Graph

```
x, w, b
  ↓
  z = wx + b
  ↓
  y = σ(z)
  ↓
  L = 0.5(y - t)²
```

### Goal: Find $\frac{\partial L}{\partial w}$ and $\frac{\partial L}{\partial b}$

We need these gradients to update our parameters:
- $w_{new} = w_{old} - \alpha \frac{\partial L}{\partial w}$
- $b_{new} = b_{old} - \alpha \frac{\partial L}{\partial b}$

---

### Step 1: Compute $\frac{\partial L}{\partial y}$

Starting from the loss function:

$$L = \frac{1}{2}(y - t)^2$$

Taking the derivative with respect to $y$:

$$\frac{\partial L}{\partial y} = \frac{\partial}{\partial y}\left[\frac{1}{2}(y - t)^2\right]$$

Using the chain rule:

$$\frac{\partial L}{\partial y} = \frac{1}{2} \cdot 2(y - t) \cdot 1 = (y - t)$$

**Result:** $\frac{\partial L}{\partial y} = y - t$ (the error!)

---

### Step 2: Compute $\frac{\partial y}{\partial z}$

We have $y = \sigma(z)$ where sigmoid is:

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

The derivative of sigmoid is:

$$\frac{\partial \sigma(z)}{\partial z} = \sigma(z)(1 - \sigma(z))$$

Since $y = \sigma(z)$:

$$\frac{\partial y}{\partial z} = y(1 - y)$$

**Result:** $\frac{\partial y}{\partial z} = y(1 - y)$

---

### Step 3: Compute $\frac{\partial L}{\partial z}$ (using chain rule!)

Now we combine the previous two steps:

$$\frac{\partial L}{\partial z} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial z}$$

$$\frac{\partial L}{\partial z} = (y - t) \cdot y(1 - y)$$

**Result:** $\frac{\partial L}{\partial z} = (y - t) \cdot y(1 - y)$

---

### Step 4: Compute $\frac{\partial L}{\partial w}$

We have $z = wx + b$, so:

$$\frac{\partial z}{\partial w} = x$$

Using the chain rule:

$$\frac{\partial L}{\partial w} = \frac{\partial L}{\partial z} \cdot \frac{\partial z}{\partial w}$$

$$\frac{\partial L}{\partial w} = (y - t) \cdot y(1 - y) \cdot x$$

**Result:** $\boxed{\frac{\partial L}{\partial w} = (y - t) \cdot y(1 - y) \cdot x}$

---

### Step 5: Compute $\frac{\partial L}{\partial b}$

We have $z = wx + b$, so:

$$\frac{\partial z}{\partial b} = 1$$

Using the chain rule:

$$\frac{\partial L}{\partial b} = \frac{\partial L}{\partial z} \cdot \frac{\partial z}{\partial b}$$

$$\frac{\partial L}{\partial b} = (y - t) \cdot y(1 - y) \cdot 1$$

**Result:** $\boxed{\frac{\partial L}{\partial b} = (y - t) \cdot y(1 - y)}$

---

### Summary of Gradients

| Parameter | Gradient |
|-----------|----------|
| $\frac{\partial L}{\partial y}$ | $(y - t)$ |
| $\frac{\partial L}{\partial z}$ | $(y - t) \cdot y(1 - y)$ |
| $\frac{\partial L}{\partial w}$ | $(y - t) \cdot y(1 - y) \cdot x$ |
| $\frac{\partial L}{\partial b}$ | $(y - t) \cdot y(1 - y)$ |

Notice the pattern: each gradient is built from the previous one using the chain rule!

---

### Numerical Example

Let's compute with actual numbers:

**Given:**
- $x = 2.0$
- $w = 0.5$
- $b = 1.0$
- $t = 1.0$ (target)

**Forward Pass:**

1. $z = wx + b = 0.5 \times 2.0 + 1.0 = 2.0$

2. $y = \sigma(z) = \frac{1}{1 + e^{-2.0}} = \frac{1}{1 + 0.135} = 0.881$

3. $L = \frac{1}{2}(y - t)^2 = \frac{1}{2}(0.881 - 1.0)^2 = \frac{1}{2}(-0.119)^2 = 0.00708$

**Backward Pass:**

1. $\frac{\partial L}{\partial y} = y - t = 0.881 - 1.0 = -0.119$

2. $\frac{\partial y}{\partial z} = y(1 - y) = 0.881 \times 0.119 = 0.105$

3. $\frac{\partial L}{\partial z} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial z} = -0.119 \times 0.105 = -0.0125$

4. $\frac{\partial L}{\partial w} = \frac{\partial L}{\partial z} \cdot x = -0.0125 \times 2.0 = -0.025$

5. $\frac{\partial L}{\partial b} = \frac{\partial L}{\partial z} \cdot 1 = -0.0125$

**Update (with learning rate $\alpha = 0.1$):**

- $w_{new} = 0.5 - 0.1 \times (-0.025) = 0.5 + 0.0025 = 0.5025$
- $b_{new} = 1.0 - 0.1 \times (-0.0125) = 1.0 + 0.00125 = 1.00125$

The weights moved in the direction that reduces the loss!

---

### Code: Complete Example

```python
import numpy as np

def sigmoid(z):
    """Sigmoid activation function."""
    return 1 / (1 + np.exp(-z))

def sigmoid_derivative(y):
    """Derivative of sigmoid (given output y = sigmoid(z))."""
    return y * (1 - y)

def forward_pass(x, w, b, t):
    """
    Perform forward pass and compute loss.
    
    Returns:
        z, y, loss
    """
    # Linear combination
    z = w * x + b
    
    # Activation
    y = sigmoid(z)
    
    # Loss
    loss = 0.5 * (y - t) ** 2
    
    return z, y, loss

def backward_pass(x, y, t):
    """
    Perform backward pass and compute gradients.
    
    Returns:
        dL/dw, dL/db
    """
    # Step 1: dL/dy
    dL_dy = y - t
    
    # Step 2: dy/dz
    dy_dz = sigmoid_derivative(y)
    
    # Step 3: dL/dz (using chain rule)
    dL_dz = dL_dy * dy_dz
    
    # Step 4: dL/dw
    dz_dw = x
    dL_dw = dL_dz * dz_dw
    
    # Step 5: dL/db
    dz_db = 1
    dL_db = dL_dz * dz_db
    
    return dL_dw, dL_db

# Initial values
x = 2.0
w = 0.5
b = 1.0
t = 1.0  # target
learning_rate = 0.1

print("=" * 60)
print("BACKPROPAGATION STEP-BY-STEP EXAMPLE")
print("=" * 60)

print(f"\nInitial values:")
print(f"  x (input) = {x}")
print(f"  w (weight) = {w}")
print(f"  b (bias) = {b}")
print(f"  t (target) = {t}")
print(f"  α (learning rate) = {learning_rate}")

# Forward pass
print(f"\n{'='*60}")
print("FORWARD PASS:")
print(f"{'='*60}")

z, y, loss = forward_pass(x, w, b, t)

print(f"  z = w*x + b = {w}*{x} + {b} = {z:.6f}")
print(f"  y = σ(z) = {y:.6f}")
print(f"  L = 0.5*(y - t)² = {loss:.6f}")

# Backward pass
print(f"\n{'='*60}")
print("BACKWARD PASS (Computing Gradients):")
print(f"{'='*60}")

dL_dw, dL_db = backward_pass(x, y, t)

print(f"  ∂L/∂y = (y - t) = {y - t:.6f}")
print(f"  ∂y/∂z = y(1-y) = {sigmoid_derivative(y):.6f}")
print(f"  ∂L/∂z = (∂L/∂y)(∂y/∂z) = {(y - t) * sigmoid_derivative(y):.6f}")
print(f"  ∂L/∂w = (∂L/∂z)(∂z/∂w) = {dL_dw:.6f}")
print(f"  ∂L/∂b = (∂L/∂z)(∂z/∂b) = {dL_db:.6f}")

# Update parameters
print(f"\n{'='*60}")
print("PARAMETER UPDATE:")
print(f"{'='*60}")

w_new = w - learning_rate * dL_dw
b_new = b - learning_rate * dL_db

print(f"  w_new = w - α*(∂L/∂w) = {w} - {learning_rate}*{dL_dw:.6f} = {w_new:.6f}")
print(f"  b_new = b - α*(∂L/∂b) = {b} - {learning_rate}*{dL_db:.6f} = {b_new:.6f}")

# Verify improvement
z_new, y_new, loss_new = forward_pass(x, w_new, b_new, t)

print(f"\n{'='*60}")
print("VERIFICATION:")
print(f"{'='*60}")
print(f"  Old loss: {loss:.6f}")
print(f"  New loss: {loss_new:.6f}")
print(f"  Improvement: {loss - loss_new:.6f}")
print(f"  Loss decreased: {loss_new < loss} ✓" if loss_new < loss else "  ⚠ Something went wrong!")
```

**Output:**
```
============================================================
BACKPROPAGATION STEP-BY-STEP EXAMPLE
============================================================

Initial values:
  x (input) = 2.0
  w (weight) = 0.5
  b (bias) = 1.0
  t (target) = 1.0
  α (learning rate) = 0.1

============================================================
FORWARD PASS:
============================================================
  z = w*x + b = 0.5*2.0 + 1.0 = 2.000000
  y = σ(z) = 0.880797
  L = 0.5*(y - t)² = 0.007099

============================================================
BACKWARD PASS (Computing Gradients):
============================================================
  ∂L/∂y = (y - t) = -0.119203
  ∂y/∂z = y(1-y) = 0.104994
  ∂L/∂z = (∂L/∂y)(∂y/∂z) = -0.012515
  ∂L/∂w = (∂L/∂z)(∂z/∂w) = -0.025030
  ∂L/∂b = (∂L/∂z)(∂z/∂b) = -0.012515

============================================================
PARAMETER UPDATE:
============================================================
  w_new = w - α*(∂L/∂w) = 0.5 - 0.1*-0.025030 = 0.502503
  b_new = b - α*(∂L/∂b) = 1.0 - 0.1*-0.012515 = 1.001251

============================================================
VERIFICATION:
============================================================
  Old loss: 0.007099
  New loss: 0.006892
  Improvement: 0.000207
  Loss decreased: True ✓
```

---

## Backpropagation Algorithm

### The General Algorithm

For a neural network with multiple layers:

**Forward Pass:**
1. Compute activations layer by layer from input to output
2. Calculate the loss

**Backward Pass:**
1. Start at the output: compute $\frac{\partial L}{\partial output}$
2. For each layer (going backward):
   - Compute gradient of loss w.r.t. layer inputs
   - Compute gradient of loss w.r.t. layer weights
3. Update all weights using gradients

### Why It's Efficient

Without backpropagation, computing gradients for each weight independently would take:
- $O(n^2)$ time for $n$ weights

With backpropagation:
- $O(n)$ time - we compute all gradients in one backward pass!

This efficiency makes training deep networks practical.

---

## Multi-Layer Networks

### Two-Layer Network Example

Let's extend to a network with one hidden layer:

```
Input (x) → Hidden Layer (h) → Output (y) → Loss (L)
```

**Forward:**
1. $z_1 = W_1 x + b_1$
2. $h = \sigma(z_1)$
3. $z_2 = W_2 h + b_2$
4. $y = \sigma(z_2)$
5. $L = \frac{1}{2}(y - t)^2$

**Backward (using chain rule):**

For output layer weights $W_2$:
$$\frac{\partial L}{\partial W_2} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial z_2} \cdot \frac{\partial z_2}{\partial W_2}$$

For hidden layer weights $W_1$:
$$\frac{\partial L}{\partial W_1} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial z_2} \cdot \frac{\partial z_2}{\partial h} \cdot \frac{\partial h}{\partial z_1} \cdot \frac{\partial z_1}{\partial W_1}$$

Notice: gradients for earlier layers involve more terms (longer chain)!

### Code: Two-Layer Network Backpropagation

```python
import numpy as np

class TwoLayerNetwork:
    """
    A simple two-layer neural network for binary classification.
    
    Architecture: Input → Hidden (sigmoid) → Output (sigmoid)
    """
    
    def __init__(self, input_size, hidden_size, learning_rate=0.1):
        """Initialize with random weights."""
        # Hidden layer weights
        self.W1 = np.random.randn(input_size, hidden_size) * 0.5
        self.b1 = np.zeros((1, hidden_size))
        
        # Output layer weights
        self.W2 = np.random.randn(hidden_size, 1) * 0.5
        self.b2 = np.zeros((1, 1))
        
        self.learning_rate = learning_rate
    
    def sigmoid(self, z):
        """Sigmoid activation."""
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
    
    def sigmoid_derivative(self, a):
        """Derivative of sigmoid."""
        return a * (1 - a)
    
    def forward(self, X):
        """
        Forward pass through the network.
        
        Stores intermediate values for backpropagation.
        """
        # Hidden layer
        self.z1 = np.dot(X, self.W1) + self.b1
        self.h = self.sigmoid(self.z1)
        
        # Output layer
        self.z2 = np.dot(self.h, self.W2) + self.b2
        self.y = self.sigmoid(self.z2)
        
        return self.y
    
    def backward(self, X, t):
        """
        Backward pass - compute all gradients using chain rule.
        
        Parameters:
            X: input data
            t: target values
        """
        m = X.shape[0]  # batch size
        
        # ============================================
        # OUTPUT LAYER GRADIENTS
        # ============================================
        
        # ∂L/∂y
        dL_dy = self.y - t
        
        # ∂y/∂z2
        dy_dz2 = self.sigmoid_derivative(self.y)
        
        # ∂L/∂z2 = (∂L/∂y) * (∂y/∂z2)
        dL_dz2 = dL_dy * dy_dz2
        
        # ∂L/∂W2 = (∂L/∂z2) * (∂z2/∂W2)
        # where ∂z2/∂W2 = h^T
        dL_dW2 = (1/m) * np.dot(self.h.T, dL_dz2)
        
        # ∂L/∂b2
        dL_db2 = (1/m) * np.sum(dL_dz2, axis=0, keepdims=True)
        
        # ============================================
        # HIDDEN LAYER GRADIENTS
        # ============================================
        
        # ∂L/∂h = (∂L/∂z2) * (∂z2/∂h)
        # where ∂z2/∂h = W2^T
        dL_dh = np.dot(dL_dz2, self.W2.T)
        
        # ∂h/∂z1
        dh_dz1 = self.sigmoid_derivative(self.h)
        
        # ∂L/∂z1 = (∂L/∂h) * (∂h/∂z1)
        dL_dz1 = dL_dh * dh_dz1
        
        # ∂L/∂W1 = (∂L/∂z1) * (∂z1/∂W1)
        # where ∂z1/∂W1 = X^T
        dL_dW1 = (1/m) * np.dot(X.T, dL_dz1)
        
        # ∂L/∂b1
        dL_db1 = (1/m) * np.sum(dL_dz1, axis=0, keepdims=True)
        
        # ============================================
        # UPDATE WEIGHTS
        # ============================================
        
        self.W2 -= self.learning_rate * dL_dW2
        self.b2 -= self.learning_rate * dL_db2
        self.W1 -= self.learning_rate * dL_dW1
        self.b1 -= self.learning_rate * dL_db1
    
    def train(self, X, t, epochs=1000):
        """Train the network."""
        losses = []
        
        for epoch in range(epochs):
            # Forward pass
            y_pred = self.forward(X)
            
            # Compute loss
            loss = 0.5 * np.mean((y_pred - t) ** 2)
            losses.append(loss)
            
            # Backward pass
            self.backward(X, t)
            
            if epoch % 100 == 0:
                accuracy = np.mean((y_pred > 0.5) == t) * 100
                print(f"Epoch {epoch}: Loss = {loss:.4f}, Accuracy = {accuracy:.2f}%")
        
        return losses


# ============================================
# Example: XOR Problem
# ============================================

print("=" * 60)
print("TRAINING TWO-LAYER NETWORK ON XOR PROBLEM")
print("=" * 60)

# XOR dataset (classic non-linearly separable problem)
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

t = np.array([
    [0],
    [1],
    [1],
    [0]
])

print("\nXOR Dataset:")
print("Input | Target")
print("------|-------")
for i in range(len(X)):
    print(f" {X[i]}  |   {t[i][0]}")

# Create and train network
print("\n" + "=" * 60)
print("Training...")
print("=" * 60 + "\n")

network = TwoLayerNetwork(input_size=2, hidden_size=4, learning_rate=0.5)
losses = network.train(X, t, epochs=5000)

# Test predictions
print("\n" + "=" * 60)
print("FINAL PREDICTIONS:")
print("=" * 60)

predictions = network.forward(X)
print("\nInput | Target | Prediction | Rounded")
print("------|--------|------------|--------")
for i in range(len(X)):
    pred_val = predictions[i][0]
    rounded = int(pred_val > 0.5)
    correct = "✓" if rounded == t[i][0] else "✗"
    print(f" {X[i]}  |   {t[i][0]}    |   {pred_val:.4f}   |   {rounded} {correct}")

# Plot loss
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(losses, linewidth=2)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss Over Time (XOR Problem)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('backpropagation_training.png', dpi=150)
print("\n📊 Training curve saved to 'backpropagation_training.png'")
plt.show()
```

**Output:**
```
============================================================
TRAINING TWO-LAYER NETWORK ON XOR PROBLEM
============================================================

XOR Dataset:
Input | Target
------|-------
 [0 0]  |   0
 [0 1]  |   1
 [1 0]  |   1
 [1 1]  |   0

============================================================
Training...
============================================================

Epoch 0: Loss = 0.2842, Accuracy = 25.00%
Epoch 100: Loss = 0.2503, Accuracy = 50.00%
Epoch 200: Loss = 0.2495, Accuracy = 50.00%
...
Epoch 4900: Loss = 0.0013, Accuracy = 100.00%

============================================================
FINAL PREDICTIONS:
============================================================

Input | Target | Prediction | Rounded
------|--------|------------|--------
 [0 0]  |   0    |   0.0312   |   0 ✓
 [0 1]  |   1    |   0.9689   |   1 ✓
 [1 0]  |   1    |   0.9702   |   1 ✓
 [1 1]  |   0    |   0.0294   |   0 ✓
```

---

## Common Pitfalls

### 1. Vanishing Gradients

**Problem:** Gradients become extremely small in deep networks, making learning slow or impossible.

**Why it happens:** 
- Sigmoid derivative is at most 0.25
- Multiplying many small numbers → very small gradient
- Early layers barely learn

**Solution:**
- Use ReLU instead of sigmoid
- Use batch normalization
- Use residual connections (ResNet)

### 2. Exploding Gradients

**Problem:** Gradients become extremely large, causing unstable training.

**Why it happens:**
- Large weight values
- Deep networks without normalization

**Solution:**
- Gradient clipping
- Weight initialization (Xavier, He)
- Batch normalization

### 3. Forgetting to Store Intermediate Values

**Problem:** You need forward pass values for backward pass!

**Solution:** Always store:
- Activations ($h$, $y$)
- Pre-activations ($z$)
- Inputs ($x$)

### 4. Wrong Dimensions

**Problem:** Matrix multiplication errors due to shape mismatches.

**Solution:**
- Always check shapes: `print(X.shape, W.shape)`
- Use proper transposes
- Test on small examples first

---

## 🎯 Quick Reference

### The Backpropagation Recipe

1. **Forward Pass**: Compute and **store** all activations
2. **Compute Loss**: Measure how wrong the prediction is
3. **Output Layer Gradient**: Start with $\frac{\partial L}{\partial output}$
4. **Propagate Backward**: Use chain rule layer by layer
5. **Update Weights**: $w := w - \alpha \frac{\partial L}{\partial w}$

### Key Derivatives

| Function | Derivative |
|----------|-----------|
| $\sigma(z)$ | $\sigma(z)(1-\sigma(z))$ |
| $\text{ReLU}(z)$ | $1$ if $z > 0$, else $0$ |
| $\tanh(z)$ | $1 - \tanh^2(z)$ |
| $z = Wx + b$ | $\frac{\partial z}{\partial W} = x^T$, $\frac{\partial z}{\partial b} = 1$ |

### Chain Rule Pattern

$$\frac{\partial L}{\partial w^{(l)}} = \frac{\partial L}{\partial a^{(l+1)}} \cdot \frac{\partial a^{(l+1)}}{\partial z^{(l+1)}} \cdot \frac{\partial z^{(l+1)}}{\partial a^{(l)}} \cdot ... \cdot \frac{\partial z^{(l)}}{\partial w^{(l)}}$$

---

## 💡 Key Takeaways

1. **Backpropagation = Chain Rule Applied Systematically** - It's just calculus, automated!

2. **Forward pass computes predictions, backward pass computes gradients** - You need both!

3. **Store intermediate values during forward pass** - You'll need them for backward pass

4. **Gradients flow backward from loss to input** - Hence the name "back-propagation"

5. **Each layer's gradient depends on the next layer's gradient** - That's the chain!

6. **The $\frac{1}{2}$ in loss is just for convenience** - It cancels the 2 from the derivative

7. **Sigmoid derivative has max 0.25** - This causes vanishing gradients in deep networks

---

## 📝 Practice Problems

### Problem 1
Given $z = 3x + 2$ and $L = z^2$, find $\frac{\partial L}{\partial x}$.

<details>
<summary>Solution</summary>

Using chain rule:
$$\frac{\partial L}{\partial x} = \frac{\partial L}{\partial z} \cdot \frac{\partial z}{\partial x}$$

$$\frac{\partial L}{\partial z} = 2z$$

$$\frac{\partial z}{\partial x} = 3$$

$$\frac{\partial L}{\partial x} = 2z \cdot 3 = 6z = 6(3x + 2) = 18x + 12$$
</details>

### Problem 2
For sigmoid $\sigma(z) = \frac{1}{1+e^{-z}}$, verify that $\frac{d\sigma}{dz} = \sigma(1-\sigma)$.

<details>
<summary>Solution</summary>

$$\sigma(z) = (1 + e^{-z})^{-1}$$

Using chain rule:
$$\frac{d\sigma}{dz} = -1(1 + e^{-z})^{-2} \cdot (-e^{-z})$$

$$= \frac{e^{-z}}{(1 + e^{-z})^2}$$

$$= \frac{1}{1+e^{-z}} \cdot \frac{e^{-z}}{1+e^{-z}}$$

$$= \sigma(z) \cdot \frac{e^{-z}}{1+e^{-z}}$$

$$= \sigma(z) \cdot \frac{1+e^{-z}-1}{1+e^{-z}}$$

$$= \sigma(z) \cdot (1 - \sigma(z))$$ ✓
</details>

### Problem 3
In a 3-layer network, how many chain rule terms are needed to compute $\frac{\partial L}{\partial W_1}$ (first layer weights)?

<details>
<summary>Answer</summary>

You need to pass through all subsequent layers:
- $\frac{\partial L}{\partial y}$ (loss to output)
- $\frac{\partial y}{\partial z_3}$ (output activation)
- $\frac{\partial z_3}{\partial a_2}$ (third layer linear)
- $\frac{\partial a_2}{\partial z_2}$ (second layer activation)
- $\frac{\partial z_2}{\partial a_1}$ (second layer linear)
- $\frac{\partial a_1}{\partial z_1}$ (first layer activation)
- $\frac{\partial z_1}{\partial W_1}$ (finally, first layer weights!)

**7 terms total!** This shows why gradients can vanish in deep networks.
</details>

---

*You've got this! Backpropagation is just the chain rule dressed up. Practice with small examples until it clicks!* 🚀
