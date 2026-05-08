# Tunneling and VPN

## Definition: Tunneling

Tunneling is the encapsulation of one protocol inside another protocol at the same or lower layer. Formally, tunneling is the process of wrapping a complete packet (including its headers and payload) of one protocol as the payload of another protocol, allowing the inner packet to traverse a network that understands only the outer protocol.

Let $P_{\text{inner}}$ denote an inner packet with headers and $P_{\text{outer}}$ denote an outer packet. Tunneling creates:

$$P_{\text{tunneled}} = [\text{Outer Headers}] + P_{\text{inner}}$$

where $P_{\text{inner}}$ becomes the payload of $P_{\text{outer}}$.

## Motivations for Tunneling

### 1. Protocol Transition

When transitioning from one protocol to another, tunneling allows old protocol traffic to traverse new infrastructure.

**Example**: IPv6 over IPv4.
- IPv6 packets are encapsulated in IPv4 packets to traverse IPv4-only networks.
- IPv4 routers forward the outer IPv4 packet; IPv6 content is preserved.

**Structure**:
```
[IPv4 Header] [IPv6 Header] [Payload]
```

### 2. Network Virtualization

Virtual networks can be created by tunneling traffic across a physical network.

**Example**: VPN (Virtual Private Network).
- Private network traffic (IP packets from a corporate LAN) is encapsulated in public Internet packets.
- Traffic appears to the public network as generic encrypted traffic.
- Privacy is maintained; the public network cannot see the private network structure.

### 3. Multicast over Unicast Networks

Some networks don't support multicast. Tunneling allows multicast packets to traverse unicast-only networks.

**Example**: MBone (Multicast Backbone).
- Multicast packets are encapsulated in unicast packets sent between multicast-capable routers.
- Non-multicast networks are transparently crossed.

### 4. Mobile IP

As discussed in [[Mobile_IP_Protocol]], the home agent tunnels packets to a mobile node's care-of address.

## Tunneling Mechanisms

### IP-in-IP Tunneling

The simplest tunneling method: one IP packet is encapsulated in another IP packet.

**Packet Structure**:
```
[Outer IP Header]
[Inner IP Header]
[Transport Layer Header (TCP/UDP)]
[Payload]
```

**Outer IP Header Fields**:
- Source Address: Tunnel entry point.
- Destination Address: Tunnel exit point.
- Protocol Field: 4 (IP-in-IP).

**Inner IP Header**: Unchanged from the original packet.

**Processing**:
- **Encapsulation** (at tunnel entry): Add outer IP header before inner packet.
- **Transmission**: Outer packet is routed normally.
- **Decapsulation** (at tunnel exit): Remove outer IP header; forward inner packet.

**Example**:
```
Original packet:
[IP: src=192.168.1.2, dst=10.0.0.5] [TCP] [Data]

After IP-in-IP tunneling (entry: 203.0.113.1, exit: 198.51.100.1):
[IP: src=203.0.113.1, dst=198.51.100.1, proto=4]
[IP: src=192.168.1.2, dst=10.0.0.5] [TCP] [Data]

At tunnel exit, decapsulation removes outer header:
[IP: src=192.168.1.2, dst=10.0.0.5] [TCP] [Data]
(forwarded to 10.0.0.5)
```

### Generic Routing Encapsulation (GRE)

GRE is a more flexible tunneling protocol (RFC 2784) that can encapsulate various protocols.

**GRE Header**:
- Version and Flags (2 bytes).
- Protocol Type (2 bytes): Type of encapsulated protocol (IP, Ethernet, etc.).
- Optional Checksum and Key fields.

**Advantages**:
- Supports encapsulation of non-IP protocols (Ethernet, AppleTalk).
- Optional security extensions for encryption.

### IPsec Tunneling

IPsec (Internet Protocol Security) provides both encryption and authentication, making it suitable for VPNs.

**Two Modes**:
1. **Transport Mode**: Only the payload (TCP/UDP) is encrypted; IP header is not encrypted.
2. **Tunnel Mode**: Entire IP packet is encrypted and encapsulated in a new IP header.

**Tunnel Mode Structure**:
```
[Outer IP Header]
[IPsec Tunnel Header (ESP/AH)]
[Encrypted Inner IP Packet]
```

## Virtual Private Networks (VPN)

### Definition

A Virtual Private Network (VPN) is a network connection that creates a secure tunnel through a public network (typically the Internet), allowing remote users or networks to communicate as if they were on the same private network.

### VPN Architecture

```
Corporate Headquarters (LAN)
│
├─ Router (VPN Gateway)
│
[IPsec Tunnel through Internet]
│
├─ Remote Office (LAN)
└─ Router (VPN Gateway)
```

