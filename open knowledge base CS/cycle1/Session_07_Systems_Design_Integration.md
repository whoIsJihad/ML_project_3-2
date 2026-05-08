# Session 7 – End-to-End System Design: Tradeoffs & Bottlenecks

## Linked Domain
[[Systems Design Integration]]

---

## Phase 1 – Clean Theory

### 1. Core Metrics

| Metric | Definition | Measurement |
|--------|------------|-------------|
| **Throughput** | Operations per unit time | RPS, QPS, bytes/sec |
| **Latency** | Request initiation to completion | Percentiles: p50, p95, p99, p999 |
| **Availability** | Fraction of successful requests | Uptime %, error rate |
| **Scalability** | Throughput vs. resources | Vertical vs. horizontal |

---

### 2. Scalability Laws

**Amdahl's Law**:
$$S(N) = \frac{1}{(1-P) + P/N}$$
where $P$ = parallelizable fraction.

**Universal Scalability Law** (refinement):
$$S(N) = \frac{N}{1 + \alpha(N-1) + \beta N(N-1)}$$
- $\alpha$: serialization coefficient
- $\beta$: coordination/crosstalk coefficient

**Little's Law** (stable system):
$$L = \lambda W$$
- $L$: average requests in system
- $\lambda$: arrival rate
- $W$: average time in system

---

### 3. Load Balancing Strategies

| Strategy | Algorithm | Pros | Cons |
|----------|-----------|------|------|
| **Round Robin** | Cyclic assignment | Simple, stateless | Ignores server load |
| **Least Connections** | Min active connections | Adapts to load | Requires state tracking |
| **Consistent Hashing** | Hash-based assignment | Minimal remapping on resize | Potential hotspots |
| **Random** | Uniform random | Simple, no state | Uneven distribution |

**Consistent Hashing**: Adding/removing node remaps $O(K/N)$ keys ($K$ = total keys, $N$ = nodes).

---

### 4. Caching Strategies

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Cache-Aside** | App checks cache, fetches on miss | General purpose |
| **Write-Through** | Write cache + DB synchronously | Strong consistency |
| **Write-Back** | Write cache, async flush to DB | High write throughput |

---

### 5. Database Scaling

| Technique | Benefit | Complexity |
|-----------|---------|------------|
| **Read Replicas** | Scale reads | Eventual consistency |
| **Sharding** | Scale reads + writes | Cross-shard queries, rebalancing |
| **Vertical Scaling** | Simple | Hardware limits |

**Sharding Challenges**:
- Shard key selection (avoid hotspots)
- Cross-shard join queries expensive
- Rebalancing on node add/remove

---

### 6. Latency Numbers (Reference)

| Operation | Latency |
|-----------|---------|
| L1 cache reference | 0.5 ns |
| L2 cache reference | 7 ns |
| Main memory reference | 100 ns |
| SSD random read (4KB) | 150 µs |
| Network (datacenter) | 500 µs |
| Disk seek | 10 ms |
| Network US East → West | 70 ms |
| Network US → Europe | 120 ms |

---

### 7. Edge Cases and Failure Modes

| Failure Mode | Description | Mitigation |
|--------------|-------------|------------|
| **Thundering Herd** | Cache expires, many requests hit DB | Lock on miss, probabilistic early expiration |
| **Hot Partition** | One shard receives disproportionate traffic | Dynamic rebalancing, replication |
| **Cascading Failure** | Service A overloads B overloads C | Circuit breakers, backpressure, bulkheads |
| **Split-Brain** | Network partition creates two leaders | Quorum-based consensus |
| **Poison Message** | Malformed request crashes service | Dead letter queue, validation at ingress |

---

### Common Mistakes

1. **Premature Sharding**: Sharding adds immense complexity (cross-shard queries, rebalancing). Exhaust vertical scaling first.

2. **Ignoring Tail Latencies**: Optimizing p50 while p99 is 10x worse. User experience dominated by tail. Optimize p99.

3. **Synchronous Cross-Service Calls**: Chain A → B → C → D with depth 4. Latencies add. Use async/event-driven when possible.

4. **Unbounded Queues**: Accepting unbounded requests during overload. Queue grows indefinitely, all requests timeout. Better: shed load early (return 503).

5. **Ignoring Saturation**: CPU at 90% seems fine, but queueing theory says latency explodes near 100%. Danger zone starts at ~70-80%.

---

### Code Snippet – Load Balancer Strategy Comparison

