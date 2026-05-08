
---

### 1. Ideal Lowpass Filter (Top Section)

An **Ideal Lowpass Filter (LPF)** is designed to keep low frequencies and block high frequencies. It’s often used to remove "noise" or smooth out a signal.

- **The Rule:**
    
    - **Allow:** Frequencies where $|f| \le B$ (Note: The image writes $f \le |B|$, but mathematically this means the magnitude of frequency is less than the bandwidth $B$).
        
    - **Suppress:** Frequencies where $|f| \ge B$.
        
- **Visualizing the Magnitude $|H(f)|$:**
    
    - The graph shows a "rectangular function" centered at 0.
        
    - Everything between $-B$ and $+B$ has a gain of **1** (passes through unchanged).
        
    - Everything outside this range has a gain of **0** (completely removed).
        
    - This "brick-wall" shape is why it's called _ideal_—in the real world, filters have a gradual slope, not a vertical drop.
        

### 2. Ideal High Pass Filter (Middle Section)

An **Ideal High Pass Filter (HPF)** does the opposite. It removes the low frequencies (like DC components or slow drifts) and keeps the high-frequency details (like edges in an image or sharp transitions).

- **The Rule:**
    
    - **Allow:** Frequencies where $|f| \ge B$.
        
    - **Suppress:** Frequencies where $|f| \le B$.
        
- **Visualizing the Magnitude $|H(f)|$:**
    
    - The graph shows the signal is zero (flat line) between $-B$ and $+B$.
        
    - Outside this gap (towards positive and negative infinity), the gain is **1**.
        

### 3. Ideal Bandpass Filter (Bottom Section)

An **Ideal Bandpass Filter (BPF)** is more selective. It only lets a specific "band" or range of frequencies through, centered around a specific carrier frequency $f_0$. This is crucial in radio tuning (e.g., picking just one radio station out of the air).

- **The Rule:**
    
    - **Allow:** Transmission for the band centered at $\pm f_0$.
        
    - **Suppress:** All other frequencies.
        
- **Visualizing the Magnitude $|H(f)|$:**
    
    - You see two rectangular blocks: one centered at $+f_0$ and one at $-f_0$.
        
    - This symmetry exists because real-valued signals always have symmetric spectrums (positive and negative frequencies).
        

---

### 🔑 Key Concept: The Dotted Line (Phase Response)

In all three diagrams, you see a dotted line passing diagonally through the origin, labeled $\theta(f)$ or $\theta_n(f)$.

- **What is it?** This represents the **Phase Response**.
    
- **Why is it a straight line?** The equation written at the very bottom is $\theta(f) = -2\pi f t_d$ (or similar).
    
- **Linear Phase = Pure Delay:** When the phase is a straight line (linear), it means all frequencies are delayed by the same amount of time ($t_d$).
    
- **Distortionless Transmission:** If the phase were curved, different frequencies would arrive at different times, scrambling the signal shape (phase distortion). The straight line ensures the signal shape is preserved, just shifted in time.
#### [[Why dotted lines in the graphs?]]
    

### Summary Table

|**Filter Type**|**What it Passes**|**Visual Shape**|**Common Use**|
|---|---|---|---|
|**Lowpass**|Low Frequencies ($< B$)|Box at center|Blurring, smoothing, audio bass|
|**High Pass**|High Frequencies ($> B$)|Gap in middle|Edge detection, sharpening|
|**Bandpass**|Specific Range ($\approx f_0$)|Two side boxes|Radio tuning, Wi-Fi channels|