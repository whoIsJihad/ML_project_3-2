# Session 21 – Service Mesh & Observability

## Linked Domain
[[Systems Design Integration]]

**Cycle**: 3 (Advanced Integration)  
**Difficulty**: ⚫⚫⚫⚪

---

## Phase 1: Theoretical Foundation

### Definitions

**Service Mesh**: Infrastructure layer for handling service-to-service communication (routing, load balancing, retries, observability) via sidecar proxies.

**Sidecar Proxy**: Proxy deployed alongside each service instance. Intercepts network traffic transparently.

**Control Plane**: Manages configuration and policy distribution to sidecar proxies (e.g., Istio, Linkerd control plane).

**Data Plane**: Sidecar proxies handling actual traffic (e.g., Envoy proxies).

**mTLS**: Mutual TLS where both client and server authenticate each other. Service mesh provides transparent mTLS.

**Observability**: Three pillars:
- **Metrics**: Aggregated statistics (request rate, latency, errors)
- **Logs**: Detailed event records
- **Traces**: Request path through services (distributed tracing)

### Core Mechanism: Traffic Management

**Load Balancing Algorithms**:
- **Round Robin**: Distribute evenly
- **Least Request**: Send to instance with fewest active requests
- **Weighted**: Prefer instances based on health/capacity

**Circuit Breaking**:
```
Max Connections: 100
Max Pending Requests: 1000
Max Requests: 10000
Max Retries: 3

If exceeded → fail fast (503)
```

**Retry Budget**:
- Limit retries to prevent retry storms
- Example: Max 10% of requests can be retries

**Timeouts & Deadlines**:
- Request timeout: 5s
- Deadline propagation: Downstream services inherit deadline

### Core Mechanism: Observability (Distributed Tracing)

**Trace Structure**:
```
Trace ID: 123e4567-e89b-12d3-a456-426614174000
  Span ID: 11111 (Frontend)
    Span ID: 22222 (Auth Service) [parent: 11111]
    Span ID: 33333 (Product Service) [parent: 11111]
      Span ID: 44444 (Database) [parent: 33333]
```

**Trace Context Propagation** (W3C standard):
```
traceparent: 00-{trace-id}-{span-id}-{flags}
```
Each service extracts, creates child span, injects new context.

**Metrics Collection**:
- RED method: **Rate, Errors, Duration**
- USE method: **Utilization, Saturation, Errors**

Sidecar proxies emit metrics for every request (L7 protocol aware).

### Mental Model

**Service Mesh = Air Traffic Control**: Each plane (service) has a co-pilot (sidecar proxy). Control tower (control plane) updates flight plans, but co-pilot actually flies. Air traffic control monitors all flights (observability), reroutes on issues (traffic management), enforces zones (security policies).

**Distributed Tracing = Package Tracking**: Trace ID is tracking number. Each handler (service) logs when package arrives/departs. At end, reconstruct full journey from distributed logs.

### Edge Cases

**1. Sidecar Overhead**
- Extra network hop (service → sidecar → remote sidecar → remote service)
- Latency: +1-5ms per hop
- Memory: 50-100MB per sidecar

**Optimization**: eBPF-based mesh (Cilium) bypasses userspace proxies.

**2. Trace Sampling**
- 100% tracing → storage/performance cost too high
- Tail sampling: Sample after trace completes (keep traces with errors/high latency)

**3. Cascading Failures**
```
Service A → B → C
C degrades (1s latency)
B accumulates pending requests (queue builds)
B degrades
A degrades
Full system outage
```

**Mitigation**: Timeouts, circuit breakers, bulkheads (isolate resources).

### Common Mistakes

1. **No Retry Budget**: Unlimited retries → retry storm when service degraded.

2. **Deep Stack Traces**: Tracing 100-service calls → trace too large, storage explodes. Sample aggressively.

3. **Ignoring Sidecar Cost**: Adding mesh to low-latency service (p99 = 10ms) → mesh overhead dominates.

### Code

