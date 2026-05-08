# Week 2: Routing Protocols - DVR vs LSR

## Overview: Two Approaches to Routing

Modern networks use two main routing approaches:
1. **Distance Vector Routing (DVR)** - Share cost information with neighbors
2. **Link State Routing (LSR)** - Share topology information with everyone

Think of it like navigation:
- **DVR**: Asking directions from locals at each intersection
- **LSR**: Having a complete map and calculating your own route

---

## 1. Distance Vector Routing (DVR)

### Core Concept

Each router only knows:
- Its direct neighbors
- The cost to reach each neighbor
- What its neighbors say about reaching other destinations

**Real-World Analogy:**  
You're in a new city. You ask a local: "How far to the museum?"  
They reply: "I don't know exactly, but the museum is 5 miles from the train station, and the train station is 2 miles from here."  
You calculate: "So it's about 7 miles total."

### How DVR Works

**Key Algorithm**: Bellman-Ford

**The Update Rule:**
$$D_x(y) = \min_v \{ \text{cost}(x,v) + D_v(y) \}$$

**In plain English:**  
Router X's cost to reach destination Y = minimum of (cost from X to neighbor V + V's cost to reach Y)

**Example Calculation:**

```
Network:
    A --3-- B --2-- C

Router A wants to reach C:
- Direct: No direct link (cost = ∞)
- Via B: cost(A,B) + cost(B,C) = 3 + 2 = 5

A stores: Distance to C = 5, via B
```

### DVR Step-by-Step Example

**Initial Network:**
```
    A --1-- B
    |       |
    2       3
    |       |
    C ------+
       4
```

**Initial Distance Vectors:**

| Router | To A | To B | To C |
|--------|------|------|------|
| A | 0 | 1 | 2 |
| B | 1 | 0 | 3 |
| C | 2 | 3 | 0 |

**Router A's Perspective:**
- "I can reach myself (A) at cost 0"
- "I can reach B directly at cost 1"
- "I can reach C directly at cost 2"

**Router A shares this with neighbors B and C**

**Router B updates:**
- "To reach C: My direct cost is 3"
- "Via A: cost(B,A) + A's_cost(A,C) = 1 + 2 = 3"
- "Both paths cost 3, I'll keep my current route"

### Pros of DVR

| Advantage | Explanation | Real Impact |
|-----------|-------------|-------------|
| ✅ **Simple Logic** | Easy to understand and implement | Cheaper routers, less CPU needed |
| ✅ **Low Memory** | Only store one table of distances | Works on resource-limited devices |
| ✅ **Distributed** | No central control needed | Survives network partitions better |
| ✅ **Automatic Updates** | Neighbors share info automatically | No manual configuration |

### Cons of DVR

| Disadvantage | Explanation | Real Impact |
|--------------|-------------|-------------|
| ❌ **Slow Convergence** | Takes many rounds to stabilize | Minutes to update after failure |
| ❌ **Count-to-Infinity** | Bad news spreads slowly | Routing loops during failures |
| ❌ **Routing Loops** | Packets can bounce between routers | Temporary network dysfunction |
| ❌ **Periodic Overhead** | Sends full table every 30 seconds | Wastes bandwidth |
| ❌ **No Full Topology View** | Can't make intelligent global decisions | Suboptimal paths possible |

### The Count-to-Infinity Problem

**Scenario**: Link between A and B fails

```
Before Failure:
    A --1-- B --1-- C

A's table: B=1, C=2
B's table: A=1, C=1
C's table: A=2, B=1
```

**What Happens:**

1. **Link A-B breaks**
2. **Round 1:**
   - A notices B is unreachable directly
   - A sees C's old vector: "C says A is 2 hops away"
   - A thinks: "I can reach B via C!" (WRONG - this path goes through A!)
   - A sets: B=3 (via C)

3. **Round 2:**
   - C hears from A: "A says B is 3 hops away"
   - C updates: B=4 (via A)

4. **Round 3:**
   - A hears from C: "C says B is 4 hops away"
   - A updates: B=5 (via C)

**This continues incrementing until reaching infinity (typically 16 in RIP)!**

### Solutions to Count-to-Infinity

#### Solution 1: Split Horizon

**Rule**: Don't advertise a route back to the neighbor you learned it from.

**Example:**
```
A learned about D from B.
A will NOT tell B about D.
(Because B already knows about D!)
```

**Effectiveness:**
- ✅ Prevents 2-node loops
- ❌ Doesn't prevent 3+ node loops

#### Solution 2: Split Horizon with Poison Reverse

**Rule**: Advertise a route back to the source, but with infinite cost.

