
---

### **Chunk 1 — Autonomous Systems (ASes)**

Imagine the Internet as a **global map of roads and highways**. Now, think about how real cities are organized: each city manages its **own streets, traffic signals, and rules**. No single city controls the entire country’s roads. Similarly, the Internet is **not one single flat network**. Instead, it is a **network of networks**, where each “network” is independently managed. These independently managed networks are called **Autonomous Systems (ASes)**.

An **AS** is essentially a collection of routers and networks under **one administrative authority**, which could be:

- A **university** managing its campus network (e.g., Harvard, AS 11)
    
- A **company or enterprise network**
    
- An **ISP (Internet Service Provider)** providing Internet access to customers
    

Each AS controls how data **enters, leaves, and moves within** its network. It makes its own routing decisions based on internal policies, security, or business agreements.

To communicate with the outside world, each AS is assigned a **unique number called an Autonomous System Number (ASN)**. This number is like a **license plate for the AS**—it tells other networks exactly which AS they are interacting with. Public ASNs are globally unique and used for global routing, while private ASNs (range 64512–65535) can be used internally within large organizations, without affecting the public Internet.

**Example Analogy:**

- Suppose Harvard’s network is an AS. It has many internal routers connecting classrooms, dorms, and labs. Harvard can decide its own paths internally. But if a student at Harvard wants to access a website hosted at UCSD, the two ASes must exchange routing information to know how to reach each other.
    

**Key takeaway:**  
An AS is a **self-contained network under one authority**, capable of managing its own traffic, but also able to connect to other ASes to reach the global Internet. Understanding ASes is the first step to understanding why the Internet is hierarchical and why routing is divided into intra-domain and inter-domain.


---

## **Chunk 2 — Why the Internet Becomes a Hierarchy**

Now that you understand what an **Autonomous System (AS)** is, the next question is **how these ASes connect to each other**.

In theory, every AS could connect directly to every other AS.  
In reality, this is **impossible**.

Why?

Because:

- There are **tens of thousands of ASes**
    
- Physical links (fiber, routers) are expensive
    
- Managing direct connections with everyone is unscalable
    

So ASes connect in a **hierarchical way**, not randomly.

Think again of roads.  
A small town does **not** build highways to every other town in the country. Instead:

- Local roads connect to **regional highways**
    
- Regional highways connect to **national highways**
    

The Internet follows the **same economic and physical logic**.

---

### Backbone ASes (Top of the Hierarchy)

Some ASes are **very large** and **very well-connected**.  
These are typically called **Tier-1 ISPs**.

A Tier-1 ISP:

- Has connections to **many other large ISPs**
    
- Can reach **every other AS on the Internet** without paying anyone
    
- Forms the **core backbone** of the Internet
    

These backbone ASes connect to each other through **peering agreements**, exchanging traffic directly.

No single Tier-1 ISP controls the Internet, but **together they form the core**.

---

### Regional and Smaller ISPs (Middle Layer)

Most ASes are **not** Tier-1.

A regional or smaller ISP:

- Does not connect to everyone
    
- Instead, it connects to **one or more larger ISPs**
    
- Pays them for **transit**, meaning “carry my traffic to the rest of the Internet”
    

So if you are a small ISP in a city:

- You don’t need global connections
    
- You just need a connection to a larger ISP that already has them
    

This naturally creates **layers**.

---

### Access Networks (Edge of the Internet)

At the bottom of the hierarchy are **access networks**.

These are ASes whose job is **not to forward global traffic**, but to:

- Connect end users
    
- Provide Internet access
    

Examples:

- University networks (like BUET)
    
- Office networks
    
- Home broadband ISPs
    

These ASes mostly **send traffic upward** into the hierarchy and **receive traffic back**.

---

### Why This Hierarchy Matters

This hierarchy is not just about cabling — it **directly affects routing**.

Because:

- Different ASes have different **business relationships**
    
- Not all ASes want to carry other people’s traffic
    
- Routing decisions are influenced by **money, policy, and control**
    

This is the **core reason** the Internet cannot use one single routing protocol everywhere.

---

At this point, you should have a mental image like this:

- Many ASes
    
- Connected in layers
    
- Bigger ASes near the top
    
- Smaller, user-facing ASes near the bottom


---

## **Chunk 3 — Stub Networks and the Idea of “Transit”**

Now that you have the picture of ASes arranged in layers, we need to introduce a **very important concept** that quietly controls Internet routing:

👉 **Transit traffic**

---

### What is “Transit” Traffic?

Imagine traffic flowing through a network.

There are **three possibilities** for any packet inside an AS:

1. **Traffic starts here**  
    (e.g., a BUET student opening a website)
    
2. **Traffic ends here**  
    (e.g., someone accessing a BUET server)
    
3. **Traffic just passes through**  
    (origin somewhere else, destination somewhere else)
    

That **third case** is called **transit traffic**.

So:

> **Transit traffic = traffic that an AS forwards for other ASes**

---

### What Is a Stub Network?

A **stub network** is an AS that **refuses to carry transit traffic**.

It only allows:

- Traffic **originating inside** the AS
    
- Traffic **destined to inside** the AS
    

But **never**:

- Traffic that passes _through_ it to reach somewhere else
    

---

### Why Would an AS Do That?

Because **carrying transit traffic costs money**.

Transit traffic means:

- More bandwidth usage
    
- More router load
    
- More operational cost
    
- No direct benefit
    

For example:

- BUET does **not** want to carry traffic between two ISPs
    
- A home ISP does **not** want to become a global relay
    

