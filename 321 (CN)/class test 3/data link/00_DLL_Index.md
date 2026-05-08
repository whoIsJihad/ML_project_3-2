# Data Link Layer (DLL) - Complete Technical Reference

## Overview

The Data Link Layer (Layer 2) solves the fundamental problem of reliable packet delivery over unreliable physical transmission media. This material applies **first principles thinking**: starting from raw bitstreams and building toward sophisticated flow control and error management protocols.

## Core Problem Statement

**Gap**: Physical Layer (Layer 1) provides raw bit transmission without reliability guarantees. Network Layer (Layer 3) expects reliable, in-order packet delivery.

**Solution Space**: The DLL bridges this gap through:
- Frame synchronization (framing)
- Error detection and correction
- Flow control
- Protocol sequencing

## Modular Topics

### [[01_DLL_Foundations_Services|1. DLL Foundations & Services]]
- Virtual vs. actual communication paths
- Service models and primitives
- Packet-to-frame encapsulation
- Why the DLL exists: the abstraction contract

### [[02_Framing_Mechanics|2. Framing Mechanics]]
- Converting bitstreams into discrete frames
- Character count framing and its vulnerabilities
- Byte stuffing (FLAG, ESC) mechanics
- Bit stuffing and the `01111110` flag structure

### [[03_Error_Detection_Correction|3. Error Detection & Correction]]
- Hamming distance and error capability
- CRC polynomial-based checksums with worked examples
- Hamming codes and burst error handling
- Practical choice of error codes

### [[04_Evolution_DLL_Protocols|4. Evolution of DLL Protocols]]
- Protocol 1 (Utopia): Idealizing assumptions
- Protocol 2 (Stop-and-Wait): Flow control introduction
- Protocol 3 (PAR): Handling packet loss with sequence numbers
- Data structures: frame, packet, event_type definitions

### [[05_Sliding_Window_Pipelining|5. Sliding Window & Pipelining]]
- Piggybacking: efficient ACK transmission
- 1-bit sliding window operation and edge cases
- Go-Back-N: simple recovery, higher overhead
- Selective Repeat: complex buffering, lower overhead
- Window size constraints and sequence number space

## Design Principles

1. **Reliability Through Redundancy**: Error codes trade bandwidth for correctness
2. **Flow Control**: Prevent receiver "swamping" through windowing
3. **Piggybacking**: Bundle ACKs with data to reduce overhead
4. **Sequence Numbers**: Enable duplicate detection and out-of-order buffering
5. **Timeout Mechanisms**: Detect packet loss without explicit negative ACKs

## Reading Path

**Linear (for context)**: Foundations → Framing → Error Detection → Protocols → Sliding Window

**By Problem**: 
- "How do I synchronize frames?" → [[02_Framing_Mechanics|Framing Mechanics]]
- "How do I detect errors?" → [[03_Error_Detection_Correction|Error Detection]]
- "How do I handle packet loss?" → [[04_Evolution_DLL_Protocols|DLL Protocols]]
- "How do I maximize throughput?" → [[05_Sliding_Window_Pipelining|Sliding Window]]

---

*Last Updated: February 2026*
*Source: Computer Engineering 321 - Chapter 3 Lecture Materials*
