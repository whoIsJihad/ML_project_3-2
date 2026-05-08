# Hierarchical Routing Examples and Simulations

## Introduction

Hierarchical routing reduces routing table size and control traffic overhead by organizing networks into multiple levels. Instead of each router maintaining routes to every destination globally, routers maintain detailed routes only within their domain and aggregated routes to other domains.

This note provides detailed examples and step-by-step simulations of hierarchical routing in realistic network topologies.

## Assumptions and Prerequisites

Familiarity with:
- [[Link_State_Routing]]: Dijkstra's algorithm and OSPF concepts.
- [[Hierarchical_Routing]]: Domain aggregation and multi-level routing.
- Graph theory: Weighted graphs and shortest path computation.

## Example 1: Three-Area OSPF Network

### Network Topology

Consider an enterprise network divided into three OSPF areas:

```
                 Area 0 (Backbone)
            ┌──────────────────────┐
            │                      │
          R1A ────────── R2A ────────R3A
          /  \            |          /  \
        5    10          5         10    8
        /      \          |          \    \
       R4       R1B ──────R2B ──────R3B   R3C
      Area 1             Area 0        Area 2
```

**Network Details**:

**Area 0 (Backbone)**:
- $R1A$ (ABR): Interface to Area 1, Interface to Area 0
- $R2A$ (Backbone Router): Backbone interfaces
- $R3A$ (ABR): Interface to Area 0, Interface to Area 2
- Link costs:
  - $(R1A, R2A)$: 5
  - $(R2A, R3A)$: 8

**Area 1**:
- $R1B$ (Internal Router): One interface in Area 1
- $R4$ (Internal Router): One interface in Area 1
- Link costs:
  - $(R1A, R1B)$: 10
  - $(R1A, R4)$: 5

**Area 2**:
- $R3B$ (Internal Router): One interface in Area 2
- $R3C$ (Internal Router): One interface in Area 2
- Link costs:
  - $(R3A, R3B)$: 10
  - $(R3A, R3C)$: 8

### Routing Table Computation

#### Step 1: Intra-Area Routing (Area 1)

Using Dijkstra's algorithm within Area 1 from $R1B$:

| Destination | Next Hop | Cost | Path |
|---|---|---|---|
| $R1B$ | Direct | 0 | - |
| $R1A$ | $R1A$ | 10 | $R1B - R1A$ |
| $R4$ | $R1A$ | 5+5=10 | $R1B - R1A - R4$ |

**Routing Table at $R1B$**:

```
Destination     Next Hop        Cost
Direct (R1B)    Local           0
R1A (ABR)       R1A             10
R4              R1A             15
```

#### Step 2: Intra-Area Routing (Area 2)

Using Dijkstra's algorithm within Area 2 from $R3B$:

| Destination | Next Hop | Cost | Path |
|---|---|---|---|
| $R3B$ | Direct | 0 | - |
| $R3A$ | $R3A$ | 10 | $R3B - R3A$ |
| $R3C$ | $R3A$ | 8+8=16 | $R3B - R3A - R3C$ |

**Routing Table at $R3B$**:

```
Destination     Next Hop        Cost
Direct (R3B)    Local           0
R3A (ABR)       R3A             10
R3C             R3A             18
```

#### Step 3: Inter-Area Routing (via ABR Summaries)

ABR $R1A$ summarizes Area 1's routes for Area 0 backbone. It originates an "Inter-Area Route Advertisement" (in OSPF, an Inter-Area Prefix LSA) indicating:

- Area 1 can reach subnets behind $R1A$, $R1B$, $R4$ with internal costs.
- Cost from ABR $R1A$ to Area 1's destinations:
  - To $R1B$: 10
  - To $R4$: 5

ABR $R1A$ advertises to Area 0:
- Route to Area 1 region, aggregate cost 10 (typical example; actual cost depends on origination cost + internal distance)

**Backbone (Area 0) Routing Table at $R2A$**:

Using Dijkstra's algorithm in Area 0:

| Destination | Next Hop | Cost | Path |
|---|---|---|---|
| $R2A$ | Direct | 0 | - |
| $R1A$ | $R1A$ | 5 | $R2A - R1A$ |
| $R3A$ | $R3A$ | 8 | $R2A - R3A$ |
| Area 1 (via $R1A$) | $R1A$ | 5+10=15 | $R2A - R1A$ (then via $R1A$ into Area 1) |
| Area 2 (via $R3A$) | $R3A$ | 8+10=18 | $R2A - R3A$ (then via $R3A$ into Area 2) |

#### Step 4: Full Routing Table at $R1B$ (with Inter-Area Routes)

$R1B$ learns inter-area routes through ABR $R1A$:

```
Destination          Next Hop        Cost         Type
Direct (R1B)         Local           0            Intra-area (Area 1)
R1A (ABR in Area 1)  R1A             10           Intra-area (Area 1)
R4 (Area 1)          R1A             15           Intra-area (Area 1)

Area 0 Routers       R1A             5+5=10      Inter-area (via ABR)
  (R1A, R2A, R3A)                               
Area 2 Routers       R1A             5+5+8+10    Inter-area (via ABR and backbone)
  (R3B, R3C)                      =28
```

**Explanation**: To reach Area 2 from $R1B$, the path is:
- $R1B$ → $R1A$ (10 cost, within Area 1)
- $R1A$ → $R2A$ (5 cost, backbone)
- $R2A$ → $R3A$ (8 cost, backbone)
- $R3A$ → Area 2 (10 cost, within Area 2)
- **Total**: 10 + 5 + 8 + 10 = 33 (not 28; corrected calculation below)

**Corrected Routing Table at $R1B$**:

```
Destination          Next Hop        Cost         Type
Direct (R1B)         Local           0            Intra-area
R1A                  R1A             10           Intra-area
R4                   R1A             15           Intra-area
R2A (backbone)       R1A             10+5=15      Inter-area
R3A (backbone)       R1A             10+5+8=23    Inter-area
R3B (Area 2)         R1A             10+5+8+10=33 Inter-area
```

### Routing Table Size Reduction

**Without Hierarchical Routing** (flat network with $N=10$ routers):
- Each router maintains explicit routes to 10 destinations.
- Total entries: 10 routers × 10 destinations = 100 entries globally.

**With Hierarchical Routing** (three areas):
- Each router maintains:
  - Intra-area routes (~3-5 destinations within area)
  - Inter-area summary routes (≤3 destinations, summarized by area)
- Total entries per router: ~5-8 entries.
- Total entries globally: 10 routers × 7 entries = 70 entries (30% reduction).

**Scaling Benefit**: With $N=100$ routers divided into 10 areas:
- Flat: 100 × 100 = 10,000 entries.
- Hierarchical: 100 × 15 = 1,500 entries (85% reduction).

## Example 2: Multi-Tier Hierarchical Routing (3 Levels)

### Topology: ISP with Regional Structure

```
                    Tier 1: Global Backbone
              ┌──────────────────────────────┐
              │                              │
          [Chicago BGP1]             [NewYork BGP1]
          /              \          /              \
         /                \        /                \
    [Chicago              [Chicago            [NewYork
     Area1]               Area2]              Area1]
     │                    │                   │
   [C1_R1]  [C1_R2]    [C2_R1]  [C2_R2]   [N1_R1] [N1_R2]
    10ms                 8ms                  12ms
```

**Hierarchy**:
- **Tier 1**: BGP routers interconnecting cities (BGP1 = Border Gateway Protocol router).
- **Tier 2**: Regional OSPF areas (Chicago Area 1 & 2, New York Area 1).
- **Tier 3**: Individual routers within areas.

### Routing Decision at Different Tiers

