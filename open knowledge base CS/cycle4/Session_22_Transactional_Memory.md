# Session 22 – Hardware Transactional Memory & Formal Verification

## Linked Domain
[[Computation & Memory]] × [[Databases & Concurrency]] × [[Discrete Math & Probability]]

**Cycle**: 4 (Expert Mastery)  
**Difficulty**: ⚫⚫⚫⚫

---

## Phase 1 – Clean Theory

### Definitions

**Transactional Memory (TM)**: Concurrency control mechanism where atomic blocks (transactions) execute speculatively and commit if no conflicts detected, abort and retry otherwise. Formally: provides atomicity and isolation without explicit locks.

**Hardware Transactional Memory (HTM)**: TM implemented in hardware using cache coherence protocol extensions. Examples: Intel TSX, IBM Power8 TM, ARM TME.

**Conflict Detection**:
- **Eager (Pessimistic)**: Detect conflicts as they occur during transaction execution. Abort immediately.
- **Lazy (Optimistic)**: Buffer writes, detect conflicts at commit. Allows more parallelism but more wasted work.

**Contention Management**: Policy for deciding which transaction aborts when conflict detected. Examples: timestamp-based, exponential backoff, priority-based, hourglass.

**Progress Guarantee Levels**:
- **Obstruction-Free**: A transaction makes progress if it executes in isolation
- **Lock-Free**: System-wide progress guaranteed (some transaction commits)
- **Wait-Free**: Per-transaction progress guaranteed (every transaction eventually commits)

**Serializability in TM**: Transaction history is equivalent to some serial execution. HTM typically provides **opacity** (stronger than serializability): aborted transactions also see consistent state.

**Capacity Limits**: HTM has bounded read-set/write-set capacity (typically limited by cache size). Transactions exceeding capacity abort unconditionally.

---

### Core Mechanism

**Intel TSX Architecture**:
```
XBEGIN label
  ... transactional code ...
  XEND
label:
  // Abort handler
```

**Implementation via Cache Protocol**:
- **Read-set**: Tracked via cache lines in Shared/Exclusive state with special "monitoring" bit
- **Write-set**: Buffered in cache, lines marked Modified with "transactional" bit
- **Conflict**: Any external write to monitored line → abort
- **Commit**: Clear transactional bits, make writes visible atomically
- **Abort**: Invalidate transactional cache lines, restore registers, jump to handler

**Abort Conditions** (Intel RTM):
1. Data conflict (coherence protocol detects conflicting access)
2. Limited resources (write-set > L1 cache capacity)
3. Unsupported instructions (syscalls, IO, floating-point in some modes)
4. Interrupts/exceptions/context switches
5. Speculative failure (rare, timing-dependent)

**Formal Semantics** (Simplified):
```
Transaction T = (read-set R, write-set W)
Conflict: T1 conflicts with T2 if (R1 ∩ W2 ≠ ∅) ∨ (W1 ∩ W2 ≠ ∅)

Commit condition: ∀ T' committed after T started: ¬conflict(T, T')
```

---

### Mental Model

**TM as Optimistic Concurrency Control**:
- Assume no conflicts → execute speculatively
- If conflicts arise → abort and retry
- Trade-off: wasted work on aborts vs. parallelism gains

**HTM as "Undo Log in Cache"**:
- Cache becomes the transaction buffer
- Commit = make cache visible
- Abort = invalidate cache
- Very efficient when fits in cache

**Progress Guarantees Hierarchy**:
```
Wait-Free (strongest, most expensive)
    ↓
Lock-Free (system progresses)
    ↓
Obstruction-Free (weakest, HTM provides this)
    ↓
Blocking (with locks, no progress guarantee)
```

**Key Insight**: HTM provides **best-effort** semantics. Not guaranteed to succeed. Always need fallback (usually locks). Pattern:
```cpp
for (int retries = 0; retries < MAX_RETRIES; retries++) {
    if (XBEGIN()) {
        // Transactional path
        XEND();
        return;
    }
}
// Fallback to lock-based path
```

---

### Edge Cases

1. **Capacity Abort Cascades**: Large transaction aborts due to capacity. Retry also aborts. Infinite loop if transaction always exceeds capacity. Need size analysis.

2. **Livelock under Contention**: Two transactions repeatedly conflict and abort each other. Neither makes progress. Exponential backoff doesn't guarantee progress (obstruction-free, not lock-free).

3. **Self-Invalidation**: Transaction reads then writes same location. On rollback, read-set invalidation might corrupt internal state if not careful. TSX handles this, but manual STM must track carefully.

