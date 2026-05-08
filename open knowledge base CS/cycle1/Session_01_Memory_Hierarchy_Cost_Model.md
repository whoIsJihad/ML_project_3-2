
---


# Session 1 — Memory Hierarchy & Cost Model

## 1. The Hierarchy

Each level is faster, smaller, and more expensive per byte than the one below it. The CPU always checks upward — L1 first, then L2/L3, then RAM, then storage. The goal is to keep hot data near the top.

**Cache line**: the minimum transfer unit between any two levels, typically **64 bytes**. When you read one byte, 64 bytes come with it. This is what makes spatial locality exploitable at all.

---
![[Pasted image 20260401150455.png]]
## 2. Locality

Caches work because programs are predictable in two ways:

- **Temporal**: if you accessed address A recently, you'll probably access it again. Keep it warm.
- **Spatial**: if you accessed A, you'll probably access A+1, A+2, ... soon. Fetching a full 64-byte line exploits this for free.

When your access pattern violates spatial locality — say, stepping through a matrix column-by-column in a row-major language — every access lands on a different cache line, and you pay full DRAM latency every time.

---

## 3. Cache Addressing

A physical address is split into three fields:

```
[ Tag ] [ Set Index ] [ Block Offset ]
```

|Field|Size|Role|
|---|---|---|
|Block Offset|log₂(line size)|Which byte within the 64-byte line|
|Set Index|log₂(num sets)|Which row (set) in the cache array|
|Tag|remaining bits|Verifies this line is actually what we asked for|

The hardware doesn't search — it uses the set index as a direct array index, then compares the tag. The lookup is O(1) in hardware.

**Associativity** is how many slots each set has. A direct-mapped cache (1-way) forces every address to one slot; conflicts evict data even when the cache is mostly empty. K-way set-associative gives each address K candidate slots, reducing conflicts. Fully associative has no index bits — maximum flexibility, but requires comparing all tags simultaneously, which is expensive in area and power. Real caches are typically 4–16 way.

---

## 4. AMAT — and Why Miss Rate Is Treacherous

$$\text{AMAT} = \text{Hit Time} + (\text{Miss Rate} \times \text{Miss Penalty})$$

This looks linear, but the miss penalty (~200 cycles to DRAM) dominates so completely that small miss rate changes are catastrophic. Consider:

|Miss Rate|AMAT (L1 hit = 4 cycles, penalty = 200)|
|---|---|
|1%|4 + 0.01 × 200 = **6 cycles**|
|5%|4 + 0.05 × 200 = **14 cycles**|
|10%|4 + 0.10 × 200 = **24 cycles**|

A 10× increase in miss rate produces a 4× increase in AMAT — not 10×, because hit time buffers the lower end. But going from 1% to 10% miss rate is the difference between a program that feels cache-resident and one that effectively runs at DRAM speed.

This is why profiling cache behavior matters. A 1% miss rate change that looks trivial in isolation can halve your throughput.

---

## 5. Replacement & Write Policies

**Replacement** decides which line gets evicted when a set is full. LRU is optimal for temporal locality but expensive to implement exactly at high associativity — most CPUs use pseudo-LRU approximations.

**Write policy** determines when stores propagate to lower levels:

- **Write-through**: every store immediately updates the next level. Simple coherence, but high bandwidth.
- **Write-back**: stores only update the cache; the line is written to lower memory when evicted. The line is marked _dirty_ to track this.

Write-back is standard in modern CPUs. The implication that's often missed: **dirty lines incur write traffic on eviction, even during read-heavy workloads**. If your working set churns — many different addresses each written once — you're generating significant write-back traffic that your read-centric analysis wouldn't predict.

---

## 6. Pitfalls Worth Understanding Deeply

**False sharing** is a coherence problem, not a capacity problem. In a multicore system, cache coherence operates at the granularity of cache lines, not variables. If two threads write different variables that happen to share a cache line, every write by one thread invalidates the other thread's copy — even though they're touching different memory locations. The result is cache line bouncing between cores, and it can reduce parallel speedup to near-zero. The fix is to pad or align hot per-thread variables to separate cache lines.
#### Article Link : https://medium.com/@khaled.smq/the-silent-killer-of-multi-threaded-performance-false-sharing-5a6b7439a0aa
```c
// Broken: x and y share a cache line
struct { int x; int y; } counters;

// Fixed: each on its own line
struct { int x; char _pad[60]; int y; char _pad2[60]; } counters;
```

Read this to know more [[False Sharing]]
**Cache thrashing** happens when your working set has more addresses that map to the same set than the cache has ways. This is a function of the stride between addresses and the cache geometry. 
A classic case: two large arrays whose sizes are multiples of the cache capacity, accessed in lockstep. Their elements index to identical sets, and they evict each other repeatedly. Increasing the associativity or slightly changing array sizes (adding a few bytes of padding) can eliminate it.
#### Read this to know more : [[Cache Thrashing Example]]
**Stride access and row-major confusion**: in C and C++, 2D arrays are row-major — `A[0][0], A[0][1], ..., A[0][N-1], A[1][0], ...`. Iterating `A[j][i]` (column-major order) steps through memory with stride N, hitting a new cache line every access. For a 1000×1000 float array, that's 4 million cache misses vs. ~62,000 for row-major traversal.

