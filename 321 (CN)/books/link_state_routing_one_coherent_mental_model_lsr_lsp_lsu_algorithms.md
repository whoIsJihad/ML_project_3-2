# Link-State Routing — One Coherent Mental Model

This note rebuilds **Link-State Routing** from first principles and fits every confusing term (LSR, LSP, LSU, LSDB, Dijkstra) into **one clean model**. No protocol soup, no memorization-first approach.

---

## 1. What problem routing is actually solving

At the data plane level, a router needs only one thing:

> **Destination prefix → Next hop interface**

That mapping is the **routing table**.

The hard part is **not forwarding packets** — it’s **learning the network topology accurately and consistently** so that table can be computed.

---

## 2. Two algorithm families (zoomed out)

All routing protocols fall into one of two families:

### Distance Vector (e.g., RIP)
- Routers exchange *beliefs*:
  - “I think destination X is Y cost away.”
- Routers do **not** know the full topology.
- Slow convergence, loops possible.

### Link State (e.g., OSPF, IS-IS)
- Routers exchange *facts*:
  - “Here are **my links** and their costs.”
- Every router builds the **same full network graph**.
- Fast convergence, deterministic behavior.

This note is only about **Link State**.

---

## 3. The core idea of Link-State Routing

**Every router independently builds the same map of the network, then locally computes best paths.**

This happens in three conceptual steps:

1. **Describe yourself** (your links)
2. **Flood that description to everyone**
3. **Run a shortest-path algorithm locally**

Everything else exists only to make these three steps reliable.

---

## 4. Terminology mapped to the model

### LSR — Link State Router

An **LSR** is simply:

> A router that participates in a link-state protocol.

If a router:
- Creates link descriptions
- Floods them
- Runs shortest-path computation

…it is an LSR. No extra meaning.

---

### LSP — Link State Packet (a.k.a. LSA in OSPF)

An **LSP** is a **router’s self-description**.

It contains **only local facts**, never routes:
- Router ID
- List of neighbors
- Cost of each link
- Sequence number (newer beats older)

Example LSP:

- Router: B
- Links:
  - B–A cost 1
  - B–C cost 1
  - B–D cost 1
- Sequence: 42

Each router generates **only its own LSP**.

---

### LSU — Link State Update

An **LSU** is the **transport envelope**.

It exists because:
- LSPs must be flooded
- Flooding must be reliable
- Multiple LSPs may be sent together

So:

> **LSU = message that carries one or more LSPs**

Different protocols name it differently, but the function is identical.

---

### LSDB — Link State Database

The **LSDB** is the collection of **all received LSPs**.

Key property:

> After convergence, **all routers have identical LSDBs**.

That means:
- Same nodes
- Same edges
- Same costs

In other words: **same graph**.

---

## 5. Flooding (why everyone sees everything)

Flooding rules (conceptual):

1. Receive an LSP
2. If it is **newer** than what you have:
   - Store it in LSDB
   - Forward it to all neighbors *except* the sender
3. If older or duplicate:
   - Drop it

Why flooding does *not* explode:
- Sequence numbers prevent loops
- Aging removes stale LSPs
- Acknowledgments ensure reliability

Flooding ends when no router has anything new to say.

---

## 6. When routing actually happens

Important separation:

- **Control plane**: topology learning (everything so far)
- **Data plane**: packet forwarding

Routing computation happens **after** LSDB convergence.

No packets are involved in this step.

---

## 7. Shortest Path First (SPF)

Each router independently runs:

> **Dijkstra’s algorithm**

Input:
- The LSDB (full graph)

Output:
- Shortest-path tree **rooted at that router**

From this tree:
- Best next hop to every destination is derived
- Routing table is installed

Routers do **not** exchange routes — only topology.

---

## 8. Concrete example

Topology:

```
A ——1—— B ——1—— C
 \        |
  \—2— D —/
```

### LSPs generated

- A: (A–B,1), (A–D,2)
- B: (B–A,1), (B–C,1), (B–D,1)
- C: (C–B,1)
- D: (D–A,2), (D–B,1)

After flooding, **every router has all four LSPs**.

### SPF at Router A

Computed shortest paths:
- To B: A→B (1)
- To D: A→D (2)
- To C: A→B→C (2)

Routing table at A is built **locally** from this.

Router C runs the *same algorithm* on the *same graph*, but rooted at C.

---

## 9. Why link-state does NOT exchange routing tables

Because:
- Routes are **derived data**
- Topology is **ground truth**

Sharing routes would:
- Propagate mistakes
- Cause loops
- Slow convergence

Sharing topology lets everyone recompute correctly.

---

## 10. One-line definitions (final lock-in)

- **LSR**: Router running a link-state protocol
- **LSP / LSA**: A router’s link description
- **LSU**: Packet carrying LSPs
- **LSDB**: Complete topology database
- **SPF / Dijkstra**: Converts topology → routing table

---

## 11. Single-sentence mental model (memorize this)

> *Link-state routing works because every router learns the same network graph and independently computes optimal forwarding decisions.*

If a detail doesn’t fit this sentence, it’s secondary.

