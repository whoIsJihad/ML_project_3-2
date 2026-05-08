# Congestion Control

## Purpose and Distinction

**Congestion** occurs when the total data arrival rate at routers exceeds link capacity, causing:
- Queue buildup
- Packet drops
- Timeouts and retransmissions
- Wasted bandwidth

**Congestion Control** (sender-side) vs. [[Flow_Control_Mechanisms|Flow Control]] (receiver-side):

| Aspect | Congestion Control | Flow Control |
|---|---|---|
| **Concern** | Network capacity | Receiver buffer |
| **Signals** | Packet loss, delay | Window advertisement |
| **Mechanism** | Sender reduces transmission rate | Sender respects advertised window |
| **Why** | Prevent network collapse | Prevent receiver overflow |
| **Consequence** | Network stability | Receiver stability |

Both must be satisfied:
$$\text{send\_rate} = \min(\text{congestion\_controlled\_rate}, \text{flow\_controlled\_rate})$$

## Problem: Congestion Collapse

### Scenario

```
10 Mbps link
4 competing flows, each generating 5 Mbps
Total demand: 20 Mbps > 10 Mbps link capacity

Without congestion control:
  Each flow continues sending at 5 Mbps
  Router queue builds infinitely
  Packets dropped after queues fill
  Senders timeout; retransmit
  More retransmitted packets → more drops
  → Congestion collapse: Useful throughput → 0
```

