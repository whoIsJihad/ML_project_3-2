# Block Coding (nB/mB)

**Block coding** adds **redundancy** by mapping n data bits to m signal elements (where m > n). This trade-offs bandwidth for robustness: better DC-free properties, synchronization, and error detection.

## Definition

**Block coding (nB/mB):**
- Take groups of n consecutive data bits
- Map each group to a unique m-bit codeword (m > n)
- Transmit the codeword using a basic line code (e.g., NRZ)

$$r = \frac{n}{m} < 1 \quad \text{(inefficient by design)}$$

**Examples:**
- **4B/5B:** 4 data bits → 5 codeword bits (25% overhead)
- **8B/10B:** 8 data bits → 10 codeword bits (25% overhead)
- **5B/6B:** 5 data bits → 6 codeword bits (20% overhead)

## The Core Idea: Sacrificing Bandwidth for Robustness

```
Data: 8 bits
Raw transmission: 8 bits (1× baseline bandwidth)

Block coded (8B/10B):
Data: 8 bits
Codeword: 10 bits (1.25× baseline bandwidth)

Trade-off:
- 25% more bandwidth needed
- BUT: Codewords chosen to ensure:
  * Always DC-free
  * Maximum run-length limited (good sync)
  * Error detection capability
  * Balanced 0s and 1s
```

## How Block Codes Work: The Codeword Table

For **4B/5B**, there are:
- 16 possible 4-bit input patterns (all equally likely)
- 32 possible 5-bit output patterns (but only 16 are chosen as valid codewords)

```
4B/5B Codeword Mapping (partial table):
Data (4B) | Codeword (5B) | Notes
--------|-------|-------
0000    | 11110 | Avoids long runs
0001    | 01001 |
0010    | 10100 |
...     | ...   |
1111    | 11101 |

Design constraint: No codeword contains more than 3 consecutive 0s
This ensures sync every 3 bits.
```

## Why Use Block Codes? The Problems They Solve

### Problem 1: Long Runs of the Same Bit

```
Raw data: 1 1 1 1 1 1 1 1 (8 consecutive 1s)

Transmitted as Unipolar NRZ: +V +V+V +V+V +V+V +V (constant +V for 8 bit periods)
Result: Baseline wandering, loss of synchronization

Transmitted as 4B/5B:
Split into: 1111 | (1 remaining bit, padded)

1111 maps to: 11101 (codeword chosen to avoid long runs)

Codeword transmission: 11101 | (next codeword)
Result: Built-in transitions prevent baseline wandering
```

### Problem 2: DC Component

```
Raw data with many 1s (unbalanced): DC offset towards +V
After 4B/5B: Each codeword chosen from balanced set
Result: DC component = 0V (guaranteed)

Mechanism: Codeword table only includes 5-bit patterns with
2-3 ones and 2-3 zeros (balanced).
```

### Problem 3: Detection of Transmission Errors

```
Raw transmission: Single bit error changes data.
Example: 1111 becomes 1110 (loss of one 1)

Block coded: Single bit error in codeword makes it invalid.
Example: 11101 becomes 11001 (invalid codeword)
Receiver can detect: "11001 is not a valid codeword → ERROR"

Not all errors are detected (16 codewords, 32 possible patterns),
but any single bit error is caught with probability ~50%.
```

## Encoding Algorithm for 4B/5B

```
Algorithm: 4B5B_Encode(datastream, codeword_table)
  
  // Build codeword table
  codeword_table = {
    0000 → 11110,
    0001 → 01001,
    0010 → 10100,
    0011 → 10101,
    0100 → 01010,
    0101 → 01011,
    0110 → 01110,
    0111 → 01111,
    1000 → 10010,
    1001 → 10011,
    1010 → 10110,
    1011 → 10111,
    1100 → 11010,
    1101 → 11011,
    1110 → 11100,
    1111 → 11101
  }
  
  for each 4-bit group in datastream:
    codeword = codeword_table[4-bit group]
    output codeword (5 bits)
```

## Transmission Process

```
Data stream:    [Data] (4 bits)  [Data] (4 bits)  [Data] (4 bits)
                    ↓                  ↓                ↓
Encoding:       [Code] (5 bits)  [Code] (5 bits)  [Code] (5 bits)
                    ↓                  ↓                ↓
NRZ encode:     [Signal] (with transitions based on 5-bit codeword)
                    ↓                  ↓                ↓
On wire:        Signal pulses (15 pulses to transmit 12 data bits)
```

## Signal Properties

| Property | 4B/5B | 8B/10B |
|----------|-------|--------|
| **Data bits per block** | 4 | 8 |
| **Codeword size** | 5 | 10 |
| **r factor** | 0.8 | 0.8 |
| **Overhead** | 25% | 25% |
| **Valid codewords** | 16 of 32 | 256 of 1024 |
| **Max run length** | 3 | 8 |
| **DC-balanced** | Yes | Yes |
| **Typical use** | 100Base-TX | 10GBase-T, USB |

## 4B/5B in Practice: Fast Ethernet (100Base-TX)

```
Standard: IEEE 802.3u (100 Mbps Ethernet)

Data rate: 100 Mbps

Using 4B/5B:
Block size: 4 bits
Codeword size: 5 bits
Symbol rate: 100 Mbps × (5/4) = 125 Mbaud

Bandwidth needed: ≈ 125 MHz

Physical implementation:
- Twisted pair with equalizer
- Maximum distance: 100 meters
- Equalization compensates for cable loss

Why 4B/5B?
- Balanced 0s and 1s ensure DC-free transmission
- Limited run-length ensures sync is maintained
- Simple to encode/decode
- Error detection capability
- Only 25% bandwidth penalty vs. 100% for Manchester
```

