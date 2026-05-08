# Leaky Bucket and Token Bucket Comparison Simulation

## Prerequisite

This note provides a detailed step-by-step comparison of the [[Leaky_Bucket_Algorithm|Leaky Bucket]] and [[Token_Bucket_Algorithm|Token Bucket]] algorithms through a practical simulation. Familiarity with both algorithms is assumed.

## Simulation Setup

### Network Scenario

A router ingress is receiving traffic from a source that must conform to a traffic profile:
- **Sustainable rate**: 1000 bits/second.
- **Burst allowance**: 3000 bits (enough for 3 seconds at sustainable rate, or 0.3 seconds at 10 Mbps link).

### Traffic Pattern

The source sends packets according to the following schedule:

| Time | Packet Size (bits) | Description |
|---|---|---|
| $t=0$ s | 1000 | Packet 1 |
| $t=0.5$ s | 1000 | Packet 2 |
| $t=1$ s | 2000 | Packet 3 (large burst) |
| $t=1.5$ s | 500 | Packet 4 |
| $t=2$ s | 500 | Packet 5 |
| $t=2.5$ s | 1000 | Packet 6 |

**Total traffic**: 6000 bits over 2.5 seconds = 2400 bits/second average.

This exceeds the sustainable rate (1000 bits/s), testing how each algorithm handles excess traffic.

## Leaky Bucket Simulation

### Setup

- Bucket capacity: $B = \infty$ (or very large; packets are queued indefinitely).
- Leak rate: $L = 1000$ bits/second.

### Algorithm

```
At each time step Δt:
  Leaked = L × Δt = 1000 × Δt bits

Queue state:
  queue_size(t) = queue_size(t-1) - Leaked + arrivals(t)
  
Transmission:
  bits_transmitted = min(queue_size(t), L × Δt)
```

### Timeline

**$t = 0$ s: Packet 1 (1000 bits) arrives**

```
queue_size(0) = 0 + 1000 = 1000 bits
transmitted(0 to Δt) = min(1000, 1000 × Δt)

Assuming Δt = 1 ms:
transmitted = 1 bit (or less, depending on time granularity)
```

For continuous time analysis, let's track queue size and transmission rate:

```
Queue Size over time (Leaky Bucket):

| Time | Arrival | Queue Size | Leak | Transmitted |
|---|---|---|---|---|
| 0 | +1000 | 1000 | 1000 × 1s = 1000 | 1000 bits/s |
| 1s | 0 | 0 | — | 0 |
| 0.5s | +1000 | 1000 | 500 | 500 bits/s |
| 1s | +2000 | 2000 + 500 = 2500 | 1000 | 1000 bits/s |
| 1.5s | +500 | 2500 - 1000 + 500 = 2000 | 1000 | 1000 bits/s |
| 1.5s to 2s | 0 | 2000 - 500 = 1500 | 500 | 500 bits/s |
| 2s | +500 | 1500 + 500 = 2000 | 1000 | 1000 bits/s |
| 2.5s | +1000 | 2000 - 500 + 1000 = 2500 | 1000 | 1000 bits/s |
| 3.5s | 0 | 0 | — | 0 |
```

**Detailed Analysis**:

**$t = 0$ to $t = 1$ s**: Packet 1 arrives. Queue builds to 1000 bits. Leaking at 1000 bits/s empties the queue in 1 second.

**$t = 0.5$ s**: Packet 2 (1000 bits) arrives. Queue size is $1000 - 500 = 500$ bits (leaked from Packet 1). New queue size: $500 + 1000 = 1500$ bits.

**$t = 1$ s**: Packet 3 (2000 bits) arrives. Queue size has dropped to $1500 - 500 = 1000$ bits. New queue size: $1000 + 2000 = 3000$ bits.

**Output Rate**: Constant 1000 bits/s (the leak rate).

**Queueing Delay**: Packets experience delay proportional to queue length.

