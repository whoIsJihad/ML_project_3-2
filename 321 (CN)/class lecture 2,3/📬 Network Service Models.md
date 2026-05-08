# 📬 Network Service Models

At the network layer, there are two fundamental approaches to delivering packets: a **Connection-Oriented** service and a **Connectionless** service. This choice defines how packets are routed and what kind of guarantees the network can offer.

---

## 1. Connectionless Service (Datagram Subnets)

This is the model used by the internet (IP). Each packet, called a **datagram**, is treated as a completely independent entity.

- **No Setup Required:** A host can start sending packets to a destination at any time without prior notification to the network.
- **Independent Routing:** Each packet is routed individually. Routers make a fresh decision for every packet based on its destination address and the current state of the network.
- **Packets Can Take Different Paths:** Because of independent routing, two packets from the same source to the same destination might travel through completely different sets of routers. This can lead to packets arriving out of order.
- **No Guarantees:** The network gives its "best effort" to deliver the packet but makes no promises. Packets can be dropped, duplicated, or arrive out of order. Reliability is the responsibility of the transport layer (e.g., TCP).



### Real-World Analogy: Sending Postcards
Sending datagrams is like mailing a series of postcards. You drop them all in the mailbox. Each one is handled independently by the postal service. Some might go by plane, some by truck. They will probably arrive, but there's no guarantee they will arrive in the order you sent them, and one might get lost.

---

## 2. Connection-Oriented Service (Virtual Circuit Subnets)

This model involves establishing a dedicated path, called a **Virtual Circuit (VC)**, before any data is sent.

- **Setup Phase Required:** A "call setup" request is sent into the network to establish a path from source to destination. This path is a fixed sequence of routers.
- **Packets Follow the Same Path:** All packets belonging to the same connection follow this pre-determined virtual circuit. They are identified by a small Virtual Circuit Identifier (VCI) in their header, not a full destination address.
- **Guaranteed Resources (Potentially):** During setup, resources like bandwidth or buffer space can be reserved at each router. This makes it possible to offer Quality of Service (QoS) guarantees, which is important for things like streaming video or voice calls.
- **Less Overhead per Packet:** Since the full destination address isn't needed in each packet (just the small VCI), the headers are smaller.


### Real-World Analogy: A Phone Call
Establishing a virtual circuit is like making a phone call. You first dial the number and wait for the connection to be established. Once it is, you have a dedicated line for your conversation. All your words (packets) travel in order over that same line until you "hang up" (terminate the connection).

---

## Comparison Table

| Feature                | Datagram Subnet (Connectionless)       | Virtual Circuit Subnet (Connection-Oriented) |
| ---------------------- | -------------------------------------- | ---------------------------------------------- |
| **Circuit Setup**      | Not needed                             | Required                                       |
| **Addressing**         | Each packet has the full destination address | Each packet has a small VCI                  |
| **State Information**  | Routers don't hold state about connections | Each router must maintain state for active VCs |
| **Routing**            | Each packet is routed independently      | All packets in a VC follow the same path       |
| **Effect of Failure**  | Packets can be routed around failures   | All VCs passing through the failed router die  |
| **Quality of Service** | Difficult to achieve                   | Easier to implement with resource reservation  |

