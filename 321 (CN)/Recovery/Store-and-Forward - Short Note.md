# Store-and-Forward Packet Switching — Short Note

Definition
- Store-and-forward switching: each network node (router/switch) receives the entire packet, checks it (integrity/address), and only then forwards it to the next hop.

How it works (brief)
1. Sender transmits a packet to the router.
2. Router buffers the full packet in memory.
3. Router verifies the packet (e.g., CRC, header checks), reads destination, and looks up next hop.
4. If valid and next hop available, router forwards the complete packet out the chosen interface.

Real-world analogy
- Like a postal sorting facility: the facility receives the whole package, inspects the address and condition, then places it on the correct outbound truck.

Why use it
- Pros: filters corrupted packets before they travel further, smooths speed differences between links (buffering), simpler error handling.
- Cons: adds per-hop latency (must receive whole packet before forwarding), requires buffering memory, risk of drops under congestion.

Cut-through vs store-and-forward
- Cut-through: forward as soon as the destination is known (lower latency), but may forward corrupted packets (error detected later).
- Store-and-forward: higher latency but prevents corrupted frames from propagating.

Quick numbers (intuition)
- 1500-byte packet on 100 Mbps link ≈ 120 μs transmission time. Store-and-forward adds roughly that receive time per hop before forwarding.

One-line summary
- "Store-and-forward: receive full packet → check → forward. Reliable and simple, at the cost of per-hop delay." 
