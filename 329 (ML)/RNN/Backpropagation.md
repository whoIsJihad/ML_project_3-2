# Backpropagation

## Definition

**Backpropagation** is the algorithm for computing gradients of loss w.r.t. network parameters.

It enables neural networks to learn from error.

Alternative name: **reverse-mode automatic differentiation**.

Uses dynamic programming to efficiently compute gradients in one backward pass.

## The Problem: Why We Need Backpropagation

Suppose we have network with loss:

$$L = f_n(f_{n-1}(...f_1(x, w_1)..., w_{n-1}), w_n)$$

Nested function with $n$ layers. Each layer depends on previous layer's output and its own parameters.

**Goal**: Compute $\frac{\partial L}{\partial w_i}$ for each layer $i$.

**Naive approach**: Use chain rule directly.

$$\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial f_n} \cdot \frac{\partial f_n}{\partial f_{n-1}} \cdot ... \cdot \frac{\partial f_2}{\partial f_1} \cdot \frac{\partial f_1}{\partial w_1}$$

Problem: Each multiplication computes full Jacobian matrices.

For network with $m$ layers, 1000 hidden units, 2000 output units:

Computing all Jacobians naively: $O(2000 \times 1000^2 \times 1000) = 10^{12}$ operations per example.

Backpropagation: $O(2000 \times 1000) = 2 \times 10^6$ operations per example.

**Speedup: 500,000×**

## The Chain Rule (Review)

For composite function:

$$L = f(g(x))$$

Chain rule:

$$\frac{dL}{dx} = \frac{dL}{dg} \cdot \frac{dg}{dx}$$

Extends to multiple functions:

$$\frac{dL}{dx} = \frac{dL}{dz_n} \cdot \frac{dz_n}{dz_{n-1}} \cdot ... \cdot \frac{dz_2}{dz_1} \cdot \frac{dz_1}{dx}$$

Where $z_i$ represents intermediate outputs.

**Key insight**: Compute right-to-left (backward), combining gradients incrementally.

## Forward Pass: Compute Loss

Process input through network, compute intermediate outputs and final loss.

### Example Network

**Input**: $x$
**Layer 1**: $z_1 = w_1 x + b_1$, $a_1 = \sigma(z_1)$
**Layer 2**: $z_2 = w_2 a_1 + b_2$, $a_2 = \sigma(z_2)$
**Loss**: $L = (y - a_2)^2$ (mean squared error, $y$ is label)

### Numeric Example

- Input: $x = 2$
- Label: $y = 0.5$
- Weights: $w_1 = 0.3, w_2 = 0.5$
- Biases: $b_1 = 0.1, b_2 = 0.2$
- Activation: sigmoid $\sigma(z) = \frac{1}{1+e^{-z}}$

**Forward pass**:

Layer 1:
$$z_1 = 0.3 \times 2 + 0.1 = 0.7$$
$$a_1 = \sigma(0.7) = \frac{1}{1+e^{-0.7}} \approx 0.668$$

Layer 2:
$$z_2 = 0.5 \times 0.668 + 0.2 = 0.534$$
$$a_2 = \sigma(0.534) = \frac{1}{1+e^{-0.534}} \approx 0.631$$

Loss:
$$L = (0.5 - 0.631)^2 = (-0.131)^2 = 0.0172$$

## Backward Pass: Compute Gradients

Start from loss, work backward to parameters.

### Key Equations

**Loss gradient w.r.t. output**:
$$\frac{\partial L}{\partial a_2} = 2(a_2 - y) = 2(0.631 - 0.5) = 0.262$$

**Output layer pre-activation gradient**:
$$\frac{\partial L}{\partial z_2} = \frac{\partial L}{\partial a_2} \cdot \frac{\partial a_2}{\partial z_2}$$

For sigmoid: $\frac{\partial \sigma}{\partial z} = \sigma(z)(1 - \sigma(z)) = a_2(1-a_2)$

$$\frac{\partial L}{\partial z_2} = 0.262 \times 0.631 \times (1-0.631) = 0.262 \times 0.631 \times 0.369 = 0.0611$$

**Gradient w.r.t. $w_2$**:
$$\frac{\partial L}{\partial w_2} = \frac{\partial L}{\partial z_2} \cdot \frac{\partial z_2}{\partial w_2}$$

