# Session 16 – Amortized Analysis & Potential Method

## Linked Domain
[[Algorithms & Complexity]]

**Cycle**: 3 (Advanced Integration)  
**Difficulty**: ⚫⚫⚫⚪

---

## Phase 1: Theoretical Foundation

### Definitions

**Amortized Analysis**: A technique to analyze the average cost of operations in a sequence, accounting for expensive operations "amortized" over many cheap ones.

**Amortized Cost**: The average cost per operation over a worst-case sequence of operations. Not the same as average-case analysis (which considers input distribution).

**Potential Method**: An amortized analysis technique using a potential function Φ that captures "stored work" in a data structure. Amortized cost = actual cost + ΔΦ.

**Accounting Method**: Assigns different charges to different operations. Some operations are "overcharged" to build credit for future expensive operations.

### Core Mechanism: Three Analysis Methods

**1. Aggregate Method**
Total cost of n operations / n

Example: Dynamic Array
- Start with capacity 1
- Double when full: copy all elements
- Insertions at indices: 1, 2, 4, 8, 16, ...
- Total copies: 1 + 2 + 4 + ... + n/2 = n - 1
- Total cost: n insertions + (n-1) copies = 2n - 1
- Amortized cost: (2n - 1) / n = O(1)

**2. Accounting Method**
- Charge each operation an amortized cost
- Build credit (positive balance) when actual cost < amortized
- Use credit when actual cost > amortized
- Maintain: credit ≥ 0 always

Example: Dynamic Array
- Charge each insertion: 3 units
  - 1 for actual insertion
  - 1 credit saved on inserted element
  - 1 credit saved on existing element
- When doubling (n items → 2n capacity):
  - Need n units to copy n elements
  - Have n credits saved (1 per element)
  - Cost covered!

**3. Potential Method**
Define Φ(D) = "potential" of data structure D
- Φ(D₀) = 0 (initial state)
- Φ(Dᵢ) ≥ 0 for all i (non-negative potential)

Amortized cost of operation:
$$\hat{c}_i = c_i + \Phi(D_i) - \Phi(D_{i-1})$$

Total amortized cost:
$$\sum_{i=1}^{n} \hat{c}_i = \sum_{i=1}^{n} c_i + \Phi(D_n) - \Phi(D_0) \geq \sum_{i=1}^{n} c_i$$

Example: Dynamic Array
- Φ(D) = 2 × size - capacity
- Initial: size=0, capacity=1 → Φ = -1 (adjust to 0 by convention)
- Insert when size < capacity: c=1, ΔΦ=2 → ĉ = 3
- Insert when size = capacity (trigger doubling):
  - c = size + 1 (copy all + insert)
  - New: size = size+1, capacity = 2×size
  - ΔΦ = 2(size+1) - 2×size - (2×size - size) = 2 - size
  - ĉ = (size + 1) + (2 - size) = 3

### Mental Model

**Amortized Analysis = Budgeting**: Think of expensive operations as "big purchases" and cheap operations as "saving money." The amortized cost is your steady monthly budget. Some months you save (cheap operations), other months you spend savings (expensive operations like resizing). The budget (amortized cost) is constant.

**Potential = Stored Energy**: Like a spring being compressed (potential energy increases). When released, stored energy does work (potential decreases, actual cost is low). The potential function captures this "elastic" behavior.

### Edge Cases

**1. Worst-Case Sequence for Binary Counter**
```
Increment from 0:
- 0 → 1: flip 1 bit
- 1 → 2 (10): flip 2 bits
- 2 → 3 (11): flip 1 bit
- 3 → 4 (100): flip 3 bits
- ...
Total for n increments: O(n log n) worst-case
Amortized: O(1) per increment
```

**2. Splay Tree Access Pattern**
After splaying deepest node repeatedly:
- First access: O(n) rotations
- Subsequent accesses: O(log n) amortized
- Potential function captures tree "balance"

**3. Fibonacci Heap Decrease-Key**
- Actual cost: O(k) where k is cascading cuts
- Potential decreases by Ω(k)
- Amortized cost: O(1)

### Common Mistakes

1. **Confusing Amortized with Average-Case**: Amortized is worst-case average over sequence. Average-case assumes input distribution.

2. **Negative Potential**: Potential must stay ≥ 0. If it goes negative, analysis breaks.

