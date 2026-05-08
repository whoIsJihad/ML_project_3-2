# 📝 Logistic Regression - Exam Answers

## Conceptual Questions

### Q1: Why is cross-entropy (not MSE) used as the loss for logistic regression? What goes wrong if you use MSE?

**Answer:**

**Cross-Entropy Loss (correct for classification):**
$$L = -\frac{1}{n}\sum_{i=1}^{n} [y_i \log(\hat{p}_i) + (1-y_i)\log(1-\hat{p}_i)]$$

where $\hat{p}_i = \sigma(x_i^T\mathbf{w})$ (probability)

**Why Cross-Entropy is better:**

1. **Natural for probabilities**
   - Output $\hat{p} \in [0,1]$ is a probability
   - Cross-entropy measures divergence between true distribution (binary: 0 or 1) and predicted distribution $\hat{p}$
   - If $y=1$ and $\hat{p}=0.99$: loss $\approx 0.01$ (small, good)
   - If $y=1$ and $\hat{p}=0.01$: loss $\approx 4.6$ (large, bad)

2. **Well-behaved gradients**
   - Gradient: $\frac{\partial L}{\partial \mathbf{w}} = \frac{1}{n}X^T(\hat{p} - y)$
   - Simple form: depends on prediction error $(\hat{p} - y)$
   - Always nonzero when wrong → forces learning

3. **Probabilistic interpretation**
   - Cross-entropy = negative log-likelihood
   - Maximum likelihood estimation (standard statistical framework)

---

**What goes wrong with MSE:**

$$L_{\text{MSE}} = \frac{1}{n}\sum_{i=1}^{n} (\hat{p}_i - y_i)^2$$

1. **Vanishing gradients on correct predictions**
   ```
   If y=1, ŷ=0.99:  error = 0.01, gradient ≈ small
   If y=1, ŷ=0.51:  error = 0.49, gradient ≈ medium
   If y=1, ŷ=0.01:  error = 0.99, gradient ≈ large (but sigmoid is saturated!)
   
   Problem: When model is very wrong, sigmoid gradient ≈ 0
   Combined: big error × small gradient = no learning
   ```

2. **Unstable for extreme predictions**
   - When $\hat{p}$ far from $y$, sigmoid is flat
   - Gradient of sigmoid: $\sigma'(z) = \sigma(z)(1-\sigma(z)) \approx 0$ for large $|z|$
   - MSE + sigmoid = double penalty for being very wrong

3. **Not treating classification seriously**
   - MSE designed for regression (continuous output)
   - Treats $\hat{p}=0.4$ almost as bad as $\hat{p}=0.6$ for label $y=0$ (similar errors)
   - Classification cares about: is it > 0.5? Not the exact value.

**Concrete example:**
```
True label: y = 1
Prediction: ŷ = 0.2 (confidently wrong)

MSE loss:    (0.2 - 1)² = 0.64
Gradient:    2(0.2 - 1) × σ'(z) = -1.6 × σ'(z)
             But σ'(z) ≈ 0.04 (sigmoid is flat)
             So gradient ≈ -0.064 (tiny!)
             
Cross-entropy: -log(0.2) ≈ 1.61 (large penalty)
Gradient:      (0.2 - 1) = -0.8 (strong signal to update)
```

**Conclusion:** Cross-entropy naturally penalizes wrong predictions, even when sigmoid is saturated. MSE fails in this regime.

---

### Q2: Why does logistic regression have no closed-form solution, while linear regression does?

**Answer:**

**Linear Regression (has closed-form):**
$$L = \|X\mathbf{w} - y\|^2 \quad \text{(quadratic in } \mathbf{w}\text{)}$$

Gradient:
$$\nabla L = 2X^T(X\mathbf{w} - y)$$

Setting to 0:
$$X^T X\mathbf{w} = X^T y \Rightarrow \mathbf{w}^* = (X^TX)^{-1}X^Ty$$

**Why it works:** Loss is quadratic polynomial in $\mathbf{w}$ → derivative is linear → easy to solve.

---

