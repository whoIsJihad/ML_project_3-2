# Solutions for Practice Questions

This file provides the answers to `Practice_Questions.md`.

---

## Part 1: Foundational Concepts (Easy)

1.  **Adaptive vs. Non-Adaptive:**
    -   **Non-Adaptive (Static)** algorithms have their routes computed in advance and are not based on real-time network conditions.
    -   **Adaptive (Dynamic)** algorithms change their routing decisions based on live changes in network topology and traffic.

2.  **Simplest Algorithm:**
    -   **Flooding** is the simplest algorithm.
    -   Its two main problems are **Exponential Traffic** (leading to congestion) and the potential for **Infinite Loops**.

3.  **DVR Table Columns:**
    1.  **Destination**: The target network/router.
    2.  **Distance (Metric)**: The cost to reach that destination.
    3.  **Next-Hop**: The neighbor to forward the packet to.

4.  **Dijkstra's in LSR:** In LSR, every router builds a complete map (the LSDB) of the network. Dijkstra's algorithm is then run locally on this map to independently calculate the shortest path from itself to every other destination.

5.  **"Open" in OSPF:** It means the protocol specification is public (an RFC) and not proprietary to a specific vendor. This ensures interoperability between different manufacturers' routers.

---

## Part 2: Mechanisms & Protocols (Medium)

1.  **Count-to-Infinity Explanation:**
    -   **Initial State:** In a network `A --- B --- C`, A knows it can reach C via B with a cost of 2. B knows it can reach C directly with a cost of 1.
    -   **Failure:** The link B-C fails. B correctly sets its distance to C to $\infty$.
    -   **Bad Timing:** Before B can inform A, A sends its regular update, telling B: "I can get to C in 2 hops."
    -   **The Loop Begins:** B sees this and thinks, "A has a path to C! If I go through A, my new path to C will cost 3 (1 to get to A + 2 from A)." B updates its table to `(Dest: C, Dist: 3, Next: A)`.
    -   **Escalation:** In the next update, B tells A: "I can get to C in 3 hops." A then updates its own cost to 4 (1 to B + 3 from B). This cycle continues until the metric reaches "infinity."

2.  **Split-Horizon:** This rule states: If a router learns about a route from a neighbor, it should not advertise that route back to the *same* neighbor. This directly prevents the simple two-node loop that causes the count-to-infinity problem.

3.  **Sequence Numbers in LSPs:**
    1.  **Old vs. New Information:** They allow a router to distinguish between an outdated (stale) LSP and a fresh one. A router will only accept an LSP if it has a strictly higher sequence number than the one it currently has stored.
    2.  **Infinite Loops:** By discarding LSPs with older or duplicate sequence numbers, they prevent a packet from being flooded endlessly in a loop.

4.  **Role of the "Age" Field:** The Age field is a TTL (Time-To-Live) for an LSP. It acts as a garbage collector.
    -   **Scenario:** A router (R1) sends out LSPs, reaching sequence number 5000. It then crashes and reboots, starting its sequence number back at 0. Without the Age field, other routers would still hold the LSP with sequence 5000 and would reject R1's new LSPs (since 0 < 5000), effectively isolating R1 from the network forever.
    -   **Solution:** With the Age field, the old LSPs from before the crash are not refreshed by R1. They eventually "age out" (Age=0) and are purged from all routers' databases. Now, R1's new LSPs (starting at sequence 0) are accepted because there's no older information to compare against.

5.  **OSPF Hello Packet Matching Parameters:** Any two from this list are critical:
    -   Hello/Dead Intervals
    -   Area ID
    -   Authentication (password/type)
    -   Subnet Mask

6.  **Flooding Control:** The most effective method is using a **History Table** that stores the `(Source Address, Sequence Number)` for each packet. When a packet arrives, the router checks its table. If the tuple is already in the table, the packet is a duplicate and is **discarded**. If not, the table is updated, and the packet is forwarded.

7.  **Fairness vs. Optimality:**
    -   **Conflict:** A routing algorithm designed for **Optimality** (maximizing total network throughput) might starve a long-distance flow to prioritize multiple short-distance flows that use fewer resources per packet. This achieves high overall packet delivery but is unfair to the long-distance flow.
    -   **Example:** Imagine one long cross-country data transfer and ten small local transfers that cross its path. An optimal algorithm might give all the bandwidth to the ten local transfers because they finish quickly, boosting the total number of "completed jobs," while the cross-country transfer gets no bandwidth. This is optimal for throughput but unfair to the single user.

