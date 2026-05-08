# 📘 Regularization: L1, L2, Dropout

## 1. Core Idea (Intuition)

* **Problem it solves:** Overfitting — model memorizes training data, performs poorly on unseen data.
* **Why it happens:** Too many parameters, not enough data. Model has enough capacity to memorize noise.
* **Key insight:** Regularization constrains the model — makes it simpler or less certain — so it generalizes better. It's a trade-off: bias ↑ slightly, variance ↓ significantly.

---

## 2. Mathematical Formulation

### L2 Regularization (Ridge / Weight Decay)

Add the sum of squared weights to the loss:

```
L_total = L_original + λ · Σ wᵢ²
```

Or equivalently:
```
L_total = L_original + λ · ||w||²
```

Where:
- `L_original` = original loss (MSE, cross-entropy, etc.)
- `λ` = regularization strength (hyperparameter)
- `||w||²` = sum of squares of all weights
- We do NOT regularize biases (only weights)

**Effect on gradient:**
```
∇L_total = ∇L_original + 2λw
```

**Effect on weight update:**
```
w = w - α(∇L_original + 2λw) = w(1 - 2αλ) - α·∇L_original
```

The `(1 - 2αλ)` factor shrinks weights by a fraction each step → "weight decay."

**What it does:** Pushes weights toward zero but never exactly to zero. Keeps all features but with small weights. Smooth penalty — large weights penalized quadratically.

**Proof that L2 prevents large weights:**
- The penalty grows as w² — a weight of 10 costs 100× more than a weight of 1.
- Optimizer settles where marginal decrease in L_original equals marginal increase in penalty.
- Result: weights distribute evenly across features rather than concentrating on few.

### L1 Regularization (Lasso)

Add the sum of absolute weights:

```
L_total = L_original + λ · Σ |wᵢ|
```

**Effect on gradient:**
```
∇L_total = ∇L_original + λ · sign(w)
```
Where `sign(w)` = +1 if w>0, -1 if w<0, 0 if w=0.

**What it does:** Pushes weights toward exactly zero. Many weights become precisely 0 → **automatic feature selection**. The model becomes sparse.

**Why L1 gives exact zeros but L2 doesn't:**
- L2 penalty derivative = `2λw`. As w → 0, penalty gradient → 0. So there's less and less push to zero.
- L1 penalty derivative = `λ·sign(w)`. As w → 0, penalty gradient = ±λ (constant!). Strong push all the way to zero.
- At w=0, L1's subgradient includes 0 → weight can stay at zero if data gradient is small enough.

### Dropout

Not a penalty term — a training technique.

**During training:**
- For each mini-batch, randomly zero out each neuron with probability p (typically p=0.5 for hidden, p=0.2 for input)
- Remaining neurons are scaled by 1/(1-p) to maintain expected output magnitude

```
mask = random_binary(shape=h.shape, prob_keep=1-p)
h_dropped = h * mask / (1-p)
```

**During inference:**
- Use ALL neurons (no dropout)
- No scaling needed (because of the 1/(1-p) during training)

**Why it works:**
- Each neuron can't rely on any particular other neuron being present → forces redundancy
- Effectively trains an ensemble of 2ⁿ sub-networks (where n = neurons) by sharing weights
- Reduces co-adaptation: prevents neurons from only working together in specific combinations

---

## 3. Algorithm / Training Procedure

### L1/L2: Add penalty to loss, compute modified gradient
```
For each mini-batch:
    g = ∇L_original(batch)
    
    # L2:
    g = g + 2λw
    
    # L1:
    g = g + λ·sign(w)
    
    w = w - α·g
```

### Dropout:
```
For each mini-batch (TRAINING):
    For each layer with dropout:
        Generate random mask (keep prob = 1-p)
        h = f(Wx + b)
        h = h * mask / (1-p)       # inverted dropout
    Compute loss and backprop normally

For INFERENCE:
    Use all neurons, no masking, no scaling
```

**Inverted dropout** (scale during training) is the standard — inference stays clean, no modification needed.

---

## 4. Optimization / Learning Dynamics

### L2:
- Makes loss surface more "bowl-shaped" (adds curvature everywhere → helps conditioning)
- High λ → aggressive weight decay → weights approach zero → underfitting
- Low λ → almost no regularization → overfitting
- Sweet spot found via cross-validation

