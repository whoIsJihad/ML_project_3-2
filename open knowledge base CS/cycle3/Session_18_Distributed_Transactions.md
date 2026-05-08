# Session 18 – Distributed Transactions & 2PC/3PC

## Linked Domain
[[Databases & Concurrency]]

**Cycle**: 3 (Advanced Integration)  
**Difficulty**: ⚫⚫⚫⚪

---

## Phase 1: Theoretical Foundation

### Definitions

**Distributed Transaction**: A transaction spanning multiple nodes/shards that must commit or abort atomically.

**Two-Phase Commit (2PC)**: Coordinator sends PREPARE, waits for votes, then sends COMMIT/ABORT. Blocking protocol (coordinator failure blocks participants).

**Three-Phase Commit (3PC)**: Adds PRE-COMMIT phase between PREPARE and COMMIT, reducing blocking window.

**ACID in Distributed Settings**:
- **Atomicity**: All-or-nothing across nodes
- **Consistency**: Application-level invariants preserved
- **Isolation**: MVCC or 2PL distributed
- **Durability**: WAL on all participants

### Core Mechanism: Two-Phase Commit

**Phase 1: PREPARE**
```
Coordinator → Participants: PREPARE(txn_id)
Participants:
  - Write undo/redo log to disk
  - Acquire locks
  - Vote YES or NO
Participants → Coordinator: VOTE
```

**Phase 2: COMMIT/ABORT**
```
If all votes YES:
  Coordinator → Participants: COMMIT
  Participants commit and release locks
Else:
  Coordinator → Participants: ABORT
  Participants rollback and release locks
```

