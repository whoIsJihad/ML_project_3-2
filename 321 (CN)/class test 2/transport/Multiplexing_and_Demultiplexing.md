# Multiplexing and Demultiplexing

## Definition

**Multiplexing** is the process by which the [[Transport_Layer|Transport Layer]] accepts data from multiple application processes and routes it downward to the Network Layer.

**Demultiplexing** is the inverse: the Transport Layer receives segments from the Network Layer and routes each to the correct application process based on [[Port_and_Addressing|port]] information.

Together, they enable multiple processes on a single host to share the network infrastructure.

## Problem Context

### Network Interface Constraint

A host may have one or multiple Network Layer addresses (IP addresses), but:
- Each typically connects to network through single interface
- Network Layer delivers segments based on destination IP address
- Multiple processes on same host need network access simultaneously

**Question**: How does Transport Layer distinguish which process should receive a segment when multiple processes listen on same IP?

**Answer**: Via [[Port_and_Addressing|ports]]

## Upward Multiplexing (Demultiplexing)

### Segment Arrival

When a segment arrives from Network Layer:

```
Network Layer:
  "Segment arrived: src IP=A, dst IP=B, protocol=TCP"

Transport Layer:
  1. Extract source/destination ports from segment header
  2. Form 4-tuple: (src IP, src port, dst IP, dst port)
  3. Lookup socket table: which process owns dst port?
  4. Deliver segment payload to process
```

### Socket Lookup Mechanism

**Kernel maintains socket table**:

```
Port 80:   HTTP Server Process (PID=1234)
Port 443:  HTTPS Server Process (PID=1235)  
Port 52341: Browser Process (PID=5678) - connected to remote
Port 52342: Email Client (PID=5679) - connected to remote
```

**Demultiplexing algorithm**:

For segment with (src IP=S, src port=P, dst IP=D, dst port=Q):

1. Look for established connection matching 4-tuple (S, P, D, Q)
   - If found: deliver to associated socket
   
2. If not found, look for listening socket on port Q
   - If found and process accepting connections: queue for ACCEPT
   
3. If not found: send RST (connection reset); discard segment

### Connectionless Demultiplexing (UDP)

UDP sockets don't have connections; all segments to same port go to same socket:

```
Server:
  socket = SOCKET(UDP)
  BIND(port=53)  // DNS port
  while True:
    (data, source) = RECVFROM()  // Receives from ANY source
    respond(data, source)

Queries:
  Query from 1.2.3.4:5000 → demultiplexed to port 53 socket
  Query from 5.6.7.8:6000 → demultiplexed to port 53 socket
  Query from 9.10.11.12:7000 → demultiplexed to port 53 socket
  
All arrive at same socket; socket knows source via RECVFROM return.
```

### Connection-Oriented Demultiplexing (TCP)

TCP has connections; each connection has its own socket:

```
Server:
  listening_socket = SOCKET(TCP)
  BIND(listening_socket, port=80)
  LISTEN(listening_socket)
  
  connection1 = ACCEPT(listening_socket)  // Connection to client 1
  connection2 = ACCEPT(listening_socket)  // Connection to client 2

Arrival:
  Segment from (1.2.3.4, 52341) dst port 80
    Lookup: match 4-tuple? No
    Lookup: listening socket on port 80? Yes
    → Queue for ACCEPT or send SYN-ACK
    
  Data segment from (1.2.3.4, 52341) to port 80 (established)
    Lookup: match 4-tuple (1.2.3.4, 52341, local_IP, 80)? Yes
    → Deliver to connection1 socket (associated with that 4-tuple)
    
  Data segment from (5.6.7.8, 52342) to port 80 (established)
    Lookup: match 4-tuple (5.6.7.8, 52342, local_IP, 80)? Yes
    → Deliver to connection2 socket (associated with that 4-tuple)
```

## Downward Multiplexing

### Multiple Processes Sending

When multiple application processes send data:

```
Process A: SEND("GET / HTTP/1.1")
Process B: SEND("250 OK")
Process C: SEND("HELLO")

↓
Transport Layer (Multiplexer):
  From Process A on port 52341: SEQ=1000, payload="GET / HTTP/1.1"
  From Process B on port 25: SEQ=2000, payload="250 OK"
  From Process C on port 5000: SEQ=3000, payload="HELLO"

→ Queue transmission; send to Network Layer
  Network Layer sees:
    Packet 1: src_port=52341, dst_port=80, src_IP=A, dst_IP=X
    Packet 2: src_port=25, dst_port=25, src_IP=A, dst_IP=Y
    Packet 3: src_port=5000, dst_port=5000, src_IP=A, dst_IP=Z
```

**Scheduling**: Transport Layer decides order and timing:
- FIFO (First-In-First-Out)
- Priority-based (interactive traffic prioritized over bulk)
- Fair queuing (each flow gets equal bandwidth)

## Multiplexing Granularity

### Port-Level Multiplexing

Multiple connections can share same port (Server side):

