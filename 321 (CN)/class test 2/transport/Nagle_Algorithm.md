# Nagle's Algorithm

## Purpose

**Nagle's Algorithm** solves the **Silly Window Syndrome** by reducing the number of small segments sent, particularly beneficial for interactive applications like Telnet.

## Problem

### Without Nagle

```
Telnet user types characters; each character is 1 byte

Application: SEND(char)
TCP: Immediately send 1-byte segment
Network sees: [40-byte header | 1-byte data]
Overhead: 40:1 header-to-data ratio

User types at 10 characters/second:
  10 segments/sec
  40 bytes header × 10 = 400 bytes header overhead
  vs. 10 bytes data
  
Network wastes 98% bandwidth on headers!
```

## Algorithm

**Rule**: Don't send a segment unless:

1. Have ≥ MSS (Maximum Segment Size) bytes accumulated, OR
2. All previously sent data has been ACK'd (pipe is empty)

### Pseudocode

```python
def send_with_nagle(data):
    append_to_send_buffer(data)
    
    if len(send_buffer) >= MSS:
        # Enough data; send immediately
        send_segment(send_buffer)
        clear(send_buffer)
    
    elif all_previous_data_acked():
        # Previous data acknowledged; send buffer even if < MSS
        send_segment(send_buffer)
        clear(send_buffer)
    
    else:
        # Have data < MSS and previous data still outstanding
        # Wait for either: (1) more data, (2) ACK of previous
        # Don't send; buffer accumulates
```

## Effect

### Telnet Scenario

```
User: Types 'H'
  SEND('H')
  send_buffer = 'H' (1 byte)
  previous_data_acked = true
  Action: Send segment with 'H'

User: Types 'e' (within RTT of previous)
  SEND('e')
  send_buffer = 'e' (1 byte)
  previous_data_acked = false (ACK for 'H' hasn't arrived)
  Action: Buffer; don't send

User: Types 'l'
  SEND('l')
  send_buffer = 'el' (2 bytes)
  Action: Still buffer

User: Types 'l'
  SEND('l')
  send_buffer = 'ell' (3 bytes)
  Action: Still buffer

ACK arrives: Acknowledges 'H'
  previous_data_acked = true
  send_buffer = 'ell' (3 bytes)
  Action: Send 'ell' segment

Result: 
  Without Nagle: 4 segments for 'Hell' (H, e, l, l)
  With Nagle: 2 segments for 'Hell' (H, ell)
  Reduction: 50% fewer segments
```

## Trade-offs

### Enabled (Default)

**Advantages**:
- Reduced segment count
- Reduced network congestion
- Better for bulk data
- Better for streaming

**Disadvantages**:
- Added latency: User sees characters appear later
- Not ideal for interactive applications
- Unpredictable RTT increases per keystroke

### Disabled

**Advantages**:
- Immediate transmission
- Low latency (no wait for ACK)
- Interactive applications (SSH, Telnet) feel responsive

**Disadvantages**:
- More segments on network
- Higher bandwidth usage for small messages
- Silly Window Syndrome risk

## Configuration

### Enable/Disable in Code

**Disable** (for interactive apps):
```python
socket.setsockopt(TCP_NODELAY, 1)
```

**Enable** (default):
```python
socket.setsockopt(TCP_NODELAY, 0)
```

### When to Disable

- **SSH, Telnet**: Interactive; low latency critical
- **Online games**: Real-time; responsive input important
- **Editors**: Character-by-character input
- **Remote procedure calls**: Expect fast response

### When to Keep Enabled

- **Web browsing (HTTP)**: Bulk data; buffering transparent
- **File transfer (FTP)**: Throughput > latency
- **Streaming**: Continuous data; buffering OK
- **Bulk database queries**: Large responses; buffering irrelevant

## Interaction with Other Mechanisms

### With [[Flow_Control_Mechanisms|Flow Control]]

```
Receiver window limits sending:
  Nagle: Don't send < MSS unless all ACK'd
  Flow control: Can only send if window > 0
  
Both constraints must be satisfied.
```

### With [[TCP_Protocol|Delayed ACK]]

```
Receiver delays ACK (e.g., 40 ms or next segment)
Sender with Nagle: Waits for ACK to send buffered data
Result: Interaction may cause latency issues
  Nagle waits for ACK
  Delayed ACK delays ~40 ms
  Total: ~40 ms latency per segment
  
Mitigation: Disable TCP_NODELAY for interactive apps
            Combine with TCP_QUICKACK to reduce ACK delay
```

## Effectiveness

### Measurements

Empirical studies (from RFC 896):

```
Telnet traffic without Nagle:
  10% of packets are minimum-size (1-40 bytes)
  Contributes 33% of traffic volume

With Nagle:
  Minimum-size packets: 2% of packets
  Reduced traffic significantly
  
Result: Better network utilization
         Interactive feel: Imperceptible to users
```

## Historical Context

**Nagle's Algorithm** (1984) published in RFC 896 to address pathological behavior observed in early Internets.

**Real-world impact**: Solved tangible problem; widely adopted.

**Modern context**: Less critical due to higher bandwidths, but principle remains valid.

## See Also

- [[Silly_Window_Syndrome]]: Problem Nagle solves
- [[Clark_Solution]]: Receiver-side counterpart
- [[Flow_Control_Mechanisms]]: Complementary mechanism
- [[TCP_Protocol]]: TCP implementation
- [[Service_Primitives]]: SEND behavior