**Example:**
```
A learned: "D is reachable via B"
A tells B: "D is unreachable (cost = ∞) from my perspective"
```

**Why this helps:**
- If B's route to D fails, B won't try to route through A

**Effectiveness:**
- ✅ Better than split horizon
- ❌ Still doesn't solve all loops
- ❌ Uses more bandwidth

#### Solution 3: Hold-Down Timers

**Rule**: After hearing a route is down, wait before accepting new routes to that destination.

**Example:**
```
1. A hears: "Route to D is down"
2. A starts 60-second timer
3. During this time, A ignores any new routes to D
4. After timer expires, A accepts new routes
```

**Why this helps:**
- Gives time for bad news to propagate everywhere
- Prevents accepting stale information

**Trade-off:**
- Slower convergence (waiting period)

#### Solution 4: Limit Infinity

**Rule**: Define infinity as a small number (RIP uses 16).

**Why:**
- Prevents counting forever
- Network converges faster
- Trade-off: Limits network diameter to 15 hops

### Real-World Protocol: RIP (Routing Information Protocol)

**Key Facts:**
- **Uses**: Distance Vector Routing
- **Metric**: Hop count only (all links = 1 hop)
- **Updates**: Every 30 seconds
- **Infinity**: 16 hops
- **Port**: UDP 520

**RIP Limitations:**

| Limitation | Impact |
|------------|--------|
| Max 15 hops | Can't use in large networks |
| Only hop count | Ignores bandwidth/delay |
| Slow convergence | 1-3 minutes after failure |
| Bandwidth waste | Full table every 30 seconds |

**When RIP is used:**
- Small networks (< 15 routers)
- Home/office networks
- Simple topology
- Legacy systems

**Monitor RIP in Linux:**
```bash
sudo tcpdump -i any port 520 -v
# You'll see routers broadcasting their distance vectors
```

---

## 2. Link State Routing (LSR)

### Core Concept

Each router:
1. Discovers all its neighbors
2. Measures the cost to each neighbor
3. Broadcasts this info to EVERYONE in the network
4. Receives everyone else's info
5. Builds a complete network map
6. Runs Dijkstra's algorithm to find shortest paths

**Real-World Analogy:**  
Everyone shares their local street information. You piece it together to create a complete city map. Then you calculate the best route yourself using the map.

### How LSR Works: 5 Steps

#### Step 1: Discover Neighbors

**Method**: Send "Hello" packets on all interfaces

**Example:**
```
Router A sends Hello on all ports.
Routers B, C, and D respond.
Router A now knows: "I have neighbors B, C, D"
```

#### Step 2: Measure Link Costs

**Methods:**
- Count hops (all links = 1)
- Measure delay (send test packets, measure round-trip time)
- Check bandwidth (higher bandwidth = lower cost)
- Manual configuration

**Example:**
```
A tests link to B: 5ms delay → cost = 5
A tests link to C: 10ms delay → cost = 10
```

#### Step 3: Build Link State Packet (LSP)

**LSP Contents:**
- Router ID (who is sending this)
- Sequence number (to detect duplicates)
- Age (time-to-live)
- List of neighbors and costs

**Example LSP from Router A:**
```
{
  "Router": "A",
  "Sequence": 42,
  "Age": 3600,
  "Links": [
    {"Neighbor": "B", "Cost": 1},
    {"Neighbor": "C", "Cost": 4}
  ]
}
```

#### Step 4: Flood LSPs to Everyone

**Process:**
1. Router A creates LSP
2. A sends LSP to all neighbors
3. Each neighbor forwards to their neighbors
4. Uses sequence numbers to prevent duplicates
5. Eventually everyone has everyone's LSP

**How to Draw the Flooding:**

```
Time 0: A creates LSP #42
        [A]
        / \
       B   C

Time 1: A sends to B and C
        [A]→LSP→[B]
        [A]→LSP→[C]

Time 2: B and C forward to their neighbors
        [B]→LSP→[D]
        [C]→LSP→[D]

Time 3: D receives LSP from both B and C
        D accepts first copy, discards second (same seq#)
```

#### Step 5: Run Dijkstra's Algorithm

Each router independently runs Dijkstra on the complete topology map.

**Example:**
```
Network map (everyone has this):
    A --1-- B
    |       |
    4       2
    |       |
    C --1-- D

Each router runs Dijkstra from their own perspective:
- Router A calculates shortest paths from A to all others
- Router B calculates shortest paths from B to all others
- etc.
```

### Pros of LSR

