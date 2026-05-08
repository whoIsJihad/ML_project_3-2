# Session 19 – Byzantine Fault Tolerance & PBFT

## Linked Domain
[[Networks & Distributed Systems]]

**Cycle**: 3 (Advanced Integration)  
**Difficulty**: ⚫⚫⚫⚪

---

## Phase 1: Theoretical Foundation

### Definitions

**Byzantine Failure**: Arbitrary failure where node may behave maliciously (send conflicting messages, lie about state, collude with other faulty nodes).

**Byzantine Fault Tolerance (BFT)**: Ability of system to reach consensus despite up to f Byzantine nodes out of n total nodes.

**Byzantine Generals Problem**: n generals must agree on attack/retreat. Up to f are traitors. Can solve iff n ≥ 3f + 1.

**PBFT (Practical Byzantine Fault Tolerance)**: BFT consensus algorithm with O(n²) message complexity, tolerates f < n/3 failures.

### Core Mechanism: PBFT Protocol

**Phases**:
1. **Request**: Client sends request to primary (leader)
2. **Pre-Prepare**: Primary broadcasts ⟨PRE-PREPARE, v, n, m⟩ (view v, sequence number n, message m)
3. **Prepare**: Replicas broadcast ⟨PREPARE, v, n, d⟩ (d = digest of m)
4. **Commit**: After receiving 2f PREPAREs, replica broadcasts ⟨COMMIT, v, n, d⟩
5. **Reply**: After receiving 2f+1 COMMITs, execute and reply to client

**Safety Invariant**: If replica executes request with sequence n, no other replica executes different request with same n (even if f replicas are Byzantine).

**Quorum Intersection**: Any two quorums of size 2f+1 in system of 3f+1 nodes intersect in at least f+1 nodes. Since at most f are faulty, intersection contains ≥1 honest node.

### Core Mechanism: View Change (Leader Replacement)

When primary suspected faulty (timeout or equivocation):
1. Replica broadcasts ⟨VIEW-CHANGE, v+1, ...⟩
2. After receiving 2f VIEW-CHANGE messages, new primary elected
3. New primary broadcasts ⟨NEW-VIEW, v+1, ...⟩ with proof

Ensures liveness even if primary is Byzantine.

### Mental Model

**Byzantine Generals = Spy Movie**: n spies must agree on mission time. Up to f are double agents. Each spy must verify messages by getting 2f+1 confirmations (quorum). Even if f spies lie, the 2f+1 quorum contains at least f+1 honest spies, guaranteeing truth.

**3f+1 Rule = Redundancy for Lies**: Need 3f+1 total to handle:
- f might be faulty (useless)
- f might disagree honestly (split vote)
- f+1 remaining to form honest majority

### Edge Cases

**1. Primary Equivocation**
```
Byzantine primary sends:
  - PRE-PREPARE(n=1, "A") to replicas {R1, R2}
  - PRE-PREPARE(n=1, "B") to replicas {R3, R4}

Replicas detect conflicting PRE-PREPAREs with same (v, n)
Trigger view change
```

**2. Network Partition with Byzantine Node**
```
Partition: {Primary, 2f nodes} | {f+1 nodes}
Byzantine primary only sends to first partition
First partition commits (has 2f+1 votes)
Second partition times out, starts view change
When healed: second partition adopts committed value
```

**3. Sybil Attack**
Single entity creates fake identities
If adversary controls > f nodes → protocol breaks
**Defense**: Proof-of-work (Bitcoin), proof-of-stake (Ethereum), or permissioned membership

### Common Mistakes

1. **Forgetting Signatures**: Messages must be signed to prevent forgery.

2. **Insufficient Replicas**: n = 2f cannot tolerate f Byzantine failures. Need n ≥ 3f+1.

3. **Weak Timeout Logic**: Byzantine nodes can delay messages to cause view changes. Need adaptive timeouts.

### Code

