# Sampling Theorem and Signal Reconstruction

## 1. Introduction and Statement

The Sampling Theorem establishes the bridge between continuous-time signals and discrete-time signals. It provides the mathematical condition under which a continuous signal can be converted into a discrete sequence and subsequently reconstructed without any loss of information.

### The Theorem

A continuous-time signal $g(t)$ is considered **band-limited** if its frequency spectrum $G(f)$ contains no energy above a certain frequency $B$.

$$G(f) = 0 \quad \text{for } |f| > B$$

Such a signal is completely determined by its samples $g(k T_s)$ taken at uniform intervals $T_s$, provided that the sampling rate $f_s$ (or $R$) satisfies the condition:

$$f_s \ge 2B$$

_(Note: Strictly speaking,_ $f_s > 2B$ _is safer to avoid ambiguity at the boundary, but_ $f_s = 2B$ _is the theoretical minimum limit)._

### Key Definitions

- **Nyquist Rate:** The minimum permissible sampling rate, $2B$.
    
- **Nyquist Interval:** The maximum permissible time interval between samples, $T_s = \frac{1}{2B}$.
    
- **Under-sampling:** When $f_s < 2B$, leading to aliasing.
    
- **Over-sampling:** When $f_s > 2B$, creating guard bands between spectral copies.
    

## 2. Mathematical Modeling of Sampling

### Time Domain Representation

Sampling is mathematically modeled as the **multiplication** of the continuous signal $g(t)$ by a periodic impulse train (also called a Dirac comb), denoted as $\delta_{T_s}(t)$.

Let the sampled signal be $\bar{g}(t)$:

$$\bar{g}(t) = g(t) \cdot \delta_{T_s}(t)$$

The periodic impulse train is defined as:

$$\delta_{T_s}(t) = \sum_{n=-\infty}^{\infty} \delta(t - n T_s)$$

Substituting this into the product:

$$\bar{g}(t) = g(t) \sum_{n=-\infty}^{\infty} \delta(t - n T_s)$$

Using the sifting property of the impulse function ($x(t)\delta(t-t_0) = x(t_0)\delta(t-t_0)$), we obtain the discrete representation:

$$\bar{g}(t) = \sum_{n=-\infty}^{\infty} g(n T_s) \delta(t - n T_s)$$

> **Physical Interpretation:** The sampled signal $\bar{g}(t)$ is a sequence of weighted impulses, where the "weight" (area) of each impulse corresponds to the amplitude of the signal $g(t)$ at that instant.

## 3. Spectral Analysis (Frequency Domain)

To understand _why_ the condition $f_s \ge 2B$ exists, we must derive the spectrum of the sampled signal $\bar{g}(t)$.

### Step 1: Fourier Series of the Impulse Train

Since $\delta_{T_s}(t)$ is periodic with period $T_s$, it can be expanded into a Fourier Series:

$$\delta_{T_s}(t) = \sum_{n=-\infty}^{\infty} c_n e^{j n \omega_s t}$$

where $\omega_s = \frac{2\pi}{T_s} = 2\pi f_s$.

The Fourier coefficients $c_n$ are calculated as:

$$c_n = \frac{1}{T_s} \int_{-T_s/2}^{T_s/2} \delta(t) e^{-j n \omega_s t} dt$$

Since the integral of a delta function is 1:

$$c_n = \frac{1}{T_s}$$

Thus, the impulse train can be rewritten as:

$$\delta_{T_s}(t) = \frac{1}{T_s} \sum_{n=-\infty}^{\infty} e^{j n \omega_s t}$$

### Step 2: Deriving $\bar{G}(f)$

Substitute the Fourier Series form back into the sampling equation $\bar{g}(t) = g(t) \delta_{T_s}(t)$:

$$\bar{g}(t) = g(t) \left[ \frac{1}{T_s} \sum_{n=-\infty}^{\infty} e^{j n \omega_s t} \right]$$$$\bar{g}(t) = \frac{1}{T_s} \sum_{n=-\infty}^{\infty} g(t) e^{j n \omega_s t}$$

Now, take the **Fourier Transform** of both sides. We utilize the **Frequency Shifting Property**:

$$\text{If } g(t) \leftrightarrow G(f), \text{ then } g(t)e^{j n \omega_s t} \leftrightarrow G(f - n f_s)$$

Applying this property term-by-term:

$$\bar{G}(f) = \frac{1}{T_s} \sum_{n=-\infty}^{\infty} G(f - n f_s)$$

