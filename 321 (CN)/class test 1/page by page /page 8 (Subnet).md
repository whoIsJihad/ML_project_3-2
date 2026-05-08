# **Subnet (Subnetwork)**

A **subnet** is a logical subdivision of an IP network. It divides a large network into smaller, manageable networks to improve **address utilization, performance, security, and routing efficiency**.

### Core idea

- An IP address has **network part + host part**.
    
- **Subnetting** borrows bits from the host part to create **smaller networks** within the same original network.
    

### How it works

- A **subnet mask** (IPv4) or **prefix length** (CIDR, e.g., `/24`) defines:
    
    - which bits identify the **network/subnet**
        
    - which bits identify the **host**
        
- Devices in the **same subnet** can communicate directly.
    
- Devices in **different subnets** require a **router**.
    

### Example

- Network: `192.168.1.0/24`
    
- Subnetting into two:
    
    - `192.168.1.0/25` → hosts `.1`–`.126`
        
    - `192.168.1.128/25` → hosts `.129`–`.254`
        
- Each subnet is a separate broadcast domain.
    

### Why subnetting is used

- **Efficient IP address use** (avoid wasting addresses)
    
- **Reduce broadcast traffic**
    
- **Improve security** (isolation between subnets)
    
- **Simplify network management**
    
- **Enable hierarchical routing** (smaller routing tables)
    

### Key terms

- **Network address**: first address in subnet (all host bits 0)
    
- **Broadcast address**: last address in subnet (all host bits 1)
    
- **Usable hosts**: total addresses − 2 (IPv4)
    
- **CIDR**: Classless Inter-Domain Routing, flexible subnet sizes
    

### One-line definition (for exams)

> A subnet is a logical division of an IP network created by using a subnet mask to split the network into smaller networks.