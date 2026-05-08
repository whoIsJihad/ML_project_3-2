# MANET, VANET, and FANET Comparison

## Overview

Mobile ad hoc networks (MANETs), Vehicular ad hoc networks (VANETs), and Flying ad hoc networks (FANETs) are specialized types of ad hoc networks distinguished by their node characteristics, deployment scenarios, mobility patterns, and performance requirements. While all share the fundamental characteristics of [[Ad_Hoc_Networks_Overview|ad hoc networks]], their differences necessitate tailored protocol designs and operational strategies.

## MANET: Mobile Ad Hoc Networks

### Definition

A Mobile Ad Hoc Network (MANET) is a collection of autonomous mobile nodes that communicate via wireless links without centralized infrastructure. Nodes can join or leave the network at any time.

### Characteristics

**Node Mobility**:
- Speed: Typically low to moderate (0-10 m/s for pedestrians, 0-20 m/s for slow vehicles).
- Randomness: Nodes may move in arbitrary directions with unpredictable trajectories.
- Degree of mobility: Varies from stationary clusters to highly mobile scenarios.

**Communication Range**:
- Typically 100-300 meters (depending on frequency and power).
- Omnidirectional or directional antennas.

**Node Density**:
- Sparse to moderate; networks may range from a dozen to several hundred nodes.
- Network can become partitioned (disconnected) due to node movement.

**Power Constraints**:
- Moderate battery life; nodes can participate in routing for hours or longer.
- Power awareness is important but not critical (unlike sensor networks).

**Resource Constraints**:
- Processors and memory are limited but functional (handheld devices, laptops).

### Typical Applications

- Emergency response and disaster recovery.
- Tactical military communications.
- Wireless sensor networks.
- Conference or event-based networking.
- Vehicular communications (though VANETs are a specialized category).

### Routing Considerations

Protocols must balance:
- Frequent topology updates (due to mobility) vs. control overhead.
- Energy efficiency vs. quality of routes.
- Scalability with network size (typically < 1000 nodes).

Example protocols: [[AODV_Protocol|AODV]], DSR, OLSR.

## VANET: Vehicular Ad Hoc Networks

### Definition

A Vehicular Ad Hoc Network (VANET) is a specialized ad hoc network where mobile nodes are vehicles equipped with wireless communication capability. VANETs enable vehicle-to-vehicle (V2V) and vehicle-to-infrastructure (V2I) communication for safety, efficiency, and convenience applications.

### Characteristics

**Node Mobility**:
- Speed: High and predictable (0-150 km/h, i.e., 0-40 m/s on roads).
- Trajectory: Constrained by road topology; vehicles follow defined paths (roads).
- Acceleration: Vehicles accelerate/decelerate smoothly; sudden direction changes are limited by road geometry.

**Communication Range**:
- 100-1000 meters depending on frequency (802.11p uses 5.9 GHz).
- Line-of-sight constraints due to buildings, terrain.

**Network Topology**:
- Linear topology along roads; vehicles form lines or clusters on highways.
- Network can be sparse (few vehicles) or dense (urban traffic).
- Highly dynamic; topology changes in seconds as vehicles move.

**Power Constraints**:
- No strict power limitation; vehicles have electrical systems (engine/battery).
- Computational resources are adequate for protocol execution.

**Channel Characteristics**:
- Doppler effect due to high relative speeds.
- Fading due to reflections and obstructions.
- High interference in urban environments.

### Typical Applications

**Safety Applications**:
- Collision avoidance: Vehicles broadcast position and velocity to warn of potential crashes.
- Emergency vehicle notification: Ambulances/fire trucks broadcast emergency status.
- Road hazard warnings: Vehicles alert others about accidents, debris, or icy roads.

**Efficiency Applications**:
- Traffic flow optimization: Vehicles share congestion information.
- Cooperative driving: Platoons of vehicles maintain safe distances and coordinate movement.

**Convenience Applications**:
- Internet access: Vehicles relay Internet connectivity to occupants.
- Entertainment: Media sharing and gaming between vehicles.

### Key Differences from Generic MANETs

| Aspect | MANET | VANET |
|---|---|---|
| **Speed** | Low to moderate (0-20 m/s) | High (0-40 m/s typical) |
| **Trajectory** | Random, arbitrary | Constrained by road topology |
| **Power** | Battery-constrained | Abundant (vehicle electrical system) |
| **Scalability** | Hundreds of nodes | Thousands of nodes (urban areas) |
| **Topology** | Arbitrary clusters | Linear or grid-like |
| **Safety Critical** | Optional | Critical (accident prevention) |
| **Delay Tolerance** | Moderate | Low (safety apps need < 100 ms latency) |

### Routing Protocols for VANETs

Standard MANET protocols (AODV) perform poorly in VANETs due to:
- High mobility invalidating routes quickly.
- Linear topology underutilized by generic routing.
- Strict latency requirements for safety applications.

Specialized VANET protocols:
- **GPSR (Greedy Perimeter Stateless Routing)**: Uses vehicle GPS positions to route geographically.
- **A-STAR (Anchor-based Street and Traffic Aware Routing)**: Exploits road topology and traffic information.
- **GyTAR (Geographical-Trajectory-Based Routing)**: Uses predicted vehicle trajectories.

### Standards and Implementations

