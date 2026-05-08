# Link State Routing (LSR): The "Global Map" Approach

Unlike DVR, where you just trust your neighbors' rumors, LSR requires every router to learn the entire network topology. Page 24 covers the first three operational steps and the trade-offs in measuring link costs.

## 1. Step 1: Discovering Neighbors

When a router boots up, it doesn't know who its neighbors are.

- **The HELLO Packet**: It sends a special `HELLO` packet on all its point-to-point lines.
    
- **The Response**: Every router that receives this responds with its unique ID. Now, the router has a list of "who is next to me."
    

## 2. Step 2: Measuring Line Cost

To find the "shortest" path, we need a metric. LSR uses **ECHO packets** to measure **Round Trip Time (RTT)**.

### The Queuing Problem

Every router interface has a **queue** (a buffer in memory). When packets arrive faster than the link can transmit them, they sit in this queue waiting their turn. This introduces **Queuing Delay**.

**The Timing Dilemma (When to start the ECHO timer?):**

1. **When the packet is queued**: The timer starts the moment the ECHO packet enters the buffer.
    
    - **Result**: The measured RTT includes the time spent waiting behind other traffic.
        
    - **Effect**: The link looks "expensive" if it is congested. This enables **Load Balancing** but causes **Oscillation**.
        
2. **When the packet hits the wire**: The timer starts only when the ECHO packet reaches the front of the queue.
    
    - **Result**: The measured RTT reflects only the physical propagation and transmission delay.
        
    - **Effect**: The cost is stable but ignores network congestion.
        

### The Load Balancing / Oscillation Problem

Your notes show a diagram of paths A-B and C-D. If we include queuing delay in our cost:

1. **Empty Link**: Path 1 is empty $\rightarrow$ Queuing delay is 0 $\rightarrow$ Cost is low.
    
2. **Sudden Load**: Every router shifts traffic to Path 1 because it's "cheapest."
    
3. **Congestion**: Path 1 is now backed up. The next ECHO packet spends a long time in the queue $\rightarrow$ Reported cost is now massive.
    
4. **The Flip**: Routers see the high cost and move _all_ traffic to Path 2.
    
5. **Oscillation**: Path 2 gets congested, Path 1 clears up, and the traffic bounces back and forth indefinitely.
    

**The Solution**: Instead of moving 100% of traffic, **split traffic** over multiple lines proportionally (e.g., 60% on Path A, 40% on Path B) to keep queues stable.

## 3. Step 3: Constructing Link State Packets (LSP)

Once costs are measured, the router builds an **LSP** to tell the rest of the world what it found.

**An LSP contains:**

- **ID**: Source router identification.
    
- **Sequence Number**: Incremented for every new LSP to distinguish new info from old info.
    
- **Age**: Decremented over time; when it hits zero, the info is discarded (prevents "zombie" routes).
    
- **Neighbor List**: A list of `(Neighbor_ID, Cost)` pairs for every active link.
    

### Why does this matter?

If you don't account for queuing properly, your Dijkstra calculation will use "jittery" data, leading to a network that is constantly rerouting and dropping packets.