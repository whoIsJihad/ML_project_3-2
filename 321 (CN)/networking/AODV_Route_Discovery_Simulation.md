# AODV Route Discovery Simulation

## Prerequisite

This note provides a detailed step-by-step simulation of the route discovery process in [[AODV_Protocol|AODV]]. Familiarity with AODV basics is assumed; refer to [[AODV_Protocol]] for algorithm overview.

## Network Topology

Consider a network with 6 nodes arranged as follows:

```
        S (Source)
       /|\
      / | \
     A  B  C
     |  |  |
     D  E  F
      \ | /
        D (Destination)
```

More precisely, the topology is:

| Link | Distance (hops) |
|---|---|
| S-A | 1 |
| S-B | 1 |
| S-C | 1 |
| A-D | 1 |
| B-E | 1 |
| C-F | 1 |
| D-E | 1 |
| E-F | 1 |

In AODV, nodes use broadcast addresses and hop counts. Assume:
- Broadcast medium allows all adjacent nodes to hear a transmission.
- Link costs are uniform (one hop = one unit cost).
- Nodes use IP addresses: S=`10.0.0.1`, A=`10.0.0.2`, ..., D=`10.0.0.8`.

## Initial State

**Route Request (RREQ) Sequence Numbers**:
- S.seq = 100 (S has sent 100 previous RREQs)
- A.seq = 20, B.seq = 15, C.seq = 22, D.seq = 50, E.seq = 18, F.seq = 25