- Packet 1: Dequeued after 1 second.
- Packet 2: Arrives at 0.5s, queue size 1500. Time to dequeue: $\frac{1500}{1000} = 1.5$ s. Transmitted around $t = 2$ s.
- Packet 3: Arrives at 1s, queue size 3000. Time to dequeue: $\frac{3000}{1000} = 3$ s. Transmitted around $t = 4$ s.

### Key Properties of Leaky Bucket

1. **Constant output rate**: Exactly 1000 bits/s (smooth).
2. **Queueing overhead**: Large queue builds up; Packet 3 waits 3 seconds.
3. **Delay increases**: Later packets experience increasing delay.
4. **No burst transmission**: Even though the bucket has capacity, the leak rate is fixed.

## Token Bucket Simulation

### Setup

- Token rate: $r = 1000$ tokens/second.
- Bucket capacity: $C = 3000$ tokens.
- Initial tokens: $T(0) = 0$.

### Algorithm

```
At packet arrival:
  // Update tokens
  time_elapsed = current_time - last_update_time
  T = min(C, T + r × time_elapsed)
  last_update_time = current_time
  
  if (T ≥ packet.size):
    T -= packet.size
    transmit immediately
  else:
    queue packet
  end if
```

### Timeline

**$t = 0$ s: Packet 1 (1000 bits) arrives**

```
Tokens available: T = 0 + 1000 × 0 = 0
Packet size: 1000 bits
Decision: Queue (insufficient tokens)
```

**$t = 0.5$ s: Packet 2 (1000 bits) arrives**

```
Time since last update: 0.5 s
Tokens added: 1000 × 0.5 = 500
T = min(3000, 0 + 500) = 500 tokens
Packet size: 1000 bits
Decision: Queue (insufficient tokens)
Total queued: 1000 + 1000 = 2000 bits
```

**$t = 1$ s: Packet 3 (2000 bits) arrives**

```
Time since last update: 0.5 s
Tokens added: 1000 × 0.5 = 500
T = min(3000, 500 + 500) = 1000 tokens
Packet size: 2000 bits
Decision: Queue (insufficient tokens)
Total queued: 2000 + 2000 = 4000 bits
```

**$t = 1.5$ s: Packet 4 (500 bits) arrives**

```
Time since last update: 0.5 s
Tokens added: 1000 × 0.5 = 500
T = min(3000, 1000 + 500) = 1500 tokens
Packet size: 500 bits
Decision: Transmit; T = 1500 - 500 = 1000 tokens
```

At this point, the scheduler can dequeue from the queue:
- Packet 1 (1000 bits): Tokens available = 1000. Transmit; T = 0.
- Queued packets remaining: 2000 + 2000 = 4000 bits.

**$t = 2$ s: Packet 5 (500 bits) arrives**

```
Time since last update: 0.5 s
Tokens added: 1000 × 0.5 = 500
T = min(3000, 0 + 500) = 500 tokens
Packet size: 500 bits
Decision: Transmit; T = 500 - 500 = 0 tokens
```

Scheduler dequeues: Nothing (tokens depleted).

**$t = 2.5$ s: Packet 6 (1000 bits) arrives**

```
Time since last update: 0.5 s
Tokens added: 1000 × 0.5 = 500
T = min(3000, 0 + 500) = 500 tokens
Packet size: 1000 bits
Decision: Queue (insufficient tokens)
```

**$t = 3$ s onwards**: Tokens continue to accumulate, dequeuing packets from the queue.

### Transmission Schedule

| Packet | Arrival Time | Transmission Time | Delay |
|---|---|---|---|
| 1 | 0 s | 1.5 s | 1.5 s |
| 2 | 0.5 s | 1.5 s | 1.0 s |
| 3 | 1 s | 3.0 s | 2.0 s |
| 4 | 1.5 s | 1.5 s | 0 s (immediate) |
| 5 | 2 s | 2.0 s | 0 s (immediate) |
| 6 | 2.5 s | 3.5 s | 1.0 s |

