# 📘 Linear Regression

## 1. Core Idea (Intuition)

Linear regression finds a **linear relationship** between features $X$ and target $y$. The goal: minimize prediction error.

**Why it's needed:**
- Baseline supervised learning method
- Interpretable (see coefficients directly)
- Fast to train
- Foundation for understanding loss, optimization, gradients

---

## 2. Mathematical Formulation

### Model
$$\hat{y} = X\mathbf{w} + b$$

where:
- $X \in \mathbb{R}^{n \times d}$: feature matrix ($n$ samples, $d$ features)
- $\mathbf{w} \in \mathbb{R}^{d}$: weight vector
- $b \in \mathbb{R}$: bias (often absorbed into $\mathbf{w}$ by augmenting $X$ with a column of 1s)
- $\hat{y} \in \mathbb{R}^{n}$: predictions

### Loss Function (Mean Squared Error)

**Two equivalent forms:**

**Form 1 (Vector notation):**
$$L(\mathbf{w}) = \frac{1}{2n} \|X\mathbf{w} - y\|^2$$

**Form 2 (Explicit summation):**
$$L(\mathbf{w}) = \frac{1}{2n} \sum_{i=1}^{n} (x_i^T\mathbf{w} - y_i)^2$$

**Why two forms?** They're **mathematically identical**. Form 1 is compact (used in theory/derivations). Form 2 makes explicit that we sum over all samples.

**Why divide by $2n$?**
- Divide by $n$: average per sample (not cumulative; scales with dataset size)
- Divide by 2: simplifies derivative (factor of 2 cancels)

---

### Example of Both Forms

**Concrete data:**
- 3 samples: $X = \begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{bmatrix}$, $y = \begin{bmatrix} 5 \\ 11 \\ 17 \end{bmatrix}$
- Guess weights: $\mathbf{w} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$

**Using Form 2 (sum notation):**

Predictions:
- Sample 1: $x_1^T\mathbf{w} = [1, 2] \cdot [1, 2] = 1 + 4 = 5$
- Sample 2: $x_2^T\mathbf{w} = [3, 4] \cdot [1, 2] = 3 + 8 = 11$
- Sample 3: $x_3^T\mathbf{w} = [5, 6] \cdot [1, 2] = 5 + 12 = 17$

Errors: $(5-5)^2 + (11-11)^2 + (17-17)^2 = 0 + 0 + 0 = 0$

$$L(\mathbf{w}) = \frac{1}{2 \cdot 3}(0) = 0$$

**Using Form 1 (vector notation):**

$$X\mathbf{w} = \begin{bmatrix} 5 \\ 11 \\ 17 \end{bmatrix}, \quad X\mathbf{w} - y = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$$

$$\|X\mathbf{w} - y\|^2 = 0^2 + 0^2 + 0^2 = 0$$

$$L(\mathbf{w}) = \frac{1}{6} \cdot 0 = 0$$

Both give the same result! ✓

---

## 3. Closed-Form Solution (Normal Equations)

### Derivation
To find optimal $\mathbf{w}$, take derivative w.r.t. $\mathbf{w}$ and set to zero:

$$\frac{\partial L}{\partial \mathbf{w}} = \frac{1}{n} X^T(X\mathbf{w} - y) = 0$$

$$X^TX\mathbf{w} = X^Ty$$

$$\mathbf{w}^* = (X^TX)^{-1}X^Ty$$

**Assumptions:**
- $X^TX$ must be **invertible** (full column rank)
- If not invertible: use pseudoinverse or regularization

**Why this is optimal:** Setting the gradient to zero gives the minimum (since loss is convex). This solution is **unique** if $X^TX$ is invertible.

---

## 4. Algorithm / Training Procedure

### Method 1: Closed-Form (Direct)
```
Input: X, y
Output: w*

1. Compute (X^T X)^{-1}
2. Compute (X^T X)^{-1} X^T y
3. Return w*
```

**Complexity:** $O(d^3)$ for matrix inversion

### Method 2: Gradient Descent (Iterative)

**Batch Gradient Descent (BGD) — Optimize TOTAL LOSS:**
```
Input: X, y, learning_rate α, iterations T
Output: w

1. Initialize w = 0 (or random)
2. For t = 1 to T:
   a. Compute gradient using ALL samples:
      g = (1/n) X^T(Xw - y)
   b. Update: w ← w - α·g
3. Return w
```

