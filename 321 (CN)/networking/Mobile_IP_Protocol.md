# Mobile IP Protocol

## Overview

Mobile IP is a standardized protocol suite (RFC 3344 for IPv4, RFC 6275 for IPv6) that implements the mobile host routing concepts described in [[Mobile_Host_Routing]]. This note details the protocol operations, message formats, and mechanisms.

## Protocol Entities

### Mobile Node (MN)

A mobile node is an IP host or router that can change its point of attachment to the Internet while maintaining its home IP address.

**Properties**:
- Maintains a permanent **home address** on its home network.
- Can be attached to any foreign network.
- Participates actively in mobility management by sending registration and binding update messages.

### Home Agent (HA)

The home agent is a router on the home network that tunnels datagrams to mobile nodes currently visiting a foreign network.

**Responsibilities**:
- Intercepts datagrams sent to the mobile node's home address.
- Maintains a binding table mapping home addresses to care-of addresses.
- Encapsulates (tunnels) intercepted datagrams to the mobile node's current care-of address.
- Advertises itself to mobile nodes via agent advertisements.

### Foreign Agent (FA)

The foreign agent is a router on a foreign network that provides services to visiting mobile nodes.

**Responsibilities**:
- Advertises its presence to mobile nodes via agent advertisements.
- Accepts registration messages from mobile nodes.
- De-tunnels datagrams received from the home agent (removes the outer IP header).
- Forwards de-tunneled datagrams to the mobile node on the local link.

**Note**: With optimizations in modern IPv6 Mobile IP, the foreign agent function may be omitted; mobile nodes may directly register care-of addresses without an intermediary.

## Agent Discovery

### Agent Advertisement

Agents (both home and foreign) periodically broadcast **agent advertisement** messages on their network links. These are ICMP Router Advertisements (ICMP type 9) with Mobile IP extensions.

**Format**:
```
ICMP Router Advertisement + Mobile IP Extension (Type 16)
  - Router Address: IP address of the advertising agent
  - Preference Level: Priority for agent selection
  - Lifetime: Duration for which the agent is reachable
  - Care-of Addresses (for FA): List of available care-of addresses
```

**Frequency**: Advertisements are sent periodically (typically every 1-3 seconds on a link).

### Mobile Node Behavior

Upon receiving an agent advertisement:

1. If the advertisement is from a **foreign agent** (via network prefix analysis):
   - The mobile node extracts a care-of address from the advertisement.
   - If not already registered with that foreign agent, initiate registration.

2. If the advertisement is from a **home agent** (recognized by home network prefix):
   - The mobile node may update its home agent state.

## Registration Process

### Registration Request

When a mobile node arrives at a foreign network, it sends a **Registration Request** message to the foreign agent.

**Format (Mobile IPv4)**:
```
Registration Request
  - Type: 1 (Request)
  - Lifetime: Requested registration lifetime (0 to 65535 seconds)
  - Home Address: The mobile node's home IP address
  - Home Agent: Home agent's IP address
  - Care-of Address: IP address assigned to mobile node on foreign network
  - Identification: Random number for matching replies
  - Extensions:
    - Authenticator (MD5 hash for security)
```

**Processing at Foreign Agent**:
```
upon Reception of Registration Request from MN:
  1. Validate request (signature, lifetime)
  2. Encapsulate and forward to Home Agent
  3. Store temporary state for MN
  4. Wait for acknowledgment from HA
```

### Registration Reply

The foreign agent encapsulates and forwards the registration request to the home agent. The home agent processes and sends a **Registration Reply** back.

**Registration Reply Format**:
```
Registration Reply
  - Type: 3 (Reply)
  - Code: 0 (registration accepted)
         1 (registration accepted, simultaneous bindings allowed)
         64-255 (various rejection codes)
  - Lifetime: Granted registration lifetime
  - Home Address: Echoed from request
  - Home Agent: Home agent's address
  - Identification: Echoed from request
  - Extensions: Authenticators
```

**Processing**:
```
at Home Agent:
  upon Reception of Registration Request from FA:
    1. Validate MN identity (authentication)
    2. Create/update binding entry: (home_addr, care_of_addr, lifetime)
    3. Send Registration Reply to FA with code = 0
    4. Set expiration timer for binding (reset on each registration)

at Foreign Agent:
  upon Reception of Registration Reply:
    1. Forward reply to MN on local link
    2. Activate care-of address for MN
    3. Store binding state with lifetime
```

### Registration Timeout and Renewal

Registrations have a limited **lifetime** (typically 10-20 minutes for mobile IPv4). The mobile node must periodically renew its registration before the binding expires.

**Timeline**:
```
t = 0:     Registration accepted with lifetime = 600 seconds
t = 300:   MN sends renewal (before half-lifetime expires)
t = 600:   Old binding expires if renewal not received
```

If registration lapses, the home agent stops tunneling packets to the mobile node's care-of address. Packets destined for the mobile node are lost.

## Tunneling: Encapsulation and Decapsulation

### IP-within-IP Tunneling

The home agent uses **IP-within-IP encapsulation** (IP protocol 4) to tunnel packets destined for the mobile node to the care-of address.

