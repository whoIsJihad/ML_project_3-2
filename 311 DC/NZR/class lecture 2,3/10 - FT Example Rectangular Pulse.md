# Example: The Fourier Transform of a Rectangular Pulse

Up: [[Map of Content (DC  l2)]]

Previous: [[09 - The Fourier Transform Pair]]

Let's apply the Fourier Transform to a fundamental, aperiodic signal: the rectangular pulse. This example reveals a crucial and recurring relationship in signal processing.
![[Pasted image 20260501114824.png|504]]
### The Signal Definition

Consider a rectangular pulse, $x(t)$, centered at the origin with a height of 1 and a total width of $\tau$ (tau).

Mathematically, it's defined as:
$$ x(t) = \begin{cases} 1 & \text{for } |t| < \frac{\tau}{2} \\ 0 & \text{otherwise} \end{cases} $$
This is often written using the notation $\text{rect}(t/\tau)$.

### Calculation of the Fourier Transform

We use the forward transform (analysis) equation:
$$ X(f) = \int_{-\infty}^{\infty} x(t) e^{-j2\pi f t} \, dt $$
Since the signal is non-zero only from $-\tau/2$ to $\tau/2$, the integral becomes:
$$ X(f) = \int_{-\tau/2}^{\tau/2} 1 \cdot e^{-j2\pi f t} \, dt $$
We perform the integration of the complex exponential:
$$ X(f) = \left[ \frac{e^{-j2\pi f t}}{-j2\pi f} \right]_{-\tau/2}^{\tau/2} = \frac{1}{-j2\pi f} \left( e^{-j\pi f\tau} - e^{j\pi f\tau} \right) $$
By absorbing the minus sign into the parentheses, we get:
$$ X(f) = \frac{1}{j2\pi f} \left( e^{j\pi f\tau} - e^{-j\pi f\tau} \right) $$
This expression is very close to Euler's identity for the sine function: $\sin(\theta) = \frac{e^{j\theta} - e^{-j\theta}}{2j}$. To use it, we can rewrite our expression:
$$ X(f) = \frac{1}{\pi f} \left( \frac{e^{j\pi f\tau} - e^{-j\pi f\tau}}{2j} \right) = \frac{1}{\pi f} \sin(\pi f\tau) $$

### The Sinc Function

This result is conventionally written using the **sinc function**. The un-normalized sinc function is defined as $\text{sinc}(x) = \frac{\sin(x)}{x}$. To get our result into this form, we arrange the denominator to match the argument of the sine function:
$$ X(f) = \tau \cdot \frac{\sin(\pi f\tau)}{\pi f\tau} = \tau \cdot \text{sinc}(\pi f\tau) $$
Since the sinc function is purely real, the phase spectrum $\angle X(f)$ is zero (or $\pi$ where the sinc is negative).

### The Result and its Significance

The Fourier Transform of a rectangular pulse is a sinc function.
$$ \text{rect}\left(\frac{t}{\tau}\right) \quad \leftrightarrow \quad \tau \cdot \text{sinc}(\pi f\tau) $$
This is a fundamental transform pair with important implications:
1.  **Time-limited vs. Band-unlimited:** A signal that is strictly limited in time (it's non-zero for only a duration of $\tau$) has a frequency spectrum that is unlimited (it extends to infinity).
2.  **The Uncertainty Principle:** There is an inverse relationship between the duration of the signal in the time domain and the width of its spectral main lobe in the frequency domain.
    *   A **wide** rectangular pulse (large $\tau$) produces a **narrow** and tall sinc function in frequency. Its signal energy is concentrated in a small band of frequencies.
    *   A **narrow** rectangular pulse (small $\tau$) produces a **wide** and short sinc function in frequency. Its signal energy is spread out over a wide range of frequencies.

This principle is fundamental to signal processing: a signal cannot be arbitrarily short in both the time and frequency domains simultaneously.

---
**Next:** [[11 - FT Property Duality|The Duality Property]]