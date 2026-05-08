# Distance Vector Routing

## Definition and Concept

**Distance Vector Routing** is a decentralized routing algorithm where:
- Each router maintains a **vector** (table) of distances (costs) to all known destinations
- Routers exchange their distance vectors with **directly connected neighbors** periodically
- Each router updates its own distances based on information from neighbors
- Routes are computed using the **Bellman-Ford algorithm principle**

The term "distance vector" comes from the data structure: a vector indexed by destination, where each entry is the distance to that destination.

## Bellman-Ford Algorithm Principle

The foundation of distance vector routing is the **Bellman-Ford equation**:

$$D_x(y) = \min_v \{ c(x,v) + D_v(y) \}$$

**Where:**
- $D_x(y)$ = Distance from node $x$ to node $y$ (computed at node $x$)
- $c(x,v)$ = Cost of direct link from $x$ to neighbor $v$
- $D_v(y)$ = Distance from $v$ to $y$ (learned from $v$'s distance vector advertisement)
- $\min_v$ = Minimum over all neighbors $v$ of $x$

**Interpretation:** To reach destination $y$ from $x$, consider going through each neighbor $v$. The path cost is the cost to reach $v$ plus the distance from $v$ to $y$. Choose the neighbor that gives the minimum total cost.

## Distance Vector Algorithm

### Formal Algorithm

**At router $x$, for each destination $y$:**

```
Algorithm: DistanceVectorRouting(router_x)
Input: Current distance vector D_x
Periodic event (e.g., every 30 seconds):

1. For each neighbor v of x:
   2. Send distance vector D_x to neighbor v
      (Contains: D_x(y) for all destinations y)

Upon receiving distance vector D_v from neighbor v:

3. For each destination y in the network:
   4. D_x_new(y) = min( D_x(y), c(x,v) + D_v(y) )
   5. If D_x_new(y) < D_x(y):
      a. D_x(y) = D_x_new(y)
      b. next_hop_to_y = v
      c. Schedule update advertisement (or wait for periodic timer)

6. If any distance decreased: announce new distance vector
   (Some algorithms send immediately, some wait for periodic timer)
```

### Algorithm Properties

**Distributed:**
- No single point of computation
- Each router independently updates based on information from neighbors
- No centralized routing authority needed

**Asynchronous:**
- Routers update at independent times
- No global synchronization required
- Messages can arrive out of order

**Iterative:**
- Routes are computed iteratively
- After $k$ iterations, each router has the correct distance to destinations reachable in $k$ hops
- Convergence takes time: $O(n)$ in best case, where $n$ = number of routers

## Step-by-Step Example: Network Convergence

### Network Topology

```mermaid
graph LR
    A -- 1 --- B
    B -- 1 --- C
    C -- 1 --- D
```

**Link costs:** Each link has cost 1. Routers form a linear topology: A-B-C-D.

**Initially:** Each router knows only its direct neighbors (cost = 0 for itself, cost = ∞ for unreachable)

### Iteration 0 (Initial State)

At time $t=0$, each router knows only itself and direct neighbors:

**Router A's distance vector:**
```
A  B  C  D
0  1  ∞  ∞
```

**Router B's distance vector:**
```
A  B  C  D
1  0  1  ∞
```

**Router C's distance vector:**
```
A  B  C  D
∞  1  0  1
```

**Router D's distance vector:**
```
A  B  C  D
∞  ∞  1  0
```

### Iteration 1

After first exchange of distance vectors (A and B exchange, B and C exchange, C and D exchange):

**Router A receives from B: [1, 0, 1, ∞]**
- Distance to A: min(0, 1+1) = 0
- Distance to B: min(1, 1+0) = 1
- Distance to C: min(∞, 1+1) = 2 ← **Updated**
- Distance to D: min(∞, 1+∞) = ∞

**Router A's updated distance vector:**
```
A  B  C  D
0  1  2  ∞
```

**Router B receives from A: [0, 1, ∞, ∞] and from C: [∞, 1, 0, 1]**
- From A: Distance to C: min(1, 1+∞) = 1 (no change)
- From C: Distance to D: min(∞, 1+1) = 2 ← **Updated**

**Router B's updated distance vector:**
```
A  B  C  D
1  0  1  2
```

**Router C receives from B: [1, 0, 1, ∞] and from D: [∞, ∞, 1, 0]**
- From B: Distance to A: min(∞, 1+1) = 2 ← **Updated**
- From D: Distance to C: min(0, 1+1) = 0 (no change)

**Router C's updated distance vector:**
```
A  B  C  D
2  1  0  1
```

**Router D receives from C: [∞, 1, 0, 1]**
- Distance to A: min(∞, 1+∞) = ∞
- Distance to B: min(∞, 1+1) = 2 ← **Updated**
- Distance to C: min(1, 1+0) = 1
- Distance to D: min(0, 1+1) = 0 (no change)

**Router D's updated distance vector:**
```
A  B  C  D
∞  2  1  0
```

### Iteration 2

Continuing the process:

**Router A receives from B: [1, 0, 1, 2]**
- Distance to D: min(∞, 1+2) = 3 ← **Updated**

**Router A's updated distance vector:**
```
A  B  C  D
0  1  2  3
```

**Router D receives from C: [2, 1, 0, 1]**
- Distance to A: min(∞, 1+2) = 3 ← **Updated**

**Router D's updated distance vector:**
```
A  B  C  D
3  2  1  0
```

### Iteration 3 and Beyond

All routers now have converged to the correct shortest paths. No more updates occur.

**Final distance vectors (converged):**

| Router | A | B | C | D |
|---|---|---|---|---|
| A | 0 | 1 | 2 | 3 |
| B | 1 | 0 | 1 | 2 |
| C | 2 | 1 | 0 | 1 |
| D | 3 | 2 | 1 | 0 |

**Observation:** Convergence took 3 iterations for a 4-node network. In general, convergence takes $O(n)$ iterations in the best case.

## Routing Tables After Convergence

Each router maintains a routing table derived from its distance vector:

**Router A's routing table:**
```
Destination | Distance | Next Hop
A           | 0        | Direct
B           | 1        | B
C           | 2        | B
D           | 3        | B
```

**Router B's routing table:**
```
Destination | Distance | Next Hop
A           | 1        | A
B           | 0        | Direct
C           | 1        | C
D           | 2        | C
```

**Router C's routing table:**
```
Destination | Distance | Next Hop
A           | 2        | B
B           | 1        | B
C           | 0        | Direct
D           | 1        | D
```

**Router D's routing table:**
```
Destination | Distance | Next Hop
A           | 3        | C
B           | 2        | C
C           | 1        | C
D           | 0        | Direct
```

## Count-to-Infinity Problem

A critical flaw in basic distance vector routing is the **count-to-infinity problem**.

### Scenario: Link Failure

**Original converged network:**
```
A ——— B ——— C
  1     1
```

**A's distance vector:** [0, 1, 2]
**B's distance vector:** [1, 0, 1]
**C's distance vector:** [2, 1, 0]

**What happens if link B-C fails?**

**Step 1:** B detects link failure (no response from C)
- B sets distance to C as ∞

**Step 2:** But B still has A's distance vector [0, 1, 2]
- B thinks: "C is reachable via A with distance 1+2=3"
- B updates: distance_to_C = 3

**Step 3:** Next exchange, A gets B's new vector [1, 0, 3, ∞]
- A thinks: "Distance to C = 1 + 3 = 4"
- A updates: distance_to_C = 4

**Step 4:** B gets A's vector [0, 1, 4, ...]
- B thinks: "Distance to C = 1 + 4 = 5"

**This continues indefinitely:** 3 → 4 → 5 → 6 → ... → ∞

The distance keeps increasing until it reaches the maximum metric (infinity).

### Solution 1: Maximum Metric / Infinity Definition

In RIP:
- Maximum metric = 15
- After 16 hops, distance is considered infinite
- Results in A-B-C-...-Z taking ~30 seconds to fully converge after a failure

**Problem:** Works only for small networks; limits network diameter to 15 hops

### Solution 2: Split Horizon with Poison Reverse

**Split Horizon Rule:** A router doesn't advertise a route back through the interface from which it learned that route.

**Poison Reverse:** When a route becomes unreachable, explicitly advertise it with infinite metric to neighbors from whom it was learned.

**Example:**

**Original state:**
- B-C link is up
- A advertises: [0, 1, 2]
- B advertises back to A: [1, 0, 1] (with split horizon, doesn't advertise C back)
- C advertises: [2, 1, 0]

**When B-C fails:**
- B detects failure, sets distance to C = ∞
- **B advertises to A:** [1, 0, ∞] (poison reverse: explicitly send ∞)
- A immediately learns C is unreachable via B

This prevents the count-to-infinity problem in most cases.

**Limitation:** Poison reverse only works for failures with 2 hops. For longer loops, other mechanisms like hold-down timers are needed.

## Examples: RIP (Routing Information Protocol)

RIP is a practical implementation of distance vector routing.

### RIP Characteristics

| Aspect | Value |
|---|---|
| **Protocol type** | Distance vector |
| **Metric** | Hop count (0-15, where 16 = ∞) |
| **Maximum network size** | 15 hops (diameter ≤ 14 routers) |
| **Update interval** | 30 seconds (periodic) |
| **Invalid timer** | 180 seconds (no update = unreachable) |
| **Versions** | RIPv1 (classful), RIPv2 (classless/CIDR) |

### RIP Message Format

A RIP update message contains:

```
RIP Header:
  Command: 1 (request) or 2 (response)
  Version: 1 or 2
  
RIP Entries (up to 25 per message):
  Route Tag: 0 (for internal routes)
  IP Address: Destination network address
  Subnet Mask: Network mask (RIPv2 only)
  Next Hop: Next-hop IP (RIPv2 only)
  Metric: 1-15 (hop count)
```

### RIP Operation

**Periodic Updates (every 30 seconds):**
1. Router sends its entire distance vector to all neighbors on RIP-enabled interfaces
2. Neighbors receive the message
3. Each neighbor updates its own distance vector using Bellman-Ford equation

**Triggered Updates:**
- If a route changes (e.g., failure detected), send update immediately
- Don't wait for next periodic timer

**Convergence:**
- Convergence time: roughly (network diameter) × 30 seconds
- Example: In a 15-hop network, convergence takes ~450 seconds = 7.5 minutes

## Practical Example: RIP Configuration and Simulation

### Linux RIP Simulation Using GNS3 or Cisco Simulator

```bash
# On Router A
configure terminal
router rip
  version 2
  network 10.0.0.0
  network 192.168.1.0
  no auto-summary

# View routing table
show ip route
show ip rip database

# On Router B (similar)
configure terminal
router rip
  version 2
  network 10.0.0.0
  network 192.168.2.0
  no auto-summary
```

### Observing Convergence

```bash
# Watch distance vector updates (debugging)
debug ip rip

# You'll see messages like:
# RIPv2: Sending update to 224.0.0.9 (multicast) on FastEthernet0/0
# RIPv2: Received v2 update from 192.168.1.2 on FastEthernet0/0
# RIPv2: added 10.2.0.0/16 (via 192.168.1.2 with metric 2)

# Check convergence completion
show ip route | include connected
```

## Comparing Distance Vector Routing

### Advantages
- Simple to implement and understand
- Minimal processing power required
- Works well in small networks
- Decentralized—no single point of failure

### Disadvantages
- Slow convergence (minutes in large networks)
- Routing loops during convergence
- Count-to-infinity problem requires complex solutions
- Frequent periodic updates consume bandwidth
- Routing decisions based only on distance, not other factors (delay, reliability)
- Doesn't scale to very large networks

### When to Use
- Small networks (< 15 hops)
- Simple, stable topologies
- Limited CPU/memory available
- RIP is legacy; modern networks use OSPF or EIGRP

---

## Next Steps

- [[Link_State_Routing]] — Compare with faster convergence method
- [[Bellman-Ford_Algorithm_Detailed]] — Deep dive into algorithm mathematics
- [[Hierarchical_Routing]] — Scaling to large networks
