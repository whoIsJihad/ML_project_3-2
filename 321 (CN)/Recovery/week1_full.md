# Week 1: Network Fundamentals & OSI Model

## 1. What is a Computer Network?

A computer network connects multiple devices (computers, routers, switches) using cables or wireless links.

**Key Components:**
- **End Systems**: Your laptop, phone, server
## 11. Dijkstra's Algorithm: How It Applies to Routing

Dijkstra (the Shortest Path First, SPF) is used by link-state routing protocols (notably OSPF and IS-IS). In routing the algorithm is applied locally by each router to a complete topology view (the Link State Database) to build a shortest-path tree rooted at that router.

How costs are compared
- Each link has a cost (metric). The cost of a path is the sum of its link costs. Metrics can reflect delay, inverse bandwidth, monetary cost, or admin preference.
- When comparing paths, routers sum link metrics; the path with the lowest total is chosen. Ties can be handled with equal-cost multipath (ECMP) or deterministic tiebreakers (router ID, interface order).

Link-State (LSA) and the Link State Database (LSDB)
- Routers advertise their local connectivity using Link State Advertisements (LSAs). Typical LSA types include router LSAs (list of links), network LSAs (multi-access networks), summary LSAs (area summaries), and AS-external LSAs (external routes).
- LSAs are flooded reliably to all routers in the area; each router stores them in the LSDB. After flooding completes, all routers in the area should have identical LSDBs.

Convergence process (high-level)
1. Topology change detected (link up/down, neighbor loss).
2. The impacted router originates a fresh LSA (incremented sequence number) describing the change.
3. The LSA is flooded to all routers in the area; reliable flooding uses ACKs and retransmissions.
4. Each router updates its LSDB and runs SPF (Dijkstra) to recompute the shortest-path tree.
5. Routing tables (RIB) are updated and next-hops are programmed into the forwarding table (FIB).

Factors affecting convergence time
- Detection latency (how fast a router notices a failure).
- LSA flooding time across the area (network diameter, link speeds).
- SPF computation time (depends on topology size and algorithm optimizations).
- Rate-limiting or LSA throttling configuration (prevents flapping but slows convergence).

Loop-free routing and transient loops
- Link-state routing is loop-free once all routers have the same LSDB and have completed their SPF computation, because each router computes a deterministic shortest-path tree from the same topology.
- Transient loops can occur during convergence while LSDBs differ or before SPF runs on all routers. Mitigations include fast flooding, incremental SPF (recompute only affected nodes), LSA sequence numbers/ageing, and careful timer tuning.

Scaling and operational techniques
- Complexity: SPF runs in roughly O(E + N log N) with a binary heap (E = edges, N = nodes). CPU and memory grow with topology size (more LSAs, larger LSDB, longer SPF time).
- Hierarchy: OSPF uses areas to limit LSDB size and SPF scope; area border routers (ABRs) summarise routes between areas.
- Aggregation & summarization: reduces LSDB and routing table size at area boundaries.
- Incremental SPF and SPF pacing: recompute only affected portions and pace SPF runs to avoid CPU storms during flaps.

From SPF to forwarding
- After SPF computes next-hops, routers build the RIB and populate the FIB. Equal-cost multiple next-hops may be inserted for load-sharing (ECMP).

In short: Dijkstra provides the per-router computation; LSAs provide the global topology input; practical routing design deals with LSA flooding, convergence timers, hierarchy (areas), and SPF optimizations to keep routing loop-free and scalable.
**Real-World Example:**  
The Internet uses IP (connectionless). When you request a webpage, each packet finds its own way to you. Some might go through New York, others through Chicago.

**Use Cases:**
- Web browsing (HTTP)
- Email (SMTP)
- DNS queries
- Short transactions

### Connection-Oriented (Virtual Circuit) - Like Phone Calls

**How It Works:**
1. **Setup Phase**: Establish a path before sending data
2. **Data Transfer**: All packets follow the same path using a circuit ID
3. **Teardown**: Close the connection when done

**Pros:**
-  Quality of Service (QoS) guarantees
-  Resources reserved in advance
-  Easier congestion control
-  Packets arrive in order
-  Lower per-packet overhead

