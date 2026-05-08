# Flow Control Mechanisms

## Purpose

**Flow control** prevents a sender from overwhelming a receiver's buffer capacity. Unlike [[Congestion_Control|congestion control]] which manages network capacity, flow control is receiver-centric: "My buffer is full; slow down."

## Problem

### Buffer Overflow

Without flow control:

```
Sender sends: 1 Mbps (1000 segments/sec, 1000 bytes each)
Receiver's buffer: 100 KB (100 segments)
Receiver processes: 100 Kbps (100 segments/sec)

After 1 second:
  Received: 1000 segments; only processed 100
  Buffer: 100 segments + 900 segments received = 1000 segments
  Buffer size: 1000 × 1000 bytes = 1 MB
  
If buffer allocated as fixed 100 KB: overflow! Segments lost.
```

**Flow control solves**: Sender asks "How much can you receive?" before sending.

## Window-Based Flow Control

### Core Mechanism

Receiver advertises **window** (buffer space available):

$$\text{sender\_send\_limit} = \text{receiver\_window}$$

**In [[TCP_Protocol|TCP]]**: 16-bit window field in segment header

```
Receiver has 64 KB buffer:
  Receiver advertises: Window = 65535 (maximum)
  
Sender can send up to 65535 bytes without further ACK
  After sending 32767 bytes: window_available = 32768
  After sending 65535 bytes: window_available = 0
  
Sender stops sending; waits for ACK.

Receiver processes 10000 bytes; buffer has 55535 bytes free
  Receiver advertises new: Window = 55535
  
Sender resumes; sends remaining 55535 bytes of accumulated data.
```

### Implementation: Sender Side

Sender maintains:

```
send_window = receiver_advertised_window
bytes_in_flight = 0

while data_to_send:
  if bytes_in_flight < send_window:
    segment = create_segment(send_window - bytes_in_flight)
    send(segment)
    bytes_in_flight += segment.size
  else:
    wait_for_ack_or_window_update()
```

**Variable**: `bytes_in_flight` tracks unacknowledged data in network.

### Implementation: Receiver Side

Receiver maintains:

```
buffer_size = 64 KB
bytes_received_not_yet_read = 0
window = buffer_size - bytes_received_not_yet_read

upon segment_arrival(segment):
  if bytes_received_not_yet_read + segment.size <= buffer_size:
    buffer.enqueue(segment)
    bytes_received_not_yet_read += segment.size
    window = buffer_size - bytes_received_not_yet_read
    send_ack_with_window(window)
  else:
    discard_segment()  // Buffer full
    window = 0
    send_ack_with_window(window)

upon application_read(n_bytes):
  data = buffer.dequeue(n_bytes)
  bytes_received_not_yet_read -= n_bytes
  window = buffer_size - bytes_received_not_yet_read
  // Next ACK sent will advertise updated window
```

## Zero Window and Probe

### Zero Window State

If receiver buffer becomes full:

```
Receiver: window = 0
Sender: bytes_in_flight ≥ send_window; cannot send

Sender blocked indefinitely:
  Waiting for ACK that increases window
  Receiver processing data; buffer space opens up
  But receiver can't send unless segment arrives from sender
  
Deadlock risk!
```

### Solution: Probe Segments

TCP uses **persist timer**:

When sender's window = 0:
```
persist_timer = set to timeout (e.g., 5 seconds)

persist_timer expires:
  Send "probe" segment (1 byte or empty ACK)
  This forces receiver to respond with updated window
  
If window still 0: restart persist_timer
If window > 0: resume sending
```

**Probe semantics**:
- May or may not contain data (typically empty)
- Forces receiver to send ACK with window update
- Breaks potential deadlock

## Buffer Management Strategies

### Fixed-Size Buffer

**Simplest approach**:
```
Buffer allocated: 64 KB
Window advertised: 64 KB initially
Upon arrival: buffer_used += segment.size
Window = 64 KB - buffer_used

No dynamic allocation; predictable memory use.
```

**Limitations**:
- If application slow, buffer fills
- Window shrinks; sender must wait
- Can't adapt to bursty traffic

### Variable-Size Buffer

**Dynamic allocation**:
```
Buffer grows as needed (up to max)
Window can increase beyond initial size

Advantages:
  - Adapt to application speed
  - Allow bursts without loss
  
Disadvantages:
  - Unpredictable memory usage
  - Need protection against runaway allocation
```

### Circular Buffer

**Memory reuse**:
```
Allocate fixed 64 KB as ring:

Write position → [new data written here]
Read position → [old data read from here]

Available space = buffer_size - (write_pos - read_pos)
Window = available_space

As application reads: read_pos advances; space recycles
Efficient; no malloc/free overhead
```

## Delayed Acknowledgment

### Problem: Inefficiency

```
Receiver gets 1 KB segment
Receiver immediately sends 1 KB ACK
Ratio: 1:1 control overhead

High ACK frequency:
  Wastes bandwidth on control packets
  Adds latency (system interrupts per ACK)
```

### Solution: Delayed ACK

TCP allows delaying ACK if:
1. More data expected from sender, OR
2. Can piggyback ACK on outgoing data

