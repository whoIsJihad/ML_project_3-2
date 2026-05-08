# AODV Route Maintenance Simulation

## Prerequisite

This note simulates route maintenance and failure handling in [[AODV_Protocol|AODV]]. Familiarity with route discovery (see [[AODV_Route_Discovery_Simulation]]) and basic AODV operations is assumed.

## Overview: Why Route Maintenance is Needed

In [[Ad_Hoc_Networks_Overview|ad hoc networks]], topology changes constantly:
- Nodes move out of range, breaking links.
- Nodes power off or fail.
- Wireless channel quality degrades, causing link failures.

When a link used by an active route breaks, the routing protocol must:
1. Detect the failure quickly.
2. Notify affected nodes (source and routing nodes).
3. Repair or rediscover the route.

AODV's route maintenance mechanisms handle these scenarios.

## Network Topology and Initial State

Assume the network from [[AODV_Route_Discovery_Simulation]], with an established route:

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

**Active Route**: S → A → D (established after route discovery).

**Routing Tables**:

**At S**:
```
Destination | Next Hop | Hops | Seq | Status | Expiry
D           | A        | 2    | 50  | ACTIVE | t+3000ms
```

**At A**:
```
Destination | Next Hop | Hops | Seq | Status | Expiry
S           | S        | 1    | 100 | ACTIVE | t+3000ms
D           | D        | 1    | 50  | ACTIVE | t+3000ms
```

**At D**:
```
Destination | Next Hop | Hops | Seq | Status | Expiry
S           | A        | 2    | 100 | ACTIVE | t+3000ms
```

**Active Routes List**:
- S has active routes to A and D.
- A has active routes to S and D.
- D has an active route to S.

## Scenario: Link A-D Failure

At time $t = 500$ ms, the link between A and D breaks. This could occur because:
- D moves out of range of A.
- A's wireless interface fails.
- An obstacle blocks the line-of-sight path.

## Step 1: Link Failure Detection

### Mechanism: Hello Messages

In AODV, routers periodically send **Hello messages** (AODV messages with TTL = 1) to neighbors:

```
Hello Message Format:
  source: A
  destination: broadcast (255.255.255.255)
  TTL: 1  // not forwarded beyond neighbors
  hop_count: 1
  sequence: 21 (A's current sequence number)
```

Hello messages allow neighbors to detect link status via:
- **Presence detection**: Receiving hello messages indicates an active link.
- **Absence detection**: Not receiving expected hello messages for a timeout period indicates link failure.

**Default Parameters**:
- Hello interval: 1000 ms (send every 1 second).
- Allowed Hello loss: 3 consecutive misses.
- Link failure timeout: 3 × 1000 ms = 3000 ms.

### Detection at Node A

**At $t = 500$ ms**: A sends a data packet to D (via routing table entry).

```
A sends packet to D:
  dest: D
  via: D (direct link)
```

At the link layer, A waits for an acknowledgment (link-layer ACK):
- In AODV over IEEE 802.11, the MAC layer provides ACK feedback.
- If the MAC layer ACK is not received after retransmissions, the link is considered broken.

**Alternatively, using Hello messages**:
- D's last Hello message was received at $t = 400$ ms.
- No Hello message is received from D by $t = 3400$ ms.
- A marks the link to D as broken.

**Assumption in this simulation**: We assume immediate link failure detection (for simplicity). A detects that D is unreachable at $t = 500$ ms.

## Step 2: Invalidating Affected Routes

When A detects that the link to D is broken, A must invalidate all routes that depend on the link to D as the next hop.

### Routes Affected by A-D Link Failure

**At A**:
```
Destination | Next Hop | Status
D           | D        | ACTIVE → BROKEN (next hop is D, which is now unreachable)
```

**Routes affected**: Any route at any node that has A as the next hop and D as the destination.

**Upstream Nodes**: Nodes that rely on A to reach D:
- S has route S → A → D.
- D has route D ← A ← S (reverse).

### Route Invalidation Process

**At A** (directly affected):
```
A.invalidate_route(D):
  A.routing_table[D].destination_sequence += 1  // increment seq of D
  A.routing_table[D].status = INVALID
  A.routing_table[D].hop_count = INFINITY  // mark as unreachable
  A.broken_link_list.add((A, D))
```

After invalidation:
```
Destination | Next Hop | Hops | Seq | Status
D           | D        | ∞    | 51  | INVALID
```

Note: D's sequence is incremented to 51 (was 50). This prevents S from using stale RREP information from before the link failure.

## Step 3: Route Error (RERR) Propagation

