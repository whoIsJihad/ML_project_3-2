# 2. Framing Mechanics

> **[[00_DLL_Index|← Back to Index]]**

## The Framing Problem

**Challenge**: The physical layer delivers a continuous bitstream with no boundaries. How does the receiver know where one frame ends and another begins?

```
Continuous bitstream (no boundaries):
01101011 01001011 10101010 11100011 10010101 ...

Frame 1         Frame 2         Frame 3
   |              |                |
   ?              ?                ?
```

Three approaches exist, each with tradeoffs:

1. **Character Count Framing**: Header specifies frame length
2. **Byte Stuffing**: Special FLAG bytes mark boundaries
3. **Bit Stuffing**: Special bit patterns mark boundaries

---

## Approach 1: Character Count Framing

### Structure

```
+---------------+---------------+
| Frame Count   | Payload       |
| (n bytes)     | (n bytes)     |
+---------------+---------------+
```

The **frame count field** in the header specifies how many bytes follow. Example:

```
Header: 0x08        Payload
        ↓           ↓
    00001000  11010110 01100101 10101010 11001100 ...
    (8 bytes) (counting: 1    2    3    4    5    6    7    8)
              ├───────────────────────────────────────────┤
              Frame ends here; next count field starts
```

### Critical Vulnerability: Single-Bit Error in Count

**Scenario**: Count field is corrupted

```
Sent:     Frame Count = 5     Payload: ABCDE FGH...
          00000101             (correct: 5 bytes follow)

Corrupted:Frame Count = 3     Payload: ABCDE FGH...
          00000011             (error: only 3 bytes follow)

Receiver interprets:
  Bytes 1-3: A B C (correct)
  Bytes 4-5: D E    (misinterpreted as count field for next frame!)
  
Complete loss of synchronization downstream ✗
```

### Why This Fails

- **Single point of failure**: One bit error in the count field cascades to all subsequent frames
- **No recovery**: Once sync is lost, receiver cannot resynchronize without external intervention
- **Practical use**: Rarely used alone in modern systems (too fragile)

**Lesson**: Length-based framing requires either extremely reliable transmission or must be paired with additional synchronization mechanisms.

---

## Approach 2: Byte Stuffing

### Concept

Use special **control bytes** to mark frame boundaries:
- **FLAG**: Marks start and end of frame (e.g., `0x7E`)
- **ESC**: Escapes control bytes if they appear in the payload

```
Frame structure:

+--------+--------+---------+---------+--------+
|  FLAG  | Header | Payload | Trailer |  FLAG  |
+--------+--------+---------+---------+--------+
```

### Standard Byte Values

```
FLAG = 0x7E  (01111110 in binary)
ESC  = 0x7D  (01111101 in binary)
```

### Transmission Rules

**Rule 1**: Every transmitted FLAG is a frame boundary

**Rule 2**: If FLAG or ESC appears in the payload, **escape it**:

```
Payload contains:     0x7E (FLAG)
Transmitted as:       ESC + (0x7E XOR 0x20)
                      0x7D + 0x5E

Payload contains:     0x7D (ESC)
Transmitted as:       ESC + (0x7D XOR 0x20)
                      0x7D + 0x5D
```

The XOR mask (0x20) flips bit 5, making the escaped byte **never equal** to FLAG or ESC.

### Example: Transmission with Byte Stuffing

**Original payload** (hex):
```
48 65 6C 6C 6F 7E 21
(H  e  l  l  o [FLAG] !)
```

**Transmitted frame** (with escaping):
```
FLAG | Header | Payload with stuffing      | Trailer | FLAG
0x7E |  ...   | 48 65 6C 6C 6F 7D 5E 21   |  ...    | 0x7E
                      ↑ ESC inserted      ↑ original 0x7E replaced
```

### Reception Rules

**Algorithm**:
```
while receiving:
  if byte == FLAG:
    frame_complete()
  else if byte == ESC:
    next_byte = read()
    payload += (next_byte XOR 0x20)  // Unescape
  else:
    payload += byte
```

### Recovery Properties

- **Self-synchronizing**: Receiving a FLAG byte instantly re-synchronizes the receiver
- **Burst error tolerance**: Loss of entire frames is recoverable; next FLAG found quickly
- **Overhead**: Variable, depends on payload content (worst case: every byte is 0x7E or 0x7D)

### Worst-Case Overhead Example

**Payload of all FLAGs**:
```
Original:  0x7E 0x7E 0x7E 0x7E (4 bytes)
Stuffed:   0x7D 0x5E 0x7D 0x5E 0x7D 0x5E 0x7D 0x5E (8 bytes)
Overhead:  100%
```

---

## Approach 3: Bit Stuffing

### Concept

Use a specific **bit pattern** as the frame boundary signal:

```
FLAG pattern: 01111110 (six consecutive 1s surrounded by 0s)
```

### Transmission Rule (Sender)

**Rule**: After transmitting five consecutive 1s in the payload, **insert a 0**.

```
Payload:     0 1 1 1 1 1 0 0 1 0 1 1 1 1 1 1 0
             ↑           ↑                   ↑ Five 1s → insert 0
             No action   Five 1s → insert 0
```

Transmitted:
```
0 1 1 1 1 1 0 0 0 1 0 1 1 1 1 1 0 0
            ↑ Inserted        ↑ Inserted
```

### Reception Rule (Receiver)

**Rule**: After seeing five consecutive 1s, remove the next 0 (if it exists).

```
Received bits: 0 1 1 1 1 1 0 0 0 1 0 1 1 1 1 1 0 0
                          ↑ Remove        ↑ Remove
```

Recovered payload:
```
0 1 1 1 1 1 0 0 1 0 1 1 1 1 1 0
```

### Why This Works for Frame Detection

The only way to get **six consecutive 1s** (without an inserted 0) is from the frame boundary:

```
Frame structure:
    Frame 1            FLAG           Frame 2
   ...01111110     01111110       01111110...
        ↑                              ↑
        Not six 1s alone              Six 1s = FLAG detected!
```

### Advantage: No Payload Restriction

Unlike byte stuffing, **any bit pattern is allowed** in the payload. The algorithm guarantees that 01111110 cannot occur naturally.

### Overhead Analysis

**Worst-case payload**: Stream of all 1s

```
Payload:  1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
Stuffed:  1 1 1 1 1 0 1 1 1 1 1 0 1 1 1 1 1 0

Inserted 0: every 5 bits
Overhead: 1/5 = 20%
```

Compare to byte stuffing (100% in worst case). Bit stuffing is more efficient.

### Implementation Consideration

Bit stuffing requires **bitwise transmission and reception** — more complex than byte-oriented I/O but essential for efficiency on long-distance or high-speed links.

---

## Comparison Table

| Property | Character Count | Byte Stuffing | Bit Stuffing |
|----------|---|---|---|
| **Resynchronization** | Manual intervention | Automatic (on FLAG) | Automatic (on 01111110) |
| **Payload restriction** | None | FLAG, ESC must be escaped | None |
| **Worst-case overhead** | None (if count correct) | 100% | 20% |
| **Implementation** | Byte-level | Byte-level | Bit-level |
| **Error tolerance** | Single count error = disaster | Good (self-sync) | Good (self-sync) |
| **Modern usage** | Frame relay, some protocols | Legacy (PPP, HDLC) | Newer protocols, LANs |

---

## Interaction with Error Detection

[[03_Error_Detection_Correction|Error detection]] (e.g., CRC) is typically added to the frame trailer **after** framing:

```
Transmitted frame:

+--------+--------+---------+-----+--------+
|  FLAG  | Header | Payload | CRC |  FLAG  |
+--------+--------+---------+-----+--------+
```

If CRC detects an error, the entire frame is discarded. [[04_Evolution_DLL_Protocols|Higher-layer protocols]] request retransmission via sequence numbers and timeouts.

---

## Key Takeaways

1. **Character count framing** is fragile: one bit error in the length field breaks all downstream synchronization
2. **Byte stuffing** self-synchronizes on FLAG boundaries; overhead depends on payload content
3. **Bit stuffing** is more efficient (max 20% overhead) but requires bit-level processing
4. **Self-synchronization** is critical for recovery from burst errors
5. Modern systems often combine **multiple techniques**: framing + error detection + sequence numbers

---

> **Next**: [[03_Error_Detection_Correction|3. Error Detection & Correction]] — How do we detect and correct transmission errors?

