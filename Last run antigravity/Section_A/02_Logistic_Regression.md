# 📘 Logistic Regression

## 1. Core Idea (Intuition)

* **Problem it solves:** Binary classification — predict whether an input belongs to class 0 or class 1.
* **Why not just use linear regression for classification?** Linear regression outputs unbounded values (-∞ to +∞). We need probabilities (0 to 1). Also, MSE loss for classification creates a non-convex optimization surface → gets stuck in local minima.
* **Key insight:** Take the linear regression output and squash it through a **sigmoid function** to get a probability. Then use a probability-based loss function (cross-entropy) that is convex.

---

## 2. Mathematical Formulation

**Step 1 — Linear combination (same as linear regression):**
```
z = wᵀx + b
```

**Step 2 — Sigmoid activation:**
```
σ(z) = 1 / (1 + e⁻ᶻ)
```

Properties of sigmoid:
- Output range: (0, 1) — interpretable as probability
- σ(0) = 0.5
- As z → +∞, σ(z) → 1
- As z → -∞, σ(z) → 0
- Derivative: σ'(z) = σ(z)(1 - σ(z)) — this is elegant and makes gradient computation easy

**Prediction:**
```
ŷ = σ(wᵀx + b) = P(y=1 | x)
```

**Decision rule:** Predict class 1 if ŷ ≥ 0.5, else class 0. (Threshold can be adjusted.)

**Loss Function — Binary Cross-Entropy (Log Loss):**

For a single example:
```
L = -[y·log(ŷ) + (1-y)·log(1-ŷ)]
```

For the full dataset:
```
J = -(1/m) Σᵢ₌₁ᵐ [yᵢ·log(ŷᵢ) + (1-yᵢ)·log(1-ŷᵢ)]
```

Where:
- `y` = true label (0 or 1)
- `ŷ` = predicted probability (output of sigmoid)
- `m` = number of examples

**Why this loss?**
- When y=1: loss = -log(ŷ). If ŷ is close to 1, loss ≈ 0. If ŷ is close to 0, loss → ∞. (Heavily penalizes confident wrong predictions.)
- When y=0: loss = -log(1-ŷ). Same logic, flipped.
- This loss is **convex** with respect to w (when combined with sigmoid), so gradient descent converges to global minimum.

**Mathematical justification (MLE connection):**

If we model P(y=1|x) = σ(wᵀx + b), then the likelihood of the entire dataset is:

```
Likelihood = Πᵢ ŷᵢʸⁱ (1-ŷᵢ)⁽¹⁻ʸⁱ⁾
```

Taking negative log:
```
-log(Likelihood) = -Σᵢ [yᵢ log(ŷᵢ) + (1-yᵢ) log(1-ŷᵢ)]
```

This IS the cross-entropy loss. So minimizing cross-entropy = Maximum Likelihood Estimation.

---

## 3. Algorithm / Training Procedure

```
Initialize w = 0 (or small random), b = 0
Set learning rate α, max iterations

Repeat until convergence:
    1. Forward pass:
       z = Xw + b
       ŷ = σ(z)                    # element-wise sigmoid
    
    2. Compute loss:
       J = -(1/m) Σ [y·log(ŷ) + (1-y)·log(1-ŷ)]
    
    3. Compute gradients:
       dJ/dw = (1/m) Xᵀ(ŷ - y)
       dJ/db = (1/m) Σ(ŷ - y)
    
    4. Update:
       w = w - α · dJ/dw
       b = b - α · dJ/db
```

**Gradient derivation:**

For a single example:
```
dL/dz = ŷ - y          (this is surprisingly clean!)
dL/dwⱼ = (ŷ - y) · xⱼ
dL/db = (ŷ - y)
```

Proof:
```
L = -[y·log(ŷ) + (1-y)·log(1-ŷ)]
dL/dŷ = -y/ŷ + (1-y)/(1-ŷ)
dŷ/dz = ŷ(1-ŷ)              # sigmoid derivative

dL/dz = dL/dŷ · dŷ/dz
      = [-y/ŷ + (1-y)/(1-ŷ)] · ŷ(1-ŷ)
      = -y(1-ŷ) + (1-y)ŷ
      = -y + yŷ + ŷ - yŷ
      = ŷ - y ✓
```

Notice: the gradient has the **exact same form** as linear regression (`ŷ - y`), but `ŷ` is computed differently (through sigmoid).

---

## 4. Optimization / Learning Dynamics