**Encapsulation**:
```
Original Packet (from Correspondent C to Mobile Node M):
┌─────────────────────────────────────┐
│ IP Header (dest = Home_Address)     │
│ Transport Layer Header (TCP/UDP)    │
│ Payload                             │
└─────────────────────────────────────┘

After Encapsulation by HA:
┌─────────────────────────────────────┐
│ Outer IP Header:                    │
│   Source: Home Agent IP             │
│   Destination: Care-of Address      │
│   Protocol: 4 (IP-in-IP)            │
├─────────────────────────────────────┤
│ Inner IP Header (original):         │
│   Source: C                         │
│   Destination: Home Address         │
│   ...rest of original packet...     │
├─────────────────────────────────────┤
│ Transport and Payload (unchanged)   │
└─────────────────────────────────────┘
```

### Decapsulation

When the foreign agent receives a tunneled packet:

```
upon Reception of IP-in-IP packet at FA:
  1. Check outer destination address (should be FA's care-of address)
  2. Remove outer IP header
  3. Extract inner IP packet
  4. Check inner destination address (should be MN's home address)
  5. Forward inner packet to MN on local link (via link-layer delivery)
```

The mobile node receives the inner packet with original source and destination intact, unaware of tunneling.

## Binding Updates for Route Optimization

### Problem: Triangle Routing

Without optimization, all traffic from correspondent $C$ to mobile node $M$ routes through the home agent, even if $C$ and $M$ are on the same network segment (inefficient).

### Binding Update Message

To optimize, the mobile node sends a **Binding Update** message to active correspondents, informing them of the current care-of address.

**Binding Update Format (IPv6 MIPv6, RFC 6275)**:
```
Binding Update Header Type (type = 2)
  - Sequence: Version number (prevents reordering attacks)
  - Lifetime: Duration binding remains valid (in 4-second units)
  - A (Acknowledge): Request binding acknowledgment
  - H (Home Registration): Register with home agent
  - L (Link-local address): Home address is link-local
  - K (Key): Use returned home keygen token
  - Mobility Options:
    - Home Address Option: MN's home address
    - Binding Authorization Data Option: Authentication
```

### Binding Cache at Correspondent

The correspondent maintains a **binding cache**:

```
Binding Cache Entry:
  - Home Address: M's permanent IP address
  - Care-of Address: M's current location address
  - Sequence Number: Binding version
  - Lifetime: When binding expires
  - Flags: Various control flags
```

When sending to $M$:
```
if (M's home address in binding cache):
  send packet to care-of address (from cache)
  include Home Address Option in IP extension header
else:
  send packet to M's home address (via default routing)
```

### Return Routing Trees (RRT)

When $M$ sends packets using route optimization:
- Source address in packet: Home address ($A_M$).
- Destination address: Correspondent's address.
- Routing: Based on correspondent's location.

Correspondents recognize the home address in the IP extension header and can verify that the return packet is from the correct mobile node.

## Security Considerations

### Authentication Mechanisms

Mobile IP uses **MD5-based authenticators** to prevent unauthorized registration and binding updates:

**Home Agent Authentication**:
```
Authenticator = MD5(Nonce || Home Address || Care-of Address || Lifetime)
         where Nonce is a shared secret or derived from challenge-response
```

**Correspondent Authentication** (in IPv6 MIPv6):
- Uses **Return Routability Procedure** to verify that MN can reach Correspondent.
- MN proves it can receive packets at both home address and care-of address.
- Only after successful proof, correspondent updates binding cache.

### Return Routability Procedure (IPv6)

To prevent binding update attacks in route optimization:

```
1. Correspondent sends Home Test Init to MN's home address
2. Home Agent forwards to care-of address
   → MN receives Home Keygen Token

3. Correspondent sends Care-of Test Init to MN's care-of address
   → MN receives Care-of Keygen Token

4. MN sends Binding Update with both tokens
   → Correspondent verifies MN can reach both addresses
   → Binding is accepted
```

This prevents an attacker from redirecting traffic to a third party.

## IPv6 Mobile IP (Mobile IPv6)

Modern Mobile IP is primarily deployed for IPv6 (RFC 6275). Key differences from IPv4 Mobile IP:

1. **No Foreign Agent**: IPv6 allows direct care-of address configuration (via stateless address autoconfiguration).
2. **Home Address Option**: Carried in IPv6 extension headers instead of IP options.
3. **Enhanced Security**: Return Routability Procedure provides stronger authentication.
4. **Prefix Optimization**: MN can form care-of address within foreign network prefix.

## Performance Metrics

### Handover Latency

Time for mobile node to restore connectivity after moving to a new network:

```
Total Handover Latency = 
  + Link loss detection time (100-500 ms)
  + Agent discovery time (0-1000 ms depending on advertisement frequency)
  + Registration processing time (10-100 ms)
  + Binding propagation time (if updating correspondents)
```

Typical total: 100 ms to several seconds.

### Packet Loss During Handover

If a mobile node loses connectivity before completing registration at the new foreign agent, packets in transit are lost. Buffering at the old foreign agent can reduce this.

## Related Concepts

- [[Mobile_Host_Routing]]: Conceptual foundations.
- [[Network_Mobility_NEMO]]: Extension to mobile subnets.
- [[Tunneling_and_VPN]]: Encapsulation mechanism.
- [[IP_Addressing_Review]]: Care-of address assignment and home address structure.

---

**Next:** [[Network_Mobility_NEMO]]
