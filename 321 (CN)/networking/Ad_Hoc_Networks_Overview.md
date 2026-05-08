# Ad Hoc Networks: Overview

## Definition

An ad hoc network is a wireless network that operates without a fixed infrastructure. Unlike traditional networks that rely on base stations, access points, or routers at predetermined locations, ad hoc networks are formed dynamically by a set of autonomous mobile nodes that communicate directly with each other through wireless links, with no centralized administrative authority.

Formally, an ad hoc network is a dynamic, self-organizing network where:
- Nodes communicate via wireless links (no wired infrastructure).
- Network topology changes frequently due to node mobility.
- Routing is distributed and decentralized.
- Nodes may be resource-constrained (battery, processing power, memory).

## Distinction from Traditional Networks

### Infrastructure Networks

Traditional wireless networks (cellular, WLAN) have an infrastructure backbone:

```
       ┌─────────────────┐
       │  Infrastructure │
       │  (base stations)|
       └─────────────────┘
              △  △
             /    \
            /      \
       Mobile      Mobile
       Node 1      Node 2
```

Communication between nodes typically flows through the infrastructure. Even when two nodes are adjacent, packets may route through the base station.

### Ad Hoc Networks

In contrast, ad hoc networks allow direct multi-hop communication:

```
    Node 1 ─→ Node 2 ─→ Node 3
    ↓
    (no infrastructure needed)
```

Nodes forward packets on behalf of other nodes, creating dynamic multi-hop paths.

## Characteristics of Ad Hoc Networks

### Dynamic Topology

The network topology changes frequently due to:
- Node mobility (nodes enter/leave network range).
- Wireless link variability (fading, interference).
- Power constraints (nodes turn off to conserve battery).

Formally, let $G(t) = (V(t), E(t))$ represent the network topology at time $t$. In ad hoc networks, $\frac{d|V(t)|}{dt}$ and $\frac{d|E(t)|}{dt}$ are non-zero; the topology is time-varying.

### Decentralized Operation

No central authority manages routing or resource allocation. Every node makes autonomous decisions about:
- Which packets to forward.
- Which neighbors to communicate with.
- When to participate in routing discovery.

This decentralization is both an advantage (robustness, no single point of failure) and a challenge (complex protocol design, potential for inconsistent states).

### Bandwidth Constraints

Wireless links have limited bandwidth compared to wired networks. Ad hoc protocols must minimize:
- Control message overhead.
- Redundant transmissions.
- Collision-induced retransmissions.

### Power Constraints

Many ad hoc nodes operate on battery power and have limited energy reserves. Routing protocols must:
- Minimize node transmissions (each transmission consumes energy).
- Avoid idle listening (listening to the channel for potential incoming packets).
- Support energy-efficient link selections.

### Asymmetric Links

Unlike wired networks where links are inherently bidirectional, wireless links can be asymmetric:
- Node A can reach Node B, but Node B cannot reach Node A due to differences in transmit power or antenna orientation.

Routing must accommodate unidirectional links or ensure bidirectionality through verification mechanisms.

## Deployment Scenarios for Ad Hoc Networks

### Emergency and Disaster Recovery

When infrastructure is destroyed (earthquake, natural disaster), ad hoc networks enable temporary communication:
- First responders form a network with handheld devices.
- No pre-existing infrastructure is available.
- Networks must self-organize rapidly.

### Military and Tactical Networks

Soldiers, vehicles, and drones form networks to coordinate operations:
- Mobility is expected (nodes move between tactical positions).
- Secrecy and jamming resistance are important.
- Network topology changes rapidly.

### Sensor Networks

Collections of low-power sensors deployed in an environment:
- Thousands of sensors distributed over an area.
- Sensors forward data toward a collection point (sink node).
- Very limited battery and processing power.

Example: Environmental monitoring, structural health monitoring of bridges.

### Vehicular Networks (VANET)

Vehicles equipped with wireless radios form networks:
- Nodes (vehicles) move at high speed.
- Communication range is typically 100-300 meters.
- Applications: collision avoidance, traffic information sharing.

