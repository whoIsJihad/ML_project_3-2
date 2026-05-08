# Port and Addressing

## Definition

A **port** is a 16-bit unsigned integer (range 0 to 65535) that uniquely identifies a process or service on a single host. Ports serve as the address abstraction at the [[Transport_Layer|Transport Layer]], distinguishing between multiple concurrent communications on the same physical host.

## Theoretical Basis

### The Multiplexing Problem

A single host connected to a network via a single Network Layer connection (single IP address) may run multiple applications that all require network communication:

- Web server (HTTP) listening for incoming requests
- Email client (SMTP/POP3) sending and receiving mail
- Video streaming application receiving media
- SSH server awaiting remote login

All these applications send and receive data over the same physical network interface. The Transport Layer must disambiguate which incoming data belongs to which application. Similarly, when an application sends data, the Transport Layer must know which communication channel (source and destination) to use.

Ports solve this through **multiplexing**: routing data between multiple application processes and the network layer.

### Port as a Service Access Point

Formally, a port is a **Transport Service Access Point (TSAP)**. It represents the interface at which an application process connects to the Transport Layer service.

**Notation:**
- TSAP = (IP address, port number) for TCP/UDP
- Also called a **socket** in Berkeley Sockets terminology
- Full transport connection: (source IP, source port, dest IP, dest port)

## Port Number Assignment

The 16-bit port space is divided into three categories:

### Well-Known Ports (0-1023)

Assigned by IANA (Internet Assigned Numbers Authority) to standardized services. Typically requires administrative (root) privilege to listen on these ports.

| Service | Port | Protocol | Purpose |
|---|---|---|---|
| HTTP | 80 | TCP | Web browsing |
| HTTPS | 443 | TCP | Secure web |
| SMTP | 25 | TCP | Email transmission |
| POP3 | 110 | TCP | Email retrieval |
| DNS | 53 | TCP/UDP | Domain name resolution |
| SSH | 22 | TCP | Secure shell |
| Telnet | 23 | TCP | Remote login |
| FTP | 21 | TCP | File transfer |
| DHCP | 67, 68 | UDP | Dynamic host config |
| NTP | 123 | UDP | Network time protocol |

### Registered Ports (1024-49151)

Assigned by IANA for specific applications/services, though typically any user process can listen on these ports without special privileges. Registration provides coordination and prevents conflicts.

### Dynamic/Private Ports (49152-65535)

Ephemeral ports used for temporary client connections. Operating systems assign ports in this range to outgoing client connections when no specific port is requested.

## Connection Tuple

At the Transport Layer, a complete communication channel is identified by a 4-tuple:

$$\text{(source IP, source port, destination IP, destination port)}$$

This tuple is unique within a host and across the network at any given time. The combination ensures that:

1. A server can distinguish between multiple clients connecting from the same IP address
2. A client can have multiple simultaneous connections to the same server
3. Packets can be correctly demultiplexed to the appropriate application process

**Example:**
```
Connection 1: (192.168.1.100, 52341) → (93.184.216.34, 80)  [Browser 1 to web server]
Connection 2: (192.168.1.100, 52342) → (93.184.216.34, 80)  [Browser 2 to web server]
Connection 3: (192.168.1.100, 52343) → (93.184.216.35, 80)  [Browser 1 to different web server]

All originate from the same host (192.168.1.100) but are distinct connections.
```

## Multiplexing and Demultiplexing

### Multiplexing (Downward)

When an application sends data through a socket:

1. Application provides: data buffer, destination IP, destination port
2. Transport layer encapsulates with: source port (from socket), source IP (from host)
3. Forms complete 4-tuple for identification
4. Passes segment down to Network Layer with destination IP

```
Application 1 (port 52341)  ─┐
Application 2 (port 52342)  ─┼─→ Transport Layer ─→ Network Layer
Application 3 (port 52343)  ─┘
           (Multiplexing)
```

### Demultiplexing (Upward)

When a segment arrives from the network:

1. Network Layer delivers segment to Transport Layer with source/destination IPs
2. Transport Layer extracts source and destination ports from segment header
3. Forms 4-tuple: (source IP, source port, destination IP, destination port)
4. Looks up which process owns the destination port
5. Delivers payload to correct application process

```
Network Layer ─→ Transport Layer ─┬→ Application 1 (port 52341)
                 (Demultiplexing) ├→ Application 2 (port 52342)
                                  └→ Application 3 (port 52343)
```

## Server-Side Port Binding

### Passive Listening

A server application must **bind** to a port before receiving incoming connections:

```
Server Application:
1. Calls BIND(port=80)
2. Kernel reserves port 80 on this host
3. Server calls LISTEN()
4. Server is now ready to receive connections

Client Connection:
1. Client sends segment to (server_IP, 80)
2. Kernel demultiplexes to server application
3. Server accepts connection
```

### Multiple Servers and Port Conflicts

Only one process can bind to a specific port at a time (for a given protocol). Attempting to bind to an already-bound port results in an error. This prevents port conflicts while allowing exclusive control of well-known services.

## Client-Side Port Selection

### Explicit vs. Implicit Assignment

When a client creates an outgoing connection:

**Option 1: Explicit port specification**
```
Client calls: CONNECT(destination_IP, destination_port, local_port=specific_port)
Kernel binds to specified local port
Used when client has specific requirements
```

**Option 2: Implicit port assignment (typical)**
```
Client calls: CONNECT(destination_IP, destination_port)
Kernel automatically selects ephemeral port from 49152-65535
Ensures uniqueness and avoids conflicts
Most common for client applications
```

## Port State and Protocol Interaction

A port's state depends on the protocol:

### UDP (Connectionless)

- Port is either unbound or bound to an application
- Multiple packets to the same port may come from different sources
- No connection state associated with port
- Port can receive from any sender simultaneously

### TCP (Connection-Oriented)

- A port may be in multiple states:
  - **LISTEN**: Waiting for incoming connections
  - **ESTABLISHED**: Active connection through this port
  - **TIME_WAIT**: Recently closed connection, waiting for delayed packets
  - **CLOSED**: Port available for new bindings

- A single listening port can support multiple simultaneous connections through the 4-tuple distinction
- Each connection maintains separate state

## Practical Implications

### Port Exhaustion

A single client host has 49152 ephemeral ports. With TCP (three-way handshake overhead), this limits:

$$\text{max\_connections} \approx \frac{49152}{\text{time\_per\_connection}}$$

where time_per\_connection includes connection establishment, data transfer, and TIME_WAIT period (typically 2 minutes).

For a client making connections to a single server:
- High-frequency connections may exhaust ephemeral ports
- Server applications (listening ports) don't have this limitation
- Solutions: reuse connections (keep-alive), wait for TIME_WAIT expiration

### Network Address Translation (NAT) Impact

NAT devices translate ports to enable multiple hosts to share a single public IP:
- Private host:port (10.0.0.1:52341) maps to public host:port (203.0.113.1:10001)
- Receiver sees connection from (203.0.113.1:10001)
- NAT maintains mapping to route responses back to private host

## See Also

- [[Segment_Structure]]: How ports appear in protocol headers
- [[Multiplexing_and_Demultiplexing]]: Detailed mechanics of routing based on ports
- [[Service_Primitives]]: How applications create and use ports (BIND, LISTEN, CONNECT)
- [[TCP_Protocol]]: TCP-specific port state and management
- [[UDP_Protocol]]: UDP use of ports