**Cons:**
-  Setup time required
-  If router fails, connection breaks
-  Resources wasted if circuit is idle
-  Less flexible to network changes
**Real-World Example:**  
ATM networks (used in older telecom infrastructure). Before data flows, a virtual circuit is established. It's like reserving a dedicated lane on a highway.

**Use Cases:**
- Voice calls (need consistent quality)
- Video streaming (need guaranteed bandwidth)
- Financial transactions (need reliability)

### When to Use Which?

| Scenario | Best Choice | Reason |
|----------|-------------|--------|
| Web browsing, short requests | Connectionless (IP) | No setup delay, efficient for bursty traffic |
| Live video streaming | Connection-Oriented (or TCP over IP) | Need guaranteed bandwidth |
| File downloads | Connectionless with TCP | Flexibility + reliability through TCP |
| Voice calls (VoIP) | Connection-Oriented or UDP | Consistent quality needed |

---

## 8. Routing Algorithms: Finding the Best Path

Routing is about finding the optimal path from source to destination.

### Key Concepts

**Metric**: How we measure "best"
- Number of hops (shortest)
- Delay (fastest)
- Bandwidth (highest capacity)
- Cost (cheapest)
- Reliability (most stable)

**Optimality Principle:**  
If router J is on the optimal path from I to K, then the path from J to K must also be optimal.

**Why?** If there were a better path from J to K, we'd use it instead!

**Sink Tree**: A tree showing optimal paths from all sources to one destination. It's always loop-free.

#### Example: Sink Tree for Node A
```

Network Graph:
    B --- D
   /|     |
  A |     |
   \|     |
    C --- E

Optimal paths TO node A:
- B → A (direct)
- C → A (direct)
- D → B → A
- E → C → A

This forms a tree with A at the root (sink).
```

### Conflicting Metrics: The Trade-offs

Real networks must balance competing goals.

| Conflict | Problem | Real-World Impact |
|----------|---------|-------------------|
| **Fairness vs. Optimality** | Maximizing total throughput may starve some users | Your video call lags while others download files |
| **Delay vs. Throughput** | High utilization = long queues = more delay | Fast internet but high ping in games |
| **Cost vs. Performance** | Cheapest path may be slower | Your ISP routes through congested links to save money |

**Solution Approaches:**
- **Weighted metrics**: Balance multiple factors (e.g., 0.5×delay + 0.5×cost)
- **QoS policies**: Prioritize certain traffic (voice over email)
- **Load balancing**: Distribute traffic across multiple paths

---

## 9. Types of Routing Algorithms

### Static (Non-Adaptive) Routing

**Definition**: Routes are fixed. They don't change based on network conditions.

**How it works:**
- Routes computed manually or offline
- Loaded into routers at startup
- Stay the same until manually changed

**Pros:**
-   Simple to implement
-   Predictable behavior
-   No overhead for route updates
-   Works well in stable networks

**Cons:**
-   Cannot adapt to failures
-   Cannot balance load dynamically
-   Requires manual updates
-   Inefficient if network changes

**Real-World Use:**
- Small networks with few routers
- Backup routes
- IoT devices with simple connectivity

### Adaptive (Dynamic) Routing

**Definition**: Routes change automatically based on network conditions.

**How it works:**
- Routers exchange information
- Algorithms recalculate routes
- Adapts to failures and congestion

**Pros:**
-   Handles failures automatically
-   Adapts to congestion
-   Optimal routes in changing conditions
-   No manual intervention needed

**Cons:**
-   More complex to implement
-   Overhead from route updates
-   Possible routing loops
-   Convergence time issues

**Real-World Use:**
- The entire Internet
- Large enterprise networks
- Dynamic networks (mobile, wireless)

---

## 10. Flooding: The Simplest Routing Algorithm

### How Flooding Works

**Rule**: When a packet arrives, send it out on ALL links EXCEPT the one it came from.

**Example:**
```
Router A receives a packet on Link 1.
Router A has 4 links (1, 2, 3, 4).
Router A sends copies on Links 2, 3, and 4.
```

**Visualization:**
```
Step 1: Source S sends packet
        S
       /|\
      1 2 3
      
Step 2: All neighbors forward to their neighbors
        S
       /|\
      A B C
     /|  |\ 
    D E  F G

Packets multiply exponentially!
```

