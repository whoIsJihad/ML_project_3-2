# Digital Logic Design

## Quick Reference
**Reading Time:** ~2 hours  
**Prerequisites:** Basic binary arithmetic  
**Next:** [[02_Computer_Architecture]]

---

## 1. Number Systems & Codes

### Binary, Octal, Hexadecimal
- **Binary:** Base-2 (0, 1)
- **Octal:** Base-8 (0-7)
- **Hexadecimal:** Base-16 (0-9, A-F)

**Conversion:**
- Binary to Decimal: $\sum_{i=0}^{n-1} b_i \cdot 2^i$
- Decimal to Binary: Repeated division by 2
- Hex to Binary: Each hex digit = 4 binary bits

### Signed Number Representations
1. **Sign-Magnitude:** MSB = sign, rest = magnitude
2. **1's Complement:** Invert all bits for negative
3. **2's Complement:** Invert and add 1 (most common)
   - Range: $[-2^{n-1}, 2^{n-1}-1]$ for n bits
   - Addition works directly, no special handling

### Binary Codes
- **BCD (Binary-Coded Decimal):** Each decimal digit in 4 bits
- **Gray Code:** Adjacent values differ by 1 bit (error reduction)
- **ASCII:** 7-bit character encoding

---

## 2. Boolean Algebra

### Fundamental Laws
| Law | AND Form | OR Form |
|-----|----------|---------|
| Identity | $A \cdot 1 = A$ | $A + 0 = A$ |
| Null | $A \cdot 0 = 0$ | $A + 1 = 1$ |
| Idempotent | $A \cdot A = A$ | $A + A = A$ |
| Complement | $A \cdot \overline{A} = 0$ | $A + \overline{A} = 1$ |
| Involution | $\overline{\overline{A}} = A$ | |
| Commutative | $A \cdot B = B \cdot A$ | $A + B = B + A$ |
| Associative | $(A \cdot B) \cdot C = A \cdot (B \cdot C)$ | $(A + B) + C = A + (B + C)$ |
| Distributive | $A + (B \cdot C) = (A+B) \cdot (A+C)$ | $A \cdot (B + C) = A \cdot B + A \cdot C$ |
| Absorption | $A + (A \cdot B) = A$ | $A \cdot (A + B) = A$ |
| De Morgan's | $\overline{A \cdot B} = \overline{A} + \overline{B}$ | $\overline{A + B} = \overline{A} \cdot \overline{B}$ |

### Standard Forms
- **SOP (Sum of Products):** OR of AND terms (minterms)
- **POS (Product of Sums):** AND of OR terms (maxterms)
- **Canonical Forms:** Include all variables in each term

---

## 3. Logic Gates

### Basic Gates
| Gate | Symbol | Expression | Truth |
|------|--------|------------|-------|
| NOT | Inverter | $Y = \overline{A}$ | $0 \to 1, 1 \to 0$ |
| AND | · | $Y = A \cdot B$ | Only 1 when all 1 |
| OR | + | $Y = A + B$ | 1 when any 1 |
| NAND | ⊼ | $Y = \overline{A \cdot B}$ | Universal gate |
| NOR | ⊽ | $Y = \overline{A + B}$ | Universal gate |
| XOR | ⊕ | $Y = A \oplus B$ | 1 when inputs differ |
| XNOR | ⊙ | $Y = \overline{A \oplus B}$ | 1 when inputs same |

**Universal Gates:** NAND and NOR can implement any Boolean function.

### Gate Delays & Propagation
- **Propagation Delay ($t_p$):** Time from input change to output stable
- **Critical Path:** Longest delay path through circuit
- **Glitches:** Temporary incorrect outputs due to unequal delays

---

## 4. Combinational Logic Design

### Karnaugh Maps (K-Maps)
**Purpose:** Minimize Boolean expressions visually

**Process:**
1. Fill truth table
2. Create K-map grid (Gray code ordering)
3. Group adjacent 1s in powers of 2 (1, 2, 4, 8...)
4. Each group eliminates one variable
5. Write minimal SOP from groups

**Rules:**
- Groups can wrap around edges
- Larger groups = simpler expression
- Each 1 must be covered

### Quine-McCluskey Algorithm
Tabular method for minimization (handles more variables than K-maps):
1. List minterms in binary
2. Group by number of 1s
3. Combine pairs differing by 1 bit
4. Repeat until no more combinations
5. Find minimal cover using prime implicant chart

---

## 5. Combinational Building Blocks

### Multiplexers (MUX)
- **Function:** Select one of many inputs based on selector
- **n-to-1 MUX:** n data inputs, $\log_2(n)$ select lines
- **Implementation:** Can implement any Boolean function
- **Formula:** $Y = \sum_{i=0}^{n-1} S_i \cdot D_i$ where $S_i$ is selector decode

### Demultiplexers (DEMUX)
- **Function:** Route one input to one of many outputs
- **1-to-n DEMUX:** 1 data input, $\log_2(n)$ select lines

