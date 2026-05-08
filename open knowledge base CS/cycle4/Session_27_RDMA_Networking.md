# Session 27 – RDMA & Kernel-Bypass Networking

**Cycle**: 4 (Expert Mastery)  
**Domain**: Networks & Distributed Systems  
**Difficulty**: ⚫⚫⚫⚫

**Prerequisites**: Network stack, DMA, memory hierarchy, cache coherence

---

## Phase 1: Core Theory & Mental Models

### 1.1 Definitions

**RDMA** (Remote Direct Memory Access): Network protocol allowing direct memory access between machines without CPU involvement.

**Verbs API**: Low-level RDMA programming interface (ibverbs in Linux).

**Queue Pair (QP)**: Bidirectional communication channel with Send Queue (SQ) and Receive Queue (RQ).

**Work Request (WR)**: Command posted to queue (SEND, RECV, RDMA READ, RDMA WRITE).

**Completion Queue (CQ)**: Asynchronous notification queue for completed operations.

**Memory Region (MR)**: Registered memory buffer accessible via RDMA.

**One-Sided Operations**: RDMA READ/WRITE that bypass remote CPU entirely.

### 1.2 Core Mechanisms

**RDMA Two-Sided Operations**:
```
Client:                    Server:
  post_send()                post_recv()
      ↓                          ↓
    [SQ] ───── network ─────► [RQ]
      ↓                          ↓
    [CQ] ← completion        [CQ]
```

**RDMA One-Sided WRITE**:
```
Client:
  post_rdma_write(remote_addr, local_buf, size)
      ↓
    [SQ] ───► NIC ───► Remote Memory (direct)
      ↓
    [CQ] ← completion

Server CPU: not involved!
```

**Memory Registration**:
```c
struct ibv_mr *mr = ibv_reg_mr(
    pd,                    // Protection domain
    buffer,                // Memory buffer
    size,                  // Buffer size
    IBV_ACCESS_LOCAL_WRITE | IBV_ACCESS_REMOTE_WRITE
);
// Returns: lkey (local key), rkey (remote key)
```

**Key Properties**:
- **Zero-copy**: Data transferred directly between NIC and application memory
- **Kernel bypass**: No system calls, no context switches
- **CPU offload**: NIC handles protocol processing
- **μs latency**: ~1-2μs one-way latency (vs ~10-50μs TCP)

### 1.3 Mental Models

**The Traditional Stack vs RDMA**:
```
Traditional:
  App → syscall → kernel → TCP/IP → NIC → wire
        many copies, context switches, CPU cycles

RDMA:
  App → NIC → wire
       zero-copy, kernel bypass, CPU-free
```

**Memory Semantics**: RDMA provides "memory-like" interface to remote machines - `WRITE(addr, val)` works the same for local and remote memory.

**Tradeoff**: RDMA sacrifices generality (requires special hardware, pinned memory) for performance.

### 1.4 Edge Cases

**Cache Coherence**: RDMA writes may bypass CPU cache, causing stale reads. Solution: memory barriers, cache invalidation.

**Memory Registration Overhead**: Pinning pages has cost - amortize via large registrations or on-demand paging (ODP).

**Lossless Fabric Required**: RDMA assumes reliable network (InfiniBand, RoCE). Regular Ethernet may drop packets.

**Receiver Not Ready**: If RECV not posted before SEND arrives, connection error. Requires careful protocol design.

### 1.5 Implementation

