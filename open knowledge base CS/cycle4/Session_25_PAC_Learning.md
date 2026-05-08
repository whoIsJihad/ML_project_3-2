# Session 25 – PAC Learning & VC Dimension

**Cycle**: 4 (Expert Mastery)  
**Domain**: ML & Optimization  
**Difficulty**: ⚫⚫⚫⚫

**Prerequisites**: Probability theory, hypothesis spaces, statistical learning

---

## Phase 1: Core Theory & Mental Models

### 1.1 Definitions

**PAC Learning** (Probably Approximately Correct): Framework for analyzing learnability.

**Formal Definition**: Concept class C is PAC-learnable if there exists algorithm A and polynomial function poly(·,·,·,·) such that:
- For any ε > 0, δ > 0, distribution D, target concept c ∈ C
- Given m ≥ poly(1/ε, 1/δ, |x|, size(c)) training examples
- A outputs hypothesis h with probability ≥ 1-δ: error(h) ≤ ε
- Runtime is poly(1/ε, 1/δ, |x|, size(c))

**VC Dimension**: Maximum number of points that can be shattered by hypothesis class H.

**Shattering**: Set S is shattered by H if ∀ labeling of S, ∃ h ∈ H consistent with that labeling.

### 1.2 Core Mechanisms

**Sample Complexity Bound**: For hypothesis class H with VC dimension d:
```
m ≥ (1/ε) · (d log(1/ε) + log(1/δ))
```
guarantees PAC learning with error ≤ ε with probability ≥ 1-δ.

**Fundamental Theorem of PAC Learning**:
- Finite H is PAC-learnable with m = O((log|H| + log(1/δ))/ε)
- Infinite H is PAC-learnable iff VCdim(H) is finite

**VC Dimension Calculation**:

