# 📝 Multilayer Perceptron - Exam Answers

## Conceptual Questions

### Q1: Why can't a 1-layer MLP with sigmoid solve the XOR problem, but a 2-layer MLP can? Use geometry to explain.

**Answer:**

**The XOR Problem:**
```
Input (x₁, x₂)  →  Output
(0, 0)          →  0
(0, 1)          →  1
(1, 0)          →  1
(1, 1)          →  0
```

Not linearly separable. Cannot be split by a single line.

---

**1-Layer MLP (Logistic Regression):**

Model:
$$\hat{y} = \sigma(x_1 w_1 + x_2 w_2 + b)$$

Decision boundary (where $\hat{p} = 0.5$):
$$x_1 w_1 + x_2 w_2 + b = 0$$

This is a **straight line** in 2D space. Cannot separate XOR's diagonal structure.

**Geometric view:**
```
(0,1) ●───────● (1,1)     A single line cannot separate
      │ \   / │           • (0,0) and (1,1) [output 0]
      │  \ /  │           from
      │  / \  │           • (0,1) and (1,0) [output 1]
      ●───────● (1,0)
     (0,0)
```

**Conclusion:** Single line fails → need curves or multiple lines.

---

**2-Layer MLP (with hidden layer):**

```
Input Layer → Hidden Layer → Output Layer

x₁ ──┐                     
     ├─→ h₁ = σ(w₁₁x₁ + w₁₂x₂)
x₂ ──┤                          ──→ ŷ = σ(u₁h₁ + u₂h₂ + c)
     └─→ h₂ = σ(w₂₁x₁ + w₂₂x₂)
```

**How it works:**

Each hidden neuron creates a **decision boundary** (a line):
- $h_1 = \sigma(x_1 + x_2 - 0.5)$ — approximately fires when $x_1 + x_2 > 0.5$
- $h_2 = \sigma(-x_1 - x_2 + 1.5)$ — approximately fires when $x_1 + x_2 < 1.5$

Combined hidden activations:
```
(0,0): h₁ ≈ 0, h₂ ≈ 1  →  (h₁, h₂) = (0, 1)
(0,1): h₁ ≈ 1, h₂ ≈ 1  →  (h₁, h₂) = (1, 1)
(1,0): h₁ ≈ 1, h₂ ≈ 1  →  (h₁, h₂) = (1, 1)
(1,1): h₁ ≈ 1, h₂ ≈ 0  →  (h₁, h₂) = (1, 0)
```

In the **(h₁, h₂) space**, the points are now **linearly separable**!

Output layer then learns: $\hat{y} = \sigma(h_1 - h_2)$ (or similar).

**Key insight:** Hidden layer **transforms** input space into new space where XOR becomes separable.

---

**General principle:**
- 1 layer = linear boundaries
- 2 layers = can create "islands" and complex regions (combinations of linear boundaries)
- Deep layers = extremely complex, non-linear decision surfaces

---

### Q2: What is the vanishing gradient problem? Why is it worse for deeper networks?

**Answer:**

**Vanishing Gradients:**

During backpropagation, gradients multiply layer by layer:

$$\frac{\partial L}{\partial \mathbf{w}^{(1)}} = \frac{\partial L}{\partial \mathbf{w}^{(L)}} \cdot \frac{\partial \mathbf{w}^{(L)}}{\partial \mathbf{w}^{(L-1)}} \cdots \frac{\partial \mathbf{w}^{(2)}}{\partial \mathbf{w}^{(1)}}$$

Each layer introduces a factor of:
$$\frac{\partial h^{(l)}}{\partial h^{(l-1)}} = \sigma'(z^{(l)}) \cdot W^{(l)}$$

**The problem:** Sigmoid derivative:
$$\sigma'(z) = \sigma(z)(1-\sigma(z)) \in (0, 0.25]$$

Maximum is 0.25 when $z = 0$.

---

**Example with 3 layers:**

$$\frac{\partial L}{\partial w^{(1)}} = \frac{\partial L}{\partial a^{(3)}} \cdot \sigma'(z^{(3)}) \cdot W^{(3)} \cdot \sigma'(z^{(2)}) \cdot W^{(2)} \cdot \sigma'(z^{(1)})$$

If each $\sigma'(z) ≈ 0.2$ and $W$ normalized:

