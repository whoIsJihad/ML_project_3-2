# Quick Command Reference for Network Layer Exploration

## Essential Linux/Unix Network Tools

This is a reference for commands to explore Network Layer concepts directly.

### Core Tools

#### ping — Test Reachability (ICMP Echo)

```bash
# Basic ping (sends 4 packets on Linux, continuous on Mac/Windows)
ping 8.8.8.8

# Specific packet count
ping -c 10 8.8.8.8

# Specific payload size (test for MTU issues)
ping -s 1472 8.8.8.8  # 1472 + 28 header = 1500 (standard MTU)

# With timeout per packet
ping -W 2 8.8.8.8  # 2 second timeout

# Flood ping (dangerous: CPU intensive)
# sudo ping -f 8.8.8.8  # Don't use in production!

# Exit after first response
ping -c 1 8.8.8.8; echo "Result: $?"
```

#### traceroute — Discover Network Path (TTL expiry)

```bash
# Basic traceroute (uses ICMP or UDP)
traceroute 8.8.8.8

# Using ICMP instead of UDP
sudo traceroute -I 8.8.8.8

# Maximum hops to try
traceroute -m 20 8.8.8.8

# Number of probes per hop
traceroute -q 1 8.8.8.8  # Fewer probes = faster, less accurate

# Don't resolve hostnames
traceroute -n 8.8.8.8
```

#### mtr — Combined ping + traceroute

```bash
# Real-time analysis (interactive)
mtr 8.8.8.8

# Report mode (non-interactive, 100 probes)
mtr -c 100 --report 8.8.8.8

# Curses mode with key options: p=pause, d=details, q=quit
mtr 8.8.8.8
```

### Routing and Interface Information

#### ip route — View/Modify Routing Table

```bash
# Show all routes
ip route show

# Show route to specific destination
ip route show 8.8.8.8

# Show routing policy (for advanced routing)
ip rule show

# Add static route
sudo ip route add 10.1.0.0/24 via 192.168.1.10

# Add default route
sudo ip route add default via 192.168.1.1

# Delete route
sudo ip route del 10.1.0.0/24 via 192.168.1.10

# Show detailed route with all info
ip -4 route show
```

#### ip addr — View Interface Information

```bash
# Show all interfaces with IP addresses
ip addr show

# Show specific interface
ip addr show eth0

# Short format
ip -br addr show

# Show IPv4 only
ip -4 addr show
```

#### route (legacy) — Old-style routing commands

```bash
# Show routing table
route -n  # -n avoids DNS lookup

# Add route
sudo route add -net 10.0.0.0 netmask 255.255.255.0 gw 192.168.1.1

# Delete route
sudo route del -net 10.0.0.0 netmask 255.255.255.0 gw 192.168.1.1

# Add default route
sudo route add default gw 192.168.1.1
```

### Packet Inspection and Capture

#### tcpdump — Capture and Analyze Packets

```bash
# Capture all packets on interface eth0
sudo tcpdump -i eth0

# Capture only ICMP (ping)
sudo tcpdump -i eth0 icmp

# Capture only TCP traffic
sudo tcpdump -i eth0 tcp

# Capture with source/destination filter
sudo tcpdump -i eth0 src 192.168.1.1
sudo tcpdump -i eth0 dst 8.8.8.8
sudo tcpdump -i eth0 src 192.168.1.1 and dst 8.8.8.8

# Save to file for later analysis
sudo tcpdump -i eth0 -w capture.pcap

# Read from file
tcpdump -r capture.pcap

# Verbose output (more details)
sudo tcpdump -i eth0 -vvv

# Show packet content (hex and ASCII)
sudo tcpdump -i eth0 -A

# Show only headers, no data
sudo tcpdump -i eth0 -H
```

#### wireshark / tshark — GUI and CLI packet analysis

```bash
# Install Wireshark
sudo apt-get install wireshark-qt wireshark-cli

# Launch GUI (requires graphical interface)
wireshark

# CLI analysis (similar to tcpdump but with Wireshark filters)
tshark -i eth0 -f "icmp"

# Capture to file and analyze
tshark -i eth0 -w trace.pcap
# Later: wireshark trace.pcap  (GUI)
```

### Network Performance and Diagnostics

#### iftop — Real-time Traffic Monitor

```bash
# Install
sudo apt-get install iftop

# Monitor eth0 in real-time
sudo iftop -i eth0

# Pause/Resume: p
# Exit: q
# Sort by: <, >, S (source), D (destination)
```