4. **Asynchronous Aborts**: Interrupt or page fault inside transaction → abort. Makes reasoning about abort rates difficult. Can't be modeled as function of logical conflicts alone.

5. **Publication Problem**: After commit, another thread observes transactional writes. That thread must use memory fences to ensure visibility (HTM commit implies fence, but relaxed atomics might not observe).

---

### Common Mistakes

1. **Assuming HTM always succeeds**: Writing code with no fallback path. Production code must always have lock-based fallback.

2. **Using system calls in transactions**: Abort guaranteed. Must hoist syscalls outside transaction or use fallback.

3. **Not analyzing capacity**: Writing transactions accessing $>32$ KB data (typical L1 size). Capacity aborts unavoidable.

4. **Ignoring abort rate**: "It compiles, ship it!" In practice, >10% abort rate might make HTM slower than locks due to wasted work.

5. **Mixing TM with locks incorrectly**: Deadlock possible if lock-based fallback interacts with transactional path incorrectly. Lock must be in write-set of transaction to detect conflict.

---

### Code Snippet – HTM with Lock Fallback

```cpp
#include <immintrin.h>  // Intel TSX intrinsics
#include <atomic>
#include <mutex>
#include <iostream>

class HTM_Counter {
    uint64_t value = 0;
    std::mutex fallback_lock;
    
    // Statistics
    std::atomic<uint64_t> commit_count{0};
    std::atomic<uint64_t> abort_count{0};
    std::atomic<uint64_t> fallback_count{0};
    
public:
    void increment() {
        constexpr int MAX_RETRIES = 3;
        
        for (int attempt = 0; attempt < MAX_RETRIES; attempt++) {
            unsigned status = _xbegin();
            
            if (status == _XBEGIN_STARTED) {
                // Transaction started successfully
                // Speculatively read lock to detect conflicts with fallback path
                if (fallback_lock.try_lock()) {
                    fallback_lock.unlock();
                    _xabort(0xFF);  // Explicit abort if lock held
                }
                
                value++;
                _xend();
                commit_count.fetch_add(1, std::memory_order_relaxed);
                return;
            } else {
                // status contains abort reason
                abort_count.fetch_add(1, std::memory_order_relaxed);
                
                // Check if abort due to conflict with locked section
                if ((status & _XABORT_EXPLICIT) && _XABORT_CODE(status) == 0xFF) {
                    break;  // Fall back to lock immediately
                }
                
                // If capacity or conflict abort, retry with backoff
                if (status & (_XABORT_CAPACITY | _XABORT_CONFLICT)) {
                    // Exponential backoff
                    for (int i = 0; i < (1 << attempt); i++) {
                        _mm_pause();
                    }
                    continue;
                }
                
                // Other aborts (e.g., interrupts), fall back
                break;
            }
        }
        
        // Fallback to lock
        std::lock_guard<std::mutex> guard(fallback_lock);
        value++;
        fallback_count.fetch_add(1, std::memory_order_relaxed);
    }
    
    uint64_t get() const { return value; }
    
    void print_stats() const {
        uint64_t total = commit_count + fallback_count;
        std::cout << "Commits: " << commit_count << " (" 
                  << (100.0 * commit_count / total) << "%)\n";
        std::cout << "Aborts: " << abort_count << "\n";
        std::cout << "Fallback: " << fallback_count << " ("
                  << (100.0 * fallback_count / total) << "%)\n";
    }
};

// Usage
// Compile: g++ -O2 -mrtm -std=c++17 -pthread htm_counter.cpp
// Requires: Intel CPU with TSX support (post-2013, pre-2021 microcode)
```

---

## Phase 2 – Conceptual Stress Questions

**Q1 – Formal Verification**: Define a formal semantics for HTM. Let $\mathcal{H} = \langle T_1, \ldots, T_n \rangle$ be a history of transactions where each $T_i = (R_i, W_i, \text{commit/abort})$. Define:
- Conflict relation: $T_i \rightsquigarrow T_j$
- Serialization graph: $G_{\mathcal{H}}$
- Prove: A history is serializable iff $G_{\mathcal{H}}$ is acyclic.

Now consider **opacity** (stronger than serializability): even aborted transactions must observe consistent state. Formalize opacity. Give an example history that is serializable but not opaque. Why does HTM need opacity?

**Q2 – Progress Analysis**: Intel TSX provides obstruction-free progress (not lock-free). Prove that under adversarial scheduling, TSX can fail to make system-wide progress. Construct an explicit counterexample with 2 threads and 1 shared variable.

