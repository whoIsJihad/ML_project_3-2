# Network Mobility (NEMO)

## Definition and Motivation

Network Mobility (NEMO) extends the mobility management concepts of [[Mobile_IP_Protocol]] from individual mobile hosts to entire network subnets. A mobile network is a subnet that changes its point of attachment to the Internet while maintaining its internal routing topology and addressing.

### Problem Statement

Consider a scenario where an entire network (e.g., a corporate LAN, a train network, a ship) moves as a unit:

- A train network maintains internal nodes (computers, servers, switches) connected via internal links.
- The train connects to the Internet through a gateway at various locations.
- The internal nodes must maintain fixed IP addresses (they are assigned addresses from the train's internal subnet).
- External nodes must be able to communicate with internal nodes despite the gateway's changing location.

**Classical Mobile IP Limitation**: Mobile IP assumes individual hosts move. Each host must independently register and maintain bindings. If hundreds of internal nodes move together, the burden of individual registrations becomes impractical.

**NEMO Solution**: A single registration at the mobile network's gateway represents the mobility of the entire subnet.

## Network Mobility Architecture

### Entities

**Mobile Network Prefix (MNP)**:
A contiguous block of IP addresses assigned to the mobile network. Example: `10.0.0.0/24`. All nodes within the mobile network have addresses from this prefix and do not change these addresses as the network moves.

**Mobile Router (MR)**:
A router at the boundary of the mobile network that:
- Maintains an IP address from the mobile network prefix (for internal communication).
- Registers care-of addresses when the mobile network moves to a new location.
- Acts as the gateway between the mobile network and external networks.

**Home Agent (HA)**:
The home agent for the mobile network (typically the same HA as in Mobile IP). It:
- Maintains a binding for the mobile network prefix to the MR's current care-of address.
- Intercepts packets destined for addresses in the mobile network prefix.
- Tunnels these packets to the MR's current care-of address.

**Correspondent Node (CN)**:
An external node communicating with nodes inside the mobile network.

### Topology Example

```
External Network (Internet)

         HA (Home Agent)
         |
    ─────┼─────────────
    |    |    |    |
    CN1  CN2  CN3  CN4
         |
         |---- NEMO Tunnel ----
                  |
          ┌──────────────────┐
          │ Mobile Network   │
          │  10.0.0.0/24     │
          ├──────────────────┤
          │   MR (gateway)   │
          │  10.0.0.1        │
          │  (current CoA)   │
          ├──────────────────┤
          │ Internal Nodes   │
          │ 10.0.0.2/3/4/.../│
          └──────────────────┘
```

In this diagram:
- External nodes CN1, CN2, etc., communicate with internal nodes.
- The HA intercepts packets destined for `10.0.0.0/24`.
- Packets are tunneled to the MR's current care-of address.

## NEMO Registration and Binding

### Binding Registration

When the mobile router detects movement to a new access network (foreign network), it performs registration similar to Mobile IP but for a **network prefix** rather than a single host address:

**Registration Request for Mobile Network**:
```
NEMO Registration Request
  - Mobile Network Prefix: 10.0.0.0/24
  - Mobile Router Home Address: 10.0.0.1
  - Care-of Address: <current address in foreign network>
  - Home Agent: <HA address>
  - Lifetime: Requested binding lifetime
  - Authenticators: Security credentials
```

**Binding at Home Agent**:
```
HA Binding Table Entry:
  Mobile Network Prefix: 10.0.0.0/24
  Care-of Address: <MR's current address>
  Binding Lifetime: <expiration time>
  Status: Active
```

### Binding Authorization

Authentication is critical to prevent unauthorized networks from hijacking a prefix registration. NEMO uses a shared secret between MR and HA:

```
Authorization Token = MD5(MR_home_address || MNP || HA_address || shared_secret)
```

This prevents any router from claiming to be the MR for the mobile network prefix.

## Tunneling for NEMO

### Encapsulation and Path

When a correspondent sends a packet to an address in the mobile network prefix, the home agent intercepts and tunnels it:

**Packet Flow**:
```
CN sends to: dest = 10.0.0.5 (internal node)
       ↓
HA intercepts (via routing/proxy)
  Outer IP Header:
    src = HA address
    dest = MR's care-of address (from binding)
  Payload = Original packet (src=CN, dest=10.0.0.5)
       ↓ [Tunnel through Internet]
MR receives tunneled packet
  De-tunnels: removes outer header
  Extracts inner packet (dest = 10.0.0.5)
       ↓
MR forwards to internal node 10.0.0.5 via internal routing
```

**Return Path**:
```
Internal node 10.0.0.5 sends to CN
  src = 10.0.0.5
  dest = CN
       ↓
MR forwards based on internal routing
  (destination is external, so forward to gateway/MR egress)
       ↓
MR routes packet outbound (from care-of address)
  src = 10.0.0.5 (preserved)
  dest = CN
       ↓
CN receives packet from 10.0.0.5
```

Note: Return packets are sent directly if routing allows (asymmetric routing). The MR doesn't normally tunnel return packets through the HA.

## Dynamic Movement and Prefix Management

### Handover Between Access Networks

When the mobile router moves from one foreign network to another:

```
t=0:     MR on foreign network 1 (access network A)
         Binding: MNP → care-of address A1

t=t1:    MR detects loss of connectivity to network A
         Performs agent discovery on network B

t=t2:    MR obtains new care-of address on network B (address B2)

t=t3:    MR sends new registration to HA
         Binding: MNP → care-of address B2

t=t3+Δ:  HA updates binding table
         All new packets to MNP tunnel to B2
```

During the transition period $(t_2, t_3)$, packets to the mobile network may be lost if they arrive at HA before the new binding is registered.

### Prefix Stability

A critical NEMO property is that the mobile network prefix remains **stable** regardless of movement:

- Internal nodes maintain fixed addresses within `10.0.0.0/24`.
- These addresses never change.
- Communication sessions ongoing within the network are unaffected by movement.

This is more efficient than having every internal node individually register with its HA (which would require changes to node addresses or complex per-node bindings).

## Route Optimization in NEMO

### NEMO Route Optimization

Similar to [[Mobile_IP_Protocol|Mobile IP]], NEMO can optimize routes to avoid triangle routing through the HA.

**Binding Update to Correspondent**:
```
MR sends Binding Update to CN:
  "Send packets for prefix 10.0.0.0/24 to my care-of address CoA"
  
CN updates binding cache:
  binding[10.0.0.0/24] = CoA
  
CN sends future packets directly to CoA (instead of HA)
  (with Home Address Option indicating original destination in MNP)
```

**Requirements**:
- CN must support NEMO (some routers may not understand prefix-based bindings).
- Authentication is more complex (must verify that the MR legitimately represents the prefix).

**Challenges**:
- Many legacy CN routers don't support NEMO Binding Updates.
- HA remains on the path for backward compatibility.

## Nested Mobile Networks (NEMO within NEMO)

A more complex scenario: a mobile network contains sub-networks, and the sub-network gateways are also mobile:

```
External Network

  HA1 (for outer mobile network)
  |
  ├─ NEMO Tunnel ────────────
                 |
           ┌─────────────────────┐
           │ Outer Mobile Net    │
           │ 10.0.0.0/24         │
           ├─────────────────────┤
           │  MR1 (outer gateway)│
           │  10.0.0.1           │
           ├─────────────────────┤
           │ Sub-network         │
           │ 10.0.1.0/25         │
           ├─────────────────────┤
           │  MR2 (inner gateway)│
           │  10.0.1.1           │
           ├─────────────────────┤
           │ Internal Nodes      │
           │ 10.0.1.2/3/4/...    │
           └─────────────────────┘
```

In this scenario:
- External traffic to `10.0.0.0/24` is tunneled by HA1 to MR1's care-of address.
- MR1 internally routes traffic destined for `10.0.1.0/25` toward MR2.
- MR2 may also be mobile, with its own HA (HA2) managing the `10.0.1.0/25` binding.

**Registration Chain**:
- MR2 registers `10.0.1.0/25` binding with HA2.
- MR1 registers `10.0.0.0/24` binding with HA1.

**Tunneling Chain**:
- External packet → HA1 tunnels to MR1 → MR1 routes to MR2 → MR2 delivers internally.

This creates a nested tunnel structure and increases complexity.

## Limitations and Current Deployment

### Challenges

1. **Poor Route Optimization**: Many networks don't support NEMO route optimization; all traffic still routes through HA.
2. **Nested Complexity**: Nested mobile networks significantly increase protocol complexity.
3. **Lack of Deployment**: NEMO is standardized (RFC 3963 for IPv6) but rarely deployed in practice.
4. **Alternative Technologies**: VPNs and software-defined networking are often preferred for mobile network scenarios.

### Modern Alternatives

In contemporary networks, NEMO scenarios are often handled by:
- **VPN tunneling**: The mobile router establishes a VPN connection to an organizational gateway.
- **SD-WAN**: Software-Defined Wide Area Networks provide more flexible mobility and traffic engineering.
- **IPv6 Deployment**: IPv6 Mobile IPv6 is standardized but adoption is limited.

## Related Concepts

- [[Mobile_IP_Protocol]]: Individual host mobility (NEMO extends this to networks).
- [[Tunneling_and_VPN]]: IP tunneling mechanism.
- [[Hierarchical_Routing]]: Addressing and routing structure for large networks.
- [[IP_Addressing_Review]]: Mobile network prefix assignment and management.

---

**Next:** [[Ad_Hoc_Networks_Overview]]
