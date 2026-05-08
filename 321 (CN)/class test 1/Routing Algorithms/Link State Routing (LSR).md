

---

# Link State Routing (LSR) — One Complete Picture

Think of **LSR** as this idea:

> **Every router independently builds the same complete map of the network, then locally computes shortest paths.**

Everything you’re confused about (LSP, sequence number, age, flooding) exists **only to make that idea work reliably**.

---

## The Big Picture (3 Phases)

LSR has **three logical phases**:

1. **Discover neighbors & link costs**
    
2. **Distribute link-state information (LSP flooding)** ← _this is where your confusion is_
    
3. **Run Dijkstra locally**
    

We’ll zoom into **Phase 2**, but first keep this global view in mind.

---

## Phase 1: What information does a router advertise?

Each router creates a packet called an **LSP (Link State Packet)**.

An LSP basically says:

> “I am router R.  
> These are my neighbors.  
> These are the costs of the links to them.”

### Typical LSP contents

```
Router ID
List of neighbors + link costs
Sequence Number
Age (TTL)
Checksum
```

That’s it.

---

## Phase 2: Distributing LSPs (the tricky part)

### Core idea: Flooding

Each router **floods** its LSP:

- Send to **all neighbors**
    
- Neighbors forward it to **their neighbors**
    
- Eventually, everyone gets it
    

But flooding has **3 big problems**:

1. Infinite looping
    
2. Old vs new information
    
3. Router crashes & corruption
    

Everything you mentioned exists to solve **these problems only**.

---

## Problem 1: Infinite Flooding & Old Packets

### → **Sequence Numbers**

Each router **numbers its own LSPs**:

```
R1 LSP #1
R1 LSP #2
R1 LSP #3
...
```

### Rule every router follows:

> **Accept an LSP only if its sequence number is strictly higher than the one already stored for that router.**

So:

- Newer → accept & forward
    
- Older or duplicate → discard
    

This **automatically stops infinite loops**.

---

## Problem 2: Sequence Number Wrapping

### (Why not small numbers?)

If sequence numbers are small (say 4-bit):

```
0 → 1 → 2 → ... → 15 → 0 (wrap)
```

Now disaster:

- Old LSP = 15
    
- New LSP = 0
    
- Router thinks **0 < 15 → discard**
    

### Solution: **32-bit sequence numbers**

- Max ≈ 4 billion
    
- 1 LSP/sec → ~137 years to wrap
    

👉 **Wrapping becomes practically impossible**, so we ignore it.

---

## Problem 3: Router Crash & Restart

### (This is subtle and important)

Scenario:

- Router R was sending LSPs with sequence ≈ 5000
    
- R crashes
    
- R restarts and begins again at sequence **0**
    

Other routers still have:

```
R : sequence 5000
```

Now R sends:

```
R : sequence 0
```

Everyone says:

> “0 < 5000 → obsolete → discard”

So R is **ignored forever**.

---

### Solution: **Age Field (TTL)**

Every LSP has an **Age**:

- Decreases with time
    
- Must be refreshed periodically by the original router
    

If router R crashed:

- It **stops refreshing old LSPs**
    
- Those old LSPs **age out**
    
- When Age = 0 → **purged from all databases**
    

After purge:

- New LSPs from R (sequence 0, 1, 2…) are accepted again
    

👉 **Age is the garbage collector of LSR.**

---

## Problem 4: Corrupted Sequence Numbers

### (MSB flip nightmare)

If a bit flips during transmission:

```
Sequence = 4
→ MSB flips
→ Sequence = 65540
```

Now everyone believes:

- 65540 is the “latest”
    
- Real future updates (5, 6, 7…) are discarded
    

### Two-layer solution:

#### 1. **Checksum / Parity**

- Detect corruption
    
- Corrupted LSP → discarded immediately
    

#### 2. **Age field (backup safety net)**

- Even if corruption somehow passes
    
- That LSP won’t be refreshed
    
- It ages out and disappears
    

---

## Important Supporting Mechanism: Holding Area

Routers **don’t instantly forward** received LSPs.

They keep them briefly to:

- Detect duplicates
    
- Avoid sending back to the sender
    
- Decide who needs ACKs
    

This prevents unnecessary traffic and loops.

---

## Phase 3: Shortest Path Computation

Once flooding settles:

- Every router has **the same full network graph**
    
- Each link appears **twice** (A→B and B→A)
    
- Router runs **Dijkstra locally**
    
- No coordination needed
    

That’s why LSR converges fast and reliably.

---

## One-Sentence Summary (Exam Gold)

> **Link State Routing works by flooding sequence-numbered LSPs with aging to ensure all routers build the same global topology database, after which each router independently runs Dijkstra to compute shortest paths.**

---