**Use case:** Small to medium datasets (can afford to process all samples per iteration)

**Complexity per step:** $O(nd)$

---

**Stochastic Gradient Descent (SGD) — Optimize SINGLE SAMPLE LOSS:**
```
Input: X, y, learning_rate α, iterations T
Output: w

1. Initialize w = 0 (or random)
2. For t = 1 to T:
   a. Pick random sample i
   b. Compute gradient using only sample i:
      g = x_i(x_i^T w - y_i)
   c. Update: w ← w - α·g
3. Return w
```

**Single sample loss:** $L_i(\mathbf{w}) = (x_i^T\mathbf{w} - y_i)^2$

**Use case:** Large datasets (much faster per iteration; noisier updates)

**Complexity per step:** $O(d)$ (process one sample only)

---

**Mini-batch Gradient Descent (Compromise):**
```
For each batch B ⊂ {1, ..., n} of size b:
  g = (1/b) Σ_{i∈B} x_i(x_i^T w - y_i)
  w ← w - α·g
```

**Balances:** Speed (SGD) + stability (BGD)

---

### 4.1 Practical Example: Batch vs. Single Sample Gradients

**Same 3-sample dataset:** $X = \begin{bmatrix} 1 & 2 \\ 3 & 4 \\ 5 & 6 \end{bmatrix}$, $y = \begin{bmatrix} 5 \\ 11 \\ 17 \end{bmatrix}$

**Current weights:** $\mathbf{w} = \begin{bmatrix} 0.9 \\ 2.1 \end{bmatrix}$

**Predictions:** 
- $\hat{y}_1 = 1(0.9) + 2(2.1) = 5.1$ → error: $+0.1$
- $\hat{y}_2 = 3(0.9) + 4(2.1) = 10.7$ → error: $-0.3$
- $\hat{y}_3 = 5(0.9) + 6(2.1) = 17.3$ → error: $+0.3$

**Batch GD (all 3 samples together):**
$$g = \frac{1}{3} X^T(\hat{y} - y) = \frac{1}{3} \begin{bmatrix} 1 & 3 & 5 \\ 2 & 4 & 6 \end{bmatrix} \begin{bmatrix} 0.1 \\ -0.3 \\ 0.3 \end{bmatrix} = \frac{1}{3} \begin{bmatrix} 0.7 \\ 0.8 \end{bmatrix} \approx \begin{bmatrix} 0.233 \\ 0.267 \end{bmatrix}$$

With $\alpha = 0.01$: $\mathbf{w} \leftarrow [0.9, 2.1] - 0.01[0.233, 0.267] = [0.878, 2.087]$

**SGD (sample 1 only):**
$$g = x_1(x_1^T\mathbf{w} - y_1) = [1, 2] \cdot (5.1 - 5) = [1, 2] \cdot 0.1 = [0.1, 0.2]$$

With $\alpha = 0.01$: $\mathbf{w} \leftarrow [0.9, 2.1] - 0.01[0.1, 0.2] = [0.899, 2.098]$

**Observation:** Even with same learning rate, they take different steps! Batch GD considers all errors at once (more stable direction). SGD uses only sample 1's error (noisier, but faster). Next iteration, SGD picks sample 2 or 3 (different error direction again).

**Over many iterations:** SGD's noisy updates still point toward optimum on average; BGD converges more smoothly.

---

## 4.2 BGD vs. SGD Comparison

| Aspect | Batch GD | Stochastic GD | Mini-Batch GD |
|--------|----------|---------------|---------------|
| **Loss optimized** | Total loss $L(\mathbf{w})$ on all $n$ samples | Single sample loss $L_i(\mathbf{w})$ | Batch average loss on $b$ samples |
| **Gradient computation** | $g = \frac{1}{n}X^T(X\mathbf{w} - y)$ | $g = x_i(x_i^T\mathbf{w} - y_i)$ | $g = \frac{1}{b}\sum_{j \in B} x_j(x_j^T\mathbf{w} - y_j)$ |
| **Update noise** | Stable, smooth | Very noisy, can oscillate | Balanced |
| **Per-iteration cost** | $O(nd)$ (high) | $O(d)$ (low) | $O(bd)$ (medium) |
| **Iterations to converge** | $O(1/\epsilon)$ steps | $O(1/\sqrt{\epsilon})$ steps | Between both |
| **When to use** | Small datasets ($n < 10^4$) | Large datasets ($n > 10^6$) | Modern standard; $b = 32-256$ |

