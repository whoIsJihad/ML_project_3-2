# 📘 Logistic Regression

## 1. Core Idea (Intuition)

**Logistic regression** solves **binary classification**: predicting class $y \in \{0, 1\}$.

Unlike linear regression (which predicts unbounded values), logistic regression:
- Uses a **sigmoid function** to squash predictions into $[0, 1]$
- Interprets output as **probability**: $P(y=1|x)$
- Finds a **linear decision boundary**

---

## 2. Mathematical Formulation

### Model
$$\sigma(z) = \frac{1}{1 + e^{-z}} \quad \text{(Sigmoid function)}$$

$$\hat{p} = \sigma(X\mathbf{w} + b)$$

where $\hat{p} = P(y=1|X)$ (predicted probability).

**Key properties of sigmoid:**
- $\sigma(0) = 0.5$
- $\sigma(z) \to 1$ as $z \to +\infty$
- $\sigma(z) \to 0$ as $z \to -\infty$
- **Derivative:** $\sigma'(z) = \sigma(z)(1 - \sigma(z))$

### Loss Function (Binary Cross-Entropy)
$$L(\mathbf{w}) = -\frac{1}{n} \sum_{i=1}^{n} \left[ y_i \log(\hat{p}_i) + (1-y_i) \log(1-\hat{p}_i) \right]$$

where $\hat{p}_i = \sigma(x_i^T\mathbf{w})$.

**Intuition:** 
- If $y_i = 1$ and $\hat{p}_i \approx 1$: loss $\approx 0$ ✓
- If $y_i = 1$ and $\hat{p}_i \approx 0$: loss $\approx \infty$ (heavily penalized)
- Symmetric for $y_i = 0$

---

## 3. Derivation of Gradient

### Step 1: Derivative of Loss w.r.t. Prediction
$$\frac{\partial L}{\partial \hat{p}_i} = -\frac{y_i}{\hat{p}_i} + \frac{1-y_i}{1-\hat{p}_i}$$

Simplify:
$$= \frac{-y_i(1-\hat{p}_i) + (1-y_i)\hat{p}_i}{\hat{p}_i(1-\hat{p}_i)} = \frac{\hat{p}_i - y_i}{\hat{p}_i(1-\hat{p}_i)}$$

### Step 2: Derivative of Prediction w.r.t. Logits
$$\frac{\partial \hat{p}_i}{\partial z_i} = \sigma(z_i)(1-\sigma(z_i)) = \hat{p}_i(1-\hat{p}_i)$$

where $z_i = x_i^T\mathbf{w}$.

### Step 3: Chain Rule
$$\frac{\partial L}{\partial z_i} = \frac{\partial L}{\partial \hat{p}_i} \cdot \frac{\partial \hat{p}_i}{\partial z_i} = \frac{\hat{p}_i - y_i}{\hat{p}_i(1-\hat{p}_i)} \cdot \hat{p}_i(1-\hat{p}_i) = \hat{p}_i - y_i$$

**Beautiful result:** The gradient w.r.t. logits is simply the **prediction error**.

### Step 4: Gradient w.r.t. Weights
$$\frac{\partial L}{\partial \mathbf{w}} = \frac{1}{n} X^T(\hat{p} - y)$$

where $\hat{p} - y$ is the **vector of errors**.

---

## 4. Training Procedure (Gradient Descent)

```
Input: X, y, learning_rate α, iterations T
Output: w

1. Initialize w = 0 (or random)
2. For t = 1 to T:
   a. Compute predictions: p_hat = sigmoid(Xw)
   b. Compute gradient: g = (1/n) X^T(p_hat - y)
   c. Update: w ← w - α·g
3. Return w
```

**Key difference from linear regression:**
- Linear: gradient depends on $Xw - y$
- Logistic: gradient depends on $\sigma(Xw) - y$ (nonlinear!)

---

## 5. Important Properties

### No Closed-Form Solution
Unlike linear regression, logistic regression **cannot be solved analytically**. Why?

The gradient $g = \frac{1}{n}X^T(\sigma(Xw) - y)$ involves $\sigma(\cdot)$, a nonlinear function. 

Setting $g = 0$ gives:
$$X^T(\sigma(Xw) - y) = 0$$