* Loss surface is **convex** → gradient descent finds global minimum.
* No closed-form solution (unlike linear regression) — must use iterative optimization.
* **Gradient magnitude:** When the model is very confident AND wrong, gradient is large → fast correction. When the model is uncertain (ŷ ≈ 0.5), gradient is moderate.

**Effect of learning rate:**

| Learning Rate | Behavior |
|---|---|
| Too small | Very slow convergence, might need 100K+ iterations |
| Just right | Converges smoothly in ~100-1000 iterations |
| Too large | Loss oscillates, may diverge |
| Zero | No learning happens |

**Decision boundary:** The set of points where `wᵀx + b = 0` (where σ(z) = 0.5). This is always a **linear boundary** (a line in 2D, a plane in 3D, a hyperplane in nD).

---

## 5. Failure Cases / Limitations

| Failure | Why |
|---|---|
| Non-linearly separable data | Decision boundary is always linear. Can't capture XOR-type patterns. |
| Perfectly separable data | Weights go to ±∞ trying to make sigmoid output exactly 0 or 1. Need regularization. |
| Class imbalance | Model biases toward majority class. Threshold adjustment or resampling needed. |
| Multiclass (>2 classes) | Basic logistic regression is binary. Need One-vs-Rest or Softmax extension. |
| Irrelevant features | Doesn't auto-select features. Performance degrades with noise features (use L1 regularization). |

---

## 6. Where It Works Well

* Binary classification with roughly linearly separable classes
* When you need probability outputs (not just labels)
* Medical diagnosis (probability of disease), spam detection, credit risk
* When interpretability matters (weight = feature importance, sign = direction of effect)
* High-dimensional sparse data (text classification with bag-of-words — logistic regression is surprisingly strong here)
* As a baseline classifier before trying complex models

---

## 7. Variants / Extensions

| Variant | What it does |
|---|---|
| **Multinomial/Softmax Regression** | Extension to K classes. Uses softmax instead of sigmoid. Loss becomes categorical cross-entropy. |
| **Regularized Logistic Regression** | Add L1 or L2 penalty to prevent overfitting and handle perfectly separable data. |
| **Kernel Logistic Regression** | Apply kernel trick for non-linear decision boundaries. |
| **One-vs-Rest (OvR)** | Train K separate binary classifiers for K classes. |

**Softmax extension:**
```
P(y=k | x) = e^(wₖᵀx) / Σⱼ e^(wⱼᵀx)
```
This normalizes outputs to sum to 1 across all K classes.

---

## 8. Comparison Table

| Method | When to Use | Strength | Weakness |
|---|---|---|---|
| Logistic Regression | Binary classification, linear boundary | Probabilistic output, interpretable, convex loss | Can't handle non-linear boundaries |
| Linear Regression (for classification) | Never for classification | — | Non-convex loss, outputs outside [0,1] |
| SVM | Max-margin boundary needed | Better generalization with clear margins | No probability output (without calibration) |
| Decision Tree | Non-linear boundaries, interpretability | Handles non-linearity naturally | Overfits easily, unstable |
| Naive Bayes | Text classification, few samples | Fast, works with little data | Strong independence assumption |

---

## 9. Exam Questions

### Conceptual:
1. Why can't we use MSE loss for logistic regression? What goes wrong with the optimization?
2. Explain the connection between logistic regression and Maximum Likelihood Estimation.
3. What is the decision boundary of logistic regression? Can it ever be non-linear?

### Derivation-based:
4. Derive the gradient of the binary cross-entropy loss with respect to weights. Show that it simplifies to `(1/m) Xᵀ(ŷ - y)`.
5. Show that the derivative of the sigmoid function is `σ(z)(1 - σ(z))`.

### Trick / Failure-case:
6. Your logistic regression weights keep growing to very large values during training and never converge. The training accuracy is 100%. What's happening?
7. You're classifying 95% negative, 5% positive data. Your model predicts all negatives and gets 95% accuracy. Is this good? What metrics should you use instead?

---

## 10. Key Takeaways

* Logistic regression = linear regression + sigmoid. It outputs probabilities, not raw values.
* Uses cross-entropy loss, not MSE. Cross-entropy is convex with sigmoid → guaranteed global minimum.
* The gradient has the same elegant form as linear regression: `(ŷ - y)·x`.
* Decision boundary is always linear. For non-linear boundaries, use feature engineering or switch models.
* Minimizing cross-entropy is equivalent to Maximum Likelihood Estimation.
* Perfectly separable data causes weights to blow up → always use regularization in practice.
* Softmax regression is the multi-class generalization.
* Despite its simplicity, logistic regression is extremely competitive on high-dimensional sparse data (e.g., NLP tasks).
