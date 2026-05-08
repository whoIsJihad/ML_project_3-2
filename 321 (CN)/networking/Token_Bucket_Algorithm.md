# Token Bucket Algorithm

## Definition and Motivation

The Token Bucket algorithm is a traffic shaping mechanism that regulates the rate at which data can be transmitted while allowing short-term bursts. Unlike the [[Leaky_Bucket_Algorithm|leaky bucket]], which enforces a constant output rate, the token bucket allows bursts up to a configurable limit.

### Comparison to Leaky Bucket

| Aspect | Leaky Bucket | Token Bucket |
|---|---|---|
| **Output Rate** | Constant | Variable (burst-capable) |
| **Burst Allowance** | No | Yes |
| **Queueing** | Packets are queued | Tokens are buffered |
| **Use Case** | Smooth traffic | Allow bursts within limits |

## Algorithm

### Conceptual Model

Imagine a bucket with a capacity of $C$ tokens. Tokens are added at a constant rate $r$ tokens per second (the bucket can hold at most $C$ tokens; excess tokens are discarded).

**Packet Transmission Rule**:
- Each packet of size $L$ bits requires $L$ tokens to be transmitted.
- If the bucket has $\geq L$ tokens, remove $L$ tokens and transmit the packet immediately.
- If the bucket has $< L$ tokens, queue the packet (or drop it, depending on policy).

### Formal State Representation

Let:
- $T(t)$ = number of tokens in the bucket at time $t$.
- $r$ = token generation rate (tokens/second).
- $C$ = bucket capacity (tokens).
- $L_i$ = size of packet $i$ (bits).

**Token Dynamics**:

Between packets (no transmissions):
$$T(t) = \min(C, T(t-1) + r \cdot \Delta t)$$

where $\Delta t$ is the time interval.

**Transmission Decision**:
```
upon arrival of packet i with size L_i:
  if (T(t) ≥ L_i):
    transmit packet
    T(t) := T(t) - L_i
  else:
    queue or drop packet
  end if
```

### Algorithm Pseudocode

```
Initialize:
  T = 0  // tokens in bucket
  r = token_rate  // tokens per second
  C = bucket_capacity  // maximum tokens
  last_update_time = current_time

Function: packet_arrival(packet):
  // Update token count
  time_elapsed = current_time - last_update_time
  tokens_added = r * time_elapsed
  T = min(C, T + tokens_added)
  last_update_time = current_time
  
  // Check if packet can be transmitted
  if (T ≥ packet.size):
    T -= packet.size
    transmit(packet)
    return ACCEPTED
  else:
    queue(packet)
    return QUEUED  // or DROP, depending on policy
  end if
```

### Continuous vs. Discrete Time

**Continuous Time**:
- Tokens are added continuously at rate $r$.
- Any packet arriving at any time can be immediately checked against current token count.

**Discrete Time**:
- Tokens are added at fixed intervals (e.g., every 1 ms).
- Simpler to implement in software; used in routers.

## Example Scenario

### Setup

- Token rate: $r = 1000$ tokens/second (tokens are bits or byte-equivalents).
- Bucket capacity: $C = 5000$ tokens.
- Initial tokens: $T(0) = 0$.

### Timeline

| Time | Event | Tokens | Action |
|---|---|---|---|
| $t=0$ | Packet 1 (1000 bits) arrives | 0 | Queue (< 1000 tokens) |
| $t=0.001$ s | Tokens added | $0 + 1 = 1$ | — |
| $t=0.002$ s | Tokens added | $1 + 1 = 2$ | — |
| ... | ... | ... | — |
| $t=1$ s | Tokens added, Total | $0 + 1000 = 1000$ | Transmit Packet 1; $T = 0$ |
| $t=1.001$ s | Tokens added | $0 + 1 = 1$ | — |
| $t=2$ s | Tokens accumulated | $1000 + 1000 = 2000$ | — |
| $t=2$ s | Packet 2 (500 bits) arrives | 2000 | Transmit; $T = 1500$ |
| $t=2$ s | Packet 3 (1500 bits) arrives | 1500 | Transmit; $T = 0$ |
| $t=2$ s | Packet 4 (2000 bits) arrives | 0 | Queue |
| $t=4$ s | Tokens accumulated | $0 + 2000 = 2000$ | Transmit Packet 4; $T = 0$ |
| $t=5$ s | Tokens accumulated | $0 + 1000 = 1000$ | — |

**Observations**:
- After the initial wait, packets can be transmitted at a rate of up to $r = 1000$ bits/second on average.
- Bursts are allowed: At $t=2$ s, two consecutive packets (500 + 1500 = 2000 bits) are transmitted immediately, exceeding the average rate.
- Burst size is limited by bucket capacity: The maximum burst is bounded by $C = 5000$ tokens.

