# 📘 CNN Architectures (LeNet, AlexNet, VGG, GoogLeNet, ResNet)

## 1. Core Idea (Intuition)

Different CNN architectures explore different design choices:
- **Depth:** How many layers?
- **Width:** How many filters per layer?
- **Connections:** Skip connections? Parallel branches?
- **Efficiency:** Fewer parameters?

This section covers influential architectures and their innovations.

---

## 2. LeNet (1998)

### Architecture
```
Input (32×32×1)
  ↓
Conv (6 filters, 5×5) → ReLU
  ↓
MaxPool (2×2)
  ↓
Conv (16 filters, 5×5) → ReLU
  ↓
MaxPool (2×2)
  ↓
Flatten → Dense (120) → ReLU
  ↓
Dense (84) → ReLU
  ↓
Dense (10) → Softmax (output)
```

### Key Points
- **First successful CNN** for digit recognition (MNIST)
- **Shallow:** Only 2 conv layers
- **Small inputs:** 32×32 images
- **Why it worked:** Exploited spatial structure of images

### Limitations
- Cannot handle larger, more complex images
- No regularization techniques (batch norm, dropout)

---

## 3. AlexNet (2012)

### Architecture
```
Input (227×227×3)
  ↓
Conv (96 filters, 11×11, stride=4) → ReLU + MaxPool (3×3)
  ↓
Conv (256 filters, 5×5, pad=2) → ReLU + MaxPool (3×3)
  ↓
Conv (384 filters, 3×3)
  ↓
Conv (384 filters, 3×3)
  ↓
Conv (256 filters, 3×3) → ReLU + MaxPool (3×3)
  ↓
Flatten → Dense (4096) → ReLU + Dropout(0.5)
  ↓
Dense (4096) → ReLU + Dropout(0.5)
  ↓
Dense (1000) → Softmax
```

### Innovations
- **Depth:** 5 conv layers (vs. 2 in LeNet); very deep for the time
- **GPU computing:** First to leverage GPU; trained on 2 GPUs in parallel
- **ReLU:** Instead of sigmoid/tanh; faster and no vanishing gradients
- **Dropout:** Regularization to prevent overfitting
- **Data augmentation:** Image crops, flips to increase effective training set

### Impact
- **ImageNet competition:** Won by large margin (top-5 error: 15% vs. 26% baseline)
- **Sparked deep learning era:** Proved CNNs could scale to large images

### Limitations
- Large models (60M parameters); hard to train without GPU
- First conv layer: very large filters (11×11) seem wasteful

---

## 4. VGG (2014)

### Architecture
**VGG-16 (16 weighted layers):**

```
Input (224×224×3)
  ↓
[Conv (64, 3×3) × 2] → MaxPool
  ↓
[Conv (128, 3×3) × 2] → MaxPool
  ↓
[Conv (256, 3×3) × 3] → MaxPool
  ↓
[Conv (512, 3×3) × 3] → MaxPool
  ↓
[Conv (512, 3×3) × 3] → MaxPool
  ↓
Flatten → Dense (4096) × 2 → Dense (1000)
```

### Key Points
- **Simplicity:** All conv layers $3 \times 3$ filters (no $11 \times 11$ or $5 \times 5$)
- **Stacking:** Two small filters cover same receptive field as one large filter, but fewer parameters
- **Depth:** VGG-19 (19 layers) also proposed

### Analysis
$$\text{Two } 3 \times 3 \text{ filters} = (3-1)^2 \times 2 = 8 \text{ weights per channel}$$
$$\text{One } 5 \times 5 \text{ filter} = (5-1)^2 = 16 \text{ weights per channel}$$

Stacking $3 \times 3$ filters is **more efficient** than single large filters.

### Limitations
- Large number of parameters (138M for VGG-16)
- High memory usage (hard to train)
- Slow inference (many conv layers)

---

## 5. GoogLeNet / Inception (2014)

### Key Innovation: Inception Module

**Problem:** Which kernel size to use in a layer? 1×1, 3×3, or 5×5?

**Solution:** Use all of them in parallel!

```
Input
  ├→ Conv (1×1) → ReLU
  ├→ Conv (3×3) after 1×1 reduction → ReLU
  ├→ Conv (5×5) after 1×1 reduction → ReLU
  └→ MaxPool (3×3) → Conv (1×1) → ReLU
           ↓
      Concatenate outputs (depth-wise)
```

### Why This Works
- **Different filter sizes** capture features at different scales
- **Parallel computation** efficient (modern GPUs)
- **1×1 convolutions** reduce channels before larger convolutions (bottleneck)

### Full Architecture
- Multiple Inception modules stacked
- **Auxiliary classifiers:** Loss computed at intermediate layers (gradient flow)
- **Global average pooling:** Instead of flatten + dense (reduces parameters)

### Parameters
- 22 layers deep
- **12M parameters** (10× fewer than VGG-16)
- Better performance than VGG with fewer parameters

