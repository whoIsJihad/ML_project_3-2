# 📘 Evaluation Metrics

## 1. Core Idea (Intuition)

**Accuracy alone is misleading:**

Example: Predicting rare disease in 1M people, 100 actually sick.
- Model predicts "not sick" for all: Accuracy = 99.99%
- But completely useless!

**Different metrics** measure different aspects of performance.

---

## 2. Classification Metrics

### Confusion Matrix

$$\begin{array}{c|cc}
& \text{Predicted} = 1 & \text{Predicted} = 0 \\
\hline
\text{Actual} = 1 & \text{TP} & \text{FN} \\
\text{Actual} = 0 & \text{FP} & \text{TN}
\end{array}$$

where:
- **TP (True Positive):** Predicted 1, actually 1 ✓
- **FP (False Positive):** Predicted 1, actually 0 ✗
- **FN (False Negative):** Predicted 0, actually 1 ✗
- **TN (True Negative):** Predicted 0, actually 0 ✓

---

### Accuracy
$$\text{Accuracy} = \frac{\text{TP} + \text{TN}}{\text{TP} + \text{FP} + \text{FN} + \text{TN}} = \frac{\text{Correct Predictions}}{\text{Total}}$$

**Interpretation:** Fraction of all predictions that are correct.

**When to use:** Balanced datasets.

**Problem:** Ignores class imbalance.

---

### Precision
$$\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}$$

**Interpretation:** Of all predicted positives, how many are actually positive?

**Question:** "When I predict 1, how often am I correct?"

**When to use:** 
- Minimize false alarms (spam detection, medical false positives)
- When cost of FP is high

---

### Recall (Sensitivity)
$$\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$

**Interpretation:** Of all actual positives, how many did we catch?

**Question:** "When the truth is 1, how often do I predict it?"

**When to use:**
- Minimize missed cases (disease detection, fraud)
- When cost of FN is high

---

### F1-Score (Harmonic Mean)
$$F_1 = 2 \cdot \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2 \cdot \text{TP}}{2 \cdot \text{TP} + \text{FP} + \text{FN}}$$

**Interpretation:** Single metric balancing precision and recall.

**Why harmonic mean?** Heavily penalizes imbalance (if precision or recall is 0, $F_1 = 0$).

**When to use:** Default metric for imbalanced classification.

---

### Specificity (True Negative Rate)
$$\text{Specificity} = \frac{\text{TN}}{\text{TN} + \text{FP}}$$

**Interpretation:** Of all actual negatives, how many did we correctly identify?

**When to use:** When false positives are costly.

---

## 3. Comparison Table

| Metric | Formula | Range | Use Case | Interprets |
|--------|---------|-------|----------|-----------|
| **Accuracy** | $\frac{\text{TP+TN}}{n}$ | $[0, 1]$ | Balanced data | Overall correctness |
| **Precision** | $\frac{\text{TP}}{\text{TP+FP}}$ | $[0, 1]$ | FP costly | Positive pred accuracy |
| **Recall** | $\frac{\text{TP}}{\text{TP+FN}}$ | $[0, 1]$ | FN costly | Capture rate |
| **F1** | $2 \frac{P \cdot R}{P+R}$ | $[0, 1]$ | Imbalanced data | Balanced P-R |
| **Specificity** | $\frac{\text{TN}}{\text{TN+FP}}$ | $[0, 1]$ | TN important | Negative pred accuracy |

---

## 4. ROC Curve & AUC

### ROC (Receiver Operating Characteristic)
Plot **True Positive Rate (TPR)** vs. **False Positive Rate (FPR)**:

$$\text{TPR} = \text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}$$

$$\text{FPR} = \frac{\text{FP}}{\text{TN} + \text{FP}}$$

As we vary the **decision threshold** $t$ from 0 to 1:
- At $t = 0$: predict all 1 → TPR = 1, FPR = 1 (right corner)
- At $t = 1$: predict all 0 → TPR = 0, FPR = 0 (left corner)
- At $t = 0.5$ (default): one point on curve

**Interpretation:** ROC curve shows tradeoff between catching positives (TPR) and false alarms (FPR).

### AUC (Area Under the Curve)
Area under ROC curve, $\text{AUC} \in [0, 1]$.

| AUC | Interpretation |
|-----|----------------|
| 0.5 | Random guessing |
| 0.7 - 0.8 | Decent |
| 0.8 - 0.9 | Good |
| > 0.9 | Excellent |

**When to use:** Imbalanced data; need threshold-independent metric.

---

## 5. Precision-Recall Curve

Plot **Recall** vs. **Precision** as threshold varies.