Now design a **contention manager** that upgrades TSX to lock-free progress. Your manager can delay transactions but not abort them explicitly. Prove lock-freedom holds. What's the worst-case latency for a transaction to commit? Compare with standard lock-based mutual exclusion.

**Q3 – Capacity Analysis**: Analyze the read-set/write-set capacity of Intel TSX. Given:
- L1 cache: 32 KB, 64-byte lines, 8-way associative
- TSX uses L1 for buffering
- Cache eviction policy: LRU within each set

A transaction accesses addresses $a_1, \ldots, a_k$ (writes). Derive:
- Maximum $k$ before guaranteed capacity abort (worst-case address mapping)
- Expected $k$ before capacity abort (random address distribution)
- How does associativity affect capacity? Compare direct-mapped vs 8-way vs fully-associative.

Extension: If transaction has $r$ reads and $w$ writes, derive capacity as function of $(r, w)$. At what ratio $r/w$ is capacity maximized?

---

## Phase 3 – Applied Problem

**Problem Statement**:

You're implementing a **lock-free hash table** using Intel TSX for a high-frequency trading system (latency-critical). Requirements:
- $10^7$ inserts/sec across 64 threads
- p99.9 latency < 1µs
- Hash table: 1M buckets, chaining with linked lists

**Part A – HTM Design**:
Each operation wraps a transaction:
```cpp
bool insert(K key, V value) {
    _xbegin();
    Bucket& b = buckets[hash(key)];
    // Check for duplicates
    // Insert new node
    _xend();
}
```

Analyze capacity constraints:
- Per-bucket max chain length before capacity abort?
- Abort rate as function of load factor $\alpha = n / \text{buckets}$?
- At what $\alpha$ does HTM become slower than lock-based due to aborts?

Design a **hybrid approach**: use HTM for short chains, locks for long chains. Derive the optimal threshold. Prove correctness (transactions and locks can coexist).

**Part B – Research-Level Optimization**:
Observation: Most aborts are due to false conflicts (different keys, same cache line). You propose:
1. **Cache-conscious layout**: Pad each bucket to cache-line boundary
2. **Probabilistic early abort**: Predict conflict likelihood, abort proactively
3. **Asymmetric TM**: Readers transactional, writers use locks (or vice versa)

For each optimization:
- Analyze space/time trade-offs
- Compute expected abort reduction
- Identify scenarios where it hurts performance
- Cite recent papers (2020-2026) exploring similar ideas

**Part C – Formal Verification**:
Use a model checker (e.g., TLA+, Spin) to verify your HTM hash table. Specify:
- Safety: no lost updates, no duplicate keys
- Liveness: operations eventually complete (under what assumptions?)
- Opacity: aborted operations don't corrupt state

What invariants do you need to check? At what scale is model checking feasible (# threads, # operations)? If state space explodes, how do you use abstraction to scale verification?

**Part D – Novel Contribution**:
Current HTM systems abort on capacity overflow. You propose **Elastic Transactional Memory**: automatically partition large transactions into sub-transactions, commit incrementally.

Design the protocol:
- How do you partition atomically? (Breaks TM semantics!)
- What consistency guarantee can you provide? (Not serializability, but what?)
- Under what conditions is this safe?
- Prove correctness for a restricted class of transactions (e.g., commutative operations)

Write a 2-page paper abstract describing your contribution, related work, and evaluation plan.

---

## Phase 4 – Feedback & Weakness Log Update

**Awaiting your responses to Phase 2 and Phase 3.**

Critique will focus on:
- Formalism and proof rigor (not just intuition)
- Research-level depth (citing papers, novelty)
- Cross-domain integration (TM + concurrency + formal methods)
- Ability to design new protocols
- Critical analysis of existing work

---

## Cross-Links for Reinforcement
- [[Session 4: Transaction Isolation]]
- [[Session 8: NUMA & Cache Coherence]]
- [[Session 15: Memory Models]]
- [[TLA+ Specifications for Concurrency]]
- [[Recent Papers: TSX, ARM TME (2020-2026)]]
- [[Herlihy & Moss: Transactional Memory (Original Paper)]]

---

## Research Papers to Read

1. **Intel TSX**: "Evaluation of Intel Transactional Synchronization Extensions" (Yoo et al., 2013)
2. **HTM Limitations**: "Performance Implications of Transient Loop Nests in Hardware Transactional Memory" (2021)
3. **Formal Verification**: "Model Checking Transactional Memories" (Guerraoui et al., 2008)
4. **Elastic TM**: Your contribution! (Or see "Transactions Across Persistent Memory Partitions", 2023)

---

**Status**: Awaiting Phase 2 & 3 responses.