**Cannot solve for $\mathbf{w}$ in closed form** → must use iterative optimization (gradient descent, Newton's method).

### Convexity
The cross-entropy loss for logistic regression is **strictly convex**, so gradient descent finds the global minimum.

---

## 6. Decision Boundary

### Binary Classification
Once trained, classify as:
$$\hat{y} = \begin{cases} 1 & \text{if } \hat{p} \geq 0.5 \\ 0 & \text{otherwise} \end{cases}$$

This is equivalent to:
$$\hat{y} = \begin{cases} 1 & \text{if } x^T\mathbf{w} \geq 0 \\ 0 & \text{otherwise} \end{cases}$$

**Decision boundary:** The hyperplane $x^T\mathbf{w} = 0$ separates the two classes.

**Limitation:** This boundary is **always linear**. Non-linear patterns cannot be captured.

---

## 7. Failure Cases / Limitations

| Problem | Why | Impact |
|---------|-----|--------|
| **Linearly inseparable data** | Model assumes linear boundary | High train and test error |
| **Imbalanced classes** | More samples from one class | Biased toward majority class |
| **Small learning rate** | Slow convergence | Needs many iterations |
| **Large learning rate** | Oscillation or divergence | Loss doesn't decrease monotonically |
| **Multicollinearity** | Features highly correlated | Unstable $\mathbf{w}$ estimates |

---

## 8. When It Works Well

- **Linearly separable or near-separable data**
- **Binary classification** problems
- **Interpretability needed:** coefficients show feature importance directly
- **Probabilistic output needed:** $\hat{p}$ can be used as confidence
- **Real-world:** spam detection, disease diagnosis, credit approval

---

## 9. Variants / Extensions

| Variant | Purpose | Key Change |
|---------|---------|------------|
| **Multinomial Logistic Regression** | Multi-class ($K > 2$ classes) | Softmax instead of sigmoid |
| **Regularized Logistic Regression** | Reduce overfitting | Add $\lambda \mathbf{w}^T\mathbf{w}$ to loss |
| **Logistic Regression + Polynomial Features** | Non-linear boundary | Expand features: $[x_1, x_2] \to [x_1, x_2, x_1^2, x_1x_2, x_2^2, ...]$ |

---

## 10. Comparison Table

| Method | When to Use | Strength | Weakness |
|--------|------------|----------|----------|
| **Logistic Regression** | Binary, linear boundary | Fast, interpretable, probabilistic | Can't handle non-linear boundaries |
| **Polynomial Logistic** | Non-linear boundary | More expressive | Risk of overfitting |
| **Neural Networks** | Complex patterns | Very expressive | Black-box, harder to interpret |
| **SVM** | Binary classification | Handles non-linearity (kernel trick) | Less intuitive than logistic regression |
| **Decision Trees** | Mixed features (numeric + categorical) | Simple, interpretable | Can overfit easily |

---

## 11. Exam Questions

### Conceptual
1. Why is cross-entropy (not MSE) used as the loss for logistic regression? What goes wrong if you use MSE?
2. Why does logistic regression have no closed-form solution, while linear regression does?
3. What does the probability $\hat{p} = 0.7$ mean? Is a prediction of $\hat{y} = 1$ always correct?

### Derivation-Based
1. **Derive** the gradient $\frac{\partial L}{\partial \mathbf{w}}$ for logistic regression from the cross-entropy loss.
2. **Prove** that the decision boundary in logistic regression is always linear (cannot be curved).

### Trick/Failure Cases
1. You train logistic regression on perfectly linearly separable data. The loss reaches 0, and training accuracy is 100%. Should you be happy? Why or why not?
2. Your training data has 1000 samples of class 0 and 10 samples of class 1. After training, the model predicts class 0 for almost every sample. How would you fix this?

---

## 12. Key Takeaways

- **Logistic regression** uses sigmoid to map linear predictions to probabilities $[0, 1]$
- **Loss:** Binary cross-entropy (not MSE)
- **Gradient:** $\nabla L = \frac{1}{n}X^T(\sigma(Xw) - y)$ (no closed form)
- **Decision boundary is always linear** → cannot capture non-linear patterns
- **Probabilistic interpretation:** $\hat{p}$ is confidence, not a hard decision
- **Convex loss** → gradient descent guaranteed to find global optimum
- **Imbalanced data:** requires special handling (resampling, class weights)

---
