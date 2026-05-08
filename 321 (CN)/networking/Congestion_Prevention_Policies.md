# Congestion Prevention Policies

## Overview

Congestion prevention policies are mechanisms implemented at different network layers to prevent congestion from occurring or to limit its severity once it begins. Unlike reactive congestion control (which responds to packet loss), prevention policies proactively manage traffic and resources.

Refer to [[Congestion_Control_Fundamentals]] for the foundational concepts.

## Layer-Based Classification

Prevention policies operate at multiple layers:

### Application Layer

**Traffic Regulation by the Application**:
- Applications (or the transport layer on their behalf) limit the rate at which data is sent.
- Example: Streaming applications use adaptive bitrate to match available bandwidth.

**Reservation Protocols**:
- Applications signal their resource needs to the network (e.g., RSVP: Resource Reservation Protocol).
- Network resources are reserved in advance.

### Transport Layer

**Rate Control**:
- TCP congestion window adjustment (CWND) limits the amount of unacknowledged data in flight.
- Prevents applications from overwhelming the network.

**Explicit Congestion Notification (ECN)**:
- Instead of inferring congestion from loss, routers mark packets to signal congestion.
- Senders reduce rate upon receiving marked packets (before loss occurs).

### Network Layer (IP / Routing)

**Traffic Engineering**:
- Traffic is distributed across multiple paths to avoid concentrating load on bottleneck links.
- Example: MPLS (Multiprotocol Label Switching) allows explicit path selection.

**Per-Hop Behavior (PHB) and Differentiated Services (DiffServ)**:
- Different traffic classes receive different treatment (priority, bandwidth allocation).
- Prevents non-critical traffic from consuming resources needed for critical traffic.

### Link Layer

**Queue Management**:
- Routers manage their output queues to prevent buffer overflow.
- Strategies: Tail Drop, Random Early Detection (RED), Weighted Random Early Detection (WRED).

**Link Aggregation**:
- Multiple physical links are bonded to increase capacity.
- Reduces the likelihood of any single link becoming a bottleneck.

## Specific Prevention Mechanisms

### 1. Admission Control

An admission control policy decides whether to accept new flows or additional traffic based on current network state.

**Decision Rule**:
```
if (available_bandwidth ≥ requested_bandwidth):
  accept_flow()
else:
  reject_flow()
end if
```

**Benefit**: Prevents oversubscription; once a flow is admitted, its bandwidth is guaranteed.

**Drawback**: May reject flows that could be accommodated; reduces network utilization.

**Implementation**: 
- Reservation protocols (RSVP) implement admission control.
- Used in QoS-enabled networks.

### 2. Resource Reservation (RSVP)

The Resource Reservation Protocol allows applications to request specific bandwidth and delay guarantees from the network.

**Process**:
1. **Path Message**: Sender explores the path to the receiver, learning about available resources at each hop.
2. **Resv Message**: Receiver requests reservation along the path.
3. **Resource Allocation**: Each router on the path allocates resources (bandwidth, buffer) for the flow.

**Effect on Congestion**:
- Once resources are reserved, competing flows cannot claim those resources.
- Prevents oversubscription on reserved paths.

### 3. Traffic Shaping

Traffic shaping regulates the rate and burstiness of traffic entering a network.

**Mechanisms**:
- **Leaky Bucket** (see [[Leaky_Bucket_Algorithm]]): Enforces a constant output rate; excess traffic is queued or discarded.
- **Token Bucket** (see [[Token_Bucket_Algorithm]]): Allows short bursts while maintaining average rate.

**Effect**: Reduces sudden spikes that could cause congestion; smooths traffic arrival pattern.

### 4. Load Balancing and Traffic Engineering

**Equal-Cost Multi-Path (ECMP) Routing**:
- If multiple paths of equal cost exist to a destination, traffic is distributed across them.
- Reduces load concentration on a single path.

**Example**:
```
Source ──→ Router1 ──→ Dest
    ╲          ╱
     └─Router2─┘
     
Without load balancing: All traffic via Router1.
With ECMP: Traffic split between Router1 and Router2.
```

