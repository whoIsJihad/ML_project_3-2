# The r Factor

The **r factor** is the ratio of data elements to signal elements. This single number determines bandwidth efficiency.

## Definition

$$r = \frac{N_d}{N_s} = \frac{\text{Number of data elements}}{\text{Number of signal elements}}$$

Equivalently:
$$r = \text{Average number of data bits per signal element}$$

## Three Cases

### Case 1: r = 1 (Most Common for Basic Schemes)

**One data bit per signal element.**

- Examples: Unipolar NRZ, Polar NRZ-L, NRZ-I, RZ, Manchester, AMI
- Characteristic: Every bit becomes exactly one "symbol" or "pulse"
- Bandwidth: Baseline (higher bandwidth than r > 1, lower than r < 1)
- Baud rate = Bit rate

### Case 2: r > 1 (Multilevel Codes – Higher Efficiency)

**Multiple data bits per signal element.**

**Beginner Explanation:** Imagine you're sending messages, but instead of sending one letter at a time (like r=1), you group several letters together and represent the whole group with a single special symbol. This way, you send fewer symbols overall, which is like talking faster without using more words. In digital terms, r>1 means packing more bits into each signal pulse, so you need fewer pulses per second to send the same amount of data.

Examples:
- 2B1Q: r = 2 (two bits → one quaternary symbol)
- 8B6T: r = 8/6 ≈ 1.33 (eight bits → six ternary symbols)
- 4D-PAM5: r = 4 (four bits → one pentary symbol)

**Characteristic:** Group multiple bits and encode them as a single voltage level

**Advantage:** Lower baud rate means **lower bandwidth requirement**
$$f_s = \frac{f_b}{r} < f_b$$
$$\text{Why? Baud rate } f_s \text{ is bit rate } f_b \text{ divided by } r. \text{ Since } r > 1, f_s \text{ is smaller than } f_b. \text{ Fewer symbols per second = less bandwidth needed.}$$

**Disadvantage:** Need $2^r$ distinguishable voltage levels, which is harder to detect reliably in noise

$$\text{Signal levels needed} = 2^r$$
$$\text{Why } 2^r\text{? With } r \text{ bits, there are } 2^r \text{ possible combinations (e.g., } r=1\text{: 2 levels for 0/1; } r=2\text{: 4 levels for 00/01/10/11). Each combination needs its own voltage level.}$$

For r = 2 (2B1Q): Need 4 levels  
For r = 4 (4D-PAM5): Need 16 levels

### Case 3: r < 1 (Block Coding – Redundancy)

**One data bit spans multiple signal elements.**

Examples:
- 4B/5B: r = 4/5 = 0.8 (four bits → five symbols, adds 1 redundant bit per group)
- 8B/10B: r = 8/10 = 0.8 (eight bits → ten symbols, adds 2 redundant bits per group)

**Characteristic:** Add redundant bits for error detection or to improve signal properties

**Advantage:** Redundant bits can be chosen to:
- Prevent long strings of 0s or 1s
- Ensure DC-free or nearly DC-free signals
- Provide error detection

**Disadvantage:** Baud rate **increases** (transmit more symbols to send the same data)
$$f_s = \frac{f_b}{r} > f_b \quad \text{(since } r < 1 \text{)}$$

## Relationship to Bandwidth

The fundamental relationship between baud rate and bandwidth is:

$$\text{Baud rate} = f_s = \frac{f_b}{r}$$

If the signal uses "simple" transitions (like on-off), then:
$$\text{Required bandwidth} \propto f_s = \frac{f_b}{r}$$

**Consequence:**
- **Large r (> 1):** Lower bandwidth (efficient use of spectrum)
- **Small r (< 1):** Higher bandwidth (redundancy costs bandwidth)

## Trade-off Matrix

```
                    Bandwidth    Signal Levels    Error Detection    Complexity
r = 1              Medium        2                Poor                Low
(Unipolar, Polar)

r > 1              Low            2^r (High)       Poor               Medium-High
(2B1Q, 4D-PAM5)

r < 1              High           2 (Low)          Excellent          Medium
(4B/5B, 8B/10B)
```

## Practical Examples

### Example 1: 2B1Q (r = 2)

```
Input bit rate: 1000 bps
r = 2
Output baud rate: 1000 / 2 = 500 baud

Bandwidth needed: ~500 Hz (vs. ~1000 Hz for r = 1)

Encoding:
00 → -3V
01 → -V
10 → +V
11 → +3V

Example: 10 11 00 01
Signal: [+V] [+3V] [-3V] [-V]

```
![[note_04.png]]
### Example 2: 4B/5B (r = 4/5)

```
Input bit rate: 1000 bps
r = 0.8
Output baud rate: 1000 / 0.8 = 1250 baud

Bandwidth needed: ~1250 Hz (vs. ~1000 Hz for r = 1)
Trade-off: Slightly wider bandwidth, but gains error detection and DC-free signal.

Encoding: (Every 4-bit group maps to a 5-bit codeword)
0000 → 11110 (example)
0001 → 01001
...and so on (256 total 4-bit patterns → 32 valid 5-bit codewords chosen)

Each 5-bit codeword is then transmitted using a basic scheme (e.g., NRZ).
```

## Choosing r for Your Problem

### If you need **maximum data rate** on a bandwidth-limited channel:
→ Use **r > 1** (multilevel)

Example: Digital Subscriber Line (DSL, r = 2 for 2B1Q, r = 4 for 4D-PAM5)

### If you need **simplicity and robustness** (error tolerance):
→ Use **r = 1** (basic schemes)

Example: Ethernet 10Base-T (Manchester, r = 1)

### If you need **reliable error detection** without increasing bandwidth much:
→ Use **r < 1** (block coding)

Example: Ethernet 4B/5B (100Base-TX) adds redundancy for sync and error detection

## Exam-Typical Questions

**Q1:** A line code uses 8 bits of data and represents them as 10 transmitted symbols. What is r? What is the baud rate if the bit rate is 1 Mbps?

**A1:**
$$r = \frac{8}{10} = 0.8$$
$$f_s = \frac{f_b}{r} = \frac{1 \text{ Mbps}}{0.8} = 1.25 \text{ Mbaud}$$

**Q2:** In 2B1Q, how many signal levels are needed? If the bit rate is 56 kbps, what is the baud rate?

**A2:**
$$\text{Levels needed} = 2^r = 2^2 = 4 \text{ levels}$$
$$f_s = \frac{56 \text{ kbps}}{2} = 28 \text{ kbaud}$$

## Related Concepts

- [[03-Data-Elements-vs-Signal-Elements|Data Elements vs. Signal Elements]] — Foundational concept
- [[05-Data-Rate-and-Signal-Rate|Data Rate and Signal Rate]] — Formal definitions and formulas
- [[09-Bandwidth-Efficiency|Bandwidth Efficiency]] — How to compare schemes systematically
- [[18-Multilevel-Coding|Multilevel Coding Principles]] — r > 1 schemes in detail
- [[22-Block-Coding|Block Coding (nB/mB)]] — r < 1 schemes in detail
