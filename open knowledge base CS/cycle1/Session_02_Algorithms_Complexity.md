# Session 2 – Amortized Analysis & Potential Method

## Linked Domain
[[Algorithms & Complexity]]

---

## Phase 1 – Clean Theory

### 1. Amortized Analysis Framework

**Amortized Cost**: Average cost per operation over a worst-case sequence of $n$ operations. Provides a guaranteed upper bound, not an expected value.

| Method | Approach | Formula |
|--------|----------|---------|
| **Aggregate** | Total cost / operations | $T(n)/n$ |
| **Accounting** | Assign artificial costs | $\sum \hat{c}_i \geq \sum c_i$ |
| **Potential** | State-based energy function | $\hat{c}_i = c_i + \Phi(D_i) - \Phi(D_{i-1})$ |

**Potential Method Requirements**:
- $\Phi(D_0) = 0$ (or known constant)
- $\Phi(D) \geq 0$ for all reachable states
- $\Phi$ increases on cheap operations, decreases on expensive ones

**Telescoping Sum**:
$$\sum_{i=1}^{n} \hat{c}_i = \sum_{i=1}^{n} c_i + \Phi(D_n) - \Phi(D_0)$$

If $\Phi(D_n) \geq \Phi(D_0)$, then $\sum \hat{c}_i \geq \sum c_i$.

---

### 2. Standard Potential Functions

| Data Structure | Potential Function | Amortized Bound |
|----------------|-------------------|-----------------|
| Dynamic array (doubling) | $2 \cdot \text{size} - \text{capacity}$ | $O(1)$ push |
| Binary counter | Number of 1-bits | $O(1)$ increment |
| Splay tree | $\sum_x \log(\text{size}(x))$ | $O(\log n)$ op |
| Fibonacci heap | $\text{trees} + 2 \cdot \text{marked}$ | $O(1)$ insert/decrease-key |

---

### 3. Key Properties

**Amortized vs. Worst-Case**:
- Amortized: Bounds average over sequence; individual ops may be $O(n)$
- Worst-case: Bounds every single operation
- Average-case: Uses probability distribution over inputs (different concept)

**Real-Time Consideration**: Amortized bounds are unsuitable for hard real-time systems where individual operation latency matters.

---

### 4. Limitations and Edge Cases

1. **Persistent Data Structures**: Potential method fails—copies inherit potential, allowing double-spending.

2. **Concurrent Operations**: Amortization assumes sequential execution; concurrent triggers can invalidate bounds.

3. **Initial State**: Non-zero $\Phi(D_0)$ requires explicit accounting.

4. **Tightness**: Amortized analysis may be conservative for operation sequences that never trigger expensive paths.

---

### Common Mistakes

1. **Amortized ≠ Average-case**: Amortized is deterministic worst-case averaged over sequences.

2. **Invalid potential**: Using $\Phi = \text{size}$ for dynamic arrays (fails to precharge for resize).

3. **Ignoring $\Phi(D_n)$**: Final potential may be large, making actual cost lower than amortized sum.

4. **Unproven non-negativity**: Claiming $\Phi \geq 0$ without proof for all reachable states.

5. **Context-free claims**: Stating "$O(1)$ amortized" without specifying the operation sequence.

---

### Code Snippet – Dynamic Array with Amortized Cost Tracking

```cpp
#include <iostream>
#include <vector>

class TrackedVector {
    int* arr;
    size_t capacity;
    size_t size;
    long long total_cost;

public:
    TrackedVector() : capacity(1), size(0), total_cost(0) {
        arr = new int[capacity];
    }

    ~TrackedVector() { delete[] arr; }

    void push_back(int val) {
        size_t local_cost = 1;

        if (size == capacity) {
            size_t new_cap = capacity * 2;
            int* new_arr = new int[new_cap];
            local_cost += size;  // Copy cost

            for (size_t i = 0; i < size; i++)
                new_arr[i] = arr[i];

            delete[] arr;
            arr = new_arr;
            capacity = new_cap;
        }

        arr[size++] = val;
        total_cost += local_cost;
    }

    double amortized_cost() const {
        return size > 0 ? (double)total_cost / size : 0;
    }

    long long potential() const {
        return 2 * size - capacity;
    }

    void print_stats(size_t n) {
        std::cout << "n=" << n << ": amortized=" << amortized_cost()
                  << ", potential=" << potential() << "\n";
    }
};

int main() {
    TrackedVector v;
    for (int i = 1; i <= 100; i++) {
        v.push_back(i);
        if (i <= 10 || i % 10 == 0)
            v.print_stats(i);
    }
    return 0;
}
```

---

## Phase 2 – Conceptual Stress Questions

**Q1**: Prove that for a dynamic array with doubling strategy, the potential function $\Phi(D) = 2 \cdot \text{size} - \text{capacity}$ gives $O(1)$ amortized cost for `push_back`. Analyze three cases: (a) no resize with room, (b) no resize near capacity, (c) resize triggered. Compute $\hat{c}_i$ for each.

**Q2**: A binary counter increments from 0 to $n$. Each bit flip costs 1 unit. Using the aggregate method, amortized cost is $O(1)$ per increment. Now suppose bit $i$ costs $2^i$ to flip. What is the new amortized cost? Design a potential function to prove your answer.

**Q3**: Splay trees have $O(\log n)$ amortized search but $O(n)$ worst-case single search. Can you construct a persistent (immutable) version that preserves $O(\log n)$ amortized cost? If not, prove why the potential method fails for persistent structures.

---

## Phase 3 – Applied Problem

**Problem Statement**:

Design a **deque** (double-ended queue) supporting:
- `push_front(x)`, `push_back(x)`: insert at front/back
- `pop_front()`, `pop_back()`: remove from front/back

Implementation: **two dynamic arrays** with doubling/halving:
- `front_array`: stores front elements in reverse order
- `back_array`: stores back elements in normal order

**Resize Rules**:
- Double when `size == capacity`
- Halve when `size == capacity / 4` (prevents thrashing)

**Part A**: Define a potential function $\Phi$ accounting for both arrays that proves $O(1)$ amortized cost for all four operations.

**Part B**: Analyze this adversarial sequence:
```
push_back(1), ..., push_back(n)
pop_back(), ..., pop_back() [n/4 times]
push_back(...), ... [n/4 times]
```
Compute actual total cost and verify your amortized bound.

**Part C**: Compare with a **circular buffer** implementation:
- Worst-case single operation cost
- Amortized cost
- Space overhead

When would you prefer each design?

---

## Phase 4 – Feedback & Weakness Log Update

**Awaiting your responses to Phase 2 and Phase 3.**

Critique will focus on:
- Rigor of potential function construction
- Handling $\Phi \geq 0$ invariant
- Distinction between worst-case and amortized
- Quantitative precision in cost accounting

---

## Cross-Links for Reinforcement
- [[Dynamic Arrays & Reallocation]]
- [[Splay Trees & Self-Adjusting Structures]]
- [[Fibonacci Heaps]]
- [[Union-Find with Path Compression]]
- [[Persistent Data Structures]]
- [[Competitive Analysis]]

---

**Status**: Awaiting Phase 2 & 3 responses.
