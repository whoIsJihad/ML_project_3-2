# Computer Networks

## Course Overview
**Depth:** University undergraduate + practical systems knowledge  
**Time:** 3-4 hours focused reading  
**Prerequisites:** Basic OS concepts, C programming fundamentals

---

# Part I: Network Fundamentals

---

## 1. The OSI and TCP/IP Models

### OSI 7-Layer Model

| Layer | Name | Function | PDU | Examples |
|-------|------|----------|-----|----------|
| 7 | Application | User interface | Data | HTTP, FTP, SMTP, DNS |
| 6 | Presentation | Data format, encryption | Data | SSL/TLS, JPEG, ASCII |
| 5 | Session | Session management | Data | NetBIOS, RPC |
| 4 | Transport | End-to-end delivery | Segment | TCP, UDP |
| 3 | Network | Routing, addressing | Packet | IP, ICMP, ARP |
| 2 | Data Link | Framing, MAC | Frame | Ethernet, Wi-Fi |
| 1 | Physical | Bits on wire | Bits | Cables, signals |

**PDU:** Protocol Data Unit - the unit of data at each layer

### TCP/IP Model (4 Layers)

| TCP/IP | OSI Equivalent | Protocols |
|--------|----------------|-----------|
| Application | 5, 6, 7 | HTTP, DNS, SMTP |
| Transport | 4 | TCP, UDP |
| Internet | 3 | IP, ICMP, ARP |
| Network Access | 1, 2 | Ethernet, Wi-Fi |

### Encapsulation

**Sending:**
```
Application Data
    ↓ (adds header)
Transport Segment: [TCP Header | Data]
    ↓ (adds header)  
Network Packet: [IP Header | TCP Header | Data]
    ↓ (adds header + trailer)
Frame: [Eth Header | IP Header | TCP Header | Data | FCS]
    ↓
Bits on physical medium
```

**Receiving:** Reverse process (decapsulation)

---

## 2. Physical Layer

### Transmission Media

**Guided Media:**
- **Twisted Pair:** Cat5e (1 Gbps), Cat6 (10 Gbps), Cat6a/7 (10 Gbps longer distances)
- **Coaxial Cable:** Higher bandwidth, better shielding, older networks
- **Fiber Optic:** Single-mode (long distance), Multi-mode (shorter, cheaper)

**Unguided Media:**
- **Radio:** Wi-Fi, Bluetooth
- **Microwave:** Point-to-point links
- **Infrared:** Short-range, line-of-sight

### Signal Encoding

**Digital Encoding:**
- **NRZ (Non-Return-to-Zero):** 1 = high, 0 = low
- **Manchester:** 1 = high-to-low transition, 0 = low-to-high
- **4B/5B:** Map 4 bits to 5-bit patterns (clock recovery)

**Bandwidth vs Data Rate:**
Nyquist: Max data rate = 2B log₂(V) bps (noiseless)
Shannon: Max capacity = B log₂(1 + S/N) bps

Where B = bandwidth (Hz), V = signal levels, S/N = signal-to-noise ratio

### Multiplexing

**FDM (Frequency Division):** Each channel gets different frequency band
**TDM (Time Division):** Each channel gets time slots
**WDM (Wavelength Division):** Different wavelengths in fiber

---

## 3. Data Link Layer

### Functions
1. Framing: Delimiting data into frames
2. Physical addressing: MAC addresses
3. Error detection/correction
4. Flow control
5. Access control (shared medium)

### MAC Addresses

**Format:** 48 bits, written as 6 hex pairs
```
AA:BB:CC:DD:EE:FF
```

**First 3 bytes:** OUI (Organizationally Unique Identifier) - manufacturer
**Last 3 bytes:** NIC-specific

**Special addresses:**
- `FF:FF:FF:FF:FF:FF` - Broadcast
- First bit = 1 - Multicast

### Framing

**Character Count:** Length field (simple but error-prone)

**Byte Stuffing:** 
- Flag byte: `0x7E`
- Escape byte: `0x7D`
- If data contains flag, insert escape

**Bit Stuffing (HDLC):**
- Flag: `01111110`
- After 5 consecutive 1s in data, insert 0
- Receiver removes 0 after five 1s

### Error Detection

**Parity:**
- Even parity: Add bit to make 1-count even
- Odd parity: Add bit to make 1-count odd
- Detects single-bit errors

