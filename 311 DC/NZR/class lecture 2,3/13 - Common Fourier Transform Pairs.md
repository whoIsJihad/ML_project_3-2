# 13 - Common Fourier Transform Pairs

Up: [[Map of Content (DC  l2)|Map of Content (DC  l2)]]

This document provides a quick reference for some of the most frequently encountered Fourier Transform pairs. The notation $x(t) \leftrightarrow X(f)$ is used, where $\omega = 2\pi f$.

### 1. The Constant (DC) Signal
A constant value of 1 in the time domain corresponds to a Dirac delta function at zero frequency. This indicates all the signal's energy is at DC (f=0).

$$ 1 \quad \leftrightarrow \quad \delta(f) $$

### 2. The Dirac Delta Function (Impulse)
An impulse at the origin in the time domain contains all frequencies with equal amplitude and zero phase.

$$ \delta(t) \quad \leftrightarrow \quad 1 $$

### 3. Shifted Dirac Delta Function
A delayed impulse in time results in a linear phase shift in the frequency domain.

$$ \delta(t - t_0) \quad \leftrightarrow \quad e^{-j2\pi f t_0} $$

### 4. The Complex Exponential
A pure complex exponential in time is a single impulse in frequency.

$$ e^{j2\pi f_0 t} \quad \leftrightarrow \quad \delta(f - f_0) $$

### 5. Cosine Function
Using Euler's identity, $\cos(2\pi f_0 t) = \frac{1}{2}(e^{j2\pi f_0 t} + e^{-j2\pi f_0 t})$, we can use the linearity and frequency shift properties to find the transform.

$$ \cos(2\pi f_0 t) \quad \leftrightarrow \quad \frac{1}{2}[\delta(f - f_0) + \delta(f + f_0)] $$

### 6. Sine Function
Similarly for the sine function, $\sin(2\pi f_0 t) = \frac{1}{2j}(e^{j2\pi f_0 t} - e^{-j2\pi f_0 t})$.

$$ \sin(2\pi f_0 t) \quad \leftrightarrow \quad \frac{1}{2j}[\delta(f - f_0) - \delta(f + f_0)] $$

### 7. The Signum (Sign) Function
The signum function, which is +1 for t > 0 and -1 for t < 0.

$$ \text{sgn}(t) \quad \leftrightarrow \quad \frac{1}{j\pi f} $$

### 8. The Unit Step Function
The unit step function, $u(t)$, can be expressed in terms of the signum function as $u(t) = \frac{1}{2}(\text{sgn}(t) + 1)$. Using linearity:

$$ u(t) \quad \leftrightarrow \quad \frac{1}{2}\left(\frac{1}{j\pi f} + \delta(f)\right) $$

### 9. Decaying Exponential
A one-sided decaying exponential, for a real constant $a > 0$.

$$ e^{-at}u(t) \quad \leftrightarrow \quad \frac{1}{a + j2\pi f} $$

---
This provides a foundation for many common signals. More complex transforms can often be derived from these using the [[12 - Properties of the Fourier Transform|properties of the Fourier Transform]].
