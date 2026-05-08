# Session 15 – Memory Models & Weak Consistency

## Linked Domain
[[Computation & Memory]] × [[Networks & Distributed Systems]]

**Cycle**: 3 (Advanced Integration)  
**Difficulty**: ⚫⚫⚫⚪

---

## Phase 1 – Clean Theory

### Definitions

**Memory Consistency Model**: Contract specifying which values a read may return, given a history of writes. Formally: A set of allowed executions under concurrent memory operations.

**Sequential Consistency (Lamport)**: Result of any execution is as if operations of all processors were executed in some sequential order, and operations of each processor appear in program order. Formally:
$$\exists \text{total order } \prec \text{ s.t. } \forall p: a \xrightarrow{po_p} b \Rightarrow a \prec b$$

**Total Store Ordering (TSO)**: Relaxes SC by allowing reads to bypass writes to different addresses. Each core has FIFO write buffer. Model used by x86/x64.

**Release Consistency (RC)**: Distinguishes *acquire* and *release* operations. All operations before release must complete before release. All operations after acquire must wait for acquire.

**Happens-Before Relation**: $a \xrightarrow{hb} b$ if:
- $a$ and $b$ are on same thread and $a$ program-order-before $b$, or
- $a$ is a release and $b$ is an acquire on same variable, or  
- Transitive closure

**Data Race**: Two conflicting operations (at least one write, same location) with no happens-before ordering between them.

**DRF-SC** (Data-Race-Free guarantees Sequential Consistency): If program has no data races, execution is sequentially consistent even on weak memory models.

---

### Core Mechanism

**Memory Model Hierarchy**:
```
Sequential Consistency (SC)
    ↓ relax read-read, read-write reordering
Total Store Ordering (TSO)
    ↓ relax write-read reordering  
Partial Store Ordering (PSO)
    ↓ relax write-write reordering
Relaxed Memory Ordering (RMO)
    ↓ remove all guarantees (C++ relaxed)
```

**Litmus Test Examples**:

**Store Buffering (SB)**:
```
Thread 1:      Thread 2:
x = 1          y = 1
r1 = y         r2 = x
```
Can we observe `r1 == 0 && r2 == 0`?
- **SC**: No
- **TSO**: Yes (write buffers allow reads to overtake writes)
- **ARM/POWER**: Yes

**Message Passing (MP)**:
```
Thread 1:      Thread 2:
x = 1          r1 = y
y = 1          r2 = x
```
Can we observe `r1 == 1 && r2 == 0`?
- **SC**: No (if y=1 is visible, x=1 must be)
- **TSO**: No (write ordering preserved)
- **Relaxed**: Yes (requires memory fence)

**C++ atomic memory orderings**:
- `memory_order_relaxed`: No synchronization
- `memory_order_acquire`: Acquire barrier (for reads)
- `memory_order_release`: Release barrier (for writes)
- `memory_order_acq_rel`: Both acquire and release
- `memory_order_seq_cst`: Sequential consistency (default)

---

### Mental Model

**Key Insight**: Hardware optimizations (store buffers, speculative execution, memory coalescing) break intuitive memory semantics. Weak memory models expose these optimizations to software.

**Synchronization as "Syncing Timelines"**:
- Each thread has its own "view" of memory (timeline)
- Release-acquire synchronizes timelines
- Without synchronization, timelines diverge arbitrarily

**DRF-SC as Contract**:
- Hardware: "If you use synchronization correctly (no data races), I'll give you SC semantics"
- Software: "I'll use atomics/locks, so I can reason sequentially"
- This contract allows aggressive hardware optimizations while preserving programmer sanity

**Mapping to Distributed Systems**:
- Memory model ≈ consistency model in distributed systems
- TSO ≈ Timeline consistency
- Release-acquire ≈ Causal consistency
- Relaxed ≈ Eventual consistency

---

### Edge Cases

1. **Thin-Air Values**: Can a read return a value that was never written? Some weak models allow this through speculative execution. C++ forbids it but hardware may not.

2. **Dependency Ordering**: ARM has *address*, *data*, and *control* dependencies that impose ordering even without explicit barriers. But subtle: dependency must be genuine (not optimized away by compiler).