3. **Wrong Potential Function**: Must increase with "work stored" and decrease when work is done.

### Implementation Code

```python
import math
import numpy as np

class DynamicArray:
    def __init__(self):
        self.capacity = 1
        self.size = 0
        self.data = [None] * self.capacity
        self.total_cost = 0
    
    def append(self, item):
        if self.size == self.capacity:
            new_capacity = 2 * self.capacity
            new_data = [None] * new_capacity
            for i in range(self.size):
                new_data[i] = self.data[i]
            self.data = new_data
            self.capacity = new_capacity
            self.total_cost += self.size
        
        self.data[self.size] = item
        self.size += 1
        self.total_cost += 1
    
    def potential(self):
        return 2 * self.size - self.capacity

class BinaryCounter:
    def __init__(self, bits):
        self.bits = [0] * bits
        self.n_bits = bits
        self.total_flips = 0
    
    def increment(self):
        flips = 0
        i = 0
        while i < self.n_bits and self.bits[i] == 1:
            self.bits[i] = 0
            flips += 1
            i += 1
        if i < self.n_bits:
            self.bits[i] = 1
            flips += 1
        self.total_flips += flips
        return flips
    
    def potential(self):
        return sum(self.bits)

# Example
arr = DynamicArray()
for i in range(100):
    arr.append(i)
print(f"Avg cost: {arr.total_cost / arr.size:.2f}, Amortized: 3")

counter = BinaryCounter(8)
for _ in range(20):
    counter.increment()
print(f"Total flips: {counter.total_flips}, Avg: {counter.total_flips/20:.2f}")
```

---

## Phase 2: Stress Questions

### Question 1: Potential Function Design
**Design a potential function for a stack with `push(x)` O(1) and `multipop(k)` O(min(k, size)) operations. Prove O(1) amortized cost.**

<details>
<summary>Hint</summary>
Use Φ(D) = size of stack. Push increases potential by 1, multipop decreases by k. Show that amortized cost of multipop is O(1).
</details>

---

### Question 2: Binary Counter Analysis
**Prove O(1) amortized cost for binary counter increments using both aggregate analysis and potential method.**

<details>
<summary>Hint</summary>
Aggregate: Total flips = n + n/2 + n/4 + ... = 2n. Potential: Φ = number of 1's. Each increment: cost ≤ k+1, ΔΦ = 2-k.
</details>

---

### Question 3: Splay Tree Proof
**Prove m operations on splay tree have O(m log n + n log n) total cost using Φ = Σ log(size(subtree)).**

<details>
<summary>Hint</summary>
Access Lemma: splaying costs ≤ 3(rank(root) - rank(x)) + 1. Sum over m operations.
</details>

---

## Phase 3: Applied Problem

### Problem: Self-Organizing List

Implement move-to-front (MTF) heuristic for self-organizing lists.

**Part A**: Prove MTF is 2-competitive against optimal offline algorithm.

**Part B**: Define potential as inversions between MTF and OPT. Prove amortized O(1) per access.

**Part C**: Implement and benchmark on Zipf-distributed accesses.

```python
class SelfOrganizingList:
    def __init__(self, items):
        self.items = list(items)
        self.access_costs = []
    
    def access_mtf(self, key):
        for i, item in enumerate(self.items):
            if item == key:
                self.items.pop(i)
                self.items.insert(0, key)
                self.access_costs.append(i + 1)
                return i + 1
        return -1

# TODO: Complete implementation and benchmarks
```

---

## Phase 4: Self-Assessment & Feedback

### Mastery Checklist
- [ ] Can apply aggregate, accounting, and potential methods
- [ ] Know how to design potential functions
- [ ] Understand amortized vs worst-case/average-case
- [ ] Can prove amortized bounds

### Reflection Questions
1. **Why is potential method** more general than accounting?
2. **When is amortized analysis** NOT appropriate?

### Next Steps
- **If strong**: [[Session 17 – Concentration Inequalities]]
- **If struggling**: Review [[Session 02 – Algorithms & Complexity]]
- **Resources**: CLRS Ch. 17, "Data Structures and Network Algorithms" (Tarjan)

---

**Navigation**: ← [[Session 15]] | **Index**: [[cycle3/INDEX]] | → [[Session 17]]