See [[MANET_VANET_FANET_Comparison]] for more detailed taxonomy.

## Routing Challenges in Ad Hoc Networks

### Challenge 1: Dynamic Topology

Routing paths become invalid as nodes move. A route that exists at time $t$ may be broken at time $t + \Delta t$ due to:
- A link node moving out of range.
- A new link becoming available.

**Consequence**: Routes must be recomputed frequently, and stale routing information must be managed.

### Challenge 2: Decentralized Route Discovery

Unlike infrastructure networks where routing tables are computed centrally, ad hoc networks must discover routes in a distributed manner:
- A source must find a route to a destination.
- No centralized routing server exists.
- Route discovery messages can only propagate through existing multi-hop paths.

This creates a **bootstrapping problem**: How does a source find a route to a destination when the network topology is unknown?

### Challenge 3: Hidden Terminal Problem

In wireless networks, a node may not detect a transmission from another node due to distance or obstacles:

```
    A ─────────── B ─────────── C
    (A cannot hear C)
```

If A and C both transmit to B, the transmissions collide at B (from B's perspective), even though A and C were unaware of each other.

Routing protocols must manage this through careful scheduling, collision avoidance, or explicit notification.

### Challenge 4: Limited Bandwidth

Control messages (routing announcements, route discovery) consume bandwidth needed for data traffic. Ad hoc protocols must balance:
- Frequent updates (to detect topology changes) vs. low overhead.
- Detailed routing information (for optimal routes) vs. message size.

### Challenge 5: Resource Constraints

Many ad hoc nodes are energy-constrained. Routing must consider:
- **Energy-efficient paths**: Not always the shortest path; a longer path with less power consumption may be preferable.
- **Sleep/wake cycles**: Nodes may periodically power off to conserve energy; routing must adapt.
- **Processing overhead**: Complex route calculations consume energy and processing.

## Routing Protocol Taxonomy

Ad hoc routing protocols are broadly categorized as:

### 1. Proactive (Table-Driven) Protocols

Routers maintain routes to all destinations at all times:
- Periodically exchange routing information (updates).
- Upon packet arrival, a route already exists (usually).
- No route discovery delay, but continuous control overhead.

Example: [[Distance_Vector_Routing|DSDV]] (Destination-Sequenced Distance Vector), OLSR (Optimized Link State Routing).

### 2. Reactive (On-Demand) Protocols

Routes are discovered only when needed:
- Source initiates route discovery upon first packet arrival.
- Subsequent packets use the discovered route.
- Control overhead is proportional to traffic; ideal for sparse communication.

Example: [[AODV_Protocol|AODV]] (Ad hoc On-Demand Distance Vector), DSR (Dynamic Source Routing).

### 3. Hybrid Protocols

Combine proactive and reactive approaches:
- Nearby nodes use proactive (table-driven) routing.
- Distant nodes are reached via reactive (on-demand) route discovery.

Example: ZRP (Zone Routing Protocol).

## Requirements and Design Goals

### Correctness

Routes must be loop-free and valid (not broken). Sequence numbers or other mechanisms prevent routing loops.

### Optimality

Ideally, routes are shortest paths. However, due to overhead, an optimal path may not be computed in resource-constrained scenarios.

### Scalability

Routing overhead must grow sub-linearly with network size. In networks with hundreds or thousands of nodes, per-destination routing state becomes infeasible.

### Adaptability

Protocols must quickly adapt to topology changes without excessive overhead.

### Energy Efficiency

Routes should minimize total energy consumption, not just minimize hop count.

## Related Concepts

- [[AODV_Protocol]]: A prominent reactive ad hoc routing protocol.
- [[MANET_VANET_FANET_Comparison]]: Taxonomy of ad hoc network types.
- [[Distance_Vector_Routing]]: Proactive routing techniques used in some ad hoc protocols.
- [[Link_State_Routing]]: Alternative routing basis for some ad hoc protocols.

---

**Next:** [[MANET_VANET_FANET_Comparison]]
