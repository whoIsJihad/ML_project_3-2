# 📘 Data Preprocessing

## 1. Core Idea (Intuition)

**Raw data** is often:
- **Different scales:** Age $\in [0, 100]$, Income $\in [0, 10^6]$
- **Different distributions:** Skewed, bimodal, outliers
- **Missing values:** Incomplete records
- **Categorical:** Non-numeric features

**Preprocessing fixes these** to make learning efficient and stable.

---

## 2. Normalization (Min-Max Scaling)

### Formula
$$X_{\text{norm}} = \frac{X - X_{\min}}{X_{\max} - X_{\min}}$$

Result: $X_{\text{norm}} \in [0, 1]$

### When to Use
- **Neural networks:** Essential; brings all features to same scale
- **Distance-based algorithms:** KNN, K-means (sensitive to scale)
- **Output layer:** For binary classification, output is normalized to $[0, 1]$

### Problems
- **Outliers affect range:** If one sample has age = 200, $X_{\max}$ becomes huge
- **Test data scaling:** Fit on training data, apply same min/max to test data (important!)

### Critical: Train vs Test Preprocessing

**WRONG approach:**
```
Fit min/max on TRAINING set
Fit min/max on TEST set (separately)  ← NO! Data leakage!
```

**CORRECT approach:**
```
Fit min/max on TRAINING set ONLY → save these values
Apply same min/max to TEST set → use saved values
```

Why? Because the test set is "unseen" data. You shouldn't learn anything from it (including its range).

### Example

```
TRAINING SET: Age ∈ [18, 70]
Compute: X_min = 18, X_max = 70
Saving these values!

NORMALIZATION FORMULA: (Age - 18) / 52

APPLYING TO TEST SET:
  Test sample with age = 25: (25 - 18) / 52 ≈ 0.13 ✓ (in [0,1])
  Test sample with age = 75: (75 - 18) / 52 ≈ 1.1 ✓ (outside [0,1], OK!)
  Test sample with age = 10: (10 - 18) / 52 ≈ -0.15 ✓ (outside [0,1], OK!)

All use X_min=18, X_max=70 from training data (never recomputed).
```

**Key insight:** Test data CAN go outside [0,1] because it's extrapolating beyond training range. This is expected and correct behavior.

---

## 3. Standardization (Z-Score Normalization)

### Formula
$$X_{\text{std}} = \frac{X - \mu}{\sigma}$$

Result: $X_{\text{std}}$ has $\mu = 0$, $\sigma = 1$ (unit normal)

where:
- $\mu = \frac{1}{n}\sum_i X_i$ (mean)
- $\sigma = \sqrt{\frac{1}{n}\sum_i (X_i - \mu)^2}$ (standard deviation)

### When to Use
- **Linear/Logistic Regression:** Helps interpret coefficients (units are now in "standard deviations")
- **Gradient-based optimization:** Smoother loss landscape
- **Algorithms assuming normality:** Many statistical methods

### Advantage over Normalization
- **Robust to outliers:** Outlier doesn't change $\sigma$ much (unlike range)
- **Unbounded:** No artificial [0,1] constraint

### Example
```
Age: [20, 25, 30, 35, 40]
μ = 30, σ = 7.07

Standardized: [-1.41, -0.71, 0, 0.71, 1.41]
Even if outlier = 100:
  New σ ≈ 28.9 (increased moderately)
  Still interpretable
```

---

## 4. Feature Scaling Comparison

| Method | Formula | Range | When to Use |
|--------|---------|-------|-------------|
| **Normalization** | $(X - \min) / (\max - \min)$ | $[0, 1]$ | Neural networks, all features on same bounded scale |
| **Standardization** | $(X - \mu) / \sigma$ | $(-\infty, \infty)$ | Linear/Logistic Regression, gradient-based optimization |

---

## 5. Missing Value Imputation

### Strategy 1: Mean Imputation
$$X_{\text{imputed}} = X_{\text{mean}}$$

Replace missing values with column mean.

**Pros:** 
- Simple and fast to implement
- Doesn't remove any samples (useful when data is limited)

**Cons:** 
- **Underestimates variance:** If original data had spread (high variance), replacing with mean artificially reduces it. This makes the model think the feature is more "certain" than it actually is, leading to overconfident predictions.
- **Loses relationships:** If a feature is correlated with other features, using just the mean ignores those relationships. Example: if Height and Weight are correlated, imputing Height with overall mean doesn't account for a person's actual Weight.

### Strategy 2: Forward/Backward Fill (Time Series)
$$X_{\text{imputed}} = X_{t-1} \text{ (last known value)}$$

For time-series data, use previous value.

**Pros:** 
- Preserves temporal structure; assumes data changes gradually over time
- Works well for time series where consecutive values are correlated (e.g., stock prices, temperature)

**Cons:** 
- Only works for ordered/time-series data
- Doesn't work for random missing values
- If values change abruptly, this method propagates stale information

### Strategy 3: KNN Imputation
$$X_{\text{imputed}} = \text{mean of } k \text{ nearest neighbors}$$

Find $k$ most similar samples (by other features), average their values for missing feature.

**Pros:** 
- Uses relationships between features; context-aware imputation
- Example: For missing Age with Weight=100kg, finds people with similar weight and imputes their average age (much better than global mean age)
- More realistic than mean imputation

**Cons:** 
- Computationally expensive; must search through all samples for each missing value
- Requires choosing $k$; small $k$ can be noisy, large $k$ can be too smooth
- Doesn't work well if many features are missing (hard to find "similar" samples)

