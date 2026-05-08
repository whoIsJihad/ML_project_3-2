# Multicast Routing Algorithms

## Overview

Multicast routing algorithms define how routers construct and maintain delivery trees for multicast groups. Major algorithms differ in whether they construct source-specific trees (SSM/ASM with SPTs) or shared trees, and in how they discover group members and manage tree dynamics.

## Prerequisite Knowledge

- [[Multicast_Routing]]: Foundational multicast concepts, group membership, tree types.
- [[Broadcast_Routing_Algorithms]]: RPF and tree-based forwarding.
- [[Link_State_Routing]]: Dijkstra's algorithm and shortest-path tree construction.

## Algorithm 1: DVMRP (Distance Vector Multicast Routing Protocol)

### Principle

DVMRP is a source-based multicast routing protocol that constructs shortest-path trees (SPT) rooted at each multicast source. It is the earliest multicast routing protocol deployed in the MBone (experimental multicast backbone).

### How It Works

**Phase 1: Unicast Routing**
DVMRP first builds unicast routing tables using distance-vector routing (similar to [[Distance_Vector_Routing|RIP]]) with hop-count metrics. Each router learns the shortest path to every other router.

**Phase 2: Reverse Path Forwarding (RPF)**
When a multicast packet from source $S$ arrives at a router $R$:
1. Check if the packet arrived on the interface that is the reverse path to $S$ (the next-hop interface in the unicast route from $R$ to $S$).
2. If yes, forward the packet on all outgoing interfaces except the incoming one, subject to membership information.
3. If no, discard the packet (RPF check failure).

**Phase 3: Membership-Based Pruning**
Initially, multicast packets are flooded to all interfaces. To reduce waste, DVMRP implements **pruning**:
- Leaf routers with no multicast group members send **prune messages** upstream to prevent receipt of unwanted packets.
- Prune state is maintained with a timeout; after timeout, the pruning is removed, and the pruning process repeats.

### Algorithm Pseudocode

```
upon reception of multicast packet P (source = S, group = G) at router R on interface i_in:
  if i_in == parent(R, S):  // RPF check
    if R has members of group G or has downstream pruned branches:
      for each interface i_out in R.interfaces where i_out != i_in:
        if (not pruned(R, S, G, i_out)):  // check if prune is active
          forward P over i_out
        end if
      end for
    end if
  else:
    discard P  // RPF check failed
  end if

upon reception of prune message from downstream router D for (S, G):
  if (all downstream routers for (S, G) have sent prunes):
    activate prune(R, S, G, interface_to_upstream)
    send prune message upstream
  end if
```

### Properties

**Correctness**: DVMRP guarantees loop-free delivery via RPF checks. Each multicast packet reaches each group member exactly once (absent packet loss).

**Scalability**: Prune-based optimization reduces overhead, but still requires initial flooding. In networks with many receivers or sparse groups, initial flooding can consume significant bandwidth.

**SPT Optimality**: Multicast trees are shortest paths from each source, minimizing latency.

**Complexity**: DVMRP implementation is complex due to prune state management and timeout handling.

### Use and Deployment

DVMRP was used extensively in the MBone experiment but is now largely obsolete, replaced by more efficient protocols like PIM.

## Algorithm 2: PIM-SM (Protocol Independent Multicast - Sparse Mode)

### Principle

PIM-SM is the dominant multicast routing protocol used today. It uses a **shared tree** architecture rooted at a core router called the **Rendezvous Point (RP)**.

### Core Concepts

**Rendezvous Point (RP)**: A designated router elected per multicast group (or set of groups). All sources and receivers meet at the RP:
- Receivers join the shared tree rooted at the RP via **PIM JOIN** messages.
- Sources unicast their packets to the RP (encapsulated in PIM REGISTER messages).
- The RP decapsulates and forwards packets along the shared tree.

### Architecture

```
       RP (Shared Tree Root)
      / | \
     /  |  \
    S   |   R1
        |   
        R2
```

In this example, source $S$ sends to the RP, and receivers $R1$, $R2$ join the tree rooted at $RP$. All traffic flows through $RP$.

### Joining a Multicast Group

A host $H$ wishes to join group $G$:

1. $H$ sends an IGMP JOIN message to the local router.
2. The local router sends a **PIM JOIN** message toward the RP for group $G$.
3. Each intermediate router on the path to $RP$ adds the incoming interface to the tree for $(*, G)$ (where $*$ denotes any source).
4. The tree is built hop-by-hop from receivers toward the RP.

### Source Registration

A source $S$ begins sending to group $G$:

1. $S$ sends multicast packets normally.
2. The first-hop router (DR) encapsulates the packet and unicasts it to the RP in a **PIM REGISTER** message.
3. RP decapsulates and forwards along the shared tree.
4. RP sends **PIM REGISTER-STOP** to $S$'s DR to stop registration (once an SPT is built).

### Shortest Path Tree (SPT) Switchover

To optimize paths, PIM-SM supports switching from the shared tree (rooted at $RP$) to a shortest-path tree (SPT) rooted at the source:

- A receiver's DR monitors incoming packets from source $S$ on group $G$.
- If traffic exceeds a threshold, the DR initiates an **SPT JOIN** toward $S$.
- Traffic is switched to the SPT when available.
- The shared tree path becomes unused (pruned via PIM PRUNE).

