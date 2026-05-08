# 📝 Linear Regression - Exam Answers

## Conceptual Questions

### Q1: Why is the loss function in linear regression typically MSE and not MAE? When would MAE be better?

**Answer:**

**MSE (Mean Squared Error):** $L = \frac{1}{n}\sum_i (y_i - \hat{y}_i)^2$
- **Advantages:**
  - Differentiable everywhere; gradients smooth and well-behaved
  - Mathematically elegant: normal equations have closed-form solution $(X^TX)^{-1}X^Ty$
  - Convex loss (single global minimum)
  - Gradient descent guaranteed to converge
  
- **Disadvantage:** Squares errors, so outliers heavily influence the solution

**MAE (Mean Absolute Error):** $L = \frac{1}{n}\sum_i |y_i - \hat{y}_i|$
- **Advantages:**
  - Robust to outliers (linear penalty, not quadratic)
  - More interpretable (average absolute deviation in target units)
  
- **Disadvantages:**
  - Not differentiable at error = 0 (kink in derivative)
  - No closed-form solution; requires iterative optimization
  - Gradient descent less stable (piecewise linear)

**When to use MAE:**
- Dataset has outliers that shouldn't dominate (real-world noisy data)
- Want robustness over mathematical convenience
- Example: House price prediction where one mansion in dataset shouldn't skew weights

**In practice:** MSE is default for simplicity and theory; switch to MAE if outliers problematic.

---

### Q2: Explain why $X^TX$ must be invertible. What happens if it isn't?

**Answer:**

**Why invertibility is needed:**

The normal equations give: $\mathbf{w}^* = (X^TX)^{-1}X^Ty$

To solve this, we need $(X^TX)^{-1}$ to exist. $(X^TX)^{-1}$ exists iff $X^TX$ is **full rank** (all eigenvalues nonzero).

**What it means geometrically:**
- $X^TX$ is a $d \times d$ matrix (square)
- Rank of $X^TX$ = rank of $X$ (always true)
- If $X^TX$ singular → $X$ has rank $< d$ → **not all features are independent**

**When $X^TX$ is NOT invertible (singular):**

**Case 1: Multicollinearity (columns linearly dependent)**
- Example: $x_1 = 2x_2$ (perfect correlation)
- Then $X^TX$ is singular
- Determinant = 0; cannot invert

**Case 2: $n < d$ (more features than samples)**
- Example: 100 features, 50 samples
- Then rank$(X) \leq n = 50 < d = 100$
- So rank$(X^TX) \leq 50 < 100$
- $X^TX$ is singular

**What happens if we try to invert anyway:**
- Numerically: inverse computation fails or produces huge values (ill-conditioned)
- Mathematically: infinitely many solutions to $X^TX\mathbf{w} = X^Ty$
- The solution space is a hyperplane; no unique optimum

**Solutions:**
1. **Remove correlated features** (feature selection)
2. **Use regularization** (Ridge/Lasso): $\mathbf{w} = (X^TX + \lambda I)^{-1}X^Ty$
   - Adding $\lambda I$ makes matrix full rank
3. **Use gradient descent** instead of normal equations (works even if singular)
4. **Pseudoinverse** $X^+$: $\mathbf{w} = X^+ y$ (generalizes when singular)

---

### Q3: In gradient descent, why does the gradient point in the direction of steepest **increase**, yet we subtract it in the update rule?

**Answer:**

**The gradient is direction of steepest increase:**

$$\nabla L(\mathbf{w}) = \frac{\partial L}{\partial \mathbf{w}}$$

By definition, gradient points in direction where $L$ **increases fastest**.

**Proof:** For small step $\epsilon > 0$:
$$L(\mathbf{w} + \epsilon \nabla L) \approx L(\mathbf{w}) + \epsilon \|\nabla L\|^2 > L(\mathbf{w})$$

Going in gradient direction increases loss.

**Why we subtract (go opposite direction):**

We want to **minimize** $L$, not maximize it. So we go in **opposite direction** of gradient:

$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \nabla L(\mathbf{w}_t)$$