### Strategy 4: Deletion
Remove rows/columns with missing values.

**Pros:** 
- Simple, no need to guess or invent data
- No bias introduced; model only sees real data
- Guarantees no information loss from imputation

**Cons:** 
- Loss of data; reduces sample size which hurts model training
- If missing values are not random, deletion introduces bias (e.g., if only rich people skip the income question, you bias your dataset toward poor people)

### When to Use Each

| Missing % | Method | Why This Percentage? |
|-----------|--------|----------------------|
| $< 5\%$ | **Delete rows** | Small enough that deleting doesn't hurt sample size; missing data is negligible |
| $5\%$ to $20\%$ | **Mean / KNN imputation** | Can't delete (lose too much data); imputation doesn't introduce significant bias |
| $> 20\%$ | **Domain expertise** | Too much missing data; model can't recover. Investigate WHY data is missing; may indicate measurement error or data quality issues |

---

## 6. Categorical Feature Encoding

### One-Hot Encoding
For categorical variable $X \in \{\text{Red, Green, Blue}\}$:

$$\begin{array}{ccc}
\text{Red} & \to & [1, 0, 0] \\
\text{Green} & \to & [0, 1, 0] \\
\text{Blue} & \to & [0, 0, 1]
\end{array}$$

**Pros:** 
- Works with all algorithms; no false ordering
- Example: "Red" and "Blue" are not ranked; they're just different

**Cons:** 
- Increases dimensionality; $k$ categories become $k$ features
- Creates sparse data (lots of zeros); can be memory-intensive with many categories
- Creates multicollinearity: if you know a sample is not Red and not Green, it must be Blue (the features are not independent)

### Label Encoding
$$\text{Red} \to 0, \quad \text{Green} \to 1, \quad \text{Blue} \to 2$$

**Pros:** 
- Compact; only 1 column instead of 3
- No increase in dimensionality

**Cons:** 
- Induces false ordering: model thinks Green (1) is "between" Red (0) and Blue (2), even though they're unrelated
- Misleads distance-based algorithms: KNN thinks Blue is closer to Green than to Red based on numeric values (distance 1 vs 2), when all three colors should be equally "far" apart

### When to Use
- **Tree-based models:** Can handle label encoding directly
- **Neural networks, KNN:** Use one-hot encoding

---

## 7. Outlier Detection & Handling

### Statistical Method: Z-Score
Outlier if $|z_i| > 3$ (approximately):
$$z_i = \frac{X_i - \mu}{\sigma}$$

### IQR Method
Outlier if $X_i < Q1 - 1.5 \cdot \text{IQR}$ or $X_i > Q3 + 1.5 \cdot \text{IQR}$

where $\text{IQR} = Q3 - Q1$ (interquartile range).

### Handling
| Approach | When |
|----------|------|
| **Delete** | Clearly measurement errors |
| **Cap/Clip** | Extreme but plausible values |
| **Model separately** | If outliers are meaningful signal |

---

## 8. Pitfalls & Common Mistakes

| Mistake | Why Wrong | Fix |
|---------|-----------|-----|
| **Fit preprocessing on all data** | Leaks test set information; preprocessing parameters (min/max, mean/std) are learned from test data, making train/test comparison invalid. You can't assess true performance on unseen data. | Fit ONLY on training set; save parameters; apply same parameters to test set |
| **Not handling missing values** | Many algorithms require complete data; missing values cause crashes or undefined operations in distance calculations or matrix multiplications | Impute or delete before training (choose method based on % missing) |
| **Scaling categorical as numeric** | Assigns fake distances between categories; KNN thinks category 2 is closer to category 1 than to category 3, even though they're all equally different | Use one-hot encoding for neural networks or distance-based algorithms |
| **Forgetting to scale test data** | Test predictions are on different scale than training; model learned patterns on scale [0,1] but makes predictions on scale [100, 1000]. Metrics become misleading. | Apply same preprocessing (fitted on training) to test set |

---

## 9. Exam Questions

### Conceptual
1. Why is normalization to $[0, 1]$ better than no scaling for neural networks?
2. When would standardization be preferable to normalization?
3. If your training data has age range $[18, 70]$, and a test sample is age 150, what happens after normalization?

### Derivation-Based
1. **Derive** the formula for standardization. Show that if $X_i' = (X_i - \mu) / \sigma$, then $\mathbb{E}[X'] = 0$ and $\text{Var}(X') = 1$.
2. **Show** that mean imputation reduces variance. Why is this a problem?

### Trick/Failure Cases
1. You normalize age to $[0,1]$ using training set. Test set has one age = 500. Model explodes. Why?
2. Dataset has 1000 features, 90% are missing. Strategy?

---

## 10. Key Takeaways

- **Normalization:** $(X - \min) / (\max - \min) \in [0, 1]$; use for neural networks
- **Standardization:** $(X - \mu) / \sigma$ (mean 0, std 1); use for linear models and gradient-based optimization
- **Always fit preprocessing on training set only** → apply same parameters to test set
- **Missing values:** Delete ($< 5\%$), mean/KNN imputation ($5\%-20\%$), investigate ($> 20\%$)
- **Categorical:** One-hot for neural networks, label encoding for trees
- **Outliers:** Z-score or IQR detection; delete if error, cap if plausible
- **Feature scaling essential for:** Neural networks, linear regression, gradient-based optimization, distance-based algorithms

---
