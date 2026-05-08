# Topic 2: DSB-SC vs. Conventional AM – The Power vs. Complexity Trade-off

## Introduction: Two Roads to Modulation

Both **DSB-SC (Double Sideband Suppressed Carrier)** and **Conventional AM (Large Carrier)** shift signals to higher frequencies. But they make fundamentally different engineering choices about power efficiency and demodulation complexity.

This section explains the trade-off mathematically and explores why we sometimes waste power on a carrier component.

---

## Part A: DSB-SC (Double Sideband Suppressed Carrier)

### Mathematical Definition

The DSB-SC modulated signal is:

$$s_{\text{DSB-SC}}(t) = m(t) \cos(2\pi f_c t)$$

where:
- $m(t)$ = baseband message signal
- $f_c$ = carrier frequency
- **No additional carrier component**

### Frequency Domain Analysis

Using the modulation theorem:

$$\mathcal{F}[m(t) \cos(2\pi f_c t)] = \frac{1}{2}M(f - f_c) + \frac{1}{2}M(f + f_c)$$

**Spectrum picture:** (DSB‑SC)


![[graphs/11_dsbsc_am_spectrum.png]]

**Key characteristic:** Two symmetric sidebands, **no spectral component at $f_c$** (the carrier is "suppressed").

### Power Analysis (simple explanation)

Start from the transmitted waveform:

$$s_{\text{DSB-SC}}(t) = m(t)\cos(2\pi f_c t).$$

Instantaneous power is the squared signal:

$$P(t)=s^2(t)=m^2(t)\cos^2(2\pi f_c t).$$

Use the identity

$$\cos^2 x = \tfrac{1}{2}[1 + \cos(2x)],$$

so

$$P(t)=\tfrac{1}{2}m^2(t) + \tfrac{1}{2}m^2(t)\cos(4\pi f_c t).$$

When you average over many carrier cycles the second term disappears (the cosine oscillates around zero), leaving

$$\overline{P_{\text{DSB-SC}}}=\tfrac{1}{2}\mathbb{E}[m^2(t)] = \tfrac{1}{2}P_m.$$

Quick numeric example (easiest view): let

- message: $m(t)=A_m\sin(2\pi f_m t)$ so $P_m=\tfrac{A_m^2}{2}$,
- then $\overline{P_{\text{DSB-SC}}}=\tfrac{A_m^2}{4}$.

If $A_m=1$ → $P_m=0.5$ and transmitted DSB‑SC power = 0.25 (all of that is information‑bearing).

Intuition: multiplying by the carrier moves the message to ±f_c and the cos^2 factor has average 1/2 — there is no extra constant carrier term in DSB‑SC, so no extra (wasted) carrier power is transmitted.

Note: this assumes the baseband has no additional constant carrier term (zero mean message), which is the normal case for communications signals.

**Efficiency statement (plain):** DSB‑SC does not add a separate carrier amplitude, so every watt sent derives from the message component (no carrier watts are wasted).

### Beginner explanation (expanded, no math required)
Read this [[gpt_on_dsbsc]]
1. What changes when we modulate?
   - We take the baseband message (the thing you want to send) and "ride" it on a high‑frequency carrier so it can travel over radio links. In DSB‑SC the carrier is only used to move the message — there is **no extra carrier tone** added.

2. Why does the formula show a factor 1/2?
   - Multiplying by the carrier cosine makes the instantaneous power fluctuate. Over many carrier cycles, the cosine factor averages to 1/2. That 1/2 is a mathematical average — it doesn't mean energy disappeared; it means the transmitted waveform's time‑average equals half the baseband mean‑square value.

3. Is power wasted in DSB‑SC?
   - **No.** The power that is transmitted in DSB‑SC all comes from the message (i.e. information‑bearing). The 1/2 factor only describes how the message power appears after modulation, not a wasteful extra carrier.

4. What does "carrier suppressed" mean in plain words?
   - In the frequency plot you would **not** see a tall spike at f_c. You only see the sidebands (the message copies at ±f_c). That absence of a spike is "carrier suppressed." The receiver must regenerate a carrier (synchronize) to demodulate.

5. Quick real‑world analogy
   - Think of AM as playing music loudly while also turning on a bright porch light (the carrier). The light wastes power but doesn't carry the song. DSB‑SC is like sending only the music — no extra light wasting energy — but the receiver needs a way to "turn its own light on" at the right time to hear the music.

6. Concrete numeric walkthrough (one readable example)
   - Let message amplitude A_m = 1 → baseband power P_m = A_m^2/2 = 0.5.
   - DSB‑SC transmitted average power = 0.5·P_m = 0.25 (this 0.25 W is all useful message power).
   - AM with carrier A = 1: carrier power = A^2/2 = 0.5, sidebands = 0.25 → total = 0.75, only 0.25/0.75 ≈ 33% useful.

