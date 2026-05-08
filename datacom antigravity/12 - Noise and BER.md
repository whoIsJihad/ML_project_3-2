# Noise and BER

> **Prerequisites**: [[11 - Bandwidth and Spectral Efficiency]], [[08 - Phase Shift Keying (PSK)]], [[09 - Quadrature Amplitude Modulation (QAM)]]
> **Related**: [[14 - Modulation Comparison Table]], [[13 - Real World Systems]]

---

## What Problem Does This Solve?

Every communication channel adds **noise**. The fundamental question is: *Given a modulation scheme and a certain noise level, how many bits will be received incorrectly?*

This is quantified by the **Bit Error Rate (BER)** — the probability that a received bit is wrong.

---

## Key Noise Concepts

### AWGN — Additive White Gaussian Noise

The standard noise model:
- **Additive**: adds to the signal ($r = s + n$)
- **White**: flat power spectral density across all frequencies
- **Gaussian**: amplitude follows a Gaussian distribution $N(0, \sigma^2)$

$$r(t) = s(t) + n(t), \qquad n(t) \sim N(0, N_0/2)$$

Where $N_0$ = noise power spectral density (W/Hz).

### Signal-to-Noise Ratio (SNR)

$$\text{SNR} = \frac{S}{N} = \frac{\text{Signal Power}}{\text{Noise Power}}, \qquad \text{SNR (dB)} = 10\log_{10}\frac{S}{N}$$

### Eb/N0 — Energy per Bit to Noise Density

The **universal** metric for comparing modulation schemes fairly:

$$\frac{E_b}{N_0} = \frac{S/R_b}{N_0} = \frac{\text{SNR} \cdot B}{R_b} = \frac{\text{SNR}}{\eta}$$

Where $\eta$ = spectral efficiency (bits/s/Hz).

> **Why Eb/N0 instead of SNR?** Different modulation schemes have different bandwidth efficiency. Eb/N0 normalizes by bit rate, making fair comparison possible.

---

## BER Formulas for Common Schemes

### Digital Modulation BER (AWGN Channel)

| Scheme | BER Formula | Relative Performance |
|--------|-------------|---------------------|
| **BPSK** | $Q\left(\sqrt{\frac{2E_b}{N_0}}\right)$ | **Best** (reference) |
| **QPSK** | $Q\left(\sqrt{\frac{2E_b}{N_0}}\right)$ | Same as BPSK! |
| **M-PSK** | $\approx \frac{2}{\log_2 M} Q\left(\sqrt{2\log_2 M \cdot \frac{E_b}{N_0}} \sin\frac{\pi}{M}\right)$ | Degrades with M |
| **M-QAM** | $\approx \frac{4(\sqrt{M}-1)}{\sqrt{M}\log_2 M} Q\left(\sqrt{\frac{3\log_2 M}{M-1}\cdot\frac{2E_b}{N_0}}\right)$ | Degrades with M |
| **BFSK** (coherent) | $Q\left(\sqrt{\frac{E_b}{N_0}}\right)$ | 3 dB worse than BPSK |
| **BFSK** (non-coh.) | $\frac{1}{2}e^{-E_b/(2N_0)}$ | ~4 dB worse than BPSK |
| **DBPSK** | $\frac{1}{2}e^{-E_b/N_0}$ | ~1 dB worse than BPSK |

Where $Q(x) = \frac{1}{2}\text{erfc}\left(\frac{x}{\sqrt{2}}\right)$

### Required Eb/N0 for BER = 10⁻⁶

| Scheme | Eb/N0 Required | Spectral Efficiency |
|--------|----------------|---------------------|
| BPSK | 10.5 dB | 1 bit/s/Hz |
| QPSK | 10.5 dB | 2 bits/s/Hz |
| 8-PSK | 14 dB | 3 bits/s/Hz |
| 16-QAM | 14.5 dB | 4 bits/s/Hz |
| 64-QAM | 18.5 dB | 6 bits/s/Hz |
| 256-QAM | 22.5 dB | 8 bits/s/Hz |

> **Pattern**: Each doubling of QAM order adds ~4 dB to the SNR requirement. You gain 1 bit/symbol but pay ~4 dB in power.

---

## BER Comparison Chart

