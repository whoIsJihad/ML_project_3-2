# Session 14 – Rate Limiting & Backpressure Mechanisms

## Linked Domain
[[Systems Design Integration]]

**Cycle**: 2 (Intermediate Depth)  
**Difficulty**: ⚫⚫⚪⚪

---

## Phase 1: Theoretical Foundation

### Definitions

**Rate Limiting**: A technique to control the rate of requests sent or received by a system, preventing resource exhaustion and ensuring fair usage.

**Token Bucket**: A rate limiting algorithm where tokens accumulate at a fixed rate in a bucket with maximum capacity. Each request consumes one token; requests are denied if no tokens available.

**Leaky Bucket**: A queue-based algorithm where requests enter a bucket and "leak" out at a constant rate, smoothing bursty traffic.

**Backpressure**: A flow control mechanism where downstream components signal upstream components to slow down when overwhelmed, preventing cascading failures.

**Circuit Breaker**: A pattern that monitors for failures and "opens" (blocks requests) when failure threshold is exceeded, preventing resource waste on doomed operations.

### Core Mechanism: Token Bucket Algorithm

**Parameters**:
- **Capacity** (C): Maximum tokens in bucket
- **Refill Rate** (R): Tokens added per second
- **Tokens** (T): Current token count

**Algorithm**:
```
On Request:
  1. Refill bucket: T = min(C, T + R × time_elapsed)
  2. If T ≥ 1:
       T = T - 1
       Allow request
     Else:
       Deny request
```

**Properties**:
- Allows bursts up to C requests
- Long-term average rate = R
- Tokens accumulate during idle periods

**Example**:
```
C = 10, R = 5 tokens/sec
t=0: T=10 (full)
t=0-0.1s: 10 requests → T=0 (burst allowed)
t=0.1-1.1s: 0 requests → T=5 (refilled)
t=1.1s: 5 requests → T=0
```

### Core Mechanism: Leaky Bucket Algorithm

**Parameters**:
- **Queue Capacity** (Q): Maximum requests in queue
- **Leak Rate** (R): Requests processed per second

**Algorithm**:
```
On Request:
  If queue.size() < Q:
    queue.enqueue(request)
  Else:
    Deny request

Background Worker:
  Every 1/R seconds:
    If queue not empty:
      process(queue.dequeue())
```

**Properties**:
- Output rate is constant (no bursts)
- Smooths bursty traffic
- Requests may be delayed (queued)

**Comparison**: Token vs Leaky Bucket
| | Token Bucket | Leaky Bucket |
|---|---|---|
| Bursts | Allows bursts up to C | No bursts (constant rate) |
| Latency | Immediate (if tokens available) | May queue requests |
| Implementation | Simpler (no queue) | Requires queue & worker |
| Use Case | API rate limits | Traffic shaping |

### Core Mechanism: Backpressure Propagation

**Scenario**: Microservice chain A → B → C

**Problem**: C is overloaded. Without backpressure:
```
A sends 1000 req/s → B queues → B's memory exhausts → B crashes
```

**With Backpressure**:
```
1. C detects overload (queue > threshold)
2. C returns 503 (Service Unavailable) to B
3. B stops sending to C, returns 503 to A
4. A reduces load or applies rate limit
```

**Reactive Streams Model**:
```
Publisher ← request(n) ← Subscriber
Publisher → onNext(items) → Subscriber
```
Subscriber controls flow by requesting only what it can handle.

### Core Mechanism: Circuit Breaker

**States**:
1. **Closed**: Normal operation, requests flow through
2. **Open**: Threshold exceeded, requests fail immediately
3. **Half-Open**: Test if service recovered

**Transitions**:
```
Closed → Open: failure_rate > threshold OR consecutive_failures > max
Open → Half-Open: after timeout
Half-Open → Closed: success_count > min_successes
Half-Open → Open: any failure
```

**Hystrix Parameters**:
- `requestVolumeThreshold`: Minimum requests before tripping (e.g., 20)
- `errorThresholdPercentage`: % failures to trip (e.g., 50%)
- `sleepWindowInMilliseconds`: Time in Open state (e.g., 5000ms)

### Mental Model