If you want, I can add a short annotated diagram or a tiny interactive table next to this note so you can try other numbers easily.
### Quick numeric comparison (copy‑friendly)

| Case | Message power $P_m$ | Transmitted power | Useful (message) % |
|---|---:|---:|---:|
| **DSB‑SC** (A_m = 1) | $0.5$ | $0.25$ | **100%** |
| **AM** (A = 1, 100% mod) | $0.5$ | $0.75$ | **33.3%** |
| **AM** (A = 10) | $0.5$ | $50.25$ | **0.5%** |

*(Explanation: for AM the carrier contributes $P_c = A^2/2$, sidebands contribute $P_s = \tfrac{1}{2}P_m$; useful fraction = $P_s/(P_c+P_s)$.)*

### Quick Python check (paste into a REPL)

```python
Am = 1.0          # message amplitude (example)
Pm = Am**2 / 2
P_dsbsc = 0.5 * Pm
print('DSB-SC P_tx =', P_dsbsc)
# AM example
A = 1.0
Pc = A**2 / 2
Ps = 0.5 * Pm
print('AM P_tx =', Pc + Ps, 'useful pct =', 100*Ps/(Pc+Ps))
```

![[graphs/02_power_efficiency.png]]

---

## Part B: Conventional AM (Large Carrier)

### Mathematical Definition

Conventional AM includes an additional **unmodulated carrier**:

$$s_{\text{AM}}(t) = [A + m(t)] \cos(2\pi f_c t)$$

where:
- $A$ = **carrier amplitude** (constant)
- $m(t)$ = message (assumed $|m(t)| \leq A$)
- The entire term $[A + m(t)]$ is the **envelope**

### Frequency Domain Analysis

Expanding:

$$s_{\text{AM}}(t) = A \cos(2\pi f_c t) + m(t) \cos(2\pi f_c t)$$

The spectrum contains:
1. **Carrier component:** A delta function at $f = \pm f_c$ with magnitude $\frac{A}{2}$
2. **Sidebands:** Same as DSB-SC, with magnitude $\frac{1}{2}M(f \pm f_c)$

![[graphs/11_dsbsc_am_spectrum.png]]
**Spectrum picture:** 

**Key characteristic:** Large spectral component **exactly at $f_c$** that carries **zero information** about the message.

### Power Analysis

The AM signal power can be decomposed:

$$s_{\text{AM}}(t) = A\cos(2\pi f_c t) + m(t)\cos(2\pi f_c t)$$

**Carrier power:**
$$P_c = \frac{A^2}{2}$$

**Sideband power (message):**
$$P_s = \frac{1}{2}P_m$$

**Total power:**
$$P_{\text{AM}} = P_c + P_s = \frac{A^2}{2} + \frac{1}{2}P_m$$

**Efficiency of AM:**
$$\eta = \frac{P_s}{P_{\text{AM}}} = \frac{\frac{1}{2}P_m}{\frac{A^2}{2} + \frac{1}{2}P_m} = \frac{P_m}{A^2 + P_m}$$

If $A \gg \sqrt{P_m}$, then $\eta \ll 1$ (most power wasted on carrier!).

**Example:** If $A = 10\sqrt{P_m}$, then:
$$\eta = \frac{P_m}{100P_m + P_m} \approx 1\%$$

**99% of the power goes to the carrier—only 1% carries the message.**

---

## Part C: Why Add a Carrier? The Demodulation Question

### DSB-SC Demodulation: Coherent Detection (Synchronous)
Read this [[demodulation_gpt]]
To recover $m(t)$ from DSB-SC, we must **multiply by a replica of the carrier** (coherent with the original):

$$r(t) = 2s_{\text{DSB-SC}}(t) \cos(2\pi f_c t) = 2m(t) \cos^2(2\pi f_c t)$$

Using the identity $\cos^2(x) = \frac{1}{2}(1 + \cos(2x))$:

$$r(t) = m(t) [1 + \cos(4\pi f_c t)]$$

After low-pass filtering (removing the $\cos(4\pi f_c t)$ term at $2f_c$):

$$m_{\text{recovered}}(t) = m(t)$$

**Requirement:** The local oscillator must be **exactly synchronized** in **phase and frequency** with the original carrier. This is demanding!

### Conventional AM Demodulation: Envelope Detection (Asynchronous)

With the carrier present, we can use a simple **diode envelope detector**:

1. Pass the AM signal through a diode (rectifier)
2. Low-pass filter to extract the envelope

