
A [[Routing Algorithm]] is the part of the [[Network Layer]] software responsible for deciding which output line an incoming [[Packet]] should be transmitted on. This decision process is the primary function of the [[Control Plane]].

## 1. Fundamental Classification

Routing algorithms are categorized based on their responsiveness to network changes:

### 1.1 Non-Adaptive Algorithms

[[Non-Adaptive Algorithms]] (Static Routing) do not base their routing decisions on measurements or estimates of the current [[Traffic Load]] or [[Network Topology]]. Instead, the choice of the route is computed in advance, off-line, and downloaded to the routers when the network is booted.

### 1.2 Adaptive Algorithms

[[Adaptive Algorithms]] (Dynamic Routing) change their routing decisions to reflect changes in the topology and the current traffic. These algorithms differ in:

- Where they get their information (locally, from adjacent routers, or from all routers).
    
- When they change the routes (periodically or when the topology changes).
    
- The metric used for optimization (e.g., distance, number of hops, or estimated transit time).
    

## 2. Formal Properties of Design

A routing algorithm must satisfy several rigorous requirements to be viable in a production environment:

1. **Correctness**: The algorithm must find valid paths that terminate at the intended destination.
    
2. **Simplicity**: The algorithm must be implementable with low computational overhead to ensure high-speed packet processing.
    
3. **Robustness**: The algorithm must remain functional despite hardware failures, software bugs, or changes in [[Network Topology]] without requiring a global reboot.
    
4. **Stability**: The algorithm must converge to a fixed set of paths within a finite time after a change.
    
5. **Fairness**: The algorithm must balance the needs of different flows to prevent starvation.
    
6. **Optimality**: The algorithm should minimize a cost function, typically related to [[Network Delay]] or [[Throughput]].
    

## 3. The Conflict Between [[Fairness]] and [[Optimality]]

There exists an inherent mathematical tension between achieving global network efficiency and maintaining individual flow fairness.

### 3.1 Scenario: Link Saturation

Consider a horizontal link $L$ with capacity $C$.

- Let $f_h$ be a long-distance horizontal flow requiring bandwidth $B_h$.
    
- Let $f_{v1}, f_{v2}, \dots, f_{vn}$ be short-distance vertical flows crossing link $L$, each requiring bandwidth $B_{vi}$.
    

If the objective is to maximize **Global Throughput** (Optimality), the algorithm may favor the $n$ vertical flows over the single horizontal flow because processing shorter paths reduces the total resource consumption per packet. In an extreme case, $f_h$ is allocated zero bandwidth to maximize the total number of packets delivered by the vertical flows. This satisfies [[Optimality]] but violates [[Fairness]].

