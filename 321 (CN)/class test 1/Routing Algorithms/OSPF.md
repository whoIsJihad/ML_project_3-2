# OSPF Part 1: The Link State Architecture

OSPF (Open Shortest Path First) is an **Interior Gateway Protocol (IGP)** designed to distribute routing information within a single Autonomous System (AS). Unlike the Distance Vector Routing (DVR) we discussed earlier—which relies on rumors from neighbors—OSPF is a **Link State Routing (LSR)** protocol.

### 1. The "Open" in OSPF

The "Open" doesn't mean it’s open-source in the GitHub sense; it means the specification is public (RFC 2328) and not proprietary (unlike Cisco's EIGRP). This allows routers from different vendors to actually talk to each other without having a stroke.

### 2. The Link State Database (LSDB)

The core difference from DVR is that every OSPF router maintains an identical **Link State Database**.

- Instead of knowing just the "distance" to a destination, an OSPF router knows the **entire topology** of the area.
    
- It achieves this by flooding **Link State Advertisements (LSAs)**.
    
- Think of the LSDB as a complete map of the city, whereas DVR was just a list of signs pointing to the next intersection.
    

### 3. Shortest Path First (SPF)

Once a router has a synchronized copy of the LSDB, it runs the **Dijkstra Algorithm** (Shortest Path First) locally.

- The router places itself at the root of the tree and calculates the shortest path to every other node.
    
- This is computationally expensive compared to DVR, but because the router has the full map, it converges much faster and is immune to the "Count-to-Infinity" problem.
    

### 4. Convergence Speed

Because every router sees the topology change almost simultaneously via flooding, OSPF can reroute traffic in milliseconds after a link failure, provided you haven't messed up the timers.

# OSPF Part 2: Neighbor Discovery and the "Hello" Protocol

Before a router can build a map of the network, it has to find its neighbors. It doesn't use a phone book; it uses the **Hello Protocol**.

### 1. The Router ID (RID)

Every OSPF router needs a name. This is the **Router ID**, a 32-bit value that looks like an IP address.

- **Selection Logic**: It’s either manually configured (best practice), the highest IP on a loopback interface, or the highest IP on an active physical interface.
    
- **Why it matters**: If two routers have the same RID, they will fight like siblings, and the adjacency will flap constantly.
    

### 2. The Hello Packet

Routers send Hello packets to the multicast address **224.0.0.5** (AllSPFRouters) every 10 seconds (default on Ethernet). **A Hello packet contains critical information that MUST match for a relationship to form:**

- **Hello/Dead Intervals**: If one router thinks "Hello" is every 10s and the other thinks 30s, they won't talk.
    
- **Area ID**: Neighbors must be in the same OSPF area.
    
- **Authentication**: Passwords (if any) must match.
    
- **Subnet Mask**: They must be on the same logical subnet.
    

### 3. The Neighbor State Machine (Part 1)

When two routers start talking, they go through these initial states:

1. **Down**: No Hellos received.
    
2. **Init**: Router A receives a Hello from Router B, but Router A doesn't see its own RID in B's "Neighbor List" yet. It’s a one-way greeting.
    
3. **Two-Way**: Router A sees its own RID in B's Hello. This is the "Friend Request Accepted" stage.
    
    - On a broadcast network (like Ethernet), this is where the **Designated Router (DR)** and **Backup Designated Router (BDR)** election happens to prevent $n(n-1)/2$ connections.
        
    - If the routers are on a point-to-point link, they move on immediately.
        

### 4. The Dead Interval

If a router doesn't hear from a neighbor for the duration of the **Dead Interval** (usually 4x the Hello interval, or 40s), it declares the neighbor "Dead," clears it from the LSDB, and triggers a new Dijkstra calculation.