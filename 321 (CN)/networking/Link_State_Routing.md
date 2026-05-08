# Link-State Routing

## Introduction and Motivation

Link-state routing protocols compute shortest paths by using global network topology information. Unlike distance-vector routing (which relies on neighbors' path costs), link-state routing requires each router to:

1. Learn the complete network topology.
2. Maintain a Link State Database (LSDB) with the state of all links.
3. Compute shortest paths independently using algorithms like Dijkstra's.

**Key Advantage**: Provides faster convergence, loop prevention through sequence numbers, and better scalability for large networks compared to distance-vector routing.

**Key Disadvantage**: Higher computational overhead and memory requirements; flooding of Link State Advertisements (LSAs) increases control traffic.

## Assumptions and Prerequisites

This note assumes familiarity with:
- [[Unicast_Routing_Overview]]: Basic routing concepts.
- [[Distance_Vector_Routing]]: Understanding of distributed routing paradigms.
- Graph theory: Dijkstra's algorithm, shortest paths, weighted graphs.

## Fundamental Concepts

### Link-State Information

Each router announces the state of its directly connected links. For a router $R$ with neighbors $\{N_1, N_2, \ldots, N_k\}$, the link-state information includes:

$$LS_R = \{(R, N_i, c_{R,N_i}) : N_i \in \text{neighbors}(R), i = 1 \ldots k\}$$

where $c_{R,N_i}$ is the cost of the link from $R$ to $N_i$.

**Link Cost Metrics**:
- Hop count (unweighted, all links cost 1)
- Bandwidth (cost = 1 / bandwidth)
- Delay (cost = propagation delay + queueing delay)
- Congestion (cost = function of current queue depth)

### Link State Database (LSDB)

The LSDB at router $R$ is a complete snapshot of all link-state advertisements received from all routers in the network:

$$\text{LSDB}_R = \{LS_X : X \in V\}$$

where $V$ is the set of all routers in the routing domain.

**LSDB Property**: In a stable network with complete convergence, LSDB is identical across all routers.

## Dijkstra's Shortest Path Algorithm

### Algorithm Description

Dijkstra's algorithm computes the shortest path tree from a source router $S$ to all destinations using the LSDB.

**Pseudo-code** (from source $S$):

```
DIJKSTRA(S, LSDB):
  // Initialize
  dist[S] = 0
  dist[X] = ∞ for all X ≠ S
  visited = ∅
  
  // Priority queue of routers, ordered by distance
  pq = {(0, S)}
  
  while pq is not empty:
    (d, u) = extract_min(pq)  // Extract router with smallest distance
    
    if u ∈ visited:
      continue
    
    visited = visited ∪ {u}
    
    // Relax edges from u
    for each neighbor v of u in LSDB:
      cost_uv = LSDB[u][v]  // Link cost from u to v
      
      if dist[u] + cost_uv < dist[v]:
        dist[v] = dist[u] + cost_uv
        predecessor[v] = u
        insert(pq, (dist[v], v))
  
  return dist[], predecessor[]
```

### Example Network and Dijkstra Execution

**Network Topology**:

```
        A (1)
       / \
      / 5 \ 2
     /     \
    S ---4--- B
    |        /|
    6|      / |1
    |     /   |
    C---2-----D
```

**Link Costs**:
- $(S, A)$: 5
- $(S, B)$: 4
- $(S, C)$: 6
- $(A, B)$: 2
- $(B, D)$: 1
- $(C, D)$: 2

**Dijkstra Execution** (from source $S$):

| Step | Current | Distance | Visited | Edges to Relax | Update |
|------|---------|----------|---------|---|---|
| 0 | Start | S:0, others:∞ | {} | - | Initialize |
| 1 | S | S:0 | {S} | (S,A):5, (S,B):4, (S,C):6 | dist[A]=5, dist[B]=4, dist[C]=6 |
| 2 | B | B:4 | {S,B} | (B,A):2, (B,D):1 | dist[A]=min(5,4+2)=5, dist[D]=5 |
| 3 | A | A:5 | {S,B,A} | (A,B):2 | No improvement |
| 4 | D | D:5 | {S,B,A,D} | (D,C):2 | dist[C]=min(6,5+2)=6 |
| 5 | C | C:6 | {S,B,A,D,C} | None | Done |

**Shortest Path Tree at $S$**:

```
        A (cost 5)
       /
      /
    S ---- B (cost 4)
    |    /
    |   /
    C  D (cost 5)
```

**Routing Table at $S$**:

| Destination | Next Hop | Distance |
|---|---|---|
| S | Direct | 0 |
| A | A | 5 |
| B | B | 4 |
| C | C | 6 |
| D | B | 5 |

Note that traffic to $D$ goes through $B$ (via S→B→D), not through A.

### Dijkstra Complexity

**Time Complexity**: $O((V + E) \log V)$ with a binary heap priority queue.
- $V$ = number of routers
- $E$ = number of links

**Space Complexity**: $O(V^2)$ for the LSDB, $O(V)$ for distance and predecessor arrays.

## Link State Advertisement (LSA) Flooding

For all routers to maintain identical LSDbs, link-state information must be reliably flooded throughout the network.

### LSA Packet Structure

```
LSA Header:
  LS Type: Type of LSA (Router-LSA, Network-LSA, etc.)
  LS ID: Identifier for this LSA (usually originating router ID)
  Advertising Router: IP address of the originating router
  LS Sequence Number: seq_num (prevents duplicate processing)
  LS Checksum: CRC of entire LSA content
  LS Age: Time since LSA was originated (incremented as it propagates)
  Length: Total length of LSA

LSA Body:
  Link Descriptions:
    For each link from the advertising router:
      - Link Type (point-to-point, network, stub)
      - Link ID (router ID of neighbor, or network address)
      - Link Data (IP interface address, subnet mask, etc.)
      - Link Metric (cost in some unit)
      - Optional: Type-of-Service (ToS) metrics
```

### Controlled Flooding

To prevent infinite loops and duplicate processing, LSAs are flooded with sequence numbers.

**Flooding Algorithm**:

```
FLOOD_LSA(LSA, incoming_interface):
  if LSA.seq_num ≤ LSDB[LSA.LS_ID].seq_num:
    // Duplicate or older LSA; discard
    return
  
  // Update LSDB
  LSDB[LSA.LS_ID] = LSA
  
  // Recompute shortest paths
  dijkstra_result = DIJKSTRA(self, LSDB)
  update_routing_table(dijkstra_result)
  
  // Forward to all interfaces except incoming_interface
  for each interface i except incoming_interface:
    send(LSA, interface i)
```

**Sequence Number Arithmetic**: To handle wraparound (32-bit numbers), sequence number comparison uses:

$$\text{seq}_A < \text{seq}_B \Leftrightarrow (\text{seq}_A - \text{seq}_B) < 0 \text{ (using signed comparison)}$$

### LSA Aging

LSAs have a maximum age (typically 3600 seconds = 1 hour). When an LSA approaches maximum age, the originating router must refresh it with a new sequence number. If a router detects an LSA reaching maximum age without refresh, it removes the LSA from the LSDB.

**Motivation**: Handles router failures; if a failed router's LSAs age out, other routers learn of the failure without explicit advertisement.

## Example: OSPF (Open Shortest Path First)

OSPF is a link-state routing protocol for interior routing within an AS (Autonomous System).

### OSPF Basics

**Routing Domain Hierarchy**:
- **Areas**: OSPF divides the network into areas to reduce control traffic and SPT computation overhead.
- **Backbone Area (Area 0)**: Core of the network; all areas connect to it via an Area Border Router (ABR).

**Router Types**:
- **Internal Router**: All interfaces in one area.
- **Area Border Router (ABR)**: Has interfaces in multiple areas.
- **Backbone Router**: Has at least one interface in Area 0.
- **AS Border Router (ASBR)**: Exports routes from external routing domains.

### OSPF Message Types

OSPF uses five message types, all encapsulated in IP protocol 89:

1. **HELLO**: Neighbor discovery and liveness; periodic (every 10 seconds).
2. **Database Description (DBD)**: Summarizes LSDB during neighbor establishment.
3. **Link State Request (LSR)**: Requests missing LSAs.
4. **Link State Update (LSU)**: Sends LSAs (one or more per packet).
5. **Link State Acknowledgment (LSACK)**: Acknowledges LSU reception.

### OSPF Neighbor Establishment

Two OSPF routers become neighbors through the following state machine:

**State Transitions**:

```
DOWN
  ↓ (send HELLO)
INIT
  ↓ (receive HELLO from neighbor, mutual recognition)
TWO-WAY
  ↓ (if not DR/BDR, stop; if DR/BDR, continue)
EXSTART
  ↓ (exchange DBD packets)
EXCHANGE
  ↓ (request missing LSAs)
LOADING
  ↓ (receive all requested LSAs)
FULL
```

**FULL State**: Neighbors have identical LSDbs; routes are advertised.

### OSPF Cost Metric

OSPF's default cost metric is:

$$c_i = \frac{10^8}{\text{bandwidth}_i}$$

where $\text{bandwidth}_i$ is the link bandwidth in bits per second.

**Examples**:
- 100 Mbps Ethernet: $c = 10^8 / 100 \times 10^6 = 1$
- 10 Mbps Ethernet: $c = 10^8 / 10 \times 10^6 = 10$
- 1 Mbps WAN: $c = 10^8 / 10^6 = 100$

Routers select paths with the lowest total cost.

### Multi-Area OSPF Example

**Topology**:

```
     Area 0 (Backbone)
         [R1]---[R2]
          |       |
          |  ABR  |
          |       |
        [R4]     [R3]
        /  \    /
       /    \  /
    Area 1  Area 2
      R5    R6
```

**Router Types**:
- $R1, R2$: Backbone routers (in Area 0).
- $R3$: ABR (Area 0 and Area 2).
- $R4$: ABR (Area 0 and Area 1).
- $R5$: Internal router (Area 1 only).
- $R6$: Internal router (Area 2 only).

**LSDB Organization**:
- Each area maintains separate LSDB for internal routes.
- ABRs summarize area routes when advertising to other areas.
- Example: ABR $R4$ advertises Area 1's subnet 192.168.1.0/24 to Area 0 with cost reflecting internal paths.

## Convergence Behavior

### Convergence Time Calculation

Link-state routing convergence comprises:

1. **Failure Detection**: $t_{\text{detect}}$ (typically 30-40 seconds via HELLO timeout).
2. **LSA Origination**: $t_{\text{orig}}$ (immediate upon failure detection).
3. **LSA Flooding**: $t_{\text{flood}} = O(D)$ where $D$ is network diameter (typically <1 second).
4. **SPT Recomputation**: $t_{\text{spf}} = O((V + E) \log V)$ (typically <1 second for networks <1000 routers).

**Total Convergence Time**:

$$t_{\text{conv}} \approx t_{\text{detect}} + t_{\text{flood}} + t_{\text{spf}} \approx 30\text{-}50\text{ seconds}$$

### Convergence Example

Assume topology:

```
S --- A --- B --- D
```

At $t=0$, link $A-B$ fails.

| Time | Event | Router State |
|---|---|---|
| $t = 0$ | A-B link failure | A and B lose neighbor |
| $t = 30$ | A detects B is down (HELLO timeout) | A purges B from LSA |
| $t = 31$ | A originates new LSA (seq_num++) | B does same |
| $t = 31.5$ | S receives both LSAs via flooding | S updates LSDB |
| $t = 32$ | S recomputes SPT with new topology | Convergence complete |

**Data Plane Impact**: Packets to $D$ from $S$ are dropped during convergence (if no alternative path exists). If alternate path exists (e.g., via $C$), packets are rerouted after convergence completes.

## Comparison: Link-State vs. Distance-Vector Routing

| Property | Link-State | Distance-Vector |
|---|---|---|
| **Information Flooded** | Full topology (LSAs) | Route distances (route advertisements) |
| **Computation** | Centralized (SPF/Dijkstra) | Distributed (Bellman-Ford) |
| **LSDB Consistency** | Identical across network (once converged) | Asymmetric per-router views |
| **Convergence Time** | Fast (~1-50 seconds) | Slow (minutes, due to count-to-infinity) |
| **Loop Prevention** | Sequence numbers in LSAs | Routing loops until convergence |
| **Bandwidth Overhead** | Lower (LSAs flood once per topology change) | Lower (periodic small route updates) |
| **Memory** | $O(V^2)$ for LSDB | $O(E)$ for routing table |
| **Scalability** | Better for large networks | Limited (count-to-infinity problem) |
| **Deployment** | Interior routing (OSPF, IS-IS) | Historic (RIPv2), fast-moving networks |
| **Load Balancing** | ECMP over equal-cost paths | Simple per-route selection |

## Practical Issues and Solutions

### Split Horizon and Poison Reverse

While link-state routing doesn't use distance-vector advertisements, similar issues can arise in multi-area OSPF when ABRs advertise area routes. Routers must not advertise back to the originating area.

### OSPF Timers

- **HELLO Interval**: Time between HELLO packets (default 10 seconds).
- **Dead Interval**: Time before neighbor is considered down (default 40 seconds = 4 × HELLO).
- **SPF Delay**: Time to wait before first SPF computation (default 0 seconds).
- **SPF Hold Time**: Minimum time between consecutive SPF computations (default 5 seconds).

Faster convergence requires shorter timers, but increases control traffic.

### Flooding Reliability

LSAs must be reliably delivered. OSPF uses:
- **Explicit Acknowledgment**: LSACKs confirm LSU reception.
- **Retransmission**: If no ACK received within timeout, LSU is resent.
- **Sequence Number Detection**: Duplicates (same seq_num) are acknowledged but not reprocessed.

## Related Concepts

- [[Distance_Vector_Routing]]: Contrasting distributed routing paradigm.
- [[Unicast_Routing_Overview]]: Routing fundamentals and forwarding.
- [[Hierarchical_Routing]]: OSPF's area hierarchy for scalability.
- [[AODV_Route_Discovery_Simulation]]: Link-state principles in on-demand ad hoc routing.

---

**Next:** [[Hierarchical_Routing_Examples_and_Simulations]]