$$z_2 = w_2 a_1 + b_2 \Rightarrow \frac{\partial z_2}{\partial w_2} = a_1 = 0.668$$

$$\frac{\partial L}{\partial w_2} = 0.0611 \times 0.668 = 0.0408$$

**Gradient w.r.t. $b_2$**:
$$\frac{\partial L}{\partial b_2} = \frac{\partial L}{\partial z_2} \cdot \frac{\partial z_2}{\partial b_2} = 0.0611 \times 1 = 0.0611$$

**Backward to layer 1**:
$$\frac{\partial L}{\partial a_1} = \frac{\partial L}{\partial z_2} \cdot \frac{\partial z_2}{\partial a_1}$$

$$\frac{\partial z_2}{\partial a_1} = w_2 = 0.5$$

$$\frac{\partial L}{\partial a_1} = 0.0611 \times 0.5 = 0.03055$$

**Layer 1 pre-activation gradient**:
$$\frac{\partial L}{\partial z_1} = \frac{\partial L}{\partial a_1} \cdot \frac{\partial a_1}{\partial z_1}$$

$$\frac{\partial a_1}{\partial z_1} = a_1(1-a_1) = 0.668 \times 0.332 = 0.222$$

$$\frac{\partial L}{\partial z_1} = 0.03055 \times 0.222 = 0.00678$$

**Gradient w.r.t. $w_1$**:
$$\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial z_1} \cdot \frac{\partial z_1}{\partial w_1}$$

$$\frac{\partial z_1}{\partial w_1} = x = 2$$

$$\frac{\partial L}{\partial w_1} = 0.00678 \times 2 = 0.01356$$

**Gradient w.r.t. $b_1$**:
$$\frac{\partial L}{\partial b_1} = 0.00678$$

## Summary Table: Full Computation

| Variable | Value | Gradient | Role |
|----------|-------|----------|------|
| $x$ | 2 | - | input |
| $z_1$ | 0.7 | 0.00678 | pre-activation layer 1 |
| $a_1$ | 0.668 | 0.03055 | activation layer 1 |
| $z_2$ | 0.534 | 0.0611 | pre-activation layer 2 |
| $a_2$ | 0.631 | 0.262 | output (prediction) |
| $L$ | 0.0172 | - | loss |
| $w_1$ | 0.3 | 0.01356 | weight layer 1 |
| $w_2$ | 0.5 | 0.0408 | weight layer 2 |
| $b_1$ | 0.1 | 0.00678 | bias layer 1 |
| $b_2$ | 0.2 | 0.0611 | bias layer 2 |

## Parameter Update

Using gradient descent with learning rate $\alpha = 0.1$:

$$w_{\text{new}} = w_{\text{old}} - \alpha \frac{\partial L}{\partial w}$$

**Layer 1 weights**:
$$w_1^{\text{new}} = 0.3 - 0.1 \times 0.01356 = 0.2986$$

**Layer 2 weights**:
$$w_2^{\text{new}} = 0.5 - 0.1 \times 0.0408 = 0.4959$$

**Biases**:
$$b_1^{\text{new}} = 0.1 - 0.1 \times 0.00678 = 0.0993$$
$$b_2^{\text{new}} = 0.2 - 0.1 \times 0.0611 = 0.1939$$

After update, loss should be slightly smaller (0.0172 → ~0.0170).

## Why Backward is Efficient

Instead of computing full Jacobians separately:

$$J_2 \times J_1 \times J_0 \text{ (multiply large matrices)}$$

Backprop computes:

$$\left(((v^T J_2) \times J_1) \times J_0\right) \text{ (multiply vectors and matrices)}$$

Where $v = \frac{\partial L}{\partial a_2}$ is gradient from loss.

**Complexity**: $O(n)$ where $n$ = number of operations in forward pass.

Not $O(n^2)$ or $O(n^3)$.

## Computational Graph

Visual representation of backprop:

```
    x=2 ──w₁=0.3──┐
         ──b₁=0.1─┤
                 z₁=0.7 ──σ── a₁=0.668 ──w₂=0.5──┐
                                          ──b₂=0.2─┤
                                                  z₂=0.534 ──σ── a₂=0.631 ──loss── L=0.0172
    y=0.5 ─────────────────────────────────────────────────────────────────────────┘
```

**Forward arrows**: Computation flows left-to-right.

