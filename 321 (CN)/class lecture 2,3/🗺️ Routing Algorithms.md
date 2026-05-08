# 🗺️ Routing Algorithms

A routing algorithm is the "brain" of the Network Layer. It's the piece of software that runs on routers and decides the best path to forward a packet towards its ultimate destination. The output of a routing algorithm is a **routing table**, which tells the router which output link to use for each possible destination.

---

## Desired Properties of a Routing Algorithm

An ideal routing algorithm should be:
- **Correct:** It must find a valid path if one exists.
- **Simple:** Easy to understand and implement without a lot of overhead.
- **Robust:** Able to handle network failures (routers crashing, links breaking) and changes in topology without bringing the whole network down. It should converge to a new, stable solution quickly after a change.
- **Stable:** The algorithm should find a long-lasting equilibrium and not oscillate between different paths.
- **Fair:** It should allocate network resources equitably among different users.
- **Optimal:** It should be able to select the "best" path according to some metric.

---

## The Conflict of Metrics: Fairness vs. Optimality

The properties of **fairness** and **optimality** are often in direct conflict.

Consider the network diagram from the lecture, where we want to send data from `A` to `A'`, `B` to `B'`, and `C` to `C'`.
- An **optimal** solution might be to send all the traffic through the shortest path, potentially overloading a central link. This maximizes total throughput but might mean one flow gets all the bandwidth while others get none.
- A **fair** solution would ensure each flow gets an equal share of the network resources, even if it means sending some flows on longer, less "optimal" paths.

![Fairness vs Optimality](https://i.imgur.com/L7p4W5g.png)
*As shown in the notes, sending all vertical flows through the central horizontal line might be optimal for throughput but is unfair to the `X-X'` flow.*

---

## The Conflict of Metrics: Delay vs. Throughput

Another common conflict is between minimizing delay and maximizing throughput.

1.  To **maximize throughput** (the total amount of data moved), the algorithm will try to use every link to its absolute maximum capacity.
2.  However, when network links and router queues are close to full capacity, **queuing delay** skyrockets. A packet might arrive at a router and have to wait a long time in a buffer before it can be forwarded.
3.  This increased queuing delay leads to a higher **total delay** (latency) for the packets.

So, maximizing throughput can directly lead to an increase in delay, and vice-versa. Network administrators must often find a balance that is "good enough" for both.

### Real-World Simulation: Highway Traffic
- **Maximizing Throughput:** Imagine packing as many cars as possible onto a highway, bumper to bumper. You have the maximum number of cars on the road (high throughput).
- **The Result:** The highway is completely jammed. It takes a very long time for any single car to get from start to finish (high delay).
- **The Trade-off:** To reduce delay, you need some space between cars, which means you can't have the absolute maximum number of cars on the road at once.

### Video Resource
- **A good introduction to routing paths and costs:** [Intro to Routing and Switching by CBT Nuggets](https://www.youtube.com/watch?v=1Oa_o2-D1rQ)
