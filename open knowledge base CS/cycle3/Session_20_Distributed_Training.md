# Session 20 – Distributed Training & Parameter Servers

## Linked Domain
[[ML & Optimization]]

**Cycle**: 3 (Advanced Integration)  
**Difficulty**: ⚫⚫⚫⚪

---

## Phase 1: Theoretical Foundation

### Definitions

**Data Parallelism**: Split training data across workers. Each worker computes gradients on its batch, gradients aggregated across workers.

**Model Parallelism**: Split model across devices (different layers on different GPUs). Used for models too large for single device.

**Parameter Server**: Central server stores parameters. Workers pull parameters, compute gradients, push updates.

**AllReduce**: Communication primitive where each node contributes value, all nodes receive sum/average. Used in Ring-AllReduce topology.

**Synchronous SGD**: All workers synchronize after each batch (barrier). Slow worker slows everyone.

**Asynchronous SGD**: Workers update parameters independently. Faster but potentially stale gradients.

### Core Mechanism: Parameter Server Architecture

**Components**:
- **Parameter Server (PS)**: Stores global model parameters θ
- **Workers**: Compute gradients on local data batches

**Synchronous Update**:
```
1. Workers pull parameters θ_t from PS
2. Each worker k computes gradient g_k on local batch
3. PS aggregates: g_t = (1/K) Σ g_k
4. PS updates: θ_{t+1} = θ_t - η g_t
5. Repeat
```

**Asynchronous Update**:
```
Worker k loop:
  1. Pull current θ from PS
  2. Compute gradient g_k
  3. Push g_k to PS
  PS updates θ immediately (no waiting)
```

**Trade-off**:
- Sync: No stale gradients, but stragglers slow training
- Async: Faster iteration, but stale gradients harm convergence

### Core Mechanism: Ring-AllReduce

**Topology**: Workers arranged in ring (worker 0 → 1 → 2 → ... → 0)

**Algorithm** (N workers, D parameters):
1. **Scatter-Reduce**: Each worker sends D/N chunk in ring, accumulates sums
   - N-1 steps, each step sends D/N data
2. **AllGather**: Each worker sends accumulated chunk, all workers get result
   - N-1 steps, each step sends D/N data

**Complexity**:
- Data transferred per worker: 2D(N-1)/N ≈ 2D
- Bandwidth-optimal (vs parameter server: sending D both ways)

**Advantage Over PS**: No bottleneck server. Scales to large N.

### Mental Model

**Parameter Server = Bank**: Workers are customers. Bank holds money (parameters). Customers withdraw (pull), do work, deposit earnings (push). Synchronous = everyone waits for slowest customer. Asynchronous = first-come-first-served, but bank balance might be stale.

**Ring-AllReduce = Bucket Brigade**: Fire brigade passing buckets in circle. Each person adds water from their bucket, passes on. After full circle, everyone has total.

### Edge Cases

**1. Stale Gradients in Async SGD**
```
Time  Worker1        Worker2      Parameter θ
0     pull θ=0       pull θ=0     θ=0
1     compute g1     compute g2   
2     push g1        -            θ=0-η·g1
3     -              push g2      θ=0-η·(g1+g2)  ← g2 computed on stale θ=0

If θ changed significantly from 0 → 0-η·g1, g2 is stale.
```

**Mitigation**: Bounded staleness (reject updates older than τ steps).

**2. Gradient Compression**
Full precision gradients expensive to communicate.
**Techniques**:
- Quantization: Float32 → Int8
- Sparsification: Send only top-k gradients
- Error feedback: Accumulate quantization error for next iteration

**3. Stragglers in Synchronous SGD**
Slow machine or network delay causes all workers to wait.
**Mitigation**:
- Backup workers (redundancy)
- Dynamic batching (skip stragglers after timeout)

### Common Mistakes

1. **Ignoring Communication Cost**: 100 GPUs don't give 100× speedup if communication dominates.

2. **Large Batch Instability**: Scaling batch size with workers can hurt generalization. Need learning rate warmup.

3. **Async Divergence**: Asynchronous SGD can diverge if learning rate not reduced or staleness not bounded.

### Code

