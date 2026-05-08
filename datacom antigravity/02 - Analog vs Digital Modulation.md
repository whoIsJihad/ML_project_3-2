# Analog vs Digital Modulation

> **Prerequisites**: [[00 - Why Modulation Exists]], [[01 - Carrier Signals]]
> **Next**: Analog path → [[03 - Amplitude Modulation (AM)]] | Digital path → [[06 - Pulse Amplitude Modulation (PAM)]]

---

## The Branching Point

You know that modulation = varying a carrier's parameters. The fundamental split is:

| | Analog Modulation | Digital Modulation |
|---|---|---|
| **Message signal** | Continuous (voice, music) | Discrete (bits: 0s and 1s) |
| **Carrier variation** | Smooth, continuous | Discrete steps/symbols |
| **Parameter values** | Infinite possibilities | Finite set (constellation points) |
| **Examples** | [[03 - Amplitude Modulation (AM)]], [[04 - Frequency Modulation (FM)]], [[05 - Phase Modulation (PM)]] | [[07 - ASK and FSK]], [[08 - Phase Shift Keying (PSK)]], [[09 - Quadrature Amplitude Modulation (QAM)]] |

---

## Analog: Smooth Variation

In analog modulation, the carrier parameter changes **continuously** and **proportionally** to the message signal.

```
Message:  ~~~∿∿∿~~~      (continuous waveform)
              │
              ▼
Carrier:  ∥∥∥∥∥∥∥∥∥∥      (pure sinusoid)
              │
              ▼ AM: amplitude follows message
AM out:   ╥╥┃┃║║┃┃╥╥      (envelope = message shape)
```

**Advantage**: Simple hardware, natural for voice/audio.  
**Problem**: Any noise added to the signal **permanently corrupts** it. You can't distinguish "was this amplitude change part of the message or noise?"

---

## Digital: Discrete Symbols

In digital modulation, the carrier jumps between a **finite set of states** (called **symbols**). Each symbol represents a group of bits.

```
Bits:    0  1  1  0  1  0  0  1
              │
              ▼
Symbol:  Choose from {state_0, state_1}
              │
              ▼ BPSK: phase = 0° or 180°
BPSK:    ─┐┌─┐┌──┐┌─┐┌──    (phase flips)
```

**Key advantage**: Because the receiver only needs to decide between **finite options**, it can **correct errors**. If the received signal is "close to state_1", the receiver snaps it to state_1 — noise is removed.

> **Analogy**: Analog = writing in cursive (any smudge distorts the message). Digital = printing in block capitals (a smudged 'A' is still recognizable as 'A').

---

## The Bridge: PAM

[[06 - Pulse Amplitude Modulation (PAM)]] sits at the **intersection** of analog and digital:

```
Analog Signal → [Sampler] → [Quantizer] → Digital Signal
                    │             │
                    │             └─ Discrete amplitude levels
                    └─ Nyquist rate: f_s ≥ 2·f_max
```

PAM is the process that **converts analog to digital** — it's the bridge between the two worlds. See [[06 - Pulse Amplitude Modulation (PAM)]] for details.

---

## Why the World Moved to Digital

| Factor | Analog | Digital |
|--------|--------|---------|
| **Noise resilience** | Degrades continuously | Threshold detection → regeneration |
| **Error correction** | Impossible | FEC codes can fix bit errors |
| **Multiplexing** | FDM only | TDM, CDM, OFDM — more flexible |
| **Encryption** | Very difficult | Natural (it's already bits) |
| **Compression** | Limited | Powerful (MP3, H.264, etc.) |
| **Hardware** | Analog circuits (drift, aging) | DSP — precise, programmable |
| **Spectral efficiency** | Fixed | Adaptive (change QAM order based on SNR) |

> **Bottom line**: Digital modulation lets you **trade complexity for performance**. Modern systems (WiFi, LTE, 5G) are 100% digital modulation.

---

## How They Connect

```
           ┌── AM  ──→  ASK (digital AM)
           │
ANALOG ────┼── FM  ──→  FSK (digital FM)
           │
           └── PM  ──→  PSK (digital PM)
                              │
                              ├── QPSK  ──→  QAM (amplitude + phase)
                              │                    │
                              └──────────────────→ OFDM (multi-carrier QAM)
```

Each digital scheme is essentially the **discrete version** of its analog counterpart:
- **ASK** = AM with discrete amplitude levels → [[07 - ASK and FSK]]
- **FSK** = FM with discrete frequency choices → [[07 - ASK and FSK]]  
- **PSK** = PM with discrete phase values → [[08 - Phase Shift Keying (PSK)]]
- **QAM** = Combines ASK + PSK → [[09 - Quadrature Amplitude Modulation (QAM)]]

---

## Connection Map

- Comes from: [[01 - Carrier Signals]] — the three knobs that define modulation
- Analog branch: [[03 - Amplitude Modulation (AM)]] → [[04 - Frequency Modulation (FM)]] → [[05 - Phase Modulation (PM)]]
- Bridge to digital: [[06 - Pulse Amplitude Modulation (PAM)]]
- Digital branch: [[07 - ASK and FSK]] → [[08 - Phase Shift Keying (PSK)]] → [[09 - Quadrature Amplitude Modulation (QAM)]] → [[10 - OFDM]]
- Compare all: [[14 - Modulation Comparison Table]]

---

## Exam-Style Questions

1. **What is the fundamental difference between analog and digital modulation?** *(Continuous vs discrete carrier parameter variation)*
2. **Why does digital modulation have better noise immunity than analog?** *(Threshold detection — receiver snaps to nearest symbol)*
3. **Name the digital counterpart of each analog modulation type.**
4. **What role does PAM play in bridging analog and digital?** *(Sampling + quantization)*

---

> **Choose your path**:
> - Analog deep-dive → [[03 - Amplitude Modulation (AM)]]
> - Jump to digital → [[06 - Pulse Amplitude Modulation (PAM)]]
