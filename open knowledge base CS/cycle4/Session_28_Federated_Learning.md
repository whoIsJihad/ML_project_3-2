# Session 28 – Federated Learning & Privacy-Preserving ML

**Cycle**: 4 (Expert Mastery)  
**Domain**: ML & Optimization + Systems Design Integration  
**Difficulty**: ⚫⚫⚫⚫

**Prerequisites**: Distributed training, differential privacy, cryptography basics

---

## Phase 1: Core Theory & Mental Models

### 1.1 Definitions

**Federated Learning (FL)**: Distributed machine learning where training data remains on edge devices; only model updates are shared.

**FederatedAveraging (FedAvg)**: Standard FL algorithm where clients train locally, server aggregates updates.

**Differential Privacy (DP)**: Mathematical framework guaranteeing that individual training examples don't significantly affect model output.

**ε-Differential Privacy**: Algorithm M satisfies ε-DP if for any two datasets D, D' differing by one element:
```
P(M(D) ∈ S) ≤ e^ε · P(M(D') ∈ S)
```
for all output sets S.

**Secure Aggregation**: Cryptographic protocol allowing server to compute sum of client updates without seeing individual updates.

**Non-IID Data**: Clients have heterogeneous data distributions (violates i.i.d. assumption of standard ML).

### 1.2 Core Mechanisms

**FederatedAveraging Algorithm**:
```
Server:
  Initialize model w_0
  for each round t = 1, 2, ..., T:
    Sample subset of clients C_t
    Send w_t to each client in C_t
    Receive updates Δw_i from clients
    Aggregate: w_{t+1} = w_t + (1/|C_t|) Σ Δw_i

Client i:
  Receive model w_t from server
  Train on local data D_i for E epochs
  Compute update: Δw_i = w'_i - w_t
  Send Δw_i to server
```

**DP-SGD (Differentially Private SGD)**:
```python
def dp_sgd_step(model, batch, sensitivity, sigma, clip_norm):
    """
    One step of DP-SGD
    
    1. Compute per-example gradients
    2. Clip each gradient to bounded sensitivity
    3. Add Gaussian noise ~ N(0, σ²)
    4. Average and apply to model
    """
    per_example_grads = compute_per_example_gradients(model, batch)
    
    # Clip gradients
    clipped_grads = [clip_gradient(g, clip_norm) for g in per_example_grads]
    
    # Aggregate
    avg_grad = sum(clipped_grads) / len(clipped_grads)
    
    # Add noise
    noise = torch.randn_like(avg_grad) * sigma * clip_norm
    noisy_grad = avg_grad + noise
    
    # Update model
    model.update(noisy_grad)
    
    return model
```

**Privacy Accounting**: Total privacy loss ε accumulates over training steps. Use moments accountant or Rényi DP for tighter bounds.

**Secure Aggregation (Simplified)**:
```
Goal: Server computes Σ x_i without learning individual x_i

Protocol:
1. Each client i samples random mask r_i
2. Client i shares r_i with client i+1, receives r_{i-1} from client i-1
3. Client i sends: y_i = x_i + r_i - r_{i-1}
4. Server computes: Σ y_i = Σ (x_i + r_i - r_{i-1}) = Σ x_i
   (masks cancel out: Σ r_i - Σ r_{i-1} = 0)
```

### 1.3 Mental Models

**The Privacy-Utility Tradeoff**:
```
More Privacy (larger ε, σ) ↔ Lower Model Accuracy
Fewer Clients Participating ↔ More Bias (non-IID)
More Communication Rounds ↔ Better Convergence but Higher Cost
```

**FL as "Distributed Optimization with Constraints"**:
- Objective: minimize global loss
- Constraints: data locality, communication efficiency, privacy

**Non-IID Visualization**: Imagine digit recognition where:
- Client A has mostly 0s and 1s
- Client B has mostly 8s and 9s
→ Standard averaging may not converge well

### 1.4 Edge Cases

**Client Dropout**: Clients may disconnect mid-training. Requires robust aggregation.

**Byzantine Clients**: Malicious clients sending corrupted updates. Needs Byzantine-robust aggregation (e.g., Krum, median).

**System Heterogeneity**: Clients have different compute/network capabilities. Stragglers slow down rounds.

**Privacy Amplification**: Subsampling clients each round amplifies privacy (smaller ε).

### 1.5 Implementation

