# 📘 Backpropagation

## 1. Core Idea (Intuition)

* **Problem it solves:** How do we compute gradients for weights in hidden layers? We can compute the loss at the output, but how does each weight deep inside the network affect that loss?
* **Why needed:** In an MLP, the loss only directly depends on the output layer. To update hidden-layer weights, we need to "propagate" the error signal backward through the network.
* **Key insight:** Chain rule of calculus. The gradient of loss w.r.t. any weight = product of local gradients along the path from that weight to the loss. We compute this efficiently by going backward, layer by layer, reusing intermediate results.

---

## 2. Mathematical Formulation

Consider a 2-layer MLP:

```
z₁ = W₁x + b₁       (pre-activation, hidden)
a₁ = f(z₁)            (activation, hidden)
z₂ = W₂a₁ + b₂       (pre-activation, output)
ŷ  = g(z₂)            (output)
L  = loss(y, ŷ)
```

Symbols:
- `z` = pre-activation (linear combination before activation)
- `a` = post-activation
- `f, g` = activation functions
- `L` = scalar loss value

**Goal:** Compute `dL/dW₁`, `dL/db₁`, `dL/dW₂`, `dL/db₂`

### Output layer gradients (straightforward):

```
δ₂ = dL/dz₂ = dL/dŷ · dŷ/dz₂ = dL/dŷ · g'(z₂)
```

For softmax + cross-entropy or sigmoid + BCE, this simplifies to:
```
δ₂ = ŷ - y
```

Then:
```
dL/dW₂ = δ₂ · a₁ᵀ
dL/db₂ = δ₂
```

### Hidden layer gradients (the "back" propagation):

```
δ₁ = dL/dz₁ = (W₂ᵀ δ₂) ⊙ f'(z₁)
```

Where `⊙` = element-wise multiplication.

Explanation:
- `W₂ᵀ δ₂` propagates the error signal backward through the weights
- `f'(z₁)` scales by the local gradient of the activation function

Then:
```
dL/dW₁ = δ₁ · xᵀ
dL/db₁ = δ₁
```

**General pattern for layer l:**
```
δₗ = (Wₗ₊₁ᵀ δₗ₊₁) ⊙ f'(zₗ)
dL/dWₗ = δₗ · aₗ₋₁ᵀ
dL/dbₗ = δₗ
```

**Proof of the chain rule step (for hidden layer):**

```
dL/dz₁ = dL/dz₂ · dz₂/da₁ · da₁/dz₁
```

- `dL/dz₂ = δ₂` (already computed)
- `dz₂/da₁ = W₂` (since z₂ = W₂a₁ + b₂, derivative w.r.t. a₁ is W₂)
- `da₁/dz₁ = f'(z₁)` (derivative of activation)

So: `δ₁ = W₂ᵀ δ₂ ⊙ f'(z₁)` ✓

