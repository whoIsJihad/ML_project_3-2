# Connectionless Protocols

## Definition

**Connectionless protocols** treat each [[Segment_Structure|segment]] (called a datagram in UDP) independently, with no prior connection establishment or subsequent termination.

## Characteristics

### No Connection Setup

Application sends data immediately:

```
Connectionless (UDP):
  socket = SOCKET()
  SENDTO(data, destination)
  
vs. Connection-oriented (TCP):
  socket = SOCKET()
  CONNECT(destination)  ← Handshake
  SEND(data)            ← Then send
```

**Latency advantage**: No 3-way handshake delay before transmission.

### Stateless

**Protocol maintains no per-flow state**:

```
Server listening on one port:
  Same socket receives datagrams from thousands of clients
  No per-connection buffer, sequence number tracking, or state machine
  Lightweight; scales easily
```

### Independent Datagrams

Each datagram is self-contained:

```
Datagram 1: Independent; may be lost
Datagram 2: Independent; may arrive before Datagram 1
Datagram 3: Independent; may be duplicated

Receiver: No guarantee about any relationship between datagrams
```

## Characteristics vs. Connection-Oriented

| Aspect | Connectionless | Connection-Oriented |
|---|---|---|
| **Setup** | None | 3-way handshake |
| **State** | None | TCB maintained |
| **Delivery** | Best-effort | Guaranteed |
| **Order** | No guarantee | Guaranteed |
| **Duplicates** | May occur | Eliminated |
| **Flow control** | None | Receiver-regulated |
| **Congestion control** | None | Sender-regulated |
| **Multicast** | Supported | Not in TCP |
| **Latency** | Low (no setup) | Higher (setup) |
| **Overhead** | 8 bytes (UDP) | 20-60 bytes (TCP) |
| **Use case** | Speed, multimedia | Reliability |

## Unreliability Implications

### Application Must Handle

**Loss detection and recovery**:
```
Application: SEND(data, server)
Application: set_timeout(1.0)
try:
  response = RECEIVE()
except Timeout:
  // Loss or server down; application decides
  retry_count += 1
  if retry_count < MAX:
    SEND(data, server)  // Retransmit
  else:
    error("Server unreachable")
```

**Ordering**:
```
Application receives datagrams; must reorder if needed
Example: RTP (Real-time Protocol) uses timestamp field
         Application buffers and plays in timestamp order
```

**Deduplication**:
```
Same datagram may arrive twice
Application must detect via sequence number in payload
Discard duplicates
```

## Use Cases

**When to use connectionless**:

### 1. Low Latency Critical
- Online games: UDP faster than TCP handshake
- VoIP: Real-time more important than perfection
- DNS queries: Simple request-response; tolerance for retransmit

### 2. Multicast/Broadcast
- Video distribution to multiple hosts
- Network discovery
- Announcements
- TCP doesn't support multicast

### 3. Bandwidth Constrained
- IoT devices: Minimal overhead
- Sensor networks: Reduce protocol overhead
- Unreliable links: Loss expected; UDP doesn't add retransmission overhead

### 4. Application-Level Reliability
- Application implements custom reliability
- Knows which data is critical (reliable) vs. best-effort
- Example: Game may use UDP for motion (can lose frames) and TCP for game state (must arrive)

### 5. High-Frequency, Stateless Requests
- DNS: Thousands of independent queries per second
- NTP (Network Time Protocol): One-way synchronization
- SNMP (network management): Query-response with retransmit at application level

## Example: DNS

```
Client:
  socket = SOCKET(UDP)
  query_encode("What is IP for google.com?")
  SENDTO(query, 8.8.8.8:53)  // Google's DNS server
  set_timeout(2.0)
  
  try:
    response = RECVFROM()
    answer = parse(response)
  except Timeout:
    retry to different DNS server
    
Server:
  socket = SOCKET(UDP)
  BIND(port=53)
  while True:
    (query, client_address) = RECVFROM()
    answer = lookup_dns(query)
    SENDTO(answer, client_address)
```

**Key features**:
- Stateless: Server doesn't remember queries
- Connectionless: Each query independent
- Application retries: Client has timeout
- Multicast capable: Can broadcast queries

## Example: NTP (Network Time Protocol)

```
Client:
  socket = SOCKET(UDP)
  SENDTO(time_request, time_server:123)
  
  response = RECVFROM()
  client_time = system_clock()
  server_time = extract_timestamp(response)
  
  adjust_clock(server_time - client_time)

Server:
  socket = SOCKET(UDP)
  BIND(port=123)
  while True:
    (request, client) = RECVFROM()
    response = create_response(system_time())
    SENDTO(response, client)
```

**Properties**:
- One-way communication: No persistent relationship
- Connectionless: Each request independent
- Simple: No complex state management

## Example: RTP (Real-time Transport Protocol)

**Application-level reliability on UDP**:

```
Sender:
  for each media chunk:
    seq_no += 1
    timestamp = current_time
    payload = media_chunk
    SENDTO(RTP_packet, receiver)
    
Receiver:
  while True:
    packet = RECVFROM()
    seq_no = packet.sequence
    if seq_no already_received:
      discard  // Duplicate
    buffer[seq_no] = packet.payload
    
    while buffer[next_expected] exists:
      play(buffer[next_expected])
      next_expected += 1
      
    if buffer gap too large (loss):
      skip; play silence; continue
      
Behavior:
  - Loss: Plays silence/skip; doesn't retransmit
  - Out-of-order: Buffers; plays in timestamp order
  - Duplicate: Detects via sequence; discards
  - Real-time: No wait for retransmission
```

## Scalability Advantage

**Server with 1 million connections**:

```
UDP server: 1 socket listening
  Receives from 1 million clients
  No per-connection memory
  Memory: Minimal (just one socket + buffers)
  
TCP server: 1 listening socket + 1 million connection sockets
  Per-connection TCB: 4 KB each
  Memory: 4 GB just for TCBs
  CPU: Context switching, state machine per connection
```

Connectionless can handle massive fan-in with minimal resources.

## Limitations

### No Guarantees

```
Data may: arrive late, arrive out-of-order, be lost, arrive multiple times
Application must: handle all these cases
Complexity: Shifted from protocol to application
```

### Requires Application Intelligence

```
Application must:
  - Implement retry logic (timeouts)
  - Detect and eliminate duplicates
  - Reorder data if order matters
  - Prioritize which data is important
  - Handle loss gracefully
  
More work; more bugs; more complexity in application
```

## Hybrid Approaches

### QUIC (Quick UDP Internet Connection)

Implements TCP-like features over UDP:

```
Carrier: UDP datagrams
Content: QUIC protocol layer
Features: Connection IDs, ordering, reliability, stream multiplexing, 0-RTT setup

Benefits: Faster establishment than TCP, UDP's firewall-friendliness
```

### SCTP (Stream Control Transmission Protocol)

Message-oriented, reliable, partially ordered:

```
Features:
  - Explicit message boundaries (like UDP)
  - Reliability (like TCP)
  - Multi-path support
  - Partial ordering: Some messages ordered, some not
  
Use: Telecom signaling (SS7, SIGTRAN)
```

## See Also

- [[UDP_Protocol]]: Primary connectionless protocol implementation
- [[Connection-Oriented_Protocols]]: TCP and alternatives
- [[Segment_Structure]]: Datagram format
- [[Service_Primitives]]: SENDTO, RECVFROM operations
- [[Transport_Layer]]: Overview of both approaches
