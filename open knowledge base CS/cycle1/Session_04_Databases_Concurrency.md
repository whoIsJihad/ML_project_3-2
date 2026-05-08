# Session 4 – Transaction Isolation & Anomalies

## Linked Domain
[[Databases & Concurrency]]

---

## Phase 1 – Clean Theory

### 1. Fundamental Concepts

**Transaction**: Sequence of read/write operations appearing atomic and isolated.
$$T = \langle r_1(x), w_1(y), \ldots \rangle$$

**Schedule**: Interleaving of operations from multiple transactions.
$$S = \langle o_1, o_2, \ldots, o_n \rangle$$

**Conflict**: Operations $o_i, o_j$ from different transactions conflict if:
- Same object accessed
- At least one is a write

---

### 2. Serializability

| Type | Definition | Complexity |
|------|------------|------------|
| **Conflict Serializability** | Conflict-equivalent to serial schedule | Polynomial (precedence graph) |
| **View Serializability** | View-equivalent to serial schedule | NP-complete |

**Precedence Graph**:
- Nodes: Transactions
- Edge $T_i \to T_j$: $T_i$ has conflicting operation before $T_j$
- **Theorem**: Schedule is conflict-serializable iff graph is acyclic

---

### 3. Concurrency Control Protocols

**Two-Phase Locking (2PL)**:
- **Growing phase**: Acquire locks, cannot release
- **Shrinking phase**: Release locks, cannot acquire
- **Theorem**: All 2PL schedules are conflict-serializable
- **Limitation**: Deadlocks possible

**Multi-Version Concurrency Control (MVCC)**:
- Maintain versions: $(x_1, t_1), (x_2, t_2), \ldots$
- Read at timestamp $t$ sees version with largest $t' \leq t$
- Writes create new versions
- Reads never block; writes never block reads

---

### 4. SQL Isolation Levels

| Level | Dirty Read | Non-repeatable Read | Phantom Read | Write Skew |
|-------|------------|---------------------|--------------|------------|
| Read Uncommitted | Possible | Possible | Possible | Possible |
| Read Committed | Prevented | Possible | Possible | Possible |
| Repeatable Read | Prevented | Prevented | Possible | Possible |
| Serializable | Prevented | Prevented | Prevented | Prevented |

**Note**: Most databases default to Read Committed or Repeatable Read, NOT Serializable.

---

### 5. Isolation Anomalies

| Anomaly | Description | Prevention |
|---------|-------------|------------|
| **Dirty Read** | Read uncommitted write | Read Committed+ |
| **Non-repeatable Read** | Same read returns different values | Repeatable Read+ |
| **Phantom Read** | Range query returns different rows | Serializable |
| **Write Skew** | Overlapping reads, disjoint writes violate constraint | Serializable |
| **Lost Update** | Concurrent writes overwrite each other | SELECT FOR UPDATE |

---

### 6. Edge Cases

1. **Write Skew under Snapshot Isolation**:
   - Constraint: at least one doctor on-call
   - Both read "two on-call", both go off-call
   - SI allows both commits; constraint violated

2. **Predicate Locks**: Standard row locks cannot prevent phantoms on range queries. Requires predicate locking or index-range locks.

3. **Lost Update**: Even under Repeatable Read, non-atomic read-modify-write can lose updates.

4. **Distributed 2PL**: Requires distributed deadlock detection; MVCC requires clock synchronization.

5. **Long-Running Transactions**: MVCC version bloat—old versions retained until transaction completes.

---

### Common Mistakes

1. **Repeatable Read ≠ Serializable**: Repeatable Read prevents non-repeatable reads but allows phantoms and write skew.

2. **Assuming default is Serializable**: Most databases default to Read Committed. Must explicitly set isolation level.

3. **Missing SELECT FOR UPDATE**: Without explicit locks, lost updates occur even under high isolation.

4. **MVCC misconceptions**: Snapshot Isolation (common MVCC variant) allows write skew. Need Serializable Snapshot Isolation (SSI) for true serializability.

5. **Deadlock denial**: Lock ordering in application code doesn't prevent deadlocks from index locks, foreign key checks, etc.

---

### Code Snippet – Write Skew Demonstration

