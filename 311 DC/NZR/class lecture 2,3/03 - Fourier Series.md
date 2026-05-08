## 3. Fourier Series for Periodic Signals

The Fourier Series is a monumental tool in signal processing, allowing us to understand the frequency content of any periodic signal. It posits that any periodic signal can be represented as a sum of harmonically related sinusoids.

### 3.1. The Core Idea: A Signal's Recipe

Imagine a complex sound from an orchestra. Despite its richness, it's just a combination of individual notes played by different instruments. Similarly, the Fourier Series suggests that any periodic signal, regardless of its apparent complexity, can be broken down into, or built up from, a collection of simple sine and cosine waves.

This breakdown provides a "recipe" for the signal, detailing:
*   **Frequencies:** The specific rates at which the constituent sine and cosine waves oscillate.
*   **Amplitudes:** The "strength" or intensity of each wave.
*   **Phases:** The starting point or shift of each wave relative to a reference.

### 3.2. Periodicity and Fundamental Frequency

A signal $x(t)$ is **periodic** if it repeats its pattern exactly over fixed intervals of time. This fixed interval is called the **fundamental period**, denoted $T_0$.

Mathematically, this means:
$$ x(t) = x(t + T_0) \quad \text{for all } t $$

Associated with the fundamental period is the **fundamental angular frequency**, $\omega_0$, measured in radians per second:
$$ \omega_0 = \frac{2\pi}{T_0} $$
All the sinusoidal components in the Fourier Series will have frequencies that are integer multiples of this fundamental frequency ($n\omega_0$), known as **harmonics**.

### What do we mean by "Harmonically Related Sinusoids"?

This phrase means that all the sine and cosine waves used in the Fourier Series have frequencies that are *integer multiples* of a single, common fundamental frequency ($\omega_0$).

For instance, if $\omega_0$ is our base frequency:
*   The first harmonic has frequency $1 \cdot \omega_0 = \omega_0$.
*   The second harmonic has frequency $2 \cdot \omega_0$.
*   The third harmonic has frequency $3 \cdot \omega_0$.
*   And so on.

The reason they *must* be harmonically related is fundamental to the concept of a periodic signal. If our original signal $x(t)$ has a period $T_0$, then all the components that sum up to form $x(t)$ must also, individually or collectively, repeat with period $T_0$. A sinusoid with frequency $n\omega_0$ has a period of $T_0/n$. This means it completes $n$ cycles within the fundamental period $T_0$, ensuring it is also periodic with $T_0$. If we included a sinusoid whose frequency was *not* an integer multiple of $\omega_0$ (e.g., $1.5\omega_0$), its period would not align with $T_0$, and the sum would no longer be periodic with $T_0$.

Think of it like different instruments in an orchestra all playing in tune with a central pitch. Each instrument might play a different note, but they are all related to the fundamental scale. This relationship ensures that when combined, they create a cohesive, repeating sound (our original periodic signal).

### 3.3. Forms of the Fourier Series

There are several equivalent forms of the Fourier Series, each offering a different perspective or convenience for specific applications.

#### 3.3.1. Trigonometric Fourier Series

This is the most intuitive form, directly showing the sine and cosine components. For a periodic signal $x(t)$ with fundamental period $T_0$ and fundamental angular frequency $\omega_0$, the trigonometric Fourier Series is given by:

$$ x(t) = a_0 + \sum_{n=1}^{\infty} \left( a_n \cos(n\omega_0 t) + b_n \sin(n\omega_0 t) \right) $$

Where:
*   **$a_0$**: The **DC component**, representing the average value of the signal over one period.
*   $\sum_{n=1}^{\infty}$   : The summation indicates that the signal is formed by an infinite sum of harmonic components.
*   **$n$**: The **harmonic number**. $n=1$ corresponds to the fundamental frequency, $n=2$ to the second harmonic, and so on.
*   **$a_n$ and $b_n$**: The **Fourier coefficients**, which quantify the amplitude of the cosine and sine components at the $n$-th harmonic, respectively.

#### 3.3.2. Compact Trigonometric Fourier Series

This form combines the sine and cosine terms of each harmonic into a single cosine term with a phase shift, often making it easier to visualize amplitude and phase directly.

$$ x(t) = C_0 + \sum_{n=1}^{\infty} C_n \cos(n\omega_0 t - \theta_n) $$

Where:
*   $C_0 = a_0$
*   $C_n = \sqrt{a_n^2 + b_n^2}$ (the peak amplitude of the $n$-th harmonic)
*   $\theta_n = \arctan\left(\frac{b_n}{a_n}\right)$ (the phase angle of the $n$-th harmonic)

#### 3.3.3. Exponential Fourier Series

This is the most general and mathematically elegant form, especially useful in advanced analysis. It uses complex exponentials, which inherently combine amplitude and phase information.

$$ x(t) = \sum_{n=-\infty}^{\infty} c_n e^{jn\omega_0 t} $$

Where $j$ is the imaginary unit ($j = \sqrt{-1}$). The coefficients $c_n$ are complex and are given by:
$$ c_n = \frac{1}{T_0} \int_{T_0} x(t) e^{-jn\omega_0 t} \, dt $$


#### Not shown by NZR 
The relationship between the exponential and trigonometric coefficients is:
*   $c_0 = a_0$
*   For $n > 0$: $c_n = \frac{1}{2}(a_n - jb_n)$
*   For $n > 0$: $c_{-n} = \frac{1}{2}(a_n + jb_n) = c_n^*$ (where $c_n^*$ is the complex conjugate of $c_n$)

The exponential form uses both positive and negative indices for $n$. These "negative frequencies" are mathematical constructs that arise naturally from Euler's formula ($e^{j\theta} = \cos\theta + j\sin\theta$) and elegantly represent the phase relationships.