For small step $\alpha > 0$:
$$L(\mathbf{w}_t - \alpha \nabla L) \approx L(\mathbf{w}_t) - \alpha \|\nabla L\|^2 < L(\mathbf{w}_t)$$

Loss **decreases**. ✓

**Intuition:**
- Gradient = "uphill" direction
- We want to go downhill → subtract it
- Learning rate $\alpha$ controls step size

**Analogy:** You're on a mountain at night. Gradient points uphill. To descend, walk downhill (opposite direction). $\alpha$ is your step size.

---

## Derivation-Based Questions

### Q1: Derive the normal equations from first principles. Start with MSE loss, take derivative w.r.t. $\mathbf{w}$, and solve.

**Answer:**

**Start with MSE loss:**
$$L(\mathbf{w}) = \frac{1}{2n} \|X\mathbf{w} - y\|^2$$

Expand norm:
$$L(\mathbf{w}) = \frac{1}{2n} (X\mathbf{w} - y)^T(X\mathbf{w} - y)$$

$$= \frac{1}{2n} (\mathbf{w}^T X^T X\mathbf{w} - 2\mathbf{w}^T X^T y + y^T y)$$

**Take derivative w.r.t. $\mathbf{w}$:**

Using chain rule:
$$\frac{\partial L}{\partial \mathbf{w}} = \frac{1}{2n}(2X^T X\mathbf{w} - 2X^T y)$$

$$= \frac{1}{n}(X^T X\mathbf{w} - X^T y)$$

**Set to zero (for minimum):**
$$\frac{\partial L}{\partial \mathbf{w}} = 0$$

$$X^T X\mathbf{w} = X^T y$$

**Solve for $\mathbf{w}$ (Normal Equations):**

Multiply both sides by $(X^TX)^{-1}$:

$$\mathbf{w}^* = (X^TX)^{-1}X^Ty$$

**Key rules used:**
- $\frac{\partial}{\partial \mathbf{w}} \mathbf{w}^T A\mathbf{w} = 2A\mathbf{w}$ (for symmetric $A$)
- $\frac{\partial}{\partial \mathbf{w}} \mathbf{w}^T b = b$

---

### Q2: Prove that the closed-form solution $\mathbf{w}^* = (X^TX)^{-1}X^Ty$ is a global minimum, not a saddle point or local minimum.

**Answer:**

**Method 1: Show loss is convex**

MSE loss is:
$$L(\mathbf{w}) = \frac{1}{2n} \|X\mathbf{w} - y\|^2$$

**Compute Hessian (second derivative):**
$$\frac{\partial^2 L}{\partial \mathbf{w}^2} = \frac{1}{n} X^T X$$

**Key observation:** $\frac{1}{n}X^TX$ is positive semi-definite (PSD):
- Eigenvalues $\geq 0$ (always true for $A^TA$ form)
- This means Hessian $\succeq 0$ everywhere

**Implication:** $L(\mathbf{w})$ is convex (curves upward everywhere)

**For convex functions:**
- Any critical point (where gradient = 0) is a global minimum
- No local minima or saddle points exist
- The solution $\mathbf{w}^*$ is unique (if $X^TX$ full rank)

---

**Method 2: Direct proof using convexity definition**

For convex function, for any $\mathbf{w}_1, \mathbf{w}_2$ and $\lambda \in [0,1]$:
$$L(\lambda \mathbf{w}_1 + (1-\lambda)\mathbf{w}_2) \leq \lambda L(\mathbf{w}_1) + (1-\lambda)L(\mathbf{w}_2)$$

Since $L(\mathbf{w}) = \|X\mathbf{w} - y\|^2$ is squared norm (quadratic form):
- Squared norms are always convex
- Linear combinations of convex functions are convex
- So MSE is convex

Therefore, $\mathbf{w}^*$ at gradient = 0 must be global minimum. QED.

---

## Trick / Failure Cases

### Q1: You fit a linear regression model with $d = 100$ features but only $n = 50$ samples. The training error is 0. Is this good? Explain.

**Answer:**

**Short answer:** NO! This is a textbook case of **severe overfitting**.

