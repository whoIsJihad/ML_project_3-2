# Line Coding: Complete Study Reference

This is your comprehensive, self-contained study material for line coding theory and practice. Use this map to navigate the notes systematically.

## How to Use This Material

1. **Read sequentially** within each section to build concepts
2. **Follow wikilinks** when you encounter unfamiliar terms
3. **Study diagrams carefully** — they show the actual signal behavior
4. **Work through examples** with pen and paper
5. **Compare schemes** using the evaluation metrics

---

## Part A: Foundational Concepts

These are the fundamental concepts you *must* understand before anything else.

1. [[01-Digital-Signal-Fundamentals|Digital Signal Fundamentals]] — What is a digital signal? Voltage levels, transitions, bit vs. symbol
2. [[02-Line-Coding-Basics|Line Coding Basics]] — Definition, purpose, and the fundamental problem it solves
3. [[03-Data-Elements-vs-Signal-Elements|Data Elements vs. Signal Elements]] — The critical distinction between bits and pulses
4. [[04-The-r-Factor|The r Factor]] — Mathematical relationship between data and signal elements
5. [[05-Data-Rate-and-Signal-Rate|Data Rate and Signal Rate]] — Bit rate, baud rate, and their relationship

---

## Part B: Evaluation Metrics

Before judging any coding scheme, understand these quality measures.

6. [[06-Baseline-Wandering|Baseline Wandering]] — Why long bit sequences cause synchronization failure
7. [[07-DC-Component|DC Component]] — The constant voltage offset that breaks AC-coupled channels
8. [[08-Self-Synchronization|Self-Synchronization]] — Why timing information in the signal matters
9. [[09-Bandwidth-Efficiency|Bandwidth Efficiency]] — How to compare signal efficiency across schemes

---

## Part C: Line Coding Schemes

Study each scheme in isolation, then compare using Part B metrics.

### Unipolar Codes
10. [[10-Unipolar-NRZ|Unipolar NRZ]] — The simplest scheme (but with major flaws)

### Polar Codes
11. [[11-Polar-NRZ-L|Polar NRZ-L]] — Using both positive and negative voltages
12. [[12-Polar-NRZ-I|Polar NRZ-I]] — Differential encoding for inversion tolerance
13. [[13-Polar-RZ|Polar RZ]] — Return-to-zero and partial-response signaling

### Biphase Codes (Self-Synchronizing)
14. [[14-Manchester-Coding|Manchester Coding]] — The industry standard (used in Ethernet, legacy protocols)
15. [[15-Differential-Manchester|Differential Manchester]] — Improved synchronization robustness

### Bipolar Codes (Three Voltage Levels)
16. [[16-AMI-Alternate-Mark-Inversion|AMI (Alternate Mark Inversion)]] — Using three levels efficiently
17. [[17-Pseudoternary|Pseudoternary]] — Variant of AMI with inverted roles

### Multilevel Codes (Efficiency Focus)
18. [[18-Multilevel-Coding|Multilevel Coding Principles]] — Encoding multiple bits per symbol
19. [[19-2B1Q|2B1Q Coding]] — 2 bits to 1 quaternary symbol
20. [[20-8B6T-4D-PAM5|8B6T and 4D-PAM5]] — Advanced multilevel schemes

### Multitransition Codes
21. [[21-MLT-3|MLT-3 (Multi-Level Transmission-3)]] — Complex transitions for specific applications

---

## Part D: Advanced Robustness

Adding redundancy and scrambling for error detection and DC removal.

22. [[22-Block-Coding|Block Coding (nB/mB)]] — Adding redundant bits (e.g., 4B/5B, 8B/10B)
23. [[23-4B5B-Coding|4B/5B Coding]] — Practical example of block coding
24. [[24-8B10B-Coding|8B/10B Coding]] — Industrial standard for high-speed links
25. [[25-Scrambling|Scrambling Principles]] — Randomizing bit patterns without bandwidth increase
26. [[26-B8ZS-HDB3|B8ZS and HDB3]] — Practical scrambling schemes for T-carrier systems

---

## Part E: Synthesis and Comparison

27. [[27-Comparison-Matrix|Complete Comparison Matrix]] — DC presence, synchronization, bandwidth, applications
28. [[28-Scheme-Selection-Criteria|How to Choose a Coding Scheme]] — Decision tree for exam and real-world problems
29. [[29-Exam-Strategy|Exam Strategy for Line Coding]] — High-probability questions and how to solve them

---

## Quick Cheat Sheet for Exams

| Scheme | DC | Self-Sync | BW | r | Notes |
|--------|----|-----------|----|---|-------|
| Unipolar NRZ | Yes | No | 1 | 1 | Simplest, avoid it |
| Polar NRZ-L | No | No | 1 | 1 | Standard for storage |
| Polar NRZ-I | No | No | 1 | 1 | Good for clock recovery |
| Polar RZ | No | No | 2 | 1 | High power, good sync detection |
| Manchester | No | Yes | 2 | 1 | Ethernet standard |
| Diff Manchester | No | Yes | 2 | 1 | Token Ring standard |
| AMI | No | No | 1 | 1 | Three levels, efficient |
| Pseudoternary | No | No | 1 | 1 | Variant of AMI |
| 2B1Q | No | No | 0.5 | 2 | Double efficiency, harder detection |
| 8B6T | No | Depends | ~0.75 | 1.33 | Balanced for real channels |
| 4D-PAM5 | No | No | 0.8 | 2.5 | Gigabit Ethernet |
| B8ZS | No | No | 1 | 1 | Fixes AMI long 0s problem |
| HDB3 | No | No | 1 | 1 | Fixes AMI long 0s, alternate method |

---

## How to Study Each Topic

For **every scheme**:
1. Understand the **encoding rule** (how bits become signals)
2. Trace through an **example bitstream** (like `10110001`)
3. Identify **advantages and disadvantages** using Part B metrics
4. Know where it's **actually used** (Ethernet, DSL, T-carriers, etc.)

For **exams**:
- You will be asked to **encode/decode** a bitstream — practice this
- You will be asked **why** a scheme is better — use the metrics
- You will be asked **how to fix problems** — think about DC, sync, and bandwidth

---

## Navigation Tips

- **If stuck on a concept:** Check the wikilinks in that note's prerequisites
- **If comparing schemes:** Go to [[27-Comparison-Matrix|Comparison Matrix]]
- **If unsure what to study:** Follow [[29-Exam-Strategy|Exam Strategy]]
- **If seeing a term you don't recognize:** Use Ctrl+F to search all notes

---

**Status:** Complete, self-contained tutorial. No external references needed.