**Checksum:**
```c
uint16_t checksum(uint16_t* data, int len) {
    uint32_t sum = 0;
    while (len > 1) {
        sum += *data++;
        len -= 2;
    }
    if (len == 1) {
        sum += *(uint8_t*)data;
    }
    while (sum >> 16) {
        sum = (sum & 0xFFFF) + (sum >> 16);
    }
    return ~sum;
}
```

**CRC (Cyclic Redundancy Check):**
- Treat data as polynomial
- Divide by generator polynomial
- Remainder = CRC
- Common: CRC-32 for Ethernet

**CRC-32 Example:**
```
Generator polynomial: x³² + x²⁶ + x²³ + x²² + x¹⁶ + x¹² + x¹¹ + x¹⁰ + x⁸ + x⁷ + x⁵ + x⁴ + x² + x + 1
Binary: 100000100110000010001110110110111
```

### Error Correction

**Hamming Code:**
- Position bits at powers of 2 (1, 2, 4, 8...)
- Each parity bit covers specific data positions
- Can detect 2-bit errors, correct 1-bit errors

**Hamming Distance:** Minimum bit flips between valid codewords
- Detect d errors: Need distance ≥ d + 1
- Correct d errors: Need distance ≥ 2d + 1

### Flow Control

**Stop-and-Wait:**
- Send one frame, wait for ACK
- Utilization: L/L + 2×propagation delay
- Poor for high bandwidth-delay product

**Sliding Window:**
- Send multiple frames before waiting for ACK
- Window size W = 2^n - 1 (for n-bit sequence numbers)
- Go-Back-N: Receiver discards out-of-order frames
- Selective Repeat: Receiver buffers out-of-order frames

### Medium Access Control (MAC)

**ALOHA:**
- Pure ALOHA: Send whenever ready, max throughput = 18.4%
- Slotted ALOHA: Time slots, max throughput = 36.8%

**CSMA (Carrier Sense Multiple Access):**
- Listen before sending
- 1-persistent: Send immediately when idle
- Non-persistent: Random backoff if busy
- p-persistent: Send with probability p when idle

**CSMA/CD (Collision Detection):**
- Detect collision while transmitting
- Send jam signal
- Binary exponential backoff: Wait random(0, 2^n - 1) × slot time
- Used in Ethernet

**CSMA/CA (Collision Avoidance):**
- Can't detect collisions (wireless)
- RTS/CTS handshake
- Used in Wi-Fi

### Ethernet

**Frame Format:**
```
| Preamble | SFD | Dest MAC | Src MAC | Type | Payload | FCS |
|    7     |  1  |    6     |    6    |  2   | 46-1500 |  4  |
```

**Types:** `0x0800` = IPv4, `0x0806` = ARP, `0x86DD` = IPv6

**Minimum frame size:** 64 bytes (for collision detection)
**Maximum frame size:** 1518 bytes (or 1522 with VLAN tag)

### Switching

**Learning Bridge Algorithm:**
```python
def process_frame(frame, ingress_port):
    # Learn: Associate source MAC with ingress port
    mac_table[frame.src_mac] = ingress_port
    
    # Forward
    if frame.dst_mac in mac_table:
        if mac_table[frame.dst_mac] != ingress_port:
            forward(frame, mac_table[frame.dst_mac])
        # else: drop (same port)
    else:
        flood(frame, all_ports_except(ingress_port))
```

**Spanning Tree Protocol (STP):**
- Prevents loops in switched networks
- Elects root bridge (lowest ID)
- Each switch finds shortest path to root
- Blocks redundant ports

**VLAN (Virtual LAN):**
- Logical segmentation of network
- 802.1Q tag: 4 bytes with 12-bit VLAN ID (4096 VLANs)
- Trunk ports carry multiple VLANs

---

# Part II: Network Layer

---

## 4. IP Addressing

### IPv4

**Format:** 32 bits, dotted decimal notation
```
192.168.1.100 = 11000000.10101000.00000001.01100100
```

**Address Classes (Historical):**
| Class | First Bits | Range | Default Mask |
|-------|------------|-------|--------------|
| A | 0 | 0.0.0.0 - 127.255.255.255 | 255.0.0.0 (/8) |
| B | 10 | 128.0.0.0 - 191.255.255.255 | 255.255.0.0 (/16) |
| C | 110 | 192.0.0.0 - 223.255.255.255 | 255.255.255.0 (/24) |
| D | 1110 | 224.0.0.0 - 239.255.255.255 | Multicast |
| E | 1111 | 240.0.0.0 - 255.255.255.255 | Reserved |

**CIDR (Classless Inter-Domain Routing):**
```
192.168.1.0/24
Network: 192.168.1.0
Netmask: 255.255.255.0 (24 ones)
Hosts: 2^(32-24) - 2 = 254
```

