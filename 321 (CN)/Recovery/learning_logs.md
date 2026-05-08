# Learning Logs

This file collects concise explanations and short notes appended during study sessions.

## 2025-12-16 — OSPF vs IS-IS (LSP vs LSA)

Both OSPF and IS-IS are link-state routing protocols. They help routers find the best path by sharing information about their connections.

- **OSPF** uses messages called **LSAs** (Link State Advertisements).
- **IS-IS** uses messages called **LSPs** (Link State Packets).

What do these messages do?
- Both LSAs and LSPs tell all routers about the network’s layout (who is connected to whom).
- Every router builds a map of the network from these messages.
- Then, each router uses Dijkstra’s algorithm to find the shortest path to every destination.

Key differences:
- OSPF is mostly used in company (enterprise) networks and sends its messages using IP.
- IS-IS (with LSPs) is often used by big internet providers and sends its messages directly over Ethernet (not using IP).
- The main difference is the name and format of the messages, and where they are most often used.

**Summary:**
OSPF and IS-IS do the same job in different ways. OSPF uses LSAs, IS-IS uses LSPs, but both help routers share network info and find the best routes.
## 2025-12-15 — Conflicting Metrics (Routing)

- What it means: In routing/network design, a metric is a number used to compare paths (e.g., hops, delay, bandwidth, cost). Conflicting metrics arise because you cannot optimise all desirable properties at once — improving one metric typically degrades another.

- Common competing metrics:
	- Delay (latency): time for a packet to travel from source to destination.
	- Throughput (bandwidth): rate data can be transferred.
	- Cost: monetary/administrative cost of using a link.
	- Reliability / Stability: likelihood the path stays up and performs consistently.
	- Fairness: how resources are shared among users/flows.

- Why they conflict (short examples):
	- Delay vs Throughput: more traffic on a high-bandwidth link increases queueing, raising delay (crowded fast highway becomes slow).
	- Cost vs Performance: cheapest route may traverse congested/slow links → lower cost but worse latency and throughput.
	- Fairness vs Optimality: always choosing best paths maximises total throughput but can starve small or latency-sensitive flows.
	- Reliability vs Cost/Utilization: highly redundant reliable routes cost more and may be underutilized.

- How networks mitigate conflicts:
	- Weighted composite metrics: combine multiple metrics with policy weights (score = w1*delay + w2*(1/bandwidth) + w3*cost).
	- Policy-based routing: different routing for traffic classes (e.g., VoIP on low-latency paths, bulk backups on low-cost paths).
	- Quality of Service (QoS): priority queues, traffic shaping, class-based queuing to reserve or prioritise resources.
	- Admission control & reservations: reserve bandwidth for real-time streams (MPLS/RSVP) at the expense of unused capacity when idle.
	- Load balancing / multi-path routing: split traffic across multiple paths (ECMP, MPTCP) to balance delay and throughput.
	- Traffic engineering: proactive rerouting and shaping (MPLS TE, SDN) to avoid hotspots while respecting cost constraints.
	- Dynamic metrics & hysteresis: adapt metrics to conditions and use damping to avoid route oscillation.
	- Differentiated services (DiffServ): mark packets by class; expedite low-latency flows, best-effort for bulk.

- Quick study tips / exam points:
	- Provide an example showing the trade-off (e.g., high-throughput path causing queueing delay).
	- Remember: no single metric fits all traffic — choose per-application goals.
	- Name mitigation techniques: QoS, weighted metrics, traffic engineering, admission control.

- One-line summary: Conflicting metrics occur because improving one objective (throughput, cost, delay, fairness, reliability) often worsens another; practical networks use classification, QoS, traffic engineering and multi-path strategies to balance trade-offs.