[[Pointer chasing]] :  (linked lists, trees) defeats the hardware prefetcher because each node's address is only known after loading the previous node. The prefetcher needs ahead-of-time address information to be useful. Arrays allow the prefetcher to predict addresses far in advance. This is why array-based structures outperform pointer-based ones even at the same asymptotic complexity.

**Write-back dirty eviction cost**: programmers often model cache behavior as "hit or miss on reads." But in write-back caches, evicting a dirty line is a write, and it competes for memory bus bandwidth with your reads. A memory-intensive program writing scattered small updates can saturate the bus with dirty evictions, starving the reads.

---

## Common Mistakes

1. **Column-major traversal in C/C++**: `A[j][i]` vs `A[i][j]` — the single most common cache miss source in numerical code.
2. **Ignoring struct padding**: `struct { char c; long l; }` — the long is 7 bytes offset by default, likely crossing a cache line boundary on access.
3. **Assuming linked structures are fine if they fit in cache**: they can be cache-resident but still slow, because pointer chasing serializes memory access.
4. **Assuming "read-only" means no write traffic**: dirty evictions happen regardless of the current operation's intent.
5. **Cache-size-specific optimization**: code tuned for one cache size may thrash on another. Cache-oblivious algorithms (recursive tiling) adapt across the hierarchy without hard-coded parameters.
### Code Snippet – Cache Benchmark

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define KB (1024)
#define MB (1024 * KB)

void stride_access(char* arr, size_t size, size_t stride) {
    size_t count = 0;
    for (size_t i = 0; i < size; i += stride) {
        arr[i]++;
        count++;
    }
}

int main() {
    size_t size = 32 * MB;
    char* arr = (char*)malloc(size);
    
    size_t strides[] = {1, 8, 64, 256, 1024, 4096};
    
    for (int s = 0; s < 6; s++) {
        clock_t start = clock();
        stride_access(arr, size, strides[s]);
        clock_t end = clock();
        
        double time = (double)(end - start) / CLOCKS_PER_SEC;
        printf("Stride %4zu bytes: %.4f sec\n", strides[s], time);
    }
    
    free(arr);
    return 0;
}
```

**Expected behavior**: Stride 64 (cache line size) shows first significant slowdown. Stride 4096 (page size) shows second cliff.

---

## Phase 2 – Conceptual Stress Questions

**Q1**: A cache is 32 KB, 8-way set-associative, with 64-byte lines. You have four arrays `A[1024]`, `B[1024]`, `C[1024]`, `D[1024]` (each element is 8 bytes), allocated sequentially in memory starting at address 0x10000. You perform `for (i = 0 to 1023) D[i] = A[i] + B[i] + C[i];` How many cache sets are there? Will conflict misses occur? Explain the mapping precisely.

**Q2**: You're debugging a multithreaded counter. Each thread increments its own `count` variable in a shared struct: `struct { long count[NUM_THREADS]; }`. Performance degrades superlinearly as threads increase. Top suspects: lock contention or false sharing. How do you distinguish between them experimentally? What would you measure?

**Q3**: System has: L1 = 4 cycles, L2 = 12 cycles, DRAM = 100 cycles. L1 hit rate = 90%, L2 hit rate (on L1 miss) = 75%. Compute Average Memory Access Time (AMAT). Now, you optimize code and increase L1 hit rate to 95% but decrease L2 hit rate to 60%. Is this always better? Prove or provide a counter-scenario.

---

## Phase 3 – Applied Problem

**Problem Statement**:

You are implementing a hash table with **chaining** for collision resolution. Each bucket is a linked list. Table has $n$ buckets, and you insert $m$ elements uniformly at random.

**Part A**: What is the expected number of cache misses during a single lookup, assuming:
- The hash table bucket array fits entirely in L1 cache
- Each linked list node is 32 bytes (one cache line)
- Cache is cold (no prior accesses)
- Chain length is $\lambda = m/n$

**Part B**: Your colleague suggests switching to **open addressing with linear probing**. Each entry is still 32 bytes. Under the same assumptions, derive the expected cache misses during a failed lookup with load factor $\alpha = m/n < 1$.

**Part C**: At what load factor $\alpha$ does linear probing become worse than chaining in terms of cache misses? State assumptions explicitly.

---

## Phase 4 – Feedback & Weakness Log Update

**Awaiting your responses to Phase 2 and Phase 3.**

Once you provide your answers, I will critique:
- Logical rigor and completeness
- Missing assumptions or edge cases
- Quantitative vs qualitative reasoning
- Abstraction level
- Cross-domain connections

---

## Cross-Links for Reinforcement
- [[Cache-Oblivious Algorithms]]
- [[Memory Consistency Models]]
- [[Virtual Memory & TLB]]
- [[Lock-Free Data Structures]]
- [[External Memory Model]]
- [[NUMA Architectures]]

---

**Status**: Awaiting Phase 2 & 3 responses.
