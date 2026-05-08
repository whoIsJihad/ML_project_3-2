# Session 23 – Cache-Oblivious Algorithms

## Linked Domain
[[Computation & Memory]]

**Cycle**: 4 (Expert Mastery)  
**Difficulty**: ⚫⚫⚫⚫

---

## Phase 1: Theoretical Foundation

### Definitions

**Cache-Oblivious Algorithm**: An algorithm that achieves optimal cache complexity without knowledge of cache parameters (cache size M, block size B).

**Ideal Cache Model**: Two-level memory hierarchy with cache size M and block size B. Algorithm doesn't know M or B, but analysis assumes optimal replacement policy (LRU).

**I/O Complexity**: Number of cache misses (block transfers between cache and memory). Goal: minimize Q(n; M, B).

**Cache-Optimal**: Achieves optimal Q for all M and B (impossible for most problems). Cache-oblivious aims for optimal within constant factors.

### Core Mechanism: Divide-and-Conquer Recursion

**Key Insight**: Recursive algorithms automatically adapt to cache size without knowing M.

**Example: Matrix Multiplication (Cache-Oblivious)**
```
Naive: O(n³) operations, O(n³/B) cache misses (no reuse)
Blocked: O(n³) operations, O(n³/√M·B) cache misses (requires knowing M)
Recursive: O(n³) operations, O(n³/√M·B) cache misses (cache-oblivious!)
```

**Recursive Matrix Multiply**:
```
multiply(A, B, C, n):
  if n == 1:
    C[0,0] += A[0,0] * B[0,0]
  else:
    # Divide matrices into 2×2 blocks
    multiply(A11, B11, C11, n/2)
    multiply(A11, B12, C12, n/2)
    # ... 8 recursive calls total
```

**Why Cache-Oblivious Works**: When n²/8 ≤ M, all 3 matrices fit in cache → no misses during recursion. This happens automatically at some level without knowing M.

### Core Mechanism: Van Emde Boas Layout

**Problem**: Traversing binary tree in-order → many cache misses (children far apart in memory).

**Van Emde Boas (vEB) Layout**: Recursive memory layout:
```
Store tree T recursively:
1. Store root
2. Store top √h subtree (recursively)
3. Store bottom √h subtrees (recursively)
```

**Result**: Any root-to-leaf path of length h incurs O(log_B h) cache misses (vs O(h/B) for standard layout).

**Application**: B-trees become cache-oblivious with vEB layout.

### Mental Model

**Cache-Oblivious = Universal Adapter**: Like a power adapter that works in any country without you setting voltage manually. Algorithm automatically "tunes" to cache size via recursion depth.

**vEB Layout = Fractal Map**: Instead of storing cities linearly (A, B, C, D), store hierarchically: {New York: {Manhattan: {Upper East, Midtown}, Brooklyn}, Los Angeles: ...}. Nearby cities in hierarchy → nearby in memory.

### Edge Cases

**1. Tall Cache (B large relative to M)**
Most algorithms assume B = Θ(√M). If B = M (single huge block), cache-oblivious loses advantage—entire memory in one block.

**2. False Sharing**
Parallel cache-oblivious algorithms must avoid false sharing (multiple cores touch same cache line).

**3. TLB Misses**
Cache-oblivious helps with cache misses but ignores TLB. For very large arrays, TLB thrashing can dominate.

### Common Mistakes

1. **Assuming All Problems Have Cache-Oblivious Solutions**: Some problems (e.g., FFT with bit-reversal) inherently require cache knowledge.

2. **Ignoring Constants**: Cache-oblivious may have 2-3× higher constants than hand-tuned blocked code.

3. **Recursive Overhead**: Deep recursion has function call overhead. Cutoff to base case when n ≤ threshold.

### Code

