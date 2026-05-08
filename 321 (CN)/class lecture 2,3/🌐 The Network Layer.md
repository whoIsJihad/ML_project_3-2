# 🌐 The Network Layer

The Network Layer is **Layer 3** in the OSI model. If you imagine the entire 7-layer model as an hourglass, the Network Layer is the narrow neck. This is because its function is very specific and crucial, but it relies on the layers below it and serves all the layers above it.

---

## Primary Goal: End-to-End Delivery

The main job of the Network Layer is to get packets from the **source host** all the way to the **destination host**. This often involves a journey across many different networks and routers.

Key responsibilities include:
- **Logical Addressing:** Assigning unique addresses (like IP addresses) to each host on the network to identify them.
- **Routing:** Determining the best path for a packet to travel from source to destination. This is the "brain" of the network layer. To do this, routers must know the [[🗺️ Routing Algorithms|network topology]].
- **Packet Forwarding:** The actual process of moving a packet from an input link to the appropriate output link on a router.

---

## Design Issues

A key design challenge at this layer is how to get packets from source to destination. This leads to two major service philosophies, which we will explore:
1.  [[📬 Network Service Models|Connectionless Service]] (e.g., The Internet's IP)
2.  [[📬 Network Service Models|Connection-Oriented Service]] (e.g., ATM, MPLS)

The fundamental mechanism used to move these packets through a network of routers is called [[🚦 Packet Switching]].

## Real-World Analogy: The Postal Service

Think of the Network Layer like the global postal service.
- **You (Application Layer)** write a letter and put an address on it.
- **The Network Layer** is the system that gets that letter from your local post office, puts it on various trucks and planes (routers and links), and gets it to the destination city's post office.
- It doesn't care *what* is in the letter (data), only about the source and destination addresses.

## Video 
https://www.youtube.com/watch?v=eelvWAURfdI&pp=ygUObmV0d29yayBsYXllciA%3D
