# Session 12 – Consensus Algorithms (Paxos & Raft)

## Linked Domain
[[Networks & Distributed Systems]]

**Cycle**: 2 (Intermediate Depth)  
**Difficulty**: ⚫⚫⚪⚪

---

## Phase 1: Theoretical Foundation

### Definitions

**Consensus Problem**: N processes must agree on a single value such that:
1. **Agreement**: All non-faulty processes decide on the same value
2. **Validity**: The decided value was proposed by some process
3. **Termination**: All non-faulty processes eventually decide

**FLP Impossibility**: In an asynchronous system with even one crash failure, no deterministic consensus algorithm can guarantee termination. (Fischer, Lynch, Paterson 1985)

**Quorum**: A majority subset of nodes (⌈N/2⌉ + 1 for N nodes). Any two quorums must intersect.

**Ballot Number**: A totally-ordered identifier (epoch, sequence number) used to prevent conflicts between concurrent proposals.

### Core Mechanism: Basic Paxos

**Roles**:
- **Proposers**: Propose values
- **Acceptors**: Vote on proposals (typically 2f+1 acceptors tolerate f failures)
- **Learners**: Learn the chosen value

**Phase 1: Prepare**
1. Proposer chooses ballot number `n` (higher than any seen)
2. Sends `PREPARE(n)` to majority of acceptors
3. Acceptor responds with:
   - Promise not to accept proposals < n
   - Highest-numbered proposal already accepted (if any)

**Phase 2: Accept**
1. If proposer receives majority promises:
   - If any acceptor returned a proposal, use that value
   - Otherwise, use proposer's own value
2. Send `ACCEPT(n, value)` to acceptors
3. Acceptor accepts if no higher-numbered prepare seen

**Value is Chosen** when majority of acceptors accept the same (n, value).

**Paxos Safety Invariant**: If value `v` is chosen, then every proposal with ballot > n has value `v`.

### Core Mechanism: Raft

**Three States**: Follower, Candidate, Leader

**Leader Election**:
1. Follower times out → becomes Candidate
2. Increments `currentTerm`, votes for self
3. Sends `RequestVote` to all nodes
4. Node votes if candidate's log is "at least as up-to-date"
5. Candidate with majority votes becomes Leader

**Log Replication**:
1. Leader receives client command
2. Appends to local log, sends `AppendEntries` to followers
3. When entry replicated on majority → commits
4. Committed entries applied to state machine

**Safety**: 
- **Election Safety**: At most one leader per term
- **Leader Append-Only**: Leader never overwrites its log
- **Log Matching**: If two logs contain entry with same index/term, all preceding entries are identical
- **Leader Completeness**: If entry committed in term T, it's in the log of all leaders for terms > T

### Mental Model

**Paxos as Voting**: Think of Paxos as a two-round voting system. Round 1 ("Prepare") is candidate registration—checking if anyone voted already. Round 2 ("Accept") is actual voting. The trick: if someone already voted, you must propose their value (ensures consistency).

**Raft as Leader-Driven**: Raft simplifies by funneling all decisions through a leader. The leader's log is the "source of truth." Elections ensure the most up-to-date log becomes leader.

**Quorum Intersection**: The magic of quorums is that any two majorities overlap. This overlap ensures information propagates even with failures.

### Edge Cases

**1. Dueling Proposers (Paxos Livelock)**
```
Proposer A: PREPARE(n=1)
Proposer B: PREPARE(n=2)  -- invalidates A's prepare
Proposer A: PREPARE(n=3)  -- invalidates B's prepare
... endless loop, no progress
```
**Solution**: Exponential backoff, leader election (→ Multi-Paxos)

**2. Split Vote in Raft**
```
5 nodes, 2 candidates:
Candidate A gets votes: {A, B}
Candidate C gets votes: {C, D}
Node E times out before deciding
No majority → new election
```