| Advantage | Explanation | Real Impact |
|-----------|-------------|-------------|
| ✅ **Fast Convergence** | Typically < 1 second | Minimal downtime during failures |
| ✅ **Loop-Free** | Dijkstra guarantees no loops | Reliable routing |
| ✅ **Complete View** | Every router has full topology | Better routing decisions |
| ✅ **Event-Driven** | Only send updates when changes occur | Efficient bandwidth use |
| ✅ **Scalable** | Works in large networks | Used across the Internet |
| ✅ **Flexible Metrics** | Can use any cost function | Optimize for delay, bandwidth, etc. |

### Cons of LSR

| Disadvantage | Explanation | Real Impact |
|--------------|-------------|-------------|
| ❌ **Complex** | More complicated logic | Requires more powerful routers |
| ❌ **Memory Intensive** | Must store complete topology | Higher memory requirements |
| ❌ **CPU Intensive** | Running Dijkstra is expensive | More processing power needed |
| ❌ **Initial Flood** | Startup generates lots of traffic | Network congestion at boot |

### Real-World Protocol: OSPF (Open Shortest Path First)

**Key Facts:**
- **Uses**: Link State Routing + Dijkstra
- **Metric**: Cost (configurable, typically based on bandwidth)
- **Updates**: Event-triggered (when topology changes)
- **Areas**: Hierarchical design for large networks
- **Protocol**: IP protocol 89

**OSPF Features:**

| Feature | Benefit | Use Case |
|---------|---------|----------|
| **Areas** | Divide large networks | Reduce flooding overhead |
| **Load Balancing** | Use multiple equal-cost paths | Better resource utilization |
| **Authentication** | MD5/SHA password protection | Prevent rogue routers |
| **Fast Convergence** | Sub-second failover | High-availability networks |

**OSPF Network Design:**

```
        [Area 0 - Backbone]
              |
    +---------+---------+
    |         |         |
[Area 1]  [Area 2]  [Area 3]
(Sales)   (Engineering) (HR)
```