**Dequeue Timeline**:
- At $t = 1.5$ s: 1000 tokens available; dequeue Packet 1 (1000 bits).
- At $t = 2$ s: 500 tokens available; dequeue first 500 bits of Packet 2; cannot complete.
- At $t = 2.5$ s: 1000 tokens available; complete Packet 2 (500 remaining bits already dequeued) and dequeue Packet 3 (2000 bits). Dequeue fails due to insufficient tokens; only partial dequeue.
- At $t = 3$ s: Bucket full (3000 tokens); dequeue remaining packets.

**Transmission Output**: Variable rate (burst transmission followed by idle periods).

### Comparison Output Rate

**Leaky Bucket**: Exactly 1000 bits/s (smooth).

**Token Bucket**: 
- $t = 0$ to $1.5$ s: 0 bits/s (queueing).
- $t = 1.5$ to $2$ s: High rate (dequeuing 1000 bits in 0.5 s = 2000 bits/s).
- $t = 2$ to $2.5$ s: Moderate rate.
- $t = 2.5$ onwards: Variable, eventually 1000 bits/s average.

## Graphical Comparison

### Queue Length Over Time

```
Queue Size (bits)

        Leaky Bucket
4000 |
     |     ╱─────────────────
3000 |    ╱╲
     |   ╱  ╲────────────
2000 |  ╱       
     | ╱
1000 |╱
     └───────────────────── Time (s)
     0   1   2   3

        Token Bucket
4000 |  ╱──────────────╲
     | ╱                ╲
3000 |╱                  ╲
     |
2000 |
     |                    ╲
1000 |                     ╲
     |                      ╲
   0 └───────────────────────── Time (s)
     0   1   2   3   4
```

Token Bucket queue builds faster initially (no transmission until sufficient tokens) but decreases faster (burst dequeuing) once tokens accumulate.

## Summary of Differences

| Aspect | Leaky Bucket | Token Bucket |
|---|---|---|
| **Output Regularity** | Perfectly smooth | Bursty (with smooth average) |
| **Burst Support** | No | Yes (up to bucket capacity) |
| **Queueing Delay** | High (all packets queued) | Lower (some packets immediate) |
| **Burst Transmission** | Impossible | Possible (when bucket full) |
| **Average Rate** | Exactly leak rate | Exactly token rate (long-term) |
| **Peak Rate** | Leak rate | Much higher (limited by link) |
| **Suitability** | Strict rate control | Flexible rate with bursts |

## Use Case Scenarios

### When to Use Leaky Bucket

- **Strict rate enforcement**: Network requires exactly constant output (e.g., ATM networks).
- **Smoothing bursty traffic**: Input traffic is bursty; must be smoothed for downstream.
- **Simple implementation**: Leaky bucket is simpler conceptually.

### When to Use Token Bucket

- **Variable rate applications**: Applications can tolerate and benefit from bursts.
- **Efficient bandwidth utilization**: Allows short periods of high transmission, improving responsiveness.
- **QoS-aware networks**: Token bucket provides flexibility in QoS design.

## Real-World Considerations

**Linux Traffic Control (tc)**:
- `tc` tool uses Token Bucket Filter (TBF) for rate limiting.
- Parameters: rate (tokens/s), buffer (bucket capacity), limit (max queue).

**Hardware Implementation**:
- Modern routers often implement token bucket algorithms in hardware for high-speed processing.

## Related Concepts

- [[Leaky_Bucket_Algorithm]]: Detailed leaky bucket mechanism.
- [[Token_Bucket_Algorithm]]: Detailed token bucket mechanism.
- [[Quality_of_Service_QoS]]: QoS framework incorporating both algorithms.
- [[Congestion_Prevention_Policies]]: Traffic shaping as congestion prevention.

---

**Next:** [[Tunneling_and_VPN]]
