# 📘 Data Preprocessing: Normalization, Standardization, Feature Scaling, Missing Value Imputation

## 1. Core Idea (Intuition)

* **Problem it solves:** Raw data is messy — features have different scales (age: 0-100, salary: 10K-1M), missing values, different units. Models (especially gradient-based) struggle with this.
* **Why needed:** If features have wildly different scales, gradient descent is inefficient (elongated elliptical loss surface). Missing values crash most algorithms. Preprocessing makes data "learnable."
* **Key insight:** Garbage in, garbage out. No model can fix bad data. Preprocessing is often more impactful than model choice.

---

## 2. Mathematical Formulation

### Normalization (Min-Max Scaling)

Rescale each feature to a fixed range, typically [0, 1]:

```
x_norm = (x - x_min) / (x_max - x_min)
```

Where:
- `x_min` = minimum value of feature in training set
- `x_max` = maximum value of feature in training set
- Output range: [0, 1]

To scale to arbitrary range [a, b]:
```
x_scaled = a + (x - x_min)(b - a) / (x_max - x_min)
```

### Standardization (Z-score Normalization)

Transform each feature to have mean=0 and standard deviation=1:

```
x_std = (x - μ) / σ
```

Where:
- `μ` = mean of feature in training set
- `σ` = standard deviation of feature in training set
- Output: centered at 0, most values in [-3, 3]

### Feature Scaling — When to Use What:

| Method | Output Range | Preserves Zero? | Sensitive to Outliers? | When to Use |
|---|---|---|---|---|
| Min-Max | [0, 1] | No | Yes (min/max shift) | Bounded features, neural networks (sigmoid/tanh inputs) |
| Standardization | Unbounded (centered at 0) | Yes (if mean ≈ 0) | Less (uses mean/std) | Gaussian-like data, gradient descent, SVM, PCA |
| Max Abs Scaling | [-1, 1] | Yes | Moderate | Sparse data (preserves zeros) |
| Robust Scaling | Uses median/IQR | Yes | No (ignores outliers) | Data with many outliers |

**Robust Scaling:**
```
x_robust = (x - median) / IQR
```
Where IQR = Q3 - Q1 (interquartile range). Outliers don't affect median or IQR.

### Missing Value Imputation

| Method | How | When to Use |
|---|---|---|
| **Mean imputation** | Replace missing with feature mean | Numerical, roughly symmetric data |
| **Median imputation** | Replace with median | Numerical, skewed data / outliers |
| **Mode imputation** | Replace with most frequent value | Categorical features |
| **Forward/Backward fill** | Use previous/next value | Time series |
| **KNN imputation** | Use K nearest neighbors' values | When feature correlations exist |
| **Model-based** | Train a model to predict missing values | Complex missing patterns |
| **Drop rows** | Remove examples with missing values | Very few missing values (<5%) |
| **Drop features** | Remove feature entirely | >50% values missing |

**Critical rule:** Compute imputation statistics (mean, median, min, max) on **training set only**. Apply the same values to test set. Otherwise you leak test information into training → overly optimistic results.

---

## 3. Algorithm / Training Procedure

```
TRAINING:
    1. Split data into train/test (BEFORE any preprocessing!)
    2. Handle missing values (compute stats on train, apply to both)
    3. Compute scaling parameters on training set:
       - For normalization: x_min, x_max per feature
       - For standardization: μ, σ per feature
    4. Transform training set
    5. Store scaling parameters

INFERENCE:
    1. Handle missing values using training statistics
    2. Apply SAME scaling parameters from training
       (Do NOT recompute min/max or mean/std on test data!)
```

**Why not recompute on test set?**
- Test set represents unseen data. In production, you have one sample at a time.
- Recomputing statistics on test data → data leakage → model seems better than it is.

---

## 4. Optimization / Learning Dynamics

**How preprocessing affects gradient descent:**