$$\frac{\partial L}{\partial w^{(1)}} ≈ \text{const} \times 0.2^3 = 0.008 \times \text{const}$$

Gradient for early layers is **1000× smaller**!

---

**Why it's worse for deep networks:**

With $L$ layers:
$$\frac{\partial L}{\partial w^{(1)}} ∝ (0.2)^{L-1}$$

```
L=2:   gradient ≈ 0.2   (OK)
L=3:   gradient ≈ 0.04  (small)
L=5:   gradient ≈ 0.0016 (very small)
L=10:  gradient ≈ 10^{-7} (near-zero!)
```

Early layers barely update → training stalls.

---

**Solutions:**

1. **ReLU activation:** $\text{ReLU}'(z) = 1$ (not 0.25)
2. **Batch normalization:** Keep activations in sweet spot
3. **Skip connections (ResNet):** Bypass layers, create "fast paths" for gradients
4. **Careful weight initialization:** Start with good $W$

---

### Q3: Why do we use ReLU instead of sigmoid in hidden layers?

**Answer:**

**ReLU (Rectified Linear Unit):**
$$\text{ReLU}(z) = \max(0, z)$$

---

**Advantages over sigmoid:**

1. **Non-vanishing gradients**
   - $\text{ReLU}'(z) = 1$ if $z > 0$ (not squeezed to 0.25)
   - Gradient flows cleanly through layers

2. **Computational efficiency**
   - ReLU: simple thresholding (max(0, z))
   - Sigmoid: requires exponential ($e^{-z}$)
   - ~10× faster to compute

3. **Sparsity**
   - ReLU outputs 0 for $z < 0$
   - Makes activations sparse (many zeros)
   - Biologically plausible (neurons can be inactive)

4. **Avoids saturation**
   - Sigmoid: output in (0, 1); gradient ≈ 0 at extremes
   - ReLU: output unbounded; always has non-zero gradient for $z > 0$

---

**Disadvantage: Dying ReLU**

For $z < 0$: ReLU outputs 0 and $\frac{\partial}{\partial z} = 0$.

If neuron stuck in negative regime, it "dies" (never updates).

**Solution:** Leaky ReLU: $\text{LeakyReLU}(z) = \max(0.01z, z)$ (small negative slope)

---

**In practice:**
- Hidden layers: ReLU (fast, trains deep networks well)
- Output layer: Sigmoid (for probability), Linear (for regression)

---

## Derivation-Based Questions

### Q1: Compute the gradient $\frac{\partial L}{\partial \mathbf{W}^{(1)}}$ for a 2-layer network.

**Answer:**

**2-Layer Network:**
```
Input x → Hidden layer h = σ(W⁽¹⁾x) → Output ŷ = σ(W⁽²⁾h)
```

**Forward pass:**
- $z^{(1)} = \mathbf{W}^{(1)}x + b^{(1)}$
- $h = \sigma(z^{(1)})$
- $z^{(2)} = \mathbf{W}^{(2)}h + b^{(2)}$
- $\hat{y} = \sigma(z^{(2)})$
- $L = (y - \hat{y})^2$ (MSE)

**Backward pass (chain rule):**

$$\frac{\partial L}{\partial \mathbf{W}^{(1)}} = \frac{\partial L}{\partial z^{(1)}} \frac{\partial z^{(1)}}{\partial \mathbf{W}^{(1)}}$$

**Step 1:** Gradient at output
$$\frac{\partial L}{\partial \hat{y}} = -2(y - \hat{y})$$

**Step 2:** Through $z^{(2)}$
$$\frac{\partial L}{\partial z^{(2)}} = \frac{\partial L}{\partial \hat{y}} \sigma'(z^{(2)}) = -2(y - \hat{y})\sigma'(z^{(2)})$$

**Step 3:** Through $h$
$$\frac{\partial L}{\partial h} = (\mathbf{W}^{(2)})^T \frac{\partial L}{\partial z^{(2)}}$$

**Step 4:** Through $z^{(1)}$
$$\frac{\partial L}{\partial z^{(1)}} = \frac{\partial L}{\partial h} \odot \sigma'(z^{(1)})$$

where $\odot$ is element-wise multiplication.