**Subnetting Example:**
```
Given: 192.168.1.0/24
Need: 4 subnets

Borrow 2 bits: /26
Subnet mask: 255.255.255.192

Subnets:
192.168.1.0/26   (0-63,   network=0, broadcast=63)
192.168.1.64/26  (64-127, network=64, broadcast=127)
192.168.1.128/26 (128-191, network=128, broadcast=191)
192.168.1.192/26 (192-255, network=192, broadcast=255)
```

**Special Addresses:**
- `127.0.0.0/8` - Loopback
- `10.0.0.0/8` - Private
- `172.16.0.0/12` - Private
- `192.168.0.0/16` - Private
- `169.254.0.0/16` - Link-local
- `0.0.0.0` - Unspecified (this host)
- `255.255.255.255` - Limited broadcast

### IPv6

**Format:** 128 bits, 8 groups of 4 hex digits
```
2001:0db8:0000:0000:0000:0000:0000:0001
= 2001:db8::1  (compressed, leading zeros + consecutive zero groups)
```

**Address Types:**
- `::1` - Loopback
- `fe80::/10` - Link-local
- `fc00::/7` - Unique local (private)
- `2000::/3` - Global unicast
- `ff00::/8` - Multicast

**IPv6 Header:** Fixed 40 bytes (simpler than IPv4)

---

## 5. IPv4 Header

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options (if IHL > 5)                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Key Fields:**
- **Version:** 4 for IPv4
- **IHL:** Header length in 32-bit words (min 5 = 20 bytes)
- **Total Length:** Entire packet including header
- **TTL:** Decremented at each hop, dropped at 0
- **Protocol:** 1=ICMP, 6=TCP, 17=UDP
- **Checksum:** Header only

### Fragmentation

**When:** Packet > MTU (Maximum Transmission Unit)
**MTU:** Ethernet = 1500 bytes