1. **Linear classifiers in R^d**: VCdim = d+1
   - d+1 points in general position can be shattered
   - d+2 points cannot (Radon's theorem)

2. **Axis-aligned rectangles in R^2**: VCdim = 4
   - 4 corner points shatterable
   - 5 points include one inside convex hull → not shatterable

3. **Intervals on R**: VCdim = 2

### 1.3 Mental Models

**The Three-Way Tradeoff**:
```
Sample Complexity ↔ Hypothesis Complexity ↔ Generalization
       m                  VCdim(H)              error(h)
```

**Shattering as "Expressiveness"**: VC dimension measures the ability of H to memorize arbitrary labelings - too high = overfitting risk.

**PAC as "Confidence Interval"**: ε controls accuracy, δ controls confidence - both require more samples when tightened.

### 1.4 Edge Cases

**Overfitting**: Even if algorithm finds h with zero training error, true error might be high if H has large VC dimension relative to m.

**Realizability Assumption**: PAC assumes target concept c ∈ H. If violated, need agnostic PAC learning.

**Improper Learning**: Algorithm may output h ∉ H (but still from another class H').

### 1.5 Implementation

**VC Dimension Calculation**:
```python
import numpy as np
from itertools import combinations, product

def check_shattering(points, hypothesis_class):
    """
    Check if a set of points can be shattered by hypothesis class.
    
    Args:
        points: numpy array of shape (n, d)
        hypothesis_class: function that takes points and labels, 
                          returns True if hypothesis exists
    
    Returns:
        True if points are shattered, False otherwise
    """
    n = len(points)
    
    # Try all 2^n possible labelings
    for labeling in product([0, 1], repeat=n):
        labeling = np.array(labeling)
        if not hypothesis_class(points, labeling):
            return False  # Found a labeling not achievable
    
    return True  # All labelings achievable

def vc_dimension_linear_classifier_2d():
    """
    Demonstrate VCdim = 3 for linear classifiers in R^2
    """
    def linear_classifier_2d(points, labels):
        """Check if linear classifier can achieve labeling"""
        from sklearn.svm import LinearSVC
        try:
            clf = LinearSVC(max_iter=10000)
            clf.fit(points, labels)
            pred = clf.predict(points)
            return np.all(pred == labels)
        except:
            return False
    
    # Test: 3 points in general position → shatterable
    points_3 = np.array([[0, 0], [1, 0], [0, 1]])
    print(f"3 points shatterable: {check_shattering(points_3, linear_classifier_2d)}")
    
    # Test: 4 points → not shatterable (one will be in convex hull)
    points_4 = np.array([[0, 0], [1, 0], [0, 1], [0.5, 0.5]])
    print(f"4 points shatterable: {check_shattering(points_4, linear_classifier_2d)}")
    
    return 3  # VCdim for R^2

def pac_sample_complexity(vc_dim, epsilon, delta):
    """
    Calculate sample complexity for PAC learning
    
    m ≥ (1/ε) · (d log(1/ε) + log(1/δ))
    """
    import math
    
    m = (1 / epsilon) * (vc_dim * math.log(1 / epsilon) + math.log(1 / delta))
    return int(np.ceil(m))

# Example usage
vc_dim = 3  # Linear classifier in R^2
epsilon = 0.1
delta = 0.05

m = pac_sample_complexity(vc_dim, epsilon, delta)
print(f"Sample complexity for ε={epsilon}, δ={delta}, VCdim={vc_dim}: {m}")
```

**PAC Learning Algorithm (Consistent Learner)**:
```python
def pac_learner_consistent(training_data, hypothesis_class, epsilon, delta):
    """
    PAC learner using Empirical Risk Minimization (ERM)
    Returns hypothesis consistent with training data (if exists)
    
    Args:
        training_data: list of (x, y) tuples
        hypothesis_class: iterable of hypotheses
        epsilon: accuracy parameter
        delta: confidence parameter
    
    Returns:
        Hypothesis h with error(h) ≤ ε with probability ≥ 1-δ
    """
    X_train = [x for x, y in training_data]
    y_train = [y for x, y in training_data]
    
    # ERM: Find hypothesis with zero training error
    for h in hypothesis_class:
        predictions = [h(x) for x in X_train]
        if predictions == y_train:
            return h
    
    return None  # No consistent hypothesis (realizability violated)

# Example: PAC learning intervals on real line
def interval_hypothesis_space(data):
    """
    Generate all interval [a, b] hypotheses that label positive points
    """
    positive_points = [x for x, y in data if y == 1]
    
    if not positive_points:
        yield lambda x: 0  # Always negative
    else:
        a = min(positive_points)
        b = max(positive_points)
        yield lambda x: 1 if a <= x <= b else 0

# Training data
training_data = [(1.5, 1), (2.3, 1), (3.1, 1), (0.5, 0), (4.5, 0)]

# Learn
h = pac_learner_consistent(training_data, interval_hypothesis_space(training_data), 0.1, 0.05)
print(f"Learned hypothesis: interval classifier")
```

---

## Phase 2: Conceptual Stress Questions

### Q1: VC Dimension Proof
**Question**: Prove that the VC dimension of linear classifiers in R^d is exactly d+1.

<details>
<summary><strong>Hint</strong></summary>

Upper bound: Use Radon's theorem (any d+2 points in R^d can be partitioned into sets with intersecting convex hulls).

Lower bound: Show d+1 points in general position (e.g., standard basis + origin) are shatterable.
</details>

---

### Q2: Sample Complexity Lower Bound
**Question**: Show that any PAC learning algorithm for hypothesis class H with VCdim(H) = d requires Ω(d/ε + log(1/δ)/ε) samples.

<details>
<summary><strong>Hint</strong></summary>

Use adversarial argument: if m < d, can construct two distributions indistinguishable from m samples but with different true errors.
</details>

---

### Q3: Agnostic PAC Learning
**Question**: In agnostic PAC learning (target not in H), why does sample complexity increase by factor 1/ε?

<details>
<summary><strong>Hint</strong></summary>

Need to estimate error of best h ∈ H to within ε, not just achieve ε-error. Requires concentration bounds with finer granularity.
</details>

---

## Phase 3: Applied Problem

### Problem: Implement PAC Learner for Decision Stumps

**Scenario**: Decision stump is a single-threshold classifier: h(x) = sign(x - θ). Implement PAC learner and verify sample complexity empirically.

**Skeleton Code**:
```python
import numpy as np
import matplotlib.pyplot as plt

class DecisionStump:
    def __init__(self, theta):
        self.theta = theta
    
    def predict(self, x):
        return 1 if x >= self.theta else 0

def pac_learn_decision_stump(X_train, y_train):
    """
    Learn decision stump using ERM
    
    Args:
        X_train: numpy array of shape (m,)
        y_train: numpy array of shape (m,) with labels {0, 1}
    
    Returns:
        DecisionStump with minimal training error
    """
    # TODO: 
    # 1. Try all possible thresholds (midpoints between consecutive points)
    # 2. Choose threshold minimizing training error
    # 3. Return learned decision stump
    
    pass

def empirical_sample_complexity(epsilon, delta, num_trials=100):
    """
    Empirically verify PAC sample complexity for decision stumps
    VCdim(decision stumps) = 2
    
    Returns:
        Average number of samples needed to achieve ε-error with probability ≥ 1-δ
    """
    # TODO:
    # 1. Generate true distribution (e.g., threshold at 0.5)
    # 2. For each trial:
    #    - Sample m training points
    #    - Learn hypothesis
    #    - Estimate true error on large test set
    #    - Check if error ≤ ε
    # 3. Find minimum m where success rate ≥ 1-δ
    
    pass

# Test
np.random.seed(42)
epsilon = 0.1
delta = 0.05

# Theoretical sample complexity
vc_dim = 2
m_theory = pac_sample_complexity(vc_dim, epsilon, delta)
print(f"Theoretical m: {m_theory}")

# Empirical verification
m_empirical = empirical_sample_complexity(epsilon, delta)
print(f"Empirical m: {m_empirical}")
print(f"Ratio: {m_empirical / m_theory:.2f}")
```

**Expected Approach**:
1. ERM: enumerate all threshold candidates
2. Evaluate training error for each
3. Return best threshold
4. Verify m = O(VCdim/ε + log(1/δ)/ε) matches theory

---

## Phase 4: Self-Assessment

### Checklist
- [ ] Can define PAC learning formally
- [ ] Understand VC dimension and shattering
- [ ] Can compute VC dimension for common hypothesis classes
- [ ] Know sample complexity bounds
- [ ] Can implement PAC learner for simple classes

### Reflection Questions
1. Why does finite VC dimension guarantee learnability?
2. How does PAC framework relate to bias-variance tradeoff?
3. What are limitations of PAC model (computational complexity, realizability)?

### Next Steps
- **Deepen**: Study agnostic PAC, Rademacher complexity, boosting
- **Connect**: Relate to statistical learning theory, online learning
- **Apply**: Analyze VC dimension of neural network architectures

**Related Sessions**:
- ← [Session 24: Approximation Algorithms](Session_24_Approximation_Algorithms.md)
- → [Session 26: NewSQL Systems](Session_26_NewSQL_Systems.md)

---

*Session 25 of Cycle 4 • Expert Mastery*
