# 🚦 Packet Switching

Packet switching is the dominant method for data transmission in computer networks. The most common form of this is **Store-and-Forward Packet Switching**.

---

## How Store-and-Forward Works

Instead of having a dedicated, continuous connection, messages are broken down into smaller pieces called **packets**. Each packet travels independently through the network.

A router in the network must receive the **entire packet** and store it in its memory (store) before it can process it and send it along the next link in the path (forward).

1.  **Receive:** The router receives an incoming packet on one of its interfaces.
2.  **Store:** The router copies the entire packet to its internal memory (RAM).
3.  **Process:** The router examines the packet's header to determine its destination address. It consults its [[🗺️ Routing Algorithms|routing table]] to decide which output link to use.
4.  **Forward:** The router places the packet in the queue for the chosen output link and transmits it once the link is free.



### Advantages:
- **Efficiency:** Network links are shared among many users, leading to better utilization of bandwidth compared to dedicated circuits.
- **Resilience:** If one path fails, packets can be dynamically rerouted around the failure.

### Disadvantages:
- **Variable Delay (Jitter):** Since packets may have to wait in queues at each router, the time it takes for them to arrive can be unpredictable. This can be problematic for real-time applications like video calls.
- **Overhead:** Each packet needs a header with source, destination, and other control information, which adds to the total data being sent.

---

## Real-World Simulation: The Relay Race

Think of a relay race where runners (routers) must wait for their teammate to arrive and hand them the *entire* baton (packet) before they can start running their leg of the race. They can't start running while only holding a piece of it.