## 8B/10B in Practice: Gigabit Ethernet

```
Standard: IEEE 802.3ab (Gigabit Ethernet over copper)

Data rate: 1000 Mbps

Using 4D-PAM5 with 8B/10B pre-coding:
Line rate: 1250 Mbaud (1000 Mbps × 1.25)
Bandwidth needed: ≈ 1250 MHz = 1.25 GHz

Why this combination?
- 4D-PAM5 (r = 4) provides efficiency (1 Gbps in lower bandwidth)
- 8B/10B pre-coding ensures DC-balance before PAM5 modulation
- Limited run-length maintains synchronization
- Robust error detection

Physical implementation:
- Cat6 or Cat6a twisted pair
- Advanced equalizers in receiver
- Maximum distance: 100 meters
```

## DC-Balance Guarantee: How It Works

**Key insight:** Only use codewords with equal 1s and 0s.

**Example for 4B/5B:**
- Valid codewords have 2 or 3 ones out of 5 bits
- 2 ones = 2 zeros (balanced)
- 3 ones = 2 zeros (only 1 difference)

Over a long transmission, the average is very close to DC = 0.

```
Codeword examples:
10100: 2 ones, 3 zeros (ratio 2:3)
10101: 3 ones, 2 zeros (ratio 3:2)
10110: 3 ones, 2 zeros (ratio 3:2)

In sequence: 10100, 10101, 10110
Total: 8 ones, 7 zeros (nearly balanced)
DC ≈ (8 - 7) × V / 15 ≈ 0.07V (nearly zero!)

Over 1000 blocks, imbalance averages out even further.
```

## Codeword Selection Constraints

When designing a block code (like 4B/5B), the valid codewords are chosen to satisfy:

1. **DC-balanced:** Equal 1s and 0s (or close)
2. **Run-length limited:** No more than k consecutive 0s or 1s
3. **Spreadable:** Can detect errors (unused codewords = errors)
4. **Low complexity:** Can encode/decode with simple logic

**Trade-off:** More constraints → fewer valid codewords → more error detection.

## Encoding Lookup Table (4B/5B – Complete)

```
Input (4B) | Output (5B) | Input (4B) | Output (5B)
0000      | 11110       | 1000      | 10010
0001      | 01001       | 1001      | 10011
0010      | 10100       | 1010      | 10110
0011      | 10101       | 1011      | 10111
0100      | 01010       | 1100      | 11010
0101      | 01011       | 1101      | 11011
0110      | 01110       | 1110      | 11100
0111      | 01111       | 1111      | 11101

Non-standard patterns (invalid codewords):
00000, 00001, 00010, 00011, 00100, 00101, 00110, 00111,
01000, 10000, 10001, 11000, 11001, 11111

When receiver sees these: ERROR detected
```

## Advantages

✓ **Always DC-free** — Codewords are balanced by design  
✓ **Good synchronization** — Limited run-length (3 bits for 4B/5B)  
✓ **Error detection** — Invalid codewords indicate transmission error  
✓ **Moderate bandwidth overhead** — Only 25% vs. 100% for Manchester  
✓ **Practical** — Used in real Ethernet standards  

## Disadvantages

❌ **Complexity** — Requires lookup tables  
❌ **Overhead** — 25% more bits to transmit  
❌ **Encoder/decoder needed** — Can't just use basic NRZ  
❌ **Run-length still finite** — Not perfect sync maintenance (but good enough)  

## Comparison: Raw Data vs. Block Coded

```
Transmitting 1 Mbps for 1 second:

Raw data (no coding):
- Bits transmitted: 1,000,000
- Time: 1 second
- DC component: Depends on data (could be high)
- Sync problems: Yes (on long runs)

4B/5B block coded:
- Data bits: 1,000,000
- Codeword bits: 1,250,000
- Time: 1.25 seconds
- DC component: ~0 (guaranteed)
- Sync problems: None (run-length limited)

Trade: 250,000 extra bits for guaranteed DC-free and sync.
```

## Exam Questions

**Q1:** What does "4B/5B" mean, and what's the r factor?

**A1:**
```
4B/5B means: 4 input data bits → 5 output codeword bits
r = 4/5 = 0.8

If transmitting 100 Mbps:
Signal rate = 100 / 0.8 = 125 Mbaud
Bandwidth ≈ 125 MHz
```

**Q2:** Why is 4B/5B suitable for AC-coupled channels?

**A2:**
```
Codewords are chosen to be DC-balanced (equal 0s and 1s).
DC component = 0V regardless of data pattern.
AC-coupled channels don't attenuate DC-balanced signals.
Therefore, 4B/5B is always suitable for AC-coupled channels.
```

**Q3:** How does 4B/5B provide error detection?

**A3:**
```
- 16 valid codewords (out of 32 possible 5-bit patterns)
- 16 invalid codewords are not used
- If receiver sees an invalid codeword, an error has occurred
- Single bit error in a valid codeword often produces an invalid one
- Therefore, many errors are detected automatically
```

## Related Concepts

- [[04-The-r-Factor|The r Factor]] — Why r < 1 reduces efficiency
- [[05-Data-Rate-and-Signal-Rate|Data Rate and Signal Rate]] — How to calculate bandwidth
- [[07-DC-Component|DC Component]] — Why DC-balance matters
- [[08-Self-Synchronization|Self-Synchronization]] — How run-length limits help
- [[09-Bandwidth-Efficiency|Bandwidth Efficiency]] — Trade-off analysis
- [[23-4B5B-Coding|4B/5B Coding]] — Detailed look at a specific block code
- [[24-8B10B-Coding|8B/10B Coding]] — More advanced block code
- [[27-Comparison-Matrix|Comparison Matrix]] — Where block codes fit overall