**Why training error is 0:**

With $d = 100$ features and $n = 50$ samples:
- We have **more parameters than data points**
- Rank of $X \leq \min(n, d) = 50$
- But $X^TX$ is $100 \times 100$ (singular; rank $\leq 50$)
- There exist infinitely many weight solutions that achieve zero training error
- The model can perfectly memorize the 50 training samples using only 50 features (or fewer)

**Why this is BAD:**

1. **Perfect fit on training ≠ good generalization**
   - Model memorizes noise in training data
   - Will perform terribly on unseen test data

2. **High variance, low bias**
   - Different training sets → completely different weights
   - Model is extremely unstable

3. **Interpretation fails**
   - Which of the 100 weights matter? Ambiguous.
   - Multiple solutions with different weights all achieve zero error

**Real-world consequence:**
- Train accuracy: 100%
- Test accuracy: ~50% or worse (random guessing for classification)

**Solutions:**
1. **Regularization:** Add L2 penalty $(X^TX + \lambda I)^{-1}X^Ty$ (Ridge Regression)
2. **Feature selection:** Reduce $d$ to $d < n$ (keep only important features)
3. **Get more data:** Collect more samples so $n > d$
4. **Cross-validation:** Use validation set to catch overfitting

**Lesson:** Training error = 0 with $n < d$ is a **red flag**, not success.

---

### Q2: Two features in your dataset are perfectly correlated ($x_1 = 2x_2$). What happens to $(X^TX)^{-1}$? How does this affect $\mathbf{w}$?

**Answer:**

**What happens to $X^TX$:**

If $x_1 = 2x_2$ (one feature is exact multiple of another):

$$X^TX = X^T X = \begin{pmatrix} x_1^T x_1 & x_1^T x_2 \\ x_2^T x_1 & x_2^T x_2 \end{pmatrix}$$

Substitute $x_1 = 2x_2$:

$$X^TX = \begin{pmatrix} 4x_2^T x_2 & 2x_2^T x_2 \\ 2x_2^T x_2 & x_2^T x_2 \end{pmatrix}$$

Notice row 1 = 2 × row 2. **Rows are linearly dependent!**

$$\text{det}(X^TX) = 0$$

**$X^TX$ is SINGULAR** (not invertible).

---

**What happens to $(X^TX)^{-1}$:**

Since $X^TX$ is singular:
- $(X^TX)^{-1}$ does **not exist**
- Numerically: inverse computation fails or returns $\infty$ / NaN
- Computationally: matrix is ill-conditioned (near-singular)

**Practical behavior:**
- If using pseudoinverse or numerical solver: inverse contains huge values
- Small rounding errors blow up

---

**Effect on weights $\mathbf{w}$:**

From normal equations: $\mathbf{w} = (X^TX)^{-1}X^Ty$

Since inversion fails:
1. **No unique solution exists**
   - Infinitely many weight vectors solve the problem equally well
   - Example: $\mathbf{w} = [4, -2] + t[2, -1]$ for any scalar $t$
   - Why? Multiplying any weight by $[2, -1]$ doesn't change prediction (since $2x_2 - x_2 = 0$)

2. **Different algorithms give different $\mathbf{w}$**
   - Closed-form: fails
   - Gradient descent: may converge to different solutions depending on initialization
   - Least-squares solver: may return arbitrary solution

3. **Predictions still work!**
   - Despite ambiguous weights, predictions $\hat{y} = X\mathbf{w}$ are unique
   - Because correlated features have dependent effects

---

**Solutions:**

1. **Remove redundant feature:**
   ```
   Drop x₁ or x₂ (they're equivalent)
   Model with only one → X^TX becomes invertible
   ```

2. **Use regularization (Ridge Regression):**
   ```
   w = (X^T X + λI)^{-1} X^T y
   Adding λI makes matrix full rank → invertible
   Picks the "smallest" solution among infinitely many
   ```

3. **Feature engineering:** Combine correlated features
   ```
   Create z = x₁ + x₂ (or other linear combo)
   Reduces multicollinearity
   ```

---

