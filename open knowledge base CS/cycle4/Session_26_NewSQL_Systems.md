# Session 26 – NewSQL & Deterministic Databases

**Cycle**: 4 (Expert Mastery)  
**Domain**: Databases & Concurrency  
**Difficulty**: ⚫⚫⚫⚫

**Prerequisites**: ACID properties, distributed transactions, consensus algorithms

---

## Phase 1: Core Theory & Mental Models

### 1.1 Definitions

**NewSQL**: Distributed relational databases providing ACID guarantees at scale while maintaining SQL interface.

**Deterministic Execution**: Transaction execution order is pre-determined before execution, eliminating coordination overhead during execution.

**External Consistency** (Google Spanner): If transaction T1 commits before T2 starts, then T1's timestamp < T2's timestamp.

**TrueTime API**: Google's service providing timestamp intervals [earliest, latest] with bounded uncertainty.

**Calvin Architecture**: Deterministic database design with three layers:
1. **Sequencing layer**: Assigns global order to transactions
2. **Scheduling layer**: Coordinates lock acquisition
3. **Storage layer**: Executes transactions

### 1.2 Core Mechanisms

**Calvin Transaction Processing**:
```
1. Client submits transaction
2. Sequencer assigns global sequence number
3. Transaction replicated to all nodes (via Paxos)
4. Scheduler acquires locks in sequence order (deterministic)
5. Execute transaction deterministically
6. Release locks, commit
```

**Key Insight**: Determinism eliminates non-deterministic sources (thread races, network delays) by pre-determining order.

**Spanner TrueTime**:
```python
class TrueTime:
    def __init__(self):
        self.uncertainty = 7_000_000  # 7ms in nanoseconds
    
    def now(self):
        """Return interval [earliest, latest]"""
        true_now = time.time_ns()
        return (true_now - self.uncertainty, true_now + self.uncertainty)
    
    def commit_wait(self, start_timestamp):
        """
        Wait until start_timestamp is guaranteed to be in the past
        
        If we assign timestamp t to transaction, must wait until
        t < TT.now().earliest (i.e., t is definitely in past)
        """
        while True:
            earliest, latest = self.now()
            if start_timestamp < earliest:
                break
            time.sleep(0.001)  # Sleep 1ms
```

**Commit Wait**: After assigning timestamp t to transaction, wait until t is guaranteed to be in the past on all servers.

**External Consistency via TrueTime**:
- T1 commits at timestamp t1
- Commit wait ensures t1 < TT.now().earliest when commit returns
- T2 starts after T1 commits, uses timestamp t2 = TT.now().latest
- Therefore: t1 < t2 (external consistency)

### 1.3 Mental Models

**The Deterministic Pipeline**:
```
Inputs: Transaction requests (non-deterministic arrival)
   ↓
Sequencer: Global ordering (consensus)
   ↓
Scheduler: Lock acquisition (deterministic)
   ↓
Execution: Read/write operations (no coordination)
   ↓
Output: Committed transactions (deterministic result)
```

**Tradeoff**: Calvin sacrifices latency (must sequence first) for high throughput (no coordination during execution).

**TrueTime Visualization**: Timestamp uncertainty = physical reality of clock drift. Commit wait "pays" latency to guarantee correctness.

### 1.4 Edge Cases

**Multi-Partition Transactions**: Calvin handles via deterministic locking across partitions (no 2PC).

**Read-Only Transactions in Spanner**: Can execute at latest safe timestamp without commit wait (snapshot isolation).

**Dependent Transactions**: If T2 reads T1's writes, Calvin's deterministic scheduling ensures T1 executes first.

### 1.5 Implementation