3. **Mixed-Size Accesses**: What if thread 1 writes 8-byte `long`, thread 2 reads as two 4-byte `int`s? Behavior is implementation-defined even in C++.

4. **Compiler vs Hardware Reordering**: Compiler can reorder independent operations *before* emitting code. Memory fences prevent hardware reordering but not compiler reordering. Need compiler barriers too.

5. **Consume Ordering (defunct)**: C++ `memory_order_consume` was intended for RCU-style patterns but no compiler implements it correctly. Promoted to acquire in practice.

---

### Common Mistakes

1. **Assuming SC on x86**: x86 is TSO, not SC. Store-buffering litmus test can observe non-SC behavior. Must use `MFENCE` or `LOCK` prefix for SC.

2. **Using `volatile` for synchronization**: `volatile` prevents compiler optimization but provides NO memory ordering guarantees. Not sufficient for multithreading.

3. **Mixing atomic and non-atomic accesses**: Accessing same location with both atomic and non-atomic operations is data race, even if atomic is `seq_cst`. Undefined behavior in C++.

4. **Thinking `relaxed` is "faster"**: `memory_order_relaxed` doesn't magically optimize code. It just removes ordering constraints. If you don't need ordering, use it. Otherwise, use acquire/release.

5. **Ignoring happens-before for DRF**: Claiming "no data race" but actually having data races due to misunderstanding happens-before (e.g., forgetting transitivity).

---

### Code Snippet – Demonstrating Weak Memory Ordering

```cpp
#include <atomic>
#include <thread>
#include <iostream>
#include <vector>

// Store Buffering Litmus Test
struct StoreBuffering {
    std::atomic<int> x{0}, y{0};
    int r1, r2;
    
    void thread1() {
        x.store(1, std::memory_order_relaxed);
        r1 = y.load(std::memory_order_relaxed);
    }
    
    void thread2() {
        y.store(1, std::memory_order_relaxed);
        r2 = x.load(std::memory_order_relaxed);
    }
    
    bool run() {
        x = 0; y = 0;
        std::thread t1(&StoreBuffering::thread1, this);
        std::thread t2(&StoreBuffering::thread2, this);
        t1.join(); t2.join();
        return (r1 == 0 && r2 == 0);  // Can this happen?
    }
};

// Message Passing with Acquire-Release
struct MessagePassing {
    int data = 0;
    std::atomic<bool> ready{false};
    
    void sender() {
        data = 42;  // Non-atomic write
        ready.store(true, std::memory_order_release);  // Release
    }
    
    int receiver() {
        while (!ready.load(std::memory_order_acquire)) {}  // Acquire
        return data;  // Guaranteed to see 42
    }
};

// Dekker's Algorithm (requires sequential consistency)
struct Dekker {
    std::atomic<bool> flag0{false}, flag1{false};
    int critical_section_count = 0;
    
    void thread0() {
        flag0.store(true, std::memory_order_seq_cst);
        while (flag1.load(std::memory_order_seq_cst)) {}
        critical_section_count++;
    }
    
    void thread1() {
        flag1.store(true, std::memory_order_seq_cst);
        while (flag0.load(std::memory_order_seq_cst)) {}
        critical_section_count++;
    }
    
    // With relaxed ordering, both threads can enter critical section!
};

int main() {
    // Test Store Buffering
    StoreBuffering sb;
    int sb_violations = 0;
    for (int i = 0; i < 100000; i++) {
        if (sb.run()) sb_violations++;
    }
    std::cout << "Store Buffering violations: " << sb_violations << "/100000\n";
    std::cout << "(Non-zero confirms weak memory ordering)\n\n";
    
    // Test Message Passing
    MessagePassing mp;
    std::thread sender(&MessagePassing::sender, &mp);
    std::thread receiver_thread([&]() {
        int val = mp.receiver();
        std::cout << "Message Passing: received " << val << " (should be 42)\n";
    });
    sender.join();
    receiver_thread.join();
    
    return 0;
}

// Compile: g++ -O2 -std=c++17 -pthread weak_memory.cpp
// Expected: On x86, few SB violations. On ARM/POWER, more frequent.
```