## Regularization Questions

### Q1: What is regularization and why do we need it in linear regression?

**Answer:**

**What is regularization:**

Add a **penalty term** to the loss function:
$$L_{\text{total}}(\mathbf{w}) = L_{\text{data}}(\mathbf{w}) + \lambda \cdot R(\mathbf{w})$$

where:
- $L_{\text{data}} = \frac{1}{2n}\|X\mathbf{w} - y\|^2$ is the original MSE loss
- $R(\mathbf{w})$ is a penalty on weights (usually $\|\mathbf{w}\|_2^2$ or $\|\mathbf{w}\|_1$)
- $\lambda \geq 0$ is regularization strength (tuned via cross-validation)

**Intuition:** Minimize both training error AND keep weights small. Forces tradeoff.

**Why we need it:**

**Problem without regularization:**
- With $n < d$ (more features than samples): can achieve zero training error by overfitting
- Model memorizes noise, doesn't generalize to test data

**Example:** 5 samples, 10 features
- Without regularization: train error = 0, test error = very high
- With regularization: train error = 0.05, test error = 0.07 (both low!)

**Solution:** Regularization penalizes complex models (large weights) to prevent memorization.

---

### Q2: Explain Ridge Regression (L2 Regularization). How does it solve the $n < d$ problem?

**Answer:**

**Ridge Regression formulation:**
$$L(\mathbf{w}) = \frac{1}{2n}\|X\mathbf{w} - y\|^2 + \lambda \|\mathbf{w}\|_2^2$$

$$= \frac{1}{2n}\|X\mathbf{w} - y\|^2 + \lambda \sum_{j=1}^{d} w_j^2$$

**Closed-form solution:**
$$\mathbf{w}^* = (X^TX + 2n\lambda I)^{-1}X^Ty$$

**Compare to ordinary linear regression:** $\mathbf{w}^* = (X^TX)^{-1}X^Ty$

The term $2n\lambda I$ **adds to diagonal of $X^TX$**.

---

**How Ridge solves the $n < d$ problem:**

**Without regularization ($\lambda = 0$):**
- $X^TX$ is singular (rank $\leq n < d$)
- Cannot invert (determinant = 0)
- No unique solution

**With Ridge ($\lambda > 0$):**
- $(X^TX + 2n\lambda I)$ is **always invertible** (all eigenvalues shifted up by $2n\lambda > 0$)
- Even if $X^TX$ has eigenvalue 0 (singular), adding $2n\lambda$ makes it nonzero

**Example numbers:**
```
X^T X eigenvalues: [10, 5, 0, 0, ..., 0]  (rank 2, singular)
X^T X + λI with λ=0.1:  [10, 5, 0.1, 0.1, ..., 0.1]  (all positive, invertible!)
```

---

**Geometric intuition (constraint view):**

**Ridge regression is equivalent to:**
$$\text{Minimize} \quad \|X\mathbf{w} - y\|^2 \quad \text{subject to} \quad \|\mathbf{w}\|_2^2 \leq C$$

This says: "Find best fit, but **keep weights inside a ball of radius $\sqrt{C}$**."

```
Visual (2D):
   w2
   │
   ├─ optimum (unconstrained)
   │  ↑
   │  │ ⭕  ball constraint
   │ ╱ ╲
   ├─── w1
   
   Solution must be inside circle.
```

- If $\lambda$ small (C large): solution close to unconstrained optimum
- If $\lambda$ large (C small): solution forced toward zero (even if train error increases)

---

**Gradient update interpretation:**

Taking derivative: $\nabla L = \frac{1}{n}X^T(X\mathbf{w} - y) + 2\lambda \mathbf{w}$

In gradient descent:
$$\mathbf{w}_{t+1} = \mathbf{w}_t - \alpha \nabla L$$
$$= \mathbf{w}_t(1 - 2\alpha\lambda) - \frac{\alpha}{n}X^T(X\mathbf{w}_t - y)$$

**Key term:** $(1 - 2\alpha\lambda) < 1$ is a **shrinkage factor**. Every iteration, weights get multiplied by this factor before gradient step. Weights automatically shrink!

