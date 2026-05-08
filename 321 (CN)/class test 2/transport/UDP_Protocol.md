# UDP Protocol

## Overview

**UDP** (User Datagram Protocol) is a [[Connectionless_Protocols|connectionless]], unreliable transport protocol that provides minimal services beyond [[Port_and_Addressing|multiplexing]] between processes. Defined in RFC 768 (1980).

**Design philosophy**: Minimal overhead

UDP delegates reliability, ordering, and flow control to the application. This allows applications to:
- Choose their own reliability levels (some data loss acceptable for speed)
- Use multicast/broadcast
- Control timing and buffering

## Service Model

### Characteristics

**UDP provides**:
1. **Best-effort delivery**: Segments may be lost without notification
2. **No ordering guarantee**: Segments may arrive out of order
3. **No duplicate detection**: Same segment may arrive multiple times
4. **No flow control**: Sender can overwhelm receiver
5. **Connectionless**: No setup or teardown; each segment independent
6. **Datagram semantics**: Message boundaries preserved
7. **Multicast/Broadcast support**: Can send to multiple receivers

### Guarantees NOT Provided

UDP does **not**:
- Guarantee delivery
- Guarantee order
- Detect or prevent duplicates
- Provide flow control
- Provide congestion control
- Establish connections
- Provide encryption (though DTLS adds this)

### When to Use UDP

