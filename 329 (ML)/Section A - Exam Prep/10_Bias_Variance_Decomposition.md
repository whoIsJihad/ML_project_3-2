# 📘 Bias-Variance Decomposition

## 1. Core Idea (Intuition)

Test error has three components:

$$\mathbb{E}[(\hat{y} - y)^2] = \text{Bias}^2 + \text{Variance} + \text{Noise}$$

- **Bias:** Model's systematic error (underfitting)
- **Variance:** Model's sensitivity to training data (overfitting)
- **Noise:** Irreducible error in data

---

## 2. Mathematical Formulation

### Setup
- True function: $y = f(x) + \epsilon$ where $\epsilon \sim \mathcal{N}(0, \sigma_n^2)$ (noise)
- Learned model: $\hat{f}(x)$
- Test error: $L(x) = (f(x) - \hat{f}(x))^2 + \epsilon^2$

### Expected Test Error
$$\mathbb{E}_x[L(x)] = \mathbb{E}_x[(f(x) - \mathbb{E}[\hat{f}(x)] + \mathbb{E}[\hat{f}(x)] - \hat{f}(x))^2] + \sigma_n^2$$

Expanding:
$$= \mathbb{E}_x[(f(x) - \mathbb{E}[\hat{f}(x)])^2] + \mathbb{E}_x[(\mathbb{E}[\hat{f}(x)] - \hat{f}(x))^2] + \sigma_n^2$$

$$= \text{Bias}^2(x) + \text{Variance}(x) + \text{Noise}$$

where expectations are over **different training sets** (different $\hat{f}$).

---

## 3. Definitions

### Bias
$$\text{Bias}(\hat{f}) = f(x) - \mathbb{E}[\hat{f}(x)]$$

**Interpretation:** Systematic error; if we could train infinitely many times and average, how far off is the prediction?

**Causes:**
- Model too simple (e.g., linear model for non-linear data)
- Underfitting

### Variance
$$\text{Variance}(\hat{f}) = \mathbb{E}[(\hat{f}(x) - \mathbb{E}[\hat{f}(x)])^2]$$

**Interpretation:** Sensitivity to training data; different training sets → different predictions?

**Causes:**
- Model too complex
- Too few training samples
- Overfitting

### Noise (Bayes Error)
$$\text{Noise} = \sigma_n^2$$

**Interpretation:** Irreducible error; inherent randomness in data.

---

## 4. Visualizations

### Low Bias, Low Variance
- Predictions clustered near true value
- **Ideal scenario**

### High Bias, Low Variance
- Predictions clustered far from true value
- **Systematic error** (underfitting)

### Low Bias, High Variance
- Predictions scattered around true value
- **Unstable predictions** (overfitting)

### High Bias, High Variance
- Predictions scattered and far from true value
- **Both underfitting and overfitting** (worst case)

---

## 5. Model Complexity & Bias-Variance Tradeoff

### Effect of Model Complexity

$$\text{Bias}^2 \uparrow \quad \text{as model complexity} \downarrow$$

- Simple model (e.g., linear regression): High bias, low variance
- Complex model (e.g., high-degree polynomial): Low bias, high variance

### Learning Curves (Diagnosis Tool)
Learning curves plot **Error** vs. **Training Set Size (m)**. They are the best way to diagnose if your model has a bias problem or a variance problem.

#### 1. High Bias (Underfitting)
*The model is too simple. Even with more data, it can't learn the pattern.*
```text
Error
 ^
 |    /--- (High) Validation Error
 |   /
 |  /------ plateau
 |  \------ plateau
 |   \--- (High) Training Error
 |
 +-----------------------------> Training Set Size (m)
```
*   **Key Sign:** Both Training and Validation error are **High**.
*   **Key Sign:** They are very close to each other (the gap is small).
*   **Fix:** More data will **NOT** help. You need a more complex model or better features.

