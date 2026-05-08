---
title: "Transport Layer Core Notes"
geometry: margin=0.5in
fontsize: 10pt
linespread: 1.0
---

# Transport Layer

## Overview

The Transport Layer (Layer 4 of the OSI model) provides end-to-end communication services between processes running on different hosts. Unlike the Network Layer which focuses on host-to-host delivery, the Transport Layer operates at the process-to-process level, introducing the concept of ports and service multiplexing.

## Fundamental Purpose

The Transport Layer serves as an intermediary between applications and the network infrastructure. It abstracts away the details of network topology, routing, and link technology, presenting a clean interface through which applications can send and receive data.

### Core Responsibilities

1. **Addressing and Multiplexing**: Distinguish between different processes on the same host using port numbers
2. **Reliability Management**: Provide mechanisms for ensuring data arrives in order and without loss (if required)
3. **Connection Management**: Establish, maintain, and terminate logical connections between processes
4. **Flow Control**: Prevent a sender from overwhelming a receiver's buffer capacity
5. **Congestion Control**: Prevent a sender from overwhelming the network
6. **Error Detection**: Identify corrupted segments through checksums

## Architectural Position

```
┌─────────────────────────────────────┐
│    Application Layer (Layer 5+)     │
│  HTTP, FTP, SMTP, DNS, etc.         │
└─────────────────────────────────────┘
              △
              │ Process-to-process
              │ communication
              ▼
┌─────────────────────────────────────┐
│    Transport Layer (Layer 4)        │
│  TCP, UDP, SCTP, etc.               │
└─────────────────────────────────────┘
              △
              │ Host-to-host
              │ communication
              ▼
┌─────────────────────────────────────┐
│    Network Layer (Layer 3)          │
│  IP, Routing protocols              │
└─────────────────────────────────────┘
```

## Protocol Taxonomy

The Transport Layer defines two primary protocol models:

### [[Connection-Oriented_Protocols|Connection-Oriented Model]]

Protocols that establish explicit connection state before data transfer:
- Require a three-phase process: establishment, data transfer, termination
- Maintain state about the connection at both endpoints
- Primary example: [[TCP_Protocol|TCP]]

### [[Connectionless_Protocols|Connectionless Model]]

Protocols that treat each message independently:
- No connection establishment or termination
- Stateless from the perspective of individual messages
- Lower overhead but fewer guarantees
- Primary example: [[UDP_Protocol|UDP]]

## Service Models

Transport protocols present different service models to applications:

### [[Reliable_Data_Stream|Reliable, In-Order Delivery]]

- All data arrives at destination
- Data arrives in the order sent
- No duplicate data
- Primary example: TCP

### [[Unreliable_Datagram|Unreliable Datagram Service]]

- Segments may be lost
- Segments may arrive out of order
- Duplicate segments may occur
- No delivery guarantees
- Primary example: UDP

## Key Abstractions

### [[Port_and_Addressing|Port and Addressing]]

Transport layer uses **ports** (16-bit numbers) to distinguish between different processes on the same host. Combined with IP address, this forms a **socket** — the fundamental abstraction for network communication.

### [[Segment_Structure|Segment]]

The unit of data transmitted by the Transport Layer. Unlike the Network Layer's "packet," the Transport Layer calls its unit of transmission a "segment" (in TCP) or "datagram" (in UDP).

## Fundamental Distinctions

### Scope of Responsibility

| Aspect | Network Layer | Transport Layer |
|---|---|---|
| **Addressing** | IP addresses identify hosts | Ports identify processes |
| **Routing** | Determine path through network | Direct communication between sockets |
| **Delivery Scope** | Host-to-host | Process-to-process |
| **Connection State** | None (in IP) | May maintain state (TCP) |
| **Reliability** | Best-effort only | Protocol-dependent |

### Transport vs. Network Services

The Network Layer provides **unreliable host-to-host delivery**. The Transport Layer builds on this foundation to provide various service models:

- **UDP**: Minimal abstraction above network layer; adds only multiplexing
- **TCP**: Extensive abstraction; adds reliability, flow control, congestion control, connection management

This approach follows the **end-to-end principle**: functionality should be implemented at the endpoints rather than in the network infrastructure itself.

## Structure of the Transport Layer

Transport protocols provide structured interaction through:

1. **Service Primitives**: Operations applications use to interact with the transport protocol
2. **Protocol Mechanisms**: Internal operations for managing connections, flow, congestion, and reliability
3. **Segment Format**: Precise bit-level structure of protocol messages

## Major Transport Protocols

### [[TCP_Protocol|TCP (Transmission Control Protocol)]]

- Connection-oriented, reliable, ordered delivery
- Used by: HTTP, SMTP, SSH, FTP, Telnet
- Covers: sequencing, acknowledgment, flow control, congestion control

### [[UDP_Protocol|UDP (User Datagram Protocol)]]

- Connectionless, unreliable, unordered delivery
- Used by: DNS, NTP, RTP, online games
- Minimal overhead; application responsible for reliability if needed

### Other Protocols

- **SCTP**: Reliable, message-oriented (between TCP and UDP)
- **DCCP**: Congestion control for streaming without TCP's ordering constraints
- **RTP**: Application-level protocol for real-time media

## Core Concepts Map

- [[Transport_Layer]]
  - [[Port_and_Addressing]]
  - [[Segment_Structure]]
  - [[Connection-Oriented_Protocols]]
    - [[Three-Way_Handshake]]
    - [[Connection_Release]]
    - [[TCP_Protocol]]
  - [[Connectionless_Protocols]]
    - [[UDP_Protocol]]
  - [[Multiplexing_and_Demultiplexing]]
  - [[Flow_Control_Mechanisms]]
  - [[Congestion_Control]]
  - [[Reliability_Mechanisms]]
  - [[The_Two_Army_Problem]]
  - [[Service_Primitives]]

## Next Steps

- Start with [[Port_and_Addressing]] to understand the fundamental addressing model
- Proceed to [[Service_Primitives]] for the API between applications and transport protocols
- Study [[UDP_Protocol]] for the simplest protocol model
- Study [[TCP_Protocol]] for comprehensive protocol design
- Understand [[Multiplexing_and_Demultiplexing]] for how multiple connections coexist
- Learn [[Reliability_Mechanisms]] for error handling and acknowledgment
- Study [[Flow_Control_Mechanisms]] and [[Congestion_Control]] for transmission regulation
