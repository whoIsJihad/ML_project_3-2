# Broadcast Routing

## Definition

Broadcast routing is the process of delivering a single packet from a source host to all other hosts in a network. Formally, broadcast is defined as a one-to-all communication pattern where a source $S$ sends a packet that must reach every destination node in the network domain.

### Key Distinction from Unicast

In [[Unicast_Routing_Overview|unicast routing]], a packet is forwarded from source to a single destination through a sequence of forwarding decisions at each router. In broadcast routing, a packet originating at source $S$ must be replicated and forwarded through the network such that every node receives exactly one copy of the packet (or at least once, depending on implementation).

Formally, let $N = \{v_1, v_2, \ldots, v_n\}$ be the set of all nodes in a network. A broadcast operation from source $s \in N$ is successful if and only if every node $v_i \in N \setminus \{s\}$ receives the packet exactly once (or at least once).

## Broadcast Delivery Semantics

### Exact-Once Delivery
In this model, every node except the source receives the packet exactly once. This requires careful duplicate suppression mechanisms at intermediate routers.

### At-Least-Once Delivery
Nodes may receive multiple copies of the same broadcast packet. The application layer is responsible for deduplication if needed.

## Motivation for Broadcast

Broadcast is essential for several network operations:

1. **Address Resolution Protocol (ARP)**: When a host needs to map an IP address to a link-layer address, it broadcasts an ARP request.
2. **Dynamic Host Configuration Protocol (DHCP)**: Clients broadcast DHCP DISCOVER messages to find available DHCP servers.
3. **Routing Protocol Updates**: Some routing protocols (particularly older protocols like RIP) use broadcast to disseminate routing information.
4. **Service Discovery**: Hosts broadcast to discover available services on a local network.
5. **Network Management**: Administrative commands may be broadcast to manage multiple hosts.

## Scope of Broadcast

### Local Area Network (LAN) Broadcast

In a LAN (e.g., an Ethernet segment), broadcast is straightforward because all hosts share the same physical medium. A broadcast packet on an Ethernet network has a destination MAC address of `ff:ff:ff:ff:ff:ff`, which causes every interface on the LAN to accept and process the frame.

### Internet-Wide Broadcast

Broadcasting across the entire Internet is generally disabled for security and efficiency reasons. Routers are typically configured to not forward broadcast packets beyond the boundaries of a single administrative domain.

### Limited Broadcast

A limited broadcast address (in IPv4, `255.255.255.255`) is used to broadcast within a single network segment. Routers do not forward limited broadcast packets.

### Directed Broadcast

A directed broadcast address for a subnet (e.g., `192.168.1.255` for the `192.168.1.0/24` network) allows broadcasting to all hosts in that specific subnet. Routers may optionally forward directed broadcast packets into the target subnet, though many now disable this for security.

## Challenges in Broadcast Routing

### Duplicate Reception

If a router forwards a broadcast packet over multiple outgoing interfaces (which is necessary to reach all nodes), adjacent routers may receive the same packet multiple times if they are connected through multiple paths. Without duplicate suppression, this leads to exponential packet replication.

### Network Overhead

Broadcasting can cause significant network load. If a single source sends a broadcast packet and the network must deliver it to $n-1$ other nodes, the total number of packet transmissions may be $O(n)$ or higher in redundant networks.

### Scalability

As networks grow, broadcast mechanisms must scale efficiently. Naive flooding approaches (sending a packet over all outgoing interfaces) can overwhelm network capacity.

## Formal Model for Broadcast

Let $G = (V, E)$ be a connected undirected graph representing the network topology, where $V$ is the set of nodes (routers and hosts) and $E$ is the set of edges (links). A broadcast tree rooted at source $s$ is a spanning tree $T_s = (V, E_s)$ where $E_s \subseteq E$ such that:

1. $T_s$ is connected.
2. $T_s$ is acyclic.
3. Every node $v \in V$ is reachable from $s$ through exactly one path in $T_s$.

For exact-once delivery, the router forwarding algorithm must:
- Forward a broadcast packet received on interface $i_{\text{in}}$ over all interfaces in $\text{outgoing}(v)$ except the interface from which the packet arrived.
- Suppress duplicate packets (packets with the same source and broadcast ID that have already been processed).

This ensures that over the broadcast tree, each node receives the packet exactly once.

## Relationship to [[Broadcast_Routing_Algorithms]]

The theoretical framework of broadcast routing leads to several algorithms that differ in how they construct and utilize broadcast trees:

- **Flooding**: A naive approach that forwards on all outgoing interfaces with hopcount limits.
- **Reverse Path Forwarding (RPF)**: A tree-based approach using reverse paths through unicast routing.
- **Spanning Tree**: Using a pre-computed spanning tree rooted at the source or at a central node.

See [[Broadcast_Routing_Algorithms]] for detailed algorithms and their properties.

## Related Concepts

- [[Multicast_Routing]]: An extension of broadcast where packets are delivered to a subset of nodes (multicast group) rather than all nodes.
- [[Unicast_Routing_Overview]]: The foundational point-to-point routing on which broadcast is layered.
- [[IP_Addressing_Review]]: IPv4 and IPv6 broadcast and multicast address formats.

---

**Next:** [[Broadcast_Routing_Algorithms]]
