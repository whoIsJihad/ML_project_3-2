# Session 11 – Serializability & MVCC Implementation

## Linked Domain
[[Databases & Concurrency]]

**Cycle**: 2 (Intermediate Depth)  
**Difficulty**: ⚫⚫⚪⚪

---

## Phase 1: Theoretical Foundation

### Definitions

**Snapshot Isolation (SI)**: A multiversion concurrency control scheme where each transaction reads from a consistent snapshot of the database taken at its start time. Writes are buffered until commit, when they're checked for conflicts.

**Write Skew**: A non-serializable anomaly where two concurrent transactions read overlapping data and make disjoint updates that violate an integrity constraint when combined.

**Multi-Version Concurrency Control (MVCC)**: A concurrency control method that maintains multiple physical versions of each object, allowing readers and writers to proceed without blocking each other.

**Serializable Snapshot Isolation (SSI)**: An enhancement of SI that detects dangerous structures (rw-antidependency cycles) and aborts transactions to guarantee serializability.

### Core Mechanism: PostgreSQL MVCC Architecture

**1. Tuple Versioning**
```
Tuple Header:
- xmin: transaction ID that created this version
- xmax: transaction ID that deleted/updated this version (0 if live)
- ctid: physical location (page, offset)
- infomask: flags (committed, aborted, frozen)
```

**Version Visibility Rules** (for transaction T with snapshot S):
1. **Created After Snapshot**: If `xmin > S.xmax` → invisible
2. **Deleted Before Snapshot**: If `xmax < S.xmin AND xmax committed` → invisible  
3. **Created By Active Transaction**: If `xmin in S.active_list` → invisible (unless xmin == T.id)
4. **Otherwise**: visible if `xmin committed AND (xmax == 0 OR xmax not committed OR xmax > S.xmax)`

**2. Write Skew Detection in SSI**

PostgreSQL SSI tracks two conflict types:
- **rw-conflicts (read-write)**: T1 reads X, T2 writes X, T2 commits before T1
- **wr-conflicts (write-read)**: T1 writes X, T2 reads old version of X

A **dangerous structure** occurs when there exists a cycle: `T1 -rw-> T2 -rw-> T3 -..-> T1`

**Algorithm**:
```
On Read(X):
  - Record in SIREAD lock table
  
On Write(X):
  - Check for readers of X → create rw-conflicts
  
On Commit:
  - Check for cycles involving this transaction
  - If cycle detected → abort this or another transaction in cycle
```

### Mental Model

**MVCC as Time Travel**: Think of the database as a 4D structure (3D space + time). Each transaction sees a "slice" of this 4D structure at a fixed time (its snapshot). Writes create new versions in the future timeline. Vacuum is garbage collection of versions no transaction can see anymore.

**SI vs Serializability**: SI prevents "lost updates" and "dirty reads" but allows write skew because it only checks for direct write-write conflicts, not the semantic constraint violations that emerge from disjoint updates.

### Edge Cases & Anomalies

**1. Write Skew Example**
```sql
-- Constraint: At least one doctor must be on call
-- Initially: doctors table has: (Alice, true), (Bob, true)

-- Transaction T1:
SELECT COUNT(*) FROM doctors WHERE on_call = true;  -- sees 2
-- Decides to go off call since count > 1
UPDATE doctors SET on_call = false WHERE name = 'Alice';

-- Transaction T2 (concurrent):
SELECT COUNT(*) FROM doctors WHERE on_call = true;  -- sees 2
UPDATE doctors SET on_call = false WHERE name = 'Bob';

-- Both commit → constraint violated! (both now false)
```

**2. Serialization Anomaly Graph**
```
T1: R(X) R(Y) W(Y)
T2:      R(Y) W(Z)
T3: R(Z)      W(X)

Cycle: T1 -rw-> T2 -rw-> T3 -rw-> T1
```

**3. Vacuum Performance Degradation**
- High update rate → many dead tuples → vacuum can't keep up
- Long-running transactions prevent vacuum from cleaning old versions
- Index bloat: dead tuples in heap still referenced by indexes

### Common Mistakes

1. **Assuming SI = Serializability**: SI does NOT prevent all anomalies (write skew, read-only transaction anomalies).

2. **Ignoring Vacuum Tuning**: Default vacuum settings insufficient for high-write workloads. Need aggressive `autovacuum_vacuum_scale_factor`.

3. **Not Handling Serialization Failures**: SSI can abort transactions with `40001` error code. Application must retry.