### Pros of Flooding

| Advantage | Explanation |
|-----------|-------------|
|   **Guaranteed Delivery** | If any path exists, packet will reach destination |
|   **Extremely Robust** | Works even if many routers fail |
|   **No Routing Tables** | No need to store or compute routes |
|   **Finds Shortest Path** | First packet to arrive took the shortest route |

### Cons of Flooding

| Disadvantage | Explanation | Impact |
|--------------|-------------|--------|
|   **Massive Overhead** | Exponential packet multiplication | Network overwhelmed with duplicates |
|   **Wastes Bandwidth** | Same packet sent everywhere | Inefficient use of network capacity |
|   **Loops Forever** | Packets can circulate indefinitely | Without controls, network crashes |

### The Problem: Packet Explosion

**Example Network:**
- 10 routers
- Each router has 3 links
- One packet sent

**Without controls:**
- Round 1: 3 copies
- Round 2: 9 copies
- Round 3: 27 copies
- Round 4: 81 copies
- Grows exponentially!

### Solutions to Control Flooding

#### Solution 1: Hop Count (TTL - Time To Live)

**How it works:**
1. Add a hop counter to each packet (e.g., TTL = 64)
2. Each router decrements the counter
3. When counter reaches 0, discard the packet

**Example:**
```
Packet starts: TTL = 5
Router A: TTL = 4 (forward)
Router B: TTL = 3 (forward)
Router C: TTL = 2 (forward)
Router D: TTL = 1 (forward)
Router E: TTL = 0 (DISCARD)
```

**Pros:**
-   Simple to implement
-   Prevents infinite loops

**Real-World:**
- IPv4 uses TTL (typically 64 or 128)
- `ping` command shows TTL: "64 bytes from google.com: icmp_seq=1 ttl=117"
- `traceroute` uses TTL to map network paths

#### Solution 2: Sequence Numbers

**How it works:**
1. Each packet gets a unique (Source, Sequence Number) pair
2. Each router remembers which (Source, Seq#) it has seen
3. If packet arrives with a seen (Source, Seq#), discard it

**Example:**
```
Source A sends Packet #123

Router B receives (A, #123) → First time, forward it & remember
Router B receives (A, #123) again → Already seen, discard
```

**Pros:**
-   Prevents duplicate processing
-   More efficient than hop count alone

**Cons:**
-   Routers must store history
-   Memory requirements grow
-   Must age out old entries

**Real-World:**
- TCP uses sequence numbers to detect duplicates
- Link-state routing protocols use sequence numbers

#### Solution 3: Selective Flooding

**How it works:**
Only forward packets on links that go approximately toward the destination.

**Example:**
```
Network:
    North
      |
West--R--East
      |
    South

Destination is East.
Router R only forwards on East link, not North/South/West.
```

**Pros:**
-   Reduces packet explosion
-   Still robust to failures

**Cons:**
-   Requires some routing knowledge
-   More complex logic

**Real-World Use:**
- Broadcast in wireless networks
- Multicast routing protocols
- Emergency routing during failures

### When Flooding is Actually Used

Despite inefficiency, flooding has legitimate uses:

| Use Case | Why Flooding? |
|----------|---------------|
| **Military Networks** | Extreme robustness needed; bandwidth less important |
| **Network Discovery** | Find all devices (ARP, DHCP discovery) |
| **Routing Protocol Bootstrap** | Initially discover neighbors (OSPF, IS-IS) |
| **Emergency Mode** | When routing tables are corrupted or lost |

---

📝 **See detailed routing deep dive:** [[Dijkstra and OSPF - Deep Dive]]

---

## Summary: Week 1 Key Takeaways

  **Layering** organizes complex networking into manageable layers  
  **OSI Model** provides a 7-layer framework (though real Internet uses TCP/IP)  
  **Connectionless** (IP) is flexible; **Connection-Oriented** (Virtual Circuits) guarantees quality  
  **Routing Metrics** involve trade-offs (delay vs. throughput, fairness vs. optimality)  
  **Flooding** is robust but inefficient; controlled with TTL and sequence numbers  
  **Dijkstra's Algorithm** finds optimal paths; used by OSPF

**Next Week Preview**: Distance Vector Routing, Link State Routing, RIP vs. OSPF