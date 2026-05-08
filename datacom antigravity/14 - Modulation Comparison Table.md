# Modulation Comparison Table

> **Prerequisites**: All previous notes
> **Related**: [[11 - Bandwidth and Spectral Efficiency]], [[12 - Noise and BER]], [[13 - Real World Systems]]

---

## Master Comparison

This is your **single-page reference** for comparing all modulation schemes side by side.

---

## Analog Modulation Comparison

| Property | [[03 - Amplitude Modulation (AM)\|AM (DSB-FC)]] | AM (SSB) | [[04 - Frequency Modulation (FM)\|FM]] | [[05 - Phase Modulation (PM)\|PM]] |
|----------|---------|---------|------|------|
| **Parameter varied** | Amplitude | Amplitude | Frequency | Phase |
| **Bandwidth** | $2f_m$ | $f_m$ | $2(\Delta f + f_m)$ | $2(\Delta\phi f_m + f_m)$ |
| **Spectral efficiency** | Low | Moderate | Very low | Very low |
| **Noise immunity** | ★☆☆☆ | ★☆☆☆ | ★★★★ | ★★★☆ |
| **Power efficiency** | ★★☆☆ (33% max) | ★★★☆ | ★★★☆ | ★★★☆ |
| **Receiver complexity** | Envelope detector | Coherent needed | Discriminator/PLL | Phase comparator |
| **Constant envelope?** | ❌ | ❌ | ✅ | ✅ |
| **Primary use** | AM radio, aircraft | Military, ham radio | FM radio, audio | Indirect FM gen. |

---

## Digital Modulation Comparison

| Property | [[07 - ASK and FSK\|ASK (OOK)]] | [[07 - ASK and FSK\|BFSK]] | [[08 - Phase Shift Keying (PSK)\|BPSK]] | [[08 - Phase Shift Keying (PSK)\|QPSK]] | [[08 - Phase Shift Keying (PSK)\|8-PSK]] | [[09 - Quadrature Amplitude Modulation (QAM)\|16-QAM]] | [[09 - Quadrature Amplitude Modulation (QAM)\|64-QAM]] | [[09 - Quadrature Amplitude Modulation (QAM)\|256-QAM]] |
|----------|----------|------|------|------|-------|--------|--------|---------|
| **Bits/symbol** | 1 | 1 | 1 | 2 | 3 | 4 | 6 | 8 |
| **η (bits/s/Hz)** | 1 | <1 | 1 | 2 | 3 | 4 | 6 | 8 |
| **Eb/N0 @ BER=10⁻⁶** | ~14 dB | ~13 dB | 10.5 dB | 10.5 dB | 14 dB | 14.5 dB | 18.5 dB | 22.5 dB |
| **Noise immunity** | ★☆ | ★★★ | ★★★★ | ★★★★ | ★★★ | ★★★ | ★★ | ★ |
| **Constant envelope** | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Complexity** | ★ | ★★ | ★★★ | ★★★ | ★★★ | ★★★★ | ★★★★ | ★★★★★ |

---

## Multi-Carrier Comparison

| Property | Single-carrier QAM | [[10 - OFDM]] | OFDMA | SC-FDMA |
|----------|-------------------|------|-------|---------|
| **Multipath resilience** | ★☆ (needs equalizer) | ★★★★ | ★★★★ | ★★★★ |
| **PAPR** | Low | **High** | **High** | Low |
| **Equalization** | Complex (multi-tap) | Simple (1-tap/subcarrier) | Simple | Simple |
| **Multi-user** | TDM only | No (single user) | **Yes** | **Yes** |
| **Used in** | Cable, microwave | WiFi (early) | LTE DL, WiFi 6 | LTE UL |

---

## The Big Picture: When to Use What

| Scenario | Best Choice | Why |
|----------|-------------|-----|
| **Extremely low SNR** (space, GPS) | BPSK + spread spectrum | Max noise immunity |
| **Low SNR, need throughput** (satellite) | QPSK | 2× BPSK throughput, same BER |
| **Moderate SNR, spectrum scarce** (cable) | 256-QAM | High spectral efficiency |
| **High SNR, multipath** (indoor WiFi) | OFDM + adaptive QAM | Handles multipath, maximizes rate |
| **Battery-powered uplink** (phone) | SC-FDMA + QPSK/16-QAM | Low PAPR saves battery |
| **Simple, cheap receiver** (RFID, remote) | OOK (ASK) | Single diode detector |
| **Low-power, long range** (IoT, LoRa) | Chirp/FSK | Non-coherent, low complexity |
| **Broadcast audio** (FM) | Wideband FM | Noise immunity, capture effect |
| **Broadcast audio** (AM) | DSB-FC AM | Cheap receiver, long range |

---

## Evolution Tree: From Simple to Complex

```
1920s  AM Radio ──────────────────────────────────────── Still used
                 ↓
1930s  FM Radio ──────────────────────────────────────── Still used
                 ↓
1960s  BPSK/QPSK (satellite) ────────────────────────── GPS, DVB-S
                 ↓
1980s  QAM (modems, cable) ──────────────────────────── Cable TV
                 ↓
1990s  OFDM (DAB, DSL) ─────────────────────────────── DSL
                 ↓
2000s  OFDM + adaptive QAM (WiFi, WiMAX) ───────────── WiFi 4/5
                 ↓
2010s  OFDMA + MIMO + 256-QAM (LTE) ────────────────── 4G
                 ↓
2020s  OFDMA + massive MIMO + 1024-QAM (5G NR) ─────── 5G
                 ↓
Future  ? (Intelligent reflecting surfaces, THz, ...)
```

---

## Connection Map

- Every row links to its detailed note: [[03 - Amplitude Modulation (AM)]] through [[10 - OFDM]]
- Mathematical backing: [[11 - Bandwidth and Spectral Efficiency]], [[12 - Noise and BER]]
- System context: [[13 - Real World Systems]]
- Analysis framework: [[15 - How to Analyze Any New Modulation]]

---

## Exam-Style Questions

1. **Compare QPSK and 16-QAM in terms of spectral efficiency, required SNR, and typical applications.**
2. **Why does the spectral efficiency of M-QAM grow only logarithmically with M while the SNR requirement grows roughly linearly?** *(η = log₂M, but SNR ∝ M — exponentially more power per linear bit)*
3. **A designer must choose between 64-QAM single-carrier and OFDM with 16-QAM. What factors decide?** *(Multipath: if significant → OFDM. If flat channel → single-carrier is simpler)*
4. **Rank the following in order of noise immunity: AM, FM, BPSK, 64-QAM, OOK.** *(BPSK > FM > 64-QAM > AM > OOK)*

---

> **Final note**: How to approach any modulation you've never seen → [[15 - How to Analyze Any New Modulation]]
