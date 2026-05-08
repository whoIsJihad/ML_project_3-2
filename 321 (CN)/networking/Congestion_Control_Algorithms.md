# Congestion Control Algorithms

## Overview

Congestion control algorithms are mechanisms used by routers and end-systems to detect congestion and respond by adjusting traffic rates. Unlike [[Congestion_Prevention_Policies|prevention policies]], these algorithms react to congestion signals (loss or explicit notification).

## Algorithm Classes

Congestion control algorithms are classified by their congestion signal source:

### Loss-Based Algorithms

Interpret packet loss as a congestion signal. Used by TCP (Tahoe, Reno, NewReno, etc.).

### Delay-Based Algorithms

Use RTT (round-trip time) increase as an early congestion signal (before loss). Example: TCP Vegas.

### Explicit Feedback Algorithms

Use explicit router feedback (e.g., Explicit Congestion Notification) instead of inferring from loss.

## Router-Side Algorithm: Random Early Detection (RED)

### Motivation

Traditional routers use **tail drop**: accept packets until the buffer is full, then discard all arrivals. This causes:
1. **Bursty losses**: When the buffer fills, many packets are lost in a short time.
2. **Synchronized retransmissions**: Multiple TCP connections lose packets simultaneously and retransmit together, causing a burst that re-congests the network.
3. **Low link utilization**: The queue drains, then fills again (sawtooth pattern).

RED (Random Early Detection) addresses these by randomly discarding packets *before* the buffer is full.

### Algorithm

RED maintains:
- Minimum threshold: $T_{\min}$ (start discarding at this queue length).
- Maximum threshold: $T_{\max}$ (discard all packets if exceeded).
- Maximum probability: $P_{\max}$ (maximum discard probability).

**Drop Probability Calculation**:

```
Calculate moving average queue length: avg_q(t)

if (avg_q < T_min):
  drop_probability = 0  // no dropping

else if (T_min ≤ avg_q ≤ T_max):
  drop_probability = P_max × (avg_q - T_min) / (T_max - T_min)
  // linear increase from 0 to P_max

else:  // avg_q > T_max
  drop_probability = 1.0  // drop all packets
end if

For each arriving packet:
  if (random() < drop_probability):
    discard packet
  else:
    accept packet into buffer
  end if
```

### Behavior

```
Drop Probability

P_max |         ╱────
      |        ╱
      |       ╱
    0 |______╱
      └──────────────── Queue Length
         T_min  T_max
```

**Effect on Congestion**:
- Packets are dropped before the buffer is full, providing early congestion feedback.
- Dropping is probabilistic, reducing synchronized losses.
- TCP senders receive distributed loss signals, desynchronizing retransmissions.
- Result: Smoother throughput, better link utilization, reduced RTT.

### Parameters

**Moving Average Queue Length**:
$$\text{avg_q}(t) = (1 - w) \cdot \text{avg_q}(t-1) + w \cdot q(t)$$

where $w$ is a weight (typically 0.002 to 0.01) and $q(t)$ is the instantaneous queue length.

The moving average smooths out temporary fluctuations in queue length.

### Variants

**Weighted RED (WRED)**: Different thresholds and probabilities for different traffic classes (based on DiffServ markings). High-priority traffic has higher thresholds or lower drop probabilities.

## Router-Side Algorithm: Explicit Congestion Notification (ECN)

### Motivation

RED and other loss-based mechanisms rely on packet loss to signal congestion. However:
- Loss wastes network bandwidth (the packet carrying information is not delivered).
- Applications must retransmit, increasing load.

ECN provides explicit router feedback without requiring loss.

### ECN Mechanism

**IP Header Markings**:
- Two bits in the IP header are reserved for ECN (ECN-Capable Transport, ECN-CE flag).
- Bit 0 (ECT): ECN-Capable Transport (0 = not capable, 1 = capable).
- Bit 1 (CE): Congestion Experienced (0 = no congestion, 1 = congestion).

**Router Behavior**:
1. If queue length exceeds threshold (similar to RED):
   - Check if the arriving packet has ECT = 1 (sender supports ECN).
   - If yes: Set CE = 1 (mark the packet as congestion experienced).
   - If no: Drop the packet (fall back to loss-based signal).
2. Forward the marked packet.

**Sender Behavior**:
1. Receiver receives packet with CE = 1.
2. Receiver acknowledges the packet with the CE flag echoed back in the TCP ACK.
3. Sender receives the ACK with CE flag and reduces its congestion window (CWND), similar to a loss-based reduction.

**Advantage over Loss**:
- Congestion is signaled without packet loss.
- Bandwidth is preserved; retransmission overhead is avoided.
- Senders can react to congestion earlier (upon receipt of ACK) rather than waiting for timeout.

### ECN-Capable Senders and Receivers

- Not all TCP implementations support ECN.
- Senders set ECT = 1 only if they support ECN.
- Routers mark only ECT = 1 packets; others are dropped (if congestion persists).
- Receivers echo the CE flag; if receivers don't support ECN, the feedback is lost, and senders must fall back to loss-based detection.