**Destination Sequence Number** for D: `50` (D's current sequence number)

**Reverse Path Routes**:
- Initially, no routes exist from destination D to any node.

## Step 1: Source Initiates Route Discovery

**Time**: $t = 0$ s

**Source S** initiates RREQ for destination D:

```
S.broadcast RREQ {
  source: S
  destination: D
  source_seq: 100
  dest_seq: 50
  hop_count: 0
  broadcast_id: 1
  request_id: S_100_1
}
```

**Action**: S creates a reverse path entry for itself (S can reach S via itself with hop count 0).

**Routing Table at S**:
```
Destination | Next Hop | Hops | Sequence | Expiry
S           | S        | 0    | 100      | t+lifetime
```

## Step 2: Intermediate Nodes Receive and Forward RREQ

**Time**: $t = 1$ s (RREQ propagates one hop)

**Nodes A, B, C** receive the RREQ from S:

Each intermediate node processes the RREQ as follows:

### Processing at Node A

**Received RREQ**:
```
RREQ {
  source: S, dest: D, source_seq: 100, dest_seq: 50,
  hop_count: 0 (will be incremented to 1)
}
```

**Step 2.1: Check if already processed**

A checks if it has processed this RREQ before. The RREQ ID is `S_100_1`. If not seen before, continue.

**Step 2.2: Create reverse path**

A creates a reverse path to S (the originator of the RREQ):
```
A.routing_table[S] = {
  next_hop: S (neighbor from which RREQ arrived)
  hop_count: 1 (received hop_count + 1)
  sequence: 100
  expiry: current_time + path_lifetime
}
```

**Step 2.3: Check if A is destination**

A compares its ID with D. A ≠ D, so A is not the destination.

**Step 2.4: Check if A has fresh route to destination**

A checks its routing table for destination D:
- If A has a route to D with `A.route_seq[D] ≥ RREQ.dest_seq` (i.e., A's knowledge of D is at least as fresh):
  - A can send a Route Reply (RREP) instead of forwarding the RREQ.
  - In this scenario, assume A has no route to D, so proceed to forward.

**Step 2.5: Forward RREQ**

A increments hop_count and rebroadcasts:
```
A.broadcast RREQ {
  source: S
  destination: D
  source_seq: 100
  dest_seq: 50
  hop_count: 1  // incremented
  broadcast_id: 1
  request_id: S_100_1
}
```

**Result**: A's routing table now contains:
```
Destination | Next Hop | Hops | Sequence | Expiry
S           | S        | 1    | 100      | t+lifetime
```

### Processing at Node B

Identical to Node A:

**B's Routing Table**:
```
Destination | Next Hop | Hops | Sequence | Expiry
S           | S        | 1    | 100      | t+lifetime
```

**B forwards RREQ with hop_count = 1**.

### Processing at Node C

Identical processing:

**C forwards RREQ with hop_count = 1**.

## Step 3: Second-Hop Propagation

**Time**: $t = 2$ s

Nodes D, E, F receive the RREQ from A, B, C respectively.

### Processing at Node D

**D receives RREQ from A** (also receives from B and C, but we trace one):

```
RREQ {
  source: S, dest: D, source_seq: 100, dest_seq: 50,
  hop_count: 1 (becomes 2)
}
```

**Step 3.1: Is D the destination?**

D checks if its address matches the destination. **Yes, D is the destination.**

**Step 3.2: Create reverse path to S**

D creates a reverse path to S via A:
```
D.routing_table[S] = {
  next_hop: A
  hop_count: 2
  sequence: 100
  expiry: current_time + path_lifetime
}
```

**Step 3.3: Update destination sequence**

D compares the RREQ's dest_seq (50) with D's current sequence number (50):
- They are equal, indicating D's sequence in the RREQ is fresh.

**Step 3.4: Send Route Reply (RREP)**

Since D is the destination, it sends a RREP back to S:

```
D.send RREP {
  source: S
  destination: D
  dest_seq: 50  // D's current sequence number
  hop_count: 2  // number of hops from D to S
  lifetime: 3000 ms
}
```

**Direction**: The RREP is sent back along the reverse path. D knows the next hop to S is A (from the reverse path created above).

**RREP is sent unicast to A** (not broadcast).

## Step 4: RREP Propagation Back to Source

**Time**: $t = 3$ s (RREP propagates back one hop)

**Node A receives RREP from D**:

```
RREP {
  source: S
  destination: D
  dest_seq: 50
  hop_count: 2
}
```

**Step 4.1: Is A the source of the RREQ?**

A checks if it originated the RREQ. **No**, S originated it. So A is not the final destination of the RREP.

**Step 4.2: Update or create forward path**

A creates a forward path to D:
```
A.routing_table[D] = {
  next_hop: D  // next hop toward D
  hop_count: 2 - 1 = 1  // RREP.hop_count - 1 (because RREP includes the hop from A to D)
  sequence: 50  // D's sequence from RREP
  expiry: current_time + RREP.lifetime
}
```

Actually, let's be more careful. The RREP arriving at A came from D with hop_count = 2. This means D is 2 hops away from S. But from A's perspective, D is 1 hop away (the RREP came directly from D). So A's forward route is:

```
A.routing_table[D] = {
  next_hop: D
  hop_count: 1
  sequence: 50
  expiry: current_time + 3000 ms
}
```

**Step 4.3: Forward RREP toward source**

A forwards the RREP toward S (the source of the original RREQ). A consults its reverse path to S:
- A knows the next hop to S is S itself (one hop away).
- A unicasts the RREP to S, decrementing hop_count:

```
A.send RREP to S {
  source: S
  destination: D
  dest_seq: 50
  hop_count: 1 + 1 = 2  // A is 1 hop from D, so 2 hops total from S
  lifetime: 3000 ms
}
```

## Step 5: Route Reply Arrives at Source

**Time**: $t = 4$ s

**Node S receives RREP from A**:

```
RREP {
  source: S
  destination: D
  dest_seq: 50
  hop_count: 2
  lifetime: 3000 ms
}
```

**Step 5.1: Create forward path**

S creates a forward route to D:
```
S.routing_table[D] = {
  next_hop: A
  hop_count: 2
  sequence: 50
  lifetime: current_time + 3000 ms
  route_status: ACTIVE
}
```

**Step 5.2: Route discovery complete**

S can now send data packets to D via A. The route is S → A → D.

### Simultaneous RREP from Node B

At approximately the same time, B also receives the RREQ and forwards it. D receives the RREQ from B and could send another RREP. However:

- The RREP from B would have hop_count = 3 (via B).
- S would receive this RREP after receiving the RREP from A.
- S would compare the two:
  - Via A: 2 hops, sequence 50.
  - Via B: 3 hops, sequence 50.
- **S prefers the route with fewer hops** (2 < 3), so the route via A is selected.

## Summary of Discovery Process

| Time | Event |
|---|---|
| $t=0$ | S broadcasts RREQ for D (hop_count = 0) |
| $t=1$ | A, B, C receive RREQ; create reverse path to S; forward with hop_count = 1 |
| $t=2$ | D, E, F receive RREQ; D is destination, creates reverse path, sends RREP |
| $t=3$ | A receives RREP from D; creates forward path to D; forwards RREP to S |
| $t=4$ | S receives RREP from A; creates forward path to D via A |

**Final Route**: S → A → D (2 hops)

## Routing Tables After Route Discovery

**At S**:
```
Destination | Next Hop | Hops | Seq | Lifetime
A           | A        | 1    | 20  | t+lifetime
B           | B        | 1    | 15  | t+lifetime
C           | C        | 1    | 22  | t+lifetime
D           | A        | 2    | 50  | t+4s
```

**At A**:
```
Destination | Next Hop | Hops | Seq | Lifetime
S           | S        | 1    | 100 | t+lifetime
D           | D        | 1    | 50  | t+4s
```

**At D**:
```
Destination | Next Hop | Hops | Seq | Lifetime
S           | A        | 2    | 100 | t+lifetime
```

## Data Packet Transmission

Once the route is established, S can send data to D:

```
Data Packet:
  source: S (10.0.0.1)
  destination: D (10.0.0.8)
  hopcount: 2
  
Path: S → A → D
```

**At S**: Consults routing table, forwards to A.
**At A**: Consults routing table, forwards to D.
**At D**: Packet arrives; destination reached.

## Key Observations

1. **Broadcast efficiency**: The RREQ flooded through the network reaches the destination; only one RREP is sent back (via the shortest path).
2. **Reverse path learning**: Intermediate nodes learn the reverse path to the source automatically.
3. **Sequence numbers**: Ensure freshness of routes and prevent loops.
4. **Loop freedom**: By following the reverse path (which is established during RREQ forward propagation), RREPs follow a loop-free path.

## Related Concepts

- [[AODV_Protocol]]: AODV algorithm overview and procedures.
- [[AODV_Route_Maintenance_Simulation]]: What happens when the route breaks.

---

**Next:** [[AODV_Route_Maintenance_Simulation]]
