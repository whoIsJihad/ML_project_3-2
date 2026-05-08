# DHCP Protocol

## Definition

DHCP (Dynamic Host Configuration Protocol) is a protocol that automatically assigns IP addresses and other network configuration parameters to hosts on a network. DHCP enables hosts to obtain network configuration without manual administration.

Formally, DHCP is a client-server protocol where:
- **DHCP Server**: Maintains a pool of IP addresses and distributes them to clients.
- **DHCP Client**: A host requesting network configuration.

## Motivation for DHCP

### Manual Configuration Problems

Historically, IP addresses were manually configured:

```
Administrator writes:
192.168.1.10/24
Gateway: 192.168.1.1
DNS: 8.8.8.8
```

on each host. This is:
- **Error-prone**: Typos lead to unreachable hosts.
- **Not scalable**: Infeasible in large networks (thousands of hosts).
- **Inflexible**: Changing networks requires reconfiguration of all hosts.
- **Wastes addresses**: Addresses are permanently assigned even to temporarily connected hosts.

### DHCP Solution

DHCP automates address assignment:
- Hosts obtain addresses upon connecting to the network.
- Addresses are reclaimed when hosts disconnect.
- Centralized configuration (on DHCP server) applies to all hosts.
- Network changes require updating only the DHCP server.

## DHCP Protocol: Message Types

DHCP uses UDP messages on ports 67 (server) and 68 (client).

### DHCP DISCOVER

**Initiator**: Client (newly booted, no IP address).

**Purpose**: Locate available DHCP servers.

**Format**:
```
DHCP DISCOVER Message:
  op: 1 (request)
  htype: 1 (Ethernet)
  hlen: 6 (MAC address length)
  hops: 0
  xid: [transaction ID, 32-bit random]
  secs: [seconds since DHCP process start]
  flags: 0x8000 (broadcast flag)
  ciaddr: 0.0.0.0 (client has no address)
  yiaddr: 0.0.0.0
  siaddr: 0.0.0.0
  giaddr: 0.0.0.0
  chaddr: [client's MAC address]
  [DHCP Options]:
    Message Type: DISCOVER
    Client Identifier: [MAC address or string]
    Requested IP Address: [optional, if client has a preferred address]
    Parameter Request List: [DNS, Gateway, etc.]
```

**Transmission**: Broadcast (destination IP 255.255.255.255, destination MAC FF:FF:FF:FF:FF:FF).

### DHCP OFFER

**Initiator**: DHCP Server.

**Purpose**: Offer an IP address and configuration to a client.

**Format**:
```
DHCP OFFER Message:
  op: 2 (reply)
  htype: 1 (Ethernet)
  xid: [same transaction ID as DISCOVER]
  yiaddr: [IP address being offered, e.g., 192.168.1.100]
  siaddr: [IP address of DHCP server, e.g., 192.168.1.1]
  [DHCP Options]:
    Message Type: OFFER
    Server Identifier: [DHCP server IP]
    Lease Time: [seconds, e.g., 3600 (1 hour)]
    Subnet Mask: [e.g., 255.255.255.0]
    Router (Gateway): [e.g., 192.168.1.1]
    DNS Servers: [e.g., 8.8.8.8, 8.8.4.4]
```

**Transmission**: Broadcast (some servers) or unicast (if possible).

### DHCP REQUEST

**Initiator**: Client.

**Purpose**: Request (formally accept) the offered IP address and parameters.

**Format**:
```
DHCP REQUEST Message:
  op: 1 (request)
  xid: [same transaction ID]
  ciaddr: 0.0.0.0 or [previously assigned IP if renewing]
  yiaddr: 0.0.0.0
  [DHCP Options]:
    Message Type: REQUEST
    Server Identifier: [IP of the DHCP server from which offer was received]
    Requested IP Address: [the offered IP, e.g., 192.168.1.100]
    Parameter Request List: [parameters being requested]
```

**Transmission**: Broadcast (during initial address acquisition) or unicast (during renewal).

### DHCP ACK (Acknowledgment)

**Initiator**: DHCP Server.

**Purpose**: Confirm the address assignment and provide binding information.

**Format**:
```
DHCP ACK Message:
  op: 2 (reply)
  xid: [same transaction ID]
  yiaddr: [assigned IP address]
  [DHCP Options]:
    Message Type: ACK
    Lease Time: [e.g., 3600 seconds]
    [All configuration parameters]
```