**Logistic Regression (no closed-form):**
$$L = \sum_{i=1}^{n} -[y_i \log(\sigma(x_i^T\mathbf{w})) + (1-y_i)\log(1-\sigma(x_i^T\mathbf{w}))]$$

where $\sigma(z) = \frac{1}{1+e^{-z}}$ (sigmoid).

Gradient:
$$\nabla L = \sum_{i=1}^{n} x_i(\sigma(x_i^T\mathbf{w}) - y_i)$$

**Why it's hard:** 
- Loss contains sigmoid (nonlinear transcendental function)
- Gradient is nonlinear in $\mathbf{w}$
- Setting $\nabla L = 0$ gives: $\sum_{i} x_i(\sigma(x_i^T\mathbf{w}) - y_i) = 0$
- This is a **nonlinear equation** (no algebraic solution for $\mathbf{w}$)

**Geometric intuition:**
```
Linear regression:  L = (w-3)² (parabola) → algebraic formula w* = 3
Logistic:           L = -log(σ(w)) (S-curve composed with log)
                       → transcendental equation → need numerical solver
```

**Mathematical reason:**
- Linear regression loss = polynomial → polynomial equations have formulas
- Logistic regression loss = composite of polynomials + sigmoid + log → transcendental equations
- Transcendental equations (e.g., $x = \cos(x)$) have no closed-form solutions

**Solution:** Use **iterative methods** (gradient descent, Newton-Raphson) to find $\mathbf{w}$ numerically.

---

### Q3: What does the probability $\hat{p} = 0.7$ mean? Is a prediction of $\hat{y} = 1$ always correct?

**Answer:**

**What $\hat{p} = 0.7$ means:**

$\hat{p}$ is the **predicted probability** of class 1:
$$\hat{p} = P(y=1 | x) = \sigma(x^T\mathbf{w}) = 0.7$$

**Interpretation:**
- Model believes sample is 70% likely to belong to class 1
- 30% likely to belong to class 0
- Model is confident, but not certain

---

**Is $\hat{y} = 1$ always correct?**

**No!** There are two separate decisions:

1. **Probability estimate:** $\hat{p} = 0.7$ (what model predicts)
2. **Class prediction:** $\hat{y} = 1$ (what you decide to predict)

These are not the same!

**The standard rule:** 
$$\hat{y} = \begin{cases} 1 & \text{if } \hat{p} > 0.5 \\ 0 & \text{if } \hat{p} \leq 0.5 \end{cases}$$

Using $\hat{p} = 0.7 > 0.5$, we predict $\hat{y} = 1$.

**But predictions can still be wrong!**

Example:
- True label: $y = 0$
- Model prediction: $\hat{p} = 0.7$
- Hard prediction: $\hat{y} = 1$
- Result: **Incorrect prediction** (despite 70% confidence)

**Why?** The 0.5 threshold is arbitrary! The true label is still determined by nature, not the model's confidence.

---

**When $\hat{y} = 1$ correct:**
- True label is $y = 1$ (not guaranteed by $\hat{p} = 0.7$)

**When $\hat{y} = 1$ incorrect:**
- True label is $y = 0$ (still happens ~30% of the time with $\hat{p} = 0.7$)

---

**Key insight:** High probability $\neq$ guaranteed correct. It means high likelihood, not certainty.

**Practical note:** Can adjust threshold based on cost:
- If predicting class 1 is expensive, use threshold = 0.8 (more confident)
- If missing class 1 is expensive, use threshold = 0.3 (more liberal)

---

## Derivation-Based Questions

### Q1: Derive the gradient $\frac{\partial L}{\partial \mathbf{w}}$ for logistic regression from cross-entropy loss.

**Answer:**

**Start with cross-entropy loss:**
$$L(\mathbf{w}) = \frac{1}{n}\sum_{i=1}^{n} -[y_i \log(\hat{p}_i) + (1-y_i)\log(1-\hat{p}_i)]$$

where $\hat{p}_i = \sigma(z_i) = \sigma(x_i^T\mathbf{w})$ and $z_i = x_i^T\mathbf{w}$.

**Step 1: Derivative of sigmoid**
$$\frac{d\sigma}{dz} = \sigma(z)(1-\sigma(z))$$