### RERR Generation at A

A generates a **Route Error (RERR)** message to notify upstream nodes that D is unreachable:

```
RERR Message:
  unreachable_destinations: [(D, 51)]
  // list of (destination, new_sequence_number) pairs
```

A must send this RERR to all nodes that have routes depending on A as the next hop to D:
- Reverse path to S: A sends RERR toward S.

A consults its reverse path to S (from route discovery):
```
A.routing_table[S] = {next_hop: S, hops: 1}
```

### Broadcasting RERR

A broadcasts the RERR to all neighbors (not just S):

```
A.broadcast RERR {
  unreachable_destinations: [(D, 51)]
  source: A
}
```

**Precursor List**: To optimize RERR propagation, A includes a **precursor list** of nodes that have routes depending on the broken link:
- S is a precursor (S has a route to D via A).

## Step 4: RERR Processing at S

**Time**: $t = 502$ ms (RERR propagates to S, 2 hops away, assuming 1 ms per hop)

**S receives RERR from A**:

```
RERR {
  unreachable_destinations: [(D, seq=51)]
}
```

### Processing at S

**Step 4.1: Identify affected routes**

S checks if it has any routes with destination D:
```
S.routing_table[D] = {next_hop: A, hops: 2, seq: 50}
```

S has a route to D, and the next hop is A (the sender of the RERR).

**Step 4.2: Invalidate the route**

S increments D's sequence number in its routing table and marks the route as invalid:

```
S.invalidate_route(D):
  S.routing_table[D].destination_sequence = max(51, 50) = 51
  S.routing_table[D].status = INVALID
  S.routing_table[D].hop_count = INFINITY
```

After invalidation:
```
Destination | Next Hop | Hops | Seq | Status
D           | A        | ∞    | 51  | INVALID
```

**Step 4.3: Propagate RERR further**

S must notify any upstream nodes that have routes depending on S to reach D. In this network:
- No node has S as the next hop to D (S is the source).
- S itself is the originator, so it doesn't propagate RERR further.

However, S checks its precursor list:
```
S.precursor_list[D] = {nodes for which S is next hop for D} = {} (empty)
```

Since there are no precursors, S stops RERR propagation.

### Alternative: RERR Propagation to Other Upstream Nodes

If the topology were different and there were nodes upstream of A also depending on A to reach D, the RERR would propagate further up the tree.

Example: If B also had a route to D via A, B would:
1. Receive RERR from A.
2. Invalidate its route to D.
3. Propagate RERR upstream (if it has precursors for D).

## Step 5: Route Rediscovery

After invalidating the broken route, S has no path to D. S must rediscover the route using RREQ.

### Initiating a New Route Discovery

**At $t = 1000$ ms**: S has a data packet destined for D but no valid route.

**S increments its own sequence number and initiates a new RREQ**:

```
S.sequence += 1  // S.seq goes from 100 to 101
S.broadcast RREQ {
  source: S
  destination: D
  source_seq: 101
  dest_seq: 51  // D's last known sequence
  hop_count: 0
  broadcast_id: 2  // new route discovery request
}
```

Note: The destination sequence is 51, from the RERR. If S didn't have this information, it would use 50 (or 0, accepting any sequence).

### RREQ Propagation

The RREQ propagates through the network:
1. **$t = 1000$ ms**: S broadcasts RREQ; neighbors A, B, C receive it.
2. **$t = 1001$ ms**: A, B, C rebroadcast (hop_count = 1).
3. **$t = 1002$ ms**: D, E, F receive RREQ.

### D Responds to RREQ

D receives the RREQ (from multiple nodes: A, B, C) and generates a RREP.

**Option 1: RREP via B**
```
RREQ from B: hop_count = 1, request_id = S_101_2
```

B forwards with hop_count = 1. E receives and forwards with hop_count = 2. F receives and forwards... or D receives directly from B or via B.

Let's assume D receives RREQ from B with hop_count = 2 (via B and one more hop):

**Via B-E**: Distance is 2 hops (B → E → D) or not directly connected in our topology.

Actually, let's reconsider our topology. Looking back:
```
  S
 /|\
A B C
|  |  |
D  E  F
\  |  /
  D
```

This is confusing. Let me redefine:

Nodes: S, A, B, C, D, E, F. But we have two D's (D as intermediate and D as destination). Let me re-index.

Let's use:
- S: source
- A, B, C: neighbors of S
- N4, N5, N6: neighbors of A, B, C respectively
- D: destination

**Updated Topology**:
```
        S
       /|\
      / | \
     A  B  C
     |  |  |
     N4 N5 N6
```

