# 📘 Multilayer Perceptron (MLP)

## 1. Core Idea (Intuition)

* **Problem it solves:** Linear models can only learn linear decision boundaries. MLP can learn **any** non-linear function.
* **Why needed:** Stacking linear layers without activations gives another linear function (`W₂(W₁x) = (W₂W₁)x`). Adding **non-linear activation functions** between layers is what gives neural networks their power.
* **Key insight:** Universal Approximation Theorem — a single hidden layer MLP with enough neurons can approximate any continuous function. But deeper networks learn more efficiently than very wide shallow ones.

---

## 2. Mathematical Formulation

**Architecture:** Input layer → Hidden layer(s) → Output layer

For a 2-layer MLP (1 hidden layer):

```
Hidden layer:   h = f(W₁x + b₁)
Output layer:   ŷ = g(W₂h + b₂)
```

Where:
- `x` = input vector (n_in × 1)
- `W₁` = weight matrix for hidden layer (n_hidden × n_in)
- `b₁` = bias vector for hidden layer (n_hidden × 1)
- `f` = activation function (ReLU, sigmoid, tanh)
- `h` = hidden layer output (n_hidden × 1)
- `W₂` = weight matrix for output layer (n_out × n_hidden)
- `b₂` = bias vector for output layer (n_out × 1)
- `g` = output activation (sigmoid for binary, softmax for multiclass, none for regression)

**Common activation functions:**

| Function | Formula | Range | Derivative |
|---|---|---|---|
| Sigmoid | σ(z) = 1/(1+e⁻ᶻ) | (0, 1) | σ(z)(1-σ(z)) |
| Tanh | (eᶻ - e⁻ᶻ)/(eᶻ + e⁻ᶻ) | (-1, 1) | 1 - tanh²(z) |
| ReLU | max(0, z) | [0, ∞) | 0 if z<0, 1 if z>0 |
| Leaky ReLU | max(αz, z), α small | (-∞, ∞) | α if z<0, 1 if z>0 |

**Why ReLU dominates:**
- No vanishing gradient for positive values (derivative = 1)
- Cheap to compute (just a max)
- Induces sparsity (negative activations → 0)

**Loss functions:**
- Regression: MSE = `(1/m) Σ(yᵢ - ŷᵢ)²`
- Binary classification: Binary Cross-Entropy
- Multiclass: Categorical Cross-Entropy = `-Σₖ yₖ log(ŷₖ)`

---

## 3. Algorithm / Training Procedure

```
Initialize weights (Xavier or He initialization)
Set learning rate, epochs, batch size

For each epoch:
  For each mini-batch:
    1. FORWARD PASS:
       z₁ = W₁x + b₁
       h  = f(z₁)
       z₂ = W₂h + b₂
       ŷ  = g(z₂)

    2. COMPUTE LOSS: L = loss(y, ŷ)

    3. BACKWARD PASS (Backpropagation):
       Compute dL/dW₂, dL/db₂, dL/dW₁, dL/db₁

    4. UPDATE:
       W = W - α · dL/dW   (for all weight matrices)
       b = b - α · dL/db   (for all biases)
```

**Weight Initialization:**

| Method | Formula | Use With |
|---|---|---|
| Xavier/Glorot | W ~ N(0, 2/(n_in + n_out)) | Sigmoid, Tanh |
| He | W ~ N(0, 2/n_in) | ReLU |
| Zero init | W = 0 | **NEVER** — causes symmetry problem |

**Symmetry problem:** If all weights are zero, all neurons compute the same gradients → update identically → remain identical forever. Network effectively has 1 neuron per layer.

---

## 4. Optimization / Learning Dynamics

* More layers = more representational power, but harder to train (vanishing/exploding gradients).
* **Width vs Depth:** Wider = more memorization; Deeper = better feature hierarchies.
* **Epoch:** One full pass through training data.
* **Overfitting signal:** Training loss ↓, validation loss ↑.

| LR | Effect |
|---|---|
| Too small | Slow convergence, stuck in shallow local minima |
| Good | Smooth loss decrease |
| Too large | Loss oscillates or explodes to NaN |

**Training dynamics:**
- Early training: learns broad patterns (low-frequency)
- Late training: learns details and noise (overfitting risk)
- This is why **early stopping** works as regularization

---

## 5. Failure Cases / Limitations

| Failure | Why |
|---|---|
| Vanishing gradients | Sigmoid/tanh squash gradients near zero in deep nets. Early layers stop learning. |
| Exploding gradients | Large weights multiply through layers → gradients → NaN. |
| Overfitting | Too many parameters, too little data. Memorizes training set. |
| Dead ReLU | If neuron input always negative → output always 0 → gradient always 0 → never recovers. |
| Symmetry problem | Zero/constant init → all neurons identical → capacity wasted. |
| No spatial/sequential awareness | Fully connected layers ignore data structure. Use CNN for images, RNN for sequences. |

---

## 6. Where It Works Well

* Tabular/structured data
* Complex feature interactions
* Function approximation
* As building blocks inside CNN, Transformer (they all contain MLP sub-components)
* Classification and regression on medium-sized datasets

---

## 7. Variants / Extensions

| Variant | What it does |
|---|---|
| Deep MLP | More hidden layers, more power, harder to train |
| Residual connections | Skip connections help gradient flow in deep nets |
| Batch Normalization | Normalizes layer outputs, speeds up training |
| Dropout | Randomly zeros neurons during training (regularization) |
| MLP-Mixer | Modern vision architecture using only MLPs (no convolution, no attention) |

---

## 8. Comparison Table

| Method | When to Use | Strength | Weakness |
|---|---|---|---|
| Single Perceptron | Linearly separable only | Simple, fast | Can't solve XOR |
| MLP (1 hidden) | Medium complexity, tabular | Universal approximator | Needs more data than linear models |
| Deep MLP (2+) | Complex patterns | Hierarchical features | Harder to train |
| CNN | Spatial data (images) | Weight sharing, translation invariance | Overkill for tabular |
| Decision Tree | Interpretability needed | No scaling needed | Overfits, high variance |

---

## 9. Exam Questions

### Conceptual:
1. Why do we need non-linear activation functions? What happens with only linear activations in a deep MLP?
2. Explain the symmetry problem with zero initialization.
3. What is the Universal Approximation Theorem and its practical limitations?

### Derivation-based:
4. For a 2-layer MLP with ReLU hidden activation and MSE loss, write out forward pass equations and weight matrix shapes for input dim=5, hidden=10, output=1.
5. Derive the gradient of loss w.r.t. W₁ in a 2-layer MLP using chain rule.

### Trick / Failure-case:
6. Your deep MLP's first-layer weights haven't changed after 1000 epochs but last-layer weights have. What's causing this?
7. You added 5 more hidden layers and performance got worse. Give two reasons and fixes.

---

## 10. Key Takeaways

* MLP = linear transforms + non-linear activations. Without non-linearity, it collapses to one linear layer.
* Universal Approximation: 1 hidden layer can approximate any function, but may need impractically many neurons.
* ReLU is default for hidden layers. Sigmoid only for binary output layer.
* He init for ReLU, Xavier for sigmoid/tanh. Never zero init.
* Depth > width in practice, but deeper = harder to train.
* MLP doesn't understand spatial or sequential structure — use CNN/RNN/Transformer instead.
* Overfitting is the #1 practical problem. Use dropout, early stopping, regularization.
