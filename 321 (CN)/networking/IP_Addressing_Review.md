# IP Addressing Review

## IPv4 Address Structure

An IPv4 address is a 32-bit binary number, typically written in **dotted-decimal notation**:

$$
\underbrace{192}_{\text{octet 1}} . \underbrace{168}_{\text{octet 2}} . \underbrace{1}_{\text{octet 3}} . \underbrace{5}_{\text{octet 4}}
$$

Each octet represents 8 bits, so the full 32-bit address is:

$$
11000000.10101000.00000001.00000101
$$

### Converting Between Decimal and Binary

**Example: Convert 192 to binary**

$$192 = 128 + 64 = 2^7 + 2^6 = 11000000_2$$

**Example: Convert 168 to binary**

$$168 = 128 + 32 + 8 = 2^7 + 2^5 + 2^3 = 10101000_2$$

## Subnet Mask

A **subnet mask** is a 32-bit number that divides an IP address into two parts:
1. **Network portion** (which hosts are in the same network?)
2. **Host portion** (which specific host within that network?)

### Subnet Mask Structure

A subnet mask has a contiguous sequence of 1s followed by 0s:

```
Network portion    Host portion
111...111          000...000
255.255.255.0      (in decimal)
/24                (in CIDR notation)
```

**Definition**: A subnet mask with $k$ leading 1-bits (and thus $32 - k$ trailing 0-bits) is written as $k$ in CIDR notation.

**Examples:**

| Subnet Mask | Binary | CIDR | Network Bits | Host Bits |
|---|---|---|---|---|
| 255.255.255.0 | 11111111.11111111.11111111.00000000 | /24 | 24 | 8 |
| 255.255.255.128 | 11111111.11111111.11111111.10000000 | /25 | 25 | 7 |
| 255.255.0.0 | 11111111.11111111.00000000.00000000 | /16 | 16 | 16 |
| 255.0.0.0 | 11111111.00000000.00000000.00000000 | /8 | 8 | 24 |
| 0.0.0.0 | 00000000.00000000.00000000.00000000 | /0 | 0 | 32 |

## Network Address and Subnet

Given an IP address and subnet mask, we can calculate the **network address** (first address in the network) by performing a bitwise AND operation:

$$
\text{Network Address} = \text{IP Address} \text{ AND } \text{Subnet Mask}
$$

### Example: Finding the Network Address

**Given:**
- IP address: 192.168.1.137
- Subnet mask: 255.255.255.128 (/25)

**Binary representation:**
```
IP Address:    11000000.10101000.00000001.10001001
Subnet Mask:   11111111.11111111.11111111.10000000
AND operation: 11000000.10101000.00000001.10000000
Result:        192.168.1.128
```

So IP 192.168.1.137 is in the network **192.168.1.128/25**.

## Broadcast Address

The **broadcast address** is the last address in a network, calculated by setting all host bits to 1:

$$
\text{Broadcast Address} = \text{Network Address} \text{ OR } \text{(NOT Subnet Mask)}
$$

### Example: Finding the Broadcast Address

**Given:**
- Network address: 192.168.1.128/25
- Subnet mask: 255.255.255.128

**Binary representation:**
```
Network Address: 11000000.10101000.00000001.10000000
NOT Subnet Mask: 00000000.00000000.00000000.01111111
OR operation:    11000000.10101000.00000001.11111111
Result:          192.168.1.255
```

So the broadcast address in network 192.168.1.128/25 is **192.168.1.255**.

## Usable Host Addresses

In a network with $m$ host bits, there are $2^m$ total addresses, but:
- The **first address** (all host bits = 0) is the **network address** (not assigned to hosts)
- The **last address** (all host bits = 1) is the **broadcast address** (not assigned to hosts)

Therefore, the number of **usable host addresses** is:

$$
\text{Usable Hosts} = 2^m - 2
$$

### Example: Hosts in a /25 Network

**Network 192.168.1.128/25:**
- Host bits: 7 (since 32 - 25 = 7)
- Total addresses: $2^7 = 128$
- Network address: 192.168.1.128 (not usable)
- Broadcast address: 192.168.1.255 (not usable)
- **Usable host addresses: $128 - 2 = 126$**
- Range: 192.168.1.129 through 192.168.1.254

## Subnet Division (Subnetting)

A network can be divided into smaller **subnets** by extending the subnet mask (increasing the number of network bits at the expense of host bits).

### Example: Subnetting 192.168.1.0/24

Original network 192.168.1.0/24 has:
- 8 host bits
- $2^8 - 2 = 254$ usable addresses

**Divide into 4 subnets** (need 2 extra network bits):
- Extend mask from /24 to /26 (adding 2 bits)
- Each subnet has $2^{8-2} - 2 = 62$ hosts

**Resulting subnets:**

| Subnet | Network Address | Broadcast | Usable Hosts | CIDR |
|---|---|---|---|---|
| 1 | 192.168.1.0 | 192.168.1.63 | 192.168.1.1 - .62 | /26 |
| 2 | 192.168.1.64 | 192.168.1.127 | 192.168.1.65 - .126 | /26 |
| 3 | 192.168.1.128 | 192.168.1.191 | 192.168.1.129 - .190 | /26 |
| 4 | 192.168.1.192 | 192.168.1.255 | 192.168.1.193 - .254 | /26 |

