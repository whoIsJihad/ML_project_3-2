# Clark's Solution

## Purpose

**Clark's Solution** (named after David Clark) solves [[Silly_Window_Syndrome|Silly Window Syndrome]] from the receiver side by preventing advertisement of small windows.

## Problem (Review)

```
Receiver: Slow application; buffer gradually fills
Window shrinks: 1000 → 500 → 100 → 50 → 10 bytes

Sender sends increasingly small segments:
  40 bytes header + 50 bytes data (44% header)
  40 bytes header + 10 bytes data (80% header)
  
Eventually: 40-byte header + 1-byte data (97% waste!)
```

Without solution: Pathological SWS on receiving side.

## Solution

### Core Principle

**Receiver doesn't immediately advertise small window increases.**

Instead:
1. If window becomes small: advertise window = 0
2. Wait until window is "sufficiently large" before advertising

### Rules

Receiver advertises window only when:

1. **Window = 0**: Always advertise (breaks potential deadlock)
2. **Window ≥ MSS**: Advertise (allows sender to send full segment)
3. **Window ≥ half of total buffer**: Advertise (significant space available)
4. **Buffer is empty**: Advertise (all space available)

Otherwise: Keep previous window advertisement (don't update).

### Pseudocode

```python
class Receiver:
    def __init__(self, buffer_size=65536):
        self.buffer_size = buffer_size
        self.buffer_used = 0
        self.buffer_free = buffer_size
        self.advertised_window = buffer_size
    
    def on_segment_received(self, segment_size):
        self.buffer_used += segment_size
        self.buffer_free = self.buffer_size - self.buffer_used
    
    def on_application_read(self, num_bytes):
        self.buffer_used -= num_bytes
        self.buffer_free = self.buffer_size - self.buffer_used
    
    def compute_advertised_window(self):
        MSS = 1500  # or negotiated value
        
        # Never advertise shrinking window
        new_window = self.buffer_free
        
        # Apply Clark's rules: only advertise if conditions met
        if self.advertised_window == 0:
            # Currently zero; update if significant space
            if new_window >= MSS or self.buffer_free == self.buffer_size:
                return new_window
            else:
                return 0  # Stay at zero
        
        else:
            # Currently non-zero; may advertise decrease or increase
            
            # Rule 1: Can always go to zero
            if new_window == 0:
                return 0
            
            # Rule 2: Advertise if >= MSS
            if new_window >= MSS:
                return new_window
            
            # Rule 3: Advertise if >= half of buffer
            if new_window >= self.buffer_size // 2:
                return new_window
            
            # Rule 4: Advertise if buffer empty
            if new_window == self.buffer_size:
                return new_window
            
            # None of above; keep previous window
            return self.advertised_window
```

## Effect

### Elimination of Small Windows

```
Buffer = 10 KB, MSS = 1500 bytes, threshold = 5 KB

Scenario: Slow receiver application

t=1: Receive 10 KB segment
  buffer_used = 10 KB, free = 0 KB
  Advertise: window = 0 (rule 1)

t=2: Application reads 100 bytes
  buffer_used = 9.9 KB, free = 0.1 KB
  New window = 100 bytes
  Check: >= MSS? No; >= half? No; buffer empty? No
  Action: Keep previous window = 0

t=3,4,5: Application slowly reads
  buffer_used decreases gradually
  Keep advertising window = 0

t=10: Application has read 5.1 KB total
  buffer_used = 4.9 KB, free = 5.1 KB
  New window = 5.1 KB
  Check: >= half (5 KB)? Yes
  Action: Advertise window = 5.1 KB

Result:
  Sender blocked with window=0 until 5 KB available
  Then sends one large segment (possibly multiple segments up to 5 KB)
  No pathological small windows!
```

## Comparison: With vs. Without Clark

### Without Clark's Solution

```
Time  Window  Sender Action
1     0       Block
2     100     Send 100 bytes (40-byte header!)
3     0       Block
4     150     Send 150 bytes (40-byte header!)
5     0       Block
...

Result: Multiple small segments; high header overhead
```

### With Clark's Solution

```
Time  Window  Sender Action
1     0       Block
2     100     Don't advertise (< MSS)
3     200     Don't advertise (< threshold)
...
10    5100    Advertise! (>= threshold)
11    5100    Send 5100 bytes (or multiple segments)
12    0       Block
...
20    5100    Advertise
21    5100    Send 5100 bytes

Result: Large segments; low header overhead
```

## Trade-offs

### Advantages

1. **Eliminates SWS**: No more 1-byte segments with 40-byte headers
2. **Low overhead**: Segments use space efficiently
3. **Preserves fairness**: Sender not starved of window info
4. **Simple**: Easy to implement

### Disadvantages

1. **Potential deadlock**: If threshold too large
   - Mitigation: Rule 1 (always advertise if window=0)
   
2. **Latency**: Receiver may not advertise immediately
   - Impact: Sender waits for window if space available
   - Typically acceptable (flow control should throttle sender anyway)
   
3. **Threshold tuning**: Requires choosing "half buffer" or MSS
   - Too large: Sender starved
   - Too small: Returns to SWS
   - MSS is natural choice

## Interaction with [[Nagle_Algorithm]]

**Both optimize differently**:

- **Receiver (Clark)**: Stops advertisement of small windows
- **Sender (Nagle)**: Prevents sending of small segments

**Combined effect**:
- Receiver: Doesn't advertise small window
- Sender: Wouldn't send small segment anyway
- Result: Efficient, large-segment transmission

**If only one implemented**:
- Only Clark: Sender may still send small segments (Nagle absent)
- Only Nagle: Receiver may advertise, but sender resists (good enough)

## Historical Context

**David Clark** (MIT) published receiver-side solution concurrent with Nagle.

Together: **Nagle + Clark** form the classic solution to [[Silly_Window_Syndrome]].

**Modern TCP**: Both approaches integrated; most implementations have both.

## Modern Relevance

### Still Important

1. **Embedded TCP stacks**: IoT, automotive systems
2. **Custom implementations**: Protocol stacks in specialized hardware
3. **Performance optimization**: Tuning thresholds for specific workloads
4. **Educational value**: Understanding protocol design trade-offs

### Less Critical in Modern Systems

1. **High bandwidth**: 40-byte header < 0.1% at Gbps speeds
2. **Buffer sizes**: 10s of KB → MB common
3. **Smart implementations**: Nagle + Clark often both present
4. **Hardware offload**: TCP implemented in NIC; transparent optimization

## Recommended Thresholds

For typical systems:

```
Threshold = max(MSS, buffer_size / 2)

Example:
  MSS = 1500 bytes
  buffer_size = 65536 bytes (64 KB)
  threshold = max(1500, 32768) = 32768 bytes
  
  Only advertise window if >= 32 KB available
  Prevents all small-window pathology
```

For resource-constrained systems:

```
Threshold = MSS
  Simpler; fewer rules
  Prevents most SWS
  May miss opportunities to advertise small windows
  Acceptable trade-off
```

## See Also

- [[Silly_Window_Syndrome]]: Problem description
- [[Nagle_Algorithm]]: Complementary sender-side solution
- [[Flow_Control_Mechanisms]]: Root mechanism
- [[TCP_Protocol]]: TCP implementation
