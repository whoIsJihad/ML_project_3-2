# CNN Architectures: Quick Summary

## 1. Normal CNN (Baseline)

**What it is:** Basic convolutional neural network with sequential layers

**Structure:**
```
Input → Conv → ReLU → Conv → ReLU → MaxPool → FC → Softmax → Output
```

**Key features:**
- Simple sequential design
- Few parameters (~1M)
- Works okay on simple tasks (MNIST, CIFAR-10)
- Gradients vanish in deep networks (>20 layers)

**Accuracy:** ~90% on CIFAR-10

**Use case:** Educational, baseline comparisons

---

## 2. LeNet-5 (1998)

**What it is:** First successful CNN, designed for digit recognition

**Architecture:**
```
Input (32×32) → Conv(6) → Sigmoid → Pool → Conv(16) → Sigmoid → Pool → 
FC(120) → Sigmoid → FC(84) → Sigmoid → FC(10) → Softmax
```

**Key features:**
- Small network (60K parameters)
- Average pooling (not max)
- Simple but effective
- Proven CNNs work for real tasks

**Accuracy:** 99% on MNIST (groundbreaking!)

**Significance:** Showed CNNs can recognize handwritten digits reliably

**Modern relevance:** Historical interest only (too small for modern tasks)

---

## 3. AlexNet (2012)

**What it is:** Breakthrough network that won ImageNet and started deep learning revolution

**Architecture:**
```
Input (227×227×3) → Conv(11×11,96) → ReLU → Pool → Conv(5×5,256) → ReLU → Pool → 
Conv(3×3,384) → ReLU → Conv(3×3,384) → ReLU → Conv(3×3,256) → ReLU → Pool → 
FC(4096) → ReLU → Dropout → FC(4096) → ReLU → Dropout → FC(1000) → Softmax
```

**Key features:**
- 60 million parameters
- 8 layers deep
- ReLU activation (faster than sigmoid)
- Dropout for regularization
- GPU training (essential for speed)
- Local Response Normalization (now deprecated)

**Accuracy:** 63.3% top-1 on ImageNet (revolutionary!)

**Significance:** Proved deep learning with GPUs beats hand-crafted features

---

## 4. VGG-16 (2014)

**What it is:** Shows that depth + small 3×3 filters = better than large filters

**Architecture:**
```
Input (224×224×3) → [Conv-ReLU-Conv-ReLU-Pool]×2 → [Conv-ReLU-Conv-ReLU-Conv-ReLU-Pool]×3 → 
FC(4096)-ReLU → FC(4096)-ReLU → FC(1000)-Softmax
```

**Key features:**
- 138 million parameters (vs AlexNet's 60M)
- 16 convolutional layers (vs AlexNet's 5)
- All 3×3 filters (uniform design)
- No fancy tricks (pure simplicity)
- Stacked small filters > one large filter (receptive field trade-off)

**Accuracy:** 71.3% top-1 on ImageNet (better than AlexNet!)

**Significance:** Showed depth matters; simple uniform architecture is powerful

**Modern relevance:** Still used as backbone for transfer learning

---

## 5. GoogLeNet/Inception (2014)

**What it is:** Multi-scale parallel feature extraction using Inception modules

**Architecture:**
```
Input → [Conv-ReLU-Pool]×2 → [Inception(3a), Inception(3b)] → Pool → 
[Inception(4a-4e) with ReLU]×5 → Pool → [Inception(5a-5b) with ReLU]×2 → 
FC(1000)-Softmax

(Note: Inception modules internally use ReLU after each Conv operation)
```

**Key features:**
- 6.9 million parameters (20× fewer than VGG!)
- Inception module: 4 parallel branches (1×1, 3×3, 5×5, MaxPool)
- 1×1 bottlenecks for efficiency (8.8× speedup in computation)
- 3 auxiliary classifiers for gradient injection
- Multi-scale feature extraction (captures features at different sizes)

**Accuracy:** 74.8% top-1 on ImageNet (better than VGG with fewer params!)

**Significance:** Efficient architecture beats brute-force depth; parallel ≠ sequential

---

## 6. ResNet (2015)

**What it is:** Skip connections enable training of 150+ layer networks

**Architecture:**
```
Input → Conv-BN-ReLU → [Residual Block]×16-48 → Pool → [Residual Block]×... → 
GlobalAvgPool → FC(1000) → Softmax

Residual Block: x → [Conv-BN-ReLU-Conv-BN] → Add(x) → ReLU → Output
                      └────────skip connection────────┘
```

**Key features:**
- 50-152 layers (ResNet-50, ResNet-101, ResNet-152)
- Skip connections (y = F(x) + x, not just y = F(x))
- Learn residual F(x) = H(x) - x (easier than learning H(x))
- Solves vanishing gradient problem (gradient highway)
- 25.5M (ResNet-50) to 60M parameters
- Works with BatchNorm

**Accuracy:** 77.6% top-1 on ImageNet (ResNet-152, best so far!)

**Significance:** Finally made very deep networks (100+ layers) trainable

**Modern relevance:** Current standard backbone for most computer vision tasks

---

## Quick Comparison Table

| Architecture | Year | Layers | Params | ImageNet Acc | Key Innovation |
|-------------|------|--------|--------|-------------|-----------------|
| LeNet-5 | 1998 | 7 | 60K | 99% (MNIST) | First successful CNN |
| AlexNet | 2012 | 8 | 60M | 63.3% | ReLU + GPU + Dropout |
| VGG-16 | 2014 | 16 | 138M | 71.3% | Depth + small 3×3 filters |
| GoogLeNet | 2014 | 22 | 6.9M | 74.8% | Inception + Multi-scale |
| ResNet-50 | 2015 | 50 | 25.5M | 76.0% | Skip connections |
| ResNet-152 | 2015 | 152 | 60M | 77.6% | Deep networks work! |

---

## Evolution Path

```
LeNet (shallow, specific task)
        ↓
AlexNet (deep, ReLU, GPU, proved deep works)
        ↓
VGG (very deep, uniform design)
        ↓
GoogLeNet (parallel operations, efficiency)
        ↓
ResNet (skip connections, finally solves gradient flow)
        ↓
Modern networks (all use skip connections + BatchNorm)
```

---

## Key Takeaways

1. **LeNet**: Foundation (CNN basics work)
2. **AlexNet**: Revolution (deep learning + GPUs)
3. **VGG**: Depth matters (uniform design, 3×3 filters)
4. **GoogLeNet**: Efficiency matters (smart architecture > more layers)
5. **ResNet**: Gradient flow matters (skip connections solve depth problem)

**Progression pattern:** Each solves a problem from the previous generation!

- LeNet → AlexNet: Use ReLU, GPU, regularization
- AlexNet → VGG: Go deeper with small filters
- VGG → GoogLeNet: Be smart with parallel operations
- GoogLeNet → ResNet: Connect output back to input (skip)

---

## Which One to Use Today?

| Task | Best Choice |
|------|------------|
| Learning CNNs | Start with LeNet/AlexNet, then VGG |
| Production (accuracy) | ResNet-50 or ResNet-101 |
| Production (speed) | MobileNet (not covered here, but ResNet is good baseline) |
| Efficiency | GoogLeNet or MobileNet |
| Transfer learning backbone | ResNet-50 (most popular) |
| Exam answers | Know all 6! Focus on progression |

