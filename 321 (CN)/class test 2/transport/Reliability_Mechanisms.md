# Reliability Mechanisms

## Definition

**Reliability mechanisms** are the technical means by which a transport protocol ensures all data arrives at the destination without loss, duplication, or corruption.

## Core Principles

Transport reliability is built on several interdependent mechanisms:

1. **Checksums**: Detect corruption
2. **Sequence numbers**: Detect loss and duplicates; enable reordering
3. **Acknowledgments**: Confirm receipt
4. **Retransmission**: Recover from loss
5. **Timeouts**: Detect unacknowledged data

## Checksums

### Detection, Not Correction

**Purpose**: Detect bit errors from transmission, memory corruption, or routing errors

**Mechanism**: [[Segment_Structure|TCP/UDP checksum]] covers header and payload

```
Sender computes checksum:
  sum = one's_complement_sum(all 16-bit words)
  checksum_field = one's_complement(sum)
  
Receiver computes:
  sum = one's_complement_sum(all 16-bit words including checksum)
  if sum == 0xFFFF:  // Correct
    Accept segment
  else:  // Error
    Discard segment
```

**Limitations**:
- Detects **errors**, doesn't **correct** them
- Single bit error → detectable
- Multiple bit errors → may not detect (low probability)
- No protection against deliberate corruption (use cryptographic hash)

## Sequence Numbers

### Deduplication

Sequence numbers allow receiver to detect and eliminate duplicates:

```
Sender sends: SEQ=1000, data="Hello" (5 bytes)
  Occupies sequence space [1000, 1005)

Sender times out; retransmits: SEQ=1000, data="Hello" (5 bytes)

Receiver state:
  Already received and delivered [1000, 1005)
  Retransmitted arrives: SEQ=1000
  → In receive window? Already processed? → Discard
  → No duplicate delivery
```

### Reordering

Network may deliver segments out of order:

```
Send: SEQ=1000, SEQ=1500, SEQ=2000

Arrive as: SEQ=2000, SEQ=1000, SEQ=1500

Receiver buffer by sequence number:
  Receive SEQ=2000: not in sequence; buffer
  Receive SEQ=1000: first in order! Deliver, remove from buffer
    Next expected: 1500
  Receive SEQ=1500: next in order! Deliver, remove from buffer
    Next expected: 2000
  Buffered SEQ=2000 now in order: Deliver
  
Application receives in order despite network reordering.
```

### Initialization

Sequence numbers initialized to reduce collision with old packets:

```
Initial Sequence Number (ISN):
  Chosen unpredictably (not 0, not incremental)
  
Typical: ISN derived from hash(IP_src, port_src, IP_dst, port_dst, timestamp)

During three-way handshake:
  Client sends: SYN with ISN_client = x
  Server sends: SYN-ACK with ISN_server = y
  Sequence spaces independent; no correlation between x and y
```

**Why important**: Old segments from previous connections shouldn't be confused with new connection.

## Acknowledgments

### Cumulative Acknowledgment

[[TCP_Protocol|TCP]] uses **cumulative ACKs**: acknowledge up to but not including ACK number

```
Sender sends:
  SEQ=1000: "Hello" (5 bytes)
  SEQ=1005: "World" (5 bytes)
  SEQ=1010: "!!!" (3 bytes)

Receiver receives all in order:
  Bytes [1000, 1015) received
  Send: ACK=1015
  Meaning: "I received everything up through byte 1014; next is byte 1015"
  
Sender upon receiving ACK=1015:
  All bytes [1000, 1015) confirmed
  Can discard from buffer; congestion window can advance
```

### ACKs for Control Segments

**SYN and FIN** also consume sequence numbers:

```
Sender sends: SYN (SEQ=1000)
  Occupies [1000, 1001)
  
Receiver sends: SYN-ACK (ACK=1001)
  Acknowledges: byte 1001 expected next
  
Sender sends: FIN (SEQ=1005, payload=5 bytes)
  Occupies [1005, 1006)
  
Receiver sends: ACK (ACK=1006)
  Acknowledges: byte 1006 expected next
```

### Selective Acknowledgment (SACK)

**Problem with cumulative ACKs**:

```
Segments arrive: 1000-1500, 2000-2500 (gap at 1500-2000)
Cumulative ACK: ACK=1500 (only acknowledges first segment)

Sender doesn't know: 2000-2500 already received!
Sender must retransmit 1500-2000 and will retransmit 2000-2500 (already received)
Wasteful: Unnecessary retransmission of received data
```

**SACK option (RFC 2018)**: Receiver specifies which ranges received

```
Receiver: "I received [1000-1500) and [2000-2500)"
Sender: Retransmit only [1500-2000)
```

**Benefit**: Reduced retransmissions when packets arrive out of order.

## Retransmission

### Timer-Based Retransmission

Sender sets timer when transmitting:

```
Send segment: SEQ=1000
Set timer: RTO (Retransmission Timeout)

Case 1: ACK arrives before timer expiration
  ACK=1005: Acknowledge this segment
  Cancel timer
  
Case 2: Timer expires without ACK
  No acknowledgment received in RTO seconds
  Assume segment lost
  Retransmit segment
  Reset timer (exponential backoff)
  Repeat up to limit
  
Case 3: ACK arrives after retransmission
  ACK may refer to original or retransmitted segment
  Receiver doesn't distinguish (both SEQ=1000)
  Either way: Acknowledged; no duplicate delivery
```

### RTO Calculation

**Adaptive** to network conditions:

```
Measure: Samples of RTT (segment send to ACK arrival)

SRTT (Smoothed RTT):
  SRTT ← (7/8) × SRTT + (1/8) × RTT_sample
  Exponentially weighted moving average (α = 1/8)

RTTVAR (RTT Variance):
  RTTVAR ← (3/4) × RTTVAR + (1/4) × |RTT_sample - SRTT|

RTO ← SRTT + 4 × RTTVAR
```

**Rationale**:
- SRTT: Average RTT (long-term)
- RTTVAR: Variability (short-term)
- RTO larger than typical RTT; accounts for variance
- Prevents spurious timeouts on variable networks

### Exponential Backoff

On repeated timeout:

```
Initial RTO: 1 second
1st timeout: Retransmit, RTO ← min(RTO × 2, 60 seconds)
2nd timeout: Retransmit, RTO ← min(RTO × 2, 60 seconds)
3rd timeout: Retransmit, RTO ← min(RTO × 2, 60 seconds)
...

Attempts: Typically 12-15 before giving up (~9 minutes)

Rationale:
  Congestion likely: Back off exponentially
  Don't hammer network with retransmissions
  Wait longer each time; eventually network recovers
```

## Fast Retransmit

### Problem with Timeout-Based Retransmit

```
Segment 2 lost among 1, 2, 3, 4, 5...

Receiver gets: 1 (in-order) ✓
               3 (out-of-order; ACK=1+5=6, wait for 2)
               4 (out-of-order; ACK=6 again)
               5 (out-of-order; ACK=6 again)

Sender gets: ACK=6, ACK=6, ACK=6
Sender: Waits for RTO (e.g., 200ms) before retransmitting segment 2

Delay: 200ms to detect loss (while receiver is ready for data!)
```

### Solution: 3-Duplicate-ACK Rule

```
RFC 5681: After receiving 3 identical ACKs, assume loss

Sender receives: ACK=6, ACK=6, ACK=6
Action: Immediately retransmit segment with SEQ=6 (don't wait for RTO)

Delay: ~25ms (time to receive 3 ACKs) vs. 200ms+ (timeout)
Speedup: 8-10× faster loss detection
```

## Example: Reliable Transfer

### Scenario

```
Sender: "Hello World"
Receiver: 5-byte buffer

Send:
  SEQ=1000, "Hello" (5 bytes) → [1000, 1005)
  SEQ=1005, "Wor" (3 bytes) → [1005, 1008)
  (stopped; wait for ACK to continue; flow control)

Receive (corrupted scenario):
  Segment 1: Received correctly
    Data: "Hello"
    ACK=1005 (expect byte 1005 next)
    
  Segment 2: Checksum error detected
    → Discarded; receiver state unchanged
    Receiver: Still expecting seq 1005
    
Sender: Sends segment 2 (again):
  SEQ=1005, "Wor" (3 bytes)
  
Receive: Correct this time
  Data: "Wor"
  ACK=1008
  
Result: Data delivered correctly; corruption handled by retransmission.
```

## Loss Detection Summary

| Trigger | Delay | Severity |
|---|---|---|
| 3-duplicate-ACK | ~25ms | Likely loss; not total congestion |
| RTO timeout | 200ms - seconds | Severe congestion; long delay |

**Rationale**:
- Duplicate ACKs: Receiver responding (network not fully congested)
- Timeout: No ACKs (likely severe congestion or crash)

## Recovery and Flow Restart

After retransmission succeeds:

```
Sender: Data successfully retransmitted
Receiver: ACK received
Sender: Resume normal transmission

Congestion control: [[Congestion_Control|TCP Reno]] uses fast recovery
  Don't reset cwnd to 1; maintain higher window
  Gradual recovery
```

## Limitations

### What Reliability Doesn't Guarantee

1. **Immediate delivery**: Data may be delayed indefinitely (no deadline)
2. **Correct ordering at application**: Application must handle message boundaries
3. **Correctness of data**: Reliability ensures delivery, not that data is meaningful
4. **Delivery of commands**: If connection lost before ack, command may execute twice (or not at all)

### [[Exactly_Once_Delivery|Exactly-Once Semantics]]

True at-most-once delivery is guaranteed. At-least-once with deduplication at application level can approximate exactly-once for idempotent operations.

## See Also

- [[Segment_Structure]]: Sequence numbers, ACK numbers, checksums
- [[TCP_Protocol]]: TCP's reliability implementation
- [[Three-Way_Handshake]]: Reliable connection setup
- [[Connection_Release]]: Reliable connection teardown
- [[Congestion_Control]]: Retransmission and loss recovery
- [[The_Two_Army_Problem]]: Theoretical limits of reliability
