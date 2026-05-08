# IP Fragmentation

## Definition and Motivation

IP fragmentation is the process of breaking a large IP datagram into smaller fragments that fit within the Maximum Transmission Unit (MTU) of a network link, then reassembling the fragments at the destination. Fragmentation occurs when a packet is too large for a link in its path.

### Maximum Transmission Unit (MTU)

The MTU is the maximum size (in bytes) of a frame that can be transmitted over a link without fragmentation. Common MTU values:

| Link Type | MTU (bytes) |
|---|---|
| Ethernet | 1500 |
| PPP (Point-to-Point Protocol) | 296-4096 (configurable) |
| ATM | 53 (cells, requires special handling) |
| Satellite | 1024-8192 |
| IP minimum | 68 |

### Problem Statement

When a router receives an IP packet larger than the outgoing link's MTU, it must either:
1. Fragment the packet into smaller pieces.
2. Drop the packet and send an ICMP error message.

IPv4 supports fragmentation at routers. IPv6 does not; only the source can fragment, and routers must drop oversized packets.

## IPv4 Fragmentation

### IP Header Fields for Fragmentation

Three fields in the IPv4 header enable fragmentation:

**Identification (ID)**: 16-bit field identifying a group of fragments.
- All fragments from the same original packet share the same ID.
- Allows reassembly to distinguish fragments from different packets.

