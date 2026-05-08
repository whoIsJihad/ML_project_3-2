# Multicast Routing

## Definition

Multicast routing is the delivery of packets from a source to multiple destinations specified by membership in a multicast group. Formally, a multicast operation involves a source $S \in V$ sending a packet to a subset $G \subseteq V$ of network nodes, where $G$ is the multicast group and $|G| < |V|$ (i.e., less than all network nodes).

## Fundamental Distinction from Broadcast and Unicast

- **Unicast** ([[Unicast_Routing_Overview]]): One-to-one communication. A source $S$ sends to a single destination $D$. Packet delivery path is a simple path from $S$ to $D$.
- **Broadcast**: One-to-all communication. A source $S$ sends to every node in the network. Delivery involves a spanning tree.
- **Multicast**: One-to-many communication. A source $S$ sends to an arbitrary subset $G$ of nodes. Delivery involves a group-specific delivery tree that reaches exactly the nodes in $G$.

Formally, for a multicast group $G$ and source $S$:
$$G = \{v_1, v_2, \ldots, v_k\} \subseteq V$$

The multicast routing operation ensures that every node $v_i \in G$ receives the packet exactly once (or at least once, depending on implementation).

## Multicast Group Architecture

### Dynamic Group Membership

Unlike broadcast, which is implicit (all nodes in network), multicast groups are dynamic:
- Hosts explicitly join a multicast group (membership announcement).
- Hosts leave a group (membership withdrawal).
- Group membership changes over time.

### Group Address Semantics

Multicast groups are identified by a multicast address:

**IPv4 Multicast**: Addresses in the range `224.0.0.0` to `239.255.255.255` (Class D addresses). For example:
- `224.0.0.1`: All hosts on this subnet.
- `224.0.0.2`: All routers on this subnet.
- `239.x.x.x`: Administratively scoped addresses (limited to an organization).

**IPv6 Multicast**: Addresses with prefix `ff00::/8`. Structure:
- `ff0S:TLID:group_id` where $S$ is scope (1=node, 2=link, 5=site, 8=organization, 14=global) and $T$ indicates transient vs permanent groups.

## Multicast Group Membership

### Host-Side Membership: IGMP/MLD

Hosts announce their membership in multicast groups using:
- **IGMP (Internet Group Management Protocol)**: For IPv4.
- **MLD (Multicast Listener Discovery)**: For IPv6.

These protocols allow a host to inform nearby routers that it wishes to receive traffic for a specific multicast group.

Process:
1. Host sends a **membership join** message to the local router, specifying the group address.
2. Router learns that the group has members on this link.
3. Host sends **membership leave** messages when it no longer wishes to receive the group.

### Router-Side Group Tracking

Routers maintain state per interface:
$$\text{GroupMembership}[i] = \{g_1, g_2, \ldots, g_m\}$$

where $i$ is an interface and $g_j$ are multicast groups with members on that interface.

## Multicast Routing Trees

### Source-Specific Multicast Trees (SSM)

In source-specific multicast, for each pair (source $S$, group $G$), a separate shortest-path tree is constructed:

$$T_{S,G} = (V', E')$$

where $V'$ includes $S$ and all nodes that are on shortest paths from $S$ to any member of $G$, and $E'$ are the edges connecting these nodes.

This is also called **source tree (SPT)** or **shortest path tree (SPT)**.

### Shared Trees

In shared tree approaches, a single tree rooted at a core node (rendezvous point or $RP$) is used for all sources and groups:

$$T_{RP} = (V, E')$$

All packets destined for group $G$ are routed through the core $RP$ regardless of source. This reduces router state (no need to track per-source trees) but may increase path length and latency.

### Tree Properties

For a multicast tree $T_{S,G}$ delivering to group $G$ from source $S$:

1. **Connectedness**: The tree is connected; there is a path from $S$ to every member in $G$.
2. **Acyclicity**: No cycles; the tree structure prevents duplicate packet reception (assuming correct forwarding).
3. **Efficiency**: Ideally, the tree has no redundant edges (it is a minimal tree reaching all group members).

A **Steiner tree** is a minimal tree connecting a source and a set of destination nodes, potentially including Steiner nodes (nodes that are neither source nor destinations but help minimize tree cost).

## Multicast Forwarding Model

### Reverse Path Forwarding for Multicast

Routers forward multicast packets using a reverse path forwarding (RPF) check similar to [[Broadcast_Routing_Algorithms|broadcast RPF]], but group-specific:

```
upon reception of multicast packet P (source = S, group = G) at router R on interface i_in:
  if (S, G) not in R.cache:
    if i_in == parent(R, S):  // reverse path check for source S
      R.cache[(S, G)] = new_state
      // Determine outgoing interfaces
      outgoing = {interfaces where group G has members} 
               minus {i_in}
      for each interface i_out in outgoing:
        forward P over i_out
      end for
    else:
      discard P (arrived on wrong interface)
    end if
  else:
    // already processed this multicast flow
    check if duplicate, suppress as needed
  end if
```

The critical difference from broadcast: packets are forwarded only on interfaces where the group has members (determined via IGMP/MLD), not to all outgoing interfaces.

## Multicast Group Semantics: Any-Source vs Source-Specific

### Any-Source Multicast (ASM)

A host joins a multicast group $G$ without specifying the source. It will receive traffic from **any** source sending to $G$.

- **Advantage**: Decouples sources from receivers; sources do not need to know group members.
- **Disadvantage**: Requires more complex group management; all sources' traffic must be filtered and merged.

### Source-Specific Multicast (SSM)

A host joins a group $G$ from a specific source $S$, denoted $(S, G)$. It receives traffic **only** from $S$ to $G$.

- **Advantage**: Simpler routing (source-specific trees); better security (can authenticate source).
- **Disadvantage**: Requires explicit knowledge of source.

## Multicast in Different Scope Domains

### Link-Local Multicast

Multicast addresses with link-local scope (e.g., `224.0.0.x`) are not forwarded beyond the local link. Routers do not forward these packets to other network segments.

### Organizational Multicast

Administratively scoped multicast (e.g., `239.0.0.0/8` in IPv4) is confined to an organization. Routers at administrative boundaries suppress these packets.

### Global Multicast

Global multicast addresses (e.g., `224.1.0.0` and above, or `ff0e::/8` in IPv6) may be routed across the Internet if the network infrastructure supports it. However, most networks restrict global multicast due to management complexity.

## Challenges in Multicast Routing

### State Explosion

Per-source, per-group trees require $O(|S| \cdot |G|)$ state in the network, where $|S|$ is the number of multicast sources and $|G|$ is the number of groups. In large networks, this can be prohibitive.

### Dynamic Membership Changes

When hosts join or leave a multicast group, the multicast tree may need to be recomputed. Frequent membership changes can cause routing instability.

### Heterogeneous Group Members

Multicast group members may be distributed across geographically distant network segments. Constructing efficient delivery trees that minimize overall cost while respecting link capacities is a hard optimization problem.

### Inter-Domain Multicast

Multicast across different autonomous systems (inter-domain multicast) is complex because:
- Not all ISPs support multicast.
- Policy-based forwarding decisions must be coordinated across domains.
- No universally deployed inter-domain multicast protocol exists (MSDP is rarely deployed).

## Related Concepts

- [[Broadcast_Routing]]: Multicast generalizes broadcast to subsets of nodes.
- [[Broadcast_Routing_Algorithms]]: RPF techniques apply to multicast as well.
- [[Multicast_Routing_Algorithms]]: Details specific algorithms (PIM, DVMRP, MOSPF).
- [[DHCP_Protocol]]: Uses broadcast for discovery; can also use unicast with relay agents.

---

**Next:** [[Multicast_Routing_Algorithms]]