**Key insight:** SGD is noisier but much faster per iteration. BGD is stable but slow on big data.

---

## 5. Optimization / Learning Dynamics
$$\nabla L = \frac{1}{n}X^T(X\mathbf{w} - y)$$

- **Large error** → large gradient → large step
- **Small error** → small gradient → small step
- **Perfect fit** → gradient = 0 → update stops

### Effect of Learning Rate $\alpha$:

| Scenario | Behavior |
|----------|----------|
| $\alpha$ too small | Converges very slowly, many iterations needed |
| $\alpha$ optimal | Smooth convergence to minimum |
| $\alpha$ too large | May oscillate or diverge (no convergence) |
| $\alpha = 0$ | No updates; $\mathbf{w}$ stays constant |

**Convergence:** Guaranteed for convex loss (quadratic). For GD to converge: $\alpha < \frac{2}{\lambda_{\max}(X^TX)}$

---

## 6. Failure Cases / Limitations

| Problem | Why | Impact |
|---------|-----|--------|
| **Multicollinearity** | Columns of $X$ are linearly dependent | $X^TX$ is singular; cannot invert |
| **Underfitting** | Model too simple for data | High bias; poor train + test performance |
| **Overfitting** | Model fits noise, not signal | Low train error, high test error |
| **Outliers** | MSE is L2 loss, sensitive to large errors | Single outlier can skew $\mathbf{w}$ significantly |
| **Non-linear patterns** | Assumes linear relationship | Systematically misses curved patterns |

---

## 7. Regularization in Linear Regression

**The Problem: Overfitting**

When $n < d$ (fewer samples than features), the model can fit **every single data point perfectly**, achieving zero training error. But it's memorizing noise, not learning signal.

**Example:**
- 5 data points, 10 features → can find weights that give perfect fit
- On new test data → terrible performance (high error)

**The Solution: Regularization**

Add a **penalty term** to the loss function:
$$L_{\text{total}}(\mathbf{w}) = L_{\text{data}}(\mathbf{w}) + \lambda \cdot R(\mathbf{w})$$

where:
- $L_{\text{data}} = \frac{1}{2n}\|X\mathbf{w} - y\|^2$ (MSE, original loss)
- $R(\mathbf{w})$ is penalty term (depends on weights)
- $\lambda \geq 0$ is regularization strength (hyperparameter you tune)

**Intuition:** Minimize both training error AND keep weights small. Forces tradeoff: fit data, but not perfectly.

---

### Ridge Regression (L2 Regularization)

**Penalty term:**
$$R(\mathbf{w}) = \|\mathbf{w}\|_2^2 = \sum_{j=1}^{d} w_j^2$$

**Total loss:**
$$L(\mathbf{w}) = \frac{1}{2n}\|X\mathbf{w} - y\|^2 + \lambda \|\mathbf{w}\|_2^2$$

**Closed-form solution:**
$$\mathbf{w}^* = (X^TX + 2n\lambda I)^{-1}X^Ty$$

**Compare to ordinary linear regression:** $\mathbf{w}^* = (X^TX)^{-1}X^Ty$

The term $2n\lambda I$ **adds to the diagonal**. Even if $X^TX$ is singular (n < d), adding $2n\lambda I$ makes it invertible!

---

**Geometric intuition (constraint view):**

Without regularization: minimize MSE without constraint.

With L2: **minimize MSE subject to** $\|\mathbf{w}\|_2^2 \leq C$

This is equivalent to saying: "Find the best fit **inside a ball** of radius $\sqrt{C}$ centered at origin."

- If $\lambda$ is small (or $C$ is large): ball is big → solution is close to unregularized optimum
- If $\lambda$ is large (or $C$ is small): ball is tiny → solution is forced toward zero (even at cost of higher MSE)

```
Visual (2D case, weights w1, w2):

Without L2:          With L2:
   w2                   w2
   │                    │
   ├─ optim           ├─ optim (unregularized)
   │                  │ ╱
   ├─── w1            ⭕  circle constraint
   
   No constraint      Solution inside circle
```

---

**Gradient & Update:**

