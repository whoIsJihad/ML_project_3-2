# Regularization & Normalization Techniques: Number-Based Guide

## Quick Overview
These techniques **prevent overfitting** and **stabilize training**:
- **L1/L2**: Penalize large weights
- **Dropout**: Randomly remove neurons
- **Batch Norm**: Normalize layer inputs
- **LRN**: Local normalization (deprecated)

---

## L1 REGULARIZATION (Lasso)

### Concept
Adds penalty proportional to **absolute value** of weights.

```
Total Loss = Data Loss + λ × Σ|weights|
```

### Formula
For a single neuron with weights [0.5, -0.3, 2.0]:
```
L1 penalty = λ × (|0.5| + |-0.3| + |2.0|)
           = λ × (0.5 + 0.3 + 2.0)
           = λ × 2.8
```

### Numerical Example

**Scenario:** Network with 3 weights, λ=0.01

| Scenario | Weights | L1 Penalty | Total Loss |
|----------|---------|-----------|-----------|
| No L1 | [0.5, -0.3, 2.0] | 0 | 5.0 |
| With L1 | [0.5, -0.3, 2.0] | 0.01 × 2.8 = 0.028 | 5.028 |

**What happens during gradient update:**
```
Weight update: w_new = w_old - lr × (gradient + λ × sign(w))

Example: w = 0.5
Gradient from data: -0.1
L1 gradient: λ × sign(0.5) = 0.01 × 1 = 0.01
Total gradient: -0.1 + 0.01 = -0.09
With lr=0.1: w_new = 0.5 - 0.1×(-0.09) = 0.509
```

### Key Effect: Feature Selection
L1 pushes weights to **EXACTLY ZERO** (sparse solutions)

```
Iteration | Weight Value | Gradient | Update |
-----------|-------------|----------|---------|
Initial    | 0.02        | -0.001   | 0.001   |
After 1    | 0.021       | -0.001   | 0.001   |
...        | ...         | ...      | ...     |
After 20   | 0.04        | -0.001   | 0.001   |
After 50   | ZERO!       | λ × sign(0) = 0 | Stops shrinking |
```

### Pros & Cons
✓ Produces sparse weights (some = 0)  
✓ Feature selection (which inputs matter?)  
✓ Interpretable  
✗ Non-differentiable at w=0 (tricky to optimize)

---

## L2 REGULARIZATION (Ridge)

### Concept
Adds penalty proportional to **squared** weights.

```
Total Loss = Data Loss + λ × Σ(weights²)
```

### Formula
For weights [0.5, -0.3, 2.0]:
```
L2 penalty = λ × (0.5² + (-0.3)² + 2.0²)
           = λ × (0.25 + 0.09 + 4.0)
           = λ × 4.34
```

### Numerical Example

**Scenario:** Same network, λ=0.01

| Scenario | Weights | L2 Penalty | Total Loss |
|----------|---------|-----------|-----------|
| No L2 | [0.5, -0.3, 2.0] | 0 | 5.0 |
| With L2 | [0.5, -0.3, 2.0] | 0.01 × 4.34 = 0.0434 | 5.0434 |

**Gradient update with L2:**
```
Weight update: w_new = w_old - lr × (gradient + λ × 2w)

Example: w = 0.5
Gradient from data: -0.1
L2 gradient: λ × 2 × 0.5 = 0.01 × 2 × 0.5 = 0.01
Total gradient: -0.1 + 0.01 = -0.09
With lr=0.1: w_new = 0.5 - 0.1×(-0.09) = 0.509
```

### Key Effect: Weight Decay
L2 **shrinks all weights gradually**, never to exactly zero.

```
Starting weight: 5.0, λ=0.1, lr=0.1

Iteration | Weight | L2 Gradient | Update | New Weight |
-----------|--------|------------|--------|-----------|
0          | 5.0    | 0.1×2×5 = 1.0 | -0.1×1 = -0.1 | 4.9 |
1          | 4.9    | 0.1×2×4.9 = 0.98 | -0.098 | 4.802 |
2          | 4.802  | 0.1×2×4.802 = 0.960 | -0.096 | 4.706 |
...        | ...    | ...        | ...    | ...     |
∞          | →0     | →0         | →0     | 0       |
```