### Encoders & Decoders
- **Encoder:** $2^n$ inputs → n outputs (binary encoding)
- **Priority Encoder:** Encodes highest priority active input
- **Decoder:** n inputs → $2^n$ outputs (binary decoding)
  - Used for address decoding, memory selection

### Comparators
- **Function:** Compare two n-bit numbers
- **Outputs:** A > B, A = B, A < B
- **Cascadable:** Connect multiple comparators for wider widths

---

## 6. Arithmetic Circuits

### Adders
**Half Adder:**
- Inputs: A, B
- Outputs: Sum = $A \oplus B$, Carry = $A \cdot B$

**Full Adder:**
- Inputs: A, B, $C_{in}$
- Sum = $A \oplus B \oplus C_{in}$
- $C_{out} = (A \cdot B) + (C_{in} \cdot (A \oplus B))$

**Ripple Carry Adder:**
- Chain n full adders
- Delay: $O(n)$ - slow due to carry propagation
- Delay = $n \cdot t_{FA}$

**Carry Lookahead Adder (CLA):**
- Parallel carry computation
- Generate: $G_i = A_i \cdot B_i$
- Propagate: $P_i = A_i \oplus B_i$
- Carry: $C_{i+1} = G_i + P_i \cdot C_i$
- Delay: $O(\log n)$

### Subtractors
- Use 2's complement: $A - B = A + \overline{B} + 1$
- Reuse adder with XOR gates for inversion

### Multipliers
**Array Multiplier:**
- AND gates generate partial products
- Adders sum partial products
- Delay: $O(n)$ for n-bit multiplication

**Booth's Algorithm:**
- Reduces partial products
- Handles signed multiplication efficiently

---

## 7. Sequential Logic

### Latches vs Flip-Flops
- **Latch:** Level-sensitive (transparent when enable high)
- **Flip-Flop:** Edge-triggered (changes on clock edge)

### SR Latch (Set-Reset)
- S=1, R=0: Set (Q=1)
- S=0, R=1: Reset (Q=0)
- S=0, R=0: Hold
- S=1, R=1: Invalid (forbidden)

### D Latch
- D (Data) input
- When Enable=1: Q follows D
- When Enable=0: Q holds

### D Flip-Flop
- Captures D on clock edge (rising or falling)
- Most common in synchronous design
- Immune to glitches outside clock edge

### JK Flip-Flop
- J=1, K=1: Toggle (opposite of current state)
- Eliminates SR invalid state

### T Flip-Flop
- T=1: Toggle
- T=0: Hold
- Used for counters

### Timing Parameters
- **Setup Time ($t_{setup}$):** Data stable before clock edge
- **Hold Time ($t_{hold}$):** Data stable after clock edge
- **Clock-to-Q Delay ($t_{cq}$):** Clock edge to output change
- **Max Frequency:** $f_{max} = \frac{1}{t_{cq} + t_{logic} + t_{setup}}$

---

## 8. Registers & Counters

### Registers
**Parallel Load Register:**
- Load all bits simultaneously on clock edge
- Enable signal controls loading

**Shift Registers:**
- **SISO:** Serial in, serial out
- **SIPO:** Serial in, parallel out
- **PISO:** Parallel in, serial out
- **PIPO:** Parallel in, parallel out
- **Applications:** Data conversion, delay lines, pattern generation

**Universal Shift Register:**
- Configurable for shift left/right, parallel load
- Mode control signals select operation

### Counters
**Asynchronous (Ripple) Counter:**
- Each FF clocked by previous FF output
- Slow: cumulative delays
- Glitches during transitions

**Synchronous Counter:**
- All FFs clocked together
- Faster, no ripple delay
- Enable logic determines count sequence

**Modulo-N Counter:**
- Counts from 0 to N-1, then resets
- Use feedback to detect terminal count

**Up/Down Counter:**
- Count increment or decrement based on control

**Ring Counter:**
- Shift register with feedback (output to input)
- One-hot encoding: only one bit high
- Requires n FFs for n states

**Johnson Counter:**
- Twisted ring counter (inverted feedback)
- 2n states from n FFs

---

## 9. Finite State Machines (FSM)

### Moore Machine
- **Output depends only on current state**
- Output stable throughout state
- May require more states

**Design:**
1. State diagram
2. State table
3. State assignment (binary encoding)
4. Next-state and output logic equations
5. Implementation with FFs and combinational logic

### Mealy Machine
- **Output depends on current state AND inputs**
- Faster response (output changes with inputs)
- Can have fewer states

### State Encoding
- **Binary:** Minimal FFs ($\lceil \log_2(n) \rceil$ for n states)
- **One-Hot:** One FF per state (simple decoding, fast)
- **Gray Code:** Minimize transitions

### State Minimization
- Merge equivalent states (same outputs, same next-states)
- Implication chart method
- Reduces hardware complexity