```
Server listening on port 80:
  Connection 1: from 1.2.3.4:52341
  Connection 2: from 5.6.7.8:52342
  Connection 3: from 9.10.11.12:52343
  
All handled by:
  listening_socket on port 80
  Individual connection sockets created by ACCEPT
```

### Socket-Level Multiplexing

Each socket encapsulates one connection or one port:

```
TCP:
  Listening socket: waits for incoming connections
  Connection socket: one per accepted connection
  
UDP:
  One socket per bound port (can receive from multiple senders)
```

## Many-to-One Multiplexing

### Definition

Many application processes or connections map to one Network Layer address.

```
     Process A ─┐
     Process B ─┤
     Process C ─┼─→ Transport Layer ─→ Network Layer (1 IP address)
     Process D ─┤
     Process E ─┘
     
All multiplexed through same IP; distinguished by ports.
```

**Extreme case**: Single host with one IP address but thousands of connections:
- Port 80 (HTTP): 1000s of connections
- Port 443 (HTTPS): 100s of connections
- Port 22 (SSH): 10s of connections
- Etc.

**Managing scale**:
- Server accepts thousands of connections on same listening port
- Each connection identified by 4-tuple (not just port)
- Modern servers use connection pooling, load balancing for this

## One-to-Many (Multicast/Broadcast)

### UDP Multicast

One sender to multiple receivers:

```
Sender:
  SENDTO(data, multicast_group_224.0.0.1)
  
Receivers (subscribers):
  socket = SOCKET(UDP)
  JOIN(multicast_group=224.0.0.1)
  BIND(port=5000)
  RECVFROM()  ← Receives from sender
```

Not traditional multiplexing (many processes on one host), but inverse: one address to many processes (or hosts).

## Multiplexing Efficiency

### Bandwidth Sharing

Multiplexing at transport layer allows efficient bandwidth sharing:

```
Link capacity: 1 Mbps

Process A (HTTP): 400 Kbps
Process B (FTP): 300 Kbps
Process C (SSH): 300 Kbps
─────────────────
Total: 1000 Kbps = full link

Without multiplexing: Each process needs separate link
With multiplexing: All share one link
```

### Latency Implications

**Problem**: Processing order matters

```
If processes sent in this order:
  B: 10000 byte FTP file (10 Kbytes)
  C: 100 byte SSH message
  
Without multiplexing scheduler:
  B's data sent first: 10000 bytes (10 seconds at 1 Kbps)
  C's data sent next: 100 bytes (0.1 seconds)
  C experiences 10 second latency!
  
With fair multiplexing:
  Interleave: B chunk, C chunk, B chunk, C chunk...
  C experiences minimal latency
```

**Scheduling algorithms** (at Transport Layer or even Network Layer):
- Round-robin (fair)
- Weighted fair queuing (high-priority traffic gets more)
- Strict priority (interactive > bulk)
- Queue management (drop low-priority when congested)

## De-multiplexing Errors

### Port Not Listening

Segment arrives for port with no listener:

```
TCP:
  Server not running on port 80
  Segment arrives: dst_port=80
  Transport Layer: No listening socket for port 80
  Action: Send RST (connection reset)

UDP:
  No socket bound to port 5000
  Datagram arrives: dst_port=5000
  Transport Layer: No socket
  Action: Send ICMP "Port Unreachable" (in some implementations)
          or silently discard
```

### Connection Reset

Segment arrives for connection that doesn't exist:

```
Client crashes; all connection state lost
Server still has active connection; sends data
Server sends segment to client's IP:port
Client TCP: No matching connection
Action: Send RST
Server receives RST; learns connection is dead
```

## Practical Considerations

### Socket Options

Application can tune multiplexing behavior:

```
socket.setsockopt(SO_REUSEADDR, 1)
  → Allows rebinding to port quickly after close
  → Addresses TIME-WAIT issue
  → Useful for restarting servers
```

### Load Balancing

Large-scale servers distribute load:

```
Physical Host A (multiple IPs):
  eth0:0 = 10.0.0.1
  eth0:1 = 10.0.0.2
  eth0:2 = 10.0.0.3
  
Load balancer directs:
  Client 1 → 10.0.0.1
  Client 2 → 10.0.0.2
  Client 3 → 10.0.0.3
  
Each connection demultiplexed to appropriate host's port 80.
```

### Namespace Isolation

Containers and virtual machines can have separate port spaces:

```
Host:
  Port 80 listening globally
  
Docker container 1:
  Internal port 8080 mapped to host:80 via NAT
  
Docker container 2:
  Internal port 8080 (different namespace)
  mapped to host:81 via NAT
  
Application in each container thinks it owns port 8080,
but OS multiplexes through different external ports.
```

## See Also

- [[Port_and_Addressing]]: Port identification and 4-tuple
- [[Service_Primitives]]: BIND, LISTEN, ACCEPT operations
- [[TCP_Protocol]]: TCP's connection-based multiplexing
- [[UDP_Protocol]]: UDP's connectionless multiplexing
- [[Segment_Structure]]: Port fields in headers
