# Subnet Architectures: Datagrams & Virtual Circuits (Page 7)

This page details the two primary methods the Network Layer uses to move packets across a subnet. It’s the difference between "figuring it out as you go" and "planning the whole trip in advance."

### 1. The Service Dichotomy

Alim Sir categorizes these based on how the subnet handles the connection:

- **Connectionless Service (Datagram Subnets):** * Think of this like sending individual letters. Each packet (datagram) is a "free agent."
    
    - Routers make a fresh decision for every single packet based on the destination address.
        
- **Connection-Oriented Service (Virtual Circuit Subnets):**
    
    - Think of this like a temporary railway. A path (the VC) is established _before_ data flows.
        
    - All packets in a session follow the exact same "virtual" path.
        

### 2. Routing within a Datagram Subnet

The diagrams of Routers A, B, C, D, E, F show how a datagram reaches its destination.

- **The Routing Table:** Every router has a local table. It doesn't know the _full_ path; it only knows the **Next-hop**.
    
- **Router A’s Table Example:**
    
    - To reach Destination **F**, the table says: Send to **C**.
        
    - To reach Destination **E**, the table says: Send to **C**.
        
    - To reach Destination **D**, the table says: Send to **B**.
        
- **Dynamic Nature:** If the link between A and C fails, Router A simply updates its table to send "E" packets to "B" instead. This is why datagrams are robust.
    

### 3. Routing over a Virtual Circuit (VC)

Virtual Circuits work differently. Instead of looking at a destination address, routers look at a **VC Identifier**.

- **The Setup:** During the "Call Setup" phase, a path is chosen (e.g., $H_1 \rightarrow A \rightarrow C \rightarrow E \rightarrow H_2$).
    
- **The VC ID:** Each packet carries a short ID (like "1" or "2").
    
- **Router E’s Table (from your notes):** 
	*  If a packet arrives from **C** with **ID 1**, send it to **F** with **ID 1**.
    
    - If a packet arrives from **C** with **ID 2**, send it to **F** with **ID 2**.
        
- **Efficiency:** Routers don't need to look up long IP addresses; they just swap IDs and forward. However, if any router on the path crashes, the whole VC is destroyed.
    

### 4. Key Terminology from the Notes

- **Next-hop:** The immediate neighbor a router sends a packet to.
    
- **Routing Algorithm:** The background process that actually builds and manages these tables (like Dijkstra or DVR, which we'll get to once you finish this page).
    
- **Subnet:** Specifically defined here as the "set of routers."
    

**Study Tip:** Alim Sir loves to ask about the "State" in routers.

- **Datagrams:** No state (stateless). Routers forget you the moment the packet is gone.
    
- **VC:** State-heavy. Routers must remember every active connection passing through them.