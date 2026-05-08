# Session 17 – Concentration Inequalities & Tail Bounds

## Linked Domain
[[Discrete Math & Probability]]

**Cycle**: 3 (Advanced Integration)  
**Difficulty**: ⚫⚫⚫⚪

---

## Phase 1: Theoretical Foundation

### Definitions

**Concentration**: A random variable X concentrates around its expectation E[X] if Pr[|X - E[X]| > t] decreases rapidly with t.

**Markov's Inequality**: For non-negative X: Pr[X ≥ a] ≤ E[X]/a

**Chebyshev's Inequality**: Pr[|X - μ| ≥ kσ] ≤ 1/k² where μ = E[X], σ² = Var[X]

**Chernoff Bound**: For sum of independent {0,1} variables: Pr[X > (1+δ)μ] ≤ exp(-δ²μ/3) for 0 ≤ δ ≤ 1

**Hoeffding's Inequality**: For X₁,...,Xₙ independent with aᵢ ≤ Xᵢ ≤ bᵢ:
$$Pr[|\bar{X} - E[\bar{X}]| ≥ t] ≤ 2\exp\left(\frac{-2n^2t^2}{\sum_i (b_i - a_i)^2}\right)$$

### Core Mechanism: Proof Techniques

**Markov via Expectation**:
$$Pr[X ≥ a] = Pr[X/a ≥ 1] ≤ E[X/a] / 1 = E[X]/a$$

**Chernoff via MGF (Moment Generating Function)**:
$$Pr[X ≥ a] = Pr[e^{tX} ≥ e^{ta}] ≤ E[e^{tX}]/e^{ta} = M_X(t)/e^{ta}$$
Optimize over t to get tightest bound.

**Application: Load Balancing**
- n balls thrown into n bins uniformly at random
- Maximum load: O(log n / log log n) with high probability
- Proof uses Chernoff + union bound

### Mental Model

**Markov = Crude Average**: "If average height is 6ft, at most 50% can be ≥ 12ft"—uses only mean, very weak.

**Chebyshev = Using Spread**: "If σ = 2 inches, only 1% are beyond 3σ from mean"—uses variance, better.

**Chernoff = Exponential Decay**: "Probability decreases exponentially with deviation"—strongest for independent variables.

### Edge Cases & Applications

**1. Coupon Collector Problem**
- n coupon types, collect randomly
- Expected time: n·H_n = n ln n
- Tail bound (Chernoff): Pr[T > 2n ln n] ≤ 1/n

**2. Bloom Filter False Positive Rate**
- k hash functions, m bits
- FP rate after n insertions: $(1 - e^{-kn/m})^k$
- Chernoff bounds the deviation from expected

**3. Randomized Algorithms**
- QuickSort: Chernoff shows O(n log n) w.h.p.
- MinCut: Union bound + Chernoff for success probability

### Common Mistakes

1. **Using Chernoff for Dependent Variables**: Chernoff requires independence!
2. **Forgetting Union Bound**: When bounding max over n events, multiply by n
3. **Loose Bounds**: Choose right inequality—Markov vs Chebyshev vs Chernoff

### Code

```python
import numpy as np
import matplotlib.pyplot as plt

def empirical_concentration(n_trials, n_samples):
    """Verify Chernoff bound empirically"""
    results = []
    for _ in range(n_trials):
        # n coin flips
        X = np.random.binomial(1, 0.5, n_samples)
        results.append(X.sum())
    
    mu = n_samples * 0.5
    deviations = np.abs(np.array(results) - mu)
    
    # Compare to Chernoff
    for delta in [0.1, 0.2, 0.5]:
        threshold = delta * mu
        empirical_pr = np.mean(deviations > threshold)
        chernoff_bound = 2 * np.exp(-delta**2 * mu / 3)
        print(f"δ={delta}: Empirical={empirical_pr:.4f}, Chernoff≤{chernoff_bound:.4f}")

empirical_concentration(10000, 100)
```

---

## Phase 2: Stress Questions

### Q1: Chernoff Derivation
**Derive Chernoff bound for sum of n independent Bernoulli(p) random variables.**

<details><summary>Hint</summary>
Use MGF: E[e^{tX_i}] = pe^t + (1-p). For sum: E[e^{t∑X_i}] = (pe^t + 1-p)^n. Minimize over t.
</details>

### Q2: Hash Table Analysis
**Hash table with n keys, m slots. Use Chernoff to bound max bucket load.**

<details><summary>Hint</summary>
For bucket i, load X_i = ∑ I[key j hashes to i]. E[X_i] = n/m. Apply Chernoff + union bound.
</details>

### Q3: Median Finding
**Randomized median algorithm samples subset. Use Hoeffding to bound sample size for ε-approximation.**

<details><summary>Hint</summary>
Sample s keys. Hoeffding: Pr[|F(x) - F̂(x)| > ε] ≤ 2e^{-2sε²}. Solve for s.
</details>

---

## Phase 3: Applied Problem

Design a distributed vote counter with probabilistic guarantees. Use concentration inequalities to bound:
1. Sample size for ε-accurate estimate
2. Probability of error given m samples
3. Effect of Byzantine voters (up to f malicious)

---

## Phase 4: Self-Assessment

### Checklist
- [ ] Understand Markov, Chebyshev, Chernoff bounds
- [ ] Can derive Chernoff via MGF
- [ ] Know when to use which inequality
- [ ] Application to randomized algorithms

### Next Steps
- **Strong**: [[Session 18 – Distributed Transactions]]
- **Struggling**: Review [[Session 03 – Discrete Math & Probability]]
- **Resources**: "Probability and Computing" (Mitzenmacher & Upfal)

---

**Navigation**: ← [[Session 16]] | **Index**: [[cycle3/INDEX]] | → [[Session 18]]
