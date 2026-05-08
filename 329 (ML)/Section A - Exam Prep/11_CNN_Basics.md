# 📘 CNN Basics
![[Pasted image 20260424230853.png]]
## 1. Core Idea (Intuition)

**Fully connected layers** don't work well for images:
- 224×224×3 image = 150K parameters per neuron in first hidden layer
- Cannot capture spatial structure (pixel $[i, j]$ is far from $[i+1, j+1]$ in vector)

**Convolutional Neural Networks (CNN)** exploit **spatial locality** and **translational invariance**:
- Use small filters that slide across image
- Share weights (same filter applied everywhere)
- Result: fewer parameters, captures local patterns

---

## 2. Convolution Operation

### 1D Convolution (for intuition)

Input signal: $x = [x_1, x_2, x_3, x_4, x_5]$

Filter (kernel): $w = [w_1, w_2, w_3]$

Output at position $i$:
$$y_i = w_1 x_i + w_2 x_{i+1} + w_3 x_{i+2}$$

**All positions use the same $w$** (weight sharing).

### 2D Convolution (for images)

Input: $X \in \mathbb{R}^{H \times W \times C}$ (height, width, channels)

Filter: $F \in \mathbb{R}^{K \times K \times C}$ (kernel size $K \times K$)

Output at position $(i, j)$:
$$Y_{i,j} = \sum_{a=0}^{K-1} \sum_{b=0}^{K-1} \sum_{c=0}^{C-1} X_{i+a, j+b, c} \cdot F_{a, b, c} + b$$

where $b$ is the bias.

**Interpretation:** Dot product of filter with $K \times K$ patch of input.

### Output Dimensions

Number of output positions:
$$H' = \frac{H - K + 2P}{S} + 1$$
$$W' = \frac{W - K + 2P}{S} + 1$$

where:
- $K$: kernel size
- $P$: padding (zeros added around input)
- $S$: stride (step size of filter)

**Example:** $H=224$, $K=3$, $P=1$, $S=1$ → $H' = \frac{224 - 3 + 2}{1} + 1 = 224$ (same size)

---

## 3. Layer Types in CNN

### Convolutional Layer
$$Y^{(l)} = \sigma(X^{(l-1)} * F^{(l)} + b^{(l)})$$

where $*$ denotes convolution, $\sigma$ is activation (ReLU).

**Parameters:** $K \times K \times C_{\text{in}} \times C_{\text{out}}$ (number of filters $C_{\text{out}}$)

### Pooling Layer
Reduce spatial dimensions by summarizing regions.

#### Max Pooling
$$\text{MaxPool}(X) = \max_{(i,j) \in \text{window}} X_{i,j}$$

**Effect:** Extract dominant feature from each region; invariant to small translations.

#### Average Pooling
$$\text{AvgPool}(X) = \text{mean}_{(i,j) \in \text{window}} X_{i,j}$$

**Use:** Less common; smoother information loss.

### Fully Connected (Dense) Layer
Flatten spatial dimensions; apply standard neural network layer.

$$Y = \sigma(X_{\text{flat}} \mathbf{W} + \mathbf{b})$$

---

## 4. Architecture Pattern

Typical CNN architecture:

```
Input Image
     ↓
[Conv → ReLU → MaxPool] × 2-4 (feature extraction)
     ↓
Flatten
     ↓
[Dense → ReLU] × 1-2 (classification)
     ↓
Output (softmax for multi-class)
```

**Why this pattern?**
- **Convolutional layers:** Extract spatial patterns (edges, textures, shapes)
- **Pooling layers:** Reduce dimensionality; add invariance
- **Dense layers:** Learn non-linear combinations of features

---

## 5. Advantages of Convolution

| Property | Benefit |
|----------|---------|
| **Weight sharing** | Fewer parameters; same filter detects pattern anywhere |
| **Local connectivity** | Exploits spatial structure; nearby pixels correlated |
| **Translation invariance** | Detecting edge is same whether at position (10, 20) or (50, 80) |
| **Computational efficiency** | $\mathcal{O}(H \cdot W \cdot K^2)$ vs. dense $\mathcal{O}(H \cdot W \cdot H \cdot W)$ |

---

## 6. Failure Cases / Limitations

| Problem | Why | Impact |
|---------|-----|--------|
| **Assumes spatial structure** | Works only for grid-like data (images, videos) | Fails for graphs, text (see attention models) |
| **Loss of information** | Pooling discards spatial details | May miss small objects |
| **Limited receptive field** | Early layers see only small patches | Needs many layers for global context |

---

## 7. Exam Questions

### Conceptual
1. Why do CNNs need fewer parameters than fully connected networks for images?
2. What is weight sharing? Why does it make sense for images?
3. What does max pooling do? Is it learnable?

### Derivation-Based
1. **Compute** output dimensions $H'$ for input $H=256$, kernel $K=5$, padding $P=2$, stride $S=2$.
2. **Count** parameters in a convolutional layer: $C_{\text{in}}=3$, $C_{\text{out}}=32$, $K=3$.

### Trick/Failure Cases
1. A CNN trained on 32×32 images performs poorly on 64×64 images (different dataset). Why?
2. Filter size $K=1$: is this useful? What does it compute?

---

## 8. Key Takeaways

- **Convolution:** Slide filter across input; compute dot product at each position
- **Weight sharing:** Same filter applied everywhere; reduces parameters
- **Output size:** $\frac{H - K + 2P}{S} + 1$
- **Pooling:** Reduces spatial dimensions; max-pooling is standard
- **Architecture:** Conv layers for features, pooling for dimensionality, dense for classification
- **Efficiency:** Convolution $O(HW K^2)$ much cheaper than dense $O(H^2W^2)$
- **Translation invariance:** Same pattern detected regardless of position

---