See the [demodulation comparison visualization](graphs/10_demodulation_comparison.png) for how these methods compare.

The envelope of $[A + m(t)] \cos(2\pi f_c t)$ is **exactly** $A + m(t)$.

Filtering removes the carrier oscillations, leaving:

$$m_{\text{recovered}}(t) \approx A + m(t)$$

DC-blocking capacitor removes the $A$ offset, yielding $m(t)$.

**Requirement:** **No phase synchronization needed!** The demodulator is passive and simple.

---

## Part D: The Trade-off Summarized

| Aspect | DSB-SC | Conventional AM |
|--------|--------|-----------------|
| **Signal** | $m(t) \cos(2\pi f_c t)$ | $[A + m(t)] \cos(2\pi f_c t)$ |
| **Bandwidth** | $2B$ | $2B$ |
| **Demodulation** | Coherent (sync required) | Envelope (no sync) |
| **Carrier Power** | 0% | $\frac{A^2/2}{P_{\text{total}}} \times 100\%$ |
| **Efficiency** | 100% (all power = message) | Up to ~33% (best case) |
| **Receiver Complexity** | High (needs PLL/sync) | Low (diode rectifier) |
| **Real-world use** | Professional broadcast, SSB | AM radio, budget receivers |

---

## Part E: Mathematical Proof of Power Efficiency

### Modulation Index ($\mu$) in Conventional AM

The **modulation index** quantifies the message strength relative to the carrier:

$$\mu = \frac{A_m}{A}$$

where $A_m = \max|m(t)|$ is the peak message amplitude.

The condition for **no over-modulation** (envelope stays positive):
$$A + m(t) > 0 \quad \forall t$$

This requires:
$$m_{\min}(t) > -A \quad \Rightarrow \quad \mu \leq 1$$

**Maximum efficiency** occurs at $\mu = 1$ (100% modulation, just avoiding over-modulation).

### Efficiency for Sinusoidal Message

Let $m(t) = A_m \sin(2\pi f_m t)$ with $\mu = \frac{A_m}{A}$.

**Message power:**
$$P_m = \frac{A_m^2}{2} = \frac{\mu^2 A^2}{2}$$

**Total AM power:**
$$P_{\text{AM}} = \frac{A^2}{2} + \frac{\mu^2 A^2}{4} = \frac{A^2}{2}\left(1 + \frac{\mu^2}{2}\right)$$

**Efficiency:**
$$\eta = \frac{\mu^2/2}{1 + \mu^2/2} = \frac{\mu^2}{2 + \mu^2}$$

For $\mu = 1$ (maximum modulation):
$$\eta_{\max} = \frac{1}{3} \approx 33\%$$

**Even at best conditions, conventional AM wastes 67% of power on the carrier!**

---

## Part F: The Coherent vs. Envelope Detector Deep Dive

### Synchronous (Coherent) Detection Block Diagram

```
Received Signal  ×  Local Oscillator      LPF
   s(t)        ×   2cos(2πf_c t)   →   ─────  →  m(t)
                                        Filter
                 
Requires: Phase/frequency lock!
```

**Math:**
$$y(t) = 2s(t) \cos(2\pi f_c t + \phi) = m(t)[1 + \cos(4\pi f_c t + 2\phi)]$$

If $\phi \neq 0$ (phase error), the message is multiplied by $\cos(2\phi)$:
- $\phi = 0°$: Full signal recovery
- $\phi = 45°$: Signal reduced by $\cos(45°) = 0.707$ (3 dB loss)
- $\phi = 90°$: $\cos(90°) = 0$ (signal vanishes completely!)

### Envelope Detector Block Diagram

```
Received Signal     Diode       RC Circuit
   s(t)        →  (Rectifier)  →  (LPF)  →  m(t)
   
No phase reference required!
```

**Why it works:** The envelope of $[A + m(t)] \cos(2\pi f_c t)$ is $|A + m(t)|$, which naturally extracts the message shape.

**Limitation:** The receiver must handle the constant $A$ (DC offset), and the diode introduces non-linearity (slightly distorting signals with large modulation index).

---

## Part G: When Each Is Used

### DSB-SC Applications
- **SSB/USZ with pilot carrier:** Professional single-sideband radio
- **Satellite communication:** Power efficiency is critical
- **Stereo FM:** Uses DSB-SC for the 19 kHz pilot tone and stereo difference signal
- **QAM:** All modern digital communications (WiFi, LTE, 5G)

**Reason:** Power efficiency and bandwidth efficiency are paramount.

