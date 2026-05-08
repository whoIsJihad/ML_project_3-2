# Session 3 – Randomized Algorithms & Tail Bounds

## Linked Domain
[[Discrete Math & Probability]]

---

## Phase 1 – Clean Theory

### 1. Algorithm Classes

| Type | Correctness | Running Time | Example |
|------|-------------|--------------|---------|
| **Las Vegas** | Always correct | Random variable | Randomized QuickSort |
| **Monte Carlo** | Probabilistic | Bounded | Min-cut algorithm |

---

### 2. Tail Inequalities

**Markov's Inequality** (expectation only):
$$P(X \geq a) \leq \frac{E[X]}{a} \quad \text{for } X \geq 0, a > 0$$

**Chebyshev's Inequality** (uses variance):
$$P(|X - \mu| \geq k\sigma) \leq \frac{1}{k^2}$$

**Chernoff Bound** (uses independence, exponentially tight):

For $X = \sum_{i=1}^n X_i$ where $X_i \in [0,1]$ independent, $\mu = E[X]$:
$$P(X \geq (1+\delta)\mu) \leq e^{-\frac{\delta^2 \mu}{3}} \quad \text{for } 0 < \delta < 1$$
$$P(X \leq (1-\delta)\mu) \leq e^{-\frac{\delta^2 \mu}{2}} \quad \text{for } 0 < \delta < 1$$

---

### 3. Tail Bound Selection Guide

| Bound | Requires | Tightness | Use Case |
|-------|----------|-----------|----------|
| Markov | $X \geq 0$, $E[X]$ | Weak ($1/k$) | Only expectation known |
| Chebyshev | $E[X]$, $\text{Var}(X)$ | Moderate ($1/k^2$) | Variance known, limited independence |
| Chernoff | Full independence | Exponential | Sum of independent bounded variables |

---

### 4. Amplification Technique

For Monte Carlo algorithms with error probability $\epsilon$:
- Run $k$ independent trials
- Take majority vote
- New error probability: $\epsilon^{\Omega(k)}$

**Trade-off**: Runtime increases by factor $k$ for exponential error reduction.

---

### 5. Concentration Intuition

For $n$ independent trials with mean $\mu$ and variance $\sigma^2$:
- Absolute deviation: $O(\sigma\sqrt{n})$
- Relative deviation: $\frac{\sigma}{\mu} \sim \frac{1}{\sqrt{n}}$

Concentration improves with more samples.

---

### 6. Edge Cases and Limitations

1. **Hidden Dependencies**: Chernoff requires independence. Correlated variables require different bounds (e.g., Azuma-Hoeffding for martingales).

2. **Unbounded Variables**: Chernoff assumes $X_i \in [0,1]$. For unbounded variables, use appropriate transformations or different inequalities.

3. **Small Expectation**: When $\mu \ll 1$, Chernoff bounds become weak. Alternative analysis needed.

4. **One-sided vs Two-sided**: Markov only bounds $P(X \geq a)$. For two-sided bounds, apply to both $X$ and $E[X] - X$.

---

### Common Mistakes

1. **Applying Chernoff to dependent variables**: Hash function outputs, sampling without replacement require modified bounds.

2. **Wrong bound selection**: Using Chebyshev when independence holds (Chernoff gives exponentially better bounds).

3. **Missing union bound**: When bounding $P(\bigcup_i A_i)$, must apply $\sum_i P(A_i)$.

4. **Expectation misinterpretation**: $E[X] = 1$ does not imply $X = 1$ with high probability—must bound deviation.

5. **Ignoring amplification cost**: Error reduction by $k$ trials costs $k \times$ runtime.

---

### Code Snippet – Randomized Quickselect Concentration Test

```python
import random
import time
import statistics

def randomized_select(arr, k):
    """Find k-th smallest element. Expected O(n)."""
    if len(arr) == 1:
        return arr[0]

    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    if k < len(left):
        return randomized_select(left, k)
    elif k < len(left) + len(mid):
        return pivot
    else:
        return randomized_select(right, k - len(left) - len(mid))

def test_concentration(n=10000, trials=100):
    """Verify running time concentration around expectation."""
    times = []

    for _ in range(trials):
        arr = list(range(n))
        random.shuffle(arr)

        start = time.perf_counter()
        randomized_select(arr, n // 2)
        end = time.perf_counter()

        times.append(end - start)

    mean_time = statistics.mean(times)
    stddev = statistics.stdev(times)
    cv = stddev / mean_time  # Coefficient of variation

    print(f"n={n}, trials={trials}")
    print(f"Mean: {mean_time:.6f}s, StdDev: {stddev:.6f}s")
    print(f"Coefficient of variation: {cv:.4f}")

    within_2sigma = sum(1 for t in times if abs(t - mean_time) <= 2*stddev)
    print(f"Within 2σ: {within_2sigma}/{trials} ({100*within_2sigma/trials:.1f}%)")
    print("Chebyshev predicts ≥75%, empirical typically >95%")

if __name__ == "__main__":
    test_concentration()
```

---

## Phase 2 – Conceptual Stress Questions

**Q1**: Estimate coin bias $p \in [0,1]$ with confidence: $P(|\hat{p} - p| > \epsilon) < \delta$ where $\hat{p} = X/n$. Using Chernoff, derive minimum $n$ as function of $\epsilon$ and $\delta$. How does the bound degrade for small $p \approx 0.01$? Can you improve it?

**Q2**: QuickSort is $O(n \log n)$ expected, $O(n^2)$ worst-case with random pivots. Strategy: "Run 10 times on different permutations, take fastest." Does this improve worst-case bound? Expected bound? Explain using tail bounds.

**Q3**: Load balancer assigns $n$ jobs to $n$ servers uniformly at random. Let $X_i$ = load on server $i$. Prove $P(\max_i X_i > c \log n / \log \log n) < 1/n$ for some constant $c$. (Hint: Union bound + Chernoff.) What does this say about worst-case vs expected load?

---

## Phase 3 – Applied Problem

**Problem Statement**:

**Karger's Min-Cut Algorithm**:
1. Pick random edge $(u, v)$
2. Contract: merge $u$ and $v$
3. Repeat until 2 nodes remain
4. Return cut edges between remaining nodes

**Part A**: Let minimum cut $C$ have $|C| = k$ edges. Prove probability of returning $C$ is at least $\binom{n}{2}^{-1}$.

**Part B**: Run algorithm $t = \binom{n}{2} \ln n$ times, return smallest cut. Use Chernoff/union bound to prove success probability $\geq 1 - 1/n$.

**Part C**: Algorithm costs $O(n^2)$ per trial. Colleague suggests: "Run only $t = n$ trials since Chernoff gives concentration." Analyze this claim. At what failure probability does it become unacceptable? What is the correct time-success trade-off?

---

## Phase 4 – Feedback & Weakness Log Update

**Awaiting your responses to Phase 2 and Phase 3.**

Critique will focus on:
- Correct application of tail bounds
- Independence assumptions
- Quantitative precision (not just "by Chernoff")
- Union bound technique
- Time-correctness trade-off analysis

---

## Cross-Links for Reinforcement
- [[Probabilistic Method]]
- [[Randomized QuickSort & Selection]]
- [[Hash Functions & Universal Hashing]]
- [[Min-Cut & Global Min-Cut]]
- [[Concentration of Measure]]
- [[Derandomization Techniques]]

---

**Status**: Awaiting Phase 2 & 3 responses.