---

### Q3: What's the difference between Ridge (L2) and Lasso (L1) regularization?

**Answer:**

| Aspect | Ridge (L2) | Lasso (L1) |
|--------|-----------|-----------|
| **Penalty term** | $\lambda \sum_{j=1}^{d} w_j^2$ | $\lambda \sum_{j=1}^{d} \|w_j\|$ |
| **Closed-form?** | Yes: $(X^TX + 2n\lambda I)^{-1}X^Ty$ | No (requires iterative solver) |
| **Sparsity** | No (weights shrink but stay nonzero) | Yes (pushes weights to exactly 0) |
| **Constraint shape** | Circle/sphere | Diamond/hypercube |

---

**Geometric comparison:**

**Ridge (L2):** Constraint is a **circle** (in 2D)
```
   w2
   │  ⭕ constraint (circle)
   │  /|\
   │ / | \
   ├───╫─── w1
```

**Lasso (L1):** Constraint is a **diamond** (in 2D)
```
   w2
   │  /\
   │ /  \
   ├───××─── w1
      ◇ constraint (diamond)
```

**Key insight:** Diamond has **sharp corners on the axes** (w1=0 or w2=0). Optimal solution often lands **on a corner**, meaning one weight is exactly 0!

This is **feature selection**: Lasso naturally zeros out unimportant features.

---

**Example: When each shines**

**Ridge Regression ($n < d$ problem):**
- 5 samples, 10 features
- Ridge: All 10 weights shrink toward zero but stay nonzero
- Good for: **Stability** (solution always exists)
- Trade-off: All features still active (not interpretable)

**Lasso Regression (feature selection):**
- 5 samples, 10 features
- Lasso: Maybe 3 weights nonzero, 7 are exactly 0
- Good for: **Interpretability** (which features matter?)
- Trade-off: Slower to train (no closed form), arbitrary choice among correlated features

---

### Q4: How do you choose the regularization strength $\lambda$? What happens if $\lambda$ is too large or too small?

**Answer:**

**How to choose $\lambda$ (Cross-Validation):**

1. **Split data** into $K$ folds (typically $K=5$ or $K=10$)
   ```
   Train set: samples 1-4
   Validation set: sample 5
   (repeat for each fold)
   ```

2. **For each candidate $\lambda$** (e.g., $[0.001, 0.01, 0.1, 1, 10, 100]$):
   - Train model on $K-1$ folds
   - Evaluate on remaining fold
   - Repeat for all $K$ folds
   - Average validation error across all folds

3. **Choose $\lambda$ with lowest average validation error**

**Example with 5-fold CV:**
```
λ = 0.001:   val errors [0.15, 0.18, 0.14, 0.16, 0.17] → avg = 0.16
λ = 0.01:    val errors [0.12, 0.13, 0.11, 0.12, 0.13] → avg = 0.122 ✓ best
λ = 0.1:     val errors [0.14, 0.15, 0.13, 0.14, 0.15] → avg = 0.142
λ = 1:       val errors [0.25, 0.26, 0.24, 0.25, 0.26] → avg = 0.252
```

Choose $\lambda = 0.01$.

---

**What happens if $\lambda$ is too small:**

**$\lambda \approx 0$ (little regularization):**
- Loss = data loss + tiny penalty
- Model tries to fit training data as well as possible
- Weights can be large
- With $n < d$: close to overfitting
- **Effect:** Low train error, high test error

**Symptoms:**
```
λ = 0:
  Train error: 0.02 (very low)
  Test error:  2.5  (very high) ← OVERFITTING
```

---

**What happens if $\lambda$ is too large:**

**$\lambda \gg 1$ (strong regularization):**
- Loss ≈ regularization penalty (dominated)
- Optimizer tries to make weights small, ignores training data
- Weights approach zero
- **Effect:** High train error, high test error (both bad)

**Symptoms:**
```
λ = 100:
  Train error: 5.0  (high)
  Test error:  5.1  (high) ← UNDERFITTING
```

**Visual: Learning curves**