**Explicit Path Selection (MPLS)**:
- Instead of hop-by-hop forwarding, a source or ingress router explicitly chooses a path.
- Paths can be selected to balance load across the network.

### 5. Differentiated Services (DiffServ)

DiffServ classifies traffic into service classes, each receiving different treatment:

**Traffic Classes**:
- **Expedited Forwarding (EF)**: Low-latency, low-loss service for critical applications (VoIP).
- **Assured Forwarding (AF)**: Tiered service; multiple drop precedences.
- **Best Effort (BE)**: Standard service, no guarantees.

**Implementation**:
- Each packet is marked with a DiffServ Codepoint (DSCP) in the IP header.
- Routers treat packets according to their DSCP marking.
- High-priority traffic (EF) is transmitted first; lower-priority traffic is dropped first during congestion.

**Effect**:
- Critical traffic is isolated from congestion caused by non-critical traffic.
- Doesn't prevent overall congestion; instead, protects priority traffic.

### 6. Queue Management Policies

**Tail Drop**:
- Accept packets until buffer is full; discard all arriving packets when full.
- Simple but crude; packet loss is bursty (many packets lost at once).

**Random Early Detection (RED)** (see [[Congestion_Control_Algorithms]]):
- Start discarding or marking packets randomly when queue exceeds a threshold (before full).
- Smoother packet loss; reduces retransmission bursts.

**Drop Precedence**:
- Discard low-priority packets first; protect high-priority traffic.
- Used with DiffServ or Weighted RED (WRED).

## Policy Hierarchy and Integration

Effective congestion prevention requires coordinated policies across layers:

```
Application Layer: Adaptive bitrate, RSVP signaling
    ↓
Transport Layer: TCP window control, ECN-aware senders
    ↓
Network Layer: Traffic engineering, DSCP marking, admission control
    ↓
Link Layer: RED queue management, shaped output
    ↓
Physical Layer: Link aggregation, bandwidth provisioning
```

## Prevention vs. Control Trade-offs

| Aspect | Prevention | Control |
|---|---|---|
| **Activation** | Proactive (before congestion) | Reactive (after congestion) |
| **Loss** | Minimal (ideally zero) | Unavoidable |
| **Complexity** | Higher (requires planning) | Lower (simple to implement) |
| **Flexibility** | Lower (reserved resources) | Higher (adapts to changes) |
| **Utilization** | Lower (over-provisioned) | Higher (reactive sharing) |

## Practical Deployment

**Enterprise Networks**:
- Use RSVP and DiffServ for QoS-critical applications.
- Implement traffic engineering to avoid congestion.

**Internet Service Providers (ISPs)**:
- Use capacity provisioning (over-provisioning) to avoid congestion.
- DiffServ and RED for traffic management.
- MPLS for traffic engineering.

**Cloud Data Centers**:
- Admission control to prevent overload.
- Traffic shaping and scheduling to isolate tenants.
- Load balancing across servers.

## Limitations of Prevention Policies

1. **Incomplete Information**: Networks cannot perfectly predict future traffic; prevention relies on estimates.
2. **Dynamic Nature**: Network conditions change constantly; static reservations may not match actual needs.
3. **Over-Provisioning Costs**: Prevention often requires over-provisioning, which is expensive.
4. **Interoperability**: Different networks may use different policies; coordination is complex.

For these reasons, prevention is complemented by control mechanisms; see [[Congestion_Control_Algorithms]].

## Related Concepts

- [[Congestion_Control_Fundamentals]]: Fundamentals of congestion.
- [[Congestion_Control_Algorithms]]: Reactive control mechanisms.
- [[Quality_of_Service_QoS]]: QoS framework incorporating both prevention and control.
- [[Leaky_Bucket_Algorithm]] and [[Token_Bucket_Algorithm]]: Traffic shaping mechanisms.

---

**Next:** [[Congestion_Control_Algorithms]]