### Conventional AM Applications
- **AM radio broadcasting:** Receivers are cheap and passive
- **Older television:** Used AM for video (visual carrier)
- **Emergency beacons:** Simplicity and reliability matter more than efficiency

**Reason:** Ease of receiver implementation for non-technical users.

---

## Part H: Common Pitfalls (Exam Critical!)

### ⚠️ Pitfall 1: Confusing Bandwidth

**Wrong:** "Conventional AM uses half the bandwidth of DSB-SC"
**Correct:** Both use exactly $2B$ bandwidth (one sideband above and one below $f_c$).

The difference is in **information carrier**: DSB-SC puts all info in sidebands; AM wastes power on the carrier.

### ⚠️ Pitfall 2: Forgetting the Factor of 2 in Recovery

When recovering DSB-SC via coherent detection:
$$r(t) = 2s_{\text{DSB-SC}}(t) \cos(2\pi f_c t) = 2m(t) \cos^2(2\pi f_c t)$$

The **2** multiplier is necessary to recover the full amplitude. Forgetting this leads to incorrect signal recovery.

### ⚠️ Pitfall 3: Assuming Envelope Detection Always Works

Envelope detection **only works** if $A + m(t) > 0$ always (no over-modulation). For signals with $\mu > 1$, the envelope detector produces **distortion** (the signal peaks get clipped by the zero crossings).

### ⚠️ Pitfall 4: Phase Error in Coherent Detection

Many students forget that coherent detection **requires perfect phase alignment**. A phase error $\phi$ reduces the recovered signal by $\cos(2\phi)$.

At $\phi = 90°$, the signal vanishes entirely—this is sometimes called the "**phase ambiguity problem**" or "**quadrature null**."

---

## Part I: Efficiency Comparison with Numerical Example

### Setup
- Message: $m(t) = A_m \sin(2\pi \times 1000 \cdot t)$ (1 kHz tone)
- Carrier: $f_c = 100$ kHz
- Assume $A = A_m$ (100% modulation in AM case)

### Power Calculations

**DSB-SC:**
$$P_{\text{DSB-SC}} = \frac{1}{2}P_m = \frac{1}{2} \cdot \frac{A_m^2}{2} = \frac{A_m^2}{4}$$

All power carries message information. ✓

**Conventional AM (100% modulation, $A = A_m$):**
$$P_c = \frac{A_m^2}{2} \quad \text{(carrier)}$$
$$P_s = \frac{1}{2}P_m = \frac{A_m^2}{4} \quad \text{(sidebands)}$$
$$P_{\text{AM}} = \frac{A_m^2}{2} + \frac{A_m^2}{4} = \frac{3A_m^2}{4}$$

Efficiency:
$$\eta = \frac{A_m^2/4}{3A_m^2/4} = 33.3\%$$

**If we want the same power radiated:**
- DSB-SC needs: $\sqrt{1}$ units of transmitter power
- AM needs: $\sqrt{3} \approx 1.73$ units of transmitter power

**DSB-SC is 73% more power-efficient.**

---

## Part J: Summary Table – Head-to-Head Comparison

| Parameter | DSB-SC | Conventional AM |
|-----------|--------|-----------------|
| **Signal equation** | $m(t)\cos(2\pi f_c t)$ | $[A+m(t)]\cos(2\pi f_c t)$ |
| **Occupied bandwidth** | $2B$ | $2B$ |
| **Power efficiency** | 100% | ≤ 33% |
| **Demodulation type** | Coherent (sync) | Envelope (passive) |
| **Receiver complexity** | Medium–High | Very Low |
| **Receiver cost** | Moderate | Cheap |
| **Phase sync required** | Yes | No |
| **Performance (SNR)** | Better | Worse (noise in carrier) |
| **Real-world ease** | Professional | Consumer |

---

## Conclusion

The DSB-SC vs. Conventional AM trade-off encapsulates a fundamental engineering principle:

**Performance vs. Simplicity**

- **DSB-SC:** All power goes to the message; requires precise synchronization; used where efficiency matters (satellites, digital communications, professional radio).
- **Conventional AM:** Simple receiver (diode detector); wastes power on unmodulated carrier; used where cost and simplicity matter (broadcast radio for non-technical users).

The reason for the carrier in AM is simple: **it enables envelope detection**, which requires no phase reference. This simplicity comes at a severe power cost.

In modern communications, DSB-SC and its descendants (SSB, QAM) dominate because power and spectrum efficiency are critical.

---

## Next Steps
- Understanding **Quadrature Modulation (QAM)** and **orthogonality**
- Exploring **Single Sideband (SSB)** and the Hilbert Transform
- Studying **Phase Locked Loops (PLL)** to achieve coherent sync automatically