**Token Bucket = Restaurant Reservation**: The restaurant has 100 tables (capacity). Tables become available at a steady rate as diners leave. If you arrive when all tables are full, you're turned away. But if the restaurant is empty, you can seat a large party immediately (burst).

**Leaky Bucket = Conveyor Belt**: Orders arrive at variable rates but the kitchen processes them at a constant pace. Orders queue on the belt. If the belt is full, new orders are rejected.

**Backpressure = Traffic Congestion**: When a highway section is congested, the entrance ramp meters turn on (red/green lights). This prevents piling more cars into the jam. Backpressure is the distributed systems equivalent of ramp metering.

**Circuit Breaker = Electrical Breaker**: When a circuit draws too much current, the breaker trips to prevent fire. Similarly, when a service fails repeatedly, the circuit breaker opens to prevent wasting resources on failing calls.

### Edge Cases

**1. Distributed Rate Limiting (Race Conditions)**
```
Two instances check token count: T=1
Both see T≥1 and allow requests
Result: 2 requests allowed when only 1 token available
```
**Solutions**:
- Centralized atomic counter (Redis INCR)
- Per-instance limits with eventual consistency
- Sticky sessions

**2. Thundering Herd on Circuit Breaker**
```
Circuit in Open state for 5s with 1000 waiting clients
Circuit transitions to Half-Open
All 1000 clients immediately retry
Service overwhelmed again
```
**Solution**: Limit Half-Open to single test request.

**3. Cascading Backpressure Deadlock**
```
Service A calls B, B calls C, C calls A (cycle)
A applies backpressure to B
B applies backpressure to C
C applies backpressure to A (deadlock!)
```
**Solution**: Break cycles, use timeouts, drop requests.

### Common Mistakes

1. **No Token Refill Cap**: Forgetting `min(C, T + refill)` allows infinite token accumulation.

2. **Global Rate Limit Without Fairness**: Single rate limit for all users → one user can starve others. Need per-user limits.

3. **Ignoring Retry Storms**: Client retries failed requests → amplifies load. Exponential backoff + jitter essential.

4. **Circuit Breaker Without Fast Failure**: Still waiting for full timeout before failing. Should fail immediately when Open.

### Implementation Code

