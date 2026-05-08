# Quality of Service (QoS)

## Definition

Quality of Service (QoS) is a set of techniques and mechanisms that guarantee specific network performance characteristics for data flows. Formally, QoS defines and enforces service level guarantees for flows with heterogeneous requirements.

Let $F$ be a network flow (a set of packets from a source to a destination with a common protocol port or identifier). QoS guarantees for $F$ include:

- **Bandwidth**: Minimum throughput $B_{\min}$ guaranteed for $F$.
- **Latency**: Maximum delay $D_{\max}$ for packets in $F$.
- **Jitter**: Maximum variation in delay $J_{\max}$.
- **Loss**: Maximum packet loss rate $L_{\max}$.
- **Priority**: Relative importance level compared to other flows.

## Motivation for QoS

Different applications have different performance requirements:

### Real-Time Applications

**VoIP (Voice over IP)**:
- Bandwidth: 64 kbps (compressed codec) to 128 kbps.
- Latency: Maximum 150 ms one-way (ITU-T G.131 recommendation).
- Jitter: Should be minimized; buffer is used to absorb jitter.
- Loss: Maximum 1% (noticeable quality degradation at > 3%).

**Video Conferencing**:
- Bandwidth: 500 kbps to 25 Mbps (depending on resolution and codec).
- Latency: < 200 ms for interactive communication.
- Jitter: Minimized through buffering.
- Loss: < 2% for acceptable quality.

### Elastic Applications

**Email**:
- Bandwidth: Flexible; as much as available.
- Latency: No strict requirement; hours are acceptable.
- Loss: Zero loss required (delivered reliably).

**Web Browsing**:
- Bandwidth: Flexible; but faster is better.
- Latency: < 1 second for interactive feel.
- Loss: Zero (TCP retransmits lost packets).

**File Transfer**:
- Bandwidth: Flexible; as much as available.
- Latency: Flexible.
- Loss: Zero required.

## QoS Framework

A complete QoS system includes:

### 1. QoS Signaling

Applications or network managers declare their QoS requirements to the network.

**Reservation Protocol (RSVP)**:
- Path message: Sender probes the path to receiver.
- Resv message: Receiver requests resources (bandwidth, delay) along the path.
- Each router reserves resources for the flow.

**Session Description Protocol (SDP)**:
- Applications describe their QoS needs in session descriptions.
- Used in VoIP and video applications to negotiate QoS parameters.

### 2. Admission Control

The network decides whether to accept a new flow based on:
- Available bandwidth.
- Current load.
- Priority of the new flow vs. existing flows.

```
new_bandwidth_available = total_capacity - allocated_to_existing_flows

if (new_bandwidth_available >= requested_bandwidth):
  admit_flow()
else:
  reject_flow()  // avoid oversubscription
end if
```

### 3. Resource Allocation

Once admitted, resources are allocated to the flow at each router.

**Bandwidth Allocation**:
- Reserve a portion of link bandwidth for the flow.
- Remaining bandwidth is shared among best-effort flows.

**Buffer Allocation**:
- Reserve buffer space for the flow's packets.
- Prevents the flow from triggering packet loss for other flows.

### 4. Traffic Shaping and Policing

**Shaping** (at the source or ingress):
- Regulate traffic to match the reserved profile.
- Mechanisms: [[Leaky_Bucket_Algorithm]], [[Token_Bucket_Algorithm]].

**Policing** (at each hop):
- Monitor traffic; discard or mark non-conformant packets.
- Protects the network from cheating sources.

### 5. Scheduling

At each router, a scheduling algorithm determines the order in which packets from different flows are transmitted.

**FIFO (First-In-First-Out)**:
- Simple but provides no QoS differentiation.
- All flows treated equally.

**Priority Queueing**:
- Separate queues for different priority classes.
- High-priority queue is serviced first; low-priority packets wait.
- Risk: Starvation of low-priority flows if high-priority traffic is continuous.

**Weighted Fair Queueing (WFQ)**:
- Each flow (or class) is allocated a weight representing its priority or bandwidth allocation.
- Packets are served in round-robin fashion among flows, with each flow receiving service proportional to its weight.

**Formula**: If flow $i$ has weight $w_i$ and there are $n$ active flows, flow $i$ receives a fraction:
$$\text{Service Fraction} = \frac{w_i}{\sum_{j=1}^{n} w_j}$$

### 6. Queue Management

As discussed in [[Congestion_Control_Algorithms]], RED and other queue management algorithms prevent congestion.

**QoS-aware Queue Management**:
- Different drop probabilities for different flow classes.
- High-priority flows have lower drop probability.

## QoS Models

### IntServ (Integrated Services)

**Approach**: Per-flow resource reservation and guarantee.