**At Tier 3 Router (C1_R1 in Chicago Area 1)**:
- Destination in same area (C1_R2): Direct OSPF route, cost 10 ms.
- Destination in Chicago Area 2 (C2_R1): Route to ABR, then to C2_R1, cost ~20 ms.
- Destination in New York Area 1 (N1_R1): Route to Area 1 ABR → Tier 2 (Chicago BGP1) → Tier 1 (backbone) → Tier 2 (NewYork BGP1) → New York Area 1, cost ~150 ms.

**Routing Decision at BGP1 (Chicago)**:
- BGP considers policies in addition to shortest path.
- May prefer expensive route for policy reasons (e.g., avoid congested links).
- Uses Tier 1 aggregated routes: "Chicago has CIDR 10.1.0.0/16", "New York has CIDR 10.2.0.0/16".

**Aggregation at BGP1**:
```
Chicago announces to backbone: "I control 10.1.0.0/16"
  (instead of listing 200 individual subnets within Chicago)
```

### Tier 1 Routing Table at Chicago BGP1

```
Destination            Next Hop         Cost    Type
Local Chicago Area     Direct           0       Intra-tier (via OSPF)
New York (10.2.0.0/16) NewYork BGP1    150ms   Inter-tier (via BGP)
Other Regions          Tier1-Router     200ms+  Inter-tier (via BGP)
```

### Hierarchical Forwarding Decision

A packet from C1_R1 destined for N1_R1 (address 10.2.1.50):

1. **At C1_R1 (Tier 3, Area 1)**:
   - Check local OSPF routing table.
   - No exact match; check if 10.2.1.50 is in Area 2 or elsewhere.
   - Not in local area; forward to ABR (area border router).

2. **At Area 1 ABR** (still Tier 3, but ABR):
   - Check if 10.2.1.50 is in OSPF inter-area routes.
   - Not found; forward to Chicago BGP1 (Tier 2/Tier 1 boundary).

3. **At Chicago BGP1** (Tier 2):
   - Check BGP routing table.
   - Match: 10.2.0.0/16 → Next Hop: New York BGP1.
   - Forward to New York BGP1.