**Simplified Calvin Sequencer**:
```python
import threading
import queue
from collections import defaultdict

class CalvinSequencer:
    def __init__(self, num_partitions):
        self.sequence_number = 0
        self.lock = threading.Lock()
        self.transaction_queue = queue.Queue()
    
    def submit_transaction(self, txn):
        """
        Assign global sequence number to transaction
        """
        with self.lock:
            txn.sequence_number = self.sequence_number
            self.sequence_number += 1
        
        # Replicate to all nodes (simplified: just enqueue)
        self.transaction_queue.put(txn)
        return txn.sequence_number

class CalvinScheduler:
    def __init__(self):
        self.locks = defaultdict(threading.Lock)
        self.held_locks = {}
    
    def acquire_locks(self, txn):
        """
        Acquire locks in deterministic order (sorted by key)
        """
        keys = sorted(txn.read_set | txn.write_set)
        acquired = []
        
        for key in keys:
            self.locks[key].acquire()
            acquired.append(key)
        
        self.held_locks[txn.sequence_number] = acquired
    
    def release_locks(self, txn):
        """
        Release all locks held by transaction
        """
        for key in self.held_locks.get(txn.sequence_number, []):
            self.locks[key].release()
        del self.held_locks[txn.sequence_number]

class CalvinExecutor:
    def __init__(self):
        self.storage = {}
    
    def execute(self, txn, scheduler):
        """
        Deterministic execution after locks acquired
        """
        scheduler.acquire_locks(txn)
        
        try:
            # Execute transaction logic
            result = txn.execute(self.storage)
            return result
        finally:
            scheduler.release_locks(txn)

# Example usage
class Transaction:
    def __init__(self, read_set, write_set, logic):
        self.read_set = set(read_set)
        self.write_set = set(write_set)
        self.logic = logic
        self.sequence_number = None
    
    def execute(self, storage):
        return self.logic(storage)

# Test
sequencer = CalvinSequencer(num_partitions=4)
scheduler = CalvinScheduler()
executor = CalvinExecutor()

# Transaction: transfer from account A to B
def transfer_logic(storage):
    balance_a = storage.get('A', 100)
    balance_b = storage.get('B', 50)
    storage['A'] = balance_a - 10
    storage['B'] = balance_b + 10
    return True

txn = Transaction(read_set=['A', 'B'], write_set=['A', 'B'], logic=transfer_logic)
seq_num = sequencer.submit_transaction(txn)
result = executor.execute(txn, scheduler)
print(f"Transaction {seq_num} committed: {result}")
```

**Spanner External Consistency**:
```python
import time

class SpannerTransaction:
    def __init__(self, truetime):
        self.truetime = truetime
        self.start_timestamp = None
        self.commit_timestamp = None
    
    def begin(self):
        """Start transaction, acquire timestamp"""
        earliest, latest = self.truetime.now()
        self.start_timestamp = latest  # Use latest for reads
        print(f"Transaction started at {self.start_timestamp}")
    
    def commit(self):
        """
        Commit with external consistency guarantee
        """
        # Assign commit timestamp
        earliest, latest = self.truetime.now()
        self.commit_timestamp = latest
        
        print(f"Commit timestamp assigned: {self.commit_timestamp}")
        
        # Commit wait: wait until commit_timestamp < TT.now().earliest
        self.truetime.commit_wait(self.commit_timestamp)
        
        print(f"Commit wait completed, transaction committed")
        return self.commit_timestamp

# Test external consistency
tt = TrueTime()

# Transaction 1
txn1 = SpannerTransaction(tt)
txn1.begin()
time.sleep(0.01)  # Simulate work
commit_ts1 = txn1.commit()

# Transaction 2 starts AFTER txn1 commits
txn2 = SpannerTransaction(tt)
txn2.begin()
commit_ts2 = txn2.commit()

# Verify external consistency: commit_ts1 < commit_ts2
assert commit_ts1 < commit_ts2, "External consistency violated!"
print(f"External consistency verified: {commit_ts1} < {commit_ts2}")
```

---

## Phase 2: Conceptual Stress Questions

### Q1: Calvin vs 2PC
**Question**: Why does Calvin achieve higher throughput than traditional 2PC-based distributed databases?

<details>
<summary><strong>Hint</strong></summary>

2PC requires synchronous coordination between coordinator and participants during execution. Calvin pre-sequences transactions, allowing parallel execution without coordination.
</details>

---

### Q2: TrueTime Uncertainty
**Question**: If TrueTime uncertainty increases from 7ms to 14ms, how does this affect Spanner's performance?

