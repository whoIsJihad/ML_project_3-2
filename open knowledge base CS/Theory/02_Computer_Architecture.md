# Computer Architecture

## Quick Reference
**Reading Time:** ~2 hours  
**Prerequisites:** [[01_Digital_Logic_Design]]  
**Next:** [[03_Microprocessors_Microcontrollers]]

---

## 1. Instruction Set Architecture (ISA)

### ISA Definition
**Interface between hardware and software**
- Defines: instructions, registers, addressing modes, memory model, interrupts
- Examples: x86-64, ARM, RISC-V, MIPS

### ISA Classifications

**CISC (Complex Instruction Set Computer):**
- Many specialized instructions
- Variable-length encoding
- Complex addressing modes
- Microcode implementation
- Example: x86
- **Pros:** Code density, backward compatibility
- **Cons:** Complex decode, harder to pipeline

**RISC (Reduced Instruction Set Computer):**
- Simple, uniform instructions
- Fixed-length encoding (usually 32-bit)
- Load/store architecture
- Many general-purpose registers
- Examples: ARM, RISC-V, MIPS
- **Pros:** Simple decode, easy pipeline, efficient
- **Cons:** More instructions needed, larger code

### Instruction Format
```
| Opcode | Rd | Rs1 | Rs2 | Immediate/Offset |
```
- **Opcode:** Operation to perform
- **Rd:** Destination register
- **Rs1, Rs2:** Source registers
- **Immediate:** Constant value or offset

**Types:**
- **R-Type:** Register-register (add, sub, and)
- **I-Type:** Immediate operations (addi, load)
- **S-Type:** Store operations
- **B-Type:** Branch operations
- **J-Type:** Jump operations

### Addressing Modes
1. **Immediate:** Operand in instruction `addi r1, r2, 5`
2. **Register:** Operand in register `add r1, r2, r3`
3. **Direct:** Address in instruction `load r1, [1000]`
4. **Indirect:** Address in register `load r1, [r2]`
5. **Indexed:** Base + offset `load r1, [r2 + 100]`
6. **PC-Relative:** PC + offset (for branches)
7. **Auto-increment:** Address in register, then increment

---

## 2. CPU Organization

### Von Neumann Architecture
- **Single memory** for instructions and data
- **Bottleneck:** Memory bandwidth (Von Neumann bottleneck)
- **Advantage:** Flexibility (self-modifying code possible)

### Harvard Architecture
- **Separate memories** for instructions and data
- **Advantage:** Parallel instruction fetch and data access
- **Used in:** DSPs, microcontrollers, modern CPU caches

### Basic CPU Components

**Datapath:**
- ALU (Arithmetic Logic Unit)
- Registers (register file)
- Multiplexers
- Buses

**Control Unit:**
- Instruction decoder
- Control signal generator
- Sequencing logic

**Registers:**
- **PC (Program Counter):** Address of next instruction
- **IR (Instruction Register):** Current instruction
- **MAR (Memory Address Register):** Address for memory access
- **MDR (Memory Data Register):** Data to/from memory
- **General Purpose Registers:** Data storage (r0-r31 typical)

---

## 3. Instruction Execution Cycle

### Classic 5-Stage Pipeline
1. **IF (Instruction Fetch):** Read instruction from memory
2. **ID (Instruction Decode):** Decode instruction, read registers
3. **EX (Execute):** Perform ALU operation
4. **MEM (Memory Access):** Read/write data memory
5. **WB (Write Back):** Write result to register

### Single-Cycle Implementation
- Each instruction completes in one clock cycle
- Clock cycle determined by slowest instruction
- Simple but inefficient (low clock frequency)

### Multi-Cycle Implementation
- Break instruction into multiple cycles
- Different instructions take different number of cycles
- Higher clock frequency possible
- Requires state machine control

### Pipelined Implementation
- Multiple instructions in flight simultaneously
- Throughput: ~1 instruction per cycle (ideal)
- Latency: Still 5 cycles per instruction
- **Speedup:** Up to N× for N-stage pipeline (ideally)

---

## 4. Pipelining

### Pipeline Hazards

**1. Structural Hazards**
- **Cause:** Hardware resource conflict
- **Example:** Single memory for instruction and data
- **Solution:** Separate I-cache and D-cache (Harvard architecture)

**2. Data Hazards**
**RAW (Read After Write):** True dependency
```
add r1, r2, r3
sub r4, r1, r5  # r1 not ready yet
```

**WAR (Write After Read):** Anti-dependency (not a problem in simple 5-stage)
**WAW (Write After Write):** Output dependency