4. **Transaction ID Wraparound**: XIDs are 32-bit. After 2 billion transactions, need aggressive vacuum to avoid database shutdown.

### Implementation Code

```python
class MVCCTuple:
    def __init__(self, data, xmin, xmax=0):
        self.data = data
        self.xmin = xmin  # creating transaction ID
        self.xmax = xmax  # deleting transaction ID (0 if live)
        self.committed = False
        
class Snapshot:
    def __init__(self, xmin, xmax, active_list):
        self.xmin = xmin  # oldest active transaction
        self.xmax = xmax  # next transaction ID to assign
        self.active_list = active_list  # transactions active at snapshot time
        
class MVCCDatabase:
    def __init__(self):
        self.data = {}  # key -> list of tuple versions
        self.current_xid = 1
        self.committed_xids = set()
        
    def begin_transaction(self):
        xid = self.current_xid
        self.current_xid += 1
        active = [x for x in range(self.xmin_active(), xid) 
                  if x not in self.committed_xids]
        return xid, Snapshot(min(active) if active else xid, xid, active)
    
    def is_visible(self, tuple, snapshot, my_xid):
        """Version visibility check"""
        # Created after snapshot
        if tuple.xmin >= snapshot.xmax:
            return False
            
        # Created by active transaction (not me)
        if tuple.xmin in snapshot.active_list and tuple.xmin != my_xid:
            return False
            
        # Created by uncommitted transaction
        if tuple.xmin not in self.committed_xids and tuple.xmin != my_xid:
            return False
            
        # Deleted by committed transaction before snapshot
        if tuple.xmax > 0:
            if tuple.xmax < snapshot.xmin and tuple.xmax in self.committed_xids:
                return False
            if tuple.xmax in self.committed_xids and tuple.xmax < snapshot.xmax:
                return False
                
        return True
    
    def read(self, key, xid, snapshot):
        """Read visible version"""
        if key not in self.data:
            return None
        for tuple in reversed(self.data[key]):  # newest first
            if self.is_visible(tuple, snapshot, xid):
                return tuple.data
        return None
    
    def write(self, key, value, xid):
        """Create new version"""
        if key in self.data:
            # Mark latest version as deleted by this transaction
            latest = self.data[key][-1]
            if latest.xmax == 0:
                latest.xmax = xid
        else:
            self.data[key] = []
        self.data[key].append(MVCCTuple(value, xid))
    
    def commit(self, xid):
        """Commit transaction"""
        self.committed_xids.add(xid)
        # Mark all tuples created by this transaction as committed
        for versions in self.data.values():
            for tuple in versions:
                if tuple.xmin == xid:
                    tuple.committed = True
    
    def vacuum(self):
        """Remove dead tuples"""
        oldest_active = self.xmin_active()
        for key in list(self.data.keys()):
            # Keep only versions visible to oldest active transaction
            visible = []
            for tuple in self.data[key]:
                if tuple.xmax == 0 or tuple.xmax >= oldest_active:
                    visible.append(tuple)
            self.data[key] = visible
            if not visible:
                del self.data[key]
    
    def xmin_active(self):
        """Find oldest active transaction"""
        active = [x for x in range(1, self.current_xid) 
                  if x not in self.committed_xids]
        return min(active) if active else self.current_xid

# Example: Write Skew
db = MVCCDatabase()
db.write('alice', True, 0)
db.write('bob', True, 0)
db.commit(0)

# Transaction 1
xid1, snap1 = db.begin_transaction()
alice_val = db.read('alice', xid1, snap1)
bob_val = db.read('bob', xid1, snap1)
count = (alice_val + bob_val)  # sees 2
if count > 1:
    db.write('alice', False, xid1)
    
# Transaction 2 (concurrent)
xid2, snap2 = db.begin_transaction()
alice_val = db.read('alice', xid2, snap2)
bob_val = db.read('bob', xid2, snap2)
count = (alice_val + bob_val)  # also sees 2
if count > 1:
    db.write('bob', False, xid2)
    
db.commit(xid1)
db.commit(xid2)

# Constraint violated: both alice and bob are now False
```

---

## Phase 2: Stress Questions

### Question 1: Write Skew Construction
**Prove that Snapshot Isolation is NOT serializable by constructing a write skew example with three transactions.**

<details>
<summary>Hint</summary>
Consider a "meeting room scheduling" scenario where constraint is "at most 2 meetings at noon". Three transactions each read the count (sees ≤ 2) and each adds a meeting.
</details>

---