### 3.4. Calculating the Fourier Coefficients
Re
The core task in Fourier analysis is finding the coefficients ($a_0, a_n, b_n$ for trigonometric; $c_n$ for exponential) that describe the signal's frequency content. This is done using integral formulas derived from the **orthogonality** of sinusoidal functions. Essentially, multiplying the signal by a specific sinusoid and integrating over a period isolates the contribution of that sinusoid.

#### For Trigonometric Form ( Not taught by NZR):
Read this here [[The unit impulse train]]
1.  **DC Component ($a_0$):**
    $$ a_0 = \frac{1}{T_0} \int_{T_0} x(t) \, dt $$
    This is simply the average value of $x(t)$ over one period.

2.  **Cosine Coefficients ($a_n$ for $n \ge 1$):**
    $$ a_n = \frac{2}{T_0} \int_{T_0} x(t) \cos(n\omega_0 t) \, dt $$
    This extracts the amplitude of the cosine component at the $n$-th harmonic.

3.  **Sine Coefficients ($b_n$ for $n \ge 1$):**
    $$ b_n = \frac{2}{T_0} \int_{T_0} x(t) \sin(n\omega_0 t) \, dt $$
    This extracts the amplitude of the sine component at the $n$-th harmonic.

#### For Exponential Form (NZR):

1.  **Complex Coefficients ($c_n$ for all $n$):**
    $$ c_n = \frac{1}{T_0} \int_{T_0} x(t) e^{-jn\omega_0 t} \, dt $$
    These complex coefficients directly provide both the amplitude and phase information for each harmonic.

### 3.5. Key Properties of Fourier Series

The Fourier Series possesses several important properties that simplify analysis and provide insights into how signals behave under various operations.

*   **Linearity:** If $x(t) \leftrightarrow FS_x$ and $y(t) \leftrightarrow FS_y$, then $A x(t) + B y(t) \leftrightarrow A FS_x + B FS_y$. (The Fourier Series of a sum is the sum of the Fourier Series).
*   **Time Shift:** Shifting a signal in time affects only the phase of its Fourier coefficients, not their magnitudes. If $x(t) \leftrightarrow c_n$, then $x(t - t_d) \leftrightarrow c_n e^{-jn\omega_0 t_d}$.
*   **Frequency Shift (Modulation):** Multiplying a signal by a complex exponential shifts its frequency components. If $x(t) \leftrightarrow c_n$, then $e^{jM\omega_0 t} x(t) \leftrightarrow c_{n-M}$.
*   **Differentiation in Time:** Differentiating a signal in the time domain corresponds to multiplying its Fourier coefficients by $jn\omega_0$. If $x(t) \leftrightarrow c_n$, then $\frac{d}{dt} x(t) \leftrightarrow (jn\omega_0) c_n$. This shows that higher frequencies are emphasized.
*   **Integration in Time:** Integrating a signal in the time domain corresponds to dividing its Fourier coefficients by $jn\omega_0$ (with special handling for the DC component). If $x(t) \leftrightarrow c_n$, then $\\int x(\\tau) d\\tau \leftrightarrow \frac{c_n}{jn\omega_0}$. This shows that lower frequencies are emphasized.
*   **Parseval's Theorem:** This theorem relates the average power of a periodic signal in the time domain to the average power of its harmonic components in the frequency domain. It states that the total average power of a periodic signal is the sum of the average powers of its individual harmonic components.
    $$ \frac{1}{T_0} \int_{T_0} |x(t)|^2 \, dt = \sum_{n=-\infty}^{\infty} |c_n|^2 $$
    This theorem is fundamental for understanding power distribution across different frequencies.

This concludes our comprehensive overview of the Fourier Series.

### 3.6. A Short, Practical Exponential-Form Explanation (Simple)

The exponential Fourier Series is a compact way to describe a periodic signal using complex exponentials. Think of each complex coefficient $c_n$ as a labeled container: it stores how much of the frequency $n\omega_0$ is present and what its phase is.

How to compute the coefficients (step-by-step):
- Identify the fundamental period $T_0$ and fundamental angular frequency $\omega_0 = 2\pi/T_0$.
- Use the formula:
    $$ c_n = \frac{1}{T_0} \int_{T_0} x(t) e^{-j n \omega_0 t} \, dt $$
- Each $c_n$ is a complex number. Its magnitude $|c_n|$ tells you the amplitude of that harmonic; its angle $\angle c_n$ is the phase shift.

Why negative indices appear: complex exponentials combine sines and cosines via Euler's formula. A real cosine at frequency $k\omega_0$ shows up as two equal complex coefficients at $n=+k$ and $n=-k$ (they are complex conjugates). Negative indices are just the other half of the pair that together make real-valued sinusoids.

Quick examples (useful to memorise):
- Pure cosine: $x(t)=A\cos(k\omega_0 t)$. Nonzero coefficients only at $n=\pm k$, with
    $$ c_{\pm k} = \frac{A}{2} \quad\text{(and all other } c_n=0) $$
- Square wave (50% duty, amplitude ±A): only odd harmonics appear, and the coefficients decay like $1/n$. That is why the square wave looks "sharp" in time — it needs many high-frequency harmonics.

Practical tips:
- If $x(t)$ is real, coefficients satisfy $c_{-n}=c_n^*$ (complex conjugates). You can therefore inspect only $n\ge0$ for amplitude info.
- Smooth signals have rapidly decaying $|c_n|$; discontinuities cause slow decay (harmonics fall off ~1/n), explaining Gibbs ringing near jumps.
- For engineering, compute a few dominant $c_n$ terms to get a good approximation of the signal.

This short, example-driven view keeps the math compact while making clear how to read and build signals from the exponential coefficients.