$$\nabla L = \frac{1}{n}X^T(X\mathbf{w} - y) + 2\lambda \mathbf{w}$$

In gradient descent:
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \nabla L$$

$$= \mathbf{w}_t - \alpha \left(\frac{1}{n}X^T(X\mathbf{w} - y) + 2\lambda \mathbf{w}_t\right)$$

$$= \mathbf{w}_t(1 - 2\alpha\lambda) - \frac{\alpha}{n}X^T(X\mathbf{w}_t - y)$$

**Key term:** $(1 - 2\alpha\lambda) < 1$ → weights are **shrunk** each iteration, even before gradient step!

---

### Lasso Regression (L1 Regularization)

**Penalty term:**
$$R(\mathbf{w}) = \|\mathbf{w}\|_1 = \sum_{j=1}^{d} |w_j|$$

**Total loss:**
$$L(\mathbf{w}) = \frac{1}{2n}\|X\mathbf{w} - y\|^2 + \lambda \|\mathbf{w}\|_1$$

**No closed-form solution!** Must use iterative methods (coordinate descent, proximal gradient, etc.)

---

**Geometric intuition (constraint view):**

With L1: **minimize MSE subject to** $\|\mathbf{w}\|_1 \leq C$

This is a **diamond** (in 2D), **hypercube** (in higher D).

```
Visual (2D case):

With L1:
   w2
   │
   ├─ diamond constraint
  ╱ │ ╲
 ╱  │  ╲  w1

Optimal solution often on axis (w1=0 or w2=0)
```

**Key difference:** L1 constraint is a **diamond with sharp corners**. Optimal point often **lies on a corner** (axis), meaning some weights are **exactly zero**!

This is **feature selection**: L1 naturally zeros out unimportant features.

---

**L1 vs L2 Comparison:**

| Aspect | Ridge (L2) | Lasso (L1) |
|--------|-----------|-----------|
| **Penalty** | $\sum w_j^2$ | $\sum \|w_j\|$ |
| **Sparsity** | No (weights shrink but stay nonzero) | Yes (pushes weights to exactly 0) |
| **Closed-form?** | Yes: $(X^TX + 2n\lambda I)^{-1}X^Ty$ | No (needs iterative solver) |
| **Constraint shape** | Circle/sphere | Diamond/hypercube |
| **When weights small** | Soft penalty | Hard penalty (constant $\lambda$) |
| **Use case** | General shrinkage, stability | Feature selection (which features matter?) |
| **Multicollinearity** | Handles well (distributed shrinking) | Can arbitrarily select 1 of 2 correlated features |

---

**Worked example: Ridge vs Lasso on $n < d$ problem**

**Setup:** 5 samples, 10 features. Without regularization, can fit perfectly (10 degrees of freedom, 5 constraints).

**Ordinary linear regression:** $X^TX$ is $10 \times 10$ but rank 5 (singular). Cannot invert!

**Ridge regression ($\lambda = 0.1$):**
- Adds $0.2I$ to diagonal of $X^TX$
- Makes it invertible (all eigenvalues now $> 0$)
- Solution: $\mathbf{w}^* = (X^TX + 0.2I)^{-1}X^Ty$
- All 10 weights are **nonzero but small** (shrunk)
- Generalizes better than overfitting

**Lasso regression ($\lambda = 0.1$):**
- No easy formula (use iterative solver)
- Solves: minimize $\frac{1}{2 \cdot 5}\|X\mathbf{w} - y\|^2 + 0.1\|\mathbf{w}\|_1$
- Result: maybe $w_1, w_3, w_7$ nonzero; others exactly 0
- Found the "important" features; others discarded
- Also generalizes well, with added interpretability

---

### How to Choose $\lambda$?

**Cross-validation:**
1. Split data into $K$ folds (e.g., $K=5$)
2. For each candidate $\lambda$ (e.g., $[0.001, 0.01, 0.1, 1, 10]$):
   - Train on $K-1$ folds
   - Evaluate on remaining fold
   - Repeat all $K$ times, average error
3. Choose $\lambda$ with lowest cross-validation error

**Intuition:**
- $\lambda = 0$: no regularization, overfitting on train data
- $\lambda$ small: some regularization, good balance
- $\lambda$ large: too much regularization, underfitting (high error even on train data)

**Learning curve:** Plot train error and validation error vs $\lambda$. Sweet spot is where both are low.