#### nethogs — Per-process Network Usage

```bash
# Install
sudo apt-get install nethogs

# Show network usage by process
sudo nethogs eth0

# For each process, shows: Sent, Received, Total usage
# Sort by column: s (sent), r (received), t (total)
# Exit: q
```

#### nload — Network Load Monitor

```bash
# Install
sudo apt-get install nload

# Monitor bandwidth usage
nload eth0

# Threshold colors, arrows showing trend
# Shows: Avg, Current, Total
```

#### netstat — Network Connections and Statistics

```bash
# Show all listening ports
netstat -tlnp  # -t (TCP), -l (listening), -n (numeric), -p (program)

# Show active connections
netstat -tnp

# Show statistics by protocol
netstat -s

# Show interface statistics
netstat -i

# Watch in real-time
watch -n 1 'netstat -tlnp'
```

#### ss — Modern netstat replacement

```bash
# Show listening sockets
ss -tlnp

# Show TCP sockets
ss -tn

# Show UDP sockets
ss -un

# Show with timer info
ss -o

# Filter by state
ss -tn state ESTABLISHED
ss -tn state LISTEN
ss -tn state TIME-WAIT
```

### IP Configuration and Testing

#### netcat — Network Swiss-Army Knife

```bash
# Test TCP port connectivity
nc -zv 8.8.8.8 53  # -z (zero I/O), -v (verbose)

# Test UDP port
nc -uzv 8.8.8.8 53

# Listen on port 9999
nc -l 9999

# Connect to listening server
nc 192.168.1.100 9999

# Send file over network
# Server: nc -l 9999 > received_file.txt
# Client: nc 192.168.1.100 9999 < send_file.txt

# Port scanning (simple)
nc -zv 192.168.1.1 1-1000  # Scan ports 1-1000
```

#### telnet — Connect to Port and Send Text

```bash
# Connect to HTTP server
telnet 8.8.8.8 80
# Type: GET / HTTP/1.1<Enter>
# Type: Host: 8.8.8.8<Enter><Enter>

# Test if port is open
telnet 192.168.1.1 22  # SSH port

# Exit: Ctrl+], then type "quit"
```

### Network Configuration

#### ifconfig (legacy) — Configure Network Interfaces

```bash
# Show all interfaces
ifconfig -a

# Show specific interface
ifconfig eth0

# Set IP address
sudo ifconfig eth0 192.168.1.100

# Set netmask
sudo ifconfig eth0 netmask 255.255.255.0

# Set both
sudo ifconfig eth0 192.168.1.100 netmask 255.255.255.0

# Bring interface up
sudo ifconfig eth0 up

# Bring interface down
sudo ifconfig eth0 down
```

#### ip addr (modern) — Configure with ip command

```bash
# Add IP address
sudo ip addr add 192.168.1.100/24 dev eth0

# Remove IP address
sudo ip addr del 192.168.1.100/24 dev eth0

# Set primary address
sudo ip addr flush eth0
sudo ip addr add 192.168.1.100/24 dev eth0

# Bring interface up
sudo ip link set eth0 up

# Bring interface down
sudo ip link set eth0 down
```

### DNS and Name Resolution

#### nslookup — Query DNS Records

```bash
# Resolve hostname to IP
nslookup google.com

# Query specific nameserver
nslookup google.com 8.8.8.8

# Reverse DNS lookup (IP to hostname)
nslookup 8.8.8.8

# Query specific record type
nslookup -type=MX gmail.com
nslookup -type=NS google.com
nslookup -type=A google.com
```

#### dig — Advanced DNS Query

```bash
# Query A record (IP address)
dig google.com

# Query specific record type
dig google.com MX
dig google.com NS
dig google.com CNAME

# Short output
dig google.com +short

# Reverse DNS
dig -x 8.8.8.8

# Query specific nameserver
dig @8.8.8.8 google.com

# Trace DNS resolution path
dig google.com +trace
```

#### host — Simple DNS Lookup

```bash
# Resolve hostname
host google.com

# Reverse DNS
host 8.8.8.8

# Query specific nameserver
host google.com 8.8.8.8

# Verbose output
host -v google.com
```

## Complex Diagnostic Scenarios

### Scenario 1: Host Is Unreachable