**Flags:**
- DF (Don't Fragment): Drop and send ICMP if too large
- MF (More Fragments): Set on all but last fragment

**Fragment Offset:** In 8-byte units

**Example:**
```
Original: 4000 bytes data, ID=1234
MTU: 1500 bytes
Max data per fragment: 1500 - 20 = 1480 bytes

Fragment 1: Offset=0, MF=1, Data=0-1479
Fragment 2: Offset=185 (1480/8), MF=1, Data=1480-2959
Fragment 3: Offset=370 (2960/8), MF=0, Data=2960-3999
```

**Path MTU Discovery:**
- Send with DF=1
- Receive ICMP "fragmentation needed"
- Reduce packet size
- Repeat until successful

---

## 6. Routing

### Static vs Dynamic

**Static Routing:**
```bash
# Linux
ip route add 10.0.2.0/24 via 192.168.1.1
ip route add default via 192.168.1.254

# Show routing table
ip route show
```

**Dynamic Routing Protocols:**
- **Interior Gateway Protocols (IGP):** Within AS
  - RIP, OSPF, IS-IS, EIGRP
- **Exterior Gateway Protocols (EGP):** Between AS
  - BGP

### Distance Vector (RIP)

**Bellman-Ford Algorithm:**
```
Distance to X via Y = Cost(self, Y) + Y's distance to X
```

**RIP:**
- Metric: Hop count (max 15)
- Update: Every 30 seconds, broadcast full table
- Problems: Count to infinity, slow convergence

**Split Horizon:** Don't advertise route back to source
**Poison Reverse:** Advertise infinity to source

### Link State (OSPF)

**Dijkstra's Algorithm:**
1. Flood link state advertisements (LSAs) to all routers
2. Build complete topology map
3. Run shortest path algorithm

**OSPF Features:**
- Metric: Cost (typically inversely proportional to bandwidth)
- Fast convergence
- Hierarchical: Areas reduce overhead
- Equal-cost multipath (ECMP)

**LSA Types:**
- Type 1: Router LSA (intra-area)
- Type 2: Network LSA
- Type 3: Summary LSA (inter-area)
- Type 5: External LSA

### BGP (Border Gateway Protocol)

**Path Vector Protocol:**
- Exchanges full path (AS list) to destination
- Prevents loops (reject if own AS in path)
- Policy-based routing

**BGP Attributes:**
- AS_PATH: Sequence of AS numbers
- NEXT_HOP: IP to reach prefix
- LOCAL_PREF: Preference (higher = better)
- MED: Multi-exit discriminator (suggest entry point)

**Decision Process:**
1. Highest LOCAL_PREF
2. Shortest AS_PATH
3. Lowest ORIGIN (IGP < EGP < incomplete)
4. Lowest MED
5. eBGP over iBGP
6. Lowest IGP cost to NEXT_HOP
7. Lowest router ID

### ARP (Address Resolution Protocol)

**Purpose:** Map IP address to MAC address

**Process:**
1. Check ARP cache
2. If not found, broadcast ARP request
3. Target responds with MAC address
4. Cache the mapping

**ARP Packet:**
```
| HW Type | Proto Type | HW Size | Proto Size | Opcode |
| Sender MAC | Sender IP | Target MAC | Target IP |
```

**Commands:**
```bash
arp -a           # View ARP cache
arp -d <ip>      # Delete entry
ip neigh show    # Linux
```

### NAT (Network Address Translation)

**Types:**
- **Static NAT:** 1:1 mapping
- **Dynamic NAT:** Pool of public IPs
- **PAT (Port Address Translation):** Many private IPs share one public IP

**NAT Table:**
```
Inside Local    Inside Global   Outside Global
192.168.1.10:5555 → 203.0.113.5:30001 → 8.8.8.8:53
192.168.1.20:6666 → 203.0.113.5:30002 → 8.8.4.4:80
```

**NAT Traversal Issues:**
- Breaks end-to-end principle
- Complicates P2P
- Solutions: STUN, TURN, ICE

### ICMP (Internet Control Message Protocol)

**Message Types:**
| Type | Name | Use |
|------|------|-----|
| 0 | Echo Reply | Ping response |
| 3 | Destination Unreachable | Network/host/port unreachable |
| 8 | Echo Request | Ping |
| 11 | Time Exceeded | TTL expired (traceroute) |
| 12 | Parameter Problem | Header error |

**Ping:**
```bash
ping -c 4 8.8.8.8
```

**Traceroute:**
```bash
traceroute google.com  # UDP/ICMP
traceroute -T google.com  # TCP
```

---

# Part III: Transport Layer

---

## 7. UDP (User Datagram Protocol)

### Characteristics
- Connectionless
- No reliability, ordering, or flow control
- Lightweight (8-byte header)
- Best-effort delivery

### UDP Header
```
 0      7 8     15 16    23 24    31
+--------+--------+--------+--------+
|     Source      |   Destination   |
|      Port       |      Port       |
+--------+--------+--------+--------+
|                 |                 |
|     Length      |    Checksum     |
+--------+--------+--------+--------+
|             Data ...              |
```

### When to Use UDP
- Real-time applications (VoIP, gaming)
- DNS queries (small, idempotent)
- DHCP
- Streaming media
- IoT (constrained devices)

### UDP Socket Programming

```c
#include <sys/socket.h>
#include <netinet/in.h>

// Server
int sockfd = socket(AF_INET, SOCK_DGRAM, 0);

struct sockaddr_in server_addr = {
    .sin_family = AF_INET,
    .sin_port = htons(8080),
    .sin_addr.s_addr = INADDR_ANY
};

bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));

char buffer[1024];
struct sockaddr_in client_addr;
socklen_t client_len = sizeof(client_addr);

int n = recvfrom(sockfd, buffer, sizeof(buffer), 0,
                 (struct sockaddr*)&client_addr, &client_len);

sendto(sockfd, buffer, n, 0,
       (struct sockaddr*)&client_addr, client_len);
```

---

## 8. TCP (Transmission Control Protocol)

### Characteristics
- Connection-oriented
- Reliable delivery (retransmissions)
- In-order delivery
- Flow control (sliding window)
- Congestion control

### TCP Header
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |           |U|A|P|R|S|F|                               |
| Offset| Reserved  |R|C|S|S|Y|I|            Window             |
|       |           |G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options (if data offset > 5)               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Flags:**
- **SYN:** Synchronize sequence numbers
- **ACK:** Acknowledgment field valid
- **FIN:** Finish, no more data
- **RST:** Reset connection
- **PSH:** Push data immediately
- **URG:** Urgent data

### Three-Way Handshake

```
Client                 Server
   |                      |
   |------- SYN --------->|  seq=x
   |                      |
   |<---- SYN+ACK --------|  seq=y, ack=x+1
   |                      |
   |------- ACK --------->|  seq=x+1, ack=y+1
   |                      |
   |   Connection Open    |
```

### Four-Way Termination

```
Client                 Server
   |                      |
   |------- FIN --------->|  (Client done sending)
   |                      |
   |<------- ACK ---------|
   |                      |
   |<------- FIN ---------|  (Server done sending)
   |                      |
   |------- ACK --------->|
   |                      |
   |    TIME_WAIT (2MSL)  |
```

**TIME_WAIT:** 2 × MSL (Maximum Segment Lifetime, typically 60 seconds)
- Ensures final ACK arrives
- Allows old packets to expire

### TCP State Machine

```
                             CLOSED
                               |
              passive open     |    active open
              -----------      |    -----------
                              |
            +------+   rcv SYN       send SYN
            |LISTEN|<-----------|---------------
            +------+            |
               |        +-------+-------+
          rcv SYN       |   SYN-SENT    |
          send SYN,ACK  +-------+-------+
               |                |
        +------+------+    rcv SYN,ACK
        |  SYN-RCVD   |    send ACK
        +------+------+        |
               |        +------+------+
          rcv ACK       | ESTABLISHED |
          ---------     +------+------+
                               |
```

### Sequence Numbers

- Initial Sequence Number (ISN): Random (security)
- Sequence number: First byte of segment
- Acknowledgment number: Next expected byte

**Example:**
```
A → B: SEQ=100, 500 bytes data
B → A: ACK=600 (expecting byte 600 next)
A → B: SEQ=600, 200 bytes data
B → A: ACK=800
```

### Reliable Delivery

**Retransmission:**
- Timeout (RTO): Based on RTT estimate
- Fast retransmit: 3 duplicate ACKs

**RTT Estimation:**
```
SRTT = (1-α) × SRTT + α × RTT_sample  (α = 0.125)
RTTVAR = (1-β) × RTTVAR + β × |SRTT - RTT_sample|  (β = 0.25)
RTO = SRTT + 4 × RTTVAR
```

### Flow Control

**Sliding Window:**
```
Receive Window = Buffer Size - (LastByteRcvd - LastByteRead)
```

- Sender limits: LastByteSent - LastByteAcked ≤ ReceiveWindow
- Window size advertised in TCP header

**Zero Window:**
- Receiver advertises window = 0
- Sender sends window probe periodically
- Silly window syndrome avoidance (Nagle's algorithm)

### Congestion Control

**Variables:**
- cwnd: Congestion window
- ssthresh: Slow start threshold
- rwnd: Receive window
- Effective window = min(cwnd, rwnd)

**Slow Start:**
```
Initial: cwnd = 1 MSS (or 10 MSS in modern implementations)
On each ACK: cwnd += 1 MSS
Effect: Exponential growth (doubles each RTT)
Until: cwnd >= ssthresh → switch to congestion avoidance
```

**Congestion Avoidance:**
```
On each ACK: cwnd += MSS × (MSS / cwnd)
Effect: Linear growth (~1 MSS per RTT)
```

**On Timeout:**
```
ssthresh = cwnd / 2
cwnd = 1 MSS
Return to slow start
```

**Fast Retransmit & Fast Recovery (TCP Reno):**
```
On 3 duplicate ACKs:
    ssthresh = cwnd / 2
    cwnd = ssthresh + 3 MSS
    Retransmit lost segment
    For each additional dup ACK: cwnd += 1 MSS
    On new ACK: cwnd = ssthresh (exit fast recovery)
```

**TCP CUBIC (Linux default):**
```
cwnd = C(t - K)³ + Wmax

Where:
K = ∛(Wmax × β / C)
Wmax = cwnd at last loss
β = 0.7 (multiplicative decrease factor)
C = 0.4 (scaling constant)
t = time since last loss
```

### TCP Socket Programming

**Server:**
```c
#include <sys/socket.h>
#include <netinet/in.h>

int sockfd = socket(AF_INET, SOCK_STREAM, 0);

int opt = 1;
setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

struct sockaddr_in addr = {
    .sin_family = AF_INET,
    .sin_port = htons(8080),
    .sin_addr.s_addr = INADDR_ANY
};

bind(sockfd, (struct sockaddr*)&addr, sizeof(addr));
listen(sockfd, SOMAXCONN);

struct sockaddr_in client_addr;
socklen_t client_len = sizeof(client_addr);
int connfd = accept(sockfd, (struct sockaddr*)&client_addr, &client_len);

char buffer[1024];
ssize_t n = recv(connfd, buffer, sizeof(buffer), 0);
send(connfd, buffer, n, 0);

close(connfd);
close(sockfd);
```

**Client:**
```c
int sockfd = socket(AF_INET, SOCK_STREAM, 0);

struct sockaddr_in server_addr = {
    .sin_family = AF_INET,
    .sin_port = htons(8080)
};
inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);

connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr));

send(sockfd, "Hello", 5, 0);

char buffer[1024];
recv(sockfd, buffer, sizeof(buffer), 0);

close(sockfd);
```

### Socket Options

```c
// Reuse address (quick restart)
int opt = 1;
setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

// Keep-alive
setsockopt(sockfd, SOL_SOCKET, SO_KEEPALIVE, &opt, sizeof(opt));

// TCP no delay (disable Nagle's algorithm)
setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, &opt, sizeof(opt));

// Receive buffer size
int rcvbuf = 65536;
setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &rcvbuf, sizeof(rcvbuf));

// Non-blocking
fcntl(sockfd, F_SETFL, O_NONBLOCK);
```

### I/O Multiplexing

**select():**
```c
fd_set readfds;
FD_ZERO(&readfds);
FD_SET(sockfd, &readfds);

struct timeval tv = {.tv_sec = 5, .tv_usec = 0};
int ret = select(sockfd + 1, &readfds, NULL, NULL, &tv);

if (FD_ISSET(sockfd, &readfds)) {
    // Ready to read
}
```

**poll():**
```c
struct pollfd fds[2];
fds[0].fd = sockfd;
fds[0].events = POLLIN;

int ret = poll(fds, 1, 5000);  // 5 second timeout

if (fds[0].revents & POLLIN) {
    // Ready to read
}
```

**epoll() (Linux):**
```c
int epfd = epoll_create1(0);

struct epoll_event ev = {
    .events = EPOLLIN,
    .data.fd = sockfd
};
epoll_ctl(epfd, EPOLL_CTL_ADD, sockfd, &ev);

struct epoll_event events[10];
int n = epoll_wait(epfd, events, 10, 5000);

for (int i = 0; i < n; i++) {
    if (events[i].data.fd == sockfd) {
        // Ready to read
    }
}
```

---

# Part IV: Application Layer

---

## 9. DNS (Domain Name System)

### Hierarchy

```
                    . (root)
                      |
        +------+------+------+
        |      |      |      |
       com    org    net    edu
        |
    +---+---+
    |       |
 google   amazon
    |
   www
```

**FQDN:** www.google.com. (note trailing dot)

### Record Types

| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address | www.example.com → 93.184.216.34 |
| AAAA | IPv6 address | www.example.com → 2606:2800:220:1:248:1893:25c8:1946 |
| CNAME | Alias | www → blog.example.com |
| MX | Mail server | example.com → 10 mail.example.com |
| NS | Name server | example.com → ns1.example.com |
| TXT | Text | example.com → "v=spf1 include:..." |
| PTR | Reverse lookup | 34.216.184.93.in-addr.arpa → www.example.com |
| SOA | Start of authority | Zone metadata |

### DNS Resolution

**Recursive Query (client → resolver):**
```
1. Client asks resolver for www.google.com
2. Resolver does all the work
3. Resolver returns final answer
```

**Iterative Query (resolver → servers):**
```
1. Resolver asks root server
   → "Ask .com servers"
2. Resolver asks .com server
   → "Ask google.com servers"
3. Resolver asks google.com server
   → "93.184.216.34"
4. Resolver caches and returns to client
```

### DNS Message Format

```
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                      ID                       |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    QDCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    ANCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    NSCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                    ARCOUNT                    |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

**Flags:**
- QR: Query (0) or Response (1)
- RD: Recursion Desired
- RA: Recursion Available
- RCODE: 0=No error, 3=NXDOMAIN

### DNS Tools

```bash
# Query
dig www.google.com
dig @8.8.8.8 google.com MX
dig +trace google.com

# Reverse lookup
dig -x 8.8.8.8

# nslookup
nslookup google.com
nslookup -type=MX google.com
```

---

## 10. HTTP (Hypertext Transfer Protocol)

### HTTP/1.1

**Request Format:**
```
GET /path HTTP/1.1
Host: www.example.com
User-Agent: curl/7.68.0
Accept: */*
Connection: keep-alive

```

**Response Format:**
```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1234
Connection: keep-alive

<html>...</html>
```

### HTTP Methods

| Method | Safe | Idempotent | Cacheable | Body |
|--------|------|------------|-----------|------|
| GET | Yes | Yes | Yes | No |
| HEAD | Yes | Yes | Yes | No |
| POST | No | No | Conditional | Yes |
| PUT | No | Yes | No | Yes |
| DELETE | No | Yes | No | Optional |
| PATCH | No | No | No | Yes |
| OPTIONS | Yes | Yes | No | Optional |

### Status Codes

| Code | Category | Examples |
|------|----------|----------|
| 1xx | Informational | 101 Switching Protocols |
| 2xx | Success | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirection | 301 Moved Permanently, 302 Found, 304 Not Modified |
| 4xx | Client Error | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| 5xx | Server Error | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable |

### Headers

**Request Headers:**
- `Host`: Required in HTTP/1.1
- `User-Agent`: Client identification
- `Accept`: Content types client accepts
- `Accept-Encoding`: Compression methods
- `Cookie`: Send cookies
- `Authorization`: Credentials

**Response Headers:**
- `Content-Type`: MIME type of body
- `Content-Length`: Size of body
- `Set-Cookie`: Set cookies
- `Cache-Control`: Caching directives
- `Location`: Redirect URL

### Caching

**Cache-Control:**
```
Cache-Control: max-age=3600         # Cache for 1 hour
Cache-Control: no-cache             # Validate with server
Cache-Control: no-store             # Don't cache at all
Cache-Control: private              # Don't cache in shared caches
```

**ETag/If-None-Match:**
```
Server: ETag: "abc123"
Client: If-None-Match: "abc123"
Server: 304 Not Modified (if unchanged)
```

**Last-Modified/If-Modified-Since:**
```
Server: Last-Modified: Wed, 01 Jan 2020 00:00:00 GMT
Client: If-Modified-Since: Wed, 01 Jan 2020 00:00:00 GMT
Server: 304 Not Modified (if unchanged)
```

### HTTP/2

**Features:**
- Binary framing (not text)
- Multiplexing (multiple streams over single connection)
- Server push
- Header compression (HPACK)
- Stream prioritization

**Frame Format:**
```
+-----------------------------------------------+
|                 Length (24)                   |
+---------------+---------------+---------------+
|   Type (8)    |   Flags (8)   |
+-+-------------+---------------+-------------------------------+
|R|                 Stream Identifier (31)                      |
+=+=============================================================+
|                   Frame Payload (0...)                      ...
+---------------------------------------------------------------+
```

### HTTP/3 (QUIC)

- Built on UDP (not TCP)
- Integrated TLS 1.3
- 0-RTT connection establishment
- Better handling of packet loss
- Connection migration (change IP without reconnection)

---

## 11. TLS/SSL

### TLS Handshake (1.2)

```
Client                                 Server
   |------- ClientHello --------------->|
   |       (versions, cipher suites,    |
   |        random)                     |
   |                                    |
   |<------ ServerHello ----------------|
   |       (chosen cipher, random)      |
   |<------ Certificate ----------------|
   |<------ ServerKeyExchange ----------|
   |<------ ServerHelloDone ------------|
   |                                    |
   |------- ClientKeyExchange --------->|
   |------- ChangeCipherSpec ---------->|
   |------- Finished ------------------>|
   |                                    |
   |<------ ChangeCipherSpec -----------|
   |<------ Finished -------------------|
   |                                    |
   |======= Encrypted Data =============|
```

### TLS 1.3 (Faster)

```
Client                                 Server
   |------- ClientHello --------------->|
   |       (key share included)         |
   |                                    |
   |<------ ServerHello ----------------|
   |<------ EncryptedExtensions --------|
   |<------ Certificate ----------------|
   |<------ CertificateVerify ----------|
   |<------ Finished -------------------|
   |                                    |
   |------- Finished ------------------>|
   |                                    |
   |======= Encrypted Data =============|
```

**1-RTT vs 0-RTT:**
- 1-RTT: Standard handshake
- 0-RTT: Resume with pre-shared key (PSK)

### Cipher Suites

**Format:** TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256

- **Key Exchange:** ECDHE (Elliptic Curve Diffie-Hellman Ephemeral)
- **Authentication:** RSA (server certificate)
- **Encryption:** AES-128-GCM
- **MAC:** SHA256 (for PRF)

### Certificate Chain

```
Root CA (self-signed, trusted)
    |
    v
Intermediate CA (signed by Root)
    |
    v
Server Certificate (signed by Intermediate)
```

---

## 12. DHCP (Dynamic Host Configuration Protocol)

### DORA Process

```
Client                                 Server
   |------- DISCOVER ------------------>|  (broadcast)
   |<------ OFFER ----------------------|
   |------- REQUEST ------------------->|  (broadcast)
   |<------ ACK ------------------------|
```

**Lease Contains:**
- IP address
- Subnet mask
- Default gateway
- DNS servers
- Lease duration

### DHCP Packet

```
op (1)  | htype (1) | hlen (1) | hops (1)
xid (4) - transaction ID
secs (2) | flags (2)
ciaddr (4) - client IP (if knows)
yiaddr (4) - your IP (server assigns)
siaddr (4) - server IP
giaddr (4) - gateway IP (relay)
chaddr (16) - client MAC
sname (64) - server hostname
file (128) - boot filename
options (variable)
```

---

## 13. Network Security

### Firewalls

**Packet Filter:**
- Stateless
- Rules based on: IP, port, protocol
- Fast but limited

**Stateful Firewall:**
- Tracks connection state
- Allows return traffic automatically
- More secure

**Application Gateway (Proxy):**
- Inspects application layer
- Can filter content
- Higher overhead

### Common Attacks

**ARP Spoofing:**
- Send fake ARP replies
- Redirect traffic through attacker
- Mitigation: Static ARP, DAI

**DNS Spoofing:**
- Return fake DNS responses
- Mitigation: DNSSEC

**SYN Flood:**
- Send many SYN packets
- Exhaust server resources
- Mitigation: SYN cookies

**Man-in-the-Middle:**
- Intercept communication
- Mitigation: TLS, certificate pinning

### IPsec

**Modes:**
- **Transport:** Encrypt payload only
- **Tunnel:** Encrypt entire IP packet (VPN)

**Protocols:**
- **AH (Authentication Header):** Integrity only
- **ESP (Encapsulating Security Payload):** Encryption + integrity

**IKE (Internet Key Exchange):**
- Phase 1: Establish secure channel
- Phase 2: Negotiate IPsec SA

---

## 14. Wireless Networks (802.11)

### Standards

| Standard | Frequency | Max Speed | Year |
|----------|-----------|-----------|------|
| 802.11b | 2.4 GHz | 11 Mbps | 1999 |
| 802.11a | 5 GHz | 54 Mbps | 1999 |
| 802.11g | 2.4 GHz | 54 Mbps | 2003 |
| 802.11n | 2.4/5 GHz | 600 Mbps | 2009 |
| 802.11ac | 5 GHz | 6.9 Gbps | 2013 |
| 802.11ax (Wi-Fi 6) | 2.4/5 GHz | 9.6 Gbps | 2019 |

### CSMA/CA

```
1. Listen to channel
2. If busy, wait
3. If idle, wait DIFS (DCF Interframe Space)
4. If still idle, send RTS (Request to Send)
5. Receive CTS (Clear to Send)
6. Send data
7. Wait for ACK
8. If collision detected, random backoff
```

### Hidden Node Problem

```
    A -------- AP -------- B
    
A can't hear B (out of range)
Both might transmit simultaneously
→ Collision at AP
```

**Solution:** RTS/CTS

### Security

**WEP (Weak):**
- RC4 encryption
- Broken, don't use

**WPA/WPA2:**
- TKIP (WPA) or CCMP/AES (WPA2)
- Personal (PSK) or Enterprise (802.1X)

**WPA3:**
- SAE (Simultaneous Authentication of Equals)
- Forward secrecy
- Protected Management Frames

---

## Network Commands Reference

### Linux Networking Commands

```bash
# Interface configuration
ip addr show                    # List interfaces
ip link set eth0 up/down        # Enable/disable interface
ip addr add 192.168.1.10/24 dev eth0

# Routing
ip route show                   # Show routing table
ip route add 10.0.0.0/8 via 192.168.1.1
ip route add default via 192.168.1.1

# DNS
cat /etc/resolv.conf
systemd-resolve --status

# Network diagnostics
ping -c 4 google.com
traceroute google.com
mtr google.com                  # Continuous traceroute
dig www.google.com
nslookup google.com

# Socket inspection
ss -tuln                        # TCP/UDP listening sockets
ss -p                           # With process info
netstat -tuln                   # Older alternative

# Packet capture
tcpdump -i eth0
tcpdump -i eth0 port 80
tcpdump -w capture.pcap
wireshark                       # GUI packet analyzer

# Network performance
iperf3 -s                       # Server
iperf3 -c server_ip             # Client

# Firewall (iptables)
iptables -L                     # List rules
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -j DROP

# Firewall (ufw - simpler)
ufw enable
ufw allow 22/tcp
ufw status

# Network namespaces (containers)
ip netns add ns1
ip netns exec ns1 ip addr show
```

---

## Cross-References

- [[02_Computer_Architecture]] - Network interface hardware
- [[07_Operating_Systems]] - Socket system calls, network stack
- [[08_C_Programming]] - Socket programming details
- [[05_Database_Systems]] - Distributed database networking