**RDMA Setup & One-Sided Write**:
```c
#include <infiniband/verbs.h>
#include <stdio.h>
#include <string.h>

// Simplified RDMA example (error checking omitted for clarity)

struct rdma_context {
    struct ibv_context *ctx;
    struct ibv_pd *pd;
    struct ibv_qp *qp;
    struct ibv_cq *cq;
    struct ibv_mr *mr;
    void *buffer;
};

void rdma_init(struct rdma_context *rctx) {
    // 1. Get device list
    struct ibv_device **dev_list = ibv_get_device_list(NULL);
    struct ibv_device *dev = dev_list[0];
    
    // 2. Open device
    rctx->ctx = ibv_open_device(dev);
    
    // 3. Allocate protection domain
    rctx->pd = ibv_alloc_pd(rctx->ctx);
    
    // 4. Create completion queue
    rctx->cq = ibv_create_cq(rctx->ctx, 10, NULL, NULL, 0);
    
    // 5. Create queue pair
    struct ibv_qp_init_attr qp_attr = {
        .send_cq = rctx->cq,
        .recv_cq = rctx->cq,
        .cap = {
            .max_send_wr = 10,
            .max_recv_wr = 10,
            .max_send_sge = 1,
            .max_recv_sge = 1
        },
        .qp_type = IBV_QPT_RC  // Reliable connection
    };
    rctx->qp = ibv_create_qp(rctx->pd, &qp_attr);
    
    // 6. Register memory
    rctx->buffer = malloc(4096);
    rctx->mr = ibv_reg_mr(rctx->pd, rctx->buffer, 4096,
                          IBV_ACCESS_LOCAL_WRITE | 
                          IBV_ACCESS_REMOTE_WRITE);
}

void rdma_write_one_sided(struct rdma_context *rctx,
                          uint64_t remote_addr,
                          uint32_t remote_rkey,
                          void *local_buf,
                          size_t size) {
    struct ibv_sge sge = {
        .addr = (uint64_t)local_buf,
        .length = size,
        .lkey = rctx->mr->lkey
    };
    
    struct ibv_send_wr wr = {
        .wr_id = 1,
        .sg_list = &sge,
        .num_sge = 1,
        .opcode = IBV_WR_RDMA_WRITE,
        .send_flags = IBV_SEND_SIGNALED,
        .wr.rdma = {
            .remote_addr = remote_addr,
            .rkey = remote_rkey
        }
    };
    
    struct ibv_send_wr *bad_wr;
    ibv_post_send(rctx->qp, &wr, &bad_wr);
    
    // Poll for completion
    struct ibv_wc wc;
    while (ibv_poll_cq(rctx->cq, 1, &wc) == 0);
    
    if (wc.status != IBV_WC_SUCCESS) {
        fprintf(stderr, "RDMA write failed\n");
    }
}

// Example usage
int main() {
    struct rdma_context client_ctx;
    rdma_init(&client_ctx);
    
    // Assume we have remote memory info from server
    uint64_t remote_addr = 0x12345678;  // From server
    uint32_t remote_rkey = 0xABCD;      // From server
    
    // Write "Hello RDMA" to remote memory
    char *msg = "Hello RDMA";
    rdma_write_one_sided(&client_ctx, remote_addr, remote_rkey,
                        msg, strlen(msg) + 1);
    
    printf("RDMA write completed\n");
    return 0;
}
```

**Python Wrapper (using pyverbs)**:
```python
from pyverbs.pd import PD
from pyverbs.cq import CQ
from pyverbs.qp import QP, QPInitAttr, QPAttr
from pyverbs.mr import MR
from pyverbs.wr import SendWR, SGE
from pyverbs.device import Context
import pyverbs.enums as e

class RDMAConnection:
    def __init__(self, device_name='mlx5_0'):
        self.ctx = Context(name=device_name)
        self.pd = PD(self.ctx)
        self.cq = CQ(self.ctx, 100, None, None, 0)
        
        # Create queue pair
        qp_init_attr = QPInitAttr(
            qp_type=e.IBV_QPT_RC,
            scq=self.cq,
            rcq=self.cq
        )
        self.qp = QP(self.pd, qp_init_attr)
        
        # Register memory
        self.buffer = bytearray(4096)
        self.mr = MR(self.pd, len(self.buffer), 
                     e.IBV_ACCESS_LOCAL_WRITE | 
                     e.IBV_ACCESS_REMOTE_WRITE)
    
    def rdma_write(self, remote_addr, remote_rkey, data):
        """
        One-sided RDMA WRITE
        """
        # Copy data to registered buffer
        self.buffer[:len(data)] = data
        
        # Create scatter-gather element
        sge = SGE(self.mr.buf, len(data), self.mr.lkey)
        
        # Create send work request
        wr = SendWR(
            opcode=e.IBV_WR_RDMA_WRITE,
            num_sge=1,
            sg=[sge]
        )
        wr.set_wr_flags(e.IBV_SEND_SIGNALED)
        wr.set_rdma_addr_key(remote_addr, remote_rkey)
        
        # Post send
        self.qp.post_send(wr)
        
        # Poll completion
        self.cq.poll()
        print(f"RDMA write of {len(data)} bytes completed")

# Usage
rdma = RDMAConnection()
rdma.rdma_write(remote_addr=0x1000, remote_rkey=0xABC, 
                data=b"Hello from RDMA")
```

---

## Phase 2: Conceptual Stress Questions

### Q1: Cache Coherence Problem
**Question**: Explain why RDMA one-sided writes can cause cache coherence issues and propose a solution.

<details>
<summary><strong>Hint</strong></summary>

