# Shannon's Channel Capacity Theorem

> **Prerequisites**: [[18 - Channel Capacity]], [[16 - Information Content and Entropy]]
> **Course**: CSE 311 — Data Communication (Md Asib Rahman)

---

## From Discrete to Continuous

The BSC in [[18 - Channel Capacity]] models a digital channel where individual bits flip with some probability. But real communication channels operate with **continuous signals** — voltage waveforms corrupted by continuous noise.

We now extend information theory to the continuous domain, culminating in Shannon's most famous result.

---

## Differential Entropy

### The Problem with Continuous Sources

For a discrete source with $n$ outcomes, entropy is well-defined and finite. For a continuous random variable $x$ with probability density function $p(x)$, we define the **differential entropy** by analogy.

> [!note] Differential Entropy
> For a continuous random variable $x$ with PDF $p(x)$:
> $$h(x) = -\int_{-\infty}^{\infty} p(x) \log_2 p(x) \, dx \quad \text{(bits)}$$

We use lowercase $h$ to distinguish from discrete entropy $H$.

> [!warning] Subtlety
> Differential entropy can be **negative** (unlike discrete entropy). It is not the "absolute" uncertainty of a continuous variable — it is a relative measure. The mutual information, however, is always non-negative.

### Key Result: Gaussian Has Maximum Entropy

Among all continuous distributions with the same **variance** $\sigma^2$, the **Gaussian distribution** has the highest differential entropy:

$$h_{\text{max}} = \frac{1}{2} \log_2(2\pi e \sigma^2) \quad \text{(bits)}$$

This is why Gaussian noise is the "worst-case" noise — it creates maximum uncertainty for a given power.

---

## Continuous Memoryless Channel

### Model

![Continuous Additive White Gaussian Noise (AWGN) Channel](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/continuous_channel_model.png)

- **Input signal** $x$ with average power $S$
- **Additive noise** $n$ with average power $N$, independent of $x$
- **Output** $y = x + n$ with power $S + N$

### Mutual Information for Continuous Channels

> [!note] Continuous Mutual Information
> $$I(x; y) = h(y) - h(y|x)$$

Since $y = x + n$ and $x, n$ are independent:
$$h(y|x) = h(n) \quad \text{(knowing } x \text{, the uncertainty in } y \text{ is just the noise)}$$

Therefore:
$$I(x; y) = h(y) - h(n)$$

### Computing $h(n)$

The noise $n$ is Gaussian with power (variance) $N$:
$$h(n) = \frac{1}{2} \log_2(2\pi e N)$$

### Maximizing $h(y)$

The output $y = x + n$ has power $S + N$. Among all distributions with this variance, the Gaussian maximizes entropy. So:
$$h_{\max}(y) = \frac{1}{2} \log_2[2\pi e(S + N)]$$

This maximum is achieved when $x$ itself is Gaussian (sum of two independent Gaussians is Gaussian).

### Channel Capacity per Symbol

> [!important] Continuous Channel Capacity
> $$C_s = \max I(x; y) = h_{\max}(y) - h(n)$$
> $$= \frac{1}{2} \log_2[2\pi e(S+N)] - \frac{1}{2} \log_2(2\pi eN)$$
> $$= \frac{1}{2} \log_2 \frac{S+N}{N}$$
> $$\boxed{C_s = \frac{1}{2} \log_2\left(1 + \frac{S}{N}\right) \quad \text{bits per channel use}}$$

The $2\pi e$ factors **cancel perfectly**, leaving this elegant result that depends only on the signal-to-noise ratio $S/N$.

---

## Band-Limited AWGN Channel: The Shannon Limit

### Adding Bandwidth

A real channel has finite **bandwidth** $B$ Hz. By the **Nyquist sampling theorem**, a band-limited channel can transmit at most $2B$ independent samples per second.

