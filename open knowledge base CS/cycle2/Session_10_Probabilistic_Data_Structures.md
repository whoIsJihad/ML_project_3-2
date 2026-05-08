# Session 10 – Probabilistic Data Structures & Space-Accuracy Tradeoffs

## Linked Domain
[[Discrete Math & Probability]]

**Cycle**: 2 (Intermediate Depth)  
**Difficulty**: ⚫⚫⚪⚪

---

## Phase 1 – Clean Theory

### Definitions

**Probabilistic Data Structure**: Uses randomization to achieve space efficiency at the cost of bounded error probability.

**Bloom Filter**: Space-efficient probabilistic set membership test. False positives possible, false negatives impossible.

**Count-Min Sketch (CMS)**: Estimates frequency of elements in a stream using hash functions. Over-estimates but never under-estimates.

**HyperLogLog (HLL)**: Estimates cardinality (distinct count) of multiset with $O(\log \log n)$ space and $\approx 2\%$ standard error.

**$(\epsilon, \delta)$-approximation**: Algorithm returns estimate $\hat{x}$ such that $P(|\hat{x} - x| > \epsilon x) \leq \delta$.

**Union Bound**:  $P(\bigcup_i A_i) \leq \sum_i P(A_i)$. Used to bound total error probability across multiple structures.

---

### Core Mechanism

**Bloom Filter**:
- Bit array of size $m$, $k$ hash functions
- **Insert** $x$: set bits $h_1(x), \ldots, h_k(x)$ to 1
- **Query** $x$: check if all $h_i(x)$ bits are 1
- False positive rate: $f = (1 - e^{-kn/m})^k$ where $n$ = elements inserted
- Optimal $k = (m/n) \ln 2 \approx 0.69 m/n$

**Count-Min Sketch**:
- 2D array: $d$ rows, $w$ columns
- Insert $x$: increments CM[i][h_i(x)] for each row $i$
- Query $x$: return $\min_i \text{CM}[i][h_i(x)]$
- Error bound: $\hat{f}(x) \leq f(x) + \epsilon N$ with probability $\geq 1 - \delta$
- Space: $w = \lceil e/\epsilon \rceil, d = \lceil \ln(1/\delta) \rceil$

**HyperLogLog**:
- Uses $m = 2^b$ buckets (typically $b = 14$)
- For each element: hash to $b$-bit prefix (bucket) + count leading zeros in remaining bits
- Keep maximum leading zeros per bucket
- Cardinality estimate: $\hat{n} = \alpha_m \cdot m^2 / \sum_{j=1}^m 2^{-M[j]}$
- Space: $O(m \log \log n) = O(2^b \cdot b)$ bits

---

### Mental Model

**Space-Accuracy Tradeoff**:
```
Exact structures (HashSet):
  Space: O(n)
  Accuracy: 100%
  
Probabilistic (Bloom Filter):
  Space: O(n log(1/ε))  (typically 10 bits/elem)
  Accuracy: 1-ε
```

**Key Insight**: Impossible to have zero error with sublinear space (information theory). Probabilistic structures carefully choose which errors to allow.

**Design Pattern**:
1. Identify acceptable error type (false positive vs false negative)
2. Use hash functions to spread elements (reduce collisions)
3. Use multiple instances (union bound to amplify confidence)
4. Trade space ($m$) vs error ($\epsilon$)

---

### Edge Cases

1. **Hash Function Independence**: CMS analysis assumes pairwise independence. Practical hash functions (e.g., MurmurHash) aren't truly independent. Can cause bias.

2. **Heavy Hitters Domination**: In Count-Min Sketch, heavy hitters inflate counts of light items in same bucket. Need hierarchical schemes for better accuracy.

3. **Cardinality Range**: HyperLogLog has different error rates at low vs high cardinalities. Below $2.5m$, needs bias correction. Above $2^{32}/30$, needs large range correction.

4. **Deletion Problem**: Standard Bloom Filter doesn't support deletion (can't unset bits, might be set by other elements). Need Counting Bloom Filter (wastes space).

5. **Union/Intersection**: Bloom filters support union (bitwise OR) but intersection is problematic (error rates multiply). Minwise hashing better for Jaccard similarity.

---

### Common Mistakes

1. **Using bad hash functions**: Using `hash() % m` in Python. Need proper hash functions with good mixing.

2. **Ignoring union bound**: Building many approximate structures and querying all. Must inflate $\delta$ by number of queries.

3. **Confusing Count-Min with Count sketch**: Count-Min only over-estimates. Count sketch (different structure) gives unbiased estimates but can under-estimate.

4. **Not tuning parameters**: Using default HLL with $m=16$ buckets. Too small for accurate estimates. Need $m \geq 2^{12}$ for good accuracy.

5. **Assuming uniform hashing**: Elements might not hash uniformly (e.g., sequential IDs). Can bias cardinality estimates significantly.

---

### Code Snippet – Bloom Filter Implementation