RDMA NIC writes directly to memory, bypassing CPU cache. If CPU has cached the memory location, it will read stale data. Solutions: cache invalidation via `_mm_clflush()`, memory barriers, or using uncached memory regions.
</details>

---

### Q2: Memory Registration Overhead
**Question**: Memory registration (pinning pages) has significant overhead. How can distributed systems amortize this cost?

<details>
<summary><strong>Hint</strong></summary>

Strategies: (1) Register large memory pools upfront, (2) Use on-demand paging (ODP) if supported, (3) Cache registrations, (4) Use huge pages to reduce page count.
</details>

---

### Q3: Reliability and Ordering
**Question**: RDMA provides reliable connections (RC QP type). What guarantees does this provide, and what does the application still need to handle?

<details>
<summary><strong>Hint</strong></summary>

RC guarantees in-order delivery and no packet loss within a QP. But application must handle: (1) Connection failures, (2) Ordering across multiple QPs, (3) Synchronization between one-sided and two-sided operations.
</details>

---

## Phase 3: Applied Problem

### Problem: Implement Distributed Hash Table with RDMA

**Scenario**: Design a simple distributed hash table where clients use RDMA one-sided operations to read/write key-value pairs directly in server memory.

**Skeleton Code**:
```python
import hashlib

class RDMAHashTable:
    """
    Distributed hash table using RDMA one-sided operations
    """
    def __init__(self, num_servers, rdma_connections):
        """
        Args:
            num_servers: number of server nodes
            rdma_connections: list of RDMAConnection objects
        """
        self.num_servers = num_servers
        self.rdma_conns = rdma_connections
        
        # Hash table metadata (addr, rkey per server)
        self.server_info = []  # [(base_addr, rkey, size), ...]
    
    def hash_key(self, key):
        """Hash key to server ID"""
        h = hashlib.md5(key.encode()).digest()
        return int.from_bytes(h[:4], 'little') % self.num_servers
    
    def put(self, key, value):
        """
        RDMA WRITE key-value pair to remote server
        
        TODO:
        1. Hash key to determine server
        2. Calculate offset in server's memory region
        3. Serialize key-value pair
        4. RDMA WRITE to remote address
        5. Handle collisions (chaining or probing)
        """
        server_id = self.hash_key(key)
        # TODO: implement
        pass
    
    def get(self, key):
        """
        RDMA READ key-value pair from remote server
        
        TODO:
        1. Hash key to server
        2. RDMA READ from calculated offset
        3. Deserialize and return value
        4. Handle key not found
        """
        server_id = self.hash_key(key)
        # TODO: implement
        pass
    
    def atomic_cas(self, key, expected, new_value):
        """
        Compare-and-swap using RDMA atomic operations
        
        TODO:
        1. Use IBV_WR_ATOMIC_CMP_AND_SWP opcode
        2. Ensure atomicity for concurrent updates
        """
        pass

# Test
# Assume RDMA connections established to 3 servers
servers = 3
# rdma_conns = [RDMAConnection() for _ in range(servers)]
# ht = RDMAHashTable(servers, rdma_conns)

# ht.put("user:123", "Alice")
# value = ht.get("user:123")
# print(f"Retrieved: {value}")
```

**Expected Approach**:
1. Use consistent hashing to map keys to servers
2. RDMA WRITE for puts (zero-copy, CPU-offload)
3. RDMA READ for gets (direct memory access)
4. Handle concurrency via RDMA atomic operations or optimistic locking
5. Measure latency: should be ~1-2μs for local network

---

## Phase 4: Self-Assessment

### Checklist
- [ ] Understand RDMA verbs API (QP, CQ, MR, WR)
- [ ] Know difference between one-sided and two-sided operations
- [ ] Can explain zero-copy and kernel bypass benefits
- [ ] Aware of cache coherence issues with RDMA
- [ ] Can design distributed protocol using RDMA

### Reflection Questions
1. Why does RDMA achieve μs latency vs ms for TCP?
2. What are the limitations of RDMA (hardware, programming complexity)?
3. How do modern systems (FaRM, HERD) leverage RDMA for distributed transactions?

### Next Steps
- **Deepen**: Study RDMA atomic operations, unreliable datagrams (UD QP)
- **Connect**: Relate to distributed shared memory (DSM), PGAS languages
- **Apply**: Benchmark RDMA vs TCP for specific workload

**Related Sessions**:
- ← [Session 26: NewSQL Systems](Session_26_NewSQL_Systems.md)
- → [Session 28: Federated Learning](Session_28_Federated_Learning.md)

---

*Session 27 of Cycle 4 • Expert Mastery*
