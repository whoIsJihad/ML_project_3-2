# False sharing

## The setup

Each core has its own L1 cache. A cache line is **64 bytes**. A single `int` is 4 bytes — so one cache line holds ~16 integers packed together in memory.

Now imagine two threads, each with their own variable — `x` (owned by Thread 1) and `y` (owned by Thread 2). They don't share data. But if `x` and `y` happen to sit next to each other in memory, they land on the **same 64-byte cache line**.

```
[ x (4B) | y (4B) | … other stuff (56B) … ]  ← one cache line
```

## What the hardware does

When Core 1 writes to `x`, the CPU's **coherence protocol** broadcasts: _"every other core's copy of this line is now stale."_

It does this at cache-line granularity — it has no concept of "only `x` changed." So Core 2's copy of the entire line gets invalidated, including its copy of `y`, which nobody touched.

Now Core 2 wants to write `y`. Its copy is stale, so it must fetch the fresh line from Core 1 — a **~40–100 cycle round trip**. It writes `y`, which invalidates Core 1's copy. Core 1 fetches it back. And so on.

The line bounces between cores on every write, even though the threads have nothing to do with each other.

> This is called **false sharing** — the cores aren't logically sharing data, but the hardware thinks they are because they share a cache line.

## Why it hurts

Two threads meant to run in parallel end up waiting on each other constantly. The coherence traffic serialises them. You can end up **slower than a single-threaded version**.

## The fix — padding

Force each variable onto its own cache line by padding it out to 64 bytes:

```c
// broken — x and y share a cache line
struct { int x; int y; } counters;

// fixed — each on its own 64-byte line
struct { int x; char _pad[60]; } counter1;
struct { int y; char _pad[60]; } counter2;
```

Now when Core 1 writes `x`, the invalidation only hits Core 1's line. Core 2's line — holding `y` — is at a different address and is completely unaffected. Both cores write at full speed.

## Key distinction

This is a **coherence problem**, not a capacity problem. The cache isn't full. There's no eviction happening. The hardware is doing exactly what it's supposed to do — keeping all cores' views of memory consistent — but it can only operate at cache-line granularity, not per-variable. False sharing is what happens when that enforcement fires on a coincidence of memory layout.