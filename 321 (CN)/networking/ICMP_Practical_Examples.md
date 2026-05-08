# ICMP Practical Examples

## Prerequisite

This note provides practical command-line examples and detailed packet traces for ICMP operations. Familiarity with [[ICMP_Protocol|ICMP Protocol]] basics is assumed.

## Ping: ICMP Echo Request/Reply

### Command and Basic Usage

```bash
$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=119 time=20.5 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=119 time=21.2 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=119 time=20.8 ms
^C
--- 8.8.8.8 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2005ms
rtt min/avg/max/stddev = 20.5/20.8/21.2/0.3 ms
```

### Packet Structure: ICMP Echo Request

```
IP Header:
  Source IP: 192.168.1.100 (local host)
  Destination IP: 8.8.8.8 (Google DNS)
  TTL: 64
  Protocol: 1 (ICMP)

ICMP Header:
  Type: 8 (Echo Request)
  Code: 0
  Checksum: 0x1234 (calculated)
  Identifier: 0x5678 (process ID or random)
  Sequence Number: 1

Payload:
  Timestamp: [8 bytes]
  Data: [48 bytes of arbitrary data]
```

### Packet Structure: ICMP Echo Reply

```
IP Header:
  Source IP: 8.8.8.8
  Destination IP: 192.168.1.100
  TTL: 119 (response TTL)
  Protocol: 1 (ICMP)

ICMP Header:
  Type: 0 (Echo Reply)
  Code: 0
  Checksum: 0x5678 (calculated)
  Identifier: 0x5678 (echoed from request)
  Sequence Number: 1 (echoed from request)

Payload:
  Timestamp: [copied from request]
  Data: [copied from request]
```

### Analysis

The output shows:
- **RTT (Round-Trip Time)**: Time for the echo request to reach the destination and reply to return (20.5 ms in the example).
- **TTL**: 119 in the reply indicates the server's TTL was 64 and crossed some hops (64 - 119 mod 256 = 9 hops, approximately, depending on IP/OS defaults).
- **Sequence Numbers**: Incremented by 1 for each request; helps verify reply correspondence and detect lost packets.

### Ping with Different Options

**Specify Packet Size**:
```bash
$ ping -s 1024 8.8.8.8
# Sends 1024-byte ICMP packets (payload size)
```

**Limit Hop Count (TTL)**:
```bash
$ ping -t 5 8.8.8.8
# Sets initial TTL = 5; stops if target unreachable before 5 hops
```

**Continuous Ping**:
```bash
$ ping -i 0.2 8.8.8.8
# Sends ping every 0.2 seconds (interval)
```

## Traceroute: ICMP Time Exceeded

### Command and Basic Usage

```bash
$ traceroute 8.8.8.8
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
 1  gateway.local (192.168.1.1)  0.5 ms  0.4 ms  0.6 ms
 2  isp-router.isp.com (203.0.113.1)  10.2 ms  10.1 ms  10.3 ms
 3  backbone1.isp.com (198.18.0.1)  20.5 ms  20.4 ms  20.6 ms
 4  google-router.peering.isp.com (199.33.0.1)  25.2 ms  25.1 ms  25.3 ms
 5  8.8.8.8 (8.8.8.8)  28.0 ms  28.1 ms  28.2 ms
```

### How Traceroute Works

**Process**:

1. **Send Packets with Increasing TTL**:
   ```
   Packet 1: TTL = 1 → Expires at hop 1
   Packet 2: TTL = 2 → Expires at hop 2
   ...
   Packet N: TTL = 30 → Reaches destination or times out
   ```

2. **Collect ICMP Time Exceeded Responses**:
   - When a packet with TTL = 1 is forwarded by the first router, TTL becomes 0.
   - Router sends ICMP Time Exceeded (Type 11, Code 0) back to source.
   - Source learns the identity of the first hop (from reply source address).

3. **Repeat for Each Hop**:
   - TTL = 2 reaches second hop, expires, generates Time Exceeded from second router.
   - Continue until destination is reached or maximum hops (default 30) exhausted.

### Packet Trace for Traceroute Hop 1

**Outgoing Packet (TTL = 1)**:
```
IP Header:
  Source: 192.168.1.100
  Destination: 8.8.8.8
  TTL: 1
  Protocol: 6 (TCP) or 17 (UDP) [depends on traceroute variant]
  Identification: 1001

[TCP/UDP Header with high port number]
```

**Router 1 Processing**:
```
Decrement TTL: 1 - 1 = 0
TTL expired; discard packet
Send ICMP Time Exceeded back
```

