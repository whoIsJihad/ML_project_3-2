# Session 8 – NUMA & Cache Coherence Protocols

## Linked Domain
[[Computation & Memory]]

**Cycle**: 2 (Intermediate Depth)  
**Difficulty**: ⚫⚫⚪⚪

---

## Phase 1 – Clean Theory

### Definitions

**Non-Uniform Memory Access (NUMA)**: Multi-processor architecture where memory access time depends on memory location relative to the processor. Formally: $\text{latency}(p, m) = \begin{cases} L_{\text{local}} & \text{if } m \in \text{local}(p) \\ L_{\text{remote}} & \text{otherwise} \end{cases}$ where typically $L_{\text{remote}} = 2-3 \times L_{\text{local}}$.

**Cache Coherence**: Guarantee that all processors see consistent view of memory. Formally: For shared variable $x$, all processors must observe writes to $x$ in some consistent order.

**MESI Protocol** (Modified, Exclusive, Shared, Invalid):
- **Modified**: Cache line is dirty, only this cache has it
- **Exclusive**: Cache line is clean, only this cache has it
- **Shared**: Cache line is clean, multiple caches may have it
- **Invalid**: Cache line is not valid

**Directory-Based Coherence**: Maintain directory tracking which caches have each memory line. Scales better than snooping for large systems ($O(1)$ messages vs $O(N)$ broadcast).

**False Sharing**: Two threads access different variables that reside on the same cache line, causing ping-ponging even though there's no logical conflict.

---

### Core Mechanism

**MESI State Transitions**:
```
PrRd = Processor Read, PrWr = Processor Write
BusRd = Bus Read, BusRdX = Bus Read Exclusive

Invalid --PrRd--> Shared (if others have it) or Exclusive (if not)
Invalid --PrWr--> Modified
Shared --PrWr--> Modified (send BusRdX to invalidate others)
Shared --BusRdX--> Invalid
Exclusive --PrWr--> Modified
Modified --BusRd--> Shared (write back to memory)
```

**NUMA Topology**:
```
CPU0 ─┬─ L1/L2 Cache
      └─ Memory Controller ─── Local DRAM
                            └─ Interconnect ─── Remote DRAM
```

**Performance Model**:
- Local access: ~100ns
- Remote access (same socket): ~140ns  
- Remote access (cross-socket): ~200ns
- Cross-NUMA write with coherence: ~300-500ns

**Directory Entry Structure**:
- Pointer to each cache holding the line
- State (shared/exclusive/modified)
- Space overhead: $O(P \cdot M / B)$ where $P$ = processors, $M$ = memory, $B$ = block size

---

### Mental Model

**Key Insight**: Cache coherence protocols are distributed consensus algorithms for memory consistency. Each cache line has an "owner" and state transitions require agreement.

**False Sharing as Distributed Lock Contention**:
Think of a cache line as a mutex. Even if threads access different bytes, they contend for the cache line lock. Solution: pad structures to cache line boundaries.

**NUMA Placement Strategy**:
- **First-touch policy**: Page allocated on first-accessing node
- **Interleave policy**: Round-robin across nodes (good for bandwidth)
- **Explicit binding**: `numactl --cpunodebind=0 --membind=0`

---

### Edge Cases

1. **Thundering Herd on Invalidation**: Write to widely-shared cache line causes broadcast invalidation to all caches. Can saturate coherence bus.

2. **Home Node Latency**: In directory-based systems, even local reads may go through remote "home node" if directory is distributed incorrectly.

3. **TLB Shootdown**: When unmapping pages, must invalidate TLBs on all cores. This is a coherence operation and can be very expensive ($O(\text{cores})$ IPIs).

4. **NUMA Balancing Oscillation**: Automatic NUMA balancing (kernel feature) can cause pages to migrate back and forth between nodes, hurting performance.

5. **Coherence Traffic on RMW**: Read-modify-write operations require exclusive ownership. On contended lock, this causes cache line to bounce between cores at ~100ns per bounce.

---

### Common Mistakes

1. **Assuming UMA on multi-socket systems**: Writing code that works well on single-socket but degrades on NUMA due to random memory placement.

2. **Not padding shared structures**: Declaring `struct { atomic<int> a; atomic<int> b; }` without ensuring `a` and `b` are on different cache lines.

3. **Ignoring coherence traffic in profiling**: Focusing on computational cost while cache coherence consumes 30% of cycles (visible via `perf` cache-misses + cache-references).

4. **Using global counters**: A single global `atomic<int> counter` shared across threads is a coherence disaster. Use per-thread counters + periodic aggregation.

5. **Misunderstanding MESI overhead**: Thinking "read-only" data has no coherence cost. Even shared reads can cause invalidations if interleaved with writes from other threads.

---

### Code Snippet – False Sharing Demonstration

