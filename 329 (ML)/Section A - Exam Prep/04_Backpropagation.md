# 📘 Backpropagation

## 1. Core Idea (Intuition)

**Backpropagation** is an efficient algorithm to compute **gradients of the loss** $\frac{\partial L}{\partial \mathbf{W}^{(l)}}$ for all layers in a neural network.

Why needed:
- Computing $\frac{\partial L}{\partial \mathbf{W}^{(l)}}$ naively for each layer is slow ($O(n^2)$ operations)
- **Backprop** uses **chain rule** to reuse intermediate derivatives, reducing to $O(n)$
- Enables training deep networks with **gradient descent**

---

## 2. Chain Rule & Computational Graphs

For a function $z = f(x)$ where $x = g(y)$:
$$\frac{\partial z}{\partial y} = \frac{\partial z}{\partial x} \cdot \frac{\partial x}{\partial y}$$

**Backprop applies this recursively through the network.**

### Computational Graph
For a 2-layer network:

$$\text{Input } X \xrightarrow{\mathbf{W}^{(1)}} \mathbf{z}^{(1)} \xrightarrow{\sigma} \mathbf{h}^{(1)} \xrightarrow{\mathbf{W}^{(2)}} \mathbf{z}^{(2)} \xrightarrow{\sigma} \mathbf{h}^{(2)} \xrightarrow{\text{loss}} L$$

---

## 3. Forward Pass

Compute predictions layer by layer:

$$\mathbf{z}^{(1)} = X\mathbf{W}^{(1)} + \mathbf{b}^{(1)}$$
$$\mathbf{h}^{(1)} = \sigma(\mathbf{z}^{(1)})$$
$$\mathbf{z}^{(2)} = \mathbf{h}^{(1)}\mathbf{W}^{(2)} + \mathbf{b}^{(2)}$$
$$\mathbf{h}^{(2)} = \sigma(\mathbf{z}^{(2)})$$
$$L = \text{loss}(\mathbf{h}^{(2)}, y)$$

**Store all intermediate values** ($\mathbf{z}^{(l)}, \mathbf{h}^{(l)}$) for backward pass.

---

## 4. Backward Pass (Backpropagation)

Define the **error term** at layer $l$:
$$\boldsymbol{\delta}^{(l)} := \frac{\partial L}{\partial \mathbf{z}^{(l)}}$$

### Step 1: Gradient at Output Layer
$$\boldsymbol{\delta}^{(L)} = \frac{\partial L}{\partial \mathbf{h}^{(L)}} \odot \sigma'(\mathbf{z}^{(L)})$$

where $\odot$ is element-wise multiplication.

**For classification (softmax + cross-entropy):** $\boldsymbol{\delta}^{(L)} = \mathbf{h}^{(L)} - y$ (simplified)

### Step 2: Backpropagate Error
For layer $l = L-1, L-2, \ldots, 1$:

$$\boldsymbol{\delta}^{(l)} = (\boldsymbol{\delta}^{(l+1)} \mathbf{W}^{(l+1)T}) \odot \sigma'(\mathbf{z}^{(l)})$$

**Intuition:** Error from layer $l+1$ is "pushed back" through weights $\mathbf{W}^{(l+1)}$, then scaled by the activation derivative $\sigma'(\mathbf{z}^{(l)})$.

### Step 3: Compute Weight Gradients
$$\frac{\partial L}{\partial \mathbf{W}^{(l)}} = \mathbf{h}^{(l-1)T} \boldsymbol{\delta}^{(l)}$$

$$\frac{\partial L}{\partial \mathbf{b}^{(l)}} = \sum_i \boldsymbol{\delta}^{(l)}_i$$

---

## 5. Backpropagation Algorithm

```
Input: X, y, network weights {W^(l), b^(l)}
Output: Gradients {dW^(l), db^(l)}

=== FORWARD PASS ===
1. For l = 1 to L:
   a. z^(l) = h^(l-1) W^(l) + b^(l)    [h^(0) = X]
   b. h^(l) = σ(z^(l))
2. Compute loss: L = loss(h^(L), y)

=== BACKWARD PASS ===
3. Compute error at output:
   δ^(L) = ∂L/∂h^(L) ⊙ σ'(z^(L))
   
4. For l = L-1 down to 1:
   a. δ^(l) = (δ^(l+1) W^(l+1)^T) ⊙ σ'(z^(l))
   b. dW^(l) = (1/n) h^(l-1)^T δ^(l)
   c. db^(l) = (1/n) Σ_i δ^(l)_i
   
5. Return {dW^(l), db^(l)} for all l
```

---

## 6. Why It Works: Chain Rule Efficiency

**Key insight:** Instead of computing gradients separately for each layer (expensive), backprop **reuses gradients** from later layers.