## End-System Algorithm: TCP Congestion Control

### TCP Tahoe (Simplified)

**Congestion Window (CWND)**: The amount of unacknowledged data (in segments) a sender can have in flight.

**Slow Start**:
```
Initial CWND = 1 segment

foreach ACK received:
  CWND += 1  // exponential growth: CWND doubles every RTT
```

Slow start grows CWND exponentially until a loss is detected or CWND reaches the slow-start threshold (SSTHRESH).

**Congestion Avoidance** (after Slow Start or Threshold):
```
foreach ACK received:
  CWND += 1 / CWND  // linear growth: CWND increases by 1 every RTT
```

Congestion avoidance increases CWND linearly.

**Fast Retransmit**: 
- Upon receiving 3 duplicate ACKs (indicating a packet loss), immediately retransmit the lost segment without waiting for timeout.

**Fast Recovery**:
- After fast retransmit, set CWND = SSTHRESH / 2 and enter congestion avoidance (TCP Reno).

**Upon Timeout**:
```
SSTHRESH = CWND / 2
CWND = 1
Enter slow start
```

### TCP Reno (Improved)

TCP Reno improves on Tahoe with fast recovery:

```
upon Fast Retransmit (3 duplicate ACKs):
  SSTHRESH = CWND / 2
  CWND = SSTHRESH + 3  // +3 for the 3 duplicate ACKs
  Enter Fast Recovery (modified congestion avoidance)

upon Timeout:
  SSTHRESH = CWND / 2
  CWND = 1
  Enter Slow Start
```

### CWND Behavior Over Time

```
CWND (segments)

  ╱╲        ╱╲     ╱─────
 ╱  ╲      ╱  ╲   ╱
╱    ╲────╱    ╲_╱
└──────────────────── Time
Slow  Congestion     Fast
Start Avoidance      Retransmit
```

## Hop-by-Hop Congestion Control: Choke Packets

In some networks, a congested router sends **choke packets** back to the source to signal congestion directly.

**Mechanism**:
```
Router detects congestion:
  send CHOKE_PACKET to source (with router address, destination address)
```

**Sender Behavior**:
Upon receiving a choke packet:
```
for each connection to the destination mentioned in choke packet:
  reduce CWND by 0.5  // or other reduction factor
```

**Advantage**: Direct feedback is faster than waiting for packet loss.

**Disadvantage**: Choke packets themselves consume bandwidth; if too many are sent, they can increase congestion.

## Comparison of Congestion Control Algorithms

| Algorithm | Signal | Detection | Speed | Fairness | Deployment |
|---|---|---|---|---|---|
| **RED** | Loss (implicit) | Late (buffer full) | Medium | Poor | Common |
| **ECN** | Explicit mark | Early (before loss) | Fast | Good | Growing |
| **TCP Tahoe** | Loss | Very late (timeout) | Slow | Poor | Legacy |
| **TCP Reno** | Loss | Late (3 DupACKs) | Medium | Medium | Standard |
| **Choke Packets** | Explicit feedback | Early | Very Fast | Good | Rare |

## Stability and Fairness

### Stability

A congestion control algorithm is stable if it converges to a steady state (CWND reaches an equilibrium value) and doesn't oscillate excessively.

**Convergence Criterion**:
$$\lim_{t \to \infty} \text{CWND}(t) = \text{stable value}$$

TCP Reno is stable; CWND oscillates around a steady-state value as the congestion window increases in congestion avoidance and decreases upon loss.

### Fairness

Multiple TCP connections should share bandwidth fairly. **Max-Min Fairness** is a desirable property:

$$\text{Allocate bandwidth to maximize minimum allocation to any flow.}$$

TCP Reno achieves approximate max-min fairness because:
- Flows experiencing loss reduce their rate.
- Flows not experiencing loss increase their rate.
- Over time, convergence to fair allocation occurs.

However, fairness is not perfect; flows with lower RTTs increase CWND faster (more ACKs per second).

## Relationship to QoS

Congestion control algorithms alone cannot provide differentiated QoS because:
1. All TCP flows respond similarly to loss; no priority distinction.
2. Flows adapt based on their own experience; no global bandwidth allocation policy.

For QoS, congestion control must be combined with:
- [[Quality_of_Service_QoS]]: Resource reservation and traffic shaping.
- [[Congestion_Prevention_Policies]]: Admission control and queue management.

## Related Concepts

- [[Congestion_Control_Fundamentals]]: Congestion dynamics and motivation.
- [[Congestion_Prevention_Policies]]: Prevention mechanisms complementing control.
- [[Quality_of_Service_QoS]]: QoS framework.
- [[Leaky_Bucket_Algorithm]] and [[Token_Bucket_Algorithm]]: Traffic shaping for control.

---

**Next:** [[Quality_of_Service_QoS]]