**Advantage over ROC:** Better for **imbalanced datasets** (ROC can be misleading with 99% negatives).

---

---

## 6. Multi-Class Metrics (The "Perspective" Problem)

When you have more than 2 classes (e.g., Cat, Dog, Bird), you calculate a separate F1-score for each class. To get one final number for your model, you must "average" them. How you average matters:

### 1. Macro-Averaging (The "Democracy" View)
Calculate the F1 for each class, then take the simple average.
- **Formula:** $(F1_{Cat} + F1_{Dog} + F1_{Bird}) / 3$
- **Analogy:** Every class gets **one vote**, regardless of how many samples it has.
- **When to use:** When you care about small classes just as much as big ones.

### 2. Micro-Averaging (The "Population" View)
Count all TPs, FPs, and FNs from all classes together first, then calculate one final F1.
- **Analogy:** Every **sample** gets one vote.
- **Key Note:** In multi-class settings, **Micro-F1 is usually equal to Accuracy.**
- **When to use:** When you want to see the overall correctness across all samples.

### 3. Weighted-Averaging (The "Proportional" View)
Average the F1-scores, but give more "weight" to classes with more samples.
- **Formula:** $\sum (F1_{i} \times \text{Percent of data in class } i)$
- **When to use:** When you want a balance between Macro and Micro.

### Concrete Example
Imagine 100 images: **90 Cats, 5 Dogs, 5 Birds.**
- **Case A:** Model gets all 90 Cats right, but misses all Dogs and Birds.
    - **Macro-F1:** Low (0.33). It penalizes you heavily for failing the small classes (Dogs/Birds).
    - **Micro-F1:** High (0.90). It sees that 90/100 samples are correct and is happy.

---

## 7. Regression Metrics

### Mean Squared Error (MSE)
$$\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (\hat{y}_i - y_i)^2$$

**Unit:** Squared units of target. Sensitive to outliers.

### Root Mean Squared Error (RMSE)
$$\text{RMSE} = \sqrt{\text{MSE}}$$

**Unit:** Same as target. More interpretable than MSE.

### Mean Absolute Error (MAE)
$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |\hat{y}_i - y_i|$$

**Unit:** Same as target. Robust to outliers (unlike RMSE).

### R² (Coefficient of Determination)
$$R^2 = 1 - \frac{\sum_i (y_i - \hat{y}_i)^2}{\sum_i (y_i - \bar{y})^2}$$

**Interpretation:** Fraction of variance explained by model.

| $R^2$ | Quality |
|-------|---------|
| 0.9 - 1.0 | Excellent |
| 0.7 - 0.9 | Good |
| 0.5 - 0.7 | Fair |
| < 0.5 | Poor |

---

## 8. Choosing the Right Metric

| Problem | Best Metric(s) |
|---------|-----------------|
| Balanced classification | **Accuracy, F1** |
| Imbalanced classification | **F1, AUC, Precision-Recall** |
| Minimize false positives | **Precision** (and adjust threshold) |
| Minimize false negatives | **Recall** (and adjust threshold) |
| Regression, no outliers | **RMSE, MAE** |
| Regression, with outliers | **MAE, R²** |
| Multi-class imbalanced | **Macro-F1 or Weighted-F1** |

---

## 9. Exam Questions

### Conceptual
1. Why is accuracy misleading for imbalanced datasets? Give an example.
2. What's the difference between precision and recall? When would you optimize for one vs. the other?
3. What does AUC = 0.5 mean? What does AUC = 1.0 mean?

### Derivation-Based
1. **Derive** F1-score from precision and recall. Why use harmonic mean instead of arithmetic mean?
2. **Show** that accuracy = (TP + TN) / n can be misleading when classes are imbalanced.

### Trick/Failure Cases
1. Spam detection: 99% accuracy but model predicts "not spam" for all emails. Good or bad?
2. ROC-AUC = 0.95 on imbalanced test set (1% positive). Is this impressive?

---

## 10. Key Takeaways

- **Confusion matrix:** TP, FP, FN, TN are building blocks for all metrics
- **Accuracy:** Overall correctness; misleading for imbalanced data
- **Precision:** $\text{TP} / (\text{TP} + \text{FP})$; minimize false alarms
- **Recall:** $\text{TP} / (\text{TP} + \text{FN})$; minimize missed cases
- **F1:** Harmonic mean of precision and recall; default for imbalanced
- **AUC-ROC:** Threshold-independent; good for imbalanced data
- **Regression:** RMSE/MAE for errors, $R^2$ for variance explained
- **Choose metric based on cost of errors, not just accuracy**

---
