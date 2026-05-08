
## 1. Computer Networks Definition
A Computer Network is defined as **a collection of nodes and connections**.

* **Node:** Any device capable of sending or receiving information (e.g., computers, servers, routers).
* **Connection:** The physical or logical link between nodes.
* **End System:** Nodes that sit at the edge of the network (e.g., your laptop, a server).

## 2. Protocols
Communication over a network is governed by a **set of rules and formats** known as a **Protocol**.

* A protocol ensures that the sender and receiver understand each other's data structure and communication procedures.
* *Crucially:* **A protocol may use another protocol in its execution** (e.g., HTTP uses TCP, which uses IP).

## 3. Layering
The form of dependency in a set of protocols is managed by **layering**.

This involves dividing the complex communication system into a stack of smaller, more manageable pieces (layers).

### Advantages of Layering
1.  **Allows Identification & Relationships:** It helps define clear identifiers and relationships between the complex system's pieces.
2.  **Eases Maintenance and Updating:** Changes in one layer (e.g., updating the Physical layer technology) generally do not require changes in other layers (e.g., the Application layer), easing maintenance and updating the entire system.

### Example Scenario: Classical Mailing System
This analogy helps illustrate layering and protocols:

| Component               | Network Analogy (Protocol/Layer)    | Role/Function                                                                        |
| :---------------------- | :---------------------------------- | :----------------------------------------------------------------------------------- |
| **Sender (Customer)**   | Application Layer                   | Writes the **Letter**.                                                               |
| **Letter in envelope**  | Transport Layer                     | The envelope acts as a "header" containing **address/metadata** needed for delivery. |
| **Post Box (local)**    | Network Layer (Local Router)        | First point of collection; determines the path.                                      |
| **Post Office (local)** | Network Layer (Local Router)        | Processes the item for forwarding.                                                   |
| **Post Office (city)**  | Network Layer (Intermediate Router) | Routes the item closer to the destination.                                           |
| **Post Office (local)** | Network Layer (Final Router)        | Final delivery point.                                                                |
| **Receiver**            | Application Layer                   | Receives and reads the **Letter**.                                                   |

### Next : [[🌐 The OSI Reference Model]]