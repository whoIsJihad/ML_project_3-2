# Deep Dive: The Hourglass & Store-and-Forward (Page 6)

This page focuses on the architectural philosophy of the **Network Layer (NL)** and the physical reality of packet movement.

### 1. The "Hourglass" Model (The Stack Diagram)

This diagram illustrates the **IP-over-anything, anything-over-IP** philosophy.

- **The Neck (Network Layer):** Notice it's the narrowest part. The goal is to keep NL functionality **minimal**. It only needs to do one thing well: **Routing** (moving packets from source to destination).
    
- **Upper Layers (AL/TL):** These are wide because there are hundreds of applications and protocols (HTTP, FTP, TCP, UDP).
    
- **Lower Layers (DLL/PL):** These are wide because there are many physical mediums (Fiber, WiFi, Ethernet).
    
- **The Logic:** By keeping the NL simple (the "thin neck"), it acts as a universal bridge, allowing any application to run over any physical hardware.
    

### 2. Store-and-Forward Packet Switching

The diagram with $H_1, H_2$ and Routers $A-F$ shows the "Subnet" in action.

- **Host vs. Router:** $H_1$ and $H_2$ are "End Systems." They generate the data. The routers ($A, B, C...$) are the "Intermediate Nodes."
    
- **The Process:** 1. $H_1$ sends a packet to Router $A$. 2. Router $A$ **stores** the entire packet in its buffer. 3. It checks the checksum (error detection). 4. It consults its routing table and **forwards** it to the next hop (e.g., Router $B$ or $C$).
    
- **The Subnet:** The collection of routers and communication lines (carrier equipment) is explicitly labeled as the **Subnet**. The hosts are _not_ part of the subnet.
    

### 3. Service Abstraction

The text at the bottom confirms that the Network Layer's job is to "shield" the Transport Layer.

- **Independence:** The TL doesn't need to know if the subnet is a mess of fiber or copper, or if there are 2 routers or 20.
    
- **Uniform Addressing:** NL provides a consistent addressing scheme (IP) across different network technologies.
    

**Key Study Point for Alim Sir:** He specifically noted that "Routing packets from source all the way to destination" requires knowing the **Subnet Topology**. If the topology changes, the routing table must update.