```bash
# 1. Check local connectivity
ping 192.168.1.1  # Your gateway

# 2. Check routing table
ip route show

# 3. Check if route exists to destination
ip route show 10.0.0.0/8

# 4. Trace path to destination
traceroute 10.0.0.1

# 5. Check interface status
ip link show eth0
# Look for: UP/DOWN status

# 6. Check if firewall is blocking
sudo iptables -L -n  # List firewall rules
```

### Scenario 2: Slow Network Performance

```bash
# 1. Check current interface stats
ifstat -i eth0 1  # Update every 1 second

# 2. Monitor real-time traffic
mtr -c 100 --report destination.com

# 3. Check for packet loss on path
ping -c 100 8.8.8.8 | tail -1  # Shows % loss

# 4. Test with different packet sizes (MTU issues)
ping -s 1472 -M do 8.8.8.8

# 5. Check if link is full duplex
ethtool eth0 | grep Duplex

# 6. Monitor bandwidth per connection
iftop -i eth0
```

### Scenario 3: Route Not Found

```bash
# 1. Check routing table
route -n

# 2. Add debug routing (depends on routing protocol)
# For static routing:
sudo ip route add 10.0.0.0/24 via 192.168.1.1

# 3. Verify route was added
ip route show 10.0.0.0/24

# 4. Test connectivity
ping 10.0.0.1

# 5. Check ARP (MAC address table)
arp -a
arp -n  # Don't resolve names

# 6. If no ARP entry, device might not respond
arp 10.0.0.1  # Check ARP entry for specific IP
```

## Quick Diagnostic Scripts

### Script 1: Check Internet Connectivity

```bash
#!/bin/bash
# Check_Internet_Connectivity.sh

echo "=== Internet Connectivity Check ==="

# 1. Check gateway
echo "1. Testing gateway..."
if ping -c 1 192.168.1.1 > /dev/null; then
    echo "✓ Gateway is reachable"
else
    echo "✗ Gateway is unreachable"
    exit 1
fi

# 2. Check DNS server
echo "2. Testing DNS server..."
if ping -c 1 8.8.8.8 > /dev/null; then
    echo "✓ DNS server is reachable"
else
    echo "✗ DNS server is unreachable"
fi

# 3. Check DNS resolution
echo "3. Testing DNS resolution..."
if host google.com > /dev/null 2>&1; then
    echo "✓ DNS resolution working"
else
    echo "✗ DNS resolution failed"
fi

# 4. Check Internet connectivity
echo "4. Testing Internet connectivity..."
if curl -s -o /dev/null -w "%{http_code}" https://www.google.com | grep -q "200"; then
    echo "✓ Internet is accessible"
else
    echo "✗ Internet is not accessible"
fi
```

### Script 2: Trace Latency Increase

```bash
#!/bin/bash
# Monitor_Latency.sh

TARGET=${1:-8.8.8.8}
INTERVAL=5
THRESHOLD=50  # ms

echo "Monitoring latency to $TARGET (threshold: ${THRESHOLD}ms)"

while true; do
    LATENCY=$(ping -c 1 -W 2 $TARGET 2>/dev/null | grep "time=" | awk -F'time=' '{print $2}' | awk '{print $1}' | tr -d 'ms')
    
    if [ -z "$LATENCY" ]; then
        echo "$(date): No response from $TARGET"
    else
        if (( $(echo "$LATENCY > $THRESHOLD" | bc -l) )); then
            echo "$(date): ALERT - Latency high: ${LATENCY}ms"
        else
            echo "$(date): OK - Latency: ${LATENCY}ms"
        fi
    fi
    
    sleep $INTERVAL
done
```

---

## Installation Guide for Common Tools

### Ubuntu/Debian

```bash
# All network tools in one command
sudo apt-get update
sudo apt-get install -y \
    iputils-ping \
    traceroute \
    mtr \
    dnsutils \
    net-tools \
    iproute2 \
    netcat \
    tcpdump \
    wireshark-cli \
    iftop \
    nethogs \
    nload \
    curl \
    wget
```

### CentOS/RHEL

```bash
# All network tools for CentOS
sudo yum install -y \
    iputils \
    traceroute \
    mtr \
    bind-utils \
    net-tools \
    iproute \
    nc \
    tcpdump \
    wireshark \
    iftop \
    nethogs \
    nload \
    curl \
    wget
```

---

## Next Steps

- [[Network_Layer_Practical_Diagrams]] — Visual diagrams and simulations
- [[Routing_Fundamentals]] — Understand concepts behind these tools
- [[ICMP_Protocol]] — Deep dive into ping and traceroute