![BER Curves and Comparison Charts](diagrams/comparison_charts.png)

The BER curves (upper right) show how quickly BER drops with increasing Eb/N0. Notice:
- BPSK/QPSK drop fastest (steepest "waterfall")
- Higher-order QAM curves are shifted right (need more power)

---

## How Noise Affects Different Modulation Types

### Amplitude-Based (AM, ASK, QAM)
- Noise **directly adds to amplitude** → worst immunity
- QAM: noise can push a point to the wrong decision region
- Higher QAM order → smaller decision regions → more errors

### Frequency-Based (FM, FSK)
- Noise affects amplitude but **not frequency** (with limiting)
- FM discriminator output: noise increases with frequency ("triangular" noise spectrum)
- FSK: non-coherent detection naturally rejects amplitude noise

### Phase-Based (PM, PSK)
- Phase noise from oscillator instability
- PSK: noise rotates the constellation → errors when crossing decision boundary
- DPSK: phase difference measurement partially cancels common-mode phase noise

### OFDM-Specific
- Per-subcarrier BER depends on that subcarrier's SNR
- **Frequency-selective fading** → some subcarriers have poor SNR
- Solution: channel coding across subcarriers + adaptive modulation

See [[10 - OFDM]] for details.

---

## Error Correction and Coding Gain

Forward Error Correction (FEC) can **dramatically** reduce BER:

| Code | Code Rate | Coding Gain | Notes |
|------|-----------|-------------|-------|
| Convolutional (K=7) | 1/2 | ~5 dB | Classic, used in early WiFi |
| Turbo codes | 1/3 to 1/2 | ~8 dB | 3G/4G cellular |
| LDPC | 1/2 to 5/6 | ~9 dB | WiFi 6, 5G, DVB |
| Polar codes | Various | ~9 dB | 5G control channel |

With coding, a system using 64-QAM + LDPC 3/4 might need only ~15 dB Eb/N0 for BER = 10⁻⁶ instead of 18.5 dB (uncoded).

---

## The BER-Bandwidth-Power Triangle

Every modulation choice involves a three-way trade-off:

```
         BER (Reliability)
            ╱╲
           ╱  ╲
          ╱    ╲
         ╱  You ╲
        ╱  pick  ╲
       ╱   two    ╲
      ╱─────────────╲
  Bandwidth          Power
 (Spectral Eff.)   (Eb/N0)
```

| Strategy | Example | Trade-Off |
|----------|---------|-----------|
| Low BER + Low BW | 256-QAM | Needs high power (SNR) |
| Low BER + Low Power | BPSK | Needs wide bandwidth |
| Low BW + Low Power | Not possible at high data rates | Shannon says no |

---

## Connection Map

- **Foundations**: [[11 - Bandwidth and Spectral Efficiency]] — Shannon limit sets theoretical bound
- **Per-scheme analysis**: [[08 - Phase Shift Keying (PSK)]], [[09 - Quadrature Amplitude Modulation (QAM)]] — individual BER formulas
- **Analog noise**: [[04 - Frequency Modulation (FM)]] — FM noise improvement
- **System design**: [[13 - Real World Systems]] — how noise drives modulation choice
- **Summary**: [[14 - Modulation Comparison Table]]

---

## Exam-Style Questions

1. **What is Eb/N0 and why is it preferred over SNR for comparing modulation schemes?** *(Normalizes by bit rate → fair comparison)*
2. **Calculate the BER of BPSK at Eb/N0 = 10 dB.** *(Q(√20) ≈ Q(4.47) ≈ 3.9×10⁻⁶)*
3. **Why does QPSK have the same BER as BPSK per bit despite sending 2 bits/symbol?** *(QPSK = 2 independent BPSK on I and Q)*
4. **A system needs BER < 10⁻⁵ with 64-QAM. What Eb/N0 is required?** *(≈17 dB uncoded)*
5. **How does FEC improve the BER-SNR trade-off?** *(Adds redundancy → "coding gain" reduces required SNR by 5-9 dB)*
6. **Explain the BER-Bandwidth-Power triangle.** *(Can optimize two at the expense of the third)*

---

> **Next**: Where all these schemes are deployed in practice → [[13 - Real World Systems]]