**Low latency critical**:
- Online games (UDP faster than TCP's handshake/acknowledgments)
- VoIP (some packet loss acceptable; real-time more important than perfection)
- Live video streaming (occasional frames dropped acceptable; low latency critical)
- DNS queries (request-response model; retransmit if timeout)

**Bandwidth constrained**:
- IoT devices with limited bandwidth
- Multicast (inherently one-to-many; TCP doesn't support)
- Broadcast-based protocols

**Application-specific reliability**:
- Application knows what reliability it needs
- Can implement selective reliability (e.g., critical data retransmitted, non-critical sent once)

## Protocol Structure

### Connectionless Model

Unlike [[TCP_Protocol|TCP]], UDP has no connection state:

```
Client Application:
  socket = SOCKET(UDP)
  BIND(socket, port)  // optional; OS picks port if omitted
  SENDTO(socket, data, server_address)
  RECVFROM(socket, buffer)  // receives from ANY sender

Server Application:
  socket = SOCKET(UDP)
  BIND(socket, well_known_port)
  while True:
    (data, client_address) = RECVFROM(socket, buffer)
    process(data)
    SENDTO(socket, response, client_address)
```

No LISTEN, ACCEPT, CONNECT, or CLOSE primitives.

**Multiple sources on same socket**:
```
Server listening on port 53 (DNS)
Query 1 arrives from client A (1.2.3.4:5000)
Query 2 arrives from client B (5.6.7.8:5001)
Query 3 arrives from client A (1.2.3.4:5001)  // different source port

Server socket receives all three; RECVFROM returns data + source address.
Server responds to appropriate client via SENDTO.
No separate connection state needed.
```

### Datagram Semantics

**Message boundaries preserved**:

```
Application writes:
  SENDTO(data="Hello", ...) → UDP segment created
  SENDTO(data="World", ...) → UDP segment created

Receiver:
  RECVFROM() → data="Hello", source=A
  RECVFROM() → data="World", source=B
  
Message structure preserved; application knows message boundaries.
```

Compare with [[TCP_Protocol|TCP]]'s stream model where SEND calls don't preserve boundaries.

## Datagram Format

### Header Structure

[[Segment_Structure|UDP header]] is minimal (8 bytes):

```
0         1         2         3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
┌─────────────────────────────────────────────────────────────────┐
│          Source Port (16 bits)     │    Destination Port (16)   │
├─────────────────────────────────────────────────────────────────┤
│          Length (16 bits)          │       Checksum (16 bits)   │
├─────────────────────────────────────────────────────────────────┤
│                       Payload (variable)                         │
└─────────────────────────────────────────────────────────────────┘
```

**Source Port**: Sender's port; 0 if not used

**Destination Port**: Recipient's port

**Length**: Total length of UDP datagram (header + payload); minimum 8 bytes

**Checksum**: Optional in IPv4; mandatory in IPv6
- Includes pseudo-header (source IP, dest IP, protocol, UDP length)
- Can be 0 in IPv4 (meaning no checksum); deprecated but still allowed
- Detects bit errors only; doesn't correct or guarantee against all failures

### Maximum Datagram Size

**Theoretical limit**: 64KB (16-bit length field)

**Practical limit**: Path MTU (Maximum Transmission Unit)

- Ethernet: 1500 bytes typical
- UDP can fragment if larger
- Application typically limits to 512-1472 bytes (leaves room for IP/UDP headers)

**Fragmentation**: IP layer fragments large UDP datagrams
- If any fragment lost: entire datagram lost (no reassembly guarantee)
- Use UDP datagrams ≤ 512 bytes to avoid fragmentation

## Reliability via Application

### Why UDP Applications Must Handle Reliability

**Loss scenario**:
```
Client sends: REQUEST (seq=1)
Network drops it.
Client times out; never receives RESPONSE.
Client's RECEIVE call blocks forever (if no timeout set).
```

**Application solution**:
```
Client:
  socket.set_timeout(1.0)  // 1 second timeout
  SENDTO(REQUEST, server)
  try:
    RECVFROM()
  except Timeout:
    retries += 1
    if retries > MAX:
      error("Server unreachable")
    else:
      goto SENDTO
```

### Application-Level Sequence Numbers

UDP doesn't provide ordering. Application must track:

```
Application places sequence number in payload:
  SENDTO(data="Seq:3:Hello", server)
  SENDTO(data="Seq:1:World", server)
  SENDTO(data="Seq:2:!!!", server)

Receiver application:
  Buffer received datagrams by sequence number
  Deliver to application in sequence order once complete
  Example: RTP (Real-time Transport Protocol) does this
```

### Timeout Selection

**Fixed timeout**: Simple but may be too short (false timeout) or too long (poor responsiveness)

**Adaptive timeout**: Like TCP's RTT estimation

```
Measure RTT for responses
SRTT = weighted average of RTT samples  
Timeout = SRTT + k * std_deviation  // k ≈ 4

Adapts to network conditions
```

## Multicast and Broadcast

### Unicast (Point-to-Point)

Standard UDP communication:
```
SENDTO(data, unicast_address)
→ Single recipient receives
```

### Multicast (Point-to-Multipoint)

Special addresses (224.0.0.0/4 in IPv4) deliver to multiple subscribers:

```
Server:
  BIND(multicast_group=224.0.0.1, port=5000)
  while True:
    SENDTO(data, 224.0.0.1:5000)  // Send to all subscribers

Clients:
  JOIN(multicast_group=224.0.0.1)
  socket = SOCKET(UDP)
  BIND(port=5000)
  while True:
    RECVFROM()  // Receive from all senders to group
```

**Use cases**:
- Video stream distribution
- Network time protocol (NTP)
- Multicast DNS (mDNS)
- Routing protocol advertisements

### Broadcast

Special address (255.255.255.255 in IPv4) delivers to all hosts on network:

```
SENDTO(data, broadcast_address)
→ All hosts on local network receive

Typically limited to LAN; routers don't forward.
```

**Use cases**:
- DHCP (server broadcasts configuration)
- ARP (broadcast to find MAC for IP)
- Wake-on-LAN
- Network discovery

### TTL (Time-To-Live) for Multicast

Multicast datagrams have TTL to limit scope:

```
TTL = 0: Same host only
TTL = 1: Same LAN only
TTL = 32: Same organization typically
TTL = 64: Same region typically
TTL = 255: Global (if not rate-limited)
```

## DNS Example: UDP in Practice

**DNS query/response**:

```
Client:
  socket = SOCKET(UDP)
  query = "What IP for google.com?"  // encoded in DNS format
  SENDTO(query, DNS_server:53)
  set_timeout(1.0)
  try:
    response = RECVFROM()
    parse(response)
  except Timeout:
    retry with different DNS server or backoff

Server:
  socket = SOCKET(UDP)
  BIND(port=53)
  while True:
    (query, client_address) = RECVFROM()
    response = lookup_dns(query)
    SENDTO(response, client_address)
```

**Key points**:
- Stateless: Server doesn't remember past queries
- Timeout: Client retransmits if no response
- Single round-trip: Request/response pattern
- Optional reliability: Critical queries sometimes sent to multiple servers; use first response

## Comparison: UDP vs. TCP

| Aspect | UDP | TCP |
|---|---|---|
| **Connection** | None (connectionless) | Explicit handshake/close |
| **Reliability** | Best-effort; loss possible | Guaranteed delivery |
| **Ordering** | No ordering guarantee | Ordered delivery |
| **Duplicates** | Possible | Eliminated |
| **Flow Control** | None | Sender regulated by receiver window |
| **Congestion Control** | None | Sender reduces rate on loss |
| **Latency** | Low (no setup) | Higher (3-way handshake) |
| **Overhead** | 8 bytes header | 20-60 bytes header |
| **Broadcast** | Supported | Not applicable |
| **Multicast** | Supported | Not supported |
| **Message Boundaries** | Preserved | Stream (no boundaries) |
| **Use Case** | Speed/Multimedia | Reliability/Data integrity |

## RTP (Real-Time Transport Protocol)

### Overview

**RTP** is an application-layer protocol built on UDP for real-time media.

RTP adds:
- Sequence numbers for detecting loss
- Timestamps for synchronizing playout
- Payload type identification
- Synchronization source (SSRC) identification

### When UDP Isn't Enough

**Problem**: UDP has no sequence numbers or timestamps

**RTP solution**: Application-layer protocol adds:

```
RTP Header (12+ bytes):
  - Sequence number: Detect missing packets
  - Timestamp: Synchronize audio/video/data streams
  - SSRC: Identify media source
  - Payload type: Identify encoding (audio codec, video codec, etc.)
```

### Reliability in RTP

Unlike [[TCP_Protocol|TCP]], RTP doesn't retransmit lost packets:

```
Timestamp T1: Send media chunk
Application waits for duration of chunk (e.g., 20ms for audio)
Timestamp T2: Send next chunk
If chunk T1 lost: Application plays silence; continues with T2
Retransmitting T1 makes no sense if we're past its playout time
```

**Trade-off**: Accept loss for real-time constraints.

## Implementation Considerations

### Kernel Buffer Sizing

UDP kernel socket buffer:
```
socket.setsockopt(SO_RCVBUF, buffer_size)
socket.setsockopt(SO_SNDBUF, buffer_size)
```

Receiver buffer size must accommodate bursts; if full, incoming datagrams dropped (silently in kernel).

### Non-blocking Send

SENDTO typically blocks if kernel buffer full. Applications can:
```
socket.setblocking(False)  // Non-blocking
try:
  SENDTO(data, address)  // Succeeds immediately or fails
except Busy:
  drop_packet()  // Application decides how to handle
```

### Receiver Thread/Loop

Must drain socket continuously:
```
// If receiver blocks on application processing:
while True:
  data, source = RECVFROM()
  queue.put((data, source))  // Non-blocking queue

// Separate thread processes queue
// Prevents kernel buffer from filling
```

## See Also

- [[Segment_Structure]]: UDP datagram format details
- [[Port_and_Addressing]]: UDP port semantics
- [[Service_Primitives]]: UDP service calls (SENDTO, RECVFROM)
- [[TCP_Protocol]]: Reliable alternative
- [[Transport_Layer]]: UDP's role in transport layer
- [[Flow_Control_Mechanisms]]: Why UDP has no flow control
- [[Congestion_Control]]: Why UDP has no congestion control
