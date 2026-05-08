# DHCP Simulation

## Prerequisite

This note provides a detailed step-by-step simulation of the DHCP four-message exchange. Familiarity with [[DHCP_Protocol|DHCP Protocol]] basics is assumed.

## Network Setup

**Network Topology**:
```
         DHCP Server
         (10.0.0.10)
            │
       [Router/Gateway]
       (192.168.1.1)
            │
      ┌─────┼─────┐
      │     │     │
   Client1 Client2 Printer
  (no IP)  (no IP)  (static: 192.168.1.100)
```

**DHCP Server Configuration**:
- Subnet: 192.168.1.0/24
- Address pool: 192.168.1.2 - 192.168.1.99
- Gateway: 192.168.1.1
- DNS servers: 8.8.8.8, 8.8.4.4
- Lease time: 3600 seconds (1 hour)
- Subnet mask: 255.255.255.0

**Client 1 Information**:
- MAC address: 00:0A:95:9D:68:16
- No IP address initially

## Timeline of DHCP Exchange

### Time $t = 0$ s: Client 1 Powers On

**Event**: Client 1 boots; network interface initializes. Client has no IP address.

**Initial Client State**:
- IP Address: None (0.0.0.0)
- MAC Address: 00:0A:95:9D:68:16
- Default Gateway: Unknown
- DNS Servers: Unknown

**Client Action**: Initiate DHCP discovery.

### Time $t = 0.1$ s: Message 1 - DHCP DISCOVER

**Sender**: Client 1
**Receiver**: All DHCP servers (broadcast)
**Transport**: UDP port 68 (client) to UDP port 67 (server)

**DHCP DISCOVER Message**:

```
Frame [Ethernet]:
  Destination MAC: FF:FF:FF:FF:FF:FF (broadcast)
  Source MAC: 00:0A:95:9D:68:16 (Client 1)

IP Header:
  Source IP: 0.0.0.0 (client doesn't have IP)
  Destination IP: 255.255.255.255 (broadcast)
  Protocol: 17 (UDP)

UDP Header:
  Source Port: 68
  Destination Port: 67

DHCP Message:
  OP: 1 (Request)
  HTYPE: 1 (Ethernet)
  HLEN: 6 (MAC address length)
  HOPS: 0
  XID: 0x12345678 (random transaction ID)
  SECS: 0 (just started)
  FLAGS: 0x8000 (broadcast flag set; client can't receive unicast)
  CIADDR: 0.0.0.0 (client IP; unknown)
  YIADDR: 0.0.0.0 (your IP; not yet assigned)
  SIADDR: 0.0.0.0 (server IP; unknown)
  GIADDR: 0.0.0.0 (gateway IP; relay not used in this case)
  CHADDR: 00:0A:95:9D:68:16 (Client 1's MAC address)
  
  DHCP Options:
    Option 53 (DHCP Message Type): 1 (DISCOVER)
    Option 50 (Requested IP Address): Not present (no preference)
    Option 55 (Parameter Request List):
      - 1 (Subnet Mask)
      - 3 (Router)
      - 6 (DNS Servers)
      - 15 (Domain Name)
      - 51 (Lease Time)
    Option 255 (End)
```

**Message Size**: ~300 bytes.

### Time $t = 0.2$ s: Message 2 - DHCP OFFER