```python
import psycopg2
import threading
import time

def write_skew_test(isolation_level, level_name):
    """Demonstrate write skew under different isolation levels."""

    conn1 = psycopg2.connect("dbname=test user=postgres")
    conn2 = psycopg2.connect("dbname=test user=postgres")

    # Setup
    cur = conn1.cursor()
    cur.execute("DROP TABLE IF EXISTS accounts")
    cur.execute("""
        CREATE TABLE accounts (id INT PRIMARY KEY, balance INT CHECK (balance >= 0))
    """)
    cur.execute("INSERT INTO accounts VALUES (1, 100), (2, 100)")
    conn1.commit()

    conn1.set_isolation_level(isolation_level)
    conn2.set_isolation_level(isolation_level)

    def transaction1():
        cur = conn1.cursor()
        cur.execute("BEGIN")
        cur.execute("SELECT SUM(balance) FROM accounts")
        total = cur.fetchone()[0]
        print(f"T1 ({level_name}): total = {total}")
        time.sleep(1)
        if total >= 100:
            cur.execute("UPDATE accounts SET balance = balance - 50 WHERE id = 1")
            print("T1: withdrew 50 from account 1")
        conn1.commit()
        print("T1: committed")

    def transaction2():
        time.sleep(0.5)
        cur = conn2.cursor()
        cur.execute("BEGIN")
        cur.execute("SELECT SUM(balance) FROM accounts")
        total = cur.fetchone()[0]
        print(f"T2 ({level_name}): total = {total}")
        time.sleep(1)
        if total >= 100:
            cur.execute("UPDATE accounts SET balance = balance - 50 WHERE id = 2")
            print("T2: withdrew 50 from account 2")
        try:
            conn2.commit()
            print("T2: committed")
        except Exception as e:
            print(f"T2: failed - {e}")
            conn2.rollback()

    t1 = threading.Thread(target=transaction1)
    t2 = threading.Thread(target=transaction2)
    t1.start(); t2.start()
    t1.join(); t2.join()

    cur = conn1.cursor()
    cur.execute("SELECT * FROM accounts")
    print(f"Final state: {cur.fetchall()}\n")

    conn1.close()
    conn2.close()

# Usage:
# write_skew_test(psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ, "RR")
# write_skew_test(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE, "Serializable")
```

---

## Phase 2 – Conceptual Stress Questions

**Q1**: Analyze this schedule:
```
T1: r1(x)  w1(x)           r1(y)     w1(y)
T2:            r2(y)  w2(y)     r2(x)     w2(x)
```
Draw the precedence graph. Is it conflict-serializable? If yes, give equivalent serial schedule. If no, what anomaly occurs? Suppose both implement `x += y; y += x`. What are possible final values of $(x, y)$ starting from $(1, 1)$?

**Q2**: Reservation system under **Snapshot Isolation**:
```sql
BEGIN;
SELECT COUNT(*) FROM seats WHERE reserved = false;  -- Both see 1 free
UPDATE seats SET reserved = true WHERE id = ? AND reserved = false;
COMMIT;
```
Both transactions see 1 free seat and try to reserve. What happens? Does either abort? How do you fix without changing isolation level?

**Q3**: Prove every 2PL schedule is conflict-serializable by showing: (a) 2PL prevents incorrect reordering of conflicting operations, (b) precedence graph from lock acquisition is acyclic. Construct a conflict-serializable schedule NOT allowed by 2PL.

---

## Phase 3 – Applied Problem

**Problem Statement**:

Design a **banking system** supporting:
- `Transfer(from, to, amount)`: Move money between accounts
- `Get_balance(account)`: Read balance
- **Invariant**: Total money conserved

**Part A**: Under **Snapshot Isolation**, show a schedule where two concurrent transfers momentarily violate conservation. Be explicit about operations and timestamps.

**Part B**: Under **Serializable** isolation, analyze deadlock probability. Model: transactions acquire locks in account ID order. Two concurrent transfers: $T_1: (A \to B)$ and $T_2: (B \to A)$. What is deadlock probability as function of accounts $n$ and transaction rate $\lambda$?

**Part C**: System has 1M transactions/second. Serializable causes 20% throughput loss from aborts/retries. Design **optimistic concurrency control** at application level that:
- Detects lost updates using version numbers/timestamps
- Guarantees correctness for transfers
- Analyze performance trade-off vs database serializability

---

## Phase 4 – Feedback & Weakness Log Update

**Awaiting your responses to Phase 2 and Phase 3.**

Critique will focus on:
- Precision in defining schedules and conflicts
- Isolation level subtleties (SI vs Serializable)
- Quantitative deadlock analysis
- System design trade-offs

---

## Cross-Links for Reinforcement
- [[Two-Phase Commit Protocol]]
- [[MVCC Implementation Details]]
- [[Deadlock Detection & Prevention]]
- [[Optimistic Concurrency Control]]
- [[Snapshot Isolation Anomalies]]
- [[Linearizability vs Serializability]]

---

**Status**: Awaiting Phase 2 & 3 responses.
