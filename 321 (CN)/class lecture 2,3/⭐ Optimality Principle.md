# ⭐ Optimality Principle

The Optimality Principle is a foundational and intuitive concept in routing. It provides a sanity check for routing algorithms and helps us understand the structure of optimal paths in a network.

---

## The Principle

The principle states:

> If router `J` is on the optimal path from router `I` to router `K`, then the optimal path from `J` to `K` is also the part of that same path.

In simpler terms, if the best way to get from New York to Los Angeles is through Chicago, then the best way to get from Chicago to Los Angeles must be that same route from Chicago onwards. If there were a better way to get from Chicago to LA, you would have used it for the original New York to LA trip as well.

---

## Sink Trees

As a direct consequence of the Optimality Principle, we can see that the set of optimal routes from all other nodes to a single destination `(K)` forms a tree rooted at that destination. This tree is called a **sink tree**.

- A sink tree is a specific type of spanning tree (a tree that connects all nodes in the graph without any cycles).
- It contains no loops.
- For a given destination, the sink tree shows the best path from every other node to that destination.
- Routing algorithms work to discover and use these sink trees. The collection of all sink trees for all routers is the goal.



Each router calculates its own sink tree to all possible destinations, and this calculation is the primary job of any [[🗺️ Routing Algorithms|routing algorithm]]. The resulting paths from these trees are then used to build the router's forwarding table.

### Real-World Example: GPS Navigation
When your GPS calculates the fastest route from your home to the airport, it's essentially building a sink tree with the airport as the destination. The Optimality Principle guarantees that if your calculated route takes you through a specific intersection, the rest of the route from that intersection to the airport is also the fastest possible. The GPS doesn't need to re-calculate from scratch at every traffic light; it just follows the pre-computed optimal path (the branch of the sink tree) you are on.