Weight shrinks exponentially (never quite zero).

### L1 vs L2 Comparison

```
Weight value over iterations:

L1 (sharp drop to zero):  5.0 → 4.5 → 4.0 → ... → 1.0 → 0.0 → 0.0 → 0.0
                          (linear decay, then stops)

L2 (smooth decay):        5.0 → 4.9 → 4.8 → 4.7 → 4.6 → ... → 0.05 → 0.049
                          (exponential decay, approaches zero)
```

### Pros & Cons
✓ Differentiable everywhere  
✓ Smoother optimization  
✓ Prevents extreme weights  
✓ "Weight decay" connection  
✗ Doesn't force weights to zero (less sparse)

---

## DROPOUT

### Concept
During training: **randomly set neurons to 0** with probability p (usually 0.5)  
During testing: use all neurons (but scale them down by 1-p)

### Numerical Example

**Network with 4 neurons, dropout p=0.5:**

```
Forward pass during TRAINING:

Forward activation: [2.0, 3.0, 1.5, 4.0]
Random mask (50%): [0, 1, 0, 1]
After dropout: [0, 3.0, 0, 4.0]
Scaled (÷0.5): [0, 6.0, 0, 8.0] ← Passed to next layer
```

Why scale? Without scaling, expected value would be half at test time.

```
Forward pass during TESTING:

Forward activation: [2.0, 3.0, 1.5, 4.0]
No dropout, scale by (1-p): [2.0×0.5, 3.0×0.5, 1.5×0.5, 4.0×0.5]
Result: [1.0, 1.5, 0.75, 2.0] ← Consistent with training expectation
```

### Dropout Effect: Ensemble Learning

Dropout is equivalent to training multiple networks!

```
With p=0.5 and 4 neurons, we have 2^4 = 16 possible sub-networks:

Network 1 (mask: 0001): Neurons [4] only
Network 2 (mask: 0010): Neurons [3] only
Network 3 (mask: 0011): Neurons [3,4] only
...
Network 16 (mask: 1111): All neurons [0,1,2,3]

Training = ensemble of all possible sub-networks
Testing = average prediction (all neurons used)
```

### Different Dropout Rates

| Dropout Rate | Effect | Use Case |
|---------|--------|----------|
| 0% | No dropout | Underfitting, fast training |
| 25% | Light dropout | Small models, regularization light |
| 50% | Standard | Most CNNs (AlexNet, VGG) |
| 75% | Heavy dropout | Large fully-connected layers |

### Numerical Intuition

**Before dropout:** 1000 neurons learning specific patterns (overfitting)  
**With dropout p=0.5:** Average ~500 neurons active, can't rely on co-adaptation  
**Result:** Forces learning of robust, independent features

---

## BATCH NORMALIZATION (BatchNorm)

### Concept
Normalize each batch of data to have **mean=0, std=1**, then learn to scale/shift it.

```
x_norm = (x - batch_mean) / sqrt(batch_var + ε)
y = γ × x_norm + β

Where γ,β are learnable parameters
```

### Numerical Example

**Batch of 8 activation values from same neuron:**

```
Raw activations: [1.2, 2.1, 0.8, 3.0, 1.5, 2.3, 0.9, 1.8]

Step 1: Calculate mean and variance
Mean = (1.2+2.1+0.8+3.0+1.5+2.3+0.9+1.8) / 8 = 1.7
Variance = [(1.2-1.7)² + (2.1-1.7)² + ... ] / 8 = 0.7275

Step 2: Normalize
x_norm = (x - 1.7) / sqrt(0.7275 + 1e-5)
       = (x - 1.7) / 0.853

Normalized:
(1.2-1.7)/0.853 = -0.586
(2.1-1.7)/0.853 = 0.468
(0.8-1.7)/0.853 = -1.054
(3.0-1.7)/0.853 = 1.524
(1.5-1.7)/0.853 = -0.234
(2.3-1.7)/0.853 = 0.703
(0.9-1.7)/0.853 = -0.938
(1.8-1.7)/0.853 = 0.117

Normalized batch: [-0.586, 0.468, -1.054, 1.524, -0.234, 0.703, -0.938, 0.117]
Mean ≈ 0, Std ≈ 1 ✓
```