### Formula for Subnetting

To divide a network into $n$ equal subnets:
- Calculate $k = \lceil \log_2(n) \rceil$ (minimum bits needed)
- New CIDR = Old CIDR + $k$
- New subnet size = $2^{32 - \text{new CIDR}}$ addresses
- Each subnet's increment = $2^{32 - \text{new CIDR}}$

## Classless Inter-Domain Routing (CIDR)

CIDR eliminated the old "classful" addressing system (Class A, B, C, D, E) and instead allows arbitrary prefix lengths.

### CIDR Notation

An address is written with its prefix length:
- 192.168.1.0/24 → network with 24-bit prefix (256 addresses)
- 10.0.0.0/8 → network with 8-bit prefix (16 million addresses)
- 172.16.50.128/25 → network with 25-bit prefix (128 addresses)

### Converting Between CIDR and Subnet Mask

| CIDR | Subnet Mask | Host Bits | Addresses |
|---|---|---|---|
| /8 | 255.0.0.0 | 24 | 16,777,216 |
| /16 | 255.255.0.0 | 16 | 65,536 |
| /24 | 255.255.255.0 | 8 | 256 |
| /25 | 255.255.255.128 | 7 | 128 |
| /26 | 255.255.255.192 | 6 | 64 |
| /27 | 255.255.255.224 | 5 | 32 |
| /28 | 255.255.255.240 | 4 | 16 |
| /29 | 255.255.255.248 | 3 | 8 |
| /30 | 255.255.255.252 | 2 | 4 |
| /31 | 255.255.255.254 | 1 | 2 |
| /32 | 255.255.255.255 | 0 | 1 |

## IPv4 Private Ranges

Not all IPv4 addresses are publicly routable. **Private address ranges** (RFC 1918) are reserved for use within organizations:

| Range | CIDR | Class | Use |
|---|---|---|---|
| 10.0.0.0 - 10.255.255.255 | 10.0.0.0/8 | A | Large organizations, enterprise networks |
| 172.16.0.0 - 172.31.255.255 | 172.16.0.0/12 | B | Medium organizations |
| 192.168.0.0 - 192.168.255.255 | 192.168.0.0/16 | C | Small networks, home/office networks |

**Special address 127.0.0.1/8:**
- Loopback range
- Packets sent to this range never leave the host
- Used for localhost communication

## IP Address Calculation Examples

### Example 1: Find all information for address 192.168.100.50/26

**Given:**
- Address: 192.168.100.50
- CIDR: /26

**Step 1: Identify bits**
- Network bits: 26
- Host bits: 32 - 26 = 6

**Step 2: Subnet mask**
- 26 ones followed by 6 zeros: 11111111.11111111.11111111.11000000
- Decimal: 255.255.255.192

**Step 3: Network address (AND with subnet mask)**
```
IP:           11000000.10101000.01100100.00110010
Subnet Mask:  11111111.11111111.11111111.11000000
Network:      11000000.10101000.01100100.00000000
              = 192.168.100.0
```

**Step 4: Broadcast address (OR with NOT subnet mask)**
```
Network Addr: 11000000.10101000.01100100.00000000
NOT Subnet:   00000000.00000000.00000000.00111111
Broadcast:    11000000.10101000.01100100.00111111
              = 192.168.100.63
```

**Step 5: Usable hosts**
- First: 192.168.100.1
- Last: 192.168.100.62
- Count: 62 hosts

**Summary:**
```
Network Address:    192.168.100.0/26
Subnet Mask:        255.255.255.192
Broadcast Address:  192.168.100.63
Usable Hosts:       192.168.100.1 - 192.168.100.62
Number of Hosts:    62
```

### Example 2: Can IP 10.5.8.200 belong to network 10.5.0.0/16?

**Step 1: Extract network bits of the IP**
- IP address: 10.5.8.200
- Network bits: 16
- Network portion: 10.5 (first 16 bits)

**Step 2: Check against network prefix**
- Network 10.5.0.0/16 has prefix 10.5
- IP's network portion: 10.5

**Step 3: Compare**
- 10.5 == 10.5 → **Yes, the IP belongs to this network**

## Practical Calculation Commands

You can perform these calculations using Linux command-line tools:

### Using ipcalc

```bash
# Install (if needed)
sudo apt-get install ipcalc

# Calculate network information
ipcalc 192.168.100.50/26

# Output:
# Address:   192.168.100.50
# Netmask:   255.255.255.192
# Broadcast: 192.168.100.63
# Usable IPs: 62 (192.168.100.1 to 192.168.100.62)
```

### Using Python

```python
from ipaddress import IPv4Network, IPv4Address

# Create network object
network = IPv4Network('192.168.100.0/26', strict=False)

# Get information
print(f"Network: {network.network_address}")
print(f"Broadcast: {network.broadcast_address}")
print(f"Netmask: {network.netmask}")
print(f"Usable hosts: {network.num_addresses - 2}")
print(f"Host range: {network[1]} to {network[-2]}")

# Check if address is in network
test_ip = IPv4Address('192.168.100.50')
print(f"{test_ip} in {network}: {test_ip in network}")
```

---

## Next Steps

- [[Routing_Fundamentals]] — Apply these concepts to routing
- [[Routing_Tables_and_Forwarding_Mechanics]] — Use CIDR for routing tables