## Peak Rate and Sustainable Rate

### Sustainable (Average) Rate

The long-term average transmission rate is limited by the token generation rate:

$$\text{Avg Rate} = r \text{ bits/second}$$

Over a long time $T$, the total tokens available are $\approx r \cdot T$; thus, the average rate approaches $r$.

### Peak (Burst) Rate

In the short term, the entire bucket can be emptied, sending up to $C$ tokens (bits) immediately:

$$\text{Peak Rate} = \frac{C}{\text{token depletion time}}$$

If a single packet of size $C$ arrives when the bucket is full, it is transmitted immediately, achieving peak rate (limited by physical link speed).

**Example**: With $C = 5000$ bits and a 10 Mbps link, the packet is transmitted in $\frac{5000}{10 \times 10^6} = 0.5$ ms.

### Burst Capacity

The maximum burst size is $C$ tokens. After a burst, the bucket depletes and must be refilled at rate $r$.

Time to send a burst of size $B$ (when bucket is full):
$$t_{\text{burst}} = \frac{C}{L_{\text{link}}}$$

where $L_{\text{link}}$ is the link transmission rate.

Time to refill the bucket after burst depletion:
$$t_{\text{refill}} = \frac{C}{r}$$

**Example**: With $C = 5000$ bits, $r = 1000$ bits/s, time to refill is 5 seconds.

## Two-Bucket Token Bucket (Hierarchical)

A more sophisticated version uses two token buckets in series:

**Bucket 1** (Peak Rate Limiter):
- Rate: $r_{\text{peak}}$ tokens/second (peak rate).
- Capacity: $C_{\text{peak}}$ tokens.

**Bucket 2** (Sustained Rate Limiter):
- Rate: $r_{\text{sustained}}$ tokens/second (sustainable rate).
- Capacity: $C_{\text{sustained}}$ tokens.

**Transmission Rule**:
- A packet must have tokens from both buckets to be transmitted.
- If either bucket is empty, the packet is queued.

**Effect**:
- Limits both burst size (via $C_{\text{peak}}$) and sustained rate (via $r_{\text{sustained}}$).
- Provides finer control over traffic profile.

## Implementation in Routers

Token buckets are implemented in router software/hardware using:

1. **Timestamp-based approach**:
   - Instead of continuously updating $T(t)$, update only when a packet arrives.
   - Calculate elapsed time since last packet and add tokens accordingly.

2. **Rate limiter module**:
   - A router scheduler enforces the token bucket rule for each flow or class.
   - Packets that violate the rule are queued or marked.

3. **Marking vs. Dropping**:
   - **Marking**: Non-conformant packets are marked (e.g., with DiffServ code) for later differentiated handling.
   - **Dropping**: Non-conformant packets are discarded.

## Applications

### Traffic Shaping at Ingress

An ISP shapes customer traffic to match a purchased profile:
- $r = 100$ Mbps (sustained rate).
- $C = 1000$ Mb (burst capacity, equivalent to 10 seconds at sustained rate).

Customer traffic exceeding this profile is queued or marked for lower priority.

### QoS Assurance

In a [[Quality_of_Service_QoS|QoS]] framework:
- Applications declare their traffic profile (rate and burst size).
- The network shapes the traffic to the declared profile.
- Routers provide priority or reservation to shaped traffic.

### Rate Control for Protocol Flows

OSPF or BGP routing updates can be rate-limited using token buckets to prevent excessive control traffic.

## Comparison with Leaky Bucket

| Aspect | Leaky Bucket | Token Bucket |
|---|---|---|
| **Token Generation** | Implicit (fixed leak rate) | Explicit (token addition) |
| **Burst Allowance** | None | Yes (up to capacity) |
| **Queuing** | Packets queued until leak time | Packets queued if tokens absent |
| **Smoothness** | Perfectly smooth output | Bursty output (smooth on average) |
| **Implementation** | Simple counter | Token counter, timestamp |
| **Suitability** | Strict rate enforcement | Flexible rate with bursts |

## Related Concepts

- [[Leaky_Bucket_Algorithm]]: Alternative traffic shaping mechanism.
- [[Leaky_Token_Bucket_Comparison_Simulation]]: Practical comparison.
- [[Quality_of_Service_QoS]]: QoS framework incorporating traffic shaping.
- [[Congestion_Prevention_Policies]]: Traffic shaping as a prevention mechanism.

---

**Next:** [[Leaky_Token_Bucket_Comparison_Simulation]]
