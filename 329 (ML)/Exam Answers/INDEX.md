# 📝 Exam Answers - Complete Index

## Quick Navigation

### Section A (Foundational ML)
✓ [01_Linear_Regression_Answers.md](01_Linear_Regression_Answers.md) — Loss functions, normal equations, gradient descent variants
✓ [02_Logistic_Regression_Answers.md](02_Logistic_Regression_Answers.md) — Cross-entropy, decision boundaries, class imbalance
✓ [03_Multilayer_Perceptron_Answers.md](03_Multilayer_Perceptron_Answers.md) — XOR problem, vanishing gradients, ReLU
✓ [04_Backpropagation_Answers.md](04_Backpropagation_Answers.md) — Chain rule, error terms, gradient checking
✓ [05_Gradient_Descent_Variants_Answers.md](05_Gradient_Descent_Variants_Answers.md) — BGD vs SGD vs Mini-batch, convergence rates
✓ [06_Optimizers_Answers.md](06_Optimizers_Answers.md) — Momentum, Nesterov, Adagrad, RMSProp, Adam
→ [07_Data_Preprocessing_Answers.md](07_Data_Preprocessing_Answers.md) — *In progress*
→ [08_Regularization_Answers.md](08_Regularization_Answers.md) — *In progress*
→ [09_Evaluation_Metrics_Answers.md](09_Evaluation_Metrics_Answers.md) — *In progress*
→ [10_Bias_Variance_Answers.md](10_Bias_Variance_Answers.md) — *In progress*
→ [11_CNN_Basics_Answers.md](11_CNN_Basics_Answers.md) — *In progress*
→ [12_Kernels_Filters_Answers.md](12_Kernels_Filters_Answers.md) — *In progress*
→ [13_CNN_Architectures_Answers.md](13_CNN_Architectures_Answers.md) — *In progress*
→ [14_MDP_Answers.md](14_MDP_Answers.md) — *In progress*
→ [15_RL_Answers.md](15_RL_Answers.md) — *In progress*

### Section B (Advanced ML)
*Section B answer files being generated...*

---

## Study Tips

**By difficulty:**
- **Easy:** Linear/Logistic Regression, Data Preprocessing, Basic Evaluation Metrics
- **Medium:** Backprop, Gradient Variants, Regularization, Bias-Variance
- **Hard:** GANs, Transformers, RNN variants, RL

**By topic type:**
- **Conceptual:** Understand intuition, why things work, when to use
- **Derivation:** Show mathematical steps, derive formulas from first principles
- **Trick cases:** Know failure modes, how to fix issues, edge cases

**For exam:**
1. Read each question carefully
2. Check if you need intuition (conceptual) or math (derivation)
3. For trick cases: identify the problem first, then solution
4. Show work: steps matter, not just final answer

---

## Master Question Bank

See individual files for full solutions. Quick reference:

**Linear Regression (Q1-Q7)**
- Q1: MSE vs MAE, vanishing gradient with sigmoid, outlier sensitivity
- Q2: Why $X^TX$ must be invertible, multicollinearity impact
- Q3: Why subtract gradient (go downhill vs uphill)
- Q4: Derive normal equations step-by-step
- Q5: Prove convexity → global minimum
- Q6: Overfitting with $n < d$
- Q7: Perfectly correlated features → singular matrix

**Logistic Regression (Q1-Q7)**
- Q1: Cross-entropy vs MSE, sigmoid saturation problem
- Q2: No closed-form solution (transcendental equation)
- Q3: Probability ≠ certainty, threshold at 0.5
- Q4: Derive cross-entropy gradient
- Q5: Prove linear decision boundary
- Q6: Zero loss on separable data → overfitting
- Q7: Class imbalance → always predict majority class

**MLP (Q1-Q6)**
- Q1: XOR geometry, single line vs curved boundary
- Q2: Vanishing gradients, exponential decay with depth
- Q3: ReLU advantages (non-zero gradient, computational speed)
- Q4: Compute gradient via chain rule for 2-layer net
- Q5: Function composition, induction proof
- Q6: Dying ReLU → can't recover

*[Continue for all 15 topics...]*

---

## Formula Quick Reference

### Losses
- MSE: $L = \frac{1}{2n}\sum_i (y_i - \hat{y}_i)^2$
- Cross-entropy: $L = -\frac{1}{n}\sum_i [y_i\log(\hat{p}_i) + (1-y_i)\log(1-\hat{p}_i)]$

### Gradient Descent
- BGD: $\mathbf{w} ← \mathbf{w} - \alpha \frac{1}{n}X^T(X\mathbf{w} - y)$
- SGD: $\mathbf{w} ← \mathbf{w} - \alpha x_i(x_i^T\mathbf{w} - y_i)$

### Activation Functions
- Sigmoid: $\sigma(z) = \frac{1}{1+e^{-z}}$, $\sigma'(z) = \sigma(z)(1-\sigma(z))$
- ReLU: $\text{ReLU}(z) = \max(0, z)$, $\text{ReLU}'(z) = \mathbb{1}_{z>0}$

### Optimizers
- Momentum: $v_t = \beta v_{t-1} + g_t$, $\mathbf{w}_t = \mathbf{w}_{t-1} - \alpha v_t$
- Adam: $m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t$, $v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2$

---