**3. Network Partition**
```
Cluster: {A, B, C, D, E}
Partition: {A, B} | {C, D, E}

Minority {A, B} cannot elect leader (need 3 votes)
Majority {C, D, E} elects leader and continues
When partition heals, minority logs updated by leader
```

### Common Mistakes

1. **Confusing "Accepted" with "Chosen"**: A value is chosen only when MAJORITY accepts, not when one acceptor accepts.

2. **Ignoring Ballot Numbers**: Without globally unique, totally-ordered ballots, two proposers can interfere catastrophically.

3. **Leader Election Timing**: Too short timeout → unnecessary elections (split votes). Too long → slow failure recovery.

4. **Log Compaction**: Raft requires snapshotting; can't keep infinite log.

### Implementation Code

```python
import time
import random
from enum import Enum

# ============= PAXOS =============

class PaxosAcceptor:
    def __init__(self, id):
        self.id = id
        self.promised_ballot = -1
        self.accepted_ballot = -1
        self.accepted_value = None
        
    def receive_prepare(self, ballot):
        """Phase 1: Prepare handler"""
        if ballot > self.promised_ballot:
            self.promised_ballot = ballot
            return {
                'promise': True,
                'accepted_ballot': self.accepted_ballot,
                'accepted_value': self.accepted_value
            }
        return {'promise': False}
    
    def receive_accept(self, ballot, value):
        """Phase 2: Accept handler"""
        if ballot >= self.promised_ballot:
            self.promised_ballot = ballot
            self.accepted_ballot = ballot
            self.accepted_value = value
            return {'accepted': True}
        return {'accepted': False}

class PaxosProposer:
    def __init__(self, id, acceptors):
        self.id = id
        self.acceptors = acceptors
        self.ballot = id  # Each proposer starts with unique ballot
        
    def propose(self, value):
        """Run full Paxos protocol"""
        self.ballot += len(self.acceptors)  # Ensure unique ballots
        
        # Phase 1: Prepare
        promises = []
        for acc in self.acceptors:
            resp = acc.receive_prepare(self.ballot)
            if resp['promise']:
                promises.append(resp)
        
        if len(promises) < len(self.acceptors) // 2 + 1:
            return None  # No quorum
        
        # Find highest-ballot accepted value
        max_ballot = -1
        chosen_value = value
        for p in promises:
            if p['accepted_ballot'] > max_ballot:
                max_ballot = p['accepted_ballot']
                chosen_value = p['accepted_value']
        
        # Phase 2: Accept
        accepts = 0
        for acc in self.acceptors:
            resp = acc.receive_accept(self.ballot, chosen_value)
            if resp['accepted']:
                accepts += 1
        
        if accepts >= len(self.acceptors) // 2 + 1:
            return chosen_value
        return None

# ============= RAFT =============

class RaftState(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3

class LogEntry:
    def __init__(self, term, command):
        self.term = term
        self.command = command

class RaftNode:
    def __init__(self, id, peer_ids):
        self.id = id
        self.peer_ids = peer_ids
        self.state = RaftState.FOLLOWER
        
        # Persistent state
        self.current_term = 0
        self.voted_for = None
        self.log = []  # List of LogEntry
        
        # Volatile state
        self.commit_index = -1
        self.last_applied = -1
        
        # Leader state
        self.next_index = {}  # peer_id -> next log index to send
        self.match_index = {}  # peer_id -> highest replicated index
        
        self.election_timeout = self._random_timeout()
        self.last_heartbeat = time.time()
        
    def _random_timeout(self):
        return random.uniform(0.15, 0.30)  # 150-300ms
    
    def request_vote(self, term, candidate_id, last_log_index, last_log_term):
        """Handle RequestVote RPC"""
        if term < self.current_term:
            return {'term': self.current_term, 'vote_granted': False}
        
        if term > self.current_term:
            self.current_term = term
            self.voted_for = None
            self.state = RaftState.FOLLOWER
        
        # Check if candidate's log is at least as up-to-date
        my_last_term = self.log[-1].term if self.log else 0
        my_last_index = len(self.log) - 1
        
        log_ok = (last_log_term > my_last_term or 
                  (last_log_term == my_last_term and last_log_index >= my_last_index))
        
        if (self.voted_for is None or self.voted_for == candidate_id) and log_ok:
            self.voted_for = candidate_id
            self.last_heartbeat = time.time()
            return {'term': self.current_term, 'vote_granted': True}
        
        return {'term': self.current_term, 'vote_granted': False}
    
    def append_entries(self, term, leader_id, prev_log_index, prev_log_term, 
                       entries, leader_commit):
        """Handle AppendEntries RPC (heartbeat or log replication)"""
        if term < self.current_term:
            return {'term': self.current_term, 'success': False}
        
        self.last_heartbeat = time.time()
        self.current_term = term
        self.state = RaftState.FOLLOWER
        
        # Check log consistency
        if prev_log_index >= 0:
            if prev_log_index >= len(self.log) or \
               self.log[prev_log_index].term != prev_log_term:
                return {'term': self.current_term, 'success': False}
        
        # Append new entries
        for i, entry in enumerate(entries):
            idx = prev_log_index + 1 + i
            if idx < len(self.log):
                if self.log[idx].term != entry.term:
                    self.log = self.log[:idx]  # Delete conflicting entries
                    self.log.append(entry)
            else:
                self.log.append(entry)
        
        # Update commit index
        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, len(self.log) - 1)
        
        return {'term': self.current_term, 'success': True}
    
    def start_election(self):
        """Convert to candidate and request votes"""
        self.state = RaftState.CANDIDATE
        self.current_term += 1
        self.voted_for = self.id
        self.election_timeout = self._random_timeout()
        
        last_log_index = len(self.log) - 1
        last_log_term = self.log[-1].term if self.log else 0
        
        # In real implementation, send RequestVote RPCs to all peers
        # and count votes
        return self.current_term

# Example Usage
acceptors = [PaxosAcceptor(i) for i in range(5)]
proposer1 = PaxosProposer(1, acceptors)
proposer2 = PaxosProposer(2, acceptors)

result1 = proposer1.propose("value_A")
result2 = proposer2.propose("value_B")
print(f"Proposer 1 result: {result1}")
print(f"Proposer 2 result: {result2}")
# Both will agree on same value (whichever completes Phase 1 first)
```