### L1:
- Loss surface has "diamond-shaped" corners → optimizer likely hits a corner where some weights = 0
- Sparse solutions → interpretable models, feature selection
- Non-differentiable at w=0 (need subgradient methods or proximal operators)

### Dropout:
- Training loss is typically HIGHER than without dropout (because we're limiting capacity)
- Validation loss is lower → that's the point
- Training takes longer (each neuron updates less frequently)
- High dropout rate (p>0.5) → too aggressive → underfitting
- Low dropout rate (p<0.1) → barely regularizes

---

## 5. Failure Cases / Limitations

| Method | Failure | Why |
|---|---|---|
| L2 | Can't do feature selection | Never zeros out weights, keeps all features |
| L2 | Too high λ | Weights crushed to near-zero → severe underfitting |
| L1 | Instability with correlated features | Among correlated features, L1 arbitrarily picks one and zeros others |
| L1 | Non-differentiable at 0 | Optimization is trickier |
| Dropout | Increases training time | Convergence slower (each neuron trains less) |
| Dropout | Bad for small networks | Too few neurons → dropping some destroys information |
| Dropout | Not useful for batch norm | BatchNorm provides its own regularization; dropout + BN can conflict |

---

## 6. Where It Works Well

| Method | Best For |
|---|---|
| L2 | Any model prone to overfitting. Default regularization. |
| L1 | When you want feature selection. High-dimensional, sparse data. |
| Elastic Net (L1+L2) | Correlated features + need some selection |
| Dropout | Large neural networks. MLPs, fully-connected layers. |

---

## 7. Variants / Extensions

| Variant | What it does |
|---|---|
| **Elastic Net** | `λ₁|w| + λ₂w²` — combines L1 and L2. Handles correlated features better than L1 alone. |
| **DropConnect** | Drops connections (weights) instead of neurons. |
| **Spatial Dropout** | Drops entire feature maps in CNNs instead of individual pixels. |
| **Early Stopping** | Stop training when validation loss starts increasing. Implicit regularization. |
| **Data Augmentation** | Create more training data by transforming existing data. The best regularization. |
| **Weight Tying** | Force certain weights to be equal. Reduces parameters. |

---

## 8. Comparison Table

| Method | Type | Feature Selection | Effect | Hyperparameter |
|---|---|---|---|---|
| L2 (Ridge) | Weight penalty | No | Shrinks all weights | λ |
| L1 (Lasso) | Weight penalty | Yes (sparse) | Zeros out some weights | λ |
| Dropout | Training technique | No | Trains sub-network ensemble | Drop rate p |
| Early Stopping | Training technique | No | Stops before overfitting | Patience epochs |
| Data Augmentation | Data technique | No | More diverse training data | Augmentation types |

---

## 9. Exam Questions

### Conceptual:
1. Why does L1 produce sparse weights (exact zeros) while L2 doesn't? Explain geometrically or analytically.
2. Explain how dropout acts as an ensemble method. How many sub-networks does it implicitly train?
3. Why do we scale activations by 1/(1-p) during dropout training?

### Derivation-based:
4. Derive the gradient update rule for L2 regularization. Show that it's equivalent to multiplying weights by (1-2αλ) each step (weight decay).
5. For L1, show that the subgradient at w=0 includes 0, which allows weights to stay at exactly zero.

### Trick / Failure-case:
6. You apply dropout with p=0.8 (dropping 80% of neurons) and your model underfits severely. Why? What dropout rate would you try?
7. You trained with L2 regularization and got 70% test accuracy. Switching to L1 gives 65% but with 10× fewer non-zero weights. When is this trade-off worth it?

---

## 10. Key Takeaways

* L2 shrinks all weights (weight decay). L1 zeros out some weights (feature selection). Both fight overfitting.
* L1 produces sparse models because its gradient is constant even as w → 0.
* Dropout randomly disables neurons during training → forces redundancy → implicit ensemble.
* Use inverted dropout (scale by 1/(1-p) during training) so inference needs no modification.
* Too much regularization → underfitting. Find the sweet spot via cross-validation.
* Dropout is for big networks. L2 is the safe default. L1 when you need interpretability/sparsity.
* Early stopping is the laziest but often very effective regularization.