**Flags**: 3-bit field.
- **DF (Don't Fragment)**: If set, packet should not be fragmented; drop if too large.
- **MF (More Fragments)**: If set, more fragments follow; if clear, this is the last fragment.
- **Reserved**: Always 0.

**Fragment Offset**: 13-bit field indicating the position of the fragment's data within the original datagram.
- Measured in 8-byte units (64 bits).
- Allows fragments to be reassembled in correct order even if they arrive out of order.

### Fragmentation Process

When a router receives a packet larger than the outgoing MTU:

```
Let:
  L_orig = original packet length
  MTU = outgoing link's MTU
  H = IP header length (typically 20 bytes)
  F = fragment size = floor((MTU - H) / 8) × 8  // must be multiple of 8

For each fragment i:
  offset(i) = (i - 1) × F / 8
  length(i) = min(F, L_orig - H - offset(i) × 8)
  MF_flag(i) = 1 if (offset(i) × 8 + length(i) < L_orig - H); else 0
  
  Create fragment:
    [IP Header] {modified}:
      Total Length = H + length(i)
      More Fragments = MF_flag(i)
      Fragment Offset = offset(i)
      Identification = (original packet's ID)
    [Payload (length(i) bytes)]
```

### Example: Fragmentation of a 3000-byte Datagram

**Original Datagram**:
- Total Length: 3000 bytes (20 byte header + 2980 bytes payload).
- Identification: 12345.
- Flags: DF = 0, MF = 0.

**Outgoing Link MTU**: 1500 bytes.

**Fragment Size Calculation**:
$$F = \left\lfloor \frac{1500 - 20}{8} \right\rfloor \times 8 = \lfloor 185 \rfloor \times 8 = 1480 \text{ bytes}$$

**Fragments**:

| Fragment | Offset (bytes) | Data Length | Total Length | MF | Offset Field |
|---|---|---|---|---|---|
| 1 | 0 | 1480 | 1500 | 1 | 0 |
| 2 | 1480 | 1480 | 1500 | 1 | 185 |
| 3 | 2960 | 20 | 40 | 0 | 370 |

**Fragment Headers**:

Fragment 1:
```
[IP Header]
  Total Length: 1500
  Identification: 12345
  Flags: DF=0, MF=1
  Fragment Offset: 0
[Payload: 1480 bytes]
```

Fragment 2:
```
[IP Header]
  Total Length: 1500
  Identification: 12345
  Flags: DF=0, MF=1
  Fragment Offset: 185  // 1480 / 8
[Payload: 1480 bytes]
```

Fragment 3:
```
[IP Header]
  Total Length: 40  // 20 (header) + 20 (remaining payload)
  Identification: 12345
  Flags: DF=0, MF=0  // last fragment
  Fragment Offset: 370  // 2960 / 8
[Payload: 20 bytes]
```

### Reassembly at Destination

When fragments arrive at the destination (or an intermediate router performing reassembly):

```
Reassembly Buffer:
  Indexed by (source, destination, identification)
  Stores: Fragment offset, length, data
  
Algorithm:
  1. Upon fragment arrival, check if reassembly buffer exists for (src, dst, id).
  2. If not, create new buffer and start a reassembly timer (typically 15-30 seconds).
  3. Insert fragment data at correct offset in buffer.
  4. Check if all fragments have arrived:
     a. Lowest offset must be 0.
     b. For each fragment, next fragment's offset = current offset + current length.
     c. Last fragment must have MF = 0.
  5. If all fragments received, reassemble into original packet and forward.
  6. If timer expires before reassembly completes, discard partial buffer and drop reassembled packets.
```

### Fragment Overlap and Out-of-Order Arrival

Fragments may arrive out of order or with overlapping ranges (a malicious or buggy sender).

**RFC 791 (IPv4)** specifies that overlapping fragments should be handled by:
- Keeping the first fragment received for overlapping ranges.
- Or some implementations keep the last fragment received (implementation-dependent).

This ambiguity can lead to security vulnerabilities (see RFC 5722 for "Handling of Out-of-order Fragments").

## Don't Fragment (DF) Flag and Path MTU Discovery

### DF Flag

If the DF flag is set in the original packet, the packet must not be fragmented. If a router cannot forward the packet without fragmentation, it must:

1. Drop the packet.
2. Send an ICMP Destination Unreachable message (code = 4, "Fragmentation Needed but DF Set") with the MTU of the next hop.

### Path MTU Discovery (PMTUD)

PMTUD uses the DF flag to discover the maximum MTU along a path.

**Algorithm**:
```
1. Source sets DF = 1 in packets.
2. Start with optimistic MTU (e.g., 1500 bytes).
3. Send packet with DF = 1.
4. If ICMP "Fragmentation Needed" received:
     a. Extract MTU from ICMP message.
     b. Update path MTU = min(current_path_MTU, extracted_MTU).
     c. Reduce packet size.
     d. Resend.
5. If packet delivered successfully, path MTU is at least current packet size.
6. Periodically probe with larger packets to detect MTU changes.
```

**Advantage**: Avoids fragmentation at intermediate routers; reduces processing overhead.

**Limitation**: Black-hole problem. If ICMP messages are filtered (by firewalls), the source never learns the MTU and packets are silently dropped. Modern implementations use various heuristics to detect and handle black-hole MTU scenarios.

## IPv6 Fragmentation

IPv6 does not support fragmentation at routers; only the source can fragment.

### Implications

1. **Source Responsibility**: The source host is responsible for determining the MTU and fragmenting if necessary.
2. **Router Simplicity**: Routers do not perform fragmentation; they simply drop oversized packets and send ICMPv6 "Packet Too Big" message.
3. **Performance**: Avoids fragmentation overhead at routers; improves router throughput.
4. **Host Complexity**: Hosts must implement PMTUD properly.

### Fragmentation in IPv6

IPv6 uses a **Fragment Extension Header** (next header type = 44) instead of fragmentation in the main header.

**Fragment Extension Header**:
```
Next Header (8 bits)
Reserved (8 bits)
Fragment Offset (13 bits) | Res (2 bits) | M Flag (1 bit)
Identification (32 bits)
[Optional: Additional headers]
[Payload]
```

### IPv6 PMTUD

IPv6 relies on PMTUD to avoid fragmentation. If ICMPv6 "Packet Too Big" messages are not received, fragmentation happens at the source (if supported by the OS).

## Performance Impact of Fragmentation

### Processor Overhead

**Fragmentation**:
- Router must compute fragment sizes, offsets, and checksums.
- Significant processing for large packets.

**Reassembly**:
- Destination must reconstruct original packet.
- Reassembly buffer must be managed.
- Out-of-order arrival handling increases complexity.

### Bandwidth Overhead

If fragmentation is required, the aggregate bandwidth used increases due to:

**Duplicate Headers**: Each fragment carries a full IP header.

Example: 3000-byte packet fragmented into 3 fragments.
- Original: 1 header + payload.
- Fragmented: 3 headers + payload.
- Additional overhead: 2 × 20 bytes = 40 bytes (1.33% increase).

For very small fragments, overhead is higher.

### Packet Loss Impact

If one fragment is lost:
- Entire original packet must be retransmitted.
- In networks with high loss, fragmented packets are more likely to lose at least one fragment.

**Example**: 
- Packet loss rate: 1% per fragment.
- Unfragmented packet: 1% loss.
- Fragmented into 3 fragments: $1 - (0.99)^3 \approx 2.97\%$ loss.

Loss increases exponentially with fragment count.

## Fragmentation Security Issues

### Fragment Overlap Attacks

A malicious sender can send overlapping fragments with conflicting data. Depending on how reassembly is implemented, the destination may accept either the first or last fragment's data. This can cause:
- Firewall bypass: Fragmented packets may pass through firewall rules if the firewall checks only the first fragment.
- Packet injection: Attacker inserts malicious data in later fragments.

**Mitigation**: RFC 5722 recommends discarding overlapping fragments.

### Tiny Fragment Attacks

Small initial fragment (with just the IP header and a tiny amount of data) followed by larger subsequent fragments. This can trick firewalls that inspect only the first fragment.

**Mitigation**: Enforce minimum fragment size.

## Best Practices

1. **Avoid Fragmentation**: Use PMTUD to determine MTU; send packets that fit.
2. **DF Flag**: Set DF = 1 for applications that can handle the error response.
3. **Buffer Management**: Implement reassembly buffers with size limits and timeout.
4. **Security**: Discard overlapping fragments; enforce minimum fragment size.
5. **IPv6 Preference**: When possible, use IPv6 to avoid router-level fragmentation overhead.

## Related Concepts

- [[Tunneling_and_VPN]]: Tunneling adds overhead, reducing available space for payload, increasing fragmentation likelihood.
- [[ICMP_Protocol]]: ICMP "Destination Unreachable" and "Packet Too Big" messages used for fragmentation feedback.
- [[IP_Addressing_Review]]: IP header structure and fields.

---

**Next:** [[ICMP_Protocol]]
