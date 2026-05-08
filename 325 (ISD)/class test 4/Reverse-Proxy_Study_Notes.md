# Reverse Proxy - Study Notes

**Source:** Reverse-Proxy.pdf | **Instructor:** Mahir Labib Dihan

---

## Core Concepts

**Reverse Proxy:** Intermediary server between clients and backend servers. Routes requests based on domain/URL, hides internal infrastructure.

**Virtual Hosting:** Multiple applications on one server; proxy routes traffic by domain name or path.

**Load Balancing:** Distributes requests across multiple servers to prevent bottlenecks.

---

## Scaling Strategies

| Strategy | Pros | Cons |
|----------|------|------|
| **Vertical (Scale Up)** | Simple | Hardware limits, single point of failure, downtime |
| **Horizontal (Scale Out)** | No failure, cost-effective | Complex, requires load balancer |

---

## Load Balancing Algorithms

1. **Round Robin:** Sequential rotation; best for uniform workloads
2. **Least Connections:** Route to server with fewest connections; variable workloads
3. **IP Hashing:** Same IP → same server; session persistence

---

## Fault Tolerance

### The Problem
If your load balancer goes down, **all traffic stops** reaching backend servers. Even though you have redundant backend servers, clients can't reach them if the load balancer fails.

### Solution: Redundant Load Balancers

#### **Active-Active Configuration**

**Setup:** 2+ load balancers running **simultaneously**, both actively handling traffic.

**How it works:**
```
Client → DNS resolves to LB1 (IP: 10.0.0.1)     ← Client 1 hits LB1
Client → DNS resolves to LB2 (IP: 10.0.0.2)     ← Client 2 hits LB2
Client → DNS resolves to LB1 (IP: 10.0.0.1)     ← Client 3 hits LB1
...

LB1 and LB2 both forward requests to the same backend servers
```

**Failover:** If LB1 fails, DNS updates to remove 10.0.0.1. New clients are directed only to LB2. Existing connections on LB1 are lost (bad).

**Advantages:**
- Better resource utilization (both servers actively work)
- Handles more total traffic
- No idle resources

**Drawbacks:**
- More complex to set up
- Existing connections lost if one LB fails
- Requires DNS updating (not instant)

---

#### **Active-Passive Configuration**

**Setup:** 1 primary LB handles all traffic; 1+ backup LB stands by idle.

**How it works:**
```
DNS → 10.0.0.1 (Active/Primary)     ← All clients hit LB1
  └─ Forwards to backend servers

10.0.0.2 (Passive/Standby)          ← LB2 is idle, monitoring LB1
  └─ Waits for LB1 to fail
```

**Failover:** If LB1 fails, a health check detects it. DNS updates to point to LB2 (10.0.0.2). LB2 becomes active and handles all traffic.

**Advantages:**
- Simpler to manage (clear primary/secondary roles)
- Faster failover (backup is already running, just need DNS update)
- Backup is always ready

**Drawbacks:**
- Passive LB is idle (wasted resources)
- Single point of failure during DNS update delay
- Lower total capacity

---

### Key Insight: The Paradox

Adding redundant servers **reduces** the probability of failure, but **somewhere** a single point of failure exists:
- DNS server
- Network link from ISP
- Power supply

**Goal:** NOT to eliminate failure (impossible), but to **reduce probability and impact to acceptable levels**.

---

## Choosing Between Active-Active and Active-Passive

| Factor | Active-Active | Active-Passive |
|--------|---------------|----------------|
| **Resource Utilization** | Better (both work) | Wasteful (one idle) |
| **Total Capacity** | Higher | Lower |
| **Setup Complexity** | Harder | Easier |
| **Cost** | Higher operational cost | Higher idle cost |
| **Best For** | High-traffic systems | Smaller systems, simplicity |

---

## API Gateway

**Purpose:** Single entry point for microservices. Handles: parameter validation, authentication, rate limiting, routing, protocol translation.

**Benefit:** Clients don't need to know individual service locations; centralized security.

---

## KEY QUESTIONS & ANSWERS

### Q1: Why horizontal scaling over vertical?
**A:** Horizontal adds servers (no single point of failure, cheaper). Vertical upgrades one machine (hits hardware limits, is a bottleneck).

### Q2: Server 1 has 5 active connections, Server 2 has 2. Which gets next request with Least Connections?
**A:** Server 2 (fewer connections). This algorithm balances variable workloads better than Round Robin.

### Q3: IP hashing ensures session persistence. True/False? Why?
**A:** True. Same client IP always routes to same server, keeping session state without re-authentication.

### Q4: What if the load balancer fails?
**A:** Redundant load balancers (Active-Active or Active-Passive) with failover. No system is 100% fault-proof; goal is reduce failure impact.

---

## Real-World Architecture

```
Internet → [Reverse Proxy/Load Balancer] → Backend Servers → Database
                (Single point, but redundant)        (Scaled)
```

---

## Study Focus

- **Algorithm selection:** Know when to use Round Robin vs Least Connections vs IP Hashing
- **Scaling choice:** Why horizontal > vertical for reliability
- **Fault tolerance:** Understand Active-Active and Active-Passive tradeoffs
- **API Gateway role:** Centralizes cross-cutting concerns (auth, rate limiting, routing)