```python
import time
import threading
from collections import deque
from enum import Enum

# ============= TOKEN BUCKET =============

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def allow_request(self, tokens=1):
        """Try to consume tokens. Returns True if allowed."""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            
            # Refill tokens
            refill = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + refill)
            self.last_refill = now
            
            # Try to consume
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

# ============= LEAKY BUCKET =============

class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity
        self.leak_rate = leak_rate  # requests per second
        self.queue = deque()
        self.lock = threading.Lock()
        self.running = False
    
    def submit_request(self, request):
        """Add request to queue. Returns True if accepted."""
        with self.lock:
            if len(self.queue) < self.capacity:
                self.queue.append(request)
                return True
            return False
    
    def start_leaking(self, process_fn):
        """Start background worker to process requests"""
        self.running = True
        interval = 1.0 / self.leak_rate
        
        def worker():
            while self.running:
                with self.lock:
                    if self.queue:
                        request = self.queue.popleft()
                        process_fn(request)
                time.sleep(interval)
        
        threading.Thread(target=worker, daemon=True).start()
    
    def stop(self):
        self.running = False

# ============= DISTRIBUTED RATE LIMITER =============

class DistributedRateLimiter:
    """Sliding window counter using Redis-like atomic ops"""
    def __init__(self, limit, window_seconds):
        self.limit = limit
        self.window_seconds = window_seconds
        self.timestamps = deque()  # In production: Redis sorted set
        self.lock = threading.Lock()
    
    def allow_request(self, user_id):
        """Sliding window: count requests in last window_seconds"""
        with self.lock:
            now = time.time()
            cutoff = now - self.window_seconds
            
            # Remove old timestamps
            while self.timestamps and self.timestamps[0] < cutoff:
                self.timestamps.popleft()
            
            if len(self.timestamps) < self.limit:
                self.timestamps.append(now)
                return True
            return False

# ============= CIRCUIT BREAKER =============

class CircuitState(Enum):
    CLOSED = 1
    OPEN = 2
    HALF_OPEN = 3

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=5.0, success_threshold=2):
        self.failure_threshold = failure_threshold
        self.timeout = timeout  # seconds in OPEN state
        self.success_threshold = success_threshold
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.lock = threading.Lock()
    
    def call(self, fn, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        with self.lock:
            if self.state == CircuitState.OPEN:
                # Check if timeout expired
                if time.time() - self.last_failure_time > self.timeout:
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                else:
                    raise Exception("Circuit breaker is OPEN")
        
        try:
            result = fn(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        with self.lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
            elif self.state == CircuitState.CLOSED:
                self.failure_count = 0
    
    def _on_failure(self):
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.OPEN
            elif self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN

# ============= BACKPRESSURE =============

class BackpressureQueue:
    """Queue with backpressure signaling"""
    def __init__(self, capacity, high_watermark=0.8):
        self.capacity = capacity
        self.high_watermark = int(capacity * high_watermark)
        self.queue = deque()
        self.lock = threading.Lock()
    
    def enqueue(self, item):
        """Returns (accepted, backpressure_signal)"""
        with self.lock:
            if len(self.queue) >= self.capacity:
                return False, True  # Rejected, signal backpressure
            
            self.queue.append(item)
            signal_backpressure = len(self.queue) >= self.high_watermark
            return True, signal_backpressure
    
    def dequeue(self):
        with self.lock:
            if self.queue:
                return self.queue.popleft()
            return None
    
    def size(self):
        with self.lock:
            return len(self.queue)

# ============= EXAMPLE USAGE =============

# Token Bucket
bucket = TokenBucket(capacity=10, refill_rate=5)
for i in range(15):
    allowed = bucket.allow_request()
    print(f"Request {i+1}: {'✓ Allowed' if allowed else '✗ Denied'}")
    time.sleep(0.1)

# Circuit Breaker
def flaky_service():
    import random
    if random.random() < 0.3:
        raise Exception("Service failed")
    return "Success"

breaker = CircuitBreaker(failure_threshold=3, timeout=2.0)
for i in range(10):
    try:
        result = breaker.call(flaky_service)
        print(f"Call {i+1}: {result}")
    except Exception as e:
        print(f"Call {i+1}: Failed - {e}")
    time.sleep(0.5)
```

---

## Phase 2: Stress Questions

### Question 1: Distributed Rate Limiter Design
**Design a distributed rate limiter for 1000 req/sec across 10 servers. Requirements:**
- **a)** Fair per-user limits (100 req/sec per user)
- **b)** Handle clock skew (servers have slightly different times)
- **c)** Minimize cross-server communication

<details>
<summary>Hint</summary>
Use sliding window counter in Redis with sorted sets. Key = user_id, members = timestamp:request_id. ZREMRANGEBYSCORE removes old entries, ZCARD counts current. For clock skew, use logical timestamps or NTP sync.
</details>

---

### Question 2: Token vs Leaky Bucket Fairness
**Prove that leaky bucket provides better fairness than token bucket when user request patterns are bursty. Define fairness as variance in service rate.**

<details>
<summary>Hint</summary>
Token bucket: User A sends 100 req (burst) at t=0, gets immediate service. User B sends 100 req at t=1, may be rate limited. Leaky bucket: Both users' requests queue and are served at constant rate, reducing variance.
</details>

---

### Question 3: Backpressure in Async Pipeline
**Design a backpressure mechanism for:**
```
Client → Gateway → Service A → Service B → Database
```
Where Service B can handle 1000 req/sec but database only 500 req/sec. Implement without dropping requests.

<details>
<summary>Hint</summary>
Use bounded queues with asynchronous flow control. When queue at Service B fills to 80%, return "slow down" signal to Service A. Service A pauses sending to B, signals Gateway. Gateway applies rate limit to clients. Requires bidirectional communication channels.
</details>

---

## Phase 3: Applied Problem

### Problem: API Gateway Rate Limiting

You're building an API gateway for a SaaS platform with:
- 10,000 customers
- Tiered pricing: Free (10 req/min), Pro (100 req/min), Enterprise (1000 req/min)
- 100 gateway instances
- Global rate limit: 50,000 req/sec

**Part A: Architecture Design**
Design a rate limiting system with:
1. Per-customer rate limits (based on tier)
2. Global rate limit across all instances
3. Minimal latency overhead (< 1ms)
4. High availability (no single point of failure)