```python
import numpy as np

def cache_oblivious_matmul(A, B, C, n, i1=0, j1=0, i2=0, j2=0, i3=0, j3=0):
    """
    Cache-oblivious matrix multiplication.
    C[i3:i3+n, j3:j3+n] += A[i1:i1+n, j1:j1+n] @ B[i2:i2+n, j2:j2+n]
    """
    if n <= 32:  # Base case: use naive multiplication
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i3+i, j3+j] += A[i1+i, j1+k] * B[i2+k, j2+j]
    else:
        # Divide into 2x2 blocks
        m = n // 2
        
        # C11 += A11*B11 + A12*B21
        cache_oblivious_matmul(A, B, C, m, i1, j1, i2, j2, i3, j3)
        cache_oblivious_matmul(A, B, C, m, i1, j1+m, i2+m, j2, i3, j3)
        
        # C12 += A11*B12 + A12*B22
        cache_oblivious_matmul(A, B, C, m, i1, j1, i2, j2+m, i3, j3+m)
        cache_oblivious_matmul(A, B, C, m, i1, j1+m, i2+m, j2+m, i3, j3+m)
        
        # C21 += A21*B11 + A22*B21
        cache_oblivious_matmul(A, B, C, m, i1+m, j1, i2, j2, i3+m, j3)
        cache_oblivious_matmul(A, B, C, m, i1+m, j1+m, i2+m, j2, i3+m, j3)
        
        # C22 += A21*B12 + A22*B22
        cache_oblivious_matmul(A, B, C, m, i1+m, j1, i2, j2+m, i3+m, j3+m)
        cache_oblivious_matmul(A, B, C, m, i1+m, j1+m, i2+m, j2+m, i3+m, j3+m)

# Van Emde Boas layout for binary tree
def veb_layout(tree, layout, index=0, start=0, end=None):
    """Convert tree to van Emde Boas memory layout"""
    if end is None:
        end = len(tree)
    
    if start >= end:
        return index
    
    # Store root
    mid = (start + end) // 2
    layout[index] = tree[mid]
    index += 1
    
    # Recursively store left and right subtrees
    index = veb_layout(tree, layout, index, start, mid)
    index = veb_layout(tree, layout, index, mid+1, end)
    return index

# Example
n = 128
A = np.random.randn(n, n)
B = np.random.randn(n, n)
C = np.zeros((n, n))

cache_oblivious_matmul(A, B, C, n)
C_numpy = A @ B
print(f"Error: {np.linalg.norm(C - C_numpy):.6f}")
```

---

## Phase 2: Stress Questions

### Q1: Cache Complexity Proof
**Prove that recursive matrix multiplication achieves Q(n; M, B) = Θ(n³/(B√M) + n²/B) cache misses.**

<details><summary>Hint</summary>
Use master theorem. When subproblem size fits in cache (n² ≤ M), misses = O(n²/B). Recurrence: Q(n) = 8Q(n/2) + O(n²/B) when n² > M.
</details>

### Q2: vEB Layout Analysis
**Prove that vEB layout achieves O(log_B n) cache misses for root-to-leaf path in binary tree of n nodes.**

<details><summary>Hint</summary>
Tree height h = log n. At each level of vEB recursion, traverse O(1) subtrees. Subtrees at level i have height h/2^i. Total levels = log h = log log n. But group into blocks → O(log_B h).
</details>

### Q3: Sorting Cache Complexity
**Funnel sort is cache-oblivious and achieves O((n/B) log_{M/B} (n/B)) cache misses. Compare to merge sort and explain why funnel sort is optimal.**

<details><summary>Hint</summary>
Merge sort: Θ((n/B) log_M n) when blocked optimally. Funnel sort uses k-way merge with k = √M, achieving O((n/B) log_{M/B} n) = optimal I/O complexity.
</details>

---

## Phase 3: Applied Problem

Implement cache-oblivious algorithms for:
1. **Matrix Transpose**: Recursive transpose achieving O(n²/B) cache misses
2. **Binary Search**: vEB layout achieving O(log_B n) cache misses
3. **Fractal Tree Index**: Cache-oblivious B-tree alternative

Compare performance against:
- Naive implementations
- Hand-tuned blocked versions (with known cache size)

Measure cache misses using hardware counters (perf on Linux).

---

## Phase 4: Self-Assessment

### Checklist
- [ ] Understand ideal cache model and I/O complexity
- [ ] Can design recursive cache-oblivious algorithms
- [ ] Know vEB layout and applications
- [ ] Understand when cache-oblivious is appropriate
- [ ] Can analyze cache miss complexity

### Next Steps
- **Strong**: [[Session 24 – Approximation Algorithms]]
- **Resources**: "Cache-Oblivious Algorithms" (Frigo et al.), CLRS Ch. 28

---

**Navigation**: ← [[Session 22]] | **Index**: [[cycle4/INDEX]] | → [[Session 24]]