- **802.11p (DSRC - Dedicated Short Range Communications)**: 5.9 GHz spectrum, 10 MHz channels, range ~1 km.
- **C-V2X (Cellular V2X)**: Uses cellular network infrastructure (4G/5G) for V2X communication.
- **ETSI ITS G5**: European standard for vehicular communications.

## FANET: Flying Ad Hoc Networks

### Definition

A Flying Ad Hoc Network (FANET) is an ad hoc network consisting of Unmanned Aerial Vehicles (UAVs) communicating wirelessly without centralized infrastructure. FANETs enable autonomous coordinated flight of multiple UAVs.

### Characteristics

**Node Mobility**:
- Speed: Moderate to high (5-50 m/s depending on UAV type).
- Trajectory: Three-dimensional; UAVs move in 3D space (not constrained to 2D roads).
- Maneuverability: High acceleration and sharp turns (especially quadcopters).

**Communication Range**:
- Typically 1-10 km depending on UAV antenna and frequency.
- Line-of-sight (LOS) is often available (no buildings blocking aerial paths).

**Network Topology**:
- 3D spatial distribution; topology not constrained to roads.
- Highly dynamic due to 3D movement and high speeds.
- Can form sparse or dense clusters depending on mission.

**Power Constraints**:
- Severe energy limitations; flight time is 20 minutes to a few hours.
- Every computation and transmission consumes battery, reducing flight time.
- Lightweight communication equipment reduces power draw.

**Computational Resources**:
- Limited processing power (embedded systems on small UAVs).
- Memory constraints for storing routing tables.

**Channel Characteristics**:
- Excellent line-of-sight propagation in open environments.
- Path loss follows free-space model more closely than terrestrial networks.
- Less multipath fading compared to ground networks.

### Typical Applications

**Surveillance and Reconnaissance**:
- UAVs collaborate to cover large areas or provide overlapping coverage.
- Cooperative sensing: UAVs share sensor data through the network.

**Disaster Response**:
- UAVs deploy emergency communication network in areas where infrastructure is destroyed.
- Multi-UAV coordination for search and rescue.

**Agriculture and Environmental Monitoring**:
- Multiple UAVs coordinate to monitor large agricultural or environmental areas.
- Data aggregation and relay to central station.

**Package Delivery**:
- Swarms of delivery drones coordinate routing and avoid collisions.

### Key Differences from MANETs and VANETs

| Aspect | MANET | VANET | FANET |
|---|---|---|---|
| **Speed** | Low-moderate | High (constrained) | Moderate-high (3D) |
| **Trajectory** | Arbitrary 2D | Road-constrained 2D | Arbitrary 3D |
| **Power** | Moderate battery | Abundant | Severe constraints |
| **Computing** | Moderate | Good | Very limited |
| **LOS Propagation** | Often blocked | Sometimes blocked | Usually available |
| **Scalability** | Hundreds | Thousands | Tens to hundreds |
| **Communication Range** | 100-300 m | 100-1000 m | 1-10 km |

### Routing Protocols for FANETs

Standard AODV performs poorly due to:
- Rapid 3D topology changes invalidating routes.
- Energy constraints requiring minimal control overhead.
- Limited computational resources.

Specialized FANET protocols:
- **GPSR-FANET**: Geographic routing adapted for 3D aerial networks.
- **Predictive routing**: Uses trajectory prediction to proactively select stable routes.
- **Energy-aware routing**: Selects paths minimizing total energy consumption.
- **Swarm-based routing**: Uses swarm intelligence (e.g., ant colony optimization) to find energy-efficient paths.

### Control and Coordination

Beyond routing, FANETs require:
- **Collision avoidance**: Preventing air collisions between UAVs.
- **Cooperative control**: Coordinating movements of multiple UAVs.
- **Distributed task allocation**: Assigning mission tasks to UAVs based on energy and capabilities.

## Comparative Table

| Property | MANET | VANET | FANET |
|---|---|---|---|
| **Mobility Constraint** | None | Road topology | None (3D) |
| **Speed Range (m/s)** | 0-20 | 0-40 | 5-50 |
| **Power Concern** | Moderate | Low | High |
| **Computational Load** | Moderate | Moderate | Low |
| **Network Size** | Tens-hundreds | Hundreds-thousands | Tens-hundreds |
| **Communication Range** | 100-300 m | 100-1000 m | 1-10 km |
| **Primary Challenge** | Topology changes | High speed, safety | Energy, 3D topology |
| **Standard Protocol** | AODV | GPSR, A-STAR | GPSR-FANET, Predictive |

## Hybrid Scenarios

### Heterogeneous Networks

In practice, multiple types of nodes may coexist:
- **V2I (Vehicle-to-Infrastructure)**: Vehicles communicate with roadside infrastructure nodes (stationary).
- **UAV-to-Vehicle**: Aerial UAVs communicate with ground vehicles.
- **Internet-connected mesh**: Some nodes have cellular or satellite connectivity, acting as gateways.

These heterogeneous networks require protocols that adapt to diverse mobility patterns and power constraints.

## Related Concepts

- [[Ad_Hoc_Networks_Overview]]: General ad hoc network concepts.
- [[AODV_Protocol]]: A foundational MANET routing protocol.
- [[Wireless_Channel_Characteristics]]: (implied) Communication challenges in each domain.

---

**Next:** [[AODV_Protocol]]