**Transmission**: Unicast to the newly assigned address (or broadcast if client's IP is not yet stable).

### DHCP NAK (Negative Acknowledgment)

**Initiator**: DHCP Server.

**Purpose**: Reject a REQUEST (e.g., requested address no longer available).

**Format**:
```
DHCP NAK Message:
  [DHCP Options]:
    Message Type: NAK
    [Optional error message]
```

**Consequence**: Client returns to DISCOVER phase.

### DHCP DECLINE

**Initiator**: Client.

**Purpose**: Inform server that the offered address is already in use (detected by ARP).

**Transmission**: Broadcast.

### DHCP RELEASE

**Initiator**: Client.

**Purpose**: Relinquish an assigned address (e.g., when host shuts down).

**Format**:
```
DHCP RELEASE Message:
  [DHCP Options]:
    Message Type: RELEASE
    Server Identifier: [DHCP server that assigned the address]
```

## DHCP Address Lifecycle

### Acquisition (Initial Binding)

**Timeline**:
1. **DISCOVER**: Client sends broadcast asking for DHCP servers.
2. **OFFER**: Servers respond with address offers.
3. **REQUEST**: Client selects one offer and requests the address.
4. **ACK**: Selected server confirms and assigns the address.

**Result**: Client has an IP address with a lease time (e.g., 1 hour).

### Renewal

Before lease expires, the client renews:

**Timeline**:
1. Client sends **REQUEST** directly to the server (unicast) at T = 0.5 × lease_time.
2. Server responds with **ACK** (renewed lease).

**If Server Unresponsive**:
3. At T = 0.875 × lease_time, client broadcasts a new **REQUEST**.
4. Any DHCP server can respond with **ACK** (rebinding).

### Expiration and Release

- If lease expires without renewal, the client must stop using the address.
- Upon graceful shutdown, client sends **RELEASE** to free the address.

## Lease Time and Address Pool Management

### Lease Time

A lease grants the address for a finite duration (lease time):

$$\text{Lease Time} = T_{\text{lease}}$$

Typical values: 1 hour to 7 days (depends on network). Short leases are common in large networks with high churn (many hosts connecting/disconnecting); long leases reduce traffic but risk address exhaustion.

### Address Pool

The DHCP server maintains a pool of available addresses:

$$\text{Available Pool} = \text{Configured Range} - \text{Reserved Addresses} - \text{Assigned Addresses}$$

**Example**: 
- Configured range: 192.168.1.100 to 192.168.1.200 (101 addresses).
- Reserved: 192.168.1.1-10 (gateway, DNS servers), 192.168.1.200 (broadcast) = 11 addresses.
- Available: 101 - 11 = 90 addresses.

### Address Exhaustion

If all available addresses are assigned, new clients cannot obtain addresses (unless leases expire). Network administrators must:
- Increase pool size.
- Reduce lease time.
- Analyze usage and free stale leases.

## DHCP Options

DHCP options (TLV - Type-Length-Value format) carry configuration parameters:

| Option # | Name | Value | Purpose |
|---|---|---|---|
| 1 | Subnet Mask | 255.255.255.0 | Network mask |
| 3 | Router | 192.168.1.1 | Default gateway |
| 6 | DNS Servers | 8.8.8.8, 8.8.4.4 | DNS resolver addresses |
| 15 | Domain Name | example.com | Domain name search |
| 28 | Broadcast Address | 192.168.1.255 | Broadcast address |
| 51 | IP Address Lease Time | 3600 | Lease duration (seconds) |
| 54 | DHCP Server Identifier | 192.168.1.1 | Identifying the server |

Clients can request specific options via **Parameter Request List** option (code 55).

## Relay Agents (DHCP Relay)

In large networks, not all subnets have a DHCP server. **DHCP Relay Agents** forward DHCP messages across subnets.

### Relay Function

```
Client (Subnet A) 
  ↓ [DHCP DISCOVER broadcast]
Relay Agent (connected to Subnet A and Subnet B)
  ↓ [Unicast DHCP DISCOVER to DHCP Server on Subnet C]
DHCP Server (Subnet C)
  ↓ [Response]
Relay Agent
  ↓ [Broadcast/Unicast response back to Subnet A]
Client
```

**Relay Message Format**:
- The relay agent modifies the `giaddr` field (gateway IP) to its own address.
- This informs the DHCP server which subnet the client is on, allowing it to assign addresses from the appropriate pool.

## DHCP Security Considerations

### Lack of Authentication

DHCP messages are not authenticated; a malicious actor can:
- Send fake DHCP OFFER with wrong gateway (DHCP spoofing).
- Redirect traffic through attacker's router (man-in-the-middle attack).

**Mitigation**:
- **DHCP Snooping** (switch-based): Switches forward DHCP only from trusted ports.
- **DHCP Authentication (DHCPv6)**: Optional authentication in DHCP for IPv6.

### IP Starvation

An attacker can request many DHCP addresses, exhausting the pool and denying service to legitimate clients.

**Mitigation**:
- Rate limiting on DHCP requests.
- Per-MAC-address request limits.

## DHCP vs. Static Configuration

| Aspect | DHCP | Static |
|---|---|---|
| **Configuration** | Automatic | Manual |
| **Scalability** | Excellent | Poor |
| **Control** | Centralized (server) | Distributed (each host) |
| **Overhead** | Periodic renewal messages | None |
| **Flexibility** | High (easy to change) | Low |
| **Server Dependency** | Required | Not required |
| **Use Case** | General networks | Servers, routers, infrastructure |

## Related Concepts

- [[DHCP_Simulation]]: Step-by-step DHCP process trace.
- [[IP_Addressing_Review]]: IP address concepts and subnetting.
- [[Broadcast_Routing]]: DHCP uses broadcast discovery.

---

**Next:** [[DHCP_Simulation]]