> [!note] Nyquist Rate
> A channel of bandwidth $B$ Hz can carry at most $2B$ independent symbols per second.

### Shannon's Channel Capacity Theorem

Combining the capacity per symbol with the sampling rate:

$$C = 2B \times C_s = 2B \times \frac{1}{2} \log_2\left(1 + \frac{S}{N}\right)$$

> [!important] Shannon-Hartley Theorem
> $$\boxed{C = B \log_2\left(1 + \frac{S}{N}\right) \quad \text{bits/second}}$$
>
> where:
> - $C$ = channel capacity (bits/second)
> - $B$ = channel bandwidth (Hz)
> - $S/N$ = signal-to-noise **power** ratio (linear, not dB)

**This is arguably the most important equation in all of communication engineering.**

### What It Tells You

1. **It's an upper bound**: No coding scheme, no modulation technique, no clever engineering can *ever* exceed $C$ bits/sec reliably. Period.

2. **It's achievable**: Shannon proved that codes *exist* that get arbitrarily close to $C$ (though he didn't say how to build them — that took decades).

3. **Two knobs**: You can increase capacity by increasing bandwidth OR by increasing SNR.

### The Bandwidth-SNR Tradeoff

| Change | Effect on Capacity |
|--------|--------------------|
| Double bandwidth $B$ | Approximately **doubles** $C$ (linear) |
| Double SNR $S/N$ | Increases $C$ by about $B$ bits/sec (logarithmic) |

Bandwidth is "more valuable" than SNR for increasing capacity. Doubling bandwidth doubles capacity; doubling SNR only adds a constant.

### Worked Example

> A telephone line has bandwidth $B = 3.4$ kHz and $S/N = 30$ dB.

**Step 1:** Convert SNR from dB to linear:
$$S/N = 10^{30/10} = 10^3 = 1000$$

**Step 2:** Apply Shannon's formula:
$$C = 3400 \times \log_2(1 + 1000) = 3400 \times \log_2(1001)$$
$$= 3400 \times 9.97 = 33{,}898 \text{ bits/sec} \approx 33.9 \text{ kbps}$$

> [!tip] Reality Check
> Early telephone modems maxed out around 33.6 kbps (V.34 standard) — remarkably close to the Shannon limit! This shows how well engineers optimized these systems.

### Another Example

> $B = 1$ MHz, $S/N = 10$ dB (linear ratio = 10):

$$C = 10^6 \times \log_2(1 + 10) = 10^6 \times \log_2(11) = 10^6 \times 3.459 = 3.46 \text{ Mbps}$$

---

## The Infinite Bandwidth Limit

### The Question

Bandwidth increases capacity linearly. So what if we had **infinite bandwidth**? Would capacity be infinite?

### The Analysis

As bandwidth increases, so does the noise power (noise is spread across the entire band). If the noise has a constant **power spectral density** $N_0/2$, then total noise power is:

$$N = N_0 \cdot B$$

Substituting into Shannon's formula:

$$C = B \log_2\left(1 + \frac{S}{N_0 B}\right)$$

As $B \to \infty$, the term $S/(N_0 B) \to 0$. Using the limit identity:

$$\lim_{x \to 0} \frac{\log_2(1+x)}{x} = \log_2 e = 1.4427$$

We get:

$$\lim_{B \to \infty} C = \lim_{B \to \infty} B \cdot \frac{S}{N_0 B} \cdot \frac{\log_2(1 + S/(N_0 B))}{S/(N_0 B)}$$

$$= \frac{S}{N_0} \cdot \log_2 e$$

> [!important] Infinite Bandwidth Capacity
> $$\boxed{C_\infty = \frac{S}{N_0} \log_2 e = 1.44 \frac{S}{N_0} \quad \text{bits/second}}$$

### What This Means

> [!caution] Bandwidth Is Not Everything
> Even with **unlimited bandwidth**, the capacity is **finite** and depends only on the ratio of signal power to noise spectral density $S/N_0$.