(The transpose is because we're going backward through the matrix multiplication.)

---

## 3. Algorithm / Training Procedure

```
FORWARD PASS (store all intermediate values):
    For l = 1 to L:
        zₗ = Wₗ · aₗ₋₁ + bₗ     (a₀ = x)
        aₗ = fₗ(zₗ)
    Loss = L(y, aₗ)

BACKWARD PASS:
    Compute δ_L = dL/dz_L at output layer
    For l = L-1 down to 1:
        δₗ = (Wₗ₊₁ᵀ δₗ₊₁) ⊙ fₗ'(zₗ)
        dL/dWₗ = δₗ · aₗ₋₁ᵀ
        dL/dbₗ = δₗ

UPDATE:
    For all l:
        Wₗ = Wₗ - α · dL/dWₗ
        bₗ = bₗ - α · dL/dbₗ
```

**Key insight:** We must store `zₗ` and `aₗ` during forward pass because backward pass needs them. This is the memory cost of backprop.

---

## 4. Optimization / Learning Dynamics

* **Computational complexity:** Forward pass + backward pass is roughly 2× the cost of forward pass alone. Backward pass reuses forward pass computations.
* **Memory:** Must store all intermediate activations. For deep networks, this is the bottleneck (not compute).

**Vanishing gradients (deep sigmoid/tanh networks):**

Since `δₗ = W₂ᵀ δₗ₊₁ ⊙ f'(zₗ)`:
- Sigmoid: max(f'(z)) = 0.25 (at z=0). Each layer multiplies gradient by ≤ 0.25.
- Through 10 layers: gradient shrinks by factor 0.25¹⁰ ≈ 0.000001
- Early layers get near-zero gradients → stop learning.

**Exploding gradients:**
- If `||W||` is large, each backward step multiplies gradient by a large factor.
- Through many layers: gradient grows exponentially → NaN.

**Solutions:**
- ReLU activation (derivative = 1 for positive values, no shrinking)
- Gradient clipping (cap gradient magnitude)
- Skip/residual connections
- Proper weight initialization (He/Xavier)
- Batch normalization

---

## 5. Failure Cases / Limitations

| Failure | Why |
|---|---|
| Vanishing gradients | Sigmoid/tanh derivatives < 1, compound over layers |
| Exploding gradients | Large weight norms multiply over layers |
| Incorrect implementation | Off-by-one errors, wrong transpose, forgetting to store intermediates |
| Memory blow-up | Very deep or wide networks: all activations stored |
| Non-differentiable activations | Hard step function has zero gradient everywhere except at 0 (where it's undefined) |

---

## 6. Where It Works Well

* Training any neural network (MLP, CNN, RNN, Transformer — all use backprop)
* Any differentiable computation graph
* When combined with automatic differentiation frameworks (PyTorch, TensorFlow)

---

## 7. Variants / Extensions

| Variant | What it does |
|---|---|
| Backprop Through Time (BPTT) | Backprop unrolled over time steps for RNNs |
| Truncated BPTT | Limits how far back gradients flow in RNNs (saves memory) |
| Automatic Differentiation | Software computes backprop automatically (PyTorch autograd) |
| Gradient Checkpointing | Trade compute for memory: recompute activations instead of storing |

---

## 8. Comparison Table

| Method | When to Use | Strength | Weakness |
|---|---|---|---|
| Backpropagation | Any differentiable neural network | Efficient, exact gradients | Memory-intensive, vanishing/exploding gradients |
| Numerical differentiation | Debugging, gradient checking | Simple to implement | Extremely slow (O(n) forward passes per parameter), approximate |
| Evolutionary strategies | Non-differentiable models | No gradients needed | Very slow convergence, high variance |
| Finite differences | Small networks, verification | Easy conceptually | O(n) cost, numerical errors |

---

## 9. Exam Questions

### Conceptual:
1. Why must we go backward (not forward) to compute gradients efficiently?
2. Why do we need to store intermediate activations during forward pass?
3. Explain vanishing gradients mathematically — why does sigmoid cause it and ReLU fix it?

### Derivation-based:
4. For a 2-layer MLP with sigmoid activations and MSE loss, derive all four gradient expressions (dL/dW₁, dL/db₁, dL/dW₂, dL/db₂) using chain rule.
5. Show that for sigmoid + binary cross-entropy, the output-layer delta simplifies to `δ = ŷ - y`.

### Trick / Failure-case:
6. You compute gradients numerically and they differ significantly from your backprop implementation. How do you debug this?
7. Training a 50-layer network with tanh activations. Loss barely decreases. First layer gradients are ~10⁻¹⁵. Diagnosis and fix?

---

## 10. Key Takeaways

* Backprop = chain rule applied layer by layer, backward from loss to input.
* The "delta" at each layer: `δₗ = (Wₗ₊₁ᵀ δₗ₊₁) ⊙ f'(zₗ)` — error signal scaled by local activation derivative.
* Forward pass stores intermediates; backward pass uses them. Memory cost = O(total activations).
* Vanishing gradients: sigmoid/tanh derivatives < 1 compound multiplicatively over depth.
* ReLU, skip connections, and BatchNorm are the practical fixes for gradient flow problems.
* Every modern deep learning framework implements backprop automatically (autograd).