**Step 3: Scale and shift (learned)**
```
If γ=2.0, β=0.5:
y = 2.0 × [-0.586, 0.468, -1.054, 1.524, -0.234, 0.703, -0.938, 0.117] + 0.5
  = [-1.172, 1.436, -2.108, 3.548, -0.468, 1.906, -1.876, 0.734] + 0.5
  = [-0.672, 1.936, -1.608, 4.048, 0.032, 2.406, -1.376, 1.234]
```

### BatchNorm Effects

**Before BatchNorm (Internal Covariate Shift):**
```
Layer 1 output: [0.1, 100.2, 50.3, 2000.1, ...]
                ↓ Very different scales!
Layer 2 input: expects normalized values, gets extreme values
→ Gradients explode or vanish, training is unstable
```

**After BatchNorm:**
```
Layer 1 output: [0.1, 100.2, 50.3, 2000.1, ...]
                ↓
BatchNorm: [-0.586, 0.468, ..., 0.117]  ← Normalized!
                ↓
Layer 2 input: receives stable, normalized values
→ Faster training, more stable gradients
```

### Training vs Testing

| Phase | What Happens | Mean/Variance |
|-------|--------------|---------------|
| **Training** | Normalize using current batch stats | Batch mean/var (changes each batch) |
| **Testing** | Normalize using running mean/var | Exponential moving average from training |

Example moving average calculation:
```
Training step 1: batch_mean = 1.7 → running_mean = 1.7
Training step 2: batch_mean = 1.9 → running_mean = 0.99×1.7 + 0.01×1.9 = 1.702
Training step 3: batch_mean = 1.6 → running_mean = 0.99×1.702 + 0.01×1.6 = 1.7008
...
Testing: use final running_mean ≈ 1.70
```

### BatchNorm Benefits

✓ **Faster training** (higher learning rates work)  
✓ **Less sensitive** to weight initialization  
✓ **Regularization effect** (acts like dropout)  
✓ **Reduced internal covariate shift**

### Problem: Batch Size Matters
```
Small batch (size=2): Noisy batch statistics, high variance in normalization
Large batch (size=512): Stable batch statistics, but requires more memory

Typical: batch size 32-256 for CNNs
```

---

## LOCAL RESPONSE NORMALIZATION (LRN)

### Concept
Normalize each neuron's activation using its **neighboring feature maps** in the same spatial location.

```
b[i,x,y] = a[i,x,y] / (k + α × Σ(a[c,x,y]²))

Where sum is over nearby feature maps c ∈ [i-r, i+r]
```

### Numerical Example

**Output of Conv layer at location (x,y) across 5 feature maps:**

```
Activations: [1.0, 2.0, 3.0, 2.5, 0.5]

LRN normalization with:
- radius r=2 (look at neighbors)
- α=0.01, k=1

For feature map i=1 (value 2.0):
Neighbors: feature maps 0,1,2 (i±r=1±2, but clipped)
Sum of squares: 1.0² + 2.0² + 3.0² = 1 + 4 + 9 = 14
Denominator: k + α × 14 = 1 + 0.01 × 14 = 1.14

Normalized: 2.0 / 1.14 = 1.754
```

### LRN Effect

**Before LRN:**
```
Feature maps: [1.0, 2.0, 3.0, 2.5, 0.5]
Large values (3.0) dominate completely
```

**After LRN:**
```
Normalized:
  1.0/1.14 = 0.877
  2.0/1.14 = 1.754
  3.0/1.14 = 2.632  ← Still large, but competing features are boosted
  2.5/1.14 = 2.193
  0.5/1.14 = 0.439
```

### LRN vs BatchNorm

| Feature | LRN | BatchNorm |
|---------|-----|-----------|
| **Method** | Local neighborhood norm | Full batch norm |
| **Speed** | Slower (complex computation) | Faster (simple) |
| **Memory** | Lower | Slightly higher |
| **Effectiveness** | Modest improvement | Large improvement |
| **Current use** | DEPRECATED (unused) | EVERYWHERE (ResNet, DenseNet, etc.) |

**Why LRN is dead:**
- BatchNorm is simpler and works better
- AlexNet used LRN, but modern networks don't bother

---

## ADDITIONAL TECHNIQUES

### WEIGHT DECAY (Connection to L2)

