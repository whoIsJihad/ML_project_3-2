# TCP Tahoe

## Historical Significance

**TCP Tahoe** (1988) is the first practical [[Congestion_Control|congestion control]] algorithm, credited to Van Jacobson. It ended the 1986 Internet congestion collapse.

## Algorithm Components

### Initialization

```
cwnd = 1 MSS  (e.g., 1500 bytes)
ssthresh = 65535
state = SLOW_START
```

### Slow Start Phase

**Condition**: cwnd < ssthresh

**Per ACK received**:
$$\text{cwnd} ← \text{cwnd} + \text{MSS}$$

**Growth rate**: Exponential (doubles per RTT)

**Intuition**: Network mostly empty at start; safe to probe aggressively

**Example**:
```
RTT 0: cwnd = 1 MSS
  Sender can send: 1 segment

RTT 1: Receive 1 ACK
  cwnd = 1 + 1 = 2 MSS
  Sender can send: 2 segments

RTT 2: Receive 2 ACKs
  For each: cwnd += 1
  cwnd = 2 + 1 + 1 = 4 MSS
  Sender can send: 4 segments

RTT 3: Receive 4 ACKs
  cwnd = 4 + 4 = 8 MSS

Growth: 1 → 2 → 4 → 8 → 16 → ... (exponential)
Duration: O(log N) RTTs to reach target window N
```

### Congestion Avoidance Phase

**Condition**: cwnd ≥ ssthresh

**Per ACK received**:
$$\text{cwnd} ← \text{cwnd} + \frac{\text{MSS}^2}{\text{cwnd}}$$

**Growth rate**: Linear (increases by 1 MSS per RTT)

**Intuition**: High utilization; risk of congestion; conservative probing

**Example**:
```
cwnd = 10 MSS at start of RTT
Receive 10 ACKs during RTT
Each ACK adds: MSS²/(cwnd) ≈ 1500²/15000 = 150 bytes
Total: 10 × 150 = 1500 bytes = 1 MSS
Result: cwnd = 11 MSS (increased by 1 MSS)

Growth: 10 → 11 → 12 → 13 → ... (linear, +1 MSS per RTT)
```

### Loss Detection and Recovery

**On timeout** (RTO expires) or **3-duplicate-ACK**:

```
ssthresh ← max(2, cwnd / 2)
cwnd ← 1 MSS
state ← SLOW_START
retransmit_lost_segment()
```

**Rationale**:
- Loss indicates congestion
- Drastically reduce sending rate (reset to 1)
- Restart probing from small window
- Conservative; prevents further congestion

## Algorithm Pseudocode

```python
def tahoe():
    cwnd = 1 * MSS
    ssthresh = 65535
    
    while True:
        # Transmit data
        while bytes_in_flight < cwnd:
            segment = create_segment()
            send(segment)
            bytes_in_flight += MSS
            set_retransmit_timer()
        
        # Wait for ACK or timeout
        event = wait_for_event()
        
        if event == "ACK received":
            bytes_in_flight -= segment.size
            
            if cwnd < ssthresh:
                # Slow Start: exponential
                cwnd += MSS
            else:
                # Congestion Avoidance: linear
                cwnd += MSS * MSS / cwnd
        
        elif event == "RTO timeout" or "3-duplicate-ACK":
            # Loss detected
            ssthresh = max(2 * MSS, cwnd / 2)
            cwnd = 1 * MSS
            retransmit()
            continue_slow_start()
```

## Throughput Behavior

### Window Growth

```
Time (RTTs)    cwnd           Behavior
0              1 MSS          Start
1              2 MSS          Slow Start (2×)
2              4 MSS          Slow Start (2×)
3              8 MSS          Slow Start (2×)
4              16 MSS         Slow Start (2×)
5              32 MSS         Slow Start (2×)
6              64 MSS         Transition (assume ssthresh = 64)
7              65 MSS         Congestion Avoidance (+1)
8              66 MSS         Congestion Avoidance (+1)
...
K              Loss detected
K+1            1 MSS          Reset; restart Slow Start
```

### Throughput After Loss

Upon loss at cwnd = W:

```
ssthresh = W/2
cwnd reset to 1
Time to recover to W/2:
  Slow Start from 1 to W/2 takes log₂(W/2) RTTs
  
Example: Loss at cwnd = 64 MSS
  ssthresh = 32 MSS
  Recover to 32 MSS: log₂(32) = 5 RTTs
  
Throughput impact: Significant reduction; slow recovery
```

## Limitations

### Aggressive Slow Start

```
Sends aggressively; may overshoot capacity
Causes burst of losses
Severe window reduction (to 1 MSS)
Recovery time: logarithmic in window size
Long recovery time after loss; underutilizes network
```

### Poor Recovery

```
Example: Loss at cwnd = 100 MSS
Result: cwnd = 1 MSS
Must rebuild: 1 → 2 → 4 → 8 → 16 → 32 → 64 → 100
Time: ~7 RTTs to recover
Network utilization drops 100× during recovery
```

## Improvements: TCP Reno

[[TCP_Reno]] addressed Tahoe's recovery problem with **Fast Recovery**:

```
On 3-duplicate-ACK (not timeout):
  ssthresh = cwnd / 2
  cwnd = ssthresh + 3 * MSS (not 1!)
  
Recovery: cwnd jumps to halfway; faster than exponential restart
```

## Historical Impact

**Tahoe (1988)**:
- First congestion control algorithm
- Solved 1986 Internet collapse
- Foundation for all modern TCP
- Used widely until replaced by Reno

**Legacy**: Tahoe concepts (slow start, AIMD) remain in all TCP variants today.

## See Also

- [[Congestion_Control]]: Overview of congestion control
- [[TCP_Reno]]: Improved algorithm with fast recovery
- [[TCP_Protocol]]: TCP's congestion control integration
- [[AIMD]]: Additive Increase Multiplicative Decrease principle