**Step 2: Derivative of cross-entropy w.r.t. $\hat{p}$**
$$\frac{\partial L}{\partial \hat{p}_i} = \frac{\partial}{\partial \hat{p}_i}[-y_i \log(\hat{p}_i) - (1-y_i)\log(1-\hat{p}_i)]$$

$$= -\frac{y_i}{\hat{p}_i} + \frac{1-y_i}{1-\hat{p}_i} = \frac{-y_i(1-\hat{p}_i) + (1-y_i)\hat{p}_i}{(1-\hat{p}_i)\hat{p}_i}$$

$$= \frac{\hat{p}_i - y_i}{\hat{p}_i(1-\hat{p}_i)}$$

**Step 3: Chain rule**
$$\frac{\partial L}{\partial z_i} = \frac{\partial L}{\partial \hat{p}_i} \cdot \frac{\partial \hat{p}_i}{\partial z_i}$$

$$= \frac{\hat{p}_i - y_i}{\hat{p}_i(1-\hat{p}_i)} \cdot \hat{p}_i(1-\hat{p}_i)$$

$$= \hat{p}_i - y_i$$

**Step 4: Chain rule again (z to w)**
$$\frac{\partial L}{\partial \mathbf{w}} = \frac{1}{n}\sum_{i=1}^{n} \frac{\partial L}{\partial z_i} \cdot \frac{\partial z_i}{\partial \mathbf{w}}$$

$$= \frac{1}{n}\sum_{i=1}^{n} (\hat{p}_i - y_i) \cdot x_i$$

$$= \frac{1}{n} X^T(\hat{p} - y)$$

**Final Result:**
$$\boxed{\frac{\partial L}{\partial \mathbf{w}} = \frac{1}{n} X^T(\hat{p} - y)}$$

where $\hat{p} = [\hat{p}_1, \ldots, \hat{p}_n]^T$.

**Intuition:** Gradient is proportional to prediction error $(\hat{p} - y)$ weighted by features $X$. Simple and clean!

---

### Q2: Prove that the decision boundary in logistic regression is always linear.

**Answer:**

**Decision boundary definition:**
The set of points where model is uncertain: $\hat{p} = 0.5$.

$$P(y=1|x) = 0.5$$

$$\sigma(x^T\mathbf{w}) = 0.5$$

**Solve for decision boundary:**

Sigmoid at 0.5:
$$\frac{1}{1+e^{-z}} = 0.5$$

$$1 = 0.5(1+e^{-z})$$

$$2 = 1 + e^{-z}$$

$$e^{-z} = 1$$

$$z = 0$$

**So decision boundary is where:**
$$x^T\mathbf{w} = 0$$

or equivalently:
$$w_1 x_1 + w_2 x_2 + \cdots + w_d x_d = 0$$

**This is a LINEAR equation in $x$!**

In 2D: $w_1 x_1 + w_2 x_2 = 0$ is a **line**.
In 3D: $w_1 x_1 + w_2 x_2 + w_3 x_3 = 0$ is a **plane**.
In $d$D: It's a **$(d-1)$-dimensional hyperplane**.

**Why always linear:**
- The sigmoid $\sigma(z)$ is monotonically increasing
- Only property that matters for decision boundary: $\sigma(z) = 0.5$ iff $z = 0$
- Since $z = x^T\mathbf{w}$ is linear in $x$, the boundary is linear

**Geometric consequence:**
Logistic regression can only separate **linearly separable** classes. Cannot fit curved boundaries.

---

## Trick / Failure Cases

### Q1: You train logistic regression on perfectly linearly separable data. The loss reaches 0, and training accuracy is 100%. Should you be happy? Why or why not?

**Answer:**

**Short answer:** NO! This indicates overfitting and potential issues.

---

**Why loss = 0 is problematic:**

With perfectly separable data, the model can learn weights such that:
- All positive samples: $x_i^T\mathbf{w} \to +\infty \Rightarrow \hat{p}_i \to 1$
- All negative samples: $x_i^T\mathbf{w} \to -\infty \Rightarrow \hat{p}_i \to 0$

