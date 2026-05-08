# LSP Flooding: Send and Ack Flags

When routers exchange Link State Packets (LSPs), they use **Send** and **Ack** flags to ensure reliable and efficient delivery to all neighbors.

## The Holding Area

Each router maintains a **holding area** (buffer) for recently received LSPs. For each LSP, the table tracks:
- **Source (Src)**
- **Sequence Number (seq#)**
- **Age**
- **Send Flags** (one per neighbor)
- **Ack Flags** (one per neighbor)

## What Do Send and Ack Flags Mean?

- **Send Flag (per neighbor):**
  - `1` = This LSP still needs to be sent to that neighbor.
  - `0` = Already sent to that neighbor.

- **Ack Flag (per neighbor):**
  - `1` = Awaiting acknowledgment from that neighbor for this LSP.
  - `0` = Acknowledgment received.

## How It Works

1. **Receiving an LSP:**  
   - Store the LSP in the holding area.
   - Set the **Send Flag** for all neighbors except the one it was received from.
   - Set the **Ack Flag** for the neighbor it was received from.

2. **Sending LSPs:**  
   - Periodically scan the holding area.
   - For each LSP with a **Send Flag = 1** for a neighbor, send the LSP and clear the flag.

3. **Acknowledgment:**  
   - When a neighbor receives an LSP, it sends back an **Ack**.
   - Upon receiving an Ack, clear the **Ack Flag** for that neighbor.

4. **Aging:**  
   - Each LSP has an **Age** field, decremented every second.
   - When Age reaches zero, the LSP is discarded.

## Why Is This Needed?

- **Reliability:** Ensures all routers receive every LSP, even if packets are lost.
- **Efficiency:** Prevents sending the same LSP repeatedly to the same neighbor.
- **Loop Prevention:** Avoids endless circulation of old LSPs.

> **Summary:**  
> The Send and Ack flags help routers track which neighbors still need to receive or acknowledge each LSP, ensuring reliable and efficient flooding of link state information throughout the network.