```
Receiver sets timer (e.g., 40 ms)
upon segment_arrival:
  if first_segment_of_burst:
    set ack_timer
  else if ack_timer_pending:
    reset ack_timer  // Restart delay
    
upon ack_timer_expiration:
  send ACK
  
upon application_send_data:
  send_data_with_piggybacked_ack()  // Include ACK in data segment
```

**Typical strategy**: ACK every other segment or after 40 ms, whichever comes first.

**Benefit**:
- Reduced ACK frequency (half or less)
- Reduced bandwidth
- Reduced CPU interrupt rate

**Cost**:
- Sender wait for ACK slightly longer
- Doesn't significantly impact [[TCP_Protocol|TCP]] throughput

## [[Silly_Window_Syndrome|Silly Window Syndrome]]

### Problem Definition

**Scenario**: Sender and receiver agreement leads to pathologically small segments:

```
Receiver buffer: 4 KB
Application slow; empties 1 KB per 100 ms
After 1 KB removed: window = 1 KB
Sender: "Only 1 KB window? Send 1 KB segment."
Receiver: Buffer accumulates 1 KB, can't read fast enough
  window = 512 bytes
Sender: "512 bytes window? Send 512 byte segment."
Sender: "256 bytes window? Send 256 byte segment."
...
Eventually: Single byte segments with full headers!
```

**Waste**: 40-byte header to send 1 byte of data.

### Clark's Solution (Receiver-Side)

Receiver doesn't advertise small windows:

```
Rules:
  1. If window < minimum_threshold: advertise window = 0
  2. Once window is 0, don't increase it until:
     a. Application has read >= half of buffer, OR
     b. Buffer is completely empty
     
Prevents: Small window advertisements that lead to tiny segments
```

**Example**:
```
Buffer 64 KB, threshold = 4 KB

Receiver: buffer_used = 62 KB, available = 2 KB
Advertise: window = 0 (less than threshold)

Application reads 32 KB: buffer_used = 30 KB, available = 34 KB
Advertise: window = 34 KB (> threshold; now advertise)
```

### [[Nagle_Algorithm|Nagle's Algorithm]] (Sender-Side)

Sender doesn't send small segments:

```
Rule: Don't send segment unless:
  1. Have >= MSS (Maximum Segment Size) bytes to send, OR
  2. All previously sent data has been ACK'd (window is full)
  
Effect:
  Small messages wait for ACK of previous segment
  Coalesces into larger packets
  
Example:
  Telnet: Each keystroke is 1 byte
  Without Nagle: Send 1 byte immediately (1 byte + 40 byte header)
  With Nagle: Wait for prior byte's ACK before sending next
              Groups keystrokes into larger segments
```

**Can disable**: For interactive apps (games, real-time) that need low latency.

```
socket.setsockopt(TCP_NODELAY, 1)  // Disable Nagle
```

**Trade-off**:
- Enabled: Good for bulk transfer, streaming
- Disabled: Good for interactive (Telnet, SSH), where latency > efficiency

## Congestion Window vs. Receiver Window

### Two Limits

Sender's actual window is minimum of:

$$\text{send\_window} = \min(\text{congestion\_window}, \text{receiver\_window})$$

**Receiver window** (rwnd):
- Advertised by receiver
- Receiver-centric: "My buffer"
- Dynamic: changes as application drains buffer
- Goal: Prevent buffer overflow at receiver

**Congestion window** (cwnd):
- Maintained by sender
- Network-centric: "Estimate of network capacity"
- Dynamic: increases in slow start, decreases on loss
- Goal: Prevent network congestion
- See [[Congestion_Control|Congestion Control]]

**Both must be respected**:

```
If cwnd = 10 KB and rwnd = 5 KB: Send at most 5 KB
If cwnd = 5 KB and rwnd = 10 KB: Send at most 5 KB
If cwnd = 10 KB and rwnd = 10 KB: Can send up to 10 KB
```

## Interaction with Reliability

### Retransmission and ACK

```
Sender sends: SEQ=1000, data="Hello" (5 bytes)
Receiver receives: acknowledges with ACK=1005, window=10000

Sender knows:
  - Data received (ACK=1005)
  - Can send up to 10000 more bytes (window=10000)
  
If ACK were lost:
  Sender times out; retransmits
  Receiver receives duplicate; discards by sequence number
  Receiver sends ACK again
  
ACK loss doesn't break flow control; retransmission recovers.
```

## Practical Scenarios

### Slow Receiver

```
Receiver: Processes 100 KB/s
Sender: Network capable of 1 Mbps

Receiver advertises window = 100 KB
Sender sends 100 KB, then stops waiting for ACK
Receiver processes at 100 KB/s
Sender throughput limited to 100 KB/s (by receiver, not network)
```

### Application Write Buffering

```
Application: SEND("Large file", 10 MB)
Transport: Can only send window_size bytes now
Remaining queued in transport send buffer
As ACKs arrive: window updates; send more

If window too small:
  Large accumulation in send buffer
  Memory usage grows
  Sender may block on SEND if buffer exceeds high water mark
```

## See Also

- [[TCP_Protocol]]: TCP window mechanism
- [[Segment_Structure]]: Window field in TCP header
- [[Congestion_Control]]: Network-side flow control
- [[Nagle_Algorithm]]: Sender-side optimization
- [[Clark_Solution]]: Receiver-side optimization
- [[Service_Primitives]]: SEND behavior with flow control