**Result:** Cross-entropy loss → 0 as $\log(1) = 0$ and $\log(0)$ is very negative.

This happens when **weights blow up** ($\|\mathbf{w}\| \to \infty$).

---

**Problems with this:**

1. **No unique solution**
   - Infinitely many weights achieve zero training loss
   - Example: $\mathbf{w}$ and $100\mathbf{w}$ both give loss → 0
   - Which should we use? No principled answer.

2. **Terrible generalization**
   - Model has memorized training decision boundary exactly
   - Tiny perturbation in weights → predictions flip
   - Test data slightly off the boundary → catastrophic error

3. **Numerical instability**
   - Huge weights cause numerical overflow
   - $e^{-x}$ where $x$ huge → underflow / NaN
   - Can't even compute predictions reliably

4. **Not calibrated**
   - Predicted probability $\hat{p} = 0.999$ is not actually 99.9% confident
   - Just means weights are large (not about true uncertainty)

---

**What to do:**

1. **Add regularization (L2/Ridge):**
   ```
   L_total = L_CE + λ||w||²
   Penalizes large weights
   Prevents weights from blowing up
   Optimal solution is unique and stable
   ```

2. **Use early stopping:**
   ```
   Monitor validation set accuracy
   Stop when validation stops improving (before loss → 0)
   ```

3. **Check generalization:**
   ```
   Test accuracy on held-out data
   If train = 100%, test = 50% → overfitting
   ```

4. **Reduce model complexity:**
   ```
   May have too many features
   Use feature selection
   ```

---

### Q2: Your training data has 1000 samples of class 0 and 10 samples of class 1. After training, the model predicts class 0 for almost every sample. How would you fix this?

**Answer:**

**Problem: Class Imbalance**

With 1000:10 ratio (99:1), logistic regression learns:
- Class 0 is very common → predict 0 to be right most of the time
- Cost of missing class 1 is lower (only 1% of data) → ignore class 1
- Result: $\hat{y} = 0$ for everything

Training accuracy = 99% (impressive!), but model is useless (never detects class 1).

---

**Solution 1: Adjust class weights**

In loss, penalize wrong predictions unequally:
$$L = \frac{1}{n}\sum_{i=1}^{n} w_i \cdot \text{loss}_i$$

where:
- $w_i = 100$ if $y_i = 1$ (class 1)
- $w_i = 1$ if $y_i = 0$ (class 0)

**Effect:** Wrong prediction on class 1 costs 100x more → forces model to learn class 1.

**Formula:**
$$w_i = \frac{\text{# negative samples}}{\text{# positive samples}} = \frac{1000}{10} = 100$$

---

**Solution 2: Threshold adjustment**

Instead of default threshold 0.5, use lower threshold:
$$\hat{y} = \begin{cases} 1 & \text{if } \hat{p} > 0.3 \\ 0 & \text{if } \hat{p} \leq 0.3 \end{cases}$$

**Why 0.3?** Prior probability of class 1 is 1% = 0.01. Using threshold 0.3 effectively says: "Predict class 1 if model is 30× more confident than the prior."

---

**Solution 3: Resampling (oversample minority class)**

Train on balanced dataset:
- Keep all 1000 class 0 samples
- Duplicate class 1 samples: 1000 copies of 10 samples
- New ratio: 1000:1000 (balanced)

**Caveat:** Can cause overfitting on repeated class 1 samples.

---

**Solution 4: Use different metrics**

Accuracy is misleading. Use:
- **Precision/Recall:** How well does model find class 1?
- **F1-score:** Balance precision and recall
- **AUC-ROC:** Area under precision-recall curve

Optimize for these instead of accuracy.

---

**Solution 5: Ensemble / cost-sensitive learning**

Use algorithms that handle imbalance:
- XGBoost with `scale_pos_weight` parameter
- Random Forests with balanced mode
- Techniques like SMOTE (synthetic oversampling)

---

**Recommended approach:**
1. **Use class weights** (Solution 1) — simplest and most effective
2. **Validate on precision/recall** (Solution 4) — use right metrics
3. Monitor **test set performance** on both classes separately

