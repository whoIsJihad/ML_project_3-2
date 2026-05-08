

---

## 🧐 Left Side: Autonomous Systems (AS) and Router Types

This section focuses on the structure and components within an Autonomous System (AS).

* **Autonomous Systems (ASs):**
    * The note says "Many Autonomous systems (ASes) are large" and "are in hierarchy." An AS is a collection of IP networks and routers under the control of one administrative entity (like a large corporation, university, or ISP). It uses its own routing policy.
    * The distinction is made between:
        * **Stub AS (Single Border Router):** A small AS that is connected to only one other AS (or provider). It usually carries only local traffic.
        * **Non-stub AS (Multiple Border Routers):** A larger AS connected to multiple other ASs, often used by large ISPs or institutions.

* **Router Types:**
    * **Area-border routers:** (Looks like it says) "for inter-level areas." These are routers connecting different "areas" within a single large AS (often seen in large-scale routing protocols like OSPF).
    * **Border routers:** Routers that connect the local AS to one or more external ASs (the Internet).
    * **Backbone area (area-0):** (Looks like it says) "Border routers summarize routes within the (area) and (are) default routers for all outside addresses." This refers to the core area in hierarchical routing protocols like OSPF, where traffic between different areas flows.

* **Other Notes:**
    * **Seg or edge load balancing:** Mentioned as "Similar as above..." suggesting a way to distribute traffic.
    * **Type of Service (ToS):** "Varying characteristics (del, thr, int, rel)." This refers to the field in the IP header used to differentiate traffic (e.g., delay, throughput, reliability).
    * **Example:** Satellites being high delay, long latency, but fiber optic being low delay, low latency. This is an analogy for different network medium characteristics.
    * **Diff-Serv Routing:** (Differentiated Services) Likely referring to quality-of-service mechanisms based on the ToS field.

---

## 🌐 Right Side: Internet Structure and Inter-Domain Routing

This section illustrates the hierarchical structure of the Internet using different tiers of ISPs.

* **ISP Hierarchy (Internet Structure):**
    * The diagram shows a hierarchical arrangement of Internet Service Providers (ISPs):
        * **Large ISP:** Often called Tier-1 ISPs, which are at the top and connect to every other large ISP, forming the global backbone.
        * **Mid-size ISP / Small ISP / Dial-up ISP:** These are lower-tier ISPs that connect to the large ISPs to gain access to the full Internet.
        * **Stub:** This refers to the local networks or small ASs (like a home, business, or university) that connect to an ISP.
        * **Access Network:** The final network connecting end-users to their ISP.

* **Routing Concepts:**
    * **Ospf here (Intra-domain routing):** OSPF (Open Shortest Path First) is a common **Interior Gateway Protocol (IGP)** used to route traffic *within* a single AS (the "Intra-domain" part).
    * **What about this? (Inter-domain routing):** This refers to routing *between* different ASs (i.e., between the ISPs and stub networks). The protocol used for this is the **Border Gateway Protocol (BGP)**, which is the protocol that essentially runs the Internet.

* **ASNs (AS Numbers):**
    * **16-bit:** The original size of an AS number.
        * **0-65535:** The original range.
        * **Ex: thousand - 11:** Likely a specific example range or a note about reserved numbers.
    * **32-bit:** The newer size for AS numbers, allowing for a much larger number of ASs.
    * **Private:** **64512 to 65535** (in the 16-bit range). These are reserved ASNs that can be used for internal testing and routing within a private network and are not advertised on the public Internet.

---

### **Summary**

The whiteboard provides an overview of:
1.  **The structure of networks** (AS, Stub vs. Non-stub).
2.  **The roles of different routers** (Area-border, Border).
3.  **The hierarchy of the Internet** (Large, Small ISPs).
4.  **The two main types of routing** (Intra-domain like OSPF, and Inter-domain like BGP).
5.  **The identification system for networks** (AS Numbers, both 16-bit and 32-bit).

It is a concise summary of the foundations of **Internet architecture and routing protocols.**

This whiteboard image focuses on **Interdomain Routing** and the economic/political relationships between different networks on the Internet, specifically using the **Border Gateway Protocol (BGP)**.

---

## 1. Interdomain Routing: BGP (Border Gateway Protocol)

The left section outlines how different Autonomous Systems (ASes) talk to each other.

* **Key Considerations:** Routing at this level is driven by scalability, the autonomy of domains, and is heavily dominated by **policy and business considerations** rather than just technical speed.
* **The Goal of BGP:** Unlike internal protocols that look for the "fastest" path, BGP simply finds *a* valid path and does not necessarily try to optimize it.
* **Path Vector Protocol:** BGP is described as a "distance vector algorithm with extra info"—specifically, the complete path of ASes to reach a destination.
* **Advantages:** This allows for policy choices based on the specific ASes in a path and makes it very easy to **avoid loops**.


* **Typical Policy:** A common rule is to prefer the path with the fewest number of AS "hops".

---

## 2. Transit and Customer-Provider Relationships

The middle section explains how data moves (or doesn't move) through different types of networks.

* **Non-transit ASes:** These are networks (like a corporate or campus network, e.g., BUET) that do not carry traffic for anyone else. They only send and receive their own data.
* **Customer-Provider Hierarchy:**
* **Provider:** Usually a larger ISP that provides access to the rest of the Internet.
* **Customer:** Pays the provider for "transit" (the ability to send data through the provider's network to the outside world).
* The diagram shows that the "upper" nodes in the hierarchy are the larger ISPs (Tier 1).



---

## 3. Peering vs. Transit

The right section compares "Peering" with "Transit" through a helpful table and diagrams.

* **Peering:** Two ISPs connect directly to exchange traffic between their *respective customers* only.
* **Key Rule:** Peers do **not** exchange money and do **not** provide transit for each other (i.e., ISP A won't let Peer B use its network to reach a third ISP C).


* **The Decision Table:**

| Peer | Don't Peer |
| --- | --- |
| Reduces upstream transit costs | You would rather have them as paying customers |
| Can increase end-to-end performance | Peers are usually competitors |
| May be the only way to connect your customers to some parts of the Internet | Relationships require constant negotiation and management |

* **Financial Impact:** Both parties can save money if they allow peer-to-peer traffic because they avoid paying a "higher-up" provider for that same data transfer.

---

## 4. Visualizing Traffic Flow

The bottom-right diagrams illustrate the difference in allowed traffic:

* **Solid lines:** Traffic is allowed to flow (e.g., customer to provider).
* **Dashed lines:** Traffic is **not** allowed (e.g., trying to use a peer to reach a non-customer network).