---

## 10. Memory Elements

### ROM (Read-Only Memory)
- Contents fixed or programmable once
- Address decoder + OR array
- **PROM:** One-time programmable (fuse links)
- **EPROM:** UV-erasable
- **EEPROM:** Electrically erasable

### RAM (Random Access Memory)
**SRAM (Static RAM):**
- Uses flip-flops (6 transistors/cell)
- Fast, volatile
- No refresh needed
- Used for cache

**DRAM (Dynamic RAM):**
- Uses capacitor (1 transistor/cell)
- Slower, volatile
- Requires refresh (capacitor leaks)
- Higher density, used for main memory

### Memory Organization
- **Word:** Unit of memory access
- **Address Lines (A):** $2^A$ locations
- **Data Lines (D):** Word size in bits
- **Capacity:** $2^A \times D$ bits

---

## 11. Programmable Logic Devices

### PLA (Programmable Logic Array)
- Programmable AND array + programmable OR array
- Implement any SOP expression
- Shared product terms

### PAL (Programmable Array Logic)
- Programmable AND array + fixed OR array
- Faster than PLA
- Less flexible

### CPLD (Complex PLD)
- Multiple PAL-like blocks
- Interconnect matrix
- Non-volatile

### FPGA (Field-Programmable Gate Array)
- Array of Configurable Logic Blocks (CLBs)
- Programmable interconnect
- LUTs (Look-Up Tables) implement logic
- Volatile configuration (SRAM-based)
- Highly flexible, reconfigurable

**CLB Structure:**
- LUTs (4-6 inputs typical)
- Flip-flops
- Multiplexers
- Carry logic

---

## 12. Hazards & Design Issues

### Types of Hazards
**Static Hazard:**
- Output momentarily glitches when should be stable
- Static-1: Glitch to 0 when should stay 1
- Static-0: Glitch to 1 when should stay 0

**Dynamic Hazard:**
- Multiple transitions when should transition once

**Causes:**
- Unequal path delays
- Race conditions
- Incomplete K-map covering

**Solutions:**
- Add redundant prime implicants
- Synchronous design (FFs eliminate combinational glitches)
- Hazard-free logic design

### Metastability
**Problem:** FF input changes near clock edge
- Output enters undefined state (between 0 and 1)
- May take arbitrarily long to resolve

**Solutions:**
- Synchronizers (chain of FFs)
- Increase MTBF (Mean Time Between Failures)
- Never allow async inputs direct to logic

---

## 13. Design Methodology

### Synchronous vs Asynchronous
**Synchronous:**
- Single clock domain
- Predictable timing
- Easier to design and test
- Preferred for most designs

**Asynchronous:**
- No global clock
- Lower power
- Complex timing analysis
- Used in special cases (handshake protocols)

### Design Flow
1. **Specification:** Requirements, interfaces
2. **Behavioral Design:** FSM, algorithms
3. **RTL Design:** Register-level structure
4. **Logic Synthesis:** Convert to gates
5. **Optimization:** Minimize area/delay/power
6. **Verification:** Simulation, formal methods
7. **Physical Design:** Placement, routing
8. **Timing Analysis:** Ensure timing constraints met

---

## Key Concepts Summary

| Concept | Core Principle |
|---------|----------------|
| **Boolean Minimization** | Reduce gates/complexity using algebra/K-maps |
| **Combinational Logic** | Output = f(current inputs) |
| **Sequential Logic** | Output = f(current inputs, state) |
| **Setup/Hold Time** | Data must be stable around clock edge |
| **Critical Path** | Limits maximum clock frequency |
| **Metastability** | Async inputs risk undefined FF states |
| **FSM Design** | State machine for control logic |
| **Universal Gates** | NAND/NOR can build any circuit |

---

## Common Pitfalls

1. **Forgetting gate delays** → Glitches and hazards
2. **Violating setup/hold times** → Metastability
3. **Asynchronous inputs to logic** → Race conditions
4. **Incomplete K-map grouping** → Sub-optimal minimization
5. **Missing edge cases in FSM** → Stuck states
6. **Ripple counters for high speed** → Too slow
7. **Not considering fan-out limits** → Degraded signals

---

## Cross-Links
- [[02_Computer_Architecture]] - How these gates build processors
- [[05_Memory_Systems]] - Memory hierarchy implementation
- [[Session_01_Memory_Hierarchy_Cost_Model]] - Cache and memory design

---

## Quick Formulas
- **Full Adder Delay (Ripple):** $t_{add} = n \cdot t_{FA}$
- **Max Clock Frequency:** $f_{max} = \frac{1}{t_{clk-to-q} + t_{logic} + t_{setup}}$
- **MTBF (Metastability):** $MTBF = \frac{e^{t_r/\tau}}{f_{clk} \cdot f_{data} \cdot \tau}$
- **Address Lines for N locations:** $A = \lceil \log_2(N) \rceil$