**Physical intuition**: As you spread your signal over more bandwidth, each symbol has less energy. Eventually, the energy per symbol is so low that you can barely distinguish signal from noise. More bandwidth gives diminishing returns and ultimately reaches a hard ceiling.

![Capacity vs. Bandwidth (AWGN Channel)](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/infinite_bandwidth_capacity.png)

The capacity curve flattens out — pouring more bandwidth in gives less and less additional capacity.

---

## Summary: The Complete Information Theory Pipeline

![The Complete Information Theory Pipeline](file:///mnt/Data/3-2/datacom%20antigravity/diagrams/information_theory_pipeline.png)

> [!note] The Coding Paradox
> Source coding **removes** redundancy (compression to $H(m)$), then channel coding **adds** redundancy back (for error correction, bounded by $C_s$). But it's *different* redundancy — structured, mathematically optimal redundancy designed to fight noise.

The beautiful irony: source coding **removes** redundancy, then channel coding **adds** redundancy back. But it's *different* redundancy — structured, mathematically optimal redundancy designed for error correction.

---

## Master Formula Reference

| Concept | Formula | Units |
|---------|---------|-------|
| Information Content | $I = \log_2(1/P) = -\log_2 P$ | bits |
| Entropy (discrete) | $H = -\sum P_i \log_2 P_i$ | bits/message |
| Code Efficiency | $\eta = H/L$ | dimensionless |
| Redundancy | $\gamma = 1 - \eta$ | dimensionless |
| Mutual Information | $I(x;y) = H(x) - H(x\|y)$ | bits/symbol |
| Channel Capacity | $C_s = \max_{P(x)} I(x;y)$ | bits/symbol |
| BSC Capacity | $C_s = 1 - H(P_e)$ | bits/symbol |
| Gaussian Channel | $C_s = \frac{1}{2}\log_2(1 + S/N)$ | bits/symbol |
| **Shannon-Hartley** | $C = B\log_2(1 + S/N)$ | **bits/second** |
| Infinite Bandwidth | $C_\infty = 1.44 \cdot S/N_0$ | bits/second |

---

## Exam-Style Questions

1. **A channel has $B = 4$ kHz and $S/N = 255$ (linear). Find the capacity.**
   $$C = 4000 \times \log_2(256) = 4000 \times 8 = 32{,}000 \text{ bps} = 32 \text{ kbps}$$

2. **Why is the Gaussian distribution the worst-case noise?**
   *(Answer: Among all distributions with the same power, Gaussian maximizes entropy $h(n)$, which maximizes $H(y|x)$, which minimizes $I(x;y)$ and therefore minimizes capacity.)*

3. **A system needs to transmit 10 Mbps. Channel bandwidth is 2 MHz. What minimum SNR is required?**
   $$10 \times 10^6 = 2 \times 10^6 \times \log_2(1 + S/N)$$
   $$\log_2(1 + S/N) = 5 \implies S/N = 2^5 - 1 = 31 \implies \text{SNR} = 10\log_{10}(31) = 14.9 \text{ dB}$$

4. **Explain intuitively why infinite bandwidth gives finite capacity.**
   *(Answer: More bandwidth means more noise power. Each additional Hz of bandwidth adds noise, and the signal power is fixed. Eventually, the signal is drowned in noise across the wider band.)*

5. **In the BSC, why does $P_e = 1$ give the same capacity as $P_e = 0$?**
   *(Answer: A channel that always inverts is deterministic — just flip the output. The worst case is $P_e = 0.5$ where the output is random.)*

---

> **Connection**: These capacity limits define what's theoretically possible. Real systems use [[09 - Quadrature Amplitude Modulation (QAM)]] and [[10 - OFDM]] to approach these limits in practice.

---

> **Next**: To actually achieve these capacity limits, we must add structured redundancy → [[26 - Block Code Basics and Foundation]]
