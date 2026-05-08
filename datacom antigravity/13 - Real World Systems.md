# Real World Systems

> **Prerequisites**: [[10 - OFDM]], [[09 - Quadrature Amplitude Modulation (QAM)]], [[12 - Noise and BER]]
> **Related**: [[14 - Modulation Comparison Table]], [[15 - How to Analyze Any New Modulation]]

---

## System-Level Thinking

Now that you understand individual modulation techniques, the question becomes: **why does each real-world system choose the modulation it does?**

The answer always comes from the **constraints** of the environment:

```
What modulation?
       │
       ├── Channel characteristics (multipath? fading? noise?)
       ├── Bandwidth available (scarce? abundant?)
       ├── Power budget (battery? plugged in?)
       ├── Cost and complexity (mass market? specialized?)
       ├── Regulatory requirements (emission limits, band allocation)
       └── Target data rate and reliability
```

---

## AM Radio Broadcasting

| Parameter | Value |
|-----------|-------|
| **Band** | 530 – 1700 kHz (MF) |
| **Modulation** | [[03 - Amplitude Modulation (AM)]] (DSB-FC) |
| **Bandwidth** | 10 kHz per channel |
| **Audio quality** | Low (5 kHz audio bandwidth) |
| **Range** | Hundreds of km (ground wave propagation) |

### Why AM?

1. **Receiver simplicity**: An AM radio needs just a diode detector — billions of cheap radios worldwide
2. **Long range**: Medium-frequency ground waves follow Earth's curvature
3. **Legacy**: Established in 1920s, infrastructure exists
4. **Audio quality is acceptable** for talk radio, news

### Why NOT FM for this use case?
FM would need 200 kHz per channel (vs 10 kHz for AM). The MF band is too narrow for FM broadcasting. Also, FM receivers are more complex.

---

## FM Radio Broadcasting

| Parameter | Value |
|-----------|-------|
| **Band** | 88 – 108 MHz (VHF) |
| **Modulation** | [[04 - Frequency Modulation (FM)]] (Wideband, β ≈ 5) |
| **Bandwidth** | 200 kHz per channel |
| **Audio quality** | High (15 kHz audio, stereo) |
| **Range** | ~100 km (line of sight) |

### Why FM?

1. **Noise immunity**: FM's amplitude limiting rejects interference → high-fidelity audio
2. **Sufficient bandwidth at VHF**: 20 MHz total band holds 100 channels at 200 kHz each
3. **Stereo capability**: FM stereo uses a 19 kHz pilot + subcarrier at 38 kHz (possible due to wide BW)
4. **Capture effect**: FM receivers lock onto the strongest signal, rejecting weaker ones (unlike AM where signals add linearly)

### Why NOT AM for music?
AM's amplitude is noise-vulnerable — unacceptable for music quality. AM's 5 kHz audio bandwidth can't carry music well.

---

## WiFi (802.11a/g/n/ac/ax)

| Parameter | 802.11a/g | 802.11n | 802.11ac | 802.11ax (WiFi 6) |
|-----------|-----------|---------|----------|-------------------|
| **Band** | 2.4/5 GHz | 2.4/5 GHz | 5 GHz | 2.4/5/6 GHz |
| **Modulation** | OFDM + up to 64-QAM | OFDM + 64-QAM | OFDM + 256-QAM | OFDMA + 1024-QAM |
| **FFT size** | 64 | 64/128 | 64-512 | 256-2048 |
| **Max data rate** | 54 Mbps | 600 Mbps | 6.9 Gbps | 9.6 Gbps |
| **Bandwidth** | 20 MHz | 20/40 MHz | 20-160 MHz | 20-160 MHz |

### Why OFDM for WiFi?

1. **Indoor multipath**: Walls, furniture, people create reflections → frequency-selective fading
2. **[[10 - OFDM]]** handles this perfectly — narrow subcarriers experience flat fading
3. **Simple equalization**: One complex multiply per subcarrier vs. multi-tap equalizer
4. **Adaptive QAM**: Different QAM order per subcarrier — use 256-QAM on good subcarriers, QPSK on bad ones
5. **WiFi 6 adds OFDMA**: Multiple users served simultaneously on different subcarrier groups

### Why NOT single-carrier QAM?
Indoor channels have delay spreads of 50-200 ns. At 100 Mbps (10 ns symbol), this causes massive ISI. OFDM with 3.2 μs symbols easily absorbs this delay spread.

---

## LTE/4G Cellular