**Example:** To get gradient for layer 1:
$$\text{Gradient}_1 = \text{(error from layer 2)} \times \text{(gradient of activation)} \times \text{(input)}$$

The "error from layer 2" is computed once and reused → **linear in number of layers**, not exponential.

**Naive approach:** Recompute everything for each layer = $O(n^2)$

**Backprop:** Reuse partial derivatives = $O(n)$

---

## 7. Complexity

| Operation | Time |
|-----------|------|
| Forward pass | $O(n \cdot d)$ |
| Backward pass | $O(n \cdot d)$ |
| **Total cost** | Linear in depth and width |

**Alternative (numerical gradient):** Much slower due to repeated forward passes

---

## 8. Common Mistakes & Pitfalls

| Mistake | Why Wrong | Fix |
|---------|-----------|-----|
| **Not storing forward pass values** | Can't compute $\sigma'(\mathbf{z}^{(l)})$ in backward | Store all $\mathbf{z}^{(l)}, \mathbf{h}^{(l)}$ during forward |
| **Forgetting activation derivative** | $\boldsymbol{\delta}^{(l)} = \boldsymbol{\delta}^{(l+1)} \mathbf{W}^{(l+1)T}$ is incomplete | Must multiply by $\sigma'(\mathbf{z}^{(l)})$ |
| **Wrong gradient shape** | $\frac{\partial L}{\partial \mathbf{W}^{(l)}} \in \mathbb{R}^{m_{l-1} \times m_l}$ | Match dimensions: $\mathbf{h}^{(l-1)T} \boldsymbol{\delta}^{(l)}$ |
| **Modifying weights during backward** | Breaks gradient computation for earlier layers | Compute all gradients first, update all weights together |

---

## 9. Numerical Gradient Checking

**Finite differences** (slow, but for verification):
$$\frac{\partial L}{\partial w_{ij}} \approx \frac{L(w_{ij} + \epsilon) - L(w_{ij} - \epsilon)}{2\epsilon}$$

where $\epsilon \approx 10^{-5}$.

**Gradient check:**
1. Compute gradients via backprop: $g_{\text{analytical}}$
2. Compute via finite differences: $g_{\text{numerical}}$
3. Check $\left\| g_{\text{analytical}} - g_{\text{numerical}} \right\| / \left\| g_{\text{analytical}} + g_{\text{numerical}} \right\| < 10^{-5}$

---

## 10. Failure Cases / Limitations

| Problem | Why | Impact |
|---------|-----|--------|
| **Vanishing gradients** | $\sigma'(z) \leq 0.25$ for sigmoid; chain rule multiplies many small values | Gradients exponentially decay; early layers don't learn |
| **Exploding gradients** | Large weights or many layers | Gradients grow unboundedly; training unstable |
| **Computational memory** | Must store all forward activations | Memory scales with depth + batch size |

---

## 11. Exam Questions

### Conceptual
1. Explain the chain rule in backpropagation. Why does backprop compute gradients in reverse order?
2. Why is gradient checking important? What does it verify?
3. In a 5-layer network, which layer's weights are hardest to update via backprop? Why?

### Derivation-Based
1. **Derive** the error term $\boldsymbol{\delta}^{(l)}$ for a 3-layer network starting from the output layer.
2. **Show** that backprop is $O(n \cdot d)$ per layer, while finite differences would be $O(n \cdot d^2)$.

### Trick/Failure Cases
1. You implement backprop and get near-zero gradients after 3 layers. The loss doesn't decrease. What's wrong?
2. Your gradient check fails: analytical gradient = 0.5, numerical gradient = 0.0001. Where's the bug?

---

## 12. Key Takeaways

- **Backprop** computes $\frac{\partial L}{\partial \mathbf{W}^{(l)}}$ efficiently via **chain rule**
- **Error terms:** $\boldsymbol{\delta}^{(l)} = \frac{\partial L}{\partial \mathbf{z}^{(l)}}$ propagate backward
- **Recurrence:** $\boldsymbol{\delta}^{(l)} = (\boldsymbol{\delta}^{(l+1)} \mathbf{W}^{(l+1)T}) \odot \sigma'(\mathbf{z}^{(l)})$
- **Weight gradient:** $\frac{\partial L}{\partial \mathbf{W}^{(l)}} = \mathbf{h}^{(l-1)T} \boldsymbol{\delta}^{(l)}$
- **Efficiency:** $O(Lnd)$ vs. $O(Ld^2)$ with finite differences
- **Memory tradeoff:** Store all forward values; backward pass is compute-dominated
- **Vanishing gradients:** main challenge; addressed by activation choice (ReLU), batch norm, careful initialization

---