#### 2. High Variance (Overfitting)
*The model memorized the training data but fails to generalize.*
```text
Error
 ^
 |  /------------------- (High) Validation Error
 | /
 |/   (Huge Gap)
 |
 |
 |  \------------------- (Low) Training Error
 |
 +-----------------------------> Training Set Size (m)
```
*   **Key Sign:** Large **Gap** between Training and Validation error.
*   **Key Sign:** Training error is very low (fits data perfectly).
*   **Fix:** More data **WILL** help (it closes the gap). Also, try regularization or simplifying the model.

#### 3. Good Fit (The Goal)
*   **Key Sign:** Low error for both curves.
*   **Key Sign:** Small gap between them.
*   **Key Sign:** Error plateaus at a low, acceptable level.

---

## 6. Bias-Variance in Different Algorithms

| Algorithm | Typical Bias | Typical Variance | Best For |
|-----------|------------|-----------------|----------|
| **Linear Regression** | High (assumes linearity) | Low | Simple linear patterns |
| **Polynomial Regression (high degree)** | Low | High | Complex patterns, small data |
| **Neural Networks** | Low | High (if complex) | Any pattern (if enough data) |
| **Decision Trees** | Low | High | Non-linear, interpretability |
| **Random Forests** | Medium | Low | Robust, handles overfitting |
| **Regularized models** (Ridge, Lasso) | Medium | Medium | Tradeoff control |

---

## 7. Strategies to Reduce Bias & Variance

### Reduce Bias (Underfitting)

| Strategy | Mechanism | Example |
|----------|-----------|---------|
| **Increase model complexity** | Use more powerful model | Switch from linear to polynomial |
| **Add more features** | Provide more information | Engineer new features |
| **Reduce regularization** | Weaken bias-inducing constraints | Decrease $\lambda$ |
| **More training time** | Optimize better | Train for more epochs |

### Reduce Variance (Overfitting)

| Strategy | Mechanism | Example |
|----------|-----------|---------|
| **Simplify model** | Use fewer parameters | Reduce polynomial degree |
| **Collect more data** | Reduce per-sample impact | Larger dataset |
| **Regularization** | Penalize complex solutions | Increase $\lambda$ |
| **Dropout** | Random zeroing of units | Add dropout to network |
| **Early stopping** | Stop before overfitting | Monitor validation error |
| **Ensemble methods** | Average multiple models | Bagging, boosting |

---

## 8. Practical Diagnosis

### How to Detect High Bias vs. High Variance?

```
Train Error  |  Interpretation
Small        |  Low bias ✓
Large        |  High bias → increase complexity
             |
Test Error   |  
Small        |  Good fit ✓
Large        |  Could be:
             |    - High bias (train also large)
             |    - High variance (train small)
```

### Decision Tree
1. Is train error small?
   - **No:** High bias → increase complexity
   - **Yes:** Continue to 2
2. Is test error small?
   - **Yes:** Good fit ✓
   - **No:** High variance → get more data, regularize

---

## 9. Exam Questions

### Conceptual
1. Explain bias and variance. Why is there a tradeoff?
2. A model achieves 98% train accuracy and 40% test accuracy. Is this high bias or high variance? How to fix?
3. As we increase model complexity, how do bias and variance change?

### Derivation-Based
1. **Derive** the bias-variance decomposition starting from squared error.
2. **Show** that bias increases and variance decreases as we add regularization.

### Trick/Failure Cases
1. Train error = 0.1, Test error = 0.11. Good or bad fit? Next step?
2. You reduce $\lambda$ in Ridge regression. Which increases: bias or variance?

---

## 10. Key Takeaways

- **Error decomposition:** $E_{\text{test}} = \text{Bias}^2 + \text{Variance} + \text{Noise}$
- **Bias:** Systematic error (underfitting); model too simple
- **Variance:** Sensitivity to training data (overfitting); model too complex
- **Tradeoff:** Can't minimize both simultaneously
- **Bias ↑** as model simplicity ↑; **Variance ↓** as training size ↑
- **Diagnosis:** High train error → bias; Low train, high test error → variance
- **Strategies:** Increase complexity for bias, get more data or regularize for variance

---