### Step 3: Interpretation of the Spectrum

This result is the core of sampling theory. The spectrum of the sampled signal consists of:

1. **Scaling Factor:** An amplitude scaling by $\frac{1}{T_s}$ (or $f_s$).
    
2. **Spectral Replication:** Infinite copies (replicas) of the original spectrum $G(f)$ shifted by integer multiples of the sampling frequency $f_s$.
    

- $n=0$ term: $\frac{1}{T_s} G(f)$ (The Baseband / Original Signal)
    
- $n=1$ term: $\frac{1}{T_s} G(f - f_s)$ (Upper Sideband Replica)
    
- $n=-1$ term: $\frac{1}{T_s} G(f + f_s)$ (Lower Sideband Replica)
    

## 4. Aliasing and the Nyquist Limit

The recoverability of the signal depends on the spacing between these spectral replicas.

- **Bandwidth of Signal:** The spectrum $G(f)$ extends from $-B$ to $+B$.
    
- **Spacing** of **Replicas:** The replicas are centered at $0, \pm f_s, \pm 2f_s, \dots$
    

### Condition 1: $f_s > 2B$ (No Aliasing)

If the sampling frequency is high enough, the replicas are far apart.

- Right edge of Baseband ($n=0$): $+B$
    
- Left edge of first Replica ($n=1$): $f_s - B$
    
- **Gap:** The space between replicas is $(f_s - B) - B = f_s - 2B$.
    
- If $f_s > 2B$, a gap exists (Guard Band). The original signal can be isolated.
    

### Condition 2: $f_s < 2B$ (Aliasing)

If the sampling frequency is too low:

- $f_s - B < B$
    
- The replicas **overlap**.
    
- High frequencies from the $n=1$ replica "fold over" into the low frequencies of the baseband ($n=0$).
    
- **Consequence:** Information is permanently lost. The original spectrum $G(f)$ is corrupted by the tails of its neighbors.
    

## 5. Signal Reconstruction (Interpolation)

Reconstruction is the process of recovering $g(t)$ from the sampled sequence $\bar{g}(t)$.

### The Reconstruction Filter

To recover $g(t)$, we must isolate the $n=0$ term from the infinite sum $\bar{G}(f)$. We use an **Ideal Low Pass Filter (LPF)** with transfer function $H(f)$.

**Filter Specifications:**

1. **Cutoff Frequency:** $B$ (or anywhere in the guard band between $B$ and $f_s - B$).
    
2. **Gain:** $T_s$ (to cancel out the $1/T_s$ scaling introduced by sampling).
    

$$H(f) = \begin{cases} T_s & |f| \le B \\ 0 & |f| > B \end{cases} = T_s \cdot \text{rect}\left(\frac{f}{2B}\right)$$

### Time Domain Reconstruction

In the frequency domain, reconstruction is multiplication:

$$G(f) = \bar{G}(f) \cdot H(f)$$

In the time domain, this corresponds to **convolution**:

$$g(t) = \bar{g}(t) * h(t)$$

1. **Impulse Response** $h(t)$**:** The inverse Fourier transform of the ideal LPF (a rectangle) is a **Sinc function**:
    
    $$h(t) = \text{sinc}(2Bt) \quad (\text{Assuming bandwidth } B = f_s/2 \text{ for simplicity})$$
    
    _Standard formula used in notes:_ $h(t) = \text{sinc}(2\pi B t)$ (depending on normalization conventions).
    
2. **Applying Convolution:** Substitute $\bar{g}(t) = \sum g(k T_s) \delta(t - k T_s)$ into the convolution:
    
    $$g(t) = \left[ \sum_{k=-\infty}^{\infty} g(k T_s) \delta(t - k T_s) \right] * h(t)$$
3. **Linearity:** Convolution with a shifted delta function simply shifts the system response:
    
    $$\delta(t - k T_s) * h(t) = h(t - k T_s)$$
4. **The Interpolation Formula:**
    
    $$g(t) = \sum_{k=-\infty}^{\infty} g(k T_s) \cdot \text{sinc}(2\pi B (t - k T_s))$$

### Physical Interpretation

This formula represents the "Sinc Interpolation."

- Every discrete sample $g(k T_s)$ is replaced by a Sinc pulse centered at time $t = k T_s$.
    
- The height of the Sinc pulse is proportional to the sample value.
    
- The summation of all these overlapping Sinc pulses perfectly reconstructs the original smooth analog curve $g(t)$.