---

## Phase 2: Stress Questions

### Question 1: Paxos Safety Proof
**Prove Paxos's safety property: If a value `v` is chosen in ballot `n`, then every proposal with ballot `m > n` must have value `v`.**

<details>
<summary>Hint</summary>
Use proof by induction on ballot numbers. Key insight: Any quorum in round m must intersect with the quorum that chose v in round n. That intersection ensures the proposer in round m learns about v.
</details>

---

### Question 2: Raft Timing Analysis
**A 5-node Raft cluster has election timeout uniformly distributed in [T, 2T]. Network latency is L. Analyze:**
- **a)** Probability of split vote
- **b)** Expected time to elect leader after failure
- **c)** Optimal T for 1ms network latency

<details>
<summary>Hint</summary>
Split vote occurs when multiple nodes timeout within L of each other. Probability ≈ (L/T)^k for k candidates. Expected election time ≈ T + kL where k is expected number of rounds.
</details>

---

### Question 3: Multi-Paxos Optimization
**Design Multi-Paxos with throughput optimization. Compare:**
- **a)** Latency: Basic Paxos vs Multi-Paxos
- **b)** Message complexity per decision
- **c)** Failure recovery mechanism

<details>
<summary>Hint</summary>
Multi-Paxos: Skip Phase 1 by electing stable leader. Leader runs only Phase 2 for subsequent values. Latency: 2 RTT → 1 RTT. Messages: 4N → 2N. Recovery: Run Phase 1 when leader changes.
</details>

