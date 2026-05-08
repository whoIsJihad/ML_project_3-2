
[[Flooding]] is a static [[Routing Algorithm]] where every incoming packet is sent out on every outgoing line except the one it arrived on.

## 1. Characteristics

- **Brute Force**: Does not require a Routing Table.
    
- **Reliability**: Guaranteed to find the shortest path and deliver the packet if a path exists, as it explores every possibility.
    
- **Robustness**: Highly resistant to node/link failures.
    

## 2. Problems

- **Exponential Traffic**: The number of packets grows exponentially with each hop, leading to severe Network Congestion.
    
- **Infinite Loops**: Without a termination mechanism, packets can circulate forever in cycles.
    

## 3. Termination Techniques

To prevent network collapse, flooding must be controlled:

### 3.1 Hop Count (TTL)

Each packet carries a counter (Time To Live).

- The counter is decremented at each router.
    
- When counter = 0, the packet is discarded.
    

#### Determining the Hop Count

- **Ideally**: The initial value should be equal to the **diameter** of the network (the longest shortest path between any two nodes).
    
- **Overshooting**: If the diameter is unknown, a large value is used. However, this increases redundant traffic.
    

### 3.2 Sequence Numbers and Source Lists

This is the most effective method to stop duplicate packet propagation and loops.

#### Data Structures

Each router maintains a **History Table** containing:

- `Source Address`: The unique ID of the router that generated the packet.
    
- `Sequence Number`: A counter incremented by the source for every new packet it creates.
    

#### The Algorithm

When a packet arrives at a router:

1. **Extract**: Read the `(Source, SeqNo)` tuple from the packet header.
    
2. **Lookup**: Check the History Table for a match.
    
3. **Decision**:
    
    - **If Match Found**: The packet has already been processed. **Discard** it immediately.
        
    - **If No Match**:
        
        - Update the History Table with the new `(Source, SeqNo)`.
            
        - Forward the packet to all outgoing links (except the source link).
            

#### Management of the History Table

To prevent the table from growing indefinitely:

- Each source entry is associated with a **Maximum Seen Sequence Number**. Packets with a `SeqNo` lower than or equal to the maximum seen are discarded.
    
- Timestamps can be used to purge old entries.
    

## 4. Optimization: Selective Flooding

A variation where routers do not flood every line. Instead, they only send packets on lines that are heading in the general direction of the destination (e.g., based on simple geographic or topological hints).

## 5. Use Cases

- **Routing Updates**: Used in [[Link State Routing (LSR)]](OSPF) to broadcast topology changes.
    
- **Military Applications**: High survivability against node destruction.
    
- **Initial Discovery**: Used when the destination's location is unknown (e.g., ARP).
    