### Limitations
- More complex design (harder to implement, understand)
- Multiple hyperparameters to tune (channel reduction ratios)

---

## 6. ResNet (2015)

### Key Innovation: Residual Connections (Skip Connections)

**Problem:** Very deep networks suffer from vanishing gradients; training doesn't improve beyond ~20-30 layers.

**Solution:** Add skip connections:

$$\mathbf{y} = F(\mathbf{x}) + \mathbf{x}$$

where $F(\mathbf{x})$ is a sequence of layers (conv, norm, activation).

**If $F(\mathbf{x}) \approx 0$, then $\mathbf{y} \approx \mathbf{x}$ (identity).**

### Why It Works
- **Gradient flow:** $\frac{\partial L}{\partial \mathbf{x}} = \frac{\partial L}{\partial \mathbf{y}} \cdot \frac{\partial \mathbf{y}}{\partial \mathbf{x}} = \frac{\partial L}{\partial \mathbf{y}} \cdot (1 + \frac{\partial F}{\partial \mathbf{x}})$
- The "+1" term ensures gradient flows even if $\frac{\partial F}{\partial \mathbf{x}}$ is small
- Solves vanishing gradient problem

### Architecture (ResNet-50)

```
Input (224×224×3)
  ↓
Conv (64, 7×7, stride=2) → BatchNorm → ReLU → MaxPool
  ↓
[Residual Block × 3]  (64 filters)
  ↓
[Residual Block × 4]  (128 filters)
  ↓
[Residual Block × 6]  (256 filters)
  ↓
[Residual Block × 3]  (512 filters)
  ↓
Global Average Pooling
  ↓
Dense (1000) → Softmax
```

Each residual block:
```
Input (x)
  ├→ Conv (1×1) to reduce channels
    ├→ Conv (3×3)
    └→ Conv (1×1) to restore channels
         ↓
    Add with x (skip connection)
         ↓
    ReLU → Output
```

### Impact
- **Very deep networks possible:** ResNet-152 (152 layers) with better performance than ResNet-50
- **Simplified architecture:** Removed auxiliary classifiers (skip connections solve gradient problem)
- **Standard baseline:** ResNet-50 is default architecture for transfer learning

### Variants
| Variant | Layers | Parameters | Use |
|---------|--------|------------|-----|
| ResNet-18 | 18 | 11M | Small, fast |
| ResNet-34 | 34 | 21M | Fast |
| ResNet-50 | 50 | 25M | Default (good balance) |
| ResNet-101 | 101 | 44M | High accuracy |
| ResNet-152 | 152 | 60M | Best accuracy, slow |

---

## 7. Comparison Table

| Architecture | Year | Depth | Parameters | Top-5 Error | Key Innovation |
|-------------|------|-------|-----------|------------|-----------------|
| **LeNet** | 1998 | 2 | 0.06M | N/A | First CNN |
| **AlexNet** | 2012 | 5 | 60M | 15% | GPU training, ReLU, Dropout |
| **VGG-16** | 2014 | 16 | 138M | 7.3% | Simple 3×3 stacking |
| **GoogLeNet** | 2014 | 22 | 12M | 6.7% | Inception module |
| **ResNet-50** | 2015 | 50 | 25M | 5.5% | Skip connections |

---

## 8. Modern Trends

### Efficiency
- **MobileNets:** Depthwise separable convolutions; optimized for mobile
- **EfficientNet:** Systematic scaling of depth, width, resolution

### Attention
- **Vision Transformer (ViT):** Replace convolution with self-attention
- **Hybrid models:** Convolution + attention

---

## 9. Exam Questions

### Conceptual
1. Why did AlexNet succeed where previous methods failed?
2. Explain the Inception module. Why use multiple filter sizes in parallel?
3. What problem does ResNet solve? Why does the skip connection help?

### Derivation-Based
1. **Count** parameters in VGG-16 (approximately). List layer sizes.
2. **Compare** two $3 \times 3$ convolutions vs. one $5 \times 5$ convolution. Which is more efficient?

### Trick/Failure Cases
1. Stacking 2 filters of size $3 \times 3$ has same receptive field as 1 filter of size $5 \times 5$. Why use 2?
2. A 100-layer CNN without skip connections trains poorly. Why? What fixes it?

---

## 10. Key Takeaways

- **LeNet:** First CNN; simple, effective for MNIST
- **AlexNet:** Deep (5 layers), GPU training, ReLU, Dropout; ImageNet breakthrough
- **VGG:** Simplicity (all $3 \times 3$); stacking is more efficient than large filters
- **Inception:** Parallel branches with different filter sizes; efficient depth
- **ResNet:** Skip connections enable very deep networks (50-152 layers); solves vanishing gradients
- **Architecture progression:** Depth first (VGG) → efficiency (Inception) → gradients (ResNet)
- **Modern:** Attention, efficiency, hybrid approaches gaining popularity

---
