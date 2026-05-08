# Mobile Host Routing

## Definition and Motivation

Mobile host routing addresses the problem of maintaining network connectivity for hosts that move across network domains. A mobile host is a node $M$ that can change its point of attachment to the network without losing its ability to receive packets.

### Problem Formulation

In traditional IP networking, a host's IP address encodes both:
1. The host's identity (which peer knows it as).
2. The host's location (the network segment it is attached to).

This binding works for stationary hosts but fails for mobile hosts:

Let $A_h$ denote a host's home address (IP address assigned in its home network). When the host moves to a foreign network, its packets arriving at the home network can no longer reach it—the host is not present on the home network segment.

**Core Challenge**: How do peers send packets to a mobile host when the host's location is unknown?

## Assumptions and Scope

This discussion assumes:
- A host has a **permanent home network** where its IP address is registered.
- The host may move to **foreign networks** (networks not its home network).
- The host may move multiple times during a communication session.
- The underlying IP network remains functional; only the host's point of attachment changes.

Scope is limited to **individual host mobility**. See [[Network_Mobility_NEMO]] for mobility of entire subnets.

## Indirect Routing with Tunneling

### Naive Approach: Problem Statement

Suppose a mobile host $M$ originally at home network $H$ moves to foreign network $F$. A correspondent node $C$ wishes to send packets to $M$.

Without special mechanisms:
1. $C$ sends packets to $M$'s home IP address $A_M$.
2. Routers forward packets toward home network $H$.
3. Packets arrive at home network but $M$ is no longer there—packets are lost.

### Solution: Indirect Routing

Indirect routing uses a **proxy** at the home network to capture packets destined for $M$ and forward them to $M$'s current location.

**Entities**:
- **Mobile Host** ($M$): Currently attached to foreign network $F$.
- **Home Agent** ($HA$): A router at the home network $H$ that proxies for $M$.
- **Correspondent** ($C$): The peer communicating with $M$.
- **Foreign Agent** ($FA$): A router at the foreign network $F$ that assists $M$.