### Question 2: Vacuum Analysis
**A PostgreSQL table has 1M rows with 10% updated per minute. Vacuum runs every 1 minute and takes 30 seconds. Analyze:**
- **a)** How many dead tuples accumulate?
- **b)** When does vacuum fall behind?
- **c)** What happens when a transaction starts and runs for 10 minutes?

<details>
<summary>Hint</summary>
Dead tuples = update_rate × time_since_vacuum. Vacuum falls behind when dead tuple creation rate > removal rate. Long transaction prevents vacuum from removing versions needed by that transaction.
</details>

---

### Question 3: SSI Conflict Detection Design
**Design a space-efficient SSI implementation that tracks rw-dependencies and detects cycles. For N concurrent transactions with M shared objects, analyze space complexity.**

<details>
<summary>Hint</summary>
Use SIREAD lock table (object → readers set) and conflict graph (adjacency list). Space = O(M × avg_readers + N²) for conflicts. Optimize by summarizing old transactions into "pivot" nodes.
</details>

---

## Phase 3: Applied Problem

### Problem: E-Commerce Inventory System with SSI

You're building an inventory system for an e-commerce platform. The requirements:
- Multiple concurrent transactions reserve items
- Each item has a quantity available
- Business rule: "No overselling" (reserved quantity ≤ available quantity)
- Must handle 10,000 concurrent transactions

**Part A: Write Skew Vulnerability**
Show how pure Snapshot Isolation can violate the overselling constraint with two concurrent transactions.

**Part B: SSI Implementation**
Implement a simplified SSI detector that:
1. Tracks SIREAD locks per item
2. Detects rw-conflicts when a reservation is made
3. Aborts transactions when a dangerous structure is detected

**Part C: Performance Analysis**
Given:
- 100,000 items
- Zipf distribution (20% of items account for 80% of traffic)
- Average transaction touches 3 items

Analyze:
- SIREAD lock table size
- False positive abort rate
- Comparison with 2PL (two-phase locking) throughput

```python
# Skeleton Code
class Item:
    def __init__(self, id, quantity):
        self.id = id
        self.quantity = quantity
        self.reserved = 0
        
class SSIDatabase:
    def __init__(self):
        self.items = {}
        self.siread_locks = {}  # item_id -> set of transaction IDs
        self.rw_conflicts = []  # list of (reader_xid, writer_xid, item_id)
        self.current_xid = 1
        
    def reserve_item(self, item_id, qty, xid):
        """
        Reserve qty of item_id for transaction xid.
        Must detect conflicts and return success/abort decision.
        """
        # TODO: Implement SSI logic
        pass
    
    def detect_cycle(self, xid):
        """
        Build conflict graph and detect if xid is part of a cycle.
        """
        # TODO: Implement cycle detection
        pass
```

**Expected Output Format**:
```
Part A: Write skew scenario with timeline
Part B: Complete SSI implementation with cycle detection
Part C: 
  - Lock table size: O(...)
  - Abort rate analysis with Zipf distribution
  - Throughput comparison: SSI vs 2PL
```

---

## Phase 4: Self-Assessment & Feedback

### Mastery Checklist
Rate your understanding (1-5):
- [ ] Can explain MVCC tuple versioning and visibility rules
- [ ] Can construct write skew examples and explain why SI ≠ Serializability  
- [ ] Understand PostgreSQL vacuum mechanics and tuning
- [ ] Can design SSI conflict detection and cycle detection
- [ ] Understand trade-offs: MVCC vs 2PL, SI vs SSI

### Reflection Questions
1. **What surprised you** about MVCC implementation details?
2. **Where did you struggle** in the applied problem?
3. **How would you explain** write skew to a colleague who only understands 2PL?

### Mistake Log
Record your mistakes:
- **Conceptual errors**: (e.g., "thought SI prevented write skew")
- **Implementation bugs**: (e.g., "forgot to check committed status")
- **Performance misunderstandings**: (e.g., "didn't realize vacuum impact")

### Next Steps
- **If comfortable**: Proceed to [[Session 12 – Consensus Algorithms]]
- **If struggling**: Review [[Session 04 – Databases & Concurrency]] basics
- **Deep dive resources**: 
  - "A Critique of ANSI SQL Isolation Levels" (Berenson et al.)
  - PostgreSQL MVCC documentation
  - "Serializable Snapshot Isolation in PostgreSQL" (Ports & Grittner)

---

**Navigation**: ← [[Session 10]] | **Index**: [[cycle2/INDEX]] | → [[Session 12]]
