# Key Properties of the Fourier Transform

Up: [[Map of Content (DC  l2)]]

Previous: [[11 - FT Property Duality]]

The Fourier Transform properties are essential tools that allow us to understand how signal operations in the time domain affect the frequency domain, and vice-versa. They often provide valuable insights and shortcuts, bypassing the need for direct integration.

Assume we have the transform pairs $x(t) \leftrightarrow X(f)$ and $y(t) \leftrightarrow Y(f)$.

### 1. Linearity
The transform of a weighted sum of signals is the weighted sum of their individual transforms.
$$ a x(t) + b y(t) \quad \leftrightarrow \quad a X(f) + b Y(f) $$

### 2. Time Shift
A delay in the time domain corresponds to a linear phase shift in the frequency domain. The magnitude of the spectrum is unaffected.
$$ x(t - t_0) \quad \leftrightarrow \quad e^{-j2\pi f t_0} X(f) $$

### 3. Frequency Shift (Modulation)
Multiplying a time-domain signal by a complex exponential (the basis of modulation) results in a shift in the frequency domain.
$$ e^{j2\pi f_0 t} x(t) \quad \leftrightarrow \quad X(f - f_0) $$

### 4. Time and Frequency Scaling
Stretching or compressing a signal in time has the opposite effect on the frequency scale. Let 'a' be a real, non-zero constant.
$$ x(at) \quad \leftrightarrow \quad \frac{1}{|a|} X\left(\frac{f}{a}\right) $$
This captures the uncertainty principle: stretching a signal in time (making it "slower") compresses its spectrum (making it more "narrow-band"), and vice-versa.

### 5. Duality
There is a fundamental symmetry between the time and frequency domains. A functional form in one domain corresponds to a dual functional form in the other.
> See note: [[11 - FT Property Duality|The Duality Property]]
$$ X(t) \quad \leftrightarrow \quad x(-f) $$

### 6. The Convolution Theorem
Perhaps the most important property for system analysis. **Convolution in the time domain becomes simple multiplication in the frequency domain.** This is why we use Fourier methods to analyze Linear Time-Invariant (LTI) systems.
$$ x(t) * y(t) \quad \leftrightarrow \quad X(f) Y(f) $$
(Where `*` denotes the convolution operation).

### 7. The Multiplication Theorem
The dual of the convolution property. Multiplication in the time domain becomes convolution in the frequency domain.
$$ x(t) y(t) \quad \leftrightarrow \quad X(f) * Y(f) $$

### 8. Differentiation in Time
Differentiating a signal in time is equivalent to multiplying its transform by $j2\pi f$. This acts as a high-pass filter, amplifying higher frequencies.
$$ \frac{d}{dt} x(t) \quad \leftrightarrow \quad j2\pi f X(f) $$

### 9. Integration in Time
Integrating a signal in time is equivalent to dividing its transform by $j2\pi f$ (with careful handling of the DC component). This acts as a low-pass filter, attenuating higher frequencies.
$$ \int_{-\infty}^{t} x(\tau) \, d\tau \quad \leftrightarrow \quad \frac{1}{j2\pi f}X(f) + \frac{1}{2}X(0) \delta(f) $$

### 10. Parseval's Theorem for Energy
This theorem relates the total energy in a signal, whether computed in the time domain or the frequency domain. Energy is conserved by the transform.
$$ \int_{-\infty}^{\infty} |x(t)|^2 \, dt = \int_{-\infty}^{\infty} |X(f)|^2 \, df $$
---

### 11. Conjugation Property
[[Conjugation Property of FT]]
This completes our introductory series on the Fourier Transform.