**Solutions:**
- **Forwarding/Bypassing:** Route data from EX/MEM stages directly
- **Stalling:** Insert bubbles (NOPs) until data ready
- **Compiler scheduling:** Reorder independent instructions

**3. Control Hazards (Branch Hazards)**
- **Cause:** Don't know next PC until branch resolves
- **Cost:** 2-3 cycle penalty if branch taken

**Solutions:**
- **Predict Not Taken:** Continue with next instruction, flush if wrong
- **Predict Taken:** Requires early PC calculation
- **Branch Delay Slot:** Execute next instruction regardless (MIPS)
- **Branch Prediction:** Guess branch outcome dynamically

### Branch Prediction

**Static Prediction:**
- Always predict taken or not taken
- Backward branches (loops) predict taken
- Forward branches predict not taken

**Dynamic Prediction:**
- **1-bit predictor:** Remember last outcome (50% accuracy for loops)
- **2-bit saturating counter:** Predict same direction twice before flip
  - States: Strongly Taken, Weakly Taken, Weakly Not Taken, Strongly Not Taken
  - Better for loops (∼85-90% accuracy)
- **Branch History Table (BHT):** Array of 2-bit counters indexed by PC
- **Branch Target Buffer (BTB):** Cache of branch targets (avoid PC calculation)

**Advanced Predictors:**
- **Correlating/Two-Level:** Use history of recent branches
- **Tournament/Hybrid:** Multiple predictors, meta-predictor chooses best
- **Neural/Perceptron:** ML-based prediction

---

## 5. Memory Hierarchy

### Hierarchy Levels (Fast → Slow, Small → Large)
1. **Registers:** <1 ns, ~100s bytes
2. **L1 Cache:** ~1 ns, 32-64 KB per core
3. **L2 Cache:** ~3-10 ns, 256 KB - 1 MB per core
4. **L3 Cache:** ~10-30 ns, 4-32 MB shared
5. **Main Memory (DRAM):** ~100 ns, GBs
6. **SSD:** ~100 μs, 100s GB - TBs
7. **HDD:** ~10 ms, TBs

### Cache Principles

**Temporal Locality:** Recently accessed data likely accessed again
**Spatial Locality:** Nearby data likely accessed soon

**Cache Line/Block:** Unit of transfer (typically 64 bytes)

### Cache Organization

**Direct-Mapped Cache:**
- Each memory block maps to exactly one cache line
- **Index:** $(address / block\_size) \mod cache\_lines$
- **Fast but high conflict rate**

**Fully Associative Cache:**
- Block can go anywhere in cache
- Requires comparing all tags (expensive)
- **Best hit rate, slowest**

**N-Way Set-Associative Cache:**
- Divide cache into sets
- Block maps to one set, can be in any way within set
- **Set index:** $(address / block\_size) \mod num\_sets$
- **Typical:** 4-way or 8-way
- **Balance of speed and hit rate**

### Cache Address Breakdown
```
| Tag | Index | Offset |
```
- **Offset:** Byte within block ($\log_2(block\_size)$ bits)
- **Index:** Which set/line ($\log_2(num\_sets)$ bits)
- **Tag:** Identify which block (remaining bits)

### Cache Policies

**Replacement:**
- **LRU (Least Recently Used):** Replace oldest access (most common)
- **FIFO:** Replace oldest allocation
- **Random:** Simple, reasonable performance
- **LFU (Least Frequently Used):** Track access frequency

**Write Policies:**
- **Write-Through:** Write to both cache and memory
  - Simple, consistent
  - Slow, high memory traffic
  - Usually with write buffer
- **Write-Back:** Write only to cache, mark dirty
  - Fast, low memory traffic
  - Complex, requires dirty bit
  - Write to memory on eviction

**Write Miss:**
- **Write-Allocate:** Load block into cache on write miss (with write-back)
- **No-Write-Allocate:** Write directly to memory (with write-through)

### Cache Performance

**Hit Rate (h):** Fraction of accesses in cache  
**Miss Rate (m):** $m = 1 - h$

**Average Memory Access Time (AMAT):**
$$AMAT = t_{hit} + m \cdot t_{miss\_penalty}$$

**Effective CPI:**
$$CPI_{eff} = CPI_{ideal} + m_{I\$} \cdot Penalty_{I\$} + m_{D\$} \cdot Penalty_{D\$}$$

---

## 6. Superscalar & Out-of-Order Execution

### Superscalar Architecture
- **Multiple instructions issued per cycle**
- **Example:** Fetch/decode/execute 4 instructions simultaneously
- **Requires:** Multiple ALUs, load/store units, register ports

**IPC (Instructions Per Cycle):**
- Single-issue: IPC ≤ 1
- Superscalar: IPC > 1
- Modern CPUs: IPC ≈ 2-4 average, up to 5-6 peak