**Sender**: DHCP Server
**Receiver**: Client 1 (broadcast, due to client's broadcast flag)
**Transport**: UDP port 67 (server) to UDP port 68 (client)

**Server Processing**:
```
1. Server receives DISCOVER from Client 1.
2. Server looks up available addresses in pool: 192.168.1.2 - 192.168.1.99
3. Server selects: 192.168.1.50 (arbitrary selection)
4. Server reserves this address temporarily.
5. Server prepares OFFER with assigned address and configuration.
```

**DHCP OFFER Message**:

```
Frame [Ethernet]:
  Destination MAC: FF:FF:FF:FF:FF:FF (broadcast)
  Source MAC: Server's MAC (e.g., 00:0B:85:AC:4D:10)

IP Header:
  Source IP: 10.0.0.10 (DHCP Server)
  Destination IP: 255.255.255.255 (broadcast, per client's flag)
  Protocol: 17 (UDP)

UDP Header:
  Source Port: 67
  Destination Port: 68

DHCP Message:
  OP: 2 (Reply)
  HTYPE: 1 (Ethernet)
  HLEN: 6
  HOPS: 0
  XID: 0x12345678 (echoed from DISCOVER)
  SECS: 1 (time since client started)
  FLAGS: 0x8000 (echoed)
  CIADDR: 0.0.0.0
  YIADDR: 192.168.1.50 (offered address)
  SIADDR: 10.0.0.10 (DHCP Server IP)
  GIADDR: 0.0.0.0
  CHADDR: 00:0A:95:9D:68:16 (echoed from DISCOVER)
  
  DHCP Options:
    Option 53 (DHCP Message Type): 2 (OFFER)
    Option 54 (Server Identifier): 10.0.0.10 (Server's IP)
    Option 51 (Lease Time): 3600 seconds (1 hour)
    Option 1 (Subnet Mask): 255.255.255.0
    Option 3 (Router): 192.168.1.1
    Option 6 (DNS Servers): 8.8.8.8, 8.8.4.4
    Option 15 (Domain Name): "example.com"
    Option 255 (End)
```

**Server State After OFFER**:
```
Address Pool Status:
  192.168.1.2 - 192.168.1.49: Available
  192.168.1.50: Reserved (offered to Client 1, Expiry: t + 60s)
  192.168.1.51 - 192.168.1.99: Available
  
Lease Table:
  MAC: 00:0A:95:9D:68:16
  State: OFFERED
  IP Address: 192.168.1.50
  Expiry: t + 60s (OFFER timeout; if no REQUEST by then, address is released)
```

### Time $t = 0.3$ s: Client 1 Receives OFFER

**Client Processing**:
```
1. Client receives OFFER from server.
2. Client extracts offered IP: 192.168.1.50.
3. Client notes server IP: 10.0.0.10.
4. Client prepares REQUEST message to confirm.
```

**Client State**:
```
IP Address: Still 0.0.0.0 (not yet bound)
Offered Address: 192.168.1.50
Selected Server: 10.0.0.10
Lease Time: 3600 seconds
```

### Time $t = 0.4$ s: Message 3 - DHCP REQUEST

**Sender**: Client 1
**Receiver**: All servers (broadcast)
**Transport**: UDP port 68 to 67

**DHCP REQUEST Message**:

```
Frame [Ethernet]:
  Destination MAC: FF:FF:FF:FF:FF:FF (broadcast)
  Source MAC: 00:0A:95:9D:68:16

IP Header:
  Source IP: 0.0.0.0 (still doesn't have IP)
  Destination IP: 255.255.255.255 (broadcast)
  Protocol: 17 (UDP)

UDP Header:
  Source Port: 68
  Destination Port: 67

DHCP Message:
  OP: 1 (Request)
  XID: 0x12345678 (same transaction ID)
  SECS: 0.4
  FLAGS: 0x8000
  CIADDR: 0.0.0.0 (still doesn't have IP)
  YIADDR: 192.168.1.50 (echoing the offered address)
  SIADDR: 10.0.0.10 (address of selected server)
  GIADDR: 0.0.0.0
  CHADDR: 00:0A:95:9D:68:16
  
  DHCP Options:
    Option 53 (DHCP Message Type): 3 (REQUEST)
    Option 54 (Server Identifier): 10.0.0.10 (confirms selection)
    Option 50 (Requested IP Address): 192.168.1.50
    Option 55 (Parameter Request List): [1, 3, 6, 15, 51]
    Option 255 (End)
```

**Note**: By specifying the server ID (10.0.0.10) in the REQUEST, the client implicitly declines OFFERs from other servers.

### Time $t = 0.5$ s: Server Processes REQUEST

**Server Processing**:
```
1. Server receives REQUEST.
2. Server checks if Requested IP == Offered IP: YES (192.168.1.50).
3. Server checks if Server ID matches its own IP: YES (10.0.0.10).
4. Server confirms the address allocation.
5. Server prepares ACK response.
```

**Server State After REQUEST**:
```
Lease Table:
  MAC: 00:0A:95:9D:68:16
  State: REQUESTING → (about to be BOUND)
  IP Address: 192.168.1.50
```

### Time $t = 0.6$ s: Message 4 - DHCP ACK

**Sender**: DHCP Server
**Receiver**: Client 1 (broadcast, per client's flag)
**Transport**: UDP 67 to 68

**DHCP ACK Message**:

```
Frame [Ethernet]:
  Destination MAC: FF:FF:FF:FF:FF:FF (broadcast)
  Source MAC: Server's MAC

IP Header:
  Source IP: 10.0.0.10 (DHCP Server)
  Destination IP: 255.255.255.255
  Protocol: 17 (UDP)

UDP Header:
  Source Port: 67
  Destination Port: 68

DHCP Message:
  OP: 2 (Reply)
  XID: 0x12345678 (echoed)
  SECS: 0.6
  FLAGS: 0x8000 (echoed)
  CIADDR: 0.0.0.0
  YIADDR: 192.168.1.50 (confirmed address)
  SIADDR: 10.0.0.10 (server IP)
  GIADDR: 0.0.0.0
  CHADDR: 00:0A:95:9D:68:16 (echoed)
  
  DHCP Options:
    Option 53 (DHCP Message Type): 5 (ACK)
    Option 54 (Server Identifier): 10.0.0.10
    Option 51 (Lease Time): 3600
    Option 1 (Subnet Mask): 255.255.255.0
    Option 3 (Router): 192.168.1.1
    Option 6 (DNS Servers): 8.8.8.8, 8.8.4.4
    Option 15 (Domain Name): "example.com"
    Option 255 (End)
```

### Time $t = 0.7$ s: Client 1 Receives ACK

**Client Processing**:
```
1. Client receives ACK.
2. Client extracts configuration:
     - IP Address: 192.168.1.50
     - Subnet Mask: 255.255.255.0
     - Gateway: 192.168.1.1
     - DNS: 8.8.8.8, 8.8.4.4
     - Lease Time: 3600 seconds
3. Client configures its network interface with these parameters.
4. Client starts lease timer:
     - Renewal time (T1): 3600 / 2 = 1800 seconds
     - Rebinding time (T2): 3600 × 7/8 = 3150 seconds
```

**Client Final State**:
```
IP Address: 192.168.1.50
Subnet Mask: 255.255.255.0
Gateway: 192.168.1.1
DNS Servers: 8.8.8.8, 8.8.4.4
Lease Expiry: t + 3600 seconds
Lease Renewal Time (T1): t + 1800 seconds
Lease Rebinding Time (T2): t + 3150 seconds
Server: 10.0.0.10
```

**Server Final State**:
```
Lease Table:
  MAC: 00:0A:95:9D:68:16
  State: BOUND
  IP Address: 192.168.1.50
  Expiry: t + 3600 seconds (at this time, address reverts to available)
  
Address Pool:
  192.168.1.2 - 192.168.1.49: Available
  192.168.1.50: LEASED to 00:0A:95:9D:68:16 (expires at t + 3600s)
  192.168.1.51 - 192.168.1.99: Available
```

## Summary of Four-Message Exchange

| Message | Source | Destination | Type | Key Data |
|---|---|---|---|---|
| 1 | Client | Broadcast | DISCOVER | XID=0x12345678, MAC, Requests options |
| 2 | Server | Broadcast | OFFER | XID=0x12345678, YIADDR=192.168.1.50, Lease time |
| 3 | Client | Broadcast | REQUEST | Server ID=10.0.0.10, Requested IP=192.168.1.50 |
| 4 | Server | Broadcast | ACK | YIADDR=192.168.1.50, Configuration, Lease time |

**Total Time for Configuration**: ~0.7 seconds (typical for local networks; can be 1-10 seconds in large networks with congestion).

## Lease Renewal at T1

### Time $t = 1800$ s (T1): Renewal Attempt

Client 1 attempts to renew its lease from the original server.

**DHCP REQUEST (Renewal)**:

```
Frame [Ethernet]:
  Source MAC: 00:0A:95:9D:68:16

IP Header:
  Source IP: 192.168.1.50 (now has IP)
  Destination IP: 10.0.0.10 (unicast to server, not broadcast)
  Protocol: 17 (UDP)

DHCP Message:
  OP: 1 (Request)
  XID: 0x87654321 (new transaction ID for renewal)
  CIADDR: 192.168.1.50 (now includes current IP)
  YIADDR: 0.0.0.0 (no longer requesting new IP)
  SIADDR: 10.0.0.10 (server being renewed with)
  CHADDR: 00:0A:95:9D:68:16
  
  DHCP Options:
    Option 53: 3 (REQUEST)
    Option 55: [1, 3, 6, 15, 51]
    Option 255: End
```

**Server Processes Renewal**:
```
1. Server receives REQUEST with CIADDR=192.168.1.50.
2. Server checks lease table for MAC 00:0A:95:9D:68:16.
3. Server finds active lease for 192.168.1.50.
4. Server ACKs the renewal, extending lease by another 3600 seconds.
```

**Server Response (Renewal ACK)**:
- Same as initial ACK, but with new lease expiry time (t + 1800 + 3600 = t + 5400 seconds).

### Time $t = 3150$ s (T2): Rebinding Attempt (if Renewal Failed)

If the original server was unreachable at T1, the client broadcasts a DHCP REQUEST at T2.

**DHCP REQUEST (Rebinding)**:

```
IP Header:
  Source IP: 192.168.1.50
  Destination IP: 255.255.255.255 (broadcast, since original server not responding)
  
DHCP Message:
  OP: 1 (Request)
  CIADDR: 192.168.1.50
  (No SIADDR specified; accepting any available server)
```

Any available DHCP server can respond with an ACK, renewing the lease.

## Related Concepts

- [[DHCP_Protocol]]: DHCP protocol specification and mechanisms.
- [[Broadcast_Routing_Algorithms]]: DHCP uses broadcast for DISCOVER and REQUEST messages.
- [[IP_Addressing_Review]]: IP address assignment and subnet masks.

---

**Previous:** [[DHCP_Protocol]]