**Step 5:** Through $\mathbf{W}^{(1)}$
$$\frac{\partial L}{\partial \mathbf{W}^{(1)}} = \frac{\partial L}{\partial z^{(1)}} x^T$$

**Final:**
$$\boxed{\frac{\partial L}{\partial \mathbf{W}^{(1)}} = [\text{errors} \odot \sigma'(z^{(1)})] \cdot x^T}$$

---

### Q2: Prove that the output of an L-layer MLP is $\sigma^{(L)} \circ \sigma^{(L-1)} \circ \cdots \circ \sigma^{(1)}(X\mathbf{W}^{(1)})$.

**Answer:**

**Proof by induction:**

**Base case (L=1):**
$$\hat{y}^{(1)} = \sigma^{(1)}(X\mathbf{W}^{(1)} + b^{(1)}) = \sigma^{(1)}(X\mathbf{W}^{(1)})$$

(ignoring bias for simplicity)

✓ Matches claim.

**Inductive step:**

Assume for $L-1$ layers:
$$h^{(L-1)} = \sigma^{(L-1)} \circ \cdots \circ \sigma^{(1)}(X\mathbf{W}^{(1)})$$

For $L$ layers:
$$h^{(L)} = \sigma^{(L)}(h^{(L-1)} \mathbf{W}^{(L)})$$

$$= \sigma^{(L)}([\sigma^{(L-1)} \circ \cdots \circ \sigma^{(1)}(X\mathbf{W}^{(1)})] \mathbf{W}^{(L)})$$

$$= (\sigma^{(L)} \circ \sigma^{(L-1)} \circ \cdots \circ \sigma^{(1)})(X\mathbf{W}^{(1)})$$

✓ By induction, holds for all $L$. QED.

---

## Trick / Failure Cases

### Q1: You train a 10-layer network. Training loss decreases for 100 iterations, then stays flat. Gradients are near-zero. What happened?

**Answer:**

**Diagnosis:** Vanishing gradients (discussed in conceptual Q2).

With 10 layers and sigmoid activation, gradients diminish exponentially:
$$\frac{\partial L}{\partial w^{(1)}} ∝ (0.2)^9 ≈ 10^{-7}$$

Weights barely update → loss plateaus.

---

**Fixes:**

1. **Switch to ReLU:** Instant fix. Replace sigmoid with ReLU in hidden layers.
2. **Batch normalization:** Keeps activations normalized; prevents saturation.
3. **Add skip connections:** $h^{(l+2)} = h^{(l)} + f(h^{(l)})$ (ResNet-style)
4. **Reduce depth:** 10 layers may be overkill; try 3-4.
5. **Better initialization:** Xavier or He initialization helps.
6. **Gradient clipping:** Prevent explosion/vanishing by clipping

**Recommended:** Use ReLU + batch norm + skip connections. These are now standard.

---

### Q2: A ReLU neuron at layer 5 always outputs 0. Can it recover during training?

**Answer:**

**What it means:**
```
z⁽⁵⁾ = W⁽⁵⁾h⁽⁴⁾ + b⁽⁵⁾ always < 0
∴ h⁽⁵⁾ = ReLU(z⁽⁵⁾) = 0 for all training samples
```

---

**Can it recover?**

**During training:** Gradients for this neuron:
$$\frac{\partial L}{\partial w^{(5)}} = \frac{\partial L}{\partial z^{(5)}} h^{(4)} = 0 \cdot h^{(4)} = 0$$

(because ReLU'(z) = 0 for z < 0)

Weights **don't update**. Neuron stays dead.

**This is the "Dying ReLU" problem.** Once dead, very hard to recover.

---

**Can we fix it before training?**

1. **Leaky ReLU:** 
   ```
   LeakyReLU(z) = max(0.01z, z)
   Even for z < 0, gradient = 0.01 ≠ 0
   Neuron can learn to change its weights
   ```

2. **Careful initialization:**
   ```
   Initialize biases to small positive values
   Increases chance z > 0 initially
   Neuron activates from start
   ```

3. **Batch normalization:**
   ```
   Keeps activations ~ N(0,1)
   z values less extreme; less likely to be always negative
   ```

---

**Bottom line:** Once a ReLU neuron dies, it's very hard to recover. Use Leaky ReLU or batch norm to prevent it.

