# 📘 Multilayer Perceptron (MLP)

## 1. Core Idea (Intuition)

A **Multilayer Perceptron** ($\text{MLP}$) is a feedforward neural network with **multiple hidden layers**, enabling it to learn **non-linear decision boundaries**.

Why needed:
- **Logistic regression** assumes $y = \sigma(X\mathbf{w})$ (linear combination → sigmoid)
- **MLP** stacks multiple sigmoid/ReLU layers: $y = \sigma(\sigma(\sigma(X\mathbf{w}^{(1)})\mathbf{w}^{(2)})\mathbf{w}^{(3)})$
- This composition of nonlinearities creates **universal approximation capability**

---

## 2. Mathematical Formulation

### Architecture
Let $\mathbf{h}^{(l)} \in \mathbb{R}^{m_l}$ be the activation vector at layer $l$.

**Layer $l$:**
$$\mathbf{z}^{(l)} = \mathbf{h}^{(l-1)} \mathbf{W}^{(l)} + \mathbf{b}^{(l)}$$

$$\mathbf{h}^{(l)} = \sigma(\mathbf{z}^{(l)})$$

where:
- $\mathbf{W}^{(l)} \in \mathbb{R}^{m_{l-1} \times m_l}$: weight matrix (from layer $l-1$ to $l$)
- $\mathbf{b}^{(l)} \in \mathbb{R}^{m_l}$: bias vector
- $\sigma(\cdot)$: activation function (sigmoid, $\tanh$, ReLU, etc.)
- $\mathbf{h}^{(0)} = X$ (input layer)

### Full Network (3-layer example)
$$\mathbf{h}^{(1)} = \sigma(X\mathbf{W}^{(1)} + \mathbf{b}^{(1)})$$

$$\mathbf{h}^{(2)} = \sigma(\mathbf{h}^{(1)}\mathbf{W}^{(2)} + \mathbf{b}^{(2)})$$

$$\hat{y} = \text{softmax}(\mathbf{h}^{(2)}\mathbf{W}^{(3)} + \mathbf{b}^{(3)})$$

### Loss Function
For regression: $L = \frac{1}{n}\sum_{i=1}^{n} \|\hat{y}_i - y_i\|^2$ (MSE)

For classification: $L = -\frac{1}{n}\sum_{i=1}^{n} y_i^T \log(\hat{y}_i)$ (cross-entropy)

---

## 3. Universal Approximation Theorem

**Theorem:** A 2-layer MLP with sufficient hidden units can approximate **any continuous function** on a compact domain.

**Intuition:**
- Each hidden neuron creates a "bump" in feature space
- Combining bumps can fit any smooth curve
- More hidden units = better approximation

**Practical takeaway:**
- Theory guarantees MLP can learn any function
- Practice: need sufficient data, good optimization, and hyperparameter tuning

---

## 4. Activation Functions

| Function | Formula | Derivative | Range | When to Use |
|----------|---------|-----------|-------|------------|
| **Sigmoid** | $\sigma(z) = \frac{1}{1+e^{-z}}$ | $\sigma'(z) = \sigma(z)(1-\sigma(z))$ | $(0,1)$ | Output layer (binary), interpretability |
| **Tanh** | $\tanh(z) = \frac{e^{z}-e^{-z}}{e^{z}+e^{-z}}$ | $\tanh'(z) = 1-\tanh^2(z)$ | $(-1,1)$ | Hidden layers, centered around 0 |
| **ReLU** | $\text{ReLU}(z) = \max(0, z)$ | $\text{ReLU}'(z) = \begin{cases}1 & z>0 \\ 0 & z\leq 0\end{cases}$ | $[0,\infty)$ | Hidden layers, default choice (fast) |
| **Leaky ReLU** | $\text{LeakyReLU}(z) = \max(\alpha z, z)$ where $\alpha \approx 0.01$ | Gradient always nonzero | $(-\infty,\infty)$ | Prevents dying ReLU |
| **Softmax** | $\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_j e^{z_j}}$ | $\frac{\partial}{\partial z_i} = \text{softmax}(z_i)(1 - \text{softmax}(z_i))$ | $(0,1)$, sums to 1 | Output layer (multi-class) |

---

## 5. Why Deep Networks?

### The Case for Depth
A $L$-layer network can express functions requiring $2^L$ hidden units in a 1-layer network.

**Example:** Representing $x_1 \oplus x_2 \oplus \cdots \oplus x_n$ (XOR-like problem):
- 1-layer MLP: exponential in $n$ hidden units needed
- 3-layer MLP: polynomial in $n$ hidden units needed

---

## 6. Failure Cases / Limitations

| Problem | Why | Impact |
|---------|-----|--------|
| **Vanishing Gradients** | In deep networks, gradients decay exponentially through layers | Weights near input don't update; only output layer learns |
| **Exploding Gradients** | Gradients grow exponentially through layers | Training unstable, weights diverge to $\infty$ |
| **Overfitting** | Too many parameters, too little data | 0% train error, 50% test error |
| **Saturation** | Sigmoid/tanh saturate near $\pm 1$, gradient $\approx 0$ | Learning stops despite error |
| **Dead ReLU** | ReLU outputs 0 for $z < 0$; once stuck, gradient is 0 forever | Neuron "dies"; contributes nothing |

---

## 7. When It Works Well

- **Complex non-linear patterns** in data
- **Sufficient training data** ($n \gg d$ to avoid overfitting)
- **Differentiable target function** (regression, classification)
- **Real-world:** image recognition, NLP, game AI

---

## 8. Key Architectural Choices

| Choice | Impact | Common Values |
|--------|--------|----------------|
| **Hidden Layers** | Depth allows hierarchical learning | 2-5 (modern: up to 100+) |
| **Hidden Units per Layer** | Capacity to fit data | 32, 64, 128, 256 |
| **Activation Function** | Nonlinearity; controls gradient flow | ReLU (most common) |
| **Output Activation** | Shapes output; depends on task | Sigmoid (binary), softmax (multi-class), identity (regression) |

---

## 9. Exam Questions

### Conceptual
1. Why can't a 1-layer MLP with sigmoid solve the XOR problem, but a 2-layer MLP can? Use geometry to explain.
2. What is the vanishing gradient problem? Why is it worse for deeper networks?
3. Why do we use ReLU instead of sigmoid in hidden layers?

### Derivation-Based
1. **Compute** the gradient $\frac{\partial L}{\partial \mathbf{W}^{(1)}}$ for a 2-layer network. (Requires backpropagation; see next section.)
2. **Prove** that the output of an $L$-layer MLP is $\sigma^{(L)} \circ \sigma^{(L-1)} \circ \cdots \circ \sigma^{(1)}(X\mathbf{W}^{(1)})$ (function composition).

### Trick/Failure Cases
1. You train a 10-layer network. Training loss decreases for 100 iterations, then stays flat. Gradients are near-zero. What happened?
2. A ReLU neuron at layer 5 always outputs 0. Can it recover during training?

---

## 10. Key Takeaways

- **MLP** stacks multiple layers of nonlinearities: $\mathbf{h}^{(l)} = \sigma(\mathbf{h}^{(l-1)}\mathbf{W}^{(l)} + \mathbf{b}^{(l)})$
- **Universal approximation:** sufficient hidden units can fit any function
- **Depth > width:** deeper networks need fewer parameters for same expressiveness
- **Activation choice matters:** ReLU avoids saturation; softmax for probability output
- **Vanishing/exploding gradients:** major training challenges in deep networks (solved later with techniques like batch norm)
- **Overfitting risk:** easy with MLPs due to high capacity; use regularization

---