```python
import random
import time
import threading
from collections import defaultdict

class Server:
    def __init__(self, server_id, capacity_rps):
        self.id = server_id
        self.capacity = capacity_rps
        self.active_requests = 0
        self.total_served = 0
        self.lock = threading.Lock()

    def handle_request(self):
        with self.lock:
            if self.active_requests >= self.capacity:
                return False
            self.active_requests += 1

        time.sleep(random.uniform(0.01, 0.05))

        with self.lock:
            self.active_requests -= 1
            self.total_served += 1
        return True

class LoadBalancer:
    def __init__(self, servers, strategy='round_robin'):
        self.servers = servers
        self.strategy = strategy
        self.rr_index = 0
        self.lock = threading.Lock()

    def select_server(self):
        if self.strategy == 'round_robin':
            with self.lock:
                server = self.servers[self.rr_index]
                self.rr_index = (self.rr_index + 1) % len(self.servers)
            return server
        elif self.strategy == 'least_connections':
            with self.lock:
                return min(self.servers, key=lambda s: s.active_requests)
        elif self.strategy == 'random':
            return random.choice(self.servers)

    def send_request(self):
        server = self.select_server()
        return server.handle_request()

def benchmark(strategy, num_servers, load_rps, duration_s):
    servers = [Server(i, capacity_rps=100) for i in range(num_servers)]
    lb = LoadBalancer(servers, strategy=strategy)

    success_count = 0
    failure_count = 0
    start_time = time.time()
    stop = threading.Event()

    def send_requests():
        nonlocal success_count, failure_count
        while not stop.is_set():
            if lb.send_request():
                success_count += 1
            else:
                failure_count += 1
            time.sleep(1.0 / load_rps)

    threads = [threading.Thread(target=send_requests) for _ in range(10)]
    for t in threads: t.start()
    time.sleep(duration_s)
    stop.set()
    for t in threads: t.join()

    total_served = sum(s.total_served for s in servers)
    print(f"\n{strategy.upper()}:")
    print(f"  Total served: {total_served}")
    print(f"  Success: {success_count}, Failures: {failure_count}")
    print(f"  Distribution: {[s.total_served for s in servers]}")

if __name__ == "__main__":
    print("Load Balancer Comparison (10 servers, 500 RPS, 5s)")
    benchmark('round_robin', 10, 500, 5)
    benchmark('least_connections', 10, 500, 5)
    benchmark('random', 10, 500, 5)
```

---

## Phase 2 – Conceptual Stress Questions

**Q1**: System with 5 services in sequence: A → B → C → D → E. Latencies:
- A: 10ms (p50), 50ms (p99)
- B: 20ms (p50), 100ms (p99)
- C: 5ms (p50), 30ms (p99)
- D: 30ms (p50), 200ms (p99)
- E: 15ms (p50), 80ms (p99)

Compute system's p99 latency (NOT sum of p99s). Which service to optimize first? Justify quantitatively.

**Q2**: Database uses consistent hashing with 100 nodes, $V = 1000$ virtual nodes. Add 10 new nodes. Using formula:
$$\text{Keys moved} = K \cdot \frac{\text{nodes added}}{N_{\text{old}} + \text{nodes added}}$$
Compute fraction of keys moved. Colleague suggests rendezvous hashing—only $O(1/N)$ keys move. Analyze this claim.

**Q3**: API gateway handles 10,000 RPS. Each request queries database with 5ms average latency. Using Little's Law, compute average concurrent database connections. If database allows max 500 connections, what happens? Does adding a queue at gateway help? Analyze using queueing theory.

---

## Phase 3 – Applied Problem

**Problem Statement**:

Design a **URL shortener** (like bit.ly):
- **Write**: Create short URL (100 writes/sec)
- **Read**: Redirect short URL (10,000 reads/sec)
- **Requirements**: p99 latency < 100ms, 99.99% availability

**Part A – Database Design**:
- Single-leader PostgreSQL handles ~5000 writes/sec. Need sharding?
- Read replicas: How many needed at 50 reads/sec per replica?
- Caching: What hit rate reduces DB load to acceptable level? Compute precisely.

**Part B – Bottleneck Analysis**:
- Network latency: 50ms p99 (datacenter)
- DB query (cache miss): 10ms p50, 30ms p99
- Redis cache: 1ms p50, 5ms p99

Construct latency breakdown table. What is critical path? If you could reduce one component's latency by 50%, which yields most improvement?

**Part C – Failure Modes**:
- Database primary fails. Replica is 2 seconds behind. What happens to writes in those 2 seconds?
- Cache invalidation fails (long URL changes but cache has stale short URL). How to detect and fix?
- Design circuit breaker: under what condition should gateway stop sending requests to database?

**Part D – Scalability Analysis**:
- Amdahl's law: 80% of work is parallelizable (stateless redirects). Compute maximum speedup with 100 servers.
- At 50 servers, throughput is 50x. At 100 servers, throughput is only 75x. Explain using Universal Scalability Law. What is coordination overhead $\beta$?

---

## Phase 4 – Feedback & Weakness Log Update

**Awaiting your responses to Phase 2 and Phase 3.**

Critique will focus on:
- Quantitative precision (not handwavy "add caching")
- Bottleneck identification methodology
- Trade-off analysis (consistency vs latency vs cost)
- Latency composition understanding
- Failure mode reasoning

---

## Cross-Links for Reinforcement
- [[Consistent Hashing Deep Dive]]
- [[Queueing Theory (M/M/1, M/M/c)]]
- [[Circuit Breakers & Bulkheads]]
- [[Cache Coherence Protocols]]
- [[Database Replication Lag]]
- [[Tail Latency Amplification]]

---

**Status**: Awaiting Phase 2 & 3 responses.