---

## Phase 2 – Conceptual Stress Questions

**Q1**: Prove or disprove: If a program is data-race-free under SC semantics, it is data-race-free under TSO semantics. Start by formally defining what "data-race-free" means in each model. Consider the happens-before relation and how it changes between models.

**Q2**: The Linux kernel's RCU (Read-Copy-Update) relies on *data dependencies* for ordering without fences. Consider:
```cpp
// Thread 1 (updater)
Node* new_node = new Node{data};
ptr.store(new_node, memory_order_release);

// Thread 2 (reader)
Node* p = ptr.load(memory_order_consume);  // Or in practice, acquire
int val = p->data;
```
On ARM, if we use `memory_order_relaxed` instead of consume/acquire, can the read of `p->data` occur before the load of `ptr`? Explain using ARM's dependency ordering rules. What instruction prevents this? What's the performance difference between dependency vs fence?

**Q3**: Design a **sequentially consistent lock-free queue** on a TSO architecture (x86). You have:
- `XCHG` (atomic exchange, full barrier)
- `LOCK prefix` (full barrier)
- `MFENCE` (full fence)
- Regular loads/stores (can be reordered by store buffer)

Which operations need fences? Prove that without proper fences, the queue can violate SC. Compute the sequential consistency cost: how many fence instructions per enqueue/dequeue?

---

## Phase 3 – Applied Problem

**Problem Statement**:

You're designing a **lock-free work-stealing scheduler** for a 64-core ARM server. Each thread has a local deque (double-ended queue). Threads push/pop from their own deque's tail (LIFO), while other threads can "steal" from the head (FIFO).

**Part A – Memory Model Design**:
The deque uses:
```cpp
std::atomic<Task*> buffer[SIZE];
std::atomic<int> head;  // Steal from here
std::atomic<int> tail;  // Push/pop here
```

For each operation, specify the minimum required memory ordering and justify:
- `push()`: Write task, increment tail
- `pop()`: Decrement tail, read task
- `steal()`: Read head, read task, increment head

Consider: What happens if `pop()` and `steal()` race on the last element? How do you detect this race without using locks?

**Part B – Performance vs Correctness**:
You profile three implementations:
1. **Seq-cst**: All atomics use `memory_order_seq_cst` (99% correctness in stress tests)
2. **Acq-rel**: push uses release, steal uses acquire (97% correctness)
3. **Relaxed**: All use relaxed (85% correctness, but 2x faster)

The "incorrect" results are: empty task pointers or tasks executed twice. Diagnose which memory ordering violations cause each symptom. Can you design a hybrid approach that's both correct and fast? (Hint: differentiate fast-path vs slow-path.)

**Part C – Cross-Domain Integration** (Distributed + Memory Model):
Now extend to a distributed work-stealing scheduler across 8 machines. Each machine has 8 cores. You use:
- **Local stealing**: Same machine, shared memory (ARM weak ordering)
- **Remote stealing**: Different machine, RPC (network latency 500µs)

Design the combined system:
- When does a thread steal remotely vs locally?
- How do you maintain work distribution across machines?
- What consistency model suffices for the global work queue? (Hint: doesn't need to be sequential consistency)
- Analyze latency: local steal with fences vs remote steal with RPC. When is remote stealing preferred?

---

## Phase 4 – Feedback & Weakness Log Update

**Awaiting your responses to Phase 2 and Phase 3.**

Critique will focus on:
- Formal reasoning about happens-before
- Understanding hardware vs compiler reordering
- Correctly applying memory orderings (not just "use seq_cst everywhere")
- Integrating memory models with distributed systems concepts
- Performance analysis including fence costs

---

## Cross-Links for Reinforcement
- [[Session 5: Consistency Models]] (distributed analog)
- [[Session 8: NUMA & Cache Coherence]] (hardware foundation)
- [[C++ Memory Model Formalism]]
- [[ARM & POWER Memory Models]]
- [[RCU (Read-Copy-Update)]]
- [[Herlihy & Shavit: Art of Multiprocessor Programming]]

---

**Status**: Awaiting Phase 2 & 3 responses.
