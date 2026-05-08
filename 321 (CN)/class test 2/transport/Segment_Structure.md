# Segment Structure

## Definition

A **segment** is the unit of data transmitted by the [[Transport_Layer|Transport Layer]]. It consists of:

1. **Protocol header**: Control information for transport protocol
2. **Payload**: Data from application layer

The term "segment" is used for [[TCP_Protocol|TCP]]; UDP uses the term "datagram" though the structure is analogous.

## Generic Segment Format

| Component | Description |
|-----------|-------------|
| Transport Layer Header | Control information for transport protocol |
| Application Data (Payload) | Data from application layer (variable length, may be empty) |

## UDP Datagram Header

UDP headers are minimal, adding only 8 bytes of overhead.

### Bit-Level Structure

| Bits | Field | Size | Description |
|------|-------|------|-------------|
| 0-15 | Source Port | 16 bits | Port number of sending process |
| 16-31 | Destination Port | 16 bits | Port number of intended receiving process |
| 32-47 | Length | 16 bits | Total length of UDP datagram in octets (bytes) |
| 48-63 | Checksum | 16 bits | One's complement sum of 16-bit words |
| 64+ | Payload | Variable | Application data (variable length) |

### Field Definitions

**Source Port (16 bits)**
- Port number of sending process
- Allows receiver to reply to sender
- For server sockets, typically from well-known port range

**Destination Port (16 bits)**
- Port number of intended receiving process
- Combined with destination IP (from Network Layer header), identifies target socket

**Length (16 bits)**
- Total length of UDP datagram in octets (bytes)
- Minimum: 8 (header only, no payload)
- Maximum: 65535
- Calculated as: header (8 bytes) + payload length

$$\text{Length} = 8 + |\text{payload}|$$

**Checksum (16 bits)**
- One's complement sum of 16-bit words
- Covers: UDP header, payload, and pseudo-header
- Pseudo-header includes: source IP, destination IP, protocol, UDP length
- Value of 0 means checksum not calculated (though this is deprecated)
- Optional in IPv4 (can be 0); mandatory in IPv6

## TCP Segment Header

TCP headers are significantly more complex, minimum 20 bytes (40 bytes with options).

### Bit-Level Structure

| Bits | Field | Size | Description |
|------|-------|------|-------------|
| 0-15 | Source Port | 16 bits | Port number of sending process |
| 16-31 | Destination Port | 16 bits | Port number of receiving process |
| 32-63 | Sequence Number | 32 bits | Identifies this segment's position in the data stream |
| 64-95 | Acknowledgment Number | 32 bits | Specifies next sequence number expected from sender |
| 96-99 | Offset | 4 bits | Length of TCP header in 32-bit words |
| 100-105 | Reserved | 6 bits | Currently unused, must be 0 |
| 106-111 | Flags | 6 bits | Control flags: URG, ACK, PSH, RST, SYN, FIN |
| 112-127 | Window Size | 16 bits | Size of receiver's advertised window for flow control |
| 128-143 | Checksum | 16 bits | One's complement sum of 16-bit words |
| 144-159 | Urgent Pointer | 16 bits | Offset from sequence number to last byte of urgent data |
| 160+ | Options | variable (0-40 bytes) | Variable-length options for specialized functionality |
| - | Payload | variable | Application data (variable length) |

### Field Definitions

**Source Port (16 bits)**
- Same as UDP
- Port of sending process

**Destination Port (16 bits)**
- Same as UDP
- Port of receiving process

**Sequence Number (32 bits)**
- Identifies this segment's position in the data stream
- First byte of this segment's payload has this sequence number
- For control segments (SYN, FIN): assigned initial value per [[Three-Way_Handshake|three-way handshake]]
- Prevents duplicate/reordered segments from being delivered twice
- Allows receiver to detect missing data

**Definition**: If segment contains $n$ bytes of data:
- Segment occupies sequence numbers: [sequence_number, sequence_number + n)
- Next segment should start at sequence_number + n

**Example**:

| Segment | Sequence Number | Data | Data Length | Sequence Range Occupied |
|---------|-----------------|------|-------------|--------------------------|
| 1 | 1000 | "Hello" | 5 bytes | [1000, 1005) |
| 2 | 1005 | "World" | 5 bytes | [1005, 1010) |
| 3 | 1010 | "!!!" | 3 bytes | [1010, 1013) |

**Acknowledgment Number (32 bits)**
- Specifies next sequence number expected from sender
- Only valid if ACK flag is set
- Implicitly acknowledges all data up to (but not including) this number

**Semantics**:
$$\text{ACK number} = \text{last correctly received sequence} + 1$$

If receiver has received bytes [1000, 1010) correctly, ACK number = 1010.

This acknowledges all data up through byte 1009 and indicates byte 1010 is expected next.

**Offset (4 bits)**
- Length of TCP header in 32-bit words
- Valid range: 5–15 (20–60 bytes)
- Offset = 5 means 20 bytes (minimum, no options)
- Offset = 7 means 28 bytes (with 8 bytes of options)

$$\text{Header length} = \text{Offset} \times 4 \text{ bytes}$$

**Reserved (6 bits)**
- Currently unused
- Must be 0; ignored by receivers
- Reserved for future use

**Flags (6 bits)**
- Single-bit control flags indicating segment purpose

| Bit Position | Flag | Name | Purpose |
|--------------|------|------|---------|
| 106 | U | URG | Urgent Pointer field is valid; urgent data present |
| 107 | A | ACK | Acknowledgment Number field is valid |
| 108 | P | PSH | Push data to application immediately; don't wait for buffer |
| 109 | R | RST | Reset connection; abrupt termination |
| 110 | S | SYN | Synchronize sequence numbers; used in connection setup |
| 111 | F | FIN | Finished; sender has no more data; request close |

