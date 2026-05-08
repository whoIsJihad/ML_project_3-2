

## 1. The OSI Model Layers
The OSI (**O**pen **S**ystem **I**nterconnection) Reference Model is a conceptual framework used to describe the functions of a networking system.

| Layer Name       | Abbreviation | Protocol Data Unit (PDU)           | Key Function                                                           |
| :--------------- | :----------- | :--------------------------------- | :--------------------------------------------------------------------- |
| **Application**  | AL           | APDU (Application PDU)             | User interface, application services (e.g., HTTP, SMTP).               |
| **Presentation** | PL           | PPDU (Presentation PDU)            | Data format, encryption, compression.                                  |
| **Session**      | SL           | SPDU (Session PDU)                 | Manages sessions (dialog control, synchronization).                    |
| **Transport**    | TL           | TPDU (Transport PDU) / **Segment** | End-to-end process-to-process communication, reliability/flow control. |
| **Network**      | NL           | **Packet** / **Datagram**          | Routing between different networks.                                    |
| **Data Link**    | DLL          | **Frame**                          | Node-to-immediate-next-node delivery, error detection.                 |
| **Physical**     | PL           | **Bit**                            | Transmission of raw data bits over a physical medium.                  |

> [!NOTE]
> The **Internet Protocol Stack (TCP/IP)** model often combines the top three layers (Application, Presentation, Session) into a single **Application Layer**.

## 2. Protocol Data Units (PDUs)
A PDU is a single unit of data transmitted between peer entities of a given layer.

* **Application/Presentation/Session:** PDU is generally referred to as an **APDU/PPDU/SPDU**.
* **Transport Layer (TL):** PDU is often called a **Segment** (TCP) or **Datagram** (UDP). Handles **end-to-end** communication (sender to receiver) and is independent of the platform/hardware.
* **Network Layer (NL):** PDU is called a **Packet** or **Datagram**. Responsible for **routing decisions** to get the packet across the internetwork.
* **Data Link Layer (DLL):** PDU is called a **Frame**. Responsible for delivery to the **immediate next node** (hop-by-hop).
* **Physical Layer (PL):** PDU is a **Bit**. Handles the **bit-by-bit** physical transmission.

## 3. Open Protocols & Open Systems
A protocol is considered **open** if:

1.  Protocol details are **publicly available**.
2.  Changes are managed by an organization where membership and transaction processes are **open to the public**.

An **Open System** is a system that implements open protocols.

* The **International Organization for Standards (ISO)** prescribes standards to connect open systems, leading to the **Open System Interconnection (OSI)** model itself.

> [!EXAMPLE]
> A **Proprietary** protocol (the opposite of open) might be one used exclusively by an internal organization like the military, where protocol details and management are kept private.

### Next : [[🧱 Data Transmission in the OSI Model]]