**Historical reality**: 1986 Internet collapse (Robert Morris's TCP bug caused this).

## [[TCP_Tahoe]]: First Congestion Control Algorithm

### Concepts

**Congestion Window (cwnd)**:
- Sender maintains estimate of network capacity
- Limits data in flight: bytes_in_flight ≤ cwnd

**Slow Start Phase**:
- Exponential growth of cwnd
- Goal: Rapidly probe network capacity

**Congestion Avoidance Phase**:
- Linear growth of cwnd
- Goal: Maintain capacity without causing loss

**Threshold (ssthresh)**:
- Boundary between Slow Start and Congestion Avoidance
- Set dynamically based on losses

### Slow Start

**Initial state**:
```
cwnd = 1 MSS (e.g., 1500 bytes)
ssthresh = 65535 (or receiver window size)
```

**Per ACK received**:
$$\text{cwnd} \leftarrow \text{cwnd} + \text{MSS}$$

**Effect**: Window doubles per round-trip time

```
RTT 0: cwnd = 1 MSS
  Send: 1 segment

RTT 1: ACK received
  cwnd = 1 + 1 = 2 MSS
  Send: 2 segments

RTT 2: 2 ACKs received
  cwnd = 2 + 1 + 1 = 4 MSS
  Send: 4 segments

RTT 3: 4 ACKs received
  cwnd = 4 + 1 + 1 + 1 + 1 = 8 MSS
  Send: 8 segments
  
Growth: 1 → 2 → 4 → 8 → 16 → ... (exponential)
```

**Why exponential?**: Network mostly underutilized at start; safe to probe aggressively.

### Congestion Avoidance

**Transition**: When cwnd ≥ ssthresh, switch to Congestion Avoidance

**Per ACK received**:
$$\text{cwnd} \leftarrow \text{cwnd} + \frac{\text{MSS}^2}{\text{cwnd}}$$

**Effect**: Window grows by 1 MSS per round-trip time (linear)

```
RTT K: cwnd = 10 MSS
  Send: 10 segments

RTT K+1: 10 ACKs received
  cwnd = 10 + (1500)^2/(10×1500) = 10 + 1.5/1 ≈ 11 MSS
  Send: 11 segments

RTT K+2: 11 ACKs received
  cwnd ≈ 12 MSS
  
Growth: 10 → 11 → 12 → 13 → ... (linear, +1 MSS/RTT)
```

**Why linear?**: At high utilization, risk of congestion. Conservative probing.

### Loss Detection and Recovery

**Upon timeout or fast retransmit** (loss detected):

```
ssthresh = cwnd / 2
cwnd = 1 MSS
state = SLOW_START

// Restart probing from small window
```

**Rationale**: Loss indicates congestion; drastically reduce sending rate and restart.

**Example**:
```
cwnd builds up to 100 MSS
Loss occurs at RTT 20
ssthresh = 50 MSS
cwnd = 1 MSS
state = SLOW_START

Restart from 1 MSS; probe up to 50 MSS; then linear.
```

### TCP Tahoe Algorithm Pseudocode

```
initialization:
  cwnd ← 1 MSS
  ssthresh ← 65535
  
on ACK received:
  if cwnd < ssthresh:  // Slow Start
    cwnd ← cwnd + MSS  // Exponential
  else:  // Congestion Avoidance
    cwnd ← cwnd + MSS²/cwnd  // Linear
    
on loss detected (timeout or 3-dup-ACK):
  ssthresh ← cwnd / 2
  cwnd ← 1 MSS
  retransmit lost segment
```

## [[TCP_Reno]]: Fast Retransmit and Fast Recovery

### Problem with Tahoe

```
Fast Retransmit (detect loss after 3 duplicate ACKs, not timeout):
  - Faster than waiting for RTO timeout
  - ACK arrives within ~100ms vs. seconds for timeout
  
Still resets cwnd to 1 MSS:
  - Severe reduction
  - Underutilizes network after transient loss
  - Throughput suffers
```

### Solution: Fast Recovery

**Upon loss detected by 3-duplicate-ACKs** (not timeout):

```
ssthresh ← cwnd / 2
cwnd ← ssthresh + 3 × MSS  // Halfway point, not 1!
(3 MSS accounts for 3 duplicate ACKs received)
state ← FAST_RECOVERY
```

**In FAST_RECOVERY state**:

```
per_ack_received:
  if ack_advances_beyond_loss:
    cwnd ← ssthresh  // Smooth return to normal
    state ← CONGESTION_AVOIDANCE
  else:  // ACK is for loss point or before
    cwnd ← cwnd + MSS  // Prevent window collapse
```

**Benefit**:
- Window reduces to half (not 1)
- Recovers quickly
- Maintains network utilization

### Example: Tahoe vs. Reno

```
Both build cwnd to 100 MSS
Loss occurs

Tahoe:
  cwnd: 100 → 1 → 2 → 4 → 8 → ... → 50 (slow!)
  
Reno:
  cwnd: 100 → 53 (= 50 + 3) → 54 → 55 → ... → normal
  Recovery: Much faster
```

## TCP Newer Variants

### CUBIC

Modern TCP focusing on high-speed, high-delay networks:

```
Window function: cubic curve (not linear + exponential)
Aims to: Detect available bandwidth quickly, maintain fairness

Used by: Linux, most modern systems
```

### BBR (Bottleneck Bandwidth and RTT)

Google's algorithm:

```
Philosophy: Avoid packet loss; model network directly
Measures: Bottleneck bandwidth, minimum RTT
Target: cwnd = bandwidth × RTT (BDP)

Avoids: Congestion collapse through intelligent probing
```

## Other Congestion Control Mechanisms

### AIMD (Additive Increase Multiplicative Decrease)

**General principle used by most algorithms**:

```
Additive Increase: Increase rate by fixed amount per RTT
  cwnd ← cwnd + increment

Multiplicative Decrease: Upon loss, reduce by factor
  cwnd ← cwnd × factor  (typically 0.5)
  
Fairness: Multiple flows converge to equal share
Stability: Prevents oscillation
```

[[TCP_Tahoe]] and [[TCP_Reno]] both use AIMD (Tahoe also multiplies by factor during recovery).

### ECN (Explicit Congestion Notification)

**RFC 3168**: Router signals congestion without dropping packets

```
Router detects congestion:
  Mark ECN bit in IP header

Receiver receives marked packet:
  Sets ECN-Echo flag in ACK

Sender receives ECN:
  Reduces cwnd (like packet loss)
  But no retransmission needed (packet not lost)

Benefit: Early signal; avoid loss
```

## Throughput and Fairness

### Steady-State Throughput

After convergence:

$$\text{Throughput} \approx \frac{\text{window\_size}}{\text{RTT}}$$

With AIMD (e.g., Tahoe):

```
Losses occur periodically when cwnd reaches capacity

Average cwnd ≈ (cwnd_max + cwnd_min) / 2
           = (2 × cwnd_before_loss + 1 ) / 2  (Tahoe, simplified)

Loss Probability p:
  Packet drop triggers when cwnd ~ 1/p
  
Theoretical: Throughput ∝ 1/√p (relates to MSS, RTT, p)
```

**Practical**: 1% loss → 10× throughput loss compared to 0% loss.

### Fairness Between Flows

**AIMD ensures fairness**:

```
Flow A: cwnd_A
Flow B: cwnd_B

If cwnd_A > cwnd_B:
  A increases slower (MSS per RTT is same)
  Both decrease together on loss (multiplicative factor)
  → Converge toward equality

After convergence: cwnd_A ≈ cwnd_B
  Throughput_A ≈ Throughput_B
```

**Bandwidth sharing**: Each flow gets fair allocation over time.

## Interaction with Flow Control

### Both Mechanisms Constrain Transmission

```
send_window = min(cwnd, receiver_advertised_window)

Scenario 1: Congestion-limited
  cwnd = 10 MSS (small, due to loss)
  receiver_window = 100 MSS
  Send: 10 MSS/RTT

Scenario 2: Receiver-limited
  cwnd = 100 MSS (large, network has capacity)
  receiver_window = 5 MSS (receiver slow)
  Send: 5 MSS/RTT
```

## Measurement and Monitoring

### Detecting Congestion

**Timeout (RTO expires)**:
```
No ACKs for RTO seconds
→ Assume heavy congestion
→ Conservative: reset cwnd to 1
→ Slow restart
```

**3 Duplicate ACKs**:
```
Receiver still acknowledging; network transmitting
→ Transient loss, not severe congestion
→ Less severe: cwnd to half (in Reno)
```

**ECN bit**:
```
Router signals without loss
→ Proactive: reduce before loss
```

### RTT Measurement

[[TCP_Protocol|TCP]] measures RTT for each segment's ACK arrival:

```
Timestamp option in segment
ACK echoes timestamp
RTT = ACK_arrival - segment_send_time

Used to: Calculate RTO for timeout
         Smooth variations in network
```

## Congestion Control in Modern Networks

### Mobile Networks (LTE, 5G)

Challenge: High loss rate, variable capacity
Solution: Algorithms like BBR adapt to capacity changes

### Data Center Networks

Challenge: Microsecond latencies, different failure modes
Solution: Custom congestion control (DCTCP, DCQCN)

### Wireless

Challenge: Loss from interference, not congestion
Solution: Distinguish congestion loss from wireless loss

## See Also

- [[TCP_Protocol]]: TCP's congestion control integration
- [[TCP_Tahoe]]: First algorithm details
- [[TCP_Reno]]: Improved algorithm with fast recovery
- [[Flow_Control_Mechanisms]]: Receiver-side control vs. congestion
- [[Segment_Structure]]: ACK mechanism
- [[Service_Primitives]]: SEND behavior during congestion
