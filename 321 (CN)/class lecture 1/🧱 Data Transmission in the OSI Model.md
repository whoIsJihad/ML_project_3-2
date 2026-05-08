
This diagram illustrates how data flows from an **End System** (Sender) through **Intermediate Nodes** (Routers) to another **End System** (Receiver) using the OSI Model.

## 1. Encapsulation (Sender Side)

When data (M) moves *down* the stack from the Application Layer (AL) to the Physical Layer (PL):

1.  The Application Layer passes the data (M) to the Presentation Layer (PL).
2.  At the Transport Layer (TL), the layer adds its own header (H_T) to the data (M). The **Segment** is formed: $H_T + M$.
3.  At the Network Layer (NL), it adds its header ( $H_N$) to the segment. The **Packet** is formed: $H_N + H_T + M$.
4.  At the Data Link Layer (DLL), it adds a header ($H_{DLL}$) and usually a trailer/footer ($F_{DLL}$). The **Frame** is formed: $H_{DLL} + (H_N + H_T + M) + F_{DLL}$.
5.  At the Physical Layer (PL), the Frame is converted into a stream of **Bits** for transmission.

> [!TIP]
> This process is called **Encapsulation**—each lower layer wraps the data and headers from the layer above it.

## 2. Hop-by-Hop Delivery (Intermediate Nodes)

Intermediate nodes (like routers) only need information up to the **Network Layer (NL)** to make routing decisions:

1.  The router receives the stream of **Bits** (PL).
2.  The Physical Layer passes the bits to the Data Link Layer (DLL), which performs error checking and *removes* the DLL header and trailer (Decapsulation).
3.  The DLL passes the remaining **Packet** ($H_N + H_T + M$) to the Network Layer (NL).
4.  The NL reads the destination IP address in its header ($H_N$) and consults its routing table to determine the next hop.
5.  **Crucially:** The NL *does not* touch the Transport Layer header ($H_T$) or the data ($M$).
6.  The NL then *re-encapsulates* the packet, passing it back down to the DLL and PL for transmission to the next intermediate node or the final destination.

## 3. Decapsulation (Receiver Side)

When data moves *up* the stack at the final End System (Receiver):

1.  The process is the reverse of encapsulation. Each layer checks the header added by its peer layer on the sender side and *removes* it before passing the data up.
2.  The **bottommost layer (Transport Layer)** cuts off its own header and delivers the original **end-to-end data ($M$)** to the Application Layer via its peer layer.

---