So they say:

> “We are not a road. We are a destination.”

That makes them **stub ASes**.

---

### Real-Life Analogy

Think of a **university campus**.

- Students and staff can enter and exit
    
- Deliveries can come in
    
- But you **cannot** use the campus roads as a shortcut between two highways
    

That’s exactly what a stub network is.

---

### Where Stub Networks Sit in the Hierarchy

Stub ASes:

- Sit at the **edges** of the Internet
    
- Connect to **one or more upstream ISPs**
    
- Do not have customers who depend on them for global transit
    

They are **leaves** of the Internet graph.

---

### Why Stub Networks Matter for Routing

This is critical:

Routing on the Internet is **not just about shortest path**.

A path may exist physically, but:

- If it passes through a stub AS as transit → **not allowed**
    
- Even if it is shorter → **not used**
    

So routing decisions must respect:

- Business relationships
    
- Transit policies
    
- Stub restrictions
    

This is one of the **fundamental reasons** Link State Routing cannot be used globally.

LSR assumes:

> “If a link exists, it can be used.”

That assumption **breaks completely** at Internet scale.

---

At this point, you should clearly see:

- What transit traffic is
    
- What a stub network is
    
- Why some ASes refuse to forward traffic
    


---

## **Chunk 4 — Why Routing Must Be Split (Intra-domain vs Inter-domain)**

Now you understand three things clearly:

- The Internet is made of **Autonomous Systems**
    
- ASes are connected in a **hierarchy**
    
- Some ASes (stub networks) **refuse to carry transit traffic**
    

This leads to a **fundamental problem**:

> **Who decides how packets move inside an AS, and who decides how packets move between ASes?**

The answer cannot be “one single routing protocol”.

---

### Two Very Different Routing Problems

Let’s separate them carefully.

#### Problem A: Routing _inside_ an AS

Inside one AS:

- All routers are under **one authority**
    
- One organization controls hardware, software, policies
    
- Routers **trust each other**
    
- The goal is usually:
    
    - Fast convergence
        
    - Efficient paths
        
    - Minimal delay
        

This is called **intra-domain routing**.

---

#### Problem B: Routing _between_ ASes

Between ASes:

- Different organizations
    
- No mutual trust
    
- Business contracts matter
    
- Some paths are **forbidden**, even if they exist physically
    

This is called **inter-domain routing**.

---

### Why One Algorithm Cannot Do Both

Imagine using the same rulebook for:

- Traffic inside a university campus
    
- Traffic across international borders between countries
    

It doesn’t work because:

- Inside → cooperation
    
- Outside → negotiation
    

Similarly:

- Inside AS → technical optimization
    
- Between ASes → political + economic decisions
    

So routing is **deliberately split** into two layers.

---

### Names of the Two Classes

- **IGP (Interior Gateway Protocol)**  
    Used **inside** an AS  
    Example: OSPF, IS-IS
    
- **EGP (Exterior Gateway Protocol)**  
    Used **between** ASes  
    Example: BGP
    

These are not just names — they reflect **different philosophies**.

---

### Key Concept: Trust Boundary

An AS boundary is a **trust boundary**.

Inside:

- Routers believe routing updates
    
- Share detailed topology information
    

Across AS boundary:

- Routers do **not** share internal topology
    
- Only advertise what is _necessary_
    
- Control what others are allowed to use
    

This trust boundary is why Link State Routing **stops at AS borders**.

---

### Why This Matters for LSR

Link State Routing assumes:

- Full topology visibility
    
- Honest information
    
- Free use of all links
    

All three assumptions are **true inside an AS**  
All three are **false across ASes**

That is the _deep reason_ LSR is restricted to intra-domain routing.

---

At this point, you should feel:

- Why routing is split
    
- Why AS boundaries are sacred
    
- Why LSR cannot cross them
    

---

## Chunk 5 — What LSR _Assumes_ (and Why That’s Dangerous)

You know how LSR works. Now let’s expose its **assumptions**.

Link State Routing _implicitly assumes_ the following:

1. Every router is **cooperative**
    
2. Every router **tells the truth**
    
3. Every router is willing to **share full topology**
    
4. Every physical link is **allowed to be used**
    
5. “Best path” means **shortest / lowest cost**
    

Inside a single AS, these assumptions are reasonable:

- One admin controls all routers
    
- Policies are aligned
    
- Costs are meaningful and trusted
    

But now imagine applying LSR to the **entire Internet**.

---

### What Breaks First: Topology Disclosure

If LSR were used globally, each AS would have to:

- Reveal its **internal routers**
    
- Reveal its **link structure**
    
- Reveal its **capacities and costs**
    

That information is:

- Commercially sensitive
    
- A security risk
    
- Completely unnecessary for outsiders
    

An ISP does **not** want competitors to know:

- Where its bottlenecks are
    
- How its internal network is structured
    
- Which paths are cheaper internally
    

So the **first thing that breaks globally is transparency**.

---

### What Breaks Next: “Shortest Path”

On the Internet:

- Shortest ≠ cheapest
    
- Cheapest ≠ allowed
    
- Allowed ≠ preferred
    

Example:

- AS A could reach AS D via AS B (short)
    
- But AS B is a competitor
    
- So AS A refuses to send traffic through B
    

LSR cannot express:

> “This path exists but is forbidden by policy.”

LSR only knows **cost**, not **politics**.

---

### The Deep Insight

LSR is:

> **A technical optimization algorithm**

The Internet is:

> **A negotiated, policy-driven system**

That mismatch is the root of **everything**.

---

