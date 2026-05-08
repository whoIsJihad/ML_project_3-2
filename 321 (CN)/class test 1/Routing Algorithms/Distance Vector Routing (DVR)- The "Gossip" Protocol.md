
Distance Vector Routing is a decentralized routing algorithm. Each router is essentially a gossiper: it knows its own neighbors and what those neighbors _claim_ is the distance to everyone else. It doesn't know the full map of the network; it just knows which door to throw a packet through to reach a destination.

## 1. Core Principles

Each router maintains a table with three columns:

1. **Destination**: Where are we going?
    
2. **Distance (Metric)**: How "expensive" is it to get there? (Hops, delay, etc.)
    
3. **Next-Hop**: Which neighbor should I send this to?
    

### The Bellman-Ford Logic

DVR is based on the Bellman-Ford equation. If router $X$ wants to get to destination $Y$ via neighbor $Z$:

$$D_x(Y) = \min \{ Cost(X, Z) + D_z(Y) \}$$

In plain English: "The best way for me to get to $Y$ is the minimum of (my distance to neighbor $Z$ + $Z$'s claimed distance to $Y$)."

## 2. The Step-by-Step Mechanism

1. **Initialization**: Every router knows the distance to its direct neighbors (usually 1 hop) and sets everything else to $\infty$.
    
2. **Exchange**: Periodically (or on change), every router sends its **entire table** to its neighbors.
    
3. **Update**: When Router A gets a table from Router B:
    
    - It adds the cost of reaching B to every entry in B's table.
        
    - If this new calculated distance to a destination is lower than what A currently has, A updates its table and sets B as the next-hop.
        

## 3. The "Count-to-Infinity" Nightmare

This is the classic DVR flaw found on page 16 of your notes.

### Example Scenario:

Imagine a linear network: **A --- B --- C**

- Initially, C is up. B knows C is 1 hop away. A knows C is 2 hops away (via B).
    
- **The Crash**: C goes down.
    
- B detects the failure and sets its distance to C as $\infty$.
    
- **The Gossip**: Before B can tell A, A sends its table to B. A says: "I can reach C in 2 hops!"
    
- **The Mistake**: B thinks: "Oh! A found a new way to C! If A is 2 hops away, I'm now 3 hops away (via A)."
    
- **The Loop**: B tells A it's 3 hops away. A then updates to 4 hops. They keep incrementing until they hit "Infinity" (usually 16 or 100).
    

## 4. Remediation Strategies

### A. Split-Horizon

If Router B learned about Destination C from Router A, B should **not** tell A that it can reach C. This prevents the simplest loops where two neighbors bounce stale info back and forth.

### B. Poison Reverse

An aggressive version of Split-Horizon. Instead of saying nothing, B tells A: "My distance to C is $\infty$," effectively "poisoning" the route so A doesn't try to use B to reach a destination that A actually provided.

### C. Triggered Updates

Don't wait for the timer. If a link goes down, send the "Infinity" update immediately. This speeds up convergence but doesn't solve the loop if a regular update is already "in flight."

## 5. Comparison Summary

- **Good News spreads fast**: If a new link appears, the network converges in $O(Diameter)$ time.
    
- **Bad News spreads slow**: A single link failure can lead to counting to infinity, making the network unstable for a long duration.