---

## Part 3: Quizzes (Multiple Choice)

1.  **b) Poison Reverse**. It's more aggressive because instead of just not advertising a route back, it advertises it with an infinite metric.
2.  **c) Discard the LSP**. It is considered old or stale information.
3.  **b) 224.0.0.5**. This is the "AllSPFRouters" multicast address.
4.  **d) Both a) and c)**. By discarding packets after a certain number of hops, it prevents them from looping forever, which in turn reduces network congestion.
5.  **b) False**. The "shortest" path depends on the metric used for link weight (cost). It could be hops, delay, bandwidth, or physical distance.

---

## Part 4: Problem Solving (Hard)

**Problem 1: Dijkstra's Algorithm**

**Initial State:**
- Visited Set: {}
- Distances: {A:0, B:$\infty$, C:$\infty$, D:$\infty$}
- Predecessors: {A:null, B:null, C:null, D:null}

**Step 1:**
- Visit node **A**.
- Relax neighbors B and C.
- **Visited Set:** {A}
- **Distances:** {A:0, B:2, C:1, D:$\infty$}
- **Predecessors:** {B:A, C:A, D:null}

**Step 2:**
- Select smallest unvisited distance: **C (Dist: 1)**. Visit C.
- Relax neighbor D. New dist(D) = dist(C) + cost(C,D) = 1 + 3 = 4.
- **Visited Set:** {A, C}
- **Distances:** {A:0, B:2, C:1, D:4}
- **Predecessors:** {B:A, C:A, D:C}

**Step 3:**
- Select smallest unvisited distance: **B (Dist: 2)**. Visit B.
- Relax neighbor D. New dist(D) = dist(B) + cost(B,D) = 2 + 5 = 7. This is *not* smaller than the current dist(D) of 4, so we **do not update D**.
- **Visited Set:** {A, C, B}
- **Distances:** {A:0, B:2, C:1, D:4}
- **Predecessors:** {B:A, C:A, D:C}

**Step 4:**
- Visit the last node, **D**.
- **Visited Set:** {A, C, B, D}
- Algorithm terminates.

**Final Result:**
- Shortest Path A->B: Cost 2 (via A)
- Shortest Path A->C: Cost 1 (via A)
- Shortest Path A->D: Cost 4 (via C)

**Problem 2: Distance Vector Routing - "Count-to-Infinity"**

**Cycle 0: The Failure & Bad Update**
1.  **B-C Link Fails:** B updates its table: `(Dest: C, Dist: ∞, Next: -)`.
2.  **A sends its update to B:** A's table is still `(Dest: C, Dist: 2, Next: B)`.
3.  **B's Mistake:** B receives A's update. It thinks: "A can get to C in 2 hops. The cost to get to A is 1. Therefore, I can get to C via A with a cost of 1+2=3."
4.  **B Updates:** B's new table becomes `(Dest: C, Dist: 3, Next: A)`.

**Cycle 1: The First Lie**
1.  **B sends its new table to A:** B tells A: "I can get to C in 3 hops."
2.  **A's Mistake:** A's current path to C was through B. A thinks: "My path through B now costs 1+3=4."
3.  **A Updates:** A's new table becomes `(Dest: C, Dist: 4, Next: B)`.

**Cycle 2: The Loop Continues**
1.  **A sends its new table to B:** A tells B: "I can get to C in 4 hops."
2.  **B's Mistake:** B's current path is through A. B thinks: "My path through A now costs 1+4=5."
3.  **B Updates:** B's new table becomes `(Dest: C, Dist: 5, Next: A)`.

**Cycle 3: And On...**
1.  **B sends its new table to A:** B tells A: "I can get to C in 5 hops."
2.  **A's Mistake:** A's path through B now costs 1+5=6.
3.  **A Updates:** A's new table becomes `(Dest: C, Dist: 6, Next: B)`.

The cost for route C will now increment between A and B (4, 5, 6, 7, 8...) until it reaches the algorithm's definition of "infinity".