Traffic between the headquarters LAN and remote office LAN is:
1. Encapsulated (tunneled).
2. Encrypted (for confidentiality).
3. Authenticated (for integrity).

To the public Internet, the traffic appears as encrypted packets between the two VPN gateways; the actual destination addresses (inside the private networks) are hidden.

### VPN Types

**Site-to-Site VPN**:
- Connects two or more entire networks (sites) securely.
- Gateways (routers) at each site manage the tunnel.
- All traffic between sites is encrypted.

**Remote Access VPN** (Client-to-Site):
- Individual users connect to a VPN gateway from remote locations.
- Each user's traffic is encrypted through the gateway.

### VPN Protocols

**IPsec**:
- Standard protocol for VPN; part of IPv4 and mandatory in IPv6.
- Provides encryption (ESP), authentication (AH), and key exchange (IKE).

**TLS/SSL VPN**:
- Uses SSL/TLS (same as HTTPS) for encryption.
- Easier to deploy through firewalls (uses port 443, typically open).
- Often used for remote access VPNs (e.g., OpenVPN).

**WireGuard**:
- Modern VPN protocol; cryptographically proven.
- Lower overhead than IPsec; faster handshakes.
- Growing adoption for VPN services.

## Tunnel Overhead

Tunneling adds overhead in multiple dimensions:

### Packet Size Overhead

Each tunneled packet is larger due to the outer header.

**Example**: IPv4-in-IPv4 tunneling adds 20 bytes (IPv4 header size).

Original MTU: 1500 bytes.
Tunneled MTU: 1500 - 20 = 1480 bytes (for inner packet).

**Impact**: Fragmentation may be required if inner packet is large. Path MTU Discovery (PMTUD) is used to determine the effective MTU through the tunnel.

### Processing Overhead

**Encapsulation**: CPU cost to add outer header.
**Encryption** (VPN): Significant CPU cost for encryption/decryption.
**Decapsulation**: CPU cost to remove outer header.

Modern CPUs and hardware accelerators (cryptographic coprocessors) minimize this overhead.

### Bandwidth Overhead

- Outer headers consume bandwidth.
- Encryption may add padding (to block size).

**Example**: A 100-byte payload encrypted may become 128 bytes (block size 16) after padding, an additional 28% overhead.

## MTU and Path MTU Discovery

### Path MTU (PMTU)

The PMTU is the smallest MTU along a path from source to destination.

**Issue with Tunneling**: The outer IP header reduces the available space for the inner packet. If the inner packet is larger than PMTU - tunnel_overhead, fragmentation is required.

**Solution**: Path MTU Discovery (PMTUD).

- Source sends probe packets of decreasing size.
- When a packet is too large, a router sends an ICMP "Packet Too Big" message.
- Source learns the PMTU and adjusts packet size.

### IPv6 Fragmentation

IPv6 eliminates in-network fragmentation; only the source can fragment. Hosts must implement PMTUD properly for IPv6.

Tunneling IPv6 packets through IPv4 requires careful MTU management.

## Tunnel Establishment and Management

### Static Tunnels

Tunnel endpoints are manually configured.

**Advantages**: Simple, no overhead.
**Disadvantages**: Not scalable; must be manually updated if endpoints change.

### Dynamic Tunnels

Tunnel endpoints are discovered automatically (e.g., via routing protocols or directory services).

**Example**: Automatic IPv6 Tunneling (6to4).
- IPv6 routers automatically form tunnels through IPv4 networks.
- No manual configuration needed.

### Tunnel Monitoring

Tunnels must be monitored for:
- Link failures (tunnel endpoint unreachable).
- High latency or packet loss.

If a tunnel is down, traffic should be rerouted (if alternate tunnels exist) or the tunnel should be re-established.

## Security Implications of Tunneling

### Encryption

Tunneling alone (IP-in-IP or GRE) provides no encryption. Content is still visible to intermediate routers.

VPN solutions add encryption to protect privacy.

### Authentication

IPsec provides authentication headers (AH) to ensure packets are not tampered with en route.

TLS/SSL provides certificate-based authentication.

### Key Management

VPN protocols must securely exchange cryptographic keys. This is typically done via:
- **IKE (Internet Key Exchange)**: Used by IPsec; negotiates keys automatically.
- **Manual keys**: Configured statically (simple but not scalable).
- **Public Key Infrastructure (PKI)**: Certificates verify identities.

## Related Concepts

- [[Mobile_IP_Protocol]]: Home agent tunneling using IP-in-IP.
- [[Network_Mobility_NEMO]]: Tunneling for mobile network prefixes.
- [[IP_Addressing_Review]]: IP headers and address formats.
- [[ICMP_Protocol]]: ICMP messages (including "Packet Too Big") used in PMTUD.

---

**Next:** [[IP_Fragmentation]]