---

## 7.5 Regularization vs Overfitting

**Without regularization ($\lambda = 0$):**
- Minimizes training MSE only
- With $n < d$: training error = 0 (memorized data)
- Test error = very high (doesn't generalize)

**With good regularization ($\lambda$ tuned):**
- Slightly higher training MSE
- Much lower test error
- Model learned signal, not noise

**Example numbers:**
- Train error: 0.05, Test error: 2.5 (overfitted, $\lambda=0$)
- Train error: 0.08, Test error: 0.10 (well-regularized, $\lambda=0.1$)

Better to sacrifice a little training accuracy to gain much more test accuracy!

---

## 8. When It Works Well

- **Linear relationships** in data
- **Small to medium datasets** (computational efficiency)
- **Well-behaved features** (no severe multicollinearity)
- **Interpretability needed** (can read coefficients directly)
- **Real-world:** predicting housing prices, sales forecasting, temperature prediction

---

## 8. Variants / Extensions

| Variant | Purpose | Key Change |
|---------|---------|------------|
| **Ridge Regression** | Reduce multicollinearity | Add $\lambda\|\mathbf{w}\|_2^2$ to loss |
| **Lasso Regression** | Feature selection | Add $\lambda\|\mathbf{w}\|_1$ to loss |
| **Elastic Net** | Balance both | Add both L1 and L2 penalties |
| **Polynomial Regression** | Capture non-linearity | Expand features: $x \to [x, x^2, x^3, ...]$ |
| **Weighted Regression** | Handle noisy samples | Different samples have different importance weights |

---

## 9. Comparison Table

| Method | When to Use | Strength | Weakness |
|--------|------------|----------|----------|
| **Linear Regression** | Linear data, interpretability needed | Fast, simple, closed-form solution | Can't capture non-linearity |
| **Ridge Regression** | Multicollinearity present, $n < d$ | Stable (invertible solution), reduces variance | Slightly increases bias, all weights nonzero |
| **Lasso Regression** | Feature selection needed, high-dimensional data | Sparse solution (exact zeros), interpretable | No closed form, slower training |
| **Elastic Net** | Want both L1 and L2 benefits | Balance sparsity + stability | More hyperparameters to tune |
| **Polynomial Regression** | Non-linear patterns | More expressive | Risk of overfitting if degree too high |
| **Logistic Regression** | Binary classification | Probabilistic, gives confidence | Assumes linear decision boundary |
| **Neural Networks** | Complex non-linear patterns | Very expressive | Harder to interpret, needs more data |

---

## 10. Exam Questions

### Conceptual
1. Why is the loss function in linear regression typically MSE and not MAE? When would MAE be better?
2. Explain why $X^TX$ must be invertible. What happens if it isn't?
3. In gradient descent, why does the gradient point in the direction of steepest **increase**, yet we subtract it in the update rule?

### Derivation-Based
1. **Derive** the normal equations from first principles. Start with the MSE loss, take the derivative w.r.t. $\mathbf{w}$, and solve.
2. **Prove** that the closed-form solution $\mathbf{w}^* = (X^TX)^{-1}X^Ty$ is a global minimum, not a saddle point or local minimum.

### Trick/Failure Cases
1. You fit a linear regression model with $d = 100$ features but only $n = 50$ samples. The training error is 0. Is this good? Explain.
2. Two features in your dataset are perfectly correlated ($x_1 = 2x_2$). What happens to $(X^TX)^{-1}$? How does this affect $\mathbf{w}$?

---

## 11. Key Takeaways

- **Linear regression minimizes MSE** via closed-form solution or gradient descent
- **Normal equations:** $\mathbf{w}^* = (X^TX)^{-1}X^Ty$ (invertibility required)
- **Gradient descent:** iterative, works when closed-form fails, controlled by learning rate
- **Regularization prevents overfitting** by penalizing large weights
- **Ridge (L2):** shrinks all weights, closed-form solution, good for multicollinearity
- **Lasso (L1):** exact zeros (feature selection), no closed form, good for high-dimensional data
- **MSE is convex** → single global minimum, guaranteed convergence
- **Outliers heavily influence MSE** due to squaring; consider L1 loss for robustness
- **Interpretability advantage:** coefficients directly show feature impact
- **Always tune $\lambda$ via cross-validation!** (not a hyperparameter to guess)

---
