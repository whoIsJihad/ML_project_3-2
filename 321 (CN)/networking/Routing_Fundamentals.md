# Routing Fundamentals

## Definition of Routing

Routing is the process by which packets (discrete units of data) are forwarded from a source host through intermediate network nodes (routers) to a destination host. The primary responsibility of a router is to determine the next hop (next intermediate node) for each packet based on the packet's destination address and the router's routing table.

Formally, routing solves the following problem:

**Given:**
- A connected graph $G = (V, E)$ where $V$ is the set of routers and $E$ is the set of links
- A source router $s \in V$
- A destination router $d \in V$
- A packet with destination address $d$

**Find:**
- A path $P = (s, v_1, v_2, \ldots, v_{n-1}, d)$ such that the packet travels from $s$ to $d$ following links in $E$

## Routing Decisions

A router makes a routing decision **per packet** based on two pieces of information:

1. **Destination Address**: The packet contains the destination IP address (in its header)
2. **Routing Table**: Each router maintains a local routing table that maps destination networks to outgoing interfaces (and optionally the next-hop router)

The routing decision at a router is **local**—the router only knows:
- Its own routing table
- The destination address in the packet
- Which physical interface the packet arrived on

The router does **not** know:
- The global network topology
- The current state of remote links
- Whether the chosen next hop will ultimately deliver the packet successfully

## Routing Table Structure

A routing table is a data structure stored in a router's memory. Each entry in a routing table typically has the following form:

| Destination Network | Next Hop Router | Outgoing Interface | Metric/Cost |
|---|---|---|---|
| 10.0.0.0/24 | 192.168.1.1 | eth0 | 1 |
| 10.1.0.0/24 | 192.168.1.2 | eth0 | 2 |
| 172.16.0.0/16 | 192.168.2.1 | eth1 | 5 |
| Default | 192.168.1.1 | eth0 | ∞ |

**Fields explained:**
- **Destination Network**: The network address (IP address + subnet mask) for which this entry applies
- **Next Hop Router**: The IP address of the next router to which the packet should be sent
- **Outgoing Interface**: The physical or logical interface on this router through which packets are sent
- **Metric/Cost**: A numerical value representing the "cost" of using this route (lower is better in most algorithms)

## Packet Forwarding Algorithm

When a router receives a packet, it executes the following forwarding algorithm:

```
Algorithm: ForwardPacket(packet)
Input: A packet with destination IP address D
Output: The outgoing interface and next-hop IP address

1. Extract destination IP address D from packet header
2. Search routing table for entry matching D
   - First, try to match D with the longest prefix match
     (most specific network address that D belongs to)
3. If matching entry found:
   a. Retrieve next-hop router address and outgoing interface
   b. Forward packet out the outgoing interface to the next-hop router
   c. Update packet's TTL (Time-To-Live) field: TTL ← TTL - 1
   d. Recalculate packet's IP header checksum
4. If TTL becomes 0:
   a. Discard packet
   b. Send ICMP Time Exceeded message to source
5. If no matching entry found:
   a. Use default route (if exists)
   b. Otherwise, discard packet and send ICMP Destination Unreachable
```

### Longest Prefix Matching

Modern routers use **longest prefix matching** to handle overlapping network addresses. This means:
- If a packet with destination 10.0.5.3 arrives
- And the routing table has entries for both 10.0.0.0/16 and 10.0.5.0/24
- The router uses the 10.0.5.0/24 entry (24-bit prefix is longer than 16-bit prefix)

This enables hierarchical routing and more specific routes to override broader ones.

## Routing vs. Forwarding

These terms are often confused but are fundamentally different:

| Aspect | Routing | Forwarding |
|---|---|---|
| **Definition** | Process of determining paths for packets across the network | Process of moving packets from input to output interface |
| **Time Scale** | Computed periodically or on-demand (seconds to minutes) | Done for every packet (milliseconds) |
| **Scope** | Involves multiple routers (global) | Happens in a single router (local) |
| **Purpose** | Build/maintain routing tables | Use routing tables to forward packets |
| **Computation** | May use complex algorithms (Dijkstra, Bellman-Ford) | Simple table lookup |