<details>
<summary><strong>Hint</strong></summary>

Commit wait duration increases proportionally. Read-only transactions must wait longer for safe snapshots. Write latency and read latency both degraded.
</details>

---

### Q3: Determinism vs Abort Rate
**Question**: Under what workload would Calvin's deterministic execution perform worse than optimistic concurrency control?

<details>
<summary><strong>Hint</strong></summary>

If many transactions have false conflicts (predicted write sets overlap but actual execution wouldn't conflict), Calvin holds locks unnecessarily. Optimistic schemes would detect no conflict and commit.
</details>

---

## Phase 3: Applied Problem

### Problem: Implement Deterministic Scheduler

**Scenario**: Build a simplified Calvin scheduler that handles multi-partition transactions with deterministic lock acquisition.

**Skeleton Code**:
```python
import threading
from collections import defaultdict, deque

class MultiPartitionScheduler:
    def __init__(self, num_partitions):
        self.num_partitions = num_partitions
        self.partition_locks = [threading.Lock() for _ in range(num_partitions)]
        self.pending_txns = deque()
    
    def submit_transaction(self, txn):
        """
        Submit transaction with read/write sets per partition
        
        txn.partitions: set of partition IDs accessed
        """
        # TODO:
        # 1. Add transaction to pending queue
        # 2. Try to schedule next transaction
        pass
    
    def try_schedule_next(self):
        """
        Attempt to schedule next transaction in queue
        Must acquire locks for ALL partitions atomically (deadlock-free)
        """
        # TODO:
        # 1. Peek at head of pending queue
        # 2. Try to acquire locks for all partitions (in sorted order)
        # 3. If successful, remove from queue and execute
        # 4. If failed, wait and retry
        pass
    
    def execute_transaction(self, txn):
        """
        Execute transaction after locks acquired
        """
        try:
            result = txn.execute()
            return result
        finally:
            self.release_locks(txn)
    
    def release_locks(self, txn):
        """Release all partition locks held by transaction"""
        for partition_id in sorted(txn.partitions):
            self.partition_locks[partition_id].release()

# Test case
class TestTransaction:
    def __init__(self, txn_id, partitions, logic):
        self.txn_id = txn_id
        self.partitions = set(partitions)
        self.logic = logic
    
    def execute(self):
        print(f"Executing transaction {self.txn_id}")
        return self.logic()

scheduler = MultiPartitionScheduler(num_partitions=4)

# Transaction 1: partitions {0, 1}
txn1 = TestTransaction(1, [0, 1], lambda: "T1 result")

# Transaction 2: partitions {1, 2} - conflicts with T1 on partition 1
txn2 = TestTransaction(2, [1, 2], lambda: "T2 result")

# Submit in order (Calvin guarantees T1 →  T2)
scheduler.submit_transaction(txn1)
scheduler.submit_transaction(txn2)
```

**Expected Approach**:
1. Implement FIFO queue with deterministic lock ordering
2. Acquire locks in sorted partition order (prevents deadlock)
3. Execute transactions serially in submission order
4. Verify T1 completes before T2 starts

---

## Phase 4: Self-Assessment

### Checklist
- [ ] Understand deterministic execution model
- [ ] Can explain Calvin's three-layer architecture
- [ ] Know how TrueTime enables external consistency
- [ ] Can implement commit wait protocol
- [ ] Understand tradeoffs: latency vs throughput vs consistency

### Reflection Questions
1. Why is determinism beneficial for distributed databases?
2. Could Calvin work without TrueTime? What would be lost?
3. How do NewSQL systems compare to eventual consistency (NoSQL)?

### Next Steps
- **Deepen**: Study Spanner's implementation details, geographic replication
- **Connect**: Relate to state machine replication, Paxos/Raft consensus
- **Apply**: Design deterministic database for specific workload (e.g., financial transactions)

**Related Sessions**:
- ← [Session 25: PAC Learning](Session_25_PAC_Learning.md)
- → [Session 27: RDMA Networking](Session_27_RDMA_Networking.md)

---

*Session 26 of Cycle 4 • Expert Mastery*