**Incoming Response (ICMP Time Exceeded)**:
```
IP Header:
  Source: 192.168.1.1 (hop 1 router)
  Destination: 192.168.1.100
  TTL: 64 (or configured value)
  Protocol: 1 (ICMP)

ICMP Header:
  Type: 11 (Time Exceeded)
  Code: 0 (TTL Exceeded in Transit)
  Checksum: [calculated]

ICMP Data:
  [Original packet IP header + first 8 bytes of original payload]
```

### Example: Tracing a Route with Hops

| Hop | TTL | Router IP | RTT (ms) | Response Type |
|---|---|---|---|---|
| 1 | 1 | 192.168.1.1 | 0.5 | Time Exceeded |
| 2 | 2 | 203.0.113.1 | 10.2 | Time Exceeded |
| 3 | 3 | 198.18.0.1 | 20.5 | Time Exceeded |
| 4 | 4 | 199.33.0.1 | 25.2 | Time Exceeded |
| 5 | 5 | 8.8.8.8 | 28.0 | Echo Reply |

At hop 5, the destination is reached; if the source sends an ICMP Echo Request instead of TCP/UDP, it receives an Echo Reply, confirming the destination.

### Interpreting Traceroute Output

**Unreachable Hop (marked with \*)**:
```
 8  * * *
```
The router at hop 8 either:
- Does not respond to ICMP Time Exceeded (firewall filtering).
- Is behind a NAT that doesn't forward ICMP.
- Is misconfigured.

**Reverse Path Different**:
```
 3  hop3.example.com (192.0.2.1)  20.5 ms
 4  hop4.example.com (192.0.2.2)  15.3 ms
```
Latency decreased from hop 3 to 4, indicating asymmetric routing (outgoing and return paths differ).

## Ping to Diagnose Host Reachability

### Scenario: Host is Unreachable

```bash
$ ping 10.0.0.50
PING 10.0.0.50 (10.0.0.50) 56(84) bytes of data.
From 192.168.1.1 icmp_seq=1 Destination Unreachable (Network Unreachable)
From 192.168.1.1 icmp_seq=2 Destination Unreachable (Network Unreachable)
```

**Analysis**: The local gateway (192.168.1.1) does not have a route to 10.0.0.50 and responds with ICMP Destination Unreachable (Type 3).

**ICMP Packet**:
```
Type: 3 (Destination Unreachable)
Code: 0 (Network Unreachable)
Checksum: [calculated]

Data:
  [Original echo request IP header + payload]
```

### Scenario: Host Responds After Delay

```bash
$ ping 10.1.1.100
64 bytes from 10.1.1.100: icmp_seq=1 ttl=64 time=150.5 ms
64 bytes from 10.1.1.100: icmp_seq=2 ttl=64 time=152.3 ms
```

**Analysis**: Host is reachable but has high latency (150 ms). Possible causes:
- Host is geographically distant.
- Network congestion.
- Host is processing other tasks (slow response).

## Diagnosing Network Issues with ICMP

### Case Study 1: Asymmetric Routing

```bash
$ traceroute server.example.com
1  gateway (0.5 ms)
2  isp-router (10.2 ms)
3  peer-router (25.5 ms)
4  server.example.com (28.0 ms)

$ traceroute -T 8 (reverse, from server to client)
1  server.example.com (0.3 ms)
2  alt-router (15.2 ms)     ← Different intermediate router
3  alt-isp (18.5 ms)        ← Different ISP router
4  client (20.1 ms)
```

The outgoing path via `peer-router` differs from the return path via `alt-router`. This is asymmetric routing, common when ISPs have multiple routes.

### Case Study 2: MTU Issue (IP Fragmentation)

```bash
$ ping -s 1472 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 1472(1500) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=119 time=20.5 ms
```

Works fine. 

```bash
$ ping -s 1473 8.8.8.8 -M do
(do = don't fragment)
PING 8.8.8.8 (8.8.8.8) 1473(1501) bytes of data.
From 192.168.1.1: icmp_seq=1 Frag needed (DF-bit set)
```

With the larger size and DF flag, the router cannot forward (would require fragmentation) and responds with ICMP Destination Unreachable (Type 3, Code 4, "Fragmentation Needed").

## Related Concepts

- [[ICMP_Protocol]]: ICMP message types, codes, and protocol details.
- [[IP_Fragmentation]]: IP Fragmentation issues related to ICMP feedback.
- [[Tunneling_and_VPN]]: ICMP Path MTU Discovery in tunneled networks.

---

**Next:** [[DHCP_Protocol]]