**Why Areas?**
- Limit flooding scope (Area 1 changes don't flood Area 2)
- Reduce routing table size
- Improve scalability

**OSPF Cost Calculation:**
```
Cost = Reference Bandwidth / Interface Bandwidth
Default Reference = 100 Mbps

Examples:
- 10 Mbps Ethernet: Cost = 100/10 = 10
- 100 Mbps FastEthernet: Cost = 100/100 = 1
- 1000 Mbps GigEthernet: Cost = 100/1000 = 1 (min cost)
```

**Monitor OSPF in Linux:**
```bash
sudo tcpdump -i any proto ospf -v
# or
sudo tcpdump -i any proto 89 -v
# You'll see Hello packets, LSA updates, etc.
```

---

## 3. DVR vs LSR: Complete Comparison

### Quick Reference Table

| Feature | Distance Vector (DVR) | Link State (LSR) |
|---------|----------------------|------------------|
| **Algorithm** | Bellman-Ford | Dijkstra |
| **Knowledge** | Neighbors' distances only | Complete network topology |
| **Updates** | Periodic (every 30s in RIP) | Event-driven (when changes occur) |
| **What's Shared** | Entire distance table | Only neighbor links |
| **Who Receives** | Direct neighbors only | Everyone (flooding) |
| **Convergence** | Slow (minutes) | Fast (sub-second) |
| **Loops** | Possible (count-to-infinity) | Never (Dijkstra is loop-free) |
| **Memory** | Low (one table) | High (complete topology database) |
| **CPU** | Low (simple math) | High (Dijkstra computation) |
| **Bandwidth** | Moderate (periodic full tables) | Low (small LSPs, event-driven) |
| **Scalability** | Limited (hop limits) | Excellent (with hierarchical design) |
| **Real Protocol** | RIP, EIGRP | OSPF, IS-IS |
| **Best For** | Small, simple networks | Large, complex networks |

### Detailed Feature Comparison

#### Routing Table Size

**DVR:**
- One entry per destination
- Contains: Destination, Cost, Next Hop
- Example: 100 destinations = 100 entries
- **Size**: Moderate

**LSR:**
- Two data structures:
  1. Link State Database (complete topology)
  2. Routing table (forwarding info)
- LSDB contains ALL routers and links
- Example: 100 routers with 3 links each = 300 link entries
- **Size**: Larger

**Real Impact:**
- DVR: 1 MB memory sufficient
- LSR: 10+ MB memory needed for large networks

#### Knowledge & View

**DVR: Local/Decentralized View**
```
Router A's perspective:
"I know:
 - B is 1 hop away
 - B says C is 2 hops away
 - Therefore, C is 3 hops via B"

A doesn't know the actual path or alternate routes.
```

**LSR: Global/Centralized View**
```
Every Router's perspective:
"I have the complete map:
    A --1-- B --2-- C
    |               |
    4               3
    |               |
    D ------5------ E

I can calculate all possible paths."
```

**Real Impact:**
- DVR: Simple but limited optimization
- LSR: Complex but optimal routing

#### Convergence Speed Example

**Scenario**: Link fails between routers

**DVR (RIP):**
```
Time 0: Link fails
Time 30s: First neighbor notices (next update cycle)
Time 60s: Second-hop neighbors update
Time 90s: Third-hop neighbors update
...
Total: 1-3 minutes until all routers converge
```

**LSR (OSPF):**
```
Time 0: Link fails
Time 0.1s: Router detects failure (Hello timeout)
Time 0.2s: LSP flooded to all routers
Time 0.5s: All routers run Dijkstra
Time 1s: New routes installed
Total: < 1 second until convergence
```

**Real Impact:**
- DVR: Minutes of potential packet loss
- LSR: Sub-second failover (barely noticeable)

#### Overhead Comparison

**DVR Overhead:**
- **When**: Every 30 seconds (RIP)
- **What**: Full routing table (all destinations)
- **Size**: Large (proportional to network size)
- **To Whom**: All direct neighbors

**Example:**
```
100 destinations × 10 bytes/entry = 1 KB
Every 30 seconds to 3 neighbors = 3 KB every 30s
= 800 bits/second continuous overhead
```

**LSR Overhead:**
- **When**: Only when topology changes
- **What**: Small Link State Packet (LSP)
- **Size**: Tiny (just neighbor links)
- **To Whom**: Everyone (but rare)

**Example:**
```
3 links × 20 bytes/link = 60 bytes per LSP
Sent only when changes occur (maybe once per hour)
= ~0.1 bits/second average overhead
```

**Real Impact:**
- Stable network: LSR uses 1000× less bandwidth
- Unstable network: LSR might use more (frequent flooding)

### When to Use Each

#### Use DVR (RIP) When:

✅ **Small Networks**
- < 15 routers
- Simple topology
- Low requirements

✅ **Resource-Constrained Devices**
- Old routers with limited CPU/memory
- IoT devices
- Embedded systems

✅ **Simplicity Matters**
- Easy to configure
- Easy to troubleshoot
- Minimal training needed

**Real Examples:**
- Home networks
- Small office (< 50 devices)
- Lab environments
- Legacy systems

#### Use LSR (OSPF) When:

✅ **Large Networks**
- Hundreds or thousands of routers
- Complex topology
- Multiple paths

✅ **Fast Convergence Needed**
- Mission-critical applications
- Real-time services (VoIP, video)
- High-availability requirements

✅ **Bandwidth is Precious**
- Expensive WAN links
- Satellite connections
- Limited bandwidth

✅ **Advanced Features Needed**
- Load balancing
- QoS support
- Hierarchical design
- Authentication

**Real Examples:**
- Internet Service Providers (ISPs)
- Enterprise corporate networks
- Data centers
- University campuses
- Government networks

---

## 4. Practical Skills: Working with Routing

### View Your Routing Table (Linux)

**Command:**
```bash
route -n
# or
ip route show
```

**Example Output:**
```
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    100    0        0 eth0
192.168.1.0     0.0.0.0         255.255.255.0   U     0      0        0 eth0
```

**What it means:**
- `0.0.0.0` (default route): Send all unknown traffic to 192.168.1.1 (your home router)
- `192.168.1.0/24`: Local network, directly connected
- `Metric`: Cost (lower is better)
- `Iface`: Network interface to use

### Monitor RIP Traffic

**Command:**
```bash
sudo tcpdump -i any port 520 -v
```

**What you'll see:**
```
RIPv2, Response, length: 124
  Destination 10.0.1.0, mask 255.255.255.0, metric 1, next-hop self
  Destination 10.0.2.0, mask 255.255.255.0, metric 2, next-hop self
```

**Meaning:**
- Routers broadcasting their distance vectors
- Every 30 seconds
- Lists all known destinations and costs

### Monitor OSPF Traffic

**Command:**
```bash
sudo tcpdump -i any proto 89 -v
# or
sudo tcpdump -i any proto ospf -v
```

**What you'll see:**
```
OSPFv2, Hello, length 48
  Router-ID 1.1.1.1, Backbone Area
  Options: E
  Hello Timer: 10s, Dead Timer: 40s

OSPFv2, LS-Update, length 124
  Advertising Router 2.2.2.2
  Link State Advertisement:
    Type: Router-LSA
    Age: 5s
```

**Meaning:**
- Hello packets: Neighbor discovery (every 10s)
- LS-Updates: Topology changes (when they occur)
- Much less frequent than RIP updates

### Debug Routing Issues

**Problem**: Can't reach a destination

**Step 1**: Check routing table
```bash
ip route get 8.8.8.8
# Shows which route will be used
```

**Step 2**: Trace the path
```bash
traceroute 8.8.8.8
# Shows all hops along the path
```

**Step 3**: Check if routing protocol is running
```bash
# For RIP
sudo netstat -an | grep 520

# For OSPF
sudo netstat -an | grep 89
```

---

## 5. Advanced Topics

### Hierarchical OSPF with Areas

**Problem**: In very large networks, flooding LSPs to everyone is expensive.

**Solution**: Divide network into Areas.

**Area Design:**
```
          Internet
             |
    [Area 0 - Backbone]
    (Core routers only)
             |
    +--------+--------+
    |        |        |
[Area 1] [Area 2] [Area 3]
(Branch1) (Branch2) (HQ)

Each area = 10-50 routers
Total network = 150 routers
```

**How it works:**
- **Intra-area**: Full LSP flooding within area
- **Inter-area**: Summary routes only
- **Area 0**: Must exist, connects all other areas
- **ABR** (Area Border Router): Connects areas

**Benefits:**
| Benefit | Explanation |
|---------|-------------|
| **Reduced Flooding** | Topology change in Area 1 doesn't flood Area 2 |
| **Smaller LSDB** | Each router only stores full topology of its area |
| **Faster Convergence** | Fewer routers to recalculate |
| **Better Scalability** | Can support thousands of routers |

### EIGRP: Hybrid Approach

**EIGRP (Enhanced Interior Gateway Routing Protocol)** combines DVR and LSR features.

**Characteristics:**
- Uses distance vector approach (like RIP)
- But maintains topology table (like OSPF)
- Fast convergence (like OSPF)
- Lower overhead than OSPF
- Cisco proprietary (though opened in 2013)

**When to use:**
- Cisco-only networks
- Want DVR simplicity with LSR performance
- Medium-sized networks (50-500 routers)

---

## 6. Summary: Key Takeaways

### The Big Picture

**Distance Vector Routing:**
- 🎯 Simple and lightweight
- 📍 Local knowledge only
- 🐌 Slow to converge
- 🏘️ Best for small networks
- 🔄 Examples: RIP, EIGRP (hybrid)

**Link State Routing:**
- 🎯 Complex but optimal
- 🗺️ Complete network map
- ⚡ Fast convergence
- 🏙️ Best for large networks
- 🔄 Examples: OSPF, IS-IS

### Decision Matrix

| Network Size | Best Choice | Why |
|--------------|-------------|-----|
| < 15 routers | DVR (RIP) | Simple, sufficient |
| 15-100 routers | LSR (OSPF) | Better performance |
| 100+ routers | LSR with Areas (OSPF) | Scalability |
| Cisco-only | EIGRP | Good balance of features |

### Quick Problem Solver

**Symptom → Likely Cause → Solution**

| Problem | DVR Issue | LSR Issue |
|---------|-----------|-----------|
| **Slow convergence** | Count-to-infinity | LSDB too large → use areas |
| **Routing loops** | Lack of split horizon | Shouldn't happen → check config |
| **High bandwidth use** | Periodic updates | Flapping links → dampen |
| **CPU high** | N/A | Frequent recalculation → stabilize topology |

### Commands Cheat Sheet

```bash
# View routing table
route -n
ip route show

# Trace packet path
traceroute <destination>
mtr <destination>  # Better traceroute

# Monitor RIP
sudo tcpdump port 520 -v

# Monitor OSPF
sudo tcpdump proto 89 -v

# Check specific route
ip route get <destination>

# Add static route (temporary)
sudo ip route add 10.0.0.0/8 via 192.168.1.1

# Delete route
sudo ip route del 10.0.0.0/8
```

---

## Next Steps

**Practice Exercises:**
1. Draw a network topology with 6 routers
2. Run DVR by hand (calculate distance vectors)
3. Run Dijkstra by hand on the same topology
4. Compare the convergence time when a link fails

**Further Study:**
- BGP (Border Gateway Protocol) - for inter-ISP routing
- MPLS (Multi-Protocol Label Switching) - combines benefits of both
- SDN (Software-Defined Networking) - centralized routing control

**Real-World Labs:**
- Use GNS3 or Packet Tracer to simulate OSPF
- Configure RIP on old routers
- Observe convergence with Wireshark