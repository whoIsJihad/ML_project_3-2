# OSI Model — Detailed Explanation with Concrete Examples

**Date:** 2025-12-27

**Purpose:** Beginner-friendly, step-by-step walk-through of the seven OSI layers with concrete examples showing how a single message (HTTP GET) is represented at each layer: application message → transport segment → IP packet → Ethernet frame → physical bits.

---

## Table of contents
- Overview
- Example scenario (end-to-end)
- Layer walkthrough (Application → Physical)
- Encapsulation summary (quick)
- Extra examples (UDP/DNS, ARP, TLS)
- Common confusions (Q&A)
- Next steps (hex dump, diagram, quiz)

---

## Overview

- The OSI model is a conceptual teaching model with seven layers. In real-world Internet stacks (TCP/IP) the top three OSI layers are usually folded into a single Application layer.
- This document uses a running example (HTTP GET) and shows the exact form of data at each step to make the model concrete for beginners.

---

## Example scenario (end-to-end)

- Client issues an HTTP GET for `/index.html` on `example.com`.
- Transport: TCP (reliable, connection-oriented). Example ports: src=54321 → dst=80.
- Network: IPv4 addresses: src=192.0.2.10 → dst=93.184.216.34.
- Link: Ethernet frames carry IP packets across the local network (example MACs used below).

---

## Layer walkthrough (with concrete examples)

Below each layer: Responsibilities, a short explanation, then a concrete example showing the exact bytes or fields the layer adds or uses.

### 1) Application (OSI Layer 7)

- Responsibilities: End-user services and application protocols (HTTP, SMTP, DNS, FTP, SSH). Produces the actual message content.
- Common protocols: `HTTP`, `HTTPS`, `SMTP`, `DNS`, `FTP`, `SSH`.
- Data unit: Application Protocol Data Unit (APDU) — usually called "message" or "payload".

Concrete HTTP request (exact text sent by the browser):

```http
GET /index.html HTTP/1.1\r\n
Host: example.com\r\n
User-Agent: ExampleClient/1.0\r\n
\r\n
```

- This ASCII block is the application payload. It contains headers and optional body. At this stage there are no transport or network headers.

### 2) Presentation (OSI Layer 6)

- Responsibilities: Data representation (encoding), compression, encryption. In practice these are often performed by libraries or application-layer protocols (e.g., TLS, gzip).

Concrete effects:
- If content is compressed (gzip) or encrypted (TLS), the application payload becomes binary compressed/encrypted bytes. Those bytes are then passed unchanged to the transport layer.

> Note: You usually do not see a separate "presentation" header in packet captures; the bytes are modified in place.

### 3) Session (OSI Layer 5)

- Responsibilities: Dialog control, session state, synchronization and recovery.

Concrete example:
- An HTTP session token (cookie) or an application-level session ID lives in the application payload. There is typically no separate network header for session state in modern stacks.

### 4) Transport (OSI Layer 4)

- Responsibilities: End-to-end delivery, segmentation/reassembly, reliability, flow control, and multiplexing via ports.
- Protocols: `TCP` (reliable) and `UDP` (unreliable).
- Data unit: TCP *segment* or UDP *datagram*.

Concrete TCP segment (simplified):

- Source port: `54321`
- Destination port: `80`
- Sequence number: `1001` (example)
- Flags: `SYN`, `ACK`, `PSH` (depending on state)
- Payload: the HTTP request bytes shown above

Conceptual layout:

```
[ TCP Header (e.g. 20 bytes) ] | [ HTTP request bytes ]
```

Example UDP (DNS query):

- Src port: `12345`, Dst port: `53`, Payload: raw DNS query bytes.

> Tip: Wireshark labels these as "TCP segment" or "UDP datagram" and shows header fields for each.

### 5) Network (OSI Layer 3)

- Responsibilities: Logical addressing and routing (IP addresses), fragmentation, TTL.
- Protocols: `IPv4`, `IPv6`, `ICMP`.
- Data unit: IP packet.

Concrete IPv4 header (simplified fields):

- Version: `4`
- Header length: `20` bytes (no options)
- Total length: (IP header + transport header + payload)
- Protocol: `6` (TCP)
- TTL: `64`
- Source IP: `192.0.2.10`
- Destination IP: `93.184.216.34`
- Payload: the entire TCP segment

Conceptual layout:

```
[ IPv4 Header ] | [ TCP Header ] | [ HTTP bytes ]
```

> Routers inspect the IP header (source/destination IP + TTL) to route packets across networks.

### 6) Data Link (OSI Layer 2)

- Responsibilities: Framing, MAC addressing, link access, error detection (CRC).
- Protocols: `Ethernet (802.3)`, `802.11 (Wi‑Fi)`, `PPP`.
- Data unit: Frame (e.g., Ethernet frame).

Concrete Ethernet II frame (simplified):

- Destination MAC: `aa:bb:cc:dd:ee:ff`
- Source MAC: `11:22:33:44:55:66`
- Ethertype: `0x0800` (IPv4)
- Payload: the IP packet
- FCS: 4-byte CRC at end

Layout:

```
[ Dst MAC (6) | Src MAC (6) | Ethertype (2) | IP packet (var) | FCS (4) ]
```

> Switches forward frames using MAC addresses. Wireless uses different link-layer fields (802.11).

### 7) Physical (OSI Layer 1)

- Responsibilities: Raw transmission of bits/signals on the medium: electrical voltages, light pulses, RF symbols, bit timing and encoding.
- Data unit: Bits (or symbols).

Concrete binary for ASCII "GET":

```
G -> 0x47 -> 01000111
E -> 0x45 -> 01000101
T -> 0x54 -> 01010100

Raw bits (start): 01000111 01000101 01010100 ...
```

These bits are encoded onto the medium using a physical code (NRZ, Manchester, MLT-3, PAM, etc.).

> Hardware (NIC, PHY) handles modulation and timing; physical impairments cause bit errors that the data link CRC can detect.

---

## Encapsulation summary (quick)

```
Application payload (HTTP request)
→ TCP segment (TCP header + payload)
→ IP packet (IP header + TCP segment)
→ Ethernet frame (Ethernet header + IP packet + FCS)
→ Physical bits/signals on the medium
```

Example label stack:

```
[Ethernet Frame: DstMAC|SrcMAC|0x0800| [IP Packet: SrcIP|DstIP|Protocol=TCP | [TCP Segment: SrcPort|DstPort|Seq|ACK | HTTP bytes ] ] | FCS ]
```

---

## Extra examples & notes

- UDP (DNS): Application: DNS query → UDP datagram (src port 54321 → dst 53) → IP packet → Ethernet frame → bits.
- ARP: Runs between Network and Data Link. ARP requests are encapsulated directly in Ethernet frames with Ethertype `0x0806` and are used to map IP → MAC on a local link.
- TLS/HTTPS: Encryption happens at the application/presentation layer. After TLS the transport payload contains encrypted bytes; network/link layers cannot read the contents.

---

## Common beginner confusions (short answers)

- "Is the application message turned into a packet?" — The application message becomes the payload of a transport segment, which becomes the payload of an IP packet, which becomes the payload of a frame. Each layer adds its own header (and sometimes footer).
- "Where is routing done?" — Routers forward based on the IP (network) header, not on transport ports or application data (unless DPI is used).
- "Where are Presentation/Session layers?" — Their responsibilities exist but are usually implemented inside applications or libraries (e.g., TLS, codecs) rather than as separate OSI-layer components in the TCP/IP stack.

---

