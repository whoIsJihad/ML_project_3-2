# 📘 Linear Regression

## 1. Core Idea (Intuition)

* **Problem it solves:** Predict a continuous output variable from one or more input features by fitting a straight line (or hyperplane) through the data.
* **Why needed:** Simplest supervised learning model. Establishes the baseline for understanding loss minimization, gradient-based learning, and generalization. Every ML model builds on ideas introduced here.
* **Key insight:** We assume the relationship between inputs and output is approximately linear, and we find the "best" line by minimizing squared errors.

---

## 2. Mathematical Formulation

**Model:**

```
ŷ = w₁x₁ + w₂x₂ + ... + wₙxₙ + b
```

In vector form:

```
ŷ = wᵀx + b
```

Where:
- `x` = input feature vector (n features)
- `w` = weight vector (n learnable parameters)
- `b` = bias (intercept term)
- `ŷ` = predicted output

**Loss Function — Mean Squared Error (MSE):**

```
L = (1/m) Σᵢ₌₁ᵐ (yᵢ - ŷᵢ)²
```

Where:
- `m` = number of training examples
- `yᵢ` = true label for example i
- `ŷᵢ` = predicted value for example i

**Why squared error?**
- Penalizes large errors more than small ones (quadratic penalty)
- Differentiable everywhere → easy to optimize with gradient descent
- Has a unique global minimum (the loss surface is a convex bowl)

**Closed-form solution (Normal Equation):**

```
w* = (XᵀX)⁻¹ Xᵀy
```

Where:
- `X` = design matrix (m × n), each row is one data point
- `y` = target vector (m × 1)
- `w*` = optimal weight vector

**Proof sketch of the Normal Equation:**

We want to minimize `L(w) = ||Xw - y||²`

Expand: `L = (Xw - y)ᵀ(Xw - y) = wᵀXᵀXw - 2wᵀXᵀy + yᵀy`

Take derivative with respect to w and set to zero:

```
dL/dw = 2XᵀXw - 2Xᵀy = 0
→ XᵀXw = Xᵀy
→ w = (XᵀX)⁻¹ Xᵀy
```

This works only if `XᵀX` is invertible (i.e., features are not perfectly collinear).

**Assumptions behind the model:**
1. Linearity: true relationship is approximately linear
2. Independence: training examples are independent of each other
3. Homoscedasticity: variance of errors is constant across all x values
4. No perfect multicollinearity: features are not perfectly correlated

---

## 3. Algorithm / Training Procedure

### Option 1: Closed-form (Normal Equation)
```
1. Construct design matrix X (add column of 1s for bias)
2. Compute w* = (XᵀX)⁻¹ Xᵀy
3. Done. No iterations needed.
```
**Cost:** O(n³) for matrix inversion. Impractical when n (features) > ~10,000.

### Option 2: Gradient Descent
```
Initialize w randomly (or zeros), set learning rate α
Repeat until convergence:
    1. Forward pass: ŷ = Xw
    2. Compute loss: L = (1/m) ||y - ŷ||²
    3. Compute gradient: dL/dw = -(2/m) Xᵀ(y - ŷ)
    4. Update weights: w = w - α * dL/dw
```

**Gradient derivation:**

Starting from `L = (1/m) Σ(yᵢ - wᵀxᵢ)²`

```
dL/dwⱼ = (1/m) Σ 2(yᵢ - wᵀxᵢ)(-xᵢⱼ)
        = -(2/m) Σ (yᵢ - ŷᵢ) xᵢⱼ
```

In matrix form: `dL/dw = -(2/m) Xᵀ(y - Xw)`

---

## 4. Optimization / Learning Dynamics

* **Gradient points toward steepest ascent** → we go opposite direction (descent).
* **Loss surface is a convex paraboloid** → only one minimum, gradient descent will always converge (with proper learning rate).

**Effect of learning rate (α):**

