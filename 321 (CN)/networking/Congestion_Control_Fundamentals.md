# Congestion Control Fundamentals

## Definition

Network congestion occurs when the aggregate demand for network resources (bandwidth, buffer space, processing capacity) exceeds the available supply over a region of the network or at a particular time. Formally, let:

- $\lambda(t)$ = aggregate arrival rate of packets at time $t$ (packets/second).
- $\mu(t)$ = aggregate service capacity at time $t$ (packets/second).

**Congestion** occurs in a link or switch when $\lambda(t) > \mu(t)$ for a sustained period.

## Why Congestion Matters

### Performance Degradation

When a network becomes congested:
1. **Packet losses**: Buffers overflow; packets are discarded.
2. **Increased latency**: Packets wait longer in queues.
3. **Throughput reduction**: The effective throughput (successfully delivered packets per second) decreases despite input load.

Formally, let $P_{\text{drop}}(t)$ be the fraction of packets dropped due to buffer overflow. Then the effective throughput is:

$$T_{\text{eff}}(t) = \lambda(t) \cdot (1 - P_{\text{drop}}(t))$$

As congestion increases, $P_{\text{drop}}(t)$ increases non-linearly, causing $T_{\text{eff}}(t)$ to eventually **decrease** even as input load increases. This is counterintuitive but fundamental to queue dynamics.

### Congestion Collapse

In extreme cases, the network can suffer **congestion collapse**:
- The effective throughput approaches zero despite sustained offered load.
- This occurred historically in the early Internet (1986-1987) when network capacity grew but throughput plummeted.
- The cause: Retransmitted packets (from undelivered originals) filled the network, consuming bandwidth without forward progress.

## Sources of Congestion

### 1. Imbalanced Link Capacities

The network has heterogeneous link speeds. In a chain of links:

```
Host A ─── Link1 ─── Router ─── Link2 ─── Host B
          100 Mbps               10 Mbps
```

If traffic flows from A to B, Link2 (the bottleneck) becomes congested while Link1 is underutilized.

### 2. Many-to-One Traffic Patterns

Multiple sources send traffic to a single destination, converging at a switch or router:

```
Source1 ──\
           └─→ Router ─→ Dest
Source2 ──/
```

The outgoing link from the router becomes the bottleneck.

### 3. Bursty Traffic

Even if the average load is below capacity, traffic can be bursty (concentrated in short time intervals):

$$\text{Peak Rate} > \text{Avg Rate}$$

During peak periods, congestion occurs even though long-term average load is acceptable.

### 4. Unexpected Load Increases

Sudden events can cause load spikes:
- A popular web server becomes trending; traffic surges.
- A network link fails, forcing traffic onto alternate paths.
- Scheduled maintenance reduces network capacity.

## Congestion Dynamics: Queuing Model

### Single Router Queue Model

Consider a single router (switch) with incoming link rate $\lambda$ and outgoing service rate $\mu$:

```
   Incoming packets at rate λ
            ↓
     ┌──────────────┐
     │    Queue     │
     │   (Buffer)   │
     └──────────────┘
            ↓
   Outgoing packets at rate μ (service)
```

Let $q(t)$ be the queue length (number of packets waiting).

**Dynamics**:
$$\frac{dq(t)}{dt} = \lambda - \mu$$

where $\lambda > 0$ is the arrival rate and $\mu$ is the service (transmission) rate, assumed constant.

**Solution**:
$$q(t) = q(0) + (\lambda - \mu) t$$

If $\lambda > \mu$:
- Queue grows linearly with time: $q(t) \approx (\lambda - \mu) t$.
- Eventually, queue exceeds buffer capacity $B$; packets are dropped.
- Time to overflow: $t_{\text{overflow}} = \frac{B}{(\lambda - \mu)}$.

### Queueing Delay

The **queueing delay** (time a packet spends in the queue) for a packet entering the queue when the queue length is $q$ is:

$$\text{Delay} = \frac{q}{S}$$

where $S$ is the service rate in packets per time unit, and $q$ is the number of packets ahead.

For an $M/M/1$ queue (Poisson arrivals, exponential service):
$$E[\text{Delay}] = \frac{1}{\mu - \lambda}$$