This mechanism allows PIM-SM to achieve both the scalability benefits of shared trees and the latency benefits of SPTs.

### Algorithm Pseudocode (Simplified)

```
// Receiver joins group G
upon IGMP_JOIN(G) from host on interface i:
  send PIM_JOIN(*, G, RP) toward RP
  tree[*, G].add_incoming(i)

// Source sends to group G
upon multicast_packet from source S to group G:
  if (S is not directly connected to RP):
    encapsulate in PIM_REGISTER and unicast to RP
  end if
  if (traffic from (S, G) exceeds threshold):
    send PIM_JOIN(S, G) toward S  // start SPT join
  end if

// RP forwards on shared tree
upon multicast_packet for group G at RP:
  for each interface i in tree[*, G].outgoing:
    forward packet over i
  end for
```

### Properties

**Scalability**: Shared trees reduce router state to $O(|G|)$ (per group) rather than $O(|S| \cdot |G|)$ (per source-group pair). This scales well to large numbers of sources.

**Flexibility**: SPT switchover allows optimizing for low latency when needed while keeping baseline overhead low.

**Deployment**: PIM-SM is the industry standard for IP multicast and is widely supported.

**Complexity**: SPT switchover logic and RP placement are non-trivial.

### RP Selection

RPs are typically elected via:
- **Static configuration**: Network administrator manually configures RP addresses.
- **Bootstrap Protocol (PIM-BSR)**: Routers dynamically elect an RP candidate bootstrap router (BSR), which selects RPs.
- **Auto-RP**: Cisco's proprietary mechanism for automatic RP discovery.

## Algorithm 3: PIM-DM (Protocol Independent Multicast - Dense Mode)

### Principle

PIM-DM assumes multicast receivers are densely distributed and uses a flood-and-prune mechanism similar to DVMRP but is routing-protocol-independent (works over any unicast routing protocol).

### How It Works

**Phase 1: Flood**
Multicast packets are flooded to all outgoing interfaces except the incoming interface (except parent in RPF check).

**Phase 2: Prune**
Leaf routers with no local group members send **PIM PRUNE** messages upstream to prevent further receipt of unwanted packets.

**Phase 3: Graft**
If a router later learns that group members exist downstream, it sends a **PIM GRAFT** message upstream to rejoin the tree.

### Suitability

PIM-DM is suitable for:
- Small networks with dense multicast receivers.
- Applications like video distribution where most hosts receive.

PIM-DM is rarely used in modern networks; PIM-SM is preferred even in dense scenarios because it provides better overall scalability.

## Algorithm 4: MOSPF (Multicast Open Shortest Path First)

### Principle

MOSPF extends [[Link_State_Routing|OSPF]] to support multicast. Each router uses its link-state database to compute multicast trees on-demand per (source, group) pair using Dijkstra's algorithm.

### How It Works

1. Routers flood multicast group membership information via OSPF extensions.
2. Each router learns which groups have members on which links.
3. Upon receiving a packet from source $S$ to group $G$, a router computes the minimal tree (Steiner tree) connecting $S$ to all nodes with $G$ members.
4. The packet is forwarded along this tree.

### Properties

**Optimality**: Computes actual shortest-path trees per (S, G) pair, achieving optimal tree structure.

**Per-SPT State**: Requires $O(|S| \cdot |G|)$ state, which can be large in dense networks.

**Deployment**: MOSPF is rarely deployed in practice; the per-SPT state explosion and computational overhead led to preference for PIM-SM's shared-tree approach.

## Comparison of Multicast Algorithms

| Algorithm | Tree Type | State | Scalability | Latency | Deployment |
|---|---|---|---|---|---|
| **DVMRP** | Source SPT | $O(\|S\| \cdot \|G\|)$ | Poor | Low | Obsolete |
| **MOSPF** | Source SPT | $O(\|S\| \cdot \|G\|)$ | Poor | Low | Rarely used |
| **PIM-SM** | Shared tree (with SPT switchover) | $O(\|G\|)$ | Excellent | Moderate (low with SPT) | Standard |
| **PIM-DM** | Source SPT | $O(\|S\| \cdot \|G\|)$ | Poor | Low | Rarely used |

## Inter-Domain Multicast

### MSDP (Multicast Source Discovery Protocol)

For multicast spanning multiple autonomous systems, MSDP is used to advertise active sources to other ASes:

- Each AS runs its own multicast routing protocol (PIM-SM internally).
- MSDP routers exchange **source announcements** (SA messages) containing information about active (source, group) pairs.
- Receivers in other ASes can then join the shared tree rooted at the announced source's RP.

**Status**: MSDP is standardized but rarely deployed in practice due to complexity and limited inter-domain multicast demand.

## Related Concepts

- [[Multicast_Routing]]: Foundational multicast concepts.
- [[Link_State_Routing]]: MOSPF and Dijkstra's algorithm.
- [[Distance_Vector_Routing]]: DVMRP basis.
- [[Quality_of_Service_QoS]]: Multicast can be used for QoS-sensitive applications.

---

**Next:** [[Mobile_Host_Routing]]