| Parameter | Value |
|-----------|-------|
| **Band** | 700-2600 MHz (various) |
| **Downlink** | OFDMA + up to 256-QAM |
| **Uplink** | SC-FDMA + up to 64-QAM |
| **Subcarrier spacing** | 15 kHz |
| **FFT sizes** | 128–2048 |
| **Bandwidth** | 1.4–20 MHz |
| **Max DL rate** | ~300 Mbps (Cat 10) |

### Why OFDMA downlink?
Same multipath argument as WiFi, plus **multi-user access** — assign subcarriers to different users.

### Why SC-FDMA uplink (not OFDMA)?
Phones are **battery-powered**. OFDM has high PAPR → needs linear amplifier → wastes power. SC-FDMA (DFT-precoded OFDMA) has lower PAPR → more efficient amplification → longer battery life.

### Why adaptive modulation?
- Near tower (high SNR): 256-QAM → maximum throughput
- Cell edge (low SNR): QPSK → maintain connection reliability
- This is done every millisecond based on channel quality reports

---

## 5G NR (New Radio)

| Parameter | Value |
|-----------|-------|
| **Sub-6 GHz** | OFDMA, 15/30/60 kHz spacing |
| **mmWave** (28/39 GHz) | OFDMA, 60/120/240 kHz spacing |
| **Max modulation** | 1024-QAM |
| **Bandwidth** | Up to 400 MHz (mmWave) |
| **Peak rate** | 20 Gbps |

### What's new vs LTE?
- **Flexible numerology**: Different subcarrier spacings for different use cases (low latency vs high throughput)
- **Wider subcarrier spacing** at mmWave to handle Doppler and phase noise at high frequencies
- **Massive MIMO** + OFDM: spatial multiplexing on top of frequency multiplexing
- **1024-QAM**: Possible only at very high SNR (close to base station)

---

## Satellite Communications

| System | Modulation | Why? |
|--------|-----------|------|
| **DVB-S** | QPSK | Long distance → low SNR → need robust modulation |
| **DVB-S2** | QPSK to 32-APSK | Adaptive based on weather/elevation |
| **GPS** | BPSK | Extremely low SNR (signal below noise floor) — use spread spectrum |
| **Starlink** | OFDM + adaptive QAM | High throughput with dynamic channel |

### Why QPSK for satellite?
Free-space path loss at 36,000 km geostationary orbit is enormous (~200 dB). Available SNR is low → need maximum noise immunity → QPSK (same BER as BPSK but 2× throughput).

---

## Quick Reference: System → Modulation Mapping

| System | Modulation | Key Constraint |
|--------|-----------|---------------|
| AM Radio | AM (DSB-FC) | Cheap receivers, legacy |
| FM Radio | Wideband FM | Audio quality, noise immunity |
| WiFi | OFDM + QAM | Indoor multipath |
| LTE/4G DL | OFDMA + QAM | Multipath + multi-user |
| LTE/4G UL | SC-FDMA | Battery life (low PAPR) |
| 5G | OFDMA + QAM | Flexible numerology |
| GPS | BPSK + spreading | Ultra-low SNR |
| Satellite TV | QPSK/APSK | Long distance, low SNR |
| Cable TV | 256-QAM | High SNR cable environment |
| DSL | DMT (OFDM) | Frequency-selective phone line |
| Bluetooth | GFSK | Low power, simple |
| LoRa | CSS (chirp) | Extreme range, low power |
| Ethernet (1G) | PAM-5 | 4 wire pairs, controlled noise |

---

## Connection Map

- **Each system links back to its modulation technique**: [[03 - Amplitude Modulation (AM)]] through [[10 - OFDM]]
- **Trade-off analysis**: [[11 - Bandwidth and Spectral Efficiency]], [[12 - Noise and BER]]
- **Master comparison**: [[14 - Modulation Comparison Table]]
- **Framework for new systems**: [[15 - How to Analyze Any New Modulation]]

---

## Exam-Style Questions

1. **Why does WiFi use OFDM instead of single-carrier QAM?** *(Indoor multipath → frequency-selective fading → OFDM makes each subcarrier flat)*
2. **Why does LTE use SC-FDMA for uplink but OFDMA for downlink?** *(Uplink: phone battery → low PAPR needed; Downlink: base station plugged in → PAPR OK)*
3. **Why is AM radio still used despite its inferior noise performance?** *(Simple receiver, long range, legacy infrastructure, sufficient for voice)*
4. **A satellite link has SNR = 5 dB. Which modulation and why?** *(QPSK or BPSK — need low Eb/N0 requirement; higher-order QAM impossible)*
5. **What drives the choice between 64-QAM and 256-QAM in a cellular system?** *(Current SNR — adaptive modulation selects highest order that maintains target BER)*

---

> **Next**: The master comparison → [[14 - Modulation Comparison Table]]