As $\lambda \to \mu$ (arrival rate approaches capacity), the expected delay approaches infinity. This is a fundamental result in queueing theory.

### Little's Law

A fundamental relationship in queueing theory:

$$\overline{q} = \lambda \cdot E[\text{Delay}]$$

where $\overline{q}$ is the average queue length. This states that the average queue length equals the arrival rate times the average delay. High delays imply high queue lengths, confirming the intuition that congestion increases delay.

## Impacts of Congestion

### 1. Packet Loss

When queue buffer is full (capacity $B$), arriving packets are dropped:

$$P_{\text{loss}} = \frac{\lambda - \mu}{λ} \quad \text{(for } \lambda > \mu \text{)}$$

In practice, losses depend on buffer size, arrival burstiness, and dropping policy.

**Consequence**: Applications using TCP must retransmit lost packets, increasing network load further (retransmitted packets don't represent new data).

### 2. Increased Latency

Both queueing delay and retransmission delays increase:

$$\text{RTT}_{\text{congestion}} = \text{RTT}_{\text{uncongested}} + \text{Queueing Delay} + \text{Retransmission Delay}$$

For real-time applications (VoIP, video), increased latency degrades user experience and may exceed maximum tolerable latency ($\sim$ 150 ms).

### 3. Fairness Issues

Without congestion control, some flows may dominate:
- Flows with aggressive senders (frequent packet transmission) claim more bandwidth.
- Well-behaved (conservative) flows reduce their rate, losing bandwidth to aggressive flows.
- Result: Unfair allocation among competing flows.

### 4. Reduced Throughput

In extreme congestion, effective throughput decreases despite increased load:

```
Effective Throughput vs. Offered Load

T_eff
  |     ╱─────  (uncongested region, slope = 1)
  |    ╱
  |   ╱
  |__╱────────── (congestion collapse region, slope ≤ 0)
  └──────────────── Offered Load
  
   (congestion point)
```

This occurs because retransmissions and losses consume bandwidth without delivering data.

## Effects on Protocol Layers

Congestion affects different protocol layers differently:

### Link Layer

- Queue overflow causes packet drops.
- Link-layer retransmissions increase.
- Link utilization may be high, but effective throughput is low.

### Network Layer (IP)

- Routers must decide which packets to drop (tail drop, random drop, etc.).
- Routing algorithms may not account for congestion (they use static metrics like hop count).
- Congestion information is not propagated backward (in traditional IP).

### Transport Layer (TCP)

- TCP interprets packet loss as congestion signal.
- TCP reduces send rate (congestion window) upon loss.
- Retransmissions increase network load.

### Application Layer

- High latency may cause application timeouts.
- Interactive applications become unresponsive.
- Streaming applications may reduce quality (adaptive bitrate).

## Congestion Control vs. Congestion Avoidance

**Congestion Control**: Reacting to congestion that has already occurred (loss-based).
- Example: TCP Tahoe/Reno, which uses packet loss as congestion signal.

**Congestion Avoidance**: Predicting and preventing congestion before it occurs (delay-based or ECN-based).
- Example: TCP Vegas, which uses latency increase as early congestion signal.
- Example: Explicit Congestion Notification (ECN), which uses router flags instead of loss.

Both approaches are necessary for efficient network operation; see [[Congestion_Control_Algorithms]] for detailed mechanisms.

## Relationship to QoS

Congestion control alone is insufficient for QoS because:
1. Not all applications are TCP-based (UDP, QUIC, etc.).
2. Different applications have different requirements (latency vs. throughput).
3. Fairness among flows must be explicitly managed.

[[Quality_of_Service_QoS]] extends congestion control with traffic shaping, prioritization, and resource reservation.

## Related Concepts

- [[Congestion_Prevention_Policies]]: Strategies to prevent congestion across network layers.
- [[Congestion_Control_Algorithms]]: Detailed algorithms (RED, ECN, etc.).
- [[Quality_of_Service_QoS]]: QoS mechanisms and requirements.
- [[Leaky_Bucket_Algorithm]]: Traffic shaping for congestion prevention.
- [[Token_Bucket_Algorithm]]: Enhanced traffic shaping with burst allowance.

---

**Next:** [[Congestion_Prevention_Policies]]