## Routing Protocols

Routers cannot simply maintain their routing tables manually. Instead, they run **routing protocols** that automatically discover network topology and compute optimal paths.

Routing protocols are classified as:

### Interior Gateway Protocols (IGP)
Used to route packets within a single autonomous system (AS).

- **Distance Vector Protocols**: [[Distance_Vector_Routing]] — RIP, IGRP
- **Link State Protocols**: [[Link_State_Routing]] — OSPF, IS-IS
- **Advanced Protocols**: [[AODV_Protocol]] — For ad hoc networks

### Exterior Gateway Protocols (EGP)
Used to route packets between autonomous systems.

- **BGP (Border Gateway Protocol)** — The standard for inter-AS routing (not covered in this tutorial set)

## Hopcount, Cost, and Metrics

The "cost" or "metric" of a route is a numerical value that quantifies the desirability of using that route. Different protocols use different metrics:

| Protocol | Metric | Formula/Definition |
|---|---|---|
| RIP | Hop count | Number of routers (hops) to reach destination; max 15 |
| OSPF | Cost | Inverse of bandwidth: $\text{Cost} = \frac{10^8 \text{ bps}}{\text{Bandwidth bps}}$ |
| IS-IS | Metric | Arbitrary value assigned to each link (typically 10) |
| Ad Hoc Protocols | Hop count or ETX | Expected Transmission Count; accounts for link quality |

For example, in OSPF:
- A 1 Gbps link has cost: $\frac{10^8}{10^9} = 0.1$
- A 10 Mbps link has cost: $\frac{10^8}{10^7} = 10$

Lower metrics are preferred; routers select paths with the lowest total cost.

## Convergence and Stability

When the network topology changes (e.g., a link fails or a new link is added), routing protocols must **converge** to a new stable state where all routers have valid routing tables consistent with the new topology.

**Convergence time**: The duration from when a topology change occurs until all routers have updated their routing tables and packets are being forwarded along the new optimal paths.

- **Fast convergence** is desirable (avoids packet loss and loops)
- **Slow convergence** can lead to:
  - **Routing loops**: Packets cycle indefinitely between routers
  - **Unreachability**: Packets cannot reach some destinations temporarily
  - **Inefficiency**: Packets take suboptimal paths during transition

## Routing Table Size

As networks grow, routing tables can become very large. This is addressed by:

1. **Aggregation**: Combining multiple smaller networks into a larger one (supernetting)
2. **Default Routes**: A catch-all entry for destinations not explicitly listed
3. **Hierarchical Routing**: [[Hierarchical_Routing]] — Organizing routers into regions/areas
4. **BGP**: Inter-AS routing with aggregated advertisements

Example:
- Flat routing table with all 4.3 billion IPv4 addresses → infeasible
- Organized by CIDR blocks and hierarchical routing → manageable (hundreds of thousands of entries)

## Key Terminology

| Term | Definition |
|---|---|
| **Autonomous System (AS)** | A network under the control of a single administrative entity (ISP, enterprise, etc.) |
| **Interior Router** | A router that is within an AS (runs IGP) |
| **Border Router** | A router on the edge of an AS that connects to other ASs (runs BGP) |
| **Subnet** | A contiguous group of IP addresses managed by a single router or network segment |
| **Default Route** | A routing table entry that matches all destinations not matched by more specific entries |
| **TTL (Time-To-Live)** | A counter in the IP header that decrements at each hop; packet is discarded when TTL reaches 0 |
| **Metric/Cost** | Numerical value assigned to a path; lower values indicate better paths |

---

## Next Steps

- **For building routing tables**: [[Routing_Tables_and_Forwarding_Mechanics]]
- **For unicast routing algorithms**: [[Unicast_Routing_Overview]]
- **For distance vector method**: [[Distance_Vector_Routing]]
- **For link state method**: [[Link_State_Routing]]
- **For IPv4 addressing prerequisites**: [[IP_Addressing_Review]]