Weight decay in SGD: `w = w - lr × gradient - lr × λ × w`

This is equivalent to L2 regularization!

```
Example: w=1.0, λ=0.01, lr=0.1
Standard: w_new = 1.0 - 0.1 × 0 = 1.0 (no gradient)
With L2: w_new = 1.0 - 0.1 × (0 + 0.01×2×1.0) = 1.0 - 0.002 = 0.998
```

### DATA AUGMENTATION (Implicit Regularization)

Artificially increase training data by transformations:

```
Original image: 224×224 RGB photo of cat

Augmented versions:
1. Rotated 15° → same label
2. Flipped horizontally → same label
3. Cropped 90% → same label
4. Color jittered → same label
5. Brightness adjusted → same label
...
100 variations from 1 image
```

Effect: Network can't memorize specific images → generalizes better

### EARLY STOPPING

Stop training when validation loss stops improving.

```
Epoch | Train Loss | Val Loss | Action |
-------|-----------|----------|--------|
1     | 2.5       | 2.4      | Continue |
2     | 2.2       | 2.1      | Continue |
3     | 1.9       | 1.85     | Continue |
4     | 1.7       | 1.75     | Continue |
5     | 1.5       | 1.78     | OVERFITTING DETECTED |
6     | 1.3       | 1.82     | ← Stop here! Use weights from epoch 4 |
7     | 1.1       | 1.90     |         |
```

### GRADIENT CLIPPING

Prevent exploding gradients by capping gradient magnitude.

```
Gradient: [-1000, 2000, 1500]
Max norm: 1000

Gradient norm = sqrt(1000²+2000²+1500²) = 2500

Scale factor = 1000/2500 = 0.4

Clipped: [-1000×0.4, 2000×0.4, 1500×0.4]
       = [-400, 800, 600]
       
Now safe to apply!
```

---

## COMPARISON TABLE

| Technique | What It Does | Lambda/Rate | Effect Size | Computational Cost |
|-----------|------------|------------|------------|------------------|
| L1 | Sparse weights | 0.001-0.1 | Medium | Very low |
| L2 | Smooth weight decay | 0.001-0.1 | Medium | Very low |
| Dropout | Remove neurons | 0.3-0.5 | High | Low |
| BatchNorm | Normalize activations | fixed | Very high | Medium |
| LRN | Local competition | fixed | Low | High |

---

## Exam Cheat Sheet

### L1 vs L2
- **L1**: Sparse, some weights → ZERO exactly
- **L2**: Smooth decay, weights → 0 gradually
- **L2 is used more** (differentiable everywhere)

### Dropout
- **During training**: p% neurons randomly zeroed
- **During testing**: all neurons used, scaled by (1-p)
- **Effect**: Ensemble of sub-networks

### BatchNorm
- **Normalizes each layer's input** (mean=0, var=1)
- **Learns scale (γ) and shift (β)** parameters
- **Internal covariate shift** prevention
- **Training vs Testing**: Training uses batch stats, testing uses running average

### LRN
- **Old technique** (AlexNet), **DEPRECATED now**
- Normalize using neighboring feature maps
- **Replaced by BatchNorm** (simpler, better)

---

## Quick Decision Guide

**Choose based on your problem:**

```
Are you overfitting?
├─ Yes → Use dropout (p=0.5) + L2 (λ=0.01)
└─ No → Might need more data

Is your network deep (>20 layers)?
├─ Yes → MUST use BatchNorm
└─ No → Optional but recommended

Is training unstable?
├─ Yes → Add BatchNorm or gradient clipping
└─ No → You're fine

Do you care about model interpretability?
├─ Yes → Use L1 (feature selection)
└─ No → Use L2 (smoother)
```

---

## Numerical Summary

| Technique | Typical Hyperparameter | Effect Per Example |
|-----------|----------------------|------------------|
| L1, λ=0.01 | weight=[1.0] | +0.01 penalty |
| L2, λ=0.01 | weight=[1.0] | +0.0001 penalty |
| Dropout, p=0.5 | 1000 neurons | ~500 active |
| BatchNorm | any | mean→0, std→1 |
| LRN, r=2 | 5 feature maps | divide by ~1.14 |

These are the **fundamental building blocks** of modern deep learning!