**Part B: Implementation**
Implement using Redis:
- Token bucket for per-customer limits
- Sliding window for global limit
- Handle race conditions and clock skew

**Part C: Adaptive Rate Limiting**
Implement adaptive limits that:
- Gradually increase limit for well-behaved customers
- Detect and throttle abusive traffic patterns
- Provide burst capacity during legitimate spikes

```python
import redis
import time
import hashlib

class APIGatewayRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.tiers = {
            'free': {'rate': 10, 'burst': 5},
            'pro': {'rate': 100, 'burst': 50},
            'enterprise': {'rate': 1000, 'burst': 500}
        }
    
    def check_rate_limit(self, customer_id, tier):
        """
        Check both per-customer and global rate limits.
        Returns: (allowed, remaining, reset_time)
        """
        # TODO: Implement token bucket for customer
        # TODO: Implement global sliding window counter
        # TODO: Use Redis Lua script for atomicity
        pass
    
    def adaptive_limit(self, customer_id, tier):
        """
        Adjust rate limit based on customer behavior.
        Good behavior → increase limit
        Suspicious patterns → decrease limit
        """
        # TODO: Track request patterns (time series)
        # TODO: Detect anomalies (sudden spikes, consistent saturation)
        # TODO: Adjust limits within tier bounds
        pass
    
    def token_bucket_lua_script(self):
        """
        Lua script for atomic token bucket operation in Redis.
        Returns tokens remaining.
        """
        return """
        local key = KEYS[1]
        local capacity = tonumber(ARGV[1])
        local rate = tonumber(ARGV[2])
        local requested = tonumber(ARGV[3])
        local now = tonumber(ARGV[4])
        
        -- TODO: Implement token bucket logic in Lua
        -- Get current tokens and last_refill
        -- Calculate refill
        -- Try to consume tokens
        -- Return remaining tokens or -1 if denied
        """

# Test Framework
class GatewaySimulator:
    def __init__(self):
        self.rate_limiter = APIGatewayRateLimiter(redis.Redis())
    
    def simulate_traffic(self, customers, duration_sec):
        """
        Simulate traffic for given customers and measure:
        - Request success rate
        - Latency percentiles (p50, p99)
        - Resource usage (Redis ops/sec)
        """
        # TODO: Generate realistic traffic patterns
        # TODO: Measure performance metrics
        pass

# Expected metrics:
# - Latency: p50 < 0.5ms, p99 < 2ms
# - Accuracy: < 1% error rate due to races
# - Throughput: 50k req/sec per Redis instance
```

**Expected Output**:
```
Part A: Architecture diagram with Redis, gateway instances, failover strategy
Part B: Complete implementation with Lua scripts
Part C: Adaptive algorithm with anomaly detection
Performance: Latency, accuracy, throughput analysis
```

---

## Phase 4: Self-Assessment & Feedback

### Mastery Checklist
Rate your understanding (1-5):
- [ ] Understand token bucket vs leaky bucket algorithms
- [ ] Can implement rate limiter with Redis
- [ ] Know backpressure propagation mechanisms
- [ ] Understand circuit breaker states and transitions
- [ ] Can design distributed rate limiting system

### Reflection Questions
1. **Why is backpressure essential** in microservices architectures?
2. **When would you choose** token bucket over leaky bucket?
3. **How does circuit breaker** prevent cascading failures?

### Mistake Log
Record mistakes:
- **Algorithm**: (e.g., "forgot to cap token refill")
- **Distributed**: (e.g., "didn't handle race conditions")
- **Performance**: (e.g., "used blocking operations in hot path")

### Next Steps
- **If strong**: Proceed to [[Session 15 – Memory Models]] (Cycle 3)
- **If struggling**: Review [[Session 07 – Systems Design Integration]]
- **Deep dive**:
  - "Designing Data-Intensive Applications" (Kleppmann) Ch. 11
  - Stripe rate limiting blog post
  - Netflix Hystrix documentation
  - RFC 6585 (HTTP Status Code 429)

---

**Navigation**: ← [[Session 13]] | **Index**: [[cycle2/INDEX]] | [[Cycle 3]] →