**FedAvg Implementation**:
```python
import torch
import torch.nn as nn
import copy

class FederatedServer:
    def __init__(self, model, num_clients, client_fraction=0.1):
        self.global_model = model
        self.num_clients = num_clients
        self.client_fraction = client_fraction
    
    def select_clients(self, round_num):
        """Randomly sample clients for this round"""
        num_selected = max(1, int(self.client_fraction * self.num_clients))
        return np.random.choice(self.num_clients, num_selected, replace=False)
    
    def aggregate(self, client_updates):
        """
        Aggregate client updates (FedAvg)
        
        Args:
            client_updates: list of (client_id, state_dict, num_samples)
        
        Returns:
            Updated global model
        """
        # Weighted average by number of samples
        total_samples = sum(num_samples for _, _, num_samples in client_updates)
        
        global_dict = self.global_model.state_dict()
        
        for key in global_dict.keys():
            global_dict[key] = torch.zeros_like(global_dict[key])
            
            for client_id, state_dict, num_samples in client_updates:
                weight = num_samples / total_samples
                global_dict[key] += weight * state_dict[key]
        
        self.global_model.load_state_dict(global_dict)
        return self.global_model
    
    def train_round(self, clients, round_num):
        """Execute one federated round"""
        selected_ids = self.select_clients(round_num)
        client_updates = []
        
        for client_id in selected_ids:
            client = clients[client_id]
            updated_model, num_samples = client.train(self.global_model)
            client_updates.append((client_id, updated_model.state_dict(), num_samples))
        
        self.aggregate(client_updates)
        return len(selected_ids)

class FederatedClient:
    def __init__(self, client_id, train_data, local_epochs=5, lr=0.01):
        self.client_id = client_id
        self.train_data = train_data
        self.local_epochs = local_epochs
        self.lr = lr
    
    def train(self, global_model):
        """
        Train on local data
        
        Returns:
            (updated_model, num_samples)
        """
        model = copy.deepcopy(global_model)
        optimizer = torch.optim.SGD(model.parameters(), lr=self.lr)
        criterion = nn.CrossEntropyLoss()
        
        model.train()
        for epoch in range(self.local_epochs):
            for batch_x, batch_y in self.train_data:
                optimizer.zero_grad()
                output = model(batch_x)
                loss = criterion(output, batch_y)
                loss.backward()
                optimizer.step()
        
        num_samples = len(self.train_data.dataset)
        return model, num_samples

# Example usage
model = SimpleCNN()  # Your model
num_clients = 100
server = FederatedServer(model, num_clients, client_fraction=0.1)

# Simulate clients with local data
clients = [FederatedClient(i, client_data[i]) for i in range(num_clients)]

# Federated training
for round_num in range(100):
    num_participated = server.train_round(clients, round_num)
    print(f"Round {round_num}: {num_participated} clients participated")
```

**DP-SGD with Gradient Clipping**:
```python
def clip_gradient(grad, max_norm):
    """Clip gradient to max_norm (for DP)"""
    grad_norm = torch.norm(grad)
    clip_coef = max_norm / (grad_norm + 1e-6)
    return grad * min(1.0, clip_coef)

class DPFederatedClient(FederatedClient):
    def __init__(self, *args, noise_multiplier=1.0, clip_norm=1.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.noise_multiplier = noise_multiplier
        self.clip_norm = clip_norm
    
    def train(self, global_model):
        """Train with differential privacy"""
        model = copy.deepcopy(global_model)
        optimizer = torch.optim.SGD(model.parameters(), lr=self.lr)
        criterion = nn.CrossEntropyLoss()
        
        model.train()
        for epoch in range(self.local_epochs):
            for batch_x, batch_y in self.train_data:
                optimizer.zero_grad()
                
                # Compute per-example gradients (simplified: use batch)
                output = model(batch_x)
                loss = criterion(output, batch_y)
                loss.backward()
                
                # Clip and add noise to gradients
                with torch.no_grad():
                    for param in model.parameters():
                        if param.grad is not None:
                            # Clip
                            param.grad = clip_gradient(param.grad, self.clip_norm)
                            
                            # Add Gaussian noise
                            noise = torch.randn_like(param.grad) * \
                                   self.noise_multiplier * self.clip_norm
                            param.grad += noise
                
                optimizer.step()
        
        num_samples = len(self.train_data.dataset)
        return model, num_samples
```

---

## Phase 2: Conceptual Stress Questions

### Q1: Non-IID Convergence
**Question**: Prove or provide intuition why FedAvg may diverge when client data is highly non-IID.

