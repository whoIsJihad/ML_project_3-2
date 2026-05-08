# 📝 Data Preprocessing & Regularization - Exam Answers

## Data Preprocessing

### Normalization vs Standardization

**Normalization:** $X' = \frac{X - X_{\min}}{X_{\max} - X_{\min}} \in [0,1]$
- When: All features naturally bounded (e.g., age, percentage)
- Pros: Interpretable (0=minimum, 1=maximum)

**Standardization:** $X' = \frac{X - \mu}{\sigma}$ (mean=0, std=1)
- When: Features from different distributions
- Pros: Works for unbounded data; mean-centered

**Why needed:** 
- Neural networks: weights initialize ≈ N(0, σ²); unnormalized data → extreme activations → training fails
- Distance-based (KNN, K-means): features with large range dominate
- Optimization: helps learning rates (gradients more stable)

### Out-of-Distribution Test Data

If test sample has value outside training range:
- Example: Train on age [18,70], test sample age=150
- Normalization: $X' = \frac{150-18}{70-18} = 2.18$ (out of [0,1]!)
- Model extrapolates (unreliable)

**Solution:** Use standardization (unbounded). Or clip test to train range.

### Missing Value Imputation

- **Mean imputation:** Replace missing with mean
  - Pro: Simple
  - Con: Reduces variance → model underconfident

- **KNN imputation:** Replace with mean of K nearest neighbors
  - Pro: Preserves structure
  - Con: Expensive

- **Drop rows:** Remove samples with missing values
  - Pro: No bias
  - Con: Lose data

---

## Regularization

### Q1: Why does L1 cause exact sparsity while L2 doesn't?

**Intuition:**

L1 penalty: $\lambda |w|$ 
L2 penalty: $\lambda w^2$

In 2D (w₁, w₂ plane):

```
L1 constraint: |w₁| + |w₂| ≤ C  (diamond shape)
L2 constraint: w₁² + w₂² ≤ C     (circle shape)
```

Loss surface (centered at optimum without regularization):

```
        |w₂
        |
    ◇   |   ◇    (L1: diamond corners at axes)
  ◇   ○ | ○   ◇  (L2: circle)
────────●────────  w₁
  ◇   ○ | ○   ◇
    ◇   |   ◇
```

When loss contours hit constraint:
- **L1 (diamond):** Corners point directly at axes → hits w₁=0 (exact zero)
- **L2 (circle):** Smooth curve → hits interior (w₁≠0, w₂≠0)

**Mathematically:**

L1 gradient at w=0⁺: $\nabla |w| = \pm 1$ (jump discontinuity)
L2 gradient at w=0: $\nabla w² = 0$ (continuous)

L1 can "cut off" a weight completely; L2 just shrinks.

### Q2: In dropout with p=0.5, why scale activations by (1-p)=0.5 at test?

**Why scale:**

Training: 50% neurons dropped randomly
- Network sees: ~50% of neurons active
- Expected value of sum: $E[h] = 0.5 \times \text{full network output}$

Test (no dropout): 100% neurons active
- Expected value: $2 \times \text{training expectation}$
- Predictions blow up (2× larger)

**Solution:** Scale by (1-p) = 0.5 at test
- Restore original expected value
- Predictions stay calibrated

**Alternative:** Inverted dropout (scale during training, not test)

---

## Evaluation Metrics

### Confusion Matrix

```
              Predicted
              Pos    Neg
Actual Pos    TP     FN
       Neg    FP     TN
```

- **TP (True Positive):** Correctly predicted positive
- **FP (False Positive):** Incorrectly predicted positive (Type I error)
- **FN (False Negative):** Missed positive (Type II error)
- **TN (True Negative):** Correctly predicted negative

---

### Key Metrics

**Accuracy:** $\frac{TP+TN}{TP+TN+FP+FN}$ — overall correctness (misleading on imbalanced data)

**Precision:** $\frac{TP}{TP+FP}$ — when predicting positive, how often right?
- Use: Spam detection (don't spam good emails)

**Recall:** $\frac{TP}{TP+FN}$ — found all positives?
- Use: Disease screening (don't miss sick people)

**F1-score:** $2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision + Recall}}$ — harmonic mean
- Use: Balanced metric when precision/recall both matter

**AUC-ROC:** Area under precision-recall curve
- Threshold-independent evaluation
- 0.5 = random, 1.0 = perfect

---

### Why Accuracy Misleading?

**Spam detection example:**
- 1000 emails, 10 spam (1% positive rate)
- Model: always predict "not spam"
- Accuracy: 990/1000 = 99%
- But catches 0 spam! (recall = 0)

**Solution:** Use precision/recall or F1-score.

---

## Bias-Variance Decomposition

### Error = Bias² + Variance + Noise

**Bias:** Model consistently wrong
- Simple model on complex data → high bias
- Example: Linear fit on nonlinear data

**Variance:** Model changes with different training sets
- Complex model → high variance
- Example: Deep neural network

**Noise:** Irreducible error (data labels noisy)
- Cannot improve below this

### Learning Curves

```
Error
   |     ──── Test Error
   |   /
   | /
   |/───────── Train Error
   |________________________________ Training Set Size
```

- High bias: Train and test error both high, close together
- High variance: Train error low, test error high, large gap

**Fix high bias:** More complex model, more features, reduce regularization
**Fix high variance:** More data, simpler model, increase regularization

---

