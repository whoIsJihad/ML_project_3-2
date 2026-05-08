# Network Layer Tutorials — Complete Reference

## Overview

This is a comprehensive, self-contained study reference for Network Layer concepts in data communications and networking. The material is organized as a set of interlinked notes using Obsidian-style `[[wikilinks]]`, enabling navigation between prerequisite concepts, detailed explanations, practical examples, step-by-step simulations, and command-line tools for exploration.

**Target Audience:** Absolute beginner in networking, but with rigorous conceptual development.

## Structure

The tutorials are organized into the following major sections:

### Foundational Concepts
- [[Routing_Fundamentals]] — Base concepts of routing, routing tables, and packet forwarding
- [[Routing_Tables_and_Forwarding_Mechanics]] — How routers make decisions
- [[IP_Addressing_Review]] — Essential IP addressing concepts (IPv4, subnetting)

### Routing Algorithms
- [[Unicast_Routing_Overview]] — General principles of unicast (one-to-one) routing
- [[Distance_Vector_Routing]] — Algorithms like RIP; detailed mechanics
- [[Link_State_Routing]] — Algorithms like OSPF; Dijkstra's algorithm
- [[Hierarchical_Routing]] — Scaling routing to large networks
- [[Hierarchical_Routing_Examples_and_Simulations]] — Practical examples and step-by-step traces

### Advanced Routing Architectures
- [[Broadcast_Routing]] — One-to-all packet transmission
- [[Broadcast_Routing_Algorithms]] — Flooding, reverse path forwarding, sink trees
- [[Multicast_Routing]] — One-to-many transmission with multicast groups
- [[Multicast_Routing_Algorithms]] — Multicast trees and protocols

### Mobile and Ad Hoc Networks
- [[Mobile_Host_Routing]] — Routing for mobile nodes with movement
- [[Mobile_IP_Protocol]] — Home agents, foreign agents, care-of addresses
- [[Network_Mobility_NEMO]] — Mobility for aggregated nodes/subnets
- [[Ad_Hoc_Networks_Overview]] — Routing in networks without fixed infrastructure
- [[MANET_VANET_FANET_Comparison]] — Types of ad hoc networks
- [[AODV_Protocol]] — AODV routing protocol (Ad hoc On-Demand Distance Vector)
- [[AODV_Route_Discovery_Simulation]] — Step-by-step route discovery process
- [[AODV_Route_Maintenance_Simulation]] — Handling failures and topology changes

### Congestion and QoS
- [[Congestion_Control_Fundamentals]] — Why congestion occurs and its impact
- [[Congestion_Prevention_Policies]] — Strategies at different layers
- [[Congestion_Control_Algorithms]] — Hop-by-hop choke packets, RED algorithm
- [[Quality_of_Service_QoS]] — Requirements, techniques, and traffic shaping
- [[Leaky_Bucket_Algorithm]] — Traffic shaping mechanism
- [[Token_Bucket_Algorithm]] — Burst-aware traffic shaping
- [[Leaky_Token_Bucket_Comparison_Simulation]] — Practical comparison with examples

### Network Services
- [[Tunneling_and_VPN]] — Encapsulation and virtual private networks
- [[IP_Fragmentation]] — Breaking large packets into smaller pieces
- [[ICMP_Protocol]] — Control messages, diagnostics, and traceroute
- [[ICMP_Practical_Examples]] — ping, traceroute, and diagnostics
- [[DHCP_Protocol]] — Dynamic host configuration
- [[DHCP_Simulation]] — Step-by-step DHCP process

## How to Use

1. **Start with fundamentals**: Begin at [[Routing_Fundamentals]] if you're new to routing concepts.
2. **Follow the wikilinks**: Each note links to prerequisite concepts and related advanced topics.
3. **Study step-by-step simulations**: Look for notes ending with "_Simulation" for detailed packet-by-packet traces.
4. **Use command reference**: Each practical section includes shell commands for Linux/Unix exploration.
5. **Review diagrams**: Mermaid diagrams visualize packet flows, state transitions, and network topologies.

## Key Features

- **Formal definitions and mathematical precision** where applicable
- **First-principles derivations** for all algorithms
- **Step-by-step simulations** showing packet movement through networks
- **Practical Linux/Unix commands** for exploring and testing concepts
- **Mermaid diagrams** for visualization of flows, trees, and state machines
- **Dense cross-linking** to navigate between related concepts
- **Complete examples** with real IP addresses, subnet masks, and packet formats

## Topics Covered

Total pages of content (conceptual): 59 pages of lecture material

- Unicast and hierarchical routing
- Broadcast and multicast routing
- Mobile IP and network mobility
- Ad hoc networks (MANET, VANET, FANET)
- AODV protocol with route discovery and maintenance
- Congestion control and QoS
- Traffic shaping algorithms
- Tunneling, VPN, and IP fragmentation
- ICMP and DHCP protocols

---

**Next step:** [[Routing_Fundamentals]]