**Flag combinations**:
- SYN: Connection setup (no data typically)
- SYN-ACK: Server acknowledges setup
- ACK: Confirms receipt of data; most segments have this
- FIN: Graceful close (may contain final data)
- RST: Abrupt close; connection state discarded
- PSH-ACK: Data with immediate delivery request

**Window Size (16 bits)**
- Size of receiver's advertised window for [[Flow_Control_Mechanisms|flow control]]
- Tells sender how many more bytes can be received
- Measured in bytes
- Allows dynamic adjustment of transmission rate

**Interpretation**:
$$\text{Maximum bytes} \text{ in flight} = \text{Window Size}$$

A receiver with a small buffer can reduce window size to slow sender.

**Checksum (16 bits)**
- One's complement sum of 16-bit words
- Covers: TCP header, payload, and pseudo-header
- Pseudo-header includes: source IP, destination IP, protocol (6 for TCP), TCP length
- Mandatory; cannot be 0
- Detects bit errors from corruption or bit flips

**Urgent Pointer (16 bits)**
- Only valid if URG flag is set
- Specifies offset (in bytes) from sequence number to last byte of urgent data
- Allows embedding high-priority data within normal stream

**Usage example**:

| Parameter | Value | Description |
|-----------|-------|-------------|
| Sequence Number | 1000 | Starting sequence number of the segment |
| Urgent Pointer | 50 | Offset from sequence number |
| Urgent Data Range | [1000, 1049] | Bytes marked as urgent |
| Normal Data Starts | 1050 | First byte of normal priority data |

Mechanism for sending control signals without waiting for send buffer to drain.

**Options (variable length, 0–40 bytes)**
- Variable-length options for specialized functionality
- Must be multiple of 4 bytes; padded with NOP (no-op) if needed

#### Common TCP Options

**Maximum Segment Size (MSS)**
- Specifies largest segment this host can receive
- Communicated during connection setup
- Typical value: 1460 bytes (1500 byte Ethernet frame − 40 bytes headers)
- Prevents fragmentation

**Window Scaling**
- Extends 16-bit window to 32-bit value
- Necessary for high-bandwidth, long-delay connections (gigabit networks)
- Shift factor multiplied with window size

**Selective Acknowledgment (SACK)**
- Allows receiver to acknowledge non-contiguous ranges
- Reduces retransmissions when packets arrive out of order
- Indicates: "I received this, this, and this, but this is missing"

**Timestamps**
- Carries 32-bit timestamp from sender and 32-bit echo from receiver
- Used for: Round-Trip Time (RTT) measurement, protection against wrapped sequence numbers

## Segment Encapsulation and Decapsulation

### Encapsulation (Downward)

**Application layer**:
- Application data: "GET / HTTP/1.1\r\n..."

**Transport layer** (TCP):
- Adds TCP header with:
  - Source/destination ports
  - Sequence number
  - Flags (PSH, ACK)
  - Checksum
- Result: TCP Segment

**Network layer** (IP):
- Adds IP header with:
  - Source/destination IP addresses
  - Protocol field = 6 (TCP)
- Result: IP Packet

**Link layer** (Ethernet):
- Adds Ethernet header with:
  - Source/destination MAC addresses
- Result: Ethernet Frame

**Final structure on wire**:

| Layer | Component | Description |
|-------|-----------|-------------|
| Link | Ethernet Header | Source/destination MAC addresses |
| Network | IP Header | Source/destination IP addresses, Protocol field = 6 (TCP) |
| Transport | TCP Header | Source/destination ports, sequence number, flags, checksum |
| Application | Application Data | Original data: "GET / HTTP/1.1\r\n..." |
| Link | Ethernet Trailer | Error detection/correction data |

### Decapsulation (Upward)

**Processing each layer in reverse order**:

| Layer | Action | Processing |
|-------|--------|------------|
| Link | Remove Ethernet header | Check destination MAC address |
| Network | Remove IP header | Check destination IP address |
| Transport | Remove TCP header | Check destination port, validate checksum |
| Application | Extract payload | Deliver data to application process |

## Segment Size Constraints

### Maximum Segment Size (MSS)

Limited by network characteristics:

**IP-level limit**:
- IPv4 maximum packet size: 65535 bytes total
- TCP header: 20–60 bytes
- Maximum TCP payload: ≈65475 bytes
- Rarely used; typically fragmented at 1500 bytes

**Path MTU Discovery**:
- Determines maximum unfragmented packet size on route
- Typical: 1500 bytes (Ethernet)
- TCP typically limits segments to 1460 bytes (1500 − 40 bytes headers)

### Segment Timing

Segments are sent:
1. When buffer has MSS bytes
2. When application calls SEND and sets push flag
3. When retransmission timer expires
4. When [[Flow_Control_Mechanisms|flow control]] window becomes available

Not necessarily immediately after application calls SEND.

## Significance of Segment Structure

The header fields enable:

1. **Delivery**: Source/destination ports direct segments to correct processes
2. **Ordering**: Sequence numbers allow receiver to reorder out-of-order arrivals
3. **Reliability**: ACK numbers and checksums detect loss and corruption
4. **Flow control**: Window size regulates transmission rate
5. **Connection management**: Flags (SYN, FIN, RST) control connection lifecycle
6. **Priority**: URG flag for urgent data

## See Also

- [[Port_and_Addressing]]: How ports are used in headers
- [[TCP_Protocol]]: Detailed TCP segment processing
- [[UDP_Protocol]]: UDP segment format
- [[Reliability_Mechanisms]]: How sequence/ACK numbers ensure reliability
- [[Flow_Control_Mechanisms]]: Window size role in flow control