```python
import numpy as np
import threading
import time

class ParameterServer:
    def __init__(self, dim):
        self.params = np.zeros(dim)
        self.lock = threading.Lock()
        self.version = 0
    
    def pull(self):
        """Worker pulls parameters"""
        with self.lock:
            return self.params.copy(), self.version
    
    def push(self, gradient, lr=0.01):
        """Worker pushes gradient"""
        with self.lock:
            self.params -= lr * gradient
            self.version += 1

class Worker:
    def __init__(self, id, ps, data, labels):
        self.id = id
        self.ps = ps
        self.data = data
        self.labels = labels
    
    def compute_gradient(self, params):
        """Compute gradient on local batch (simplified linear regression)"""
        # Loss = (y - Xθ)²
        # Gradient = -2X^T(y - Xθ)
        pred = self.data @ params
        error = self.labels - pred
        gradient = -2 * self.data.T @ error / len(self.labels)
        return gradient
    
    def train_sync(self, iterations):
        """Synchronous training"""
        for i in range(iterations):
            params, version = self.ps.pull()
            gradient = self.compute_gradient(params)
            # In real system: synchronize here (barrier)
            self.ps.push(gradient)
            if self.id == 0:  # Only one worker prints
                print(f"Iteration {i}, Version {version}")
    
    def train_async(self, iterations):
        """Asynchronous training"""
        for i in range(iterations):
            params, version = self.ps.pull()
            gradient = self.compute_gradient(params)
            time.sleep(np.random.uniform(0.01, 0.1))  # Simulate varying compute time
            self.ps.push(gradient)

class RingAllReduce:
    def __init__(self, workers):
        self.workers = workers
        self.n = len(workers)
    
    def all_reduce(self, gradients):
        """Ring-AllReduce algorithm (simplified)"""
        # gradients: list of gradient arrays (one per worker)
        D = len(gradients[0])
        chunk_size = D // self.n
        
        # Scatter-Reduce phase
        accumulated = [g.copy() for g in gradients]
        for step in range(self.n - 1):
            for i in range(self.n):
                src = i
                dst = (i + 1) % self.n
                chunk_idx = (i - step) % self.n
                start = chunk_idx * chunk_size
                end = start + chunk_size
                
                # Worker dst receives chunk from worker src and accumulates
                accumulated[dst][start:end] += accumulated[src][start:end]
        
        # AllGather phase
        result = [np.zeros_like(g) for g in gradients]
        for step in range(self.n - 1):
            for i in range(self.n):
                src = i
                dst = (i + 1) % self.n
                chunk_idx = (i - step + 1) % self.n
                start = chunk_idx * chunk_size
                end = start + chunk_size
                
                # Worker dst receives accumulated chunk from src
                result[dst][start:end] = accumulated[src][start:end]
        
        # Average
        avg_gradient = sum(result) / self.n
        return avg_gradient

# Example: Parameter Server
dim = 10
ps = ParameterServer(dim)

# Generate synthetic data for workers
np.random.seed(42)
data_per_worker = 100
workers = []
for i in range(4):
    X = np.random.randn(data_per_worker, dim)
    y = X @ np.random.randn(dim) + np.random.randn(data_per_worker) * 0.1
    workers.append(Worker(i, ps, X, y))

# Synchronous training (sequential simulation)
print("=== Synchronous Training ===")
for _ in range(10):
    for w in workers:
        w.train_sync(1)

print(f"\nFinal params: {ps.params[:5]}...")
```

---

## Phase 2: Stress Questions

### Q1: Communication Bottleneck Analysis
**For N workers, D parameters, bandwidth B, compute time T_comp per batch:**
- **a)** Derive training time formula for Parameter Server
- **b)** Derive for Ring-AllReduce
- **c)** Find N where communication dominates

<details><summary>Hint</summary>
PS: T = T_comp + 2D/B (send + receive). Ring: T = T_comp + 2D(N-1)/(NB). Communication dominates when T_comm > T_comp.
</details>

### Q2: Async SGD Convergence
**Prove that asynchronous SGD with bounded staleness τ converges if learning rate η = O(1/√T) and τ = O(√T).**

<details><summary>Hint</summary>
Stale gradient g(θ_{t-τ}) ≈ g(θ_t) + ∇²f·(θ_{t-τ} - θ_t). Bound error using Lipschitz constant. Requires η small enough to overcome staleness.
</details>

### Q3: Large Batch Generalization
**Explain why doubling batch size (for parallelism) sometimes reduces test accuracy. Propose mitigation.**

<details><summary>Hint</summary>
Large batch → flatter minima → worse generalization. Mitigation: learning rate warmup, reduce batch size gradually, use ghost batch norm.
</details>

---

## Phase 3: Applied Problem

Train ResNet-50 on ImageNet with 64 GPUs:
- 1.2M images, batch size 32 per GPU
- Model: 25M parameters (100MB)
- GPUs: 100 GB/s interconnect

**Part A**: Compare Parameter Server vs Ring-AllReduce:
- Communication time per iteration
- Scalability to 128 GPUs

**Part B**: Implement gradient compression (top-10% sparsification).

**Part C**: Design fault tolerance (what if 1 GPU fails mid-training?).

```python
class DistributedTrainer:
    def __init__(self, model, n_workers, strategy='ring-allreduce'):
        self.model = model
        self.n_workers = n_workers
        self.strategy = strategy
    
    def compute_comm_time(self, params_size, bandwidth):
        """Compute communication time"""
        # TODO: Implement for PS and Ring-AllReduce
        pass
    
    def gradient_compression(self, gradients, sparsity=0.9):
        """Compress gradients (keep only top-k)"""
        # TODO: Zero out bottom 90% of gradients by magnitude
        pass
    
    def fault_tolerant_training(self, checkpoint_freq=100):
        """Handle worker failures"""
        # TODO: Checkpoint every N iterations, resume on failure
        pass
```

---

## Phase 4: Self-Assessment

### Checklist
- [ ] Understand data vs model parallelism
- [ ] Know Parameter Server vs AllReduce trade-offs
- [ ] Can analyze communication bottleneck
- [ ] Understand sync vs async SGD convergence
- [ ] Know gradient compression techniques

### Next Steps
- **Strong**: [[Session 21 – Service Mesh]]
- **Struggling**: Review [[Session 06 – ML & Optimization]]
- **Resources**: "Accurate, Large Minibatch SGD" (Goyal et al.), Horovod documentation

---

**Navigation**: ← [[Session 19]] | **Index**: [[cycle3/INDEX]] | → [[Session 21]]