### Out-of-Order (OoO) Execution

**Motivation:** Avoid stalling on data hazards

**Components:**
1. **Reservation Stations:** Hold instructions waiting for operands
2. **Register Renaming:** Eliminate false dependencies (WAR, WAW)
   - Map architectural registers to physical registers
   - Example: 16 architectural regs → 100+ physical regs
3. **Reorder Buffer (ROB):** Maintain program order for commit
4. **Issue Logic:** Select ready instructions to execute

**Tomasulo's Algorithm:**
- Dynamic instruction scheduling
- Register renaming via tags
- Common data bus broadcasts results

**Steps:**
1. **Issue:** Decode and enter reservation station
2. **Execute:** When operands ready, execute out of order
3. **Write Back:** Broadcast result on common data bus
4. **Commit:** Retire instructions in program order from ROB

**Benefits:**
- Tolerate cache misses (execute independent instructions)
- Exploit instruction-level parallelism (ILP)

---

## 7. Parallelism & Multicore

### Flynn's Taxonomy
- **SISD:** Single Instruction, Single Data (traditional CPU)
- **SIMD:** Single Instruction, Multiple Data (vector processors, GPUs)
- **MISD:** Multiple Instruction, Single Data (rare)
- **MIMD:** Multiple Instruction, Multiple Data (multicore, multiprocessor)

### SIMD (Vector Processing)
- One instruction operates on multiple data elements
- **Examples:** SSE, AVX (x86), NEON (ARM)
- **Vector Length:** 128-bit (4×32-bit), 256-bit (8×32-bit), 512-bit (16×32-bit)
- **Use Cases:** Multimedia, scientific computing, ML

### Multicore Architecture

**Symmetric Multiprocessing (SMP):**
- Multiple cores, shared memory
- Each core has private L1/L2, shared L3
- Cache coherence protocols required

**Cache Coherence:**
**Problem:** Multiple caches may have different values for same address

**MESI Protocol (Most Common):**
- **M (Modified):** Exclusive, dirty (only copy, modified)
- **E (Exclusive):** Exclusive, clean (only copy, not modified)
- **S (Shared):** Multiple caches have copy, clean
- **I (Invalid):** Not valid

**Transitions:**
- Read miss → Broadcast on bus
- Write → Invalidate other caches

**Snooping:** Each cache monitors bus for relevant addresses  
**Directory-Based:** Centralized directory tracks cache copies (scalable)

### Multithreading

**Coarse-Grained:** Switch threads on long-latency events (cache miss)  
**Fine-Grained:** Switch threads every cycle (interleaved)  
**Simultaneous Multithreading (SMT/Hyper-Threading):**
- Multiple threads share execution units
- Increase resource utilization
- Example: Intel HT (2 threads per core)

---

## 8. Memory Systems

### Virtual Memory

**Purpose:**
- Isolate processes (protection)
- Larger address space than physical memory
- Simplified programming (contiguous addresses)

**Virtual Address → Physical Address:**
1. **Page Table:** Map virtual page → physical frame
2. **TLB (Translation Lookaside Buffer):** Cache of recent translations
3. **Page Fault:** Requested page not in memory, load from disk

**Address Translation:**
```
Virtual Address: | VPN (Virtual Page Number) | Offset |
Physical Address: | PFN (Physical Frame Number) | Offset |
```

**Page Table Entry (PTE):**
- Physical frame number
- Valid bit (in memory?)
- Dirty bit (modified?)
- Reference bit (recently accessed?)
- Protection bits (read/write/execute)

**Multi-Level Page Tables:**
- Reduce page table memory overhead
- Example: 4-level (x86-64), 3-level (ARM)
- Only allocate tables for used regions

**TLB:**
- Fast cache of virtual → physical mappings
- Fully associative or set-associative
- 64-512 entries typical
- **TLB Miss:** Requires page table walk (expensive)

### DRAM Organization

**Rows, Columns, Banks:**
- **Row Buffer:** Caching row data
- **Row Hit:** Access open row (fast, ~15 ns)
- **Row Miss:** Close row, open new row (slow, ~50 ns)
- **Bank Interleaving:** Multiple banks allow parallel access

**DRAM Refresh:** Capacitors leak, must refresh every ~64 ms

**DDR (Double Data Rate):**
- Transfer on both clock edges
- DDR4: ~2400-3200 MT/s
- DDR5: ~4800-6400 MT/s

---

## 9. Input/Output (I/O)

### I/O Techniques

**1. Programmed I/O (Polling):**
- CPU repeatedly checks device status
- Simple but wastes CPU cycles