```python
import hashlib
import math

class BloomFilter:
    def __init__(self, n_expected, false_positive_rate=0.01):
        """
        n_expected: expected number of elements
        false_positive_rate: desired false positive rate
        """
        # Compute optimal parameters
        self.m = math.ceil(-(n_expected * math.log(false_positive_rate)) / (math.log(2)**2))
        self.k = math.ceil((self.m / n_expected) * math.log(2))
        
        # Bit array
        self.bits = [False] * self.m
        self.n_inserted = 0
        
        print(f"Bloom filter: m={self.m} bits, k={self.k} hash functions")
        print(f"Space: {self.m / 8 / 1024:.2f} KB for {n_expected} elements")
    
    def _hashes(self, item):
        """Generate k hash values using double hashing."""
        # Use two hash functions to simulate k hash functions
        h1 = int(hashlib.md5(item.encode()).hexdigest(), 16)
        h2 = int(hashlib.sha1(item.encode()).hexdigest(), 16)
        
        for i in range(self.k):
            yield (h1 + i * h2) % self.m
    
    def add(self, item):
        """Add item to set."""
        for h in self._hashes(item):
            self.bits[h] = True
        self.n_inserted += 1
    
    def contains(self, item):
        """Check if item *might* be in set."""
        return all(self.bits[h] for h in self._hashes(item))
    
    def false_positive_rate(self):
        """Estimate current false positive rate."""
        # f = (1 - e^(-kn/m))^k
        exponent = -self.k * self.n_inserted / self.m
        return (1 - math.exp(exponent)) ** self.k

# Demonstration
bf = BloomFilter(n_expected=100000, false_positive_rate=0.01)

# Insert elements
for i in range(10000):
    bf.add(f"user_{i}")

# Test membership
print("Test present:", bf.contains("user_5000"))  # True
print("Test absent:", bf.contains("user_99999"))  # False (likely)

# Measure false positives
false_positives = sum(1 for i in range(10000, 20000) 
                      if bf.contains(f"user_{i}"))
print(f"False positives: {false_positives}/10000 = {false_positives/10000:.4f}")
print(f"Theoretical FP rate: {bf.false_positive_rate():.4f}")
```

---

## Phase 2 – Conceptual Stress Questions

**Q1**: Bloom filter has false positive rate $f = (1 - e^{-kn/m})^k$. Derive the optimal $k$ that minimizes $f$ for fixed $m$ and $n$. Prove that $k^* = (m/n) \ln 2$. Now compute: if you have $m = 1000$ bits and $n = 100$ elements, what's the minimum achievable false positive rate?

**Q2**: Count-Min Sketch guarantees $\hat{f}(x) \leq f(x) + \epsilon N$ with probability $1 - \delta$. You run 1000 queries. Using the union bound, what's the probability that *at least one* query violates the guarantee? How should you adjust $\delta$ to ensure all 1000 queries succeed with 99% probability? What's the space overhead of this adjustment?

**Q3**: HyperLogLog uses leading zeros to estimate cardinality. Explain the intuition: why does the maximum leading zeros across $m$ buckets correlate with cardinality? Formalize this: if you hash $n$ distinct elements into $m$ buckets, what's the expected maximum leading zeros in any bucket? Derive the estimator formula (sketch-level OK, full derivation is hard).

---

## Phase 3 – Applied Problem

**Problem Statement**:

You're building a **real-time analytics system** tracking user events. Requirements:
- 100M users, 1B events/day
- Query: "Is user X active today?" (set membership)
- Query: "How many times did user X do action Y today?" (frequency)
- Query: "How many distinct users visited page Z today?" (cardinality)

**Part A – Structure Selection**:
For each query type, choose a probabilistic structure (Bloom Filter, CMS, HLL) and justify. Compute space requirements:
- Bloom Filter: false positive rate $\epsilon = 0.01$
- CMS: error $\epsilon = 0.001$, confidence $\delta = 0.01$
- HLL: $m = 2^{14}$ buckets

Compare with exact structures (HashSet, HashMap, etc.). At what scale do probabilistic structures become essential?

**Part B – Compound Structure**:
You want to answer: "How many distinct users did action Y on page Z today?" This requires combining HLL (cardinality) with filtering (action Y on page Z).

Design a solution using:
- Multiple HLLs per (action, page) pair
- Space optimization (thousands of action/page combinations)

Analysis:
- If you have 1000 actions, 10000 pages, how many HLLs do you need?
- Space per HLL = $m \cdot b$ bits where $b = \log \log n$
- Can you share buckets across HLLs? (Tradeoff: space vs accuracy)

**Part C – Distributed Variant**:
System is distributed across 100 machines. Each machine sees subset of events. To answer global queries, you must merge probabilistic structures.

For each structure, analyze:
- **Bloom Filter**: Can you merge by OR-ing bits? Does error rate increase?
- **CMS**: Can you merge by element-wise addition? Error bound after merge?
- **HLL**: Can you merge by taking max per bucket? Does this affect accuracy?

Prove or disprove: merging $k$ independent structures increases error by factor $\sqrt{k}$.

---

## Phase 4 – Feedback & Weakness Log Update

**Awaiting your responses to Phase 2 and Phase 3.**

Critique will focus on:
- Derivations and mathematical rigor
- Understanding union bound applications
- Design tradeoffs (space vs accuracy vs query types)
- Distributed systems considerations

---

## Cross-Links for Reinforcement
- [[Session 3: Randomized Algorithms]] (prerequisite)
- [[Streaming Algorithms]]
- [[MinHash & Locality-Sensitive Hashing]]
- [[Approximate Query Processing]]
- [[Information Theory Lower Bounds]]

---

**Status**: Awaiting Phase 2 & 3 responses.