In the previous simulation, let's assume:
- A-N4 link exists and breaks.
- B-N5 link and C-N6 link are not used in the original route.
- D is node N4.

**Original route**: S → A → N4 (D).

After the A-N4 link breaks, the RREQ propagates and can reach D via:
- S → B → N5 → (need path to N4)
- S → C → N6 → (need path to N4)

Depending on topology connectivity, an alternative path might be found. For simplicity, assume:
- S → B → N5 → N4 (3 hops).
- S → C → N6 → N4 (3 hops).

Either of these could be used as the new route.

## Step 6: New Route Establishment

D generates a RREP to S via B (assuming the RREQ reached D through B first or B provides a better path):

```
D sends RREP {
  source: S
  destination: D (i.e., N4)
  dest_seq: 51
  hop_count: 3
}
```

The RREP propagates back to S: D → B → S.

S receives RREP and updates its routing table:

```
S.routing_table[D]:
  next_hop: B
  hop_count: 3
  seq: 51
  status: ACTIVE
  lifetime: current_time + 3000 ms
```

**New route**: S → B → N5 → N4 (D).

## Step 7: Local Route Repair (Optional)

In some AODV implementations, intermediate nodes can attempt **local route repair** instead of waiting for the source to rediscover the route.

**Precondition**: The intermediate node (e.g., A) has sufficient information to repair the route locally.

**Process at A**:
```
A.broken_route(D):
  if (A.hop_count[D] > THRESHOLD):  // route was relatively fresh
    A.local_repair = true
    A.initiate_RREQ_for_D()  // A acts as a source for route discovery
  else:
    // do nothing; wait for source to rediscover
  end if
```

In our scenario, A's route to D had hop_count = 1 (A was directly connected to D). This is not a case for repair; instead, A waits for the source to rediscover.

**Local repair is useful** when:
- A has a route to D via other neighbors (N5, N6).
- A can quickly find an alternative path to D by sending an RREQ.

However, local repair adds complexity and is disabled in many AODV implementations.

## Summary of Route Maintenance

| Time | Event | Action |
|---|---|---|
| 500 ms | A-D link breaks | A detects broken link |
| 500 ms | A invalidates route to D | A increments D's seq to 51 |
| 501 ms | A broadcasts RERR | All nodes with A as next hop to D learn of failure |
| 502 ms | S receives RERR | S invalidates route to D |
| 1000 ms | S sends new RREQ | S initiates route rediscovery with seq 101 |
| 1002 ms | D receives RREQ | D generates RREP |
| 1003 ms | S receives RREP | S establishes new route via B |

## Routing Tables After Maintenance

**At S** (after new route):
```
Destination | Next Hop | Hops | Seq | Status
A           | A        | 1    | 20  | ACTIVE
B           | B        | 1    | 15  | ACTIVE
C           | C        | 1    | 22  | ACTIVE
D           | B        | 3    | 51  | ACTIVE  // changed from A to B
```

**At A** (after link failure and rediscovery):
```
Destination | Next Hop | Hops | Seq | Status
S           | S        | 1    | 101 | ACTIVE
D           | D        | ∞    | 51  | INVALID  // original route broken
```

**At B**:
```
Destination | Next Hop | Hops | Seq | Status
S           | S        | 1    | 101 | ACTIVE
D           | (next toward D) | ... | 51 | ACTIVE
```

## Key Concepts

### Sequence Numbers in Maintenance

Sequence numbers are critical:
- **D's original sequence**: 50.
- **After RERR**: D's sequence becomes 51 (RERR informs that D's routes have changed).
- **S uses 51** in the new RREQ, ensuring it doesn't accidentally use an RREP based on the old sequence (50).

### Precursor Lists

AODV maintains a **precursor list** for each route entry:
```
precursor_list[destination] = {nodes for which this node is next hop}
```

When a route is broken, RERR is sent only to precursors, reducing control overhead.

### Route Timeout and Cleanup

Routes that are not used for a period (e.g., 3000 ms) expire and are removed:
```
route_lifetime = current_time + ACTIVE_ROUTE_TIMEOUT
if (current_time > route_lifetime):
  delete routing_table[destination]
end if
```

## Related Concepts

- [[AODV_Protocol]]: AODV algorithm details.
- [[AODV_Route_Discovery_Simulation]]: How routes are initially discovered.
- [[Ad_Hoc_Networks_Overview]]: Overview of ad hoc routing challenges.

---

**Next:** [[Congestion_Control_Fundamentals]]