```
Error
  ^
  │    Train error (λ=0.001)   ╱
  │                    ╱─────╱  overfitting region
  │                  ╱
  │           ╱─────╱  λ=0.01 (optimal)
  │         ╱      ╱
  │       ╱─────╱
  │     ╱        underfitting region
  │   ╱─────────────  (λ=100)
  └──────────────────────────────> λ
         sweet spot
```

**Optimal $\lambda$:**
- Balances train and test error
- Neither too high nor too low
- Found via cross-validation
- Different for every dataset!

---

### Q5: You have a dataset with $n = 1000$ samples and $d = 500$ features. No regularization gives train error 0.01, test error 0.50. What should you do?

**Answer:**

**Diagnosis:** Train error = 0.01 (good), Test error = 0.50 (terrible) → **Severe overfitting**

**Root cause:** 500 features is still large relative to 1000 samples (ratio 1:2). Model has too much freedom, fits noise.

**Solutions (in order of effectiveness):**

**Option 1: Increase regularization strength**
- Current: probably $\lambda \approx 0$
- Try: $\lambda \in [0.01, 0.1, 1]$ via cross-validation
- Expected: Train error increases slightly (e.g., 0.02), test error drops dramatically (e.g., 0.08)
- **Cost:** Very cheap (retrain 5-10 models)
- **Recommend:** Try this first!

**Option 2: Feature selection (reduce $d$)**
- Remove irrelevant features (keep only top 50-100)
- Methods: correlation analysis, variance threshold, RFE
- Expected: Both train and test error stay low
- **Cost:** Medium (need to identify important features)

**Option 3: Collect more data**
- Get more samples (increase $n$)
- With $n \gg d$: overfitting naturally decreases
- **Cost:** Highest (data collection is expensive)

**Option 4: Use domain knowledge**
- Simple features that make sense
- Avoid redundant/noisy features
- **Cost:** Requires expertise

---

**Recommended approach:**
1. **First:** Tune $\lambda$ (cheapest)
2. **Then:** If still poor, do feature selection
3. **Then:** Collect more data if budget allows

**Expected outcome after tuning:**
```
Before:  Train = 0.01,  Test = 0.50  (λ ≈ 0)
After:   Train = 0.05,  Test = 0.08  (λ ≈ 0.1)  ✓ Good generalization
```

---

### Q6: In Ridge regression, if $\lambda = 0$, we get ordinary linear regression. If $\lambda = \infty$, what happens?

**Answer:**

**Closed-form solution:**
$$\mathbf{w}^* = (X^TX + 2n\lambda I)^{-1}X^Ty$$

**As $\lambda \to \infty$:**

Rewrite by factoring out $2n\lambda$ from inside:
$$\mathbf{w}^* = \frac{1}{2n\lambda}\left(\frac{X^TX}{2n\lambda} + I\right)^{-1}X^Ty$$

As $\lambda \to \infty$:
- $(X^TX) / 2n\lambda \to 0$
- $(X^TX + 2n\lambda I)^{-1} \approx \frac{1}{2n\lambda} I$
- $\mathbf{w}^* \approx \frac{1}{2n\lambda} I \cdot X^Ty = \frac{1}{2n\lambda} X^Ty$

**Result:** $\mathbf{w}^* \to \mathbf{0}$ (all weights approach zero!)

---

**Intuition:**

With huge penalty on weights:
- Optimizer must choose: fit data or keep weights small
- Small weights win
- **Predictions become:** $\hat{y} = X\mathbf{w} \approx 0$ (predicts nearly zero for all samples)

**Consequence:**
- Train error: very high (model is too simple)
- Test error: very high (model is useless)
- This is **severe underfitting**

```
λ = 0:          λ = 0.1 (optimal):     λ = ∞:
w ≠ 0           w = medium             w ≈ 0
Train: 0.01     Train: 0.05            Train: 5.0
Test: 0.50      Test: 0.08             Test: 5.1
(overfitting)   (good)                 (underfitting)
```

**Lesson:** $\lambda = 0$ and $\lambda = \infty$ are both extremes. Optimal is in between (found via CV).

---