**Mechanism**:
1. $M$ informs $HA$ of its current location (via a registration message).
2. $HA$ intercepts packets destined for $M$ via a broadcast on the home network link (claiming to own $M$'s address via ARP spoofing or proxy ARP).
3. $HA$ encapsulates captured packets and tunnels them to $FA$ at the foreign network.
4. $FA$ receives the tunneled packets and delivers them to $M$ on the foreign network link.

Reverse: $M$ sends packets to $C$ directly with source address $A_M$; $C$ replies to $A_M$, which routes back to $HA$, which tunnels to $FA$.

### Detailed Process

**Registration Phase**:
```
M (at foreign network) 
  → sends Care-of-Address (CoA) registration message
    → FA (learns M is present)
      → FA forwards registration to HA
        ← HA registers (M, CoA) mapping
```

**Packet Flow (C → M)**:
```
C sends packet with dest addr = A_M
  ↓ (routed to home network)
HA (intercepts via proxy ARP)
  ↓ (encapsulates packet, tunnels to FA)
Tunnel: IP_src=HA, IP_dest=FA, 
        Payload=(original packet with dest A_M)
  ↓
FA (receives tunneled packet)
  ↓ (decapsulates, extracts original packet)
M (receives packet with dest A_M)
```

**Return Path (M → C)**:
```
M sends packet with src=A_M, dest=C
  ↓ (routed normally)
C (receives packet from A_M)
```

Return packets are sent directly from $M$ to $C$ without tunneling through $HA$. This is called **asymmetric routing** or **triangle routing** because the forward path goes $C \to HA \to FA \to M$ but the return path goes directly $M \to C$.

## Triangle Routing Inefficiency

The indirect routing approach has a critical limitation: the **triangle routing problem**.

When $M$ is far from its home network and $C$ is near the home network, routing packets through $HA$ adds unnecessary delay and consumes bandwidth on the path $C \to HA \to FA$.

**Example**:
- Home network in New York.
- Mobile host in Tokyo (attached to a network near Tokyo).
- Correspondent in London.

Optimal path from London to Tokyo: direct routing through Pacific gateway.

Actual path with indirect routing: London → New York (home) → Tokyo. Much longer and less efficient.

## Optimization: Direct Routing with Route Optimization

To eliminate triangle routing, **route optimization** allows $C$ to learn $M$'s current location (care-of address) and send packets directly.

### Binding Update Mechanism

When $M$ moves and registers with $HA$, it also informs $C$ of its new care-of address:

```
M registers with HA:
  HA learns: (A_M, CoA_current)
  
M sends binding update to C:
  "Send future packets to me at CoA_current"
  
C updates its binding cache:
  binding[A_M] = CoA_current
  
C sends future packets to CoA_current directly
```

### Direct Forwarding with Tunneling Back to Home

However, direct forwarding to CoA has a security problem: the source address in $C$'s packets is still $C$'s actual address, but the destination changes from $A_M$ (home address) to CoA (current address). This breaks the original address semantics.

Solution: $M$ maintains the home address in the packet header via a special IP header extension:

- **Destination Address** in standard IP header: CoA (routing destination).
- **Home Address** in IP extension header: $A_M$ (identifies the host identity).

When $C$ receives a reply from $M$, it sees the home address in the extension header, which allows it to verify that the reply is from the correct correspondent.

## Formal Model for Mobile Host Routing

Let:
- $A_M$ = home address of mobile host $M$.
- $CoA_M$ = care-of address (current location identifier) of $M$.
- $L_H$ = network location of home agent.
- $L_C$ = network location of correspondent.

**Indirect routing state**:
```
At Home Agent HA:
  binding_table[A_M] = (CoA_M, registration_time, lifetime)

At Foreign Agent FA (at CoA):
  local_hosts[CoA_M] = M
```

**Routing decision**:
- If packet dest = $A_M$ and sender is $C$ at location $L_C$:
  - If $L_C$ = home network: deliver normally.
  - Else: intercept at $HA$, tunnel to CoA_M.

## Handover and Binding Updates

### Handover Delay

When $M$ moves from one foreign network to another, a new registration is required:

1. $M$ detects loss of link with previous $FA$.
2. $M$ discovers the new $FA$ at the new location.
3. $M$ sends a new registration to $HA$ with updated $CoA$.
4. During this process, packets destined for $M$ may be lost or delayed.

**Handover latency**: Time from link loss to completion of registration at new $FA$. Typical values range from 100 ms to several seconds.

### Binding Consistency Problem

When $M$ changes location and updates its binding with $HA$, existing correspondents may still have the old binding cached. Packets may be sent to the old $CoA$, which is no longer valid:

**Solution**: 
- $M$ sends binding updates to all active correspondents (those with cached bindings).
- Old $CoA$ (previous foreign agent) can serve as a **forwarding agent**, re-tunneling packets to the new $CoA$ for a transitional period.

## Comparison with Alternative Approaches

### Host-Based Mobility Management vs. Network-Based

**Host-Based** (as discussed above):
- Host actively participates in mobility management.
- Host sends registration and binding update messages.
- Advantages: Works transparently to network infrastructure; can optimize based on application needs.
- Disadvantages: Mobile host must have sufficient battery and processing power.

**Network-Based** (e.g., Proxy Mobile IPv6):
- Network elements (routers, gateways) manage mobility on behalf of hosts.
- Hosts are not aware of handover.
- Advantages: Simpler for hosts; useful for lightweight devices.
- Disadvantages: More complex network infrastructure.

## Related Concepts

- [[Mobile_IP_Protocol]]: Detailed protocol specification for IPv4 mobile networking.
- [[Network_Mobility_NEMO]]: Mobility for entire subnets.
- [[Tunneling_and_VPN]]: IP tunneling mechanism used by mobile routing.
- [[IP_Addressing_Review]]: IP addressing and address resolution.

---

**Next:** [[Mobile_IP_Protocol]]