**Failure Handling**:
- Participant fails during Phase 1 → timeout → ABORT
- Coordinator fails after Phase 1 → Participants BLOCKED (don't know outcome)
- Participant fails during Phase 2 → retry COMMIT message

### Core Mechanism: Three-Phase Commit

**Phases**:
1. **CAN-COMMIT**: Coordinator asks if participants can commit
2. **PRE-COMMIT**: If all agree, coordinator sends PRE-COMMIT (participants know commit is coming)
3. **DO-COMMIT**: Final commit

**Non-Blocking Property**: If coordinator fails, participants can elect new coordinator and complete protocol (because PRE-COMMIT means all participants agreed).

**Limitation**: Requires synchronized clocks or perfect failure detection. Network partitions can violate safety.

### Mental Model

**2PC = Marriage Proposal**: Proposer (coordinator) asks "Will you marry me?" (PREPARE). If both say yes, proceeding ring (COMMIT). If one says no or doesn't respond, wedding off (ABORT). Problem: If proposer disappears after hearing "yes" but before saying "I do," everyone's stuck waiting.

**3PC = Adding Engagement**: Engagement phase (PRE-COMMIT) means "we're definitely getting married." If proposer vanishes, others can proceed without them.

### Edge Cases

**1. Coordinator Failure in 2PC**
```
Coordinator sends PREPARE
All participants vote YES and wait
Coordinator crashes
Participants are BLOCKED (can't commit or abort without knowing coordinator's decision)
```
**Recovery**: Participants must wait for coordinator recovery or timeout and abort (losing work).

**2. Network Partition in 3PC**
```
Partition 1: {Coordinator, P1}
Partition 2: {P2, P3}

Coordinator sends PRE-COMMIT to P1
Partition occurs
P2, P3 timeout, elect new coordinator, abort
P1 receives DO-COMMIT from old coordinator and commits
INCONSISTENCY!
```

**3. Cascading Aborts**
Transaction T1 (distributed) aborts
All reads of T1's uncommitted data must also abort
Expensive in distributed setting

### Common Mistakes

1. **Forgetting to Log Before Voting**: Participant votes YES but crashes before logging—can't recover state.

2. **Not Handling Timeouts**: Infinite wait for coordinator response → resource leakage.

3. **Assuming 3PC is Perfect**: Requires perfect failure detection (impossible in asynchronous networks).

### Code

```python
import time
import threading
from enum import Enum

class TxnState(Enum):
    INIT = 1
    PREPARED = 2
    COMMITTED = 3
    ABORTED = 4

class Participant:
    def __init__(self, id):
        self.id = id
        self.state = TxnState.INIT
        self.log = []
    
    def prepare(self, txn_id):
        """Phase 1: Vote YES or NO"""
        # Simulate logging and lock acquisition
        self.log.append(f"PREPARE {txn_id}")
        self.state = TxnState.PREPARED
        # In real system: write WAL, acquire locks
        return "YES"  # or "NO" if can't prepare
    
    def commit(self, txn_id):
        """Phase 2: Commit transaction"""
        if self.state == TxnState.PREPARED:
            self.log.append(f"COMMIT {txn_id}")
            self.state = TxnState.COMMITTED
            # Release locks
            return "ACK"
        return "ERROR"
    
    def abort(self, txn_id):
        """Phase 2: Abort transaction"""
        self.log.append(f"ABORT {txn_id}")
        self.state = TxnState.ABORTED
        # Rollback, release locks
        return "ACK"

class Coordinator:
    def __init__(self, participants):
        self.participants = participants
        self.txn_id = 0
    
    def run_2pc(self):
        """Execute 2PC protocol"""
        self.txn_id += 1
        txn = self.txn_id
        
        # Phase 1: PREPARE
        print(f"[2PC] Phase 1: PREPARE txn {txn}")
        votes = []
        for p in self.participants:
            vote = p.prepare(txn)
            votes.append(vote)
            print(f"  Participant {p.id} voted: {vote}")
        
        # Phase 2: COMMIT or ABORT
        if all(v == "YES" for v in votes):
            print(f"[2PC] Phase 2: COMMIT txn {txn}")
            for p in self.participants:
                ack = p.commit(txn)
                print(f"  Participant {p.id}: {ack}")
            return "COMMITTED"
        else:
            print(f"[2PC] Phase 2: ABORT txn {txn}")
            for p in self.participants:
                ack = p.abort(txn)
                print(f"  Participant {p.id}: {ack}")
            return "ABORTED"

# Example
participants = [Participant(i) for i in range(3)]
coordinator = Coordinator(participants)
result = coordinator.run_2pc()
print(f"Transaction result: {result}")
```

---

## Phase 2: Stress Questions

### Q1: 2PC Blocking Proof
**Prove that 2PC is blocking: construct scenario where participants cannot make progress without coordinator.**

<details><summary>Hint</summary>
Coordinator sends PREPARE, all vote YES, coordinator crashes. Participants in PREPARED state can't unilaterally commit or abort (others might have voted NO).
</details>

### Q2: 3PC Partition Scenario
**Show that 3PC can violate consistency under network partition despite being non-blocking.**

<details><summary>Hint</summary>
Partition after PRE-COMMIT sent to subset. Minority elects new coordinator and aborts, majority commits. Both sides think they're correct!
</details>

### Q3: Spanner TrueTime
**Google Spanner uses TrueTime (GPS+atomic clocks) to provide external consistency without 2PC for read-only transactions. Explain how.**

<details><summary>Hint</summary>
TrueTime provides [earliest, latest] bound on current time. Transactions use commit timestamp with wait period to ensure external consistency: if T1 commits before T2 starts, T1's timestamp < T2's.
</details>

---

## Phase 3: Applied Problem

Design a distributed order processing system:
- Inventory service (deduct stock)
- Payment service (charge card)
- Shipping service (book pickup)

**Part A**: Implement 2PC coordinator with timeout handling.

**Part B**: Add compensation-based saga pattern (alternative to 2PC).

**Part C**: Compare latency, availability, consistency guarantees.

```python
class OrderCoordinator:
    def __init__(self, inventory_svc, payment_svc, shipping_svc):
        self.services = [inventory_svc, payment_svc, shipping_svc]
    
    def process_order_2pc(self, order):
        """Use 2PC for atomicity"""
        # TODO: Implement
        pass
    
    def process_order_saga(self, order):
        """Use SAGA pattern with compensation"""
        # TODO: Implement
        # If payment fails, compensate inventory (add stock back)
        pass
```

---

## Phase 4: Self-Assessment

### Checklist
- [ ] Understand 2PC phases and blocking issue
- [ ] Know 3PC and its limitations
- [ ] Understand CAP theorem implications
- [ ] Can design compensating transactions (SAGAs)

### Next Steps
- **Strong**: [[Session 19 – Byzantine Fault Tolerance]]
- **Struggling**: Review [[Session 04 – Databases & Concurrency]]
- **Resources**: "Designing Data-Intensive Applications" Ch. 7, 9

---

**Navigation**: ← [[Session 17]] | **Index**: [[cycle3/INDEX]] | → [[Session 19]]
