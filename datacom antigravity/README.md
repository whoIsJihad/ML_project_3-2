# Data Communications (CSE 311) — Study Vault Syllabus

Welcome to the comprehensive, exam-ready study vault for Data Communications. This vault is designed to be read sequentially, building from the raw physics of why we need modulation all the way to advanced error-correcting codes and information theory.

Follow this sequence to build a coherent mental model of the entire course.

---

## Module 1: The Foundations of Modulation
*Start here to understand what a carrier is and why we can't just plug a microphone straight into an antenna.*
1. [[00 - Why Modulation Exists]]
2. [[01 - Carrier Signals]]
3. [[02 - Analog vs Digital Modulation]]

## Module 2: Analog Amplitude Modulation (AM)
*The earliest form of radio. Learn how we bury data in the voltage level of a wave.*
4. [[03 - Amplitude Modulation (AM)]]
5. [[20 - DSB-SC Modulation]]
6. [[21 - Single Sideband Modulation (SSB)]]
7. [[22 - Vestigial Sideband Modulation (VSB)]]
8. [[23 - AM Modulators and Demodulators]]
9. [[24 - Frequency Division Multiplexing (FDM)]]

## Module 3: Analog Angle Modulation (FM & PM)
*Moving from voltage to rotation speed. The mathematical jump that gave us noise immunity.*
10. [[04 - Angle Modulation (FM and PM)]]
11. [[25 - Phase Locked Loop (PLL)]]

## Module 4: The Digital Bridge
*How do we take analog concepts and apply them to discrete bits (0s and 1s)? This is the transition to modern communications.*
12. [[06 - Signals, Sampling, and Pulse Modulation]] *(Niaz Sir's comprehensive module on Fourier, Sampling, PCM, and Line Coding)*
13. [[05 - Advanced Angle and Digital Modulation]] *(This is the massive transition guide covering ASK, FSK, PSK, and DPSK)*
14. [[09 - Quadrature Amplitude Modulation (QAM)]]
15. [[10 - OFDM]]

## Module 5: System Performance & Trade-offs
*In engineering, everything is a trade-off. How do bandwidth, noise, and power interact?*
16. [[11 - Bandwidth and Spectral Efficiency]]
17. [[12 - Noise and BER]]
18. [[14 - Modulation Comparison Table]]
19. [[15 - How to Analyze Any New Modulation]]
20. [[13 - Real World Systems]]

## Module 6: Information Theory
*Shannon's mathematical laws of the universe. What is "data", and what are the physical limits of transmitting it?*
21. [[16 - Information Content and Entropy]]
22. [[17 - Source Coding and Huffman Coding]]
23. [[18 - Channel Capacity]]
24. [[19 - Shannon's Channel Capacity Theorem]]

## Module 7: Error Correcting Codes (ECC)
*We've hit the Shannon limit. The channel is noisy and bits are flipping. How do we add mathematical redundancy to fix errors on the fly?*
25. [[26 - Block Code Basics and Foundation]]
26. [[27 - Linear Block Codes]]
27. [[28 - Hamming Codes]]
28. [[29 - Cyclic Codes]]
29. [[30 - Cyclic Redundancy Checks (CRC)]]
30. [[31 - ECC Comparison and Synthesis]]

## Module 8: Advanced ECC (State & Memory)
*Moving from blocks of data to continuous streams. How modern satellites and 5G actually handle noise.*
31. [[32 - Convolutional Codes: Foundations and Encoding]]
32. [[33 - The Viterbi Algorithm: Decoding and Trellis Math]]

---

> [!tip] Note on Deprecated Files
> As this vault evolved to be more unified and comprehensive, several older notes were merged. You will see files like `04 - Frequency Modulation (FM).md`, `05 - Phase Modulation (PM).md`, `07 - ASK and FSK.md`, and `08 - Phase Shift Keying (PSK).md`. These are now **redirects**. Follow the syllabus above and it will naturally guide you to the newest, most comprehensive versions.