```python
import hashlib
from collections import defaultdict

class PBFTReplica:
    def __init__(self, id, n_replicas, f):
        self.id = id
        self.n = n_replicas
        self.f = f  # max Byzantine failures
        self.view = 0
        self.sequence = 0
        self.log = []
        
        # Message buffers
        self.pre_prepare_msgs = {}
        self.prepare_msgs = defaultdict(list)
        self.commit_msgs = defaultdict(list)
    
    def is_primary(self):
        return self.id == self.view % self.n
    
    def hash_message(self, msg):
        return hashlib.sha256(msg.encode()).hexdigest()[:16]
    
    def receive_request(self, client_req):
        """Client request received"""
        if not self.is_primary():
            return None  # Forward to primary
        
        self.sequence += 1
        seq = self.sequence
        digest = self.hash_message(client_req)
        
        # Broadcast PRE-PREPARE
        pre_prepare = {
            'type': 'PRE-PREPARE',
            'view': self.view,
            'seq': seq,
            'digest': digest,
            'msg': client_req
        }
        self.pre_prepare_msgs[seq] = pre_prepare
        return pre_prepare
    
    def receive_pre_prepare(self, pp):
        """Replica receives PRE-PREPARE from primary"""
        v, n, d = pp['view'], pp['seq'], pp['digest']
        
        # Verify: correct view, in sequence, digest matches
        if v != self.view:
            return None
        if self.hash_message(pp['msg']) != d:
            return None  # Digest mismatch → Byzantine primary
        
        self.pre_prepare_msgs[n] = pp
        
        # Broadcast PREPARE
        prepare = {
            'type': 'PREPARE',
            'view': v,
            'seq': n,
            'digest': d,
            'replica_id': self.id
        }
        return prepare
    
    def receive_prepare(self, prep):
        """Receive PREPARE from other replica"""
        key = (prep['view'], prep['seq'], prep['digest'])
        self.prepare_msgs[key].append(prep)
        
        # Check if prepared (2f PREPAREs received)
        if len(self.prepare_msgs[key]) >= 2 * self.f:
            # Broadcast COMMIT
            commit = {
                'type': 'COMMIT',
                'view': prep['view'],
                'seq': prep['seq'],
                'digest': prep['digest'],
                'replica_id': self.id
            }
            return commit
        return None
    
    def receive_commit(self, comm):
        """Receive COMMIT from other replica"""
        key = (comm['view'], comm['seq'], comm['digest'])
        self.commit_msgs[key].append(comm)
        
        # Check if committed-local (2f+1 COMMITs received)
        if len(self.commit_msgs[key]) >= 2 * self.f + 1:
            # Execute request
            seq = comm['seq']
            if seq in self.pre_prepare_msgs:
                request = self.pre_prepare_msgs[seq]['msg']
                result = self.execute(request)
                return {"type": "REPLY", "result": result}
        return None
    
    def execute(self, request):
        """Execute client request"""
        self.log.append(request)
        return f"Executed: {request}"

# Simulation
n_replicas = 4
f = 1  # Tolerate 1 Byzantine failure
replicas = [PBFTReplica(i, n_replicas, f) for i in range(n_replicas)]

# Client request
request = "TRANSFER $100 from Alice to Bob"
primary = replicas[0]
pp_msg = primary.receive_request(request)
print(f"Primary broadcasts PRE-PREPARE: {pp_msg}")

# Replicas receive PRE-PREPARE and send PREPARE
for r in replicas[1:]:
    prep_msg = r.receive_pre_prepare(pp_msg)
    if prep_msg:
        print(f"Replica {r.id} broadcasts PREPARE")
```

---

## Phase 2: Stress Questions

### Q1: 3f+1 Lower Bound Proof
**Prove that n ≥ 3f+1 is necessary for Byzantine consensus.**

<details><summary>Hint</summary>
Assume n = 3f. Partition into 3 groups of f. Two groups must agree, but could be 2f Byzantine nodes. Honest nodes can't distinguish.
</details>

### Q2: PBFT Message Complexity
**Analyze PBFT message complexity. Show it's O(n²) per request.**

<details><summary>Hint</summary>
PRE-PREPARE: 1 → n (O(n)). PREPARE: n → n (O(n²)). COMMIT: n → n (O(n²)). Total: O(n²).
</details>

### Q3: Economic Byzantine Model
**In blockchain with f Byzantine miners out of n total, what fraction f/n can system tolerate? Compare PoW (Bitcoin) vs PoS (Ethereum).**

<details><summary>Hint</summary>
PoW (longest chain): Tolerates f < n/2 (50% attack). PoS (BFT-based): Tolerates f < n/3 (33% attack). Economic cost matters: attacking PoW requires hardware, attacking PoS risks staked capital.
</details>

---

## Phase 3: Applied Problem

Design a Byzantine-tolerant blockchain for supply chain:
- Participants: manufacturers, shippers, retailers
- Each signs transactions
- Byzantine node may create fake shipments

**Part A**: Implement PBFT for transaction ordering.

**Part B**: Add checkpointing to compact log.

**Part C**: Analyze cost: message overhead, latency vs Raft.

---

## Phase 4: Self-Assessment

### Checklist
- [ ] Understand Byzantine failures vs crash failures
- [ ] Know why n ≥ 3f+1 required
- [ ] Can explain PBFT phases
- [ ] Understand blockchain consensus (PoW, PoS)

### Next Steps
- **Strong**: [[Session 20 – Distributed Training]]
- **Struggling**: Review [[Session 05 – Networks & Distributed Systems]]
- **Resources**: PBFT paper (Castro & Liskov), "Bitcoin" whitepaper

---

**Navigation**: ← [[Session 18]] | **Index**: [[cycle3/INDEX]] | → [[Session 20]]
