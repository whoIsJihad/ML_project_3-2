# Session 5 – Consistency Models & CAP Spectrum

## Linked Domain
[[Networks & Distributed Systems]]

---

## Phase 1 – Clean Theory

### 1. Consistency Model Hierarchy

| Model | Guarantee | Coordination Cost | Example Systems |
|-------|-----------|-------------------|-----------------|
| **Linearizability** | Real-time total order | Highest (consensus) | ZooKeeper, etcd, Spanner |
| **Sequential Consistency** | Program-order total order | High | Some shared memory systems |
| **Causal Consistency** | Causal-order only | Moderate | Vector clock systems |
| **Eventual Consistency** | Convergence only | Lowest | Dynamo, Cassandra (default) |

---

### 2. Formal Definitions

**Linearizability**: Every operation appears atomic at some point between invocation and response. Exists total order $\prec$ such that:
- Real-time order preserved: if $op_1$ completes before $op_2$ starts, then $op_1 \prec op_2$
- Sequential semantics respected

**Sequential Consistency**: Operations appear in some total order consistent with each process's program order (no real-time constraint).

**Causal Consistency**: Causally-related operations seen in same order by all processes. Concurrent operations may be seen in different orders.

**Eventual Consistency**: If no new updates, all replicas eventually converge. No ordering guarantees.

---

### 3. CAP Theorem

In presence of network partitions, cannot simultaneously guarantee:

| Property | Definition |
|----------|------------|
| **Consistency** | Linearizability (all nodes see same data at same time) |
| **Availability** | Every request receives a response (non-error) |
| **Partition Tolerance** | System operates despite message loss |

**Choice**: Must pick 2 of 3. In practice: P is mandatory (networks fail), so choose C or A.

| Choice | Behavior During Partition | Example |
|--------|--------------------------|---------|
| **CP** | Sacrifice availability | ZooKeeper, etcd, HBase |
| **AP** | Sacrifice consistency | Dynamo, Cassandra, Riak |

---

### 4. Implementation Mechanisms

**Linearizability via Consensus**:
- Total order broadcast (Paxos, Raft)
- Each operation assigned global sequence number
- Cost: $O(\text{latency})$ per operation

**Causal Consistency via Vector Clocks**:
- Each process maintains vector $V[1..n]$
- $V[i]$ = events from process $i$ seen
- Causal order: $V_1 < V_2$ iff $\forall i: V_1[i] \leq V_2[i]$ and $\exists j: V_1[j] < V_2[j]$

**Eventual Consistency via CRDTs**:
- Conflict-Free Replicated Data Types
- Operations commute: $f(g(x)) = g(f(x))$
- Merge: associative, commutative, idempotent
- Examples: G-Counter, PN-Counter, LWW-Register

---

### 5. Key Trade-offs

**Consistency vs. Latency**:
```
Strong Consistency ←→ High Availability
     (CP)                  (AP)
       ↑                     ↑
   Consensus            Leaderless
   Synchronous          Asynchronous
   High latency         Low latency
```

**Real-time Constraint Cost**:
- Linearizability: requires wall-clock coordination (expensive)
- Sequential: program order only (cheaper)
- Causal: happens-before only (vector clocks)
- Eventual: no ordering (cheapest)

---

### 6. Edge Cases

1. **Monotonic Reads Violation**: Under eventual consistency, read $x=10$, then $x=5$ (stale replica).

2. **Causal Anomaly**: A writes $x$, messages B. If message arrives before replication, B's read may not see A's write.

3. **Asymmetric Partition**: A can send to B, but B cannot send to A. Breaks quorum assumptions.

4. **Clock Skew**: Timestamp-based sequential consistency fails with unsynchronized clocks.

5. **Split-Brain**: Network partition creates two leaders. Both accept writes; conflicts on heal.

---

### Common Mistakes

1. **"Eventually consistent" ≠ "converges quickly"**: "Eventually" has no time bound unless explicitly specified.

2. **Assuming linearizability is default**: Most distributed databases (Cassandra, Dynamo) provide eventual consistency by default.

3. **Ignoring partition behavior**: Testing only in healthy network. Partition behavior differs (e.g., Cassandra accepts writes, resolves conflicts later).

4. **CAP misinterpretation**: CAP applies **during partition**. When network healthy, you can have all three.