Without scaling (feature 1: range [0, 1], feature 2: range [0, 1000]):
- Loss surface is a stretched ellipse
- Gradient in feature 2 direction is huge, feature 1 direction is tiny
- GD oscillates across feature 2, crawls along feature 1
- Need very small learning rate → slow convergence

With scaling (both features: range [0, 1]):
- Loss surface is roughly circular
- Gradients are balanced across features
- GD goes straight toward minimum
- Can use larger learning rate → fast convergence

**This is why standardization is so important for:**
- Neural networks (any gradient-based model)
- SVM (distance-based)
- KNN (distance-based)
- PCA (variance-based)

**Models that DON'T need scaling:**
- Decision trees (split on thresholds, scale-invariant)
- Random forests
- Naive Bayes

---

## 5. Failure Cases / Limitations

| Failure | Why |
|---|---|
| Computing stats on test set | Data leakage. Inflated performance metrics. |
| Min-Max with outliers | Single outlier shifts min or max → everything compressed into a tiny range |
| Mean imputation on skewed data | Mean ≠ center of distribution → biased imputation |
| Imputing too many values | If 50% of feature is missing, imputed values are basically noise |
| Not scaling for gradient models | Convergence is extremely slow or fails entirely |
| Scaling for tree models | Unnecessary, wastes time (trees don't care about scale) |

---

## 6. Where It Works Well

* **Standardization:** Default choice for most ML models. Always safe.
* **Normalization:** When you need bounded inputs (image pixels → [0,1], sigmoid inputs)
* **Robust scaling:** Datasets with significant outliers
* **Mean/Median imputation:** Quick-and-dirty baseline for missing values
* **KNN imputation:** When features are correlated and you want better imputation quality

---

## 7. Variants / Extensions

| Variant | What it does |
|---|---|
| **Log transform** | For heavily right-skewed features (income, population). Makes distribution more Gaussian. |
| **Box-Cox transform** | Generalized power transform to normalize distributions |
| **One-hot encoding** | Convert categorical features to binary vectors |
| **Target encoding** | Replace category with mean of target variable (risky — can leak) |
| **MICE** | Multiple Imputation by Chained Equations — iterative model-based imputation |

---

## 8. Comparison Table

| Method | Handles Outliers | Preserves Distribution | Bounded Output | Best For |
|---|---|---|---|---|
| Min-Max | No | Somewhat | Yes [0,1] | Neural nets, bounded activations |
| Standardization | Somewhat | Yes (just shifts) | No | General purpose, gradient models |
| Robust Scaling | Yes | Somewhat | No | Outlier-heavy data |
| Log Transform | Yes (compresses) | No (changes shape) | No | Right-skewed distributions |

---

## 9. Exam Questions

### Conceptual:
1. Why must scaling parameters be computed on the training set only? What happens if you include the test set?
2. When would you choose normalization over standardization? Give a specific example.
3. A feature has values [1, 2, 3, 4, 1000]. Compare the effect of min-max vs standardization vs robust scaling.

### Derivation-based:
4. Show that after standardization, the feature has μ=0 and σ=1. Start from the formula and prove both properties.
5. Derive the min-max normalization formula for scaling to arbitrary range [a, b]. Show that x_min maps to a and x_max maps to b.

### Trick / Failure-case:
6. You standardized your entire dataset before splitting into train/test. Your test accuracy is 95%. After fixing the pipeline (standardize on train only), accuracy drops to 82%. Why?
7. You used mean imputation for a feature with values [1, 1, 1, 1, 100, NaN, NaN]. Is this a good idea? What would you use instead?

---

## 10. Key Takeaways

* Preprocessing is often more impactful than model selection. Never skip it.
* Standardization (z-score) is the safest default. Use it for gradient-based models, SVM, PCA.
* Min-Max normalization for bounded outputs. Watch out for outliers.
* Robust scaling (median/IQR) when outliers are present.
* **NEVER compute statistics on test data.** Fit on train, transform both.
* Missing value strategy depends on: % missing, feature type, data distribution.
* Tree-based models don't need feature scaling (but every other model likely does).