**Mechanism**:
- Applications signal QoS requirements via RSVP.
- Each router reserves resources for each flow.
- Routers maintain state for all flows (per-flow state explosion in large networks).

**Guarantee**: Hard guarantees (strict bounds on latency and loss).

**Scalability**: Poor; does not scale to millions of flows.

**Deployment**: Limited; used in enterprise networks with manageable flow counts.

### DiffServ (Differentiated Services)

**Approach**: Per-class resource differentiation without per-flow reservation.

**Mechanism**:
- Traffic is classified into classes (e.g., VoIP, video, best-effort) based on DSCP markings.
- Each class receives predefined treatment (bandwidth allocation, priority).
- No explicit resource reservation; over-provisioning is assumed.

**Guarantee**: Soft guarantees (statistical bounds); best-effort + priority ordering.

**Scalability**: Excellent; scales to any number of flows (no per-flow state at core routers).

**Deployment**: Widespread; used by ISPs and large networks.

### Service Classes in DiffServ

| Class | DSCP | Characteristics |
|---|---|---|
| **EF (Expedited Forwarding)** | 46 | Low-latency, low-loss, low-jitter (VoIP) |
| **AF1x** | 10, 12, 14 | High-priority assured forwarding (video) |
| **AF2x** | 18, 20, 22 | Medium-priority assured forwarding |
| **AF3x** | 26, 28, 30 | Low-priority assured forwarding |
| **BE (Best Effort)** | 0 | Standard Internet service |

The 'x' in AF represents drop precedence (1=low drop, 3=high drop).

## Metrics for QoS

### Throughput (Bandwidth)

$$\text{Throughput} = \frac{\text{bytes delivered}}{\text{time}} \quad \text{(bits/second)}$$

Measured or guaranteed throughput for a flow.

### Delay (Latency)

$$\text{Delay} = \text{time from source to destination}$$

Components:
- **Propagation delay**: Physical transmission time (fixed, determined by distance).
- **Queueing delay**: Time spent waiting in buffers (variable).
- **Processing delay**: Time for routing/switching decisions (typically negligible).

Typical values:
- Local network: 1-10 ms.
- Long-distance (transcontinental): 100-200 ms.
- Real-time applications: < 200-300 ms acceptable.

### Jitter

$$\text{Jitter} = \text{std}_{\text{dev}}(\text{Delay})$$

Variation in delay between packets. High jitter can cause audio/video quality degradation. Buffering at the receiver absorbs jitter.

### Packet Loss Rate

$$\text{PLR} = \frac{\text{packets dropped}}{\text{packets sent}}$$

Typical requirements:
- VoIP: < 1-3%.
- Video streaming: < 2-5%.
- Best-effort: Tolerates higher loss (TCP retransmits).

### Availability

$$\text{Availability} = \frac{\text{uptime}}{\text{uptime} + \text{downtime}}$$

Percentage of time the service is available. Enterprise SLAs often guarantee 99.9% availability (4.3 hours downtime per year).

## Traffic Conditioner

A **traffic conditioner** (shaper or policer) at the network ingress ensures that traffic conforms to the reserved profile:

```
┌─────────────────────────────────────────┐
│        Traffic Conditioner              │
│   (Leaky or Token Bucket)               │
├─────────────────────────────────────────┤
│                                         │
│  Incoming Traffic (possibly bursty)     │
│           ↓                             │
│    [Check Token/Leak]                   │
│    Conformant? ─→ Forward (marked)      │
│    Non-conformant? ─→ Mark or Drop      │
│                                         │
└─────────────────────────────────────────┘
           ↓
     Network Core
```

See [[Leaky_Bucket_Algorithm]] and [[Token_Bucket_Algorithm]] for detailed mechanisms.

## End-to-End QoS Architecture

```
Application Signaling (SDP, RSVP)
         ↓
Ingress Router: Admission Control, Traffic Shaping
         ↓
Core Network: Routing, Scheduling (WFQ/Priority), Queue Management (RED)
         ↓
Egress Router: Delivery
         ↓
Receiver: Buffer/Jitter Compensation
```

At each step, QoS parameters (bandwidth, delay, loss) are monitored and maintained.

## Related Concepts

- [[Congestion_Control_Fundamentals]]: Congestion occurs when QoS cannot be maintained.
- [[Congestion_Prevention_Policies]]: Prevention ensures QoS requirements are met.
- [[Congestion_Control_Algorithms]]: Control mechanisms work in conjunction with QoS.
- [[Leaky_Bucket_Algorithm]]: Traffic shaping mechanism for QoS.
- [[Token_Bucket_Algorithm]]: Enhanced traffic shaping allowing bursts.

---

**Next:** [[Leaky_Bucket_Algorithm]]