```cpp
#include <iostream>
#include <thread>
#include <atomic>
#include <vector>
#include <chrono>

// Problematic: false sharing
struct CountersBad {
    std::atomic<long> count1{0};
    std::atomic<long> count2{0};
};

// Fixed: cache line padding
struct alignas(64) CountersGood {
    std::atomic<long> count1{0};
    char pad[64 - sizeof(std::atomic<long>)];
    std::atomic<long> count2{0};
};

template<typename T>
double benchmark(T& counters, int iterations) {
    auto start = std::chrono::high_resolution_clock::now();
    
    std::thread t1([&]() {
        for (int i = 0; i < iterations; i++) {
            counters.count1.fetch_add(1, std::memory_order_relaxed);
        }
    });
    
    std::thread t2([&]() {
        for (int i = 0; i < iterations; i++) {
            counters.count2.fetch_add(1, std::memory_order_relaxed);
        }
    });
    
    t1.join();
    t2.join();
    
    auto end = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double>(end - start).count();
}

int main() {
    const int ITER = 10'000'000;
    
    CountersBad bad;
    CountersGood good;
    
    double time_bad = benchmark(bad, ITER);
    double time_good = benchmark(good, ITER);
    
    std::cout << "False sharing (bad): " << time_bad << "s\n";
    std::cout << "Cache-line aligned (good): " << time_good << "s\n";
    std::cout << "Speedup: " << (time_bad / time_good) << "x\n";
    
    return 0;
}

// Compile: g++ -O3 -pthread false_sharing.cpp
// Expected: 2-5x speedup on multi-socket NUMA system
```

---

## Phase 2 – Conceptual Stress Questions

**Q1**: A 4-socket NUMA system has 16 cores per socket. You run 64 threads (4 per core with SMT). Each thread increments a shared counter using `fetch_add`. Assuming MESI protocol and 64-byte cache lines:
- Compute the rate of cache line transfers if each increment takes 5ns compute + coherence overhead
- If coherence latency is 200ns per transfer, what's the effective throughput (increments/sec)?
- How does this compare to theoretical peak if there were no coherence overhead?

**Q2**: In a directory-based system with 1024 nodes, each cache line is 64 bytes. The directory needs to track which nodes have each line. Three schemes:
- **Full bit-vector**: 1 bit per node (1024 bits = 128 bytes per line)
- **Limited pointers**: Track up to $k=8$ sharers, use broadcast if $>8$
- **Sparse directory**: Hash table of (line, sharer-set) pairs

Analyze space overhead and worst-case coherence message complexity for each. When would you choose each scheme?

**Q3**: You profile a multithreaded application and observe:
```
L1 cache hit rate: 95%
L2 cache hit rate: 99% (of L1 misses)
LLC cache hit rate: 85% (of L2 misses)
CPU utilization: 40%
```
But wall-clock time is poor. You suspect coherence overhead. How do you measure coherence traffic? What `perf` counters would you use? If coherence misses are 20% of all LLC accesses, how much could you gain by eliminating false sharing?

---

## Phase 3 – Applied Problem

**Problem Statement**:

You're optimizing a **parallel hash table** with 1M buckets for a 4-socket NUMA system (64 cores total, 16 per socket). Workload: 80% reads, 20% writes, uniformly distributed.

**Part A – NUMA Placement**:
- If hash table is allocated on socket 0, what's the expected access latency for threads on other sockets? 
- You partition the hash table across NUMA nodes (256K buckets per socket). De rive expected latency now. Assume: local = 100ns, remote = 200ns.
- What's the speedup? At what read/write ratio does partitioning hurt due to cross-socket write traffic?

**Part B – Coherence Analysis**:
Each bucket has a lock (1 byte). You pack 64 bucket locks into a single cache line. Under write-heavy workload (50% writes), compute:
- Probability two threads contend for *different* buckets but *same* cache line
- Expected coherence traffic (cache line transfers/sec) if operations take 100ns each
- Redesign: one lock per cache line (64 bytes). Compare coherence traffic and space overhead.

**Part C – MESI Trace**:
Consider 2 cores accessing shared variable `x` (initially in memory):
```
Time  Core0         Core1         MESI State (Core0, Core1)
0     -             -             I, I
1     Read x        -             ?, ?
2     -             Read x        ?, ?
3     Write x       -             ?, ?
4     -             Read x        ?, ?
```
Fill in MESI states. How many cache line transfers occur? Now add a third core that only reads `x`—how does the protocol change?

---

## Phase 4 – Feedback & Weakness Log Update

**Awaiting your responses to Phase 2 and Phase 3.**

Critique will focus on:
- Quantitative analysis of coherence overhead
- Understanding NUMA latency composition
- MESI protocol state transitions
- System-level design decisions (partitioning, padding)
- Profiling and measurement methodology

---

## Cross-Links for Reinforcement
- [[Session 1: Memory Hierarchy]] (prerequisite)
- [[MOESI & MESIF Protocols]]
- [[Lock-Free Data Structures]]
- [[Hardware Transactional Memory]]
- [[Linux NUMA API]]
- [[Cache Line Bouncing]]

---

**Status**: Awaiting Phase 2 & 3 responses.