| Learning Rate | Behavior |
|---|---|
| Too small | Converges, but extremely slowly. Thousands of iterations to reach minimum. |
| Just right | Smooth convergence to minimum in reasonable iterations. |
| Too large | Overshoots the minimum. Loss oscillates or diverges. |
| Zero | Weights never update. Model stays at initialization. |

**Convergence check:** Stop when `|L_new - L_old| < ε` (some small threshold).

---

## 5. Failure Cases / Limitations

| Failure | Why |
|---|---|
| Non-linear data | Linear model can't capture curves, polynomials, or complex patterns. Underfits. |
| Outliers | Squared loss amplifies outlier influence. One extreme point can drag the entire line. |
| Multicollinearity | When features are highly correlated, `XᵀX` becomes near-singular → weights become unstable, huge magnitudes. |
| High-dimensional data (n >> m) | More features than data points → infinite solutions, overfitting. Need regularization. |
| Heteroscedastic errors | If error variance changes with x, MSE estimates are unbiased but inefficient. |

---

## 6. Where It Works Well

* Truly linear relationships (price vs. area, temperature vs. ice cream sales)
* When you need an interpretable model (each weight tells you feature importance)
* Low-dimensional data with enough samples
* As a baseline before trying complex models
* Feature engineering can make non-linear data "look" linear (e.g., add x² as a feature → polynomial regression, still linear in parameters)

---

## 7. Variants / Extensions

| Variant | What it does |
|---|---|
| **Ridge Regression (L2)** | Adds `λ||w||²` to loss. Shrinks weights, handles multicollinearity. |
| **Lasso Regression (L1)** | Adds `λ|w|` to loss. Can zero out weights → feature selection. |
| **Elastic Net** | Combines L1 + L2 penalties. |
| **Polynomial Regression** | Add polynomial features (x², x³, x₁x₂). Still "linear" regression in the expanded feature space. |
| **Bayesian Linear Regression** | Treats weights as distributions instead of point estimates. Gives uncertainty in predictions. |

---

## 8. Comparison Table

| Method | When to Use | Strength | Weakness |
|---|---|---|---|
| Linear Regression | Linear relationships, interpretability needed | Simple, fast, closed-form solution exists | Can't model non-linear patterns |
| Polynomial Regression | Curved relationships | Captures non-linearity while staying in linear framework | Overfits with high degree |
| Ridge Regression | Multicollinearity present | Stable weights, prevents overfitting | All features kept (no selection) |
| Lasso Regression | Feature selection needed | Zeros out irrelevant features | Can be unstable with correlated features |
| KNN Regression | No assumption about data shape | Non-parametric, flexible | Slow at inference, curse of dimensionality |

---

## 9. Exam Questions

### Conceptual:
1. Why does linear regression use squared error instead of absolute error? What happens to the loss surface if we use absolute error?
2. Under what conditions does the Normal Equation fail? What's the fix?
3. Why is linear regression considered a "linear model" even when we use polynomial features?

### Derivation-based:
4. Derive the gradient of MSE loss with respect to weights. Show each step.
5. Starting from `L = ||Xw - y||²`, derive the Normal Equation `w* = (XᵀX)⁻¹Xᵀy`.

### Trick / Failure-case:
6. You train a linear regression model and get extremely large weight values (some >10⁶). What's likely happening, and how do you fix it?
7. Your training loss is very low but test loss is very high. Diagnose the issue and propose two different solutions.

---

## 10. Key Takeaways

* Linear regression finds the best straight line through data by minimizing squared error.
* MSE loss is convex → gradient descent always finds the global minimum.
* Normal equation gives exact solution in O(n³) — use it for small feature sets.
* Gradient descent is preferred when n is large (>10K features).
* Outliers destroy linear regression — consider robust alternatives or preprocessing.
* Multicollinearity makes weights unstable → use Ridge/Lasso.
* Adding polynomial features makes it "polynomial regression" but the optimization is still linear regression.
* Always try linear regression first as a baseline — you'd be surprised how often it's competitive.