4. **At New York BGP1** (Tier 2):
   - Receive packet destined for 10.2.1.50 (New York's CIDR space).
   - Check local routes; 10.2.1.50 is within New York Area 1.
   - Forward to Area 1 router (via OSPF).

5. **At N1_R1** (Tier 3, Area 1):
   - Deliver packet.

**Total Hops**: C1_R1 → Area 1 ABR → Chicago BGP1 → New York BGP1 → Area 1 ABR → N1_R1 (6 hops).

## Example 3: Failure Recovery in Hierarchical Networks

### Scenario: Link Failure in Area 1

**Topology before failure**:

```
     Chicago ABR
         |
        5ms
         |
      [C1_R1]---10ms---[C1_R2]
         |               |
         └───20ms────────┘
```

**Routes from C1_R1** (before failure):
- To C1_R2: Direct (10 ms) [primary]
- To C1_R2: Via Chicago ABR (5+5=10 ms) [backup, equal cost]

At $t=0$, the direct link (C1_R1)----(C1_R2) fails.

**Recovery Timeline**:

| Time | Event | Router Action | Packets |
|---|---|---|---|
| $t=0$ | Link C1_R1 - C1_R2 fails | Interface down; HELLO timeout starts | Backlog |
| $t=5$ | C1_R1 detects loss (HELLO timeout) | Purge C1_R2 from LSDB; initiate SPF | Reroute via ABR |
| $t=7$ | SPF completes at C1_R1 | Next hop to C1_R2 = Chicago ABR | Forwarding updates |
| $t=8$ | C1_R1 receives updated LSAs from C1_R2 | C1_R2 also updates its routes | Both routers converged |

**Packets affected**: Those transmitted between $t=0$ and $t=7$ are either dropped or rerouted through the ABR.

### Convergence Time Analysis

Convergence time consists of:
1. **Failure detection** (30-40 seconds typical, 5-10 seconds with BFD): $t_{\text{detect}}$
2. **LSA origination** (immediate): $t_{\text{orig}}$
3. **LSA flooding within area** (< 1 second): $t_{\text{flood}}$
4. **SPF computation** (< 1 second): $t_{\text{spf}}$
5. **ABR route propagation** (if inter-area, add ~1-2 seconds)

**Total**: ~5-10 seconds with BFD (Bidirectional Forwarding Detection), ~30-50 seconds without.

## Example 4: Load Balancing in Hierarchical Networks

### Equal-Cost Multi-Path (ECMP) Routing

When multiple paths have equal cost, routers use ECMP to distribute traffic across all paths.

**Scenario**: Two equal-cost paths from C1_R1 to C1_R2.

```
C1_R1 ──10ms── C1_R2
  \           /
   └──5ms──ABR──5ms──┘
```

**Costs**:
- Direct: 10 ms
- Via ABR: 5 + 5 = 10 ms (equal cost)

**ECMP forwarding at C1_R1**:
```
When sending to C1_R2:
  - If hash(source, destination) mod 2 == 0:
      Forward via direct link
  - Else:
      Forward via ABR
```

This distributes traffic 50/50 between paths, improving throughput and resilience.

## Example 5: Anycast Routing

Hierarchical routing enables anycast services where multiple instances of a service are deployed across different areas, and clients are routed to the nearest one.

**Scenario**: DNS service deployed at:
- C1_DNS (Chicago Area 1): IP 10.1.1.1
- C2_DNS (Chicago Area 2): IP 10.1.1.1 (same IP, different location)
- N1_DNS (New York Area 1): IP 10.1.1.1 (same IP, different location)

**Routing**:
- From C1_R1: Route to 10.1.1.1 → C1_DNS (0 hops, same area, cost 5 ms)
- From C2_R1: Route to 10.1.1.1 → C2_DNS (via ABR, cost ~10 ms)
- From N1_R1: Route to 10.1.1.1 → N1_DNS (via ABR and backbone, cost ~150 ms)

**Result**: Each client automatically reaches the nearest DNS instance.

## Practical Considerations

### Area Design Guidelines

1. **Area Size**: Keep intra-area routers between 50-200. Larger areas increase SPF computation overhead.
2. **Area Interconnection**: All areas must connect to Area 0 (backbone). Creating direct inter-area links violates OSPF rules.
3. **Stub Areas**: Mark areas that have no ASBRs as "stub" to prevent external route flooding.

### Stub Area Example

```
         Area 0 (Backbone)
             [R1]
              |
          [ABR to Area 1]
              |
           Area 1 (Stub)
             [R2]
```

In Area 1 (stub area):
- R2 doesn't receive AS-external routes (routes from outside the OSPF domain).
- R2 uses a default route (0.0.0.0/0) to reach external networks via the ABR.
- **Benefit**: Reduces LSDB size in Area 1 by ~90% (no external route advertisements).

### Scaling Example

**Network with 5000 routers**:

**Flat OSPF** (no areas):
- Each router maintains LSDB with 5000 entries.
- SPF computation: $O(5000 + \text{links})$ per change.
- Very high control traffic and CPU overhead.

**Hierarchical OSPF** (100 areas, 50 routers per area):
- Each router maintains LSDB with 50 entries (intra-area) + 100 entries (inter-area summary) = 150 entries.
- SPF computation: $O(50 + \text{links per area})$ per change.
- Control traffic reduced by 95%.
- CPU overhead reduced by 98%.

## Related Concepts

- [[Link_State_Routing]]: OSPF foundation and Dijkstra's algorithm.
- [[Broadcast_Routing]]: Area flooding mechanisms.
- [[Unicast_Routing_Overview]]: Basic routing principles.
- [[Congestion_Control_Fundamentals]]: Impact of routing changes on congestion.

---

**Previous:** [[Link_State_Routing]]
**Next:** [[Network_Layer_Summary]]
