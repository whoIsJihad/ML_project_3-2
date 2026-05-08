# Ensemble Learning: A First-Principles Guide

## Table of Contents
1. [Philosophy of Ensemble Learning](#1-philosophy-of-ensemble-learning)
2. [Bias-Variance Tradeoff: The Foundation](#2-bias-variance-tradeoff-the-foundation)
3. [Parallel Methods: Bagging](#3-parallel-methods-bagging)
4. [Random Forests: Enhanced Bagging](#4-random-forests-enhanced-bagging)
5. [Sequential Methods: Boosting](#5-sequential-methods-boosting)
6. [AdaBoost: Adaptive Boosting](#6-adaboost-adaptive-boosting)
7. [Gradient Boosting: Function Space Optimization](#7-gradient-boosting-function-space-optimization)
8. [XGBoost: Regularized Gradient Boosting](#8-xgboost-regularized-gradient-boosting)
9. [Summary Comparison](#9-summary-comparison)

---

## 1. Philosophy of Ensemble Learning

### 1.1 Why Ensemble Methods?

**The Core Question**: Why would combining multiple "weak" models produce a "strong" model?

**The Intuition**: Think of decision-making by committee. If you ask 100 independent experts a question, and each expert is correct more than 50% of the time, the majority vote will be highly accurate. This is the **wisdom of crowds** principle.

**Three Key Conditions for Success**:
1. **Diversity**: Models must make different kinds of errors (uncorrelated errors)
2. **Independence**: Models should be trained on different data or use different features
3. **Better-than-random**: Each model must be at least slightly better than random guessing

### 1.2 Two Fundamental Strategies

**Parallel Ensembles** (Bagging):
- Train models independently in parallel
- Each model sees a different "view" of data
- Combine via averaging (regression) or voting (classification)
- **Goal**: Reduce variance while maintaining bias

**Sequential Ensembles** (Boosting):
- Train models sequentially, each correcting previous errors
- Later models focus on "hard" examples
- Combine via weighted sum
- **Goal**: Reduce both bias and variance (primarily bias)

---

## 2. Bias-Variance Tradeoff: The Foundation

### 2.1 Why We Care

For any learning algorithm, the expected prediction error can be decomposed as:

$$
\text{Expected Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Error}
$$

**Bias**: Error from incorrect assumptions in the model (underfitting)
- High bias → model is too simple
- Example: Using linear regression for non-linear data

**Variance**: Error from sensitivity to small fluctuations in training data (overfitting)
- High variance → model is too complex
- Example: Deep decision tree that memorizes training noise

### 2.2 How Ensembles Address This

**Bagging's Effect**:
- ✓ Reduces variance (averaging decorrelates errors)
- ✗ Does not reduce bias (averaging biased estimates stays biased)
- Best for: High-variance models (deep trees)

**Boosting's Effect**:
- ✓ Reduces bias (sequentially corrects errors)
- ✓ Can reduce variance (if regularized properly)
- ⚠ Risk: Can increase variance if overtrained
- Best for: High-bias models (shallow trees)

**Mathematical Insight**: 

For $n$ independent, identically distributed models with variance $\sigma^2$:

$$
\text{Var}\left(\frac{1}{n}\sum_{i=1}^{n} f_i\right) = \frac{\sigma^2}{n}
$$

As $n \to \infty$, variance $\to 0$. But if models are correlated with correlation $\rho$:

$$
\text{Var}\left(\frac{1}{n}\sum_{i=1}^{n} f_i\right) = \rho\sigma^2 + \frac{1-\rho}{n}\sigma^2
$$

Even with infinite models, variance stays at $\rho\sigma^2$. **This is why model diversity matters!**

---

## 3. Parallel Methods: Bagging

### 3.1 The Core Idea

**Bagging** = **B**ootstrap **Agg**regat**ing**

**Why Bagging?**
1. We want multiple diverse models
2. But we only have one dataset
3. Solution: Create multiple datasets via **bootstrapping**

### 3.2 Bootstrap Sampling

**Bootstrapping**: Sample $n$ points from original dataset of size $n$ **with replacement**

**Why with replacement?**
- Without replacement → you just get the same dataset
- With replacement → each bootstrap sample is different
- Creates diversity while maintaining data distribution

### 3.3 Mathematical Proof: Bootstrap Selection Probability

**Question**: What fraction of original data appears in each bootstrap sample?

**Proof**:

For a dataset of size $n$, when we sample $n$ times with replacement:
- Probability a specific point is **selected** in one draw: $\frac{1}{n}$
- Probability it is **not selected** in one draw: $1 - \frac{1}{n}$
- Probability it is **not selected** in $n$ draws: $\left(1 - \frac{1}{n}\right)^n$

Therefore, probability it **is selected** at least once:

$$
P(\text{selected}) = 1 - \left(1 - \frac{1}{n}\right)^n
$$

As $n \to \infty$, recall that:

$$
\lim_{n \to \infty} \left(1 - \frac{1}{n}\right)^n = \lim_{n \to \infty} \left[\left(1 - \frac{1}{n}\right)^{-n}\right]^{-1} = e^{-1}
$$

Therefore:

$$
P(\text{selected}) = 1 - e^{-1} = 1 - 0.368 \approx 0.632
$$

**Interpretation**: 
- About **63.2%** of original data appears in each bootstrap sample
- About **36.8%** is left out (called "Out-Of-Bag" or OOB samples)
- OOB samples can be used for validation without a separate test set!

### 3.4 Bagging Algorithm

**The Big Picture (In Plain English)**:

Imagine you're trying to predict house prices. Instead of training one model, you:
1. **Create many versions of your dataset** by randomly sampling (with replacement)
2. **Train one model on each version** - each model sees slightly different data
3. **When predicting**, ask all models and take the average (for numbers) or vote (for categories)

**Why this works**: Each model makes different mistakes because they see different data. When you average, the mistakes cancel out!

---

**Step-by-Step Algorithm**:

**TRAINING PHASE:**

```
Start with: Your original dataset (say 1000 data points)
            A model type (like Decision Tree)
            Number of models you want (say 100)

For each model (1 to 100):
    Step 1: Create a new dataset
            - Randomly pick 1000 points from your original 1000
            - BUT: Put each point back after picking (replacement!)
            - Result: Some points appear multiple times, some don't appear
            
    Step 2: Train a model on this new dataset
            - Model 1 trained on Version 1 of data
            - Model 2 trained on Version 2 of data
            - ... and so on
            
    Store this model
```

**PREDICTION PHASE:**

```
When you get a new data point to predict:

For REGRESSION (predicting numbers like price, temperature):
    - Ask Model 1: "What's your prediction?" → 150
    - Ask Model 2: "What's your prediction?" → 148  
    - Ask Model 3: "What's your prediction?" → 152
    - ... ask all 100 models
    - Final prediction = Average = (150 + 148 + 152 + ...) / 100
    
For CLASSIFICATION (predicting categories like spam/not spam):
    - Ask Model 1: "What's your prediction?" → Spam
    - Ask Model 2: "What's your prediction?" → Not Spam
    - Ask Model 3: "What's your prediction?" → Spam
    - ... ask all 100 models
    - Final prediction = Majority vote
      (If 65 models say "Spam" and 35 say "Not Spam" → predict "Spam")
```

---

**Formal Algorithm** (for reference):

```
Input: 
    - Dataset D = {(x₁, y₁), ..., (xₙ, yₙ)}
    - Base learner L (e.g., Decision Tree)
    - Number of models B (e.g., 100)

Training:
    For b = 1 to B:
        1. Create bootstrap sample Dᵦ by sampling n points from D with replacement
        2. Train model fᵦ = L(Dᵦ)
        3. Store fᵦ
    
Prediction for new point x:
    - Regression: ŷ = (1/B) Σᵦ₌₁ᴮ fᵦ(x)        [average of all predictions]
    - Classification: ŷ = majority_vote{f₁(x), f₂(x), ..., fᴮ(x)}
```

**Key Insight**: You're trading one complex, unstable model for many simple models whose predictions you combine. The combination is more stable than any individual model!

### 3.5 Mini-Simulation: Bagging with Toy Dataset

**Dataset** (5 points):

| Index | x | y |
|-------|---|---|
| 1 | 1 | 2 |
| 2 | 2 | 4 |
| 3 | 3 | 6 |
| 4 | 4 | 8 |
| 5 | 5 | 10 |

**Base Learner**: Simple rule - predict mean of training y-values

**Bootstrap Samples** (3 models):

**Bootstrap Sample 1**: [1, 1, 3, 4, 5]
- Data points: (1,2), (1,2), (3,6), (4,8), (5,10)
- Model 1 prediction: $f_1(x) = \text{mean}(2,2,6,8,10) = 5.6$

**Bootstrap Sample 2**: [2, 2, 2, 3, 5]
- Data points: (2,4), (2,4), (2,4), (3,6), (5,10)
- Model 2 prediction: $f_2(x) = \text{mean}(4,4,4,6,10) = 5.6$

**Bootstrap Sample 3**: [1, 2, 4, 4, 5]
- Data points: (1,2), (2,4), (4,8), (4,8), (5,10)
- Model 3 prediction: $f_3(x) = \text{mean}(2,4,8,8,10) = 6.4$

**Bagged Prediction**:
$$
\hat{y}_{\text{bagged}} = \frac{1}{3}(5.6 + 5.6 + 6.4) = \frac{17.6}{3} = 5.87
$$

**Single Model** (trained on all data):
$$
f(x) = \text{mean}(2,4,6,8,10) = 6.0
$$

**Observation**: 
- The bagged model gives 5.87 vs. single model 6.0
- The difference comes from sampling variation
- With more trees (B→∞) and proper base learners (e.g., decision trees), variance reduction becomes significant

**Variance Analysis**:
- Single model variance: High (if base learner is complex like deep tree)
- Bagged variance: $\text{Var}(\text{average}) \approx \frac{\text{Var}(single)}{B} \times (1 + (B-1)\rho)$
- If $\rho$ (correlation) is low, variance reduction is substantial

---

## 4. Random Forests: Enhanced Bagging

### 4.1 Why Random Forests?

**Problem with Standard Bagging (especially with trees)**:
- Bootstrap samples are still correlated
- Trees tend to split on the same strong features
- If one feature is very predictive, all bagged trees will use it first
- High correlation $\rho$ → limited variance reduction

**Solution**: **Feature Randomness**

### 4.2 The Key Innovation

At each split in each tree:
- Select random subset of $m$ features from total $p$ features
- Consider only these $m$ features for splitting
- **Typical choice**: $m = \sqrt{p}$ for classification, $m = p/3$ for regression

**Why this works**:
- Forces trees to be more diverse
- Even if one feature is strongest, it won't always be available
- Reduces correlation $\rho$ between trees
- Remember: $\text{Var}_{\text{ensemble}} = \rho\sigma^2 + \frac{1-\rho}{n}\sigma^2$
- Lower $\rho$ → better variance reduction!

### 4.3 Random Forest Algorithm

```
Input: Dataset D, Number of trees B, Features per split m

For b = 1 to B:
    1. Create bootstrap sample Dᵦ
    2. Grow tree Tᵦ:
       - At each node:
         a. Randomly select m features from p total features
         b. Find best split among these m features only
         c. Split the node
       - Do not prune (grow trees fully)
    
Prediction:
    - Regression: ŷ = (1/B) Σᵦ Tᵦ(x)
    - Classification: ŷ = majority_vote{T₁(x), ..., Tᵦ(x)}
```

### 4.4 Why Not Prune Trees?

**Conventional wisdom**: Prune trees to prevent overfitting

**Random Forest approach**: Grow fully, don't prune

**Why?**
1. Individual trees have **high variance** (good! → more diversity)
2. Individual trees have **low bias** (good! → accurate on average)
3. Averaging removes the variance
4. Pruning would increase bias without enough benefit

This is bias-variance tradeoff in action:
$$
\text{Error}_{\text{RF}} = \underbrace{\text{Bias}^2}_{\text{low (deep trees)}} + \underbrace{\text{Variance}}_{\text{reduced by averaging}} + \text{Noise}
$$

### 4.5 Feature Importance

**Out-of-Bag (OOB) Error**:
- For each tree, ~37% of data wasn't used in training
- Use OOB samples as validation set (free cross-validation!)

**Permutation Importance**:
1. Compute baseline OOB error
2. For each feature $j$:
   - Randomly permute feature $j$ in OOB samples
   - Compute new OOB error
   - Importance of $j$ = increase in error
3. Features causing large error increases are important

**Why this works**: Permuting breaks the relationship between feature and target. If error increases a lot, that feature was important.

---

## 5. Sequential Methods: Boosting

### 5.1 The Philosophical Shift

**Bagging**: "Train many models independently and average"
- Parallel approach
- Each model is equally weighted
- Reduces variance

**Boosting**: "Train models sequentially, each fixing previous errors"
- Sequential approach
- Models have different weights
- Focuses on hard examples
- Reduces bias (and sometimes variance)

### 5.2 The Core Intuition

Think of learning to shoot basketballs:
1. First attempt: You miss in various ways
2. Second attempt: Focus on the misses, adjust technique
3. Third attempt: Focus on remaining errors
4. Continue until expert

**Boosting does this with models**:
- Model 1: Learns overall pattern
- Model 2: Focuses on where Model 1 failed
- Model 3: Focuses on where Models 1+2 failed
- Combine: Weighted sum of all models

### 5.3 Weight Updates: Why?

**Question**: How do we make models "focus on hard examples"?

**Answer**: Increase the weight/importance of misclassified points

After training model $m$:
- Points correctly classified → decrease weight (we got them)
- Points misclassified → increase weight (need more attention)

Next model sees these weights → effectively focuses on hard examples.

---

## 6. AdaBoost: Adaptive Boosting

### 6.1 AdaBoost Algorithm (Classification)

**Goal**: Combine weak learners to create strong learner

**Weak Learner**: Classifier that's slightly better than random (accuracy > 50%)

**Algorithm**:

```
Input: Dataset D = {(x₁, y₁), ..., (xₙ, yₙ)}, yᵢ ∈ {-1, +1}
       Base learner L, Number of rounds T

Initialize: w₁(i) = 1/n for all i = 1,...,n

For t = 1 to T:
    1. Train weak learner hₜ on D with weights wₜ
    
    2. Calculate weighted error:
       εₜ = Σᵢ wₜ(i) · 𝟙[hₜ(xᵢ) ≠ yᵢ] / Σᵢ wₜ(i)
    
    3. Calculate model weight:
       αₜ = (1/2) ln((1 - εₜ) / εₜ)
    
    4. Update sample weights:
       wₜ₊₁(i) = wₜ(i) · exp(-αₜ · yᵢ · hₜ(xᵢ))
    
    5. Normalize: wₜ₊₁(i) = wₜ₊₁(i) / Σⱼ wₜ₊₁(j)

Final classifier:
    H(x) = sign(Σₜ αₜ · hₜ(x))
```

### 6.2 Understanding the Components

**Why weighted error $\epsilon_t$?**
- We want the learner to focus on examples with high weights
- Weighted error measures performance on current "priority" examples

**Why $\alpha_t = \frac{1}{2}\ln\frac{1-\epsilon_t}{\epsilon_t}$?**
- If $\epsilon_t$ is small (good classifier) → $\alpha_t$ is large (big influence)
- If $\epsilon_t = 0.5$ (random) → $\alpha_t = 0$ (no influence)
- If $\epsilon_t > 0.5$ (worse than random) → $\alpha_t < 0$ (flip its prediction!)

**Graph of $\alpha$ vs $\epsilon$**:

| $\epsilon_t$ | $\alpha_t$ | Interpretation |
|-------------|-----------|----------------|
| 0.1 | 1.10 | Excellent classifier, high weight |
| 0.2 | 0.69 | Good classifier |
| 0.3 | 0.42 | Decent classifier |
| 0.4 | 0.20 | Weak classifier |
| 0.5 | 0.00 | Random, no contribution |

**Why $w_{t+1}(i) = w_t(i) \cdot \exp(-\alpha_t \cdot y_i \cdot h_t(x_i))$?**

Consider the product $y_i \cdot h_t(x_i)$:
- If correct: $y_i = h_t(x_i)$ → product = +1 → $\exp(-\alpha_t)$ → weight **decreases**
- If wrong: $y_i \neq h_t(x_i)$ → product = -1 → $\exp(+\alpha_t)$ → weight **increases**

Magnitude of change depends on $\alpha_t$ (how good the classifier was).

### 6.3 Mathematical Proof: AdaBoost Minimizes Exponential Loss

**Claim**: AdaBoost performs coordinate descent on exponential loss function.

**Exponential Loss**:

$$
L = \sum_{i=1}^{n} \exp\left(-y_i \sum_{t=1}^{T} \alpha_t h_t(x_i)\right)
$$

**Proof Strategy**: Show that at iteration $t$, choosing $\alpha_t$ as AdaBoost prescribes minimizes the loss.

At iteration $t$, we've already fixed $\alpha_1, ..., \alpha_{t-1}$. Define:

$$
F_{t-1}(x_i) = \sum_{s=1}^{t-1} \alpha_s h_s(x_i)
$$

The loss after adding $h_t$ with weight $\alpha_t$ is:

$$
L_t(\alpha_t) = \sum_{i=1}^{n} \exp(-y_i(F_{t-1}(x_i) + \alpha_t h_t(x_i)))
$$

Let $w_t(i) = \exp(-y_i F_{t-1}(x_i))$ (this is the unnormalized weight at step $t$):

$$
L_t(\alpha_t) = \sum_{i=1}^{n} w_t(i) \exp(-y_i \alpha_t h_t(x_i))
$$

Split the sum into correct and incorrect predictions:

$$
L_t(\alpha_t) = \sum_{y_i = h_t(x_i)} w_t(i) \exp(-\alpha_t) + \sum_{y_i \neq h_t(x_i)} w_t(i) \exp(\alpha_t)
$$

Let:
- $W_{\text{correct}} = \sum_{y_i = h_t(x_i)} w_t(i)$
- $W_{\text{wrong}} = \sum_{y_i \neq h_t(x_i)} w_t(i)$
- $W_{\text{total}} = W_{\text{correct}} + W_{\text{wrong}}$
- Weighted error: $\epsilon_t = \frac{W_{\text{wrong}}}{W_{\text{total}}}$

Then $W_{\text{correct}} = W_{\text{total}}(1 - \epsilon_t)$ and $W_{\text{wrong}} = W_{\text{total}} \epsilon_t$

$$
L_t(\alpha_t) = W_{\text{total}}[(1-\epsilon_t)e^{-\alpha_t} + \epsilon_t e^{\alpha_t}]
$$

To minimize, take derivative with respect to $\alpha_t$ and set to zero:

$$
\frac{dL_t}{d\alpha_t} = W_{\text{total}}[-(1-\epsilon_t)e^{-\alpha_t} + \epsilon_t e^{\alpha_t}] = 0
$$

$$
\epsilon_t e^{\alpha_t} = (1-\epsilon_t)e^{-\alpha_t}
$$

$$
\frac{\epsilon_t}{1-\epsilon_t} = e^{-2\alpha_t}
$$

$$
\ln\frac{\epsilon_t}{1-\epsilon_t} = -2\alpha_t
$$

$$
\alpha_t = \frac{1}{2}\ln\frac{1-\epsilon_t}{\epsilon_t}
$$

**This is exactly the $\alpha_t$ used in AdaBoost!** ✓

**Second Derivative Check**:

$$
\frac{d^2L_t}{d\alpha_t^2} = W_{\text{total}}[(1-\epsilon_t)e^{-\alpha_t} + \epsilon_t e^{\alpha_t}] > 0
$$

This is positive, confirming we have a minimum.

**Training Error Bound**:

With this choice of $\alpha_t$, the training error can be bounded:

$$
\text{Training Error} \leq \exp\left(-2\sum_{t=1}^{T}(1/2 - \epsilon_t)^2\right)
$$

As long as each weak learner has $\epsilon_t < 1/2$ (better than random), the bound shows exponential decrease in training error. This is why AdaBoost is so powerful!

### 6.4 Mini-Simulation: AdaBoost Step-by-Step

**Dataset** (5 points, binary classification):

| Index | x | y |
|-------|---|---|
| 1 | 1 | -1 |
| 2 | 2 | -1 |
| 3 | 3 | +1 |
| 4 | 4 | +1 |
| 5 | 5 | +1 |

**Base Learner**: Decision stump (one-level tree): $h(x) = \text{sign}(x - \theta)$

---

**Round 1**:

**Initial weights**: $w_1(i) = 1/5 = 0.2$ for all $i$

**Train**: Find best threshold $\theta$

Try $\theta = 2.5$: $h_1(x) = \text{sign}(x - 2.5)$
- Predictions: [-1, -1, +1, +1, +1]
- Correct: [✓, ✓, ✓, ✓, ✓]
- Weighted error: $\epsilon_1 = 0$

(This is a perfect classifier on this toy data, but let's use $\theta = 1.5$ to make it interesting)

Try $\theta = 1.5$: $h_1(x) = \text{sign}(x - 1.5)$
- Predictions: [-1, +1, +1, +1, +1]
- Correct: [✓, ✗, ✓, ✓, ✓]
- Weighted error: $\epsilon_1 = 0.2$

**Model weight**:
$$
\alpha_1 = \frac{1}{2}\ln\frac{1-0.2}{0.2} = \frac{1}{2}\ln(4) = 0.693
$$

**Update weights**:

For point 1: correct → $w_2(1) = 0.2 \times \exp(-0.693 \times (-1) \times (-1)) = 0.2 \times e^{-0.693} = 0.1$

For point 2: **wrong** → $w_2(2) = 0.2 \times \exp(-0.693 \times (-1) \times (+1)) = 0.2 \times e^{0.693} = 0.4$

For point 3: correct → $w_2(3) = 0.2 \times e^{-0.693} = 0.1$

For point 4: correct → $w_2(4) = 0.2 \times e^{-0.693} = 0.1$

For point 5: correct → $w_2(5) = 0.2 \times e^{-0.693} = 0.1$

**Sum**: $0.1 + 0.4 + 0.1 + 0.1 + 0.1 = 0.8$

**Normalize**:
- $w_2(1) = 0.1/0.8 = 0.125$
- $w_2(2) = 0.4/0.8 = 0.500$ ← Highest weight (misclassified point)
- $w_2(3) = 0.1/0.8 = 0.125$
- $w_2(4) = 0.1/0.8 = 0.125$
- $w_2(5) = 0.1/0.8 = 0.125$

---

**Round 2**:

**Weights**: [0.125, 0.500, 0.125, 0.125, 0.125]

**Train**: Find best threshold with new weights

Point 2 now has weight 0.5, so it's critical to classify it correctly.

Try $\theta = 2.5$: $h_2(x) = \text{sign}(x - 2.5)$
- Predictions: [-1, -1, +1, +1, +1]
- Weighted error: $\epsilon_2 = 0$ (all correct)

**Model weight**:
$$
\alpha_2 = \frac{1}{2}\ln\frac{1-0}{0} \to \infty
$$

(In practice, we'd set a small $\epsilon_{\min}$ to avoid infinity, or stop here)

For illustration, assume $\epsilon_2 = 0.05$:
$$
\alpha_2 = \frac{1}{2}\ln\frac{0.95}{0.05} = \frac{1}{2}\ln(19) = 1.47
$$

**Final Classifier**:
$$
H(x) = \text{sign}(0.693 \cdot h_1(x) + 1.47 \cdot h_2(x))
$$

For $x = 2$: $H(2) = \text{sign}(0.693 \times 1 + 1.47 \times (-1)) = \text{sign}(-0.777) = -1$ ✓

**Observation**: 
- Point 2 was initially misclassified
- Its weight increased from 0.2 to 0.5
- The second learner focused on getting it right
- The ensemble corrected the mistake!

---

## 7. Gradient Boosting: Function Space Optimization

### 7.1 The Paradigm Shift

**AdaBoost**: Reweight samples, minimize exponential loss

**Gradient Boosting**: General framework for any differentiable loss function

**Key Insight**: Think of ensemble as a function:

$$
F(x) = \sum_{t=1}^{T} f_t(x)
$$

We want to find $F$ that minimizes loss:

$$
L(F) = \sum_{i=1}^{n} \ell(y_i, F(x_i))
$$

**Traditional optimization**: Minimize $L(\mathbf{w})$ by updating parameters $\mathbf{w}$ via gradient descent:

$$
\mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} - \eta \nabla_{\mathbf{w}} L
$$

**Gradient Boosting**: Minimize $L(F)$ by updating function $F$ via "gradient descent in function space":

$$
F^{(t+1)} = F^{(t)} - \eta \nabla_{F} L
$$

But $\nabla_F L$ is not a direction in parameter space—it's a function! We approximate it with a new model.

### 7.2 Understanding "Gradient Descent in Function Space"

At iteration $t$, we have current model $F_{t-1}$. We want to add a function $f_t$ to improve it:

$$
F_t = F_{t-1} + \eta f_t
$$

where $\eta$ is the learning rate.

**Question**: What should $f_t$ be?

**Answer**: $f_t$ should point in the direction that most reduces loss.

For each training point $i$, the derivative of loss with respect to the prediction is:

$$
-\frac{\partial \ell(y_i, F_{t-1}(x_i))}{\partial F_{t-1}(x_i)} = \text{"residual" or "pseudo-residual"}
$$

Let's call this $r_i$:

$$
r_i = -\frac{\partial \ell(y_i, F_{t-1}(x_i))}{\partial F_{t-1}(x_i)}
$$

**Ideal step**: We want $f_t(x_i) = r_i$ for all $i$.

But we can't fit every point exactly. So we train $f_t$ to predict these residuals:

$$
f_t = \arg\min_f \sum_{i=1}^{n} (r_i - f(x_i))^2
$$

This is just regression on the residuals!

### 7.3 Different Loss Functions

**Squared Loss** (Regression):

$$
\ell(y, F(x)) = \frac{1}{2}(y - F(x))^2
$$

$$
-\frac{\partial \ell}{\partial F(x)} = y - F(x) = \text{residual}
$$

Gradient boosting with squared loss = fit each tree to residuals!

**Absolute Loss** (Robust Regression):

$$
\ell(y, F(x)) = |y - F(x)|
$$

$$
-\frac{\partial \ell}{\partial F(x)} = \text{sign}(y - F(x))
$$

**Logistic Loss** (Binary Classification):

$$
\ell(y, F(x)) = \ln(1 + \exp(-y F(x))), \quad y \in \{-1, +1\}
$$

$$
-\frac{\partial \ell}{\partial F(x)} = \frac{y}{1 + \exp(y F(x))}
$$

### 7.4 Gradient Boosting Algorithm

```
Input: Dataset D = {(x₁, y₁), ..., (xₙ, yₙ)}
       Loss function ℓ(y, F(x))
       Number of iterations M
       Learning rate η

Initialize: F₀(x) = arg min_γ Σᵢ ℓ(yᵢ, γ)
           (Constant prediction that minimizes loss)

For t = 1 to M:
    1. Compute pseudo-residuals:
       rᵢ = -∂ℓ(yᵢ, F_{t-1}(xᵢ)) / ∂F_{t-1}(xᵢ)  for i = 1,...,n
    
    2. Fit base learner to residuals:
       fₜ = arg min_f Σᵢ (rᵢ - f(xᵢ))²
    
    3. Update model:
       Fₜ(x) = F_{t-1}(x) + η · fₜ(x)

Final model: F_M(x)
```

### 7.5 Mini-Simulation: Gradient Boosting (Squared Loss)

**Dataset** (5 points):

| Index | x | y |
|-------|---|---|
| 1 | 1 | 2 |
| 2 | 2 | 4 |
| 3 | 3 | 6 |
| 4 | 4 | 8 |
| 5 | 5 | 10 |

**Base Learner**: Simple stumps (constant prediction in each region)

**Loss**: Squared loss, Learning rate $\eta = 0.5$

---

**Initialization**:

$$
F_0(x) = \arg\min_{\gamma} \sum_i (y_i - \gamma)^2 = \text{mean}(y) = \frac{2+4+6+8+10}{5} = 6
$$

All predictions: [6, 6, 6, 6, 6]

---

**Iteration 1**:

**Compute residuals**:
$$
r_i = y_i - F_0(x_i)
$$

| i | $y_i$ | $F_0(x_i)$ | $r_i$ |
|---|-------|-----------|-------|
| 1 | 2 | 6 | -4 |
| 2 | 4 | 6 | -2 |
| 3 | 6 | 6 | 0 |
| 4 | 8 | 6 | 2 |
| 5 | 10 | 6 | 4 |

**Fit tree to residuals**:

Best split at $x = 3$:
- Left (x ≤ 3): predict mean(-4, -2, 0) = -2
- Right (x > 3): predict mean(2, 4) = 3

Tree $f_1(x)$:
```
if x ≤ 3: return -2
else: return 3
```

**Update**:
$$
F_1(x) = F_0(x) + 0.5 \cdot f_1(x)
$$

| i | $x_i$ | $F_0(x_i)$ | $f_1(x_i)$ | $F_1(x_i)$ |
|---|-------|-----------|-----------|-----------|
| 1 | 1 | 6 | -2 | 5 |
| 2 | 2 | 6 | -2 | 5 |
| 3 | 3 | 6 | -2 | 5 |
| 4 | 4 | 6 | 3 | 7.5 |
| 5 | 5 | 6 | 3 | 7.5 |

**Loss**: 
$$
L_1 = \sum_i (y_i - F_1(x_i))^2 = (2-5)^2 + (4-5)^2 + (6-5)^2 + (8-7.5)^2 + (10-7.5)^2 = 9 + 1 + 1 + 0.25 + 6.25 = 17.5
$$

Initial loss: $L_0 = \sum_i (y_i - 6)^2 = 16 + 4 + 0 + 4 + 16 = 40$

**Improvement**: $40 \to 17.5$ (56% reduction!)

---

**Iteration 2**:

**New residuals**:

| i | $y_i$ | $F_1(x_i)$ | $r_i$ |
|---|-------|-----------|-------|
| 1 | 2 | 5 | -3 |
| 2 | 4 | 5 | -1 |
| 3 | 6 | 5 | 1 |
| 4 | 8 | 7.5 | 0.5 |
| 5 | 10 | 7.5 | 2.5 |

**Fit tree**: Best split at $x = 2.5$:
- Left (x ≤ 2.5): predict mean(-3, -1) = -2
- Right (x > 2.5): predict mean(1, 0.5, 2.5) = 1.33

**Update**:
$$
F_2(x) = F_1(x) + 0.5 \cdot f_2(x)
$$

And so on... Each iteration reduces loss further by fitting to residuals.

**Key Observation**: Each new tree corrects the errors of the previous ensemble, gradually approaching the true function.

---

## 8. XGBoost: Regularized Gradient Boosting

### 8.1 Motivation

**Standard Gradient Boosting limitations**:
1. No explicit regularization → prone to overfitting
2. Doesn't account for tree complexity
3. Can be slow and memory-intensive

**XGBoost innovations**:
1. Regularized objective function
2. Second-order derivatives (Newton's method)
3. Efficient implementation (weighted quantile sketch, cache-aware access, sparsity awareness)

### 8.2 The Regularized Objective

At iteration $t$, we want to add tree $f_t$ to minimize:

$$
\mathcal{L}^{(t)} = \sum_{i=1}^{n} \ell(y_i, F_{t-1}(x_i) + f_t(x_i)) + \Omega(f_t)
$$

where $\Omega(f_t)$ is the **regularization term** (this is the key difference!):

$$
\Omega(f_t) = \gamma T + \frac{1}{2}\lambda \sum_{j=1}^{T} w_j^2
$$

- $T$ = number of leaves in tree $f_t$
- $w_j$ = score/prediction in leaf $j$
- $\gamma$ = penalty for each leaf (encourages fewer splits)
- $\lambda$ = L2 penalty on leaf weights (shrinks predictions)

**Why this matters**:
- Standard GBM: Only cares about fitting training data
- XGBoost: Balances fit vs. tree complexity
- Prevents overly complex trees that overfit

### 8.3 Second-Order Taylor Approximation

To optimize, XGBoost uses second-order Taylor expansion:

$$
\ell(y_i, F_{t-1}(x_i) + f_t(x_i)) \approx \ell(y_i, F_{t-1}(x_i)) + g_i f_t(x_i) + \frac{1}{2} h_i f_t^2(x_i)
$$

where:
- $g_i = \frac{\partial \ell(y_i, F_{t-1}(x_i))}{\partial F_{t-1}(x_i)}$ (first derivative = gradient)
- $h_i = \frac{\partial^2 \ell(y_i, F_{t-1}(x_i))}{\partial F_{t-1}(x_i)^2}$ (second derivative = Hessian)

**Why second-order?**
- Standard GBM uses only first derivative (gradient descent)
- XGBoost uses first AND second derivative (Newton's method)
- Newton's method converges faster and is more accurate

### 8.4 Optimal Leaf Weights

For a tree structure with leaves $\{1, 2, ..., T\}$, let $I_j$ be the set of instances in leaf $j$.

After dropping constants and simplifying with Taylor approximation:

$$
\mathcal{L}^{(t)} \approx \sum_{j=1}^{T} \left[ \left(\sum_{i \in I_j} g_i\right) w_j + \frac{1}{2} \left(\sum_{i \in I_j} h_i + \lambda\right) w_j^2 \right] + \gamma T
$$

This is a quadratic in $w_j$. Taking derivative and setting to zero:

$$
\frac{\partial \mathcal{L}^{(t)}}{\partial w_j} = \sum_{i \in I_j} g_i + \left(\sum_{i \in I_j} h_i + \lambda\right) w_j = 0
$$

**Optimal weight for leaf $j$**:

$$
w_j^* = -\frac{\sum_{i \in I_j} g_i}{\sum_{i \in I_j} h_i + \lambda}
$$

**Minimum achievable loss** (given tree structure):

$$
\mathcal{L}^{(t)*} = -\frac{1}{2} \sum_{j=1}^{T} \frac{\left(\sum_{i \in I_j} g_i\right)^2}{\sum_{i \in I_j} h_i + \lambda} + \gamma T
$$

### 8.5 Split Finding

**Question**: When should we split a leaf?

**Gain from splitting** leaf $I$ into left $I_L$ and right $I_R$:

$$
\text{Gain} = \frac{1}{2} \left[ \frac{(\sum_{i \in I_L} g_i)^2}{\sum_{i \in I_L} h_i + \lambda} + \frac{(\sum_{i \in I_R} g_i)^2}{\sum_{i \in I_R} h_i + \lambda} - \frac{(\sum_{i \in I} g_i)^2}{\sum_{i \in I} h_i + \lambda} \right] - \gamma
$$

- First two terms: Loss with split
- Third term: Loss without split
- $-\gamma$: Penalty for adding a leaf

**Split decision**:
- If Gain > 0: Make the split
- If Gain ≤ 0: Don't split (regularization stops us!)

**This is the key regularization mechanism**: $\gamma$ prevents splits that don't sufficiently improve the objective.

### 8.6 XGBoost vs. Standard Gradient Boosting

| Feature | Standard GBM | XGBoost |
|---------|-------------|---------|
| **Regularization** | None explicitly | $\Omega(f) = \gamma T + \frac{1}{2}\lambda \sum w_j^2$ |
| **Optimization** | First-order (gradient) | Second-order (gradient + Hessian) |
| **Split criterion** | Impurity reduction | Regularized gain |
| **Leaf weights** | Mean of residuals | $w_j^* = -\frac{\sum g_i}{\sum h_i + \lambda}$ |
| **Overfitting** | More prone | Less prone |
| **Speed** | Slower | Faster (better algorithms) |

### 8.7 Mini Example: XGBoost Regularization Effect

**Dataset**: [Same 5-point dataset from before]

**Suppose without regularization**:
- Best split has gain = 0.8
- Creates 2 leaves with complex patterns

**With regularization** ($\gamma = 0.5, \lambda = 1$):
- Penalized gain = $0.8 - 0.5 = 0.3$
- Might prevent the split if gain is small
- Leaf weights shrunk by $\lambda$: $w_j^* = -\frac{g_j}{h_j + 1}$ vs. $w_j = -\frac{g_j}{h_j}$

**Effect**:
- Simpler trees (fewer leaves)
- Smaller predictions (shrunk weights)
- Better generalization

This is why **XGBoost often dominates Kaggle competitions**: it balances fit and complexity optimally!

---

## 9. Summary Comparison

### 9.1 Quick Reference Table

| Method | Training | Diversity Source | Bias | Variance | Speed | Overfitting Risk |
|--------|----------|------------------|------|----------|-------|------------------|
| **Bagging** | Parallel | Bootstrap samples | No change | ↓↓ | Fast | Low (if base is complex) |
| **Random Forest** | Parallel | Bootstrap + feature sampling | No change | ↓↓↓ | Fast | Very low |
| **AdaBoost** | Sequential | Reweighting | ↓↓ | ↓ | Moderate | Medium-High |
| **Gradient Boosting** | Sequential | Residual fitting | ↓↓ | ↓ | Slow | High |
| **XGBoost** | Sequential | Residual + regularization | ↓↓ | ↓ | Fast | Low-Medium |

### 9.2 When to Use What?

**Use Bagging/Random Forest when**:
- Base model has high variance (e.g., deep trees)
- You need fast training
- You want out-of-the-box good performance
- Interpretability is not critical (but feature importance helps)

**Use AdaBoost when**:
- You have weak learners (e.g., shallow trees, stumps)
- Data is not too noisy (AdaBoost is sensitive to outliers)
- Binary classification problem
- You need to understand which examples are "hard"

**Use Gradient Boosting when**:
- You need state-of-the-art accuracy
- You can afford longer training
- You have flexibility to tune many hyperparameters
- You want to use custom loss functions

**Use XGBoost when**:
- You want best accuracy with regularization
- You need speed (hardware optimization)
- You want to win a Kaggle competition 😊
- You need handling of missing values and sparsity

### 9.3 Key Hyperparameters

**Bagging/Random Forest**:
- `n_estimators`: Number of trees (more is better, diminishing returns after ~500)
- `max_features`: Features per split ($\sqrt{p}$ for classification, $p/3$ for regression)
- `max_depth`: Tree depth (None for RF, ~10-20 for others)

**Boosting (all variants)**:
- `n_estimators`: Number of rounds (too many → overfit)
- `learning_rate` ($\eta$): Step size (smaller → need more trees, but better generalization)
- `max_depth`: Tree depth (shallow like 3-6 for boosting)

**XGBoost specific**:
- `gamma`: Minimum gain to split (regularization)
- `lambda`: L2 regularization on weights
- `min_child_weight`: Minimum sum of Hessian in child (prevents overfitting)
- `subsample`: Fraction of samples per tree (adds randomness)
- `colsample_bytree`: Fraction of features per tree (like RF)

### 9.4 The Bias-Variance Tradeoff Revisited

**Visual Summary**:

```
High Variance     →     Bagging/RF     →     Low Variance
(Overfitting)                                (Stable)

High Bias         →     Boosting       →     Low Bias
(Underfitting)                               (Accurate)

Sweet Spot: XGBoost (Reduces bias via boosting + controls variance via regularization)
```

**Formula reminder**:

$$
\underbrace{\mathbb{E}[(y - \hat{f}(x))^2]}_{\text{Expected test error}} = \underbrace{(\mathbb{E}[\hat{f}(x)] - f(x))^2}_{\text{Bias}^2} + \underbrace{\mathbb{E}[(\hat{f}(x) - \mathbb{E}[\hat{f}(x)])^2]}_{\text{Variance}} + \underbrace{\sigma^2}_{\text{Irreducible}}
$$

- **Bagging**: Keeps bias, reduces variance
- **Boosting**: Reduces bias, may increase variance slightly
- **XGBoost**: Reduces bias (boosting) AND controls variance (regularization)

---

## 10. Final Thoughts: From First Principles

### 10.1 The Unifying Theme

All ensemble methods exploit the same fundamental idea: **Aggregate diverse predictors to reduce error**.

The differences lie in **how** they create diversity:
- Bagging: Different data subsets
- Random Forest: Different data + different features
- Boosting: Different focus (hard examples get more attention)

And **how** they combine:
- Bagging: Equal-weight average
- Boosting: Weighted sum (weights learned from data)

### 10.2 Why These Methods Work

**Conditioning on Independence** (for bagging):

If predictors are independent and each has error rate $\epsilon$:
- Majority vote error (with $n$ predictors): $\sum_{k > n/2} \binom{n}{k} \epsilon^k (1-\epsilon)^{n-k}$
- As $n \to \infty$, this goes to 0 (for $\epsilon < 0.5$)

**Conditioning on Sequential Improvement** (for boosting):

If each model reduces residual error by factor $\epsilon$:
- After $T$ rounds: Error $\propto (1-\epsilon)^T$
- Exponential decrease!

### 10.3 Practical Wisdom

1. **Start simple**: Try Random Forest first (great baseline)
2. **Tune carefully**: Boosting needs careful hyperparameter tuning
3. **Cross-validate**: Use CV to select number of trees and learning rate
4. **Monitor training**: Watch for overfitting (train vs. validation error)
5. **Use regularization**: Especially for boosting methods
6. **Leverage OOB**: Random Forest's OOB error is free validation
7. **Feature importance**: Use it to understand your model
8. **Ensemble of ensembles**: Can even ensemble RF + XGBoost!

### 10.4 Further Exploration

**Extensions not covered**:
- **Stacking**: Train meta-learner on base model predictions
- **LightGBM**: Gradient boosting with histogram-based splitting (faster than XGBoost)
- **CatBoost**: Handles categorical features natively
- **Isolation Forest**: Random forest for anomaly detection
- **Extra-Trees**: Even more randomness than Random Forest

**Advanced topics**:
- Theoretical analysis of ensemble methods
- Infinite ensembles and their limits
- Connection to neural networks (boosting ≈ shallow NN)
- Online/streaming ensemble methods

---

## Appendix: Mathematical Proofs Summary

### A.1 Bootstrap Probability (~63.2%)

$$
P(\text{selected}) = 1 - \left(1 - \frac{1}{n}\right)^n \xrightarrow{n \to \infty} 1 - e^{-1} \approx 0.632
$$

### A.2 AdaBoost Exponential Loss Minimization

Objective at round $t$:

$$
L_t(\alpha_t) = W_{\text{total}}[(1-\epsilon_t)e^{-\alpha_t} + \epsilon_t e^{\alpha_t}]
$$

Setting $\frac{dL_t}{d\alpha_t} = 0$:

$$
\alpha_t^* = \frac{1}{2}\ln\frac{1-\epsilon_t}{\epsilon_t}
$$

### A.3 XGBoost Optimal Leaf Weight

Objective for leaf $j$:

$$
\mathcal{L}_j = \left(\sum_{i \in I_j} g_i\right) w_j + \frac{1}{2} \left(\sum_{i \in I_j} h_i + \lambda\right) w_j^2
$$

Minimizing:

$$
w_j^* = -\frac{\sum_{i \in I_j} g_i}{\sum_{i \in I_j} h_i + \lambda}
$$

---

## References and Further Reading

**Books**:
1. *The Elements of Statistical Learning* by Hastie, Tibshirani, Friedman (Chapter 10, 15, 16)
2. *Pattern Recognition and Machine Learning* by Bishop
3. *Ensemble Methods* by Zhi-Hua Zhou

**Papers**:
1. Breiman (1996): "Bagging Predictors"
2. Breiman (2001): "Random Forests"
3. Freund & Schapire (1997): "A Decision-Theoretic Generalization of On-Line Learning"
4. Friedman (2001): "Greedy Function Approximation: A Gradient Boosting Machine"
5. Chen & Guestrin (2016): "XGBoost: A Scalable Tree Boosting System"

**Online Resources**:
- scikit-learn documentation (excellent explanations)
- XGBoost documentation
- StatQuest YouTube channel (Josh Starmer)

---

**End of Notes**

*These notes are designed for deep understanding from first principles. Work through the simulations with your own toy datasets, derive the proofs yourself, and experiment with implementations. True mastery comes from doing, not just reading!*

Good luck with your Machine Learning journey! 🎓