**Backward arrows** (implicit): Gradients flow right-to-left.

At each node: gradient in = (gradient out) × (local derivative).

## Matrix Backprop

For matrix operations:

**Forward**: $y = W x + b$ (where $W \in \mathbb{R}^{m \times n}$, $x \in \mathbb{R}^n$)

**Backward** (given $\frac{\partial L}{\partial y} \in \mathbb{R}^m$):

$$\frac{\partial L}{\partial W} = \frac{\partial L}{\partial y} \times x^T \in \mathbb{R}^{m \times n}$$

$$\frac{\partial L}{\partial x} = W^T \times \frac{\partial L}{\partial y} \in \mathbb{R}^n$$

$$\frac{\partial L}{\partial b} = \frac{\partial L}{\partial y}$$

### Numeric Example: Matrix Backprop

**Forward**:
- $W = \begin{bmatrix} 0.1 & 0.2 \\ 0.3 & 0.4 \end{bmatrix}$ (shape 2×2)
- $x = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$ (shape 2)
- $b = \begin{bmatrix} 0.5 \\ 0.6 \end{bmatrix}$ (shape 2)

$$z = \begin{bmatrix} 0.1 & 0.2 \\ 0.3 & 0.4 \end{bmatrix} \begin{bmatrix} 1 \\ 2 \end{bmatrix} + \begin{bmatrix} 0.5 \\ 0.6 \end{bmatrix} = \begin{bmatrix} 0.5 \\ 1.1 \end{bmatrix} + \begin{bmatrix} 0.5 \\ 0.6 \end{bmatrix} = \begin{bmatrix} 1.0 \\ 1.7 \end{bmatrix}$$

**Backward** (assume $\frac{\partial L}{\partial z} = \begin{bmatrix} 2 \\ 3 \end{bmatrix}$):

$$\frac{\partial L}{\partial W} = \begin{bmatrix} 2 \\ 3 \end{bmatrix} \begin{bmatrix} 1 & 2 \end{bmatrix} = \begin{bmatrix} 2 & 4 \\ 3 & 6 \end{bmatrix}$$

$$\frac{\partial L}{\partial x} = \begin{bmatrix} 0.1 & 0.3 \\ 0.2 & 0.4 \end{bmatrix} \begin{bmatrix} 2 \\ 3 \end{bmatrix} = \begin{bmatrix} 1.1 \\ 1.6 \end{bmatrix}$$

$$\frac{\partial L}{\partial b} = \begin{bmatrix} 2 \\ 3 \end{bmatrix}$$

## Batch Processing

In practice, process multiple examples simultaneously (batch size $B$).

**Forward**: $Y = W X + b$ where $X \in \mathbb{R}^{n \times B}$, $Y \in \mathbb{R}^{m \times B}$

**Backward** (given $\frac{\partial L}{\partial Y} \in \mathbb{R}^{m \times B}$):

$$\frac{\partial L}{\partial W} = \frac{\partial L}{\partial Y} \times X^T / B \in \mathbb{R}^{m \times n}$$

(Divide by $B$ to average over batch)

$$\frac{\partial L}{\partial b} = \text{mean}(\frac{\partial L}{\partial Y}, \text{axis}=1)$$

## Automatic Differentiation

Modern frameworks (PyTorch, TensorFlow) implement backprop automatically.

Build computational graph as code runs, then reverse it.

**Example (PyTorch)**:

```python
x = torch.tensor(2.0, requires_grad=True)
w = torch.tensor(0.3, requires_grad=True)
b = torch.tensor(0.1, requires_grad=True)

z = w * x + b
a = torch.sigmoid(z)
loss = (a - 0.5) ** 2

loss.backward()  # Automatic backprop!

print(f"dx/loss = {x.grad}")   # 0.01356
print(f"dw/loss = {w.grad}")   # 0.0408
print(f"db/loss = {b.grad}")   # 0.00678
```

No manual derivative computation needed!

## Related Concepts

- [[Neural Networks Basics]] - Network architecture
- [[Backpropagation Through Time]] - RNNs adaptation
- [[Vanishing Gradients and Exploding Gradients]] - Training challenges

## Summary

Backpropagation computes gradients efficiently using dynamic programming.

Works by computing chain rule right-to-left (backward).

Each node: incoming gradient × local derivative.

Enables learning in deep neural networks.

Foundation of modern deep learning.