```python
import time
import random
import uuid
from collections import defaultdict

class TraceContext:
    def __init__(self, trace_id=None, span_id=None, parent_span_id=None):
        self.trace_id = trace_id or str(uuid.uuid4())
        self.span_id = span_id or str(uuid.uuid4())[:8]
        self.parent_span_id = parent_span_id
    
    def create_child(self):
        """Create child span"""
        return TraceContext(
            trace_id=self.trace_id,
            span_id=str(uuid.uuid4())[:8],
            parent_span_id=self.span_id
        )

class Span:
    def __init__(self, service_name, trace_ctx):
        self.service = service_name
        self.trace_id = trace_ctx.trace_id
        self.span_id = trace_ctx.span_id
        self.parent_span_id = trace_ctx.parent_span_id
        self.start_time = time.time()
        self.end_time = None
        self.tags = {}
    
    def finish(self):
        self.end_time = time.time()
        return self
    
    def to_dict(self):
        return {
            'trace_id': self.trace_id,
            'span_id': self.span_id,
            'parent_span_id': self.parent_span_id,
            'service': self.service,
            'duration_ms': (self.end_time - self.start_time) * 1000 if self.end_time else None,
            'tags': self.tags
        }

class ServiceMeshProxy:
    def __init__(self, service_name):
        self.service_name = service_name
        self.circuit_breaker = CircuitBreaker(threshold=5, timeout=5.0)
        self.metrics = defaultdict(int)
        self.traces = []
    
    def handle_request(self, downstream_service, trace_ctx=None):
        """Sidecar proxy handles request"""
        # Create/propagate trace context
        if not trace_ctx:
            trace_ctx = TraceContext()
        
        span = Span(self.service_name, trace_ctx)
        
        # Circuit breaker check
        if not self.circuit_breaker.allow_request():
            span.tags['error'] = 'circuit_breaker_open'
            span.finish()
            self.traces.append(span.to_dict())
            self.metrics['errors'] += 1
            raise Exception("Circuit breaker open")
        
        # Retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Simulate request
                result = downstream_service.process(trace_ctx.create_child())
                span.finish()
                self.traces.append(span.to_dict())
                self.metrics['requests'] += 1
                self.circuit_breaker.record_success()
                return result
            except Exception as e:
                if attempt == max_retries - 1:
                    span.tags['error'] = str(e)
                    span.finish()
                    self.traces.append(span.to_dict())
                    self.metrics['errors'] += 1
                    self.circuit_breaker.record_failure()
                    raise
                time.sleep(0.1 * (2 ** attempt))  # Exponential backoff

class CircuitBreaker:
    def __init__(self, threshold, timeout):
        self.threshold = threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def allow_request(self):
        if self.state == 'CLOSED':
            return True
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
                return True
            return False
        if self.state == 'HALF_OPEN':
            return True
    
    def record_success(self):
        if self.state == 'HALF_OPEN':
            self.state = 'CLOSED'
            self.failure_count = 0
    
    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.threshold:
            self.state = 'OPEN'

class ServiceA:
    def __init__(self):
        self.proxy = ServiceMeshProxy('ServiceA')
    
    def handle(self, service_b):
        return self.proxy.handle_request(service_b)

class ServiceB:
    def __init__(self):
        self.name = 'ServiceB'
    
    def process(self, trace_ctx):
        span = Span(self.name, trace_ctx)
        time.sleep(random.uniform(0.01, 0.1))
        # Simulate occasional failures
        if random.random() < 0.1:
            span.tags['error'] = 'random_failure'
            span.finish()
            raise Exception("Service failed")
        span.finish()
        return "Success"

# Example
service_a = ServiceA()
service_b = ServiceB()

for i in range(20):
    try:
        result = service_a.handle(service_b)
        print(f"Request {i+1}: {result}")
    except Exception as e:
        print(f"Request {i+1}: Failed - {e}")

# Print metrics
print(f"\nMetrics: {dict(service_a.proxy.metrics)}")
print(f"Circuit Breaker State: {service_a.proxy.circuit_breaker.state}")
```

---

## Phase 2: Stress Questions

### Q1: Cascading Failure Analysis
**Given service chain A → B → C → D where D's latency increases from 10ms to 2s. Each service has 100 max connections, 5s timeout. Analyze cascade.**

<details><summary>Hint</summary>
D slow → C's connections exhaust → C slow → B's connections exhaust. Calculate time to cascade based on request rate and connection limits.
</details>

### Q2: Trace Sampling Strategy
**Design adaptive sampling: target 1% overall, but 100% for errors. With 1M requests/sec, 0.1% error rate, what's storage requirements?**

<details><summary>Hint</summary>
Sampled: 1% × 1M = 10k traces. Errors: 0.1% × 1M = 1k traces (all kept, already in 1%). Thus 10k traces total. If avg trace = 10 spans × 1KB = 10KB, storage = 100MB/sec.
</details>

### Q3: mTLS Performance Impact
**Measure mTLS overhead: TLS handshake = 2 RTT, symmetric encryption = 0.5ms per request. For 10ms baseline latency, analyze:**
- **a)** Handshake cost (with connection pooling 100 requests/connection)
- **b)** Per-request cost
- **c)** Total overhead

<details><summary>Hint</summary>
Handshake amortized: 2 RTT / 100 = 0.02 RTT per request. Encryption: 0.5ms. If RTT = 1ms, overhead = 0.02ms + 0.5ms = 0.52ms (5% of 10ms).
</details>

---

## Phase 3: Applied Problem

Design service mesh for e-commerce platform:
- 20 microservices
- 10k requests/sec peak
- Requirements: mTLS, per-service circuit breakers, distributed tracing (1% sampling)

**Part A**: Architecture diagram with control plane, data plane, and observability backend.

**Part B**: Implement traffic shifting for canary deployment (90% stable, 10% canary).

**Part C**: Analyze cost: latency overhead, memory per sidecar, trace storage.

```python
class ServiceMesh:
    def __init__(self):
        self.control_plane = ControlPlane()
        self.sidecars = {}
    
    def register_service(self, service_name):
        """Register service and deploy sidecar"""
        # TODO: Deploy sidecar proxy
        pass
    
    def canary_deployment(self, service_name, stable_weight=90, canary_weight=10):
        """Route traffic between stable and canary versions"""
        # TODO: Implement weighted routing
        pass
    
    def collect_traces(self, sample_rate=0.01):
        """Collect and aggregate traces"""
        # TODO: Sample traces, send to backend (Jaeger/Zipkin)
        pass
```

---

## Phase 4: Self-Assessment

### Checklist
- [ ] Understand service mesh architecture (control/data plane)
- [ ] Know traffic management patterns (circuit breaker, retries, timeouts)
- [ ] Can implement distributed tracing
- [ ] Understand mTLS and security policies
- [ ] Know observability best practices (RED/USE methods)

### Next Steps
- **Strong**: [[Cycle 4 – Session 22]] (Expert level)
- **Struggling**: Review [[Session 07 – Systems Design Integration]]
- **Resources**: Istio documentation, Envoy proxy docs, "Distributed Tracing in Practice" (OpenTelemetry)

---

**Navigation**: ← [[Session 20]] | **Index**: [[cycle3/INDEX]] | [[Cycle 4]] →