---

## Phase 3: Applied Problem

### Problem: Distributed Configuration Service

You're building a configuration service (like ZooKeeper) using Raft. Requirements:
- 5-node cluster
- Clients read/write key-value pairs
- Strong consistency (linearizability)
- Must handle: node crashes, network partitions

**Part A: Raft Implementation**
Complete the Raft implementation:
1. Leader election with randomized timeouts
2. Log replication with AppendEntries RPCs
3. Commit logic (majority replication)
4. Read optimization (leader lease)

**Part B: Failure Scenarios**
Analyze behavior in:
1. Leader crash immediately after receiving client write
2. Network partition: {Leader, Node2} | {Node3, Node4, Node5}
3. Cascading failures: 2 nodes crash simultaneously

**Part C: Performance Tuning**
Given:
- Network RTT: 1ms (same datacenter)
- Disk write: 10ms
- Target: 10,000 writes/sec

Optimize for:
- Batching strategy
- Pipeline depth
- Election timeout values

```python
class RaftLog:
    def __init__(self):
        self.entries = []
        self.commit_index = -1
        
    def append(self, term, command):
        """Add entry to log"""
        self.entries.append(LogEntry(term, command))
        return len(self.entries) - 1
    
    def commit_up_to(self, index):
        """Mark entries as committed"""
        self.commit_index = min(index, len(self.entries) - 1)
    
    def get_committed(self):
        """Return committed entries"""
        return self.entries[:self.commit_index + 1]

class RaftLeader:
    def __init__(self, node_id, peer_ids):
        self.node_id = node_id
        self.peer_ids = peer_ids
        self.log = RaftLog()
        self.next_index = {p: 0 for p in peer_ids}
        self.match_index = {p: -1 for p in peer_ids}
        
    def replicate_to_followers(self):
        """
        Send AppendEntries to all followers.
        TODO: Implement replication logic
        """
        pass
    
    def update_commit_index(self):
        """
        Update commit index based on majority replication.
        TODO: Find highest index replicated on majority
        """
        pass
    
    def handle_client_write(self, command):
        """
        Handle client write request.
        TODO: Append to log, replicate, commit, respond to client
        """
        pass
```

**Expected Output**:
```
Part A: Complete Raft implementation with all RPCs
Part B: Failure scenario analysis with state transitions
Part C: 
  - Batching: [parameters]
  - Pipeline depth: [value]
  - Election timeout: [range]
  - Predicted throughput: [writes/sec]
```

---

## Phase 4: Self-Assessment & Feedback

### Mastery Checklist
Rate your understanding (1-5):
- [ ] Understand Paxos Phase 1 and Phase 2 mechanics
- [ ] Can prove Paxos safety invariant
- [ ] Understand Raft leader election and log replication
- [ ] Know when Raft guarantees safety vs liveness
- [ ] Can compare Paxos vs Raft trade-offs

### Reflection Questions
1. **Why is FLP impossibility** not a practical concern for Raft/Paxos?
2. **What's the key insight** that makes quorum-based consensus work?
3. **How would you explain** the difference between Paxos and Raft to a new engineer?

### Mistake Log
Record errors:
- **Conceptual**: (e.g., "thought Leader Completeness only requires any quorum")
- **Implementation**: (e.g., "forgot to check term when handling RPC")
- **Edge cases**: (e.g., "didn't consider split vote scenario")

### Next Steps
- **If strong**: Proceed to [[Session 13 – Second-Order Methods]]
- **If struggling**: Review [[Session 05 – Networks & Distributed Systems]]
- **Deep dive**:
  - "Paxos Made Simple" (Lamport)
  - "In Search of an Understandable Consensus Algorithm" (Raft paper)
  - "Designing Data-Intensive Applications" Ch. 9

---

**Navigation**: ← [[Session 11]] | **Index**: [[cycle2/INDEX]] | → [[Session 13]]
