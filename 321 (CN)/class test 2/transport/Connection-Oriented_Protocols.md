# Connection-Oriented Protocols

## Definition

**Connection-oriented protocols** require explicit connection establishment before data transfer and explicit termination after transfer completes.

## Characteristics

### Required Sequence

1. **Establishment Phase** ([[Three-Way_Handshake]]): Both parties agree connection exists
2. **Data Transfer Phase**: Bidirectional communication while connection active
3. **Termination Phase** ([[Connection_Release]]): Explicit close; both parties acknowledge closure

### Connection State

Protocols maintain **connection state** at endpoints:

```
Per-connection data structure (TCB - Transmission Control Block):
  - Sequence numbers (send and receive)
  - Acknowledgment numbers
  - Window sizes
  - Congestion window
  - Timers
  - Send/receive buffers
  - State machine state (ESTABLISHED, TIME-WAIT, etc.)
  
Memory cost: KB per connection
Processor cost: State machine operations
```

### Full-Duplex Communication

After establishment, both directions transmit simultaneously and independently:

```
Client → Server
Server → Client

Sequence numbers independent per direction
Each direction has own flow control
Close can be asymmetric (one direction closed; other still open)
```

## Guarantees

**Typical guarantees**:
- Delivery: All data arrives
- Ordering: In sequence sent
- No duplicates: Deduplication
- Flow control: Receiver not overwhelmed
- Congestion control: Network not overwhelmed

Example: [[TCP_Protocol]]

## Cost-Benefit Analysis

### Overhead

**Setup**: 3-way handshake requires 3 segments before data transmits

```
TCP: 3 segments just to establish connection
Latency: 1.5 × RTT before first data segment
```

**Per-connection state**: Memory and CPU per connection

```
1 million connections: 1 million TCBs (GBs of memory)
Context switching: Scheduler overhead
```

### Benefit

**Reliability**: Application assumes delivery; no need for application-level retry logic

**Ordering**: Simplifies application logic; processes data in order

**Flow control**: Prevents receiver overflow

**Congestion control**: Prevents network meltdown

## Use Cases

**When to use connection-oriented**:
- Bulk data transfer (FTP, HTTP)
- Reliability critical (email, financial)
- Order matters (telnet, SSH)
- Long-lived interactions

## Comparison with Connectionless

See [[UDP_Protocol|Connectionless Protocols]] for alternative approach.

## Implementation: TCP

[[TCP_Protocol]] is the primary connection-oriented protocol.

## See Also

- [[Three-Way_Handshake]]: Establishment procedure
- [[Connection_Release]]: Termination procedure
- [[TCP_Protocol]]: Implementation details
- [[Service_Primitives]]: API for connection establishment
- [[The_Two_Army_Problem]]: Theoretical foundations