5. **Quorum ≠ Linearizability**: Quorum (R + W > N) ensures convergence but NOT linearizability (read-repair, sloppy quorums can violate).

---

### Code Snippet – Linearizability Violation Simulation

```python
import threading
import time
import random

class EventuallyConsistentKV:
    """Simulates eventually consistent KV store with replication lag."""

    def __init__(self, num_replicas=3, replication_delay_ms=100):
        self.replicas = [{} for _ in range(num_replicas)]
        self.delay = replication_delay_ms / 1000.0
        self.lock = threading.Lock()

    def write(self, key, value):
        """Write to primary, asynchronously replicate."""
        with self.lock:
            self.replicas[0][key] = value

        def replicate():
            time.sleep(self.delay + random.uniform(0, 0.05))
            with self.lock:
                for i in range(1, len(self.replicas)):
                    self.replicas[i][key] = value

        threading.Thread(target=replicate, daemon=True).start()

    def read(self, key):
        """Read from random replica."""
        replica_id = random.randint(0, len(self.replicas) - 1)
        with self.lock:
            return self.replicas[replica_id].get(key, None), replica_id

def test_linearizability_violation():
    store = EventuallyConsistentKV(num_replicas=3, replication_delay_ms=200)

    print("Write x = 10")
    store.write('x', 10)
    time.sleep(0.05)

    val1, r1 = store.read('x')
    print(f"Read 1: x = {val1} (replica {r1})")
    time.sleep(0.05)

    val2, r2 = store.read('x')
    print(f"Read 2: x = {val2} (replica {r2})")

    if val1 is not None and val2 is None:
        print("⚠️ Linearizability violated: saw value, then None")

    time.sleep(0.3)  # Wait for replication
    val3, r3 = store.read('x')
    print(f"Read 3: x = {val3} (replica {r3}) [after replication]")

if __name__ == "__main__":
    test_linearizability_violation()
```

---

## Phase 2 – Conceptual Stress Questions

**Q1**: Three operations on a register:
```
P1: write(x, 1) at time 0-10
P2: write(x, 2) at time 5-15
P3: read(x) → 2 at time 12-18, then read(x) → 1 at time 20-25
```
Is this linearizable? Draw possible linearization points. If not, what consistency model does it satisfy (sequential? causal? eventual?)?

**Q2**: Linearizable counter with 5 replicas using quorum (R=3, W=3, N=5). Prove or disprove: this guarantees linearizability. If not, what additional mechanism is needed? Consider: Client A writes count=10, Client B reads count=10, Client C reads count=5. Is this possible under quorum?

**Q3**: CAP says no C+A during partition. But **Spanner** claims strong consistency AND high availability. How? What's the catch? Analyze using formal CAP definitions.

---

## Phase 3 – Applied Problem

**Problem Statement**:

Design a **distributed collaborative document editor** (like Google Docs). Multiple users edit concurrently. Each character insertion/deletion is an operation.

**Part A – Linearizability**: Compute latency overhead:
- 3 replicas (US-East, US-West, Europe)
- Latencies: US-East ↔ US-West = 70ms, US ↔ Europe = 120ms
- Consensus requires majority (2 of 3)

What is minimum latency per keystroke for US-East user?

**Part B – Causal Consistency**: Design protocol using vector clocks:
- How to represent operations?
- How to track causality (vector clock updates)?
- How to handle concurrent insertions at same position?

Give concrete example with 2 concurrent users.

**Part C – CRDTs**: Design CRDT for text editing:
- Data structure?
- Handle `insert(pos, char)`?
- Ensure commutativity?
- Analyze space overhead: document has $n$ characters, $m$ edits—what is metadata size?

---

## Phase 4 – Feedback & Weakness Log Update

**Awaiting your responses to Phase 2 and Phase 3.**

Critique will focus on:
- Formal reasoning about consistency models
- Distinguishing linearizability vs sequential vs causal
- Quantitative latency analysis
- Protocol design precision
- CAP trade-off understanding

---

## Cross-Links for Reinforcement
- [[Consensus Algorithms (Paxos, Raft)]]
- [[Vector Clocks & Lamport Timestamps]]
- [[Conflict-Free Replicated Data Types]]
- [[Quorum Systems]]
- [[Google Spanner Architecture]]
- [[Operational Transformation]]

---

**Status**: Awaiting Phase 2 & 3 responses.