<details>
<summary><strong>Hint</strong></summary>

Each client's local update optimizes a different objective (local loss). When aggregated, updates may point in conflicting directions, causing oscillation or divergence. Solutions: FedProx (add proximal term), personalization layers.
</details>

---

### Q2: Privacy Budget Exhaustion
**Question**: In DP-SGD, privacy budget ε increases with training iterations. How can you train longer without violating privacy?

<details>
<summary><strong>Hint</strong></summary>

Use privacy amplification via subsampling (smaller batch → smaller ε per step). Use advanced accounting (Rényi DP). Trade off: larger noise multiplier σ for same target ε.
</details>

---

### Q3: Secure Aggregation Overhead
**Question**: Secure aggregation adds cryptographic overhead. Under what conditions is the communication cost acceptable?

<details>
<summary><strong>Hint</strong></summary>

Cost ~ O(n²) for pairwise key exchange, or O(n log n) for tree-based protocols. Acceptable when: (1) client updates are large (amortized), (2) number of clients moderate, (3) privacy gain outweighs cost.
</details>

---

## Phase 3: Applied Problem

### Problem: Implement Federated Learning with Privacy

**Scenario**: Train a federated model with differential privacy guarantees. Measure privacy-accuracy tradeoff.

**Skeleton Code**:
```python
import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset

def create_non_iid_data(num_clients, num_classes=10):
    """
    Create non-IID data partitions for clients
    Each client gets data from subset of classes
    
    TODO:
    1. Generate or load dataset (e.g., MNIST)
    2. Partition by class (e.g., clients 0-9 get class 0-1, etc.)
    3. Return list of DataLoaders
    """
    pass

def measure_privacy_accuracy_tradeoff(noise_multipliers, num_rounds=50):
    """
    Train federated models with different privacy levels
    
    Returns:
        List of (noise_multiplier, final_accuracy, privacy_epsilon)
    """
    results = []
    
    for noise_mult in noise_multipliers:
        # TODO:
        # 1. Initialize server and DP clients
        # 2. Train for num_rounds
        # 3. Evaluate final accuracy on test set
        # 4. Compute total privacy cost ε using privacy accounting
        # 5. Append (noise_mult, accuracy, epsilon) to results
        pass
    
    return results

def plot_privacy_utility_curve(results):
    """
    Plot accuracy vs privacy budget (1/ε)
    """
    import matplotlib.pyplot as plt
    
    epsilons = [r[2] for r in results]
    accuracies = [r[1] for r in results]
    
    plt.plot(epsilons, accuracies, marker='o')
    plt.xlabel('Privacy Budget ε (lower = more private)')
    plt.ylabel('Test Accuracy')
    plt.title('Privacy-Utility Tradeoff in Federated Learning')
    plt.grid(True)
    plt.show()

# Test
noise_multipliers = [0.5, 1.0, 1.5, 2.0, 3.0]
# results = measure_privacy_accuracy_tradeoff(noise_multipliers)
# plot_privacy_utility_curve(results)
```

**Expected Approach**:
1. Implement DP-FedAvg with gradient clipping and noise
2. Use Gaussian mechanism for (ε, δ)-DP
3. Track privacy budget across rounds using moments accountant
4. Measure accuracy drop as noise increases
5. Verify: higher noise → lower ε (more private) but lower accuracy

---

## Phase 4: Self-Assessment

### Checklist
- [ ] Understand FedAvg algorithm and convergence challenges
- [ ] Can explain differential privacy formally (ε-DP)
- [ ] Know DP-SGD mechanism (clip + noise)
- [ ] Familiar with secure aggregation protocols
- [ ] Aware of non-IID data problem and solutions

### Reflection Questions
1. Why is federated learning necessary (vs centralized training)?
2. How does differential privacy quantify information leakage?
3. What are the systems challenges in deploying FL at scale (millions of devices)?

### Next Steps
- **Deepen**: Study personalized FL, federated transfer learning, FL for NLP
- **Connect**: Relate to distributed optimization, privacy-preserving computation (MPC, homomorphic encryption)
- **Apply**: Implement FL system for real-world application (healthcare, mobile keyboards)

**Related Sessions**:
- ← [Session 27: RDMA Networking](Session_27_RDMA_Networking.md)
- 🎯 **Cycle 4 Complete"✓ Session 27 created"* Return to [Cycle 4 Index](INDEX.md)

---

*Session 28 of Cycle 4 • Expert Mastery - Final Session! 🎉*
