# 📘 Kernels / Filters in CNN

## 1. Core Idea (Intuition)

A **kernel** (filter) is a small matrix that detects **local patterns** in input.

Different kernels detect different features:
- **Edge detection:** Gradient-based kernels
- **Blur:** Averaging kernels
- **Sharpen:** Difference kernels
- **Learned features:** Kernels trained via backpropagation

---

## 2. Hand-Crafted Kernels (Classical)

### Sobel Edge Detection (Vertical)
$$F_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}$$

**Effect:** Detects vertical edges (high response when intensity changes left-to-right).

### Sobel Edge Detection (Horizontal)
$$F_y = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}$$

**Effect:** Detects horizontal edges.

### Laplacian Edge Detection
$$F = \begin{bmatrix} 0 & 1 & 0 \\ 1 & -4 & 1 \\ 0 & 1 & 0 \end{bmatrix}$$

**Effect:** Detects edges in all directions (second derivative).

### Gaussian Blur
$$F = \frac{1}{16} \begin{bmatrix} 1 & 2 & 1 \\ 2 & 4 & 2 \\ 1 & 2 & 1 \end{bmatrix}$$

**Effect:** Smooths image; reduces noise.

---

## 3. Learned Kernels in CNN

Unlike classical kernels (fixed), CNN kernels are **optimized via backpropagation**.

**Key insight:** Backprop updates filter weights to minimize loss.

$$\frac{\partial L}{\partial F} = \text{(gradient w.r.t. filter)}$$

### Example: What a Learned Filter Might Look Like

**Layer 1 filters:** Learn edge and corner detectors (similar to Sobel)

**Layer 2 filters:** Learn combinations of edges → textures (stripes, corners, etc.)

**Layer 3 filters:** Learn parts (eyes, wheels, fur)

**Deeper layers:** Learn object-specific patterns

**This hierarchical learning is automatic via backprop.**

---

## 4. Number of Filters & Capacity

### Depth (Number of Filters per Layer)
Each filter produces one output channel.

**Input:** $H \times W \times C_{\text{in}}$

**Output:** $H' \times W' \times C_{\text{out}}$ (where $C_{\text{out}}$ = number of filters)

**Interpretation:** More filters → more capacity to learn diverse features.

**Typical values:** 32, 64, 128, 256, 512 (increase as we go deeper).

### Parameter Count
**Convolutional layer:**
$$\text{Parameters} = K \times K \times C_{\text{in}} \times C_{\text{out}} + C_{\text{out}}$$

(Last term: biases, one per output channel)

**Example:** $K=3$, $C_{\text{in}}=64$, $C_{\text{out}}=128$
$$\text{Parameters} = 3 \times 3 \times 64 \times 128 + 128 = 73,856$$

**Compare to fully connected:** If input is $8 \times 8 \times 64$ → $4,096$ parameters per neuron. One hidden layer with 128 neurons would have $4,096 \times 128 = 524,288$ parameters (7x more!).

---

## 5. Effective Receptive Field

**Receptive field:** Size of input region influencing one output neuron.

**After 1 conv layer** ($K=3$): Receptive field = 3

**After 2 conv layers** ($K=3$ each): Receptive field = $3 + 2 \times (3-1) = 7$

**General formula:** $R_l = R_{l-1} + (K - 1) \prod_{i=l-1}^{1} S_i$

**Interpretation:** Deeper layers see larger context; early layers see local details.

**Why it matters:** Need enough depth to capture global context (e.g., full object).

---

## 6. Dilation & Stride

### Stride $S$
Filter moves by $S$ positions at a time (vs. default $S=1$).

$$\text{Output height} = \frac{H - K}{S} + 1$$

**Effect:** Reduces output spatial dimensions faster; fewer parameters.

**Tradeoff:** Lose fine-grained information; cheaper computation.

### Dilation (Atrous Convolution)
Filter samples input at intervals (not consecutive positions).

$$\text{Dilation} = d \implies \text{filter covers } (K - 1) \cdot d + 1 \text{ input positions}$$

**Effect:** Increase receptive field without increasing kernel size.

**Example:** $K=3$, $d=2$ samples positions $[0, 2, 4]$ → receptive field of 5 without $5 \times 5$ kernel.

---

## 7. 1×1 Convolutions

$$F = \begin{bmatrix} w \end{bmatrix}$$

**Effect:** Multiply each spatial location by $w$; no weight sharing across space. Channel-wise combination.

**Use cases:**
- Reduce/increase channels without spatial mixing
- Add nonlinearity between spatial operations
- Bottleneck layers (cheaper computation)

**Example:** $1 \times 1$ conv with $C_{\text{in}}=256$, $C_{\text{out}}=64$ reduces channels by 4× with minimal parameters.

---

## 8. Batch Normalization (Brief)

Normalize activations **per batch** before activation function:

$$\hat{h} = \gamma \frac{h - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}} + \beta$$

where $\mu_B, \sigma_B$ are computed over batch.

**Effect:**
- Stabilizes training (allows higher learning rates)
- Reduces internal covariate shift (distribution of layer inputs changes)
- Acts as regularizer (slight randomness from batch statistics)

**Note:** Separate statistics at train vs. test time (exponential moving average used at test).

---

## 9. Exam Questions

### Conceptual
1. Why do Sobel filters detect edges? Explain the math.
2. How do learned kernels differ from hand-crafted ones?
3. Why is a $1 \times 1$ convolution useful despite no spatial mixing?

### Derivation-Based
1. **Compute** parameters in a layer: $K=5$, $C_{\text{in}}=3$, $C_{\text{out}}=64$.
2. **Derive** output spatial dimensions: $H=256$, $K=3$, $P=1$, $S=1$.

### Trick/Failure Cases
1. Filter size $K=1 \times 1$: is this useful for detecting edges?
2. Stride $S=2$: what information is lost compared to $S=1$?

---

## 10. Key Takeaways

- **Kernels detect local patterns:** Edges, textures, shapes (depending on layer depth)
- **Learned kernels** optimized via backprop; automatically discover useful features
- **Parameter count:** $K \times K \times C_{\text{in}} \times C_{\text{out}}$ (grows with kernel size and channel depth)
- **Receptive field:** Increases with depth; needed for global context
- **Stride $S$:** Faster spatial reduction but information loss
- **Dilation $d$:** Larger receptive field without larger kernel
- **1×1 convolution:** Channel mixing without spatial operations
- **Batch normalization:** Stabilizes training; acts as regularizer

---
