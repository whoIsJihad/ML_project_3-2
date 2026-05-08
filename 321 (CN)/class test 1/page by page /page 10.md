# Study Guide 1: Datagram vs. Virtual Circuit (VC) Subnets

In computer networking, the network layer can provide either a connectionless service (Datagram) or a connection-oriented service (Virtual Circuit). If you're planning on building anything more complex than a "Hello World" app, you should probably understand why these matter.

## 1. Comparative Analysis

|Issue|Datagram Subnet (Connectionless)|Virtual Circuit Subnet (Connection-oriented)|
|---|---|---|
|**Circuit Setup**|**Not Required.** Packets are injected into the network immediately. No handshake or signaling phase.|**Required.** A connection must be established (using setup packets) before any data packets can be sent.|
|**Addressing**|**Full Source & Destination.** Every single packet must carry the complete global address of the sender and receiver.|**VC Identifier.** Packets only carry a short, local Virtual Circuit Number (VCN) or Label.|
|**Routing Strategy**|**Independent.** Each packet is routed individually based on the current state of the network. Two packets from the same source to the same destination might take different paths.|**Fixed Path.** All packets follow the pre-established route determined during the setup phase.|
|**Router Failure**|**Robust.** If a router fails, only packets currently being processed by it are lost. Subsequent packets simply route around the failure.|**Brittle.** If any router on the established path goes down, the entire VC is terminated. All connections passing through it must be re-established.|
|**Quality of Service (QoS)**|**Difficult.** Since packets are scattered across different paths, it is nearly impossible to guarantee bandwidth or delay (jitter).|**Easier.** Resources (like buffers and CPU cycles) can be reserved at each router along the path during the setup phase.|
|**Congestion Control**|**Difficult.** Congestion is hard to predict because traffic patterns are erratic and independent.|**Easier.** The network can refuse to establish new VCs if the path is already congested (Admission Control).|

## 2. Deep Dive Explanations

### Why Datagrams are "Self-Healing"

In a Datagram network (like the IP layer of the Internet), routers maintain "routing tables" rather than "connection tables." If a link goes down, the routing protocol (like OSPF or BGP) eventually updates the tables, and the next packet just takes a different exit interface. It’s chaotic but highly resilient.

### Why Virtual Circuits are "Efficient but Fragile"

In a VC network (like ATM or MPLS), the setup phase creates a "state" in every router along the path. This allows for faster switching because the router only looks at a short VC ID instead of a 128-bit IPv6 address. However, this state is also its undoing; if a router loses power, it loses the "memory" of that connection, and the whole thing collapses.

## 3. Essential Traffic Control Definitions

You often confuse these two, so pay attention.

- **Flow Control:** This is a **Point-to-Point** mechanism. It ensures a fast sender doesn't overwhelm a slow receiver. If the destination's buffer is full, the sender must throttle back.
    
- **Congestion Control:** This is a **Network-Wide** mechanism. It ensures that the sum of all traffic injected into the subnet does not exceed the capacity of the routers or links within the network.
    

## 4. Summary for Exams

- **Use Datagrams** when the overhead of setup is too high for short bursts of data, or when high availability/survivability is the priority (e.g., The Internet).
    
- **Use Virtual Circuits** when you need guaranteed performance, predictable latency, or when you are billing users for specific "calls" or "sessions."

# Study Guide 2: Routing Algorithms & Metrics

## 1. Overview

A routing algorithm is the part of the network layer software responsible for deciding which output line an incoming packet should be transmitted on. For a routing algorithm to be effective, it must satisfy several key properties.

## 2. Desired Properties of Routing Algorithms

To avoid complete network chaos, an algorithm must adhere to these principles:

|Property|Description|
|---|---|
|**Correctness**|The algorithm must accurately deliver packets to the intended destination.|
|**Simplicity**|It must be efficient and minimize computational/memory overhead on the routers.|
|**Stability**|**Initial Phase:** It takes time to converge (reach a steady state).<br><br>**Post-Convergence:** Once stable, the algorithm should not fluctuate or oscillate unnecessarily.|
|**Robustness**|The algorithm must gracefully handle **topology changes**, such as link failures, router crashes, or the addition of new nodes.|
|**Fairness**|Every node should be granted a reasonable opportunity to transmit data without being indefinitely blocked.|
|**Optimality**|The algorithm should aim to **maximize total usage** (throughput) of the available network resources.|

## 3. The Conflict: Fairness vs. Optimality

In networking, "Optimality" and "Fairness" are often mutually exclusive. Maximizing the total throughput of a network (optimality) frequently leads to the "starvation" of specific paths (unfairness).

### Case Study: The Backbone Link Saturation

**Scenario Setup:** Consider a network with a central horizontal backbone link connecting two points, $X$ and $X'$.

- **Vertical Flows:** Three independent vertical flows exist: $A \rightarrow A'$, $B \rightarrow B'$, and $C \rightarrow C'$.
    
- **Horizontal Flow:** One horizontal flow exists: $X \rightarrow X'$.
    
- **The Constraint:** The vertical flows $A$, $B$, and $C$ together are sufficient to fully **saturate** the capacity of the horizontal link they cross.
    

**The Resulting Conflict:**

1. **Optimality Approach:** To maximize the total number of packets delivered across the entire network, we would allow $A$, $B$, and $C$ to transmit at their maximum rate. This utilizes the horizontal link's capacity most efficiently.
    
2. **The Impact on Fairness:** Because $A, B, C$ have completely saturated the link, the flow $X \rightarrow X'$ receives **zero bandwidth**.
    
3. **Conclusion:** A strategy that is "Optimal" for the system as a whole can be "Unfair" to individual users or flows. Finding a balance between these two is a primary challenge in network protocol design.
    

## 4. Key Definitions for Review

- **Convergence:** The process by which all routers in a network come to an agreement on the best paths.
    
- **Topology Change:** Any change in the physical or logical arrangement of the network (e.g., a cable being unplugged).
    
- **Throughput:** The actual amount of data successfully transferred over a link in a given period.