**2. Interrupt-Driven I/O:**
- Device signals CPU when ready
- CPU handles via interrupt handler
- Better CPU utilization
- Overhead for many small transfers

**3. DMA (Direct Memory Access):**
- Dedicated hardware transfers data without CPU
- CPU sets up transfer, DMA controller executes
- Interrupt when complete
- Best for large transfers

### Interrupts

**Interrupt Vector Table:** Array of handler addresses  
**Priority:** Some interrupts higher priority (e.g., hardware faults)  
**Maskable vs Non-Maskable:** Can CPU disable interrupt?

**Handling Steps:**
1. Finish current instruction
2. Save PC and processor state
3. Disable interrupts (if maskable)
4. Jump to interrupt handler (via vector)
5. Execute handler
6. Restore state and return

### I/O Buses
- **Address Bus:** Select device/register
- **Data Bus:** Transfer data
- **Control Bus:** Read/write signals

**Examples:**
- PCIe: High-speed peripheral (GPUs, NVMe)
- USB: External devices
- SATA: Storage

---

## 10. Performance Metrics

### Latency vs Throughput
- **Latency:** Time per operation
- **Throughput:** Operations per time

### Execution Time
$$Time = Instructions \times CPI \times Cycle\ Time$$
$$Time = \frac{Instructions \times CPI}{Frequency}$$

### Speedup
$$Speedup = \frac{Time_{old}}{Time_{new}}$$

### Amdahl's Law
**Limited speedup from optimizing part of program:**
$$Speedup_{overall} = \frac{1}{(1-f) + \frac{f}{s}}$$
- $f$: Fraction enhanced
- $s$: Speedup of that fraction

**Implication:** Optimize common case, diminishing returns on rare cases

### CPI Calculation
$$CPI = CPI_{ideal} + Stalls_{data} + Stalls_{control} + Stalls_{structural}$$

### MIPS (Misleading!)
$$MIPS = \frac{Frequency}{CPI \times 10^6}$$
- **Problem:** Different ISAs, different work per instruction

---

## 11. Advanced Topics Overview

### Very Long Instruction Word (VLIW)
- Compiler bundles multiple operations
- Hardware executes bundle in parallel
- Simple hardware, complex compiler
- Example: Intel Itanium

### Speculative Execution
- Execute instructions before knowing if needed
- Branch prediction + execution
- Security concerns (Spectre/Meltdown)

### Power & Energy
**Dynamic Power:** $P_{dyn} \propto f \cdot V^2$  
**Static Power:** Leakage current

**Techniques:**
- Dynamic Voltage/Frequency Scaling (DVFS)
- Clock gating (disable unused units)
- Power gating (turn off unused units)

### Quantum Computing (Emerging)
- Qubits (superposition + entanglement)
- Quantum gates
- Dramatically different architecture paradigm

---

## Key Concepts Summary

| Concept | Core Principle |
|---------|----------------|
| **ISA** | Contract between hardware and software |
| **Pipelining** | Overlap instruction execution stages |
| **Hazards** | Pipeline stalls from resource/data/control conflicts |
| **Cache** | Exploit locality for fast average access |
| **OoO Execution** | Execute independent instructions out of order |
| **Virtual Memory** | Isolate processes, larger address space |
| **Cache Coherence** | Keep multiple caches consistent |
| **Amdahl's Law** | Diminishing returns from partial optimization |

---

## Common Pitfalls

1. **Ignoring hazards in pipeline** → Incorrect results
2. **Confusing throughput and latency** → Wrong bottleneck analysis
3. **Forgetting write-back on cache eviction** → Data loss
4. **Not considering TLB misses** → Underestimate memory latency
5. **Assuming linear speedup** → Amdahl's Law violation
6. **Mixing physical and virtual addresses** → Incorrect memory access
7. **Ignoring cache line size** → Poor spatial locality

---

## Cross-Links
- [[01_Digital_Logic_Design]] - Hardware building blocks
- [[03_Microprocessors_Microcontrollers]] - Specific implementations
- [[05_Memory_Systems]] - Deep dive on memory
- [[Session_01_Memory_Hierarchy_Cost_Model]] - Performance modeling
- [[Session_02_Algorithms_Complexity]] - Algorithm efficiency on real hardware

---

## Quick Formulas

**AMAT:** $AMAT = t_{cache} + miss\_rate \times t_{mem}$  
**Speedup:** $S = \frac{T_{old}}{T_{new}}$  
**Amdahl:** $S = \frac{1}{(1-f) + f/s}$  
**Execution Time:** $T = \frac{Instructions \times CPI}{f_{clock}}$  
**CPI with cache misses:** $CPI = CPI_{ideal} + miss\_rate \times miss\_penalty$
