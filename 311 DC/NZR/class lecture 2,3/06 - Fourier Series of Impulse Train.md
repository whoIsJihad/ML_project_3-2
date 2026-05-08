## 6. Fourier Series of a Unit Impulse Train

The unit impulse train is a fundamental periodic signal in digital signal processing and communications. Its Fourier series reveals a deep and important relationship between the time and frequency domains.

### The Signal: The Unit Impulse Train

A unit impulse train, denoted $x(t)$, is an infinite series of uniformly spaced Dirac delta functions.

Let the period of the train be $T_0$. The signal is defined as:
$$ x(t) = \sum_{k=-\infty}^{\infty} \delta(t - k T_0) $$
This signal consists of unit impulses at every integer multiple of the period $T_0$ (..., $-2T_0$, $-T_0$, 0, $T_0$, $2T_0$, ...). The fundamental angular frequency is, as always, $\omega_0 = 2\pi / T_0$.

### The Goal: Finding the Fourier Coefficients

For this derivation, the **exponential Fourier series** is the most direct and elegant approach. Our goal is to find the complex coefficients, $c_n$, in the series representation:
$$ x(t) = \sum_{n=-\infty}^{\infty} c_n e^{jn\omega_0 t} $$

The formula for the coefficients is:
$$ c_n = \frac{1}{T_0} \int_{T_0} x(t) e^{-jn\omega_0 t} \, dt $$
The integral is over any single period of duration $T_0$. For convenience, let's choose the interval from $-T_0/2$ to $T_0/2$.

### The Calculation

Within our chosen integration interval, $[-T_0/2, T_0/2]$, the impulse train $x(t) = \sum_{k=-\infty}^{\infty} \delta(t - k T_0)$ has only **one** impulse: the one at $k=0$.

Therefore, within this interval, $x(t) = \delta(t)$.

Let's substitute this into the coefficient formula:
$$ c_n = \frac{1}{T_0} \int_{-T_0/2}^{T_0/2} \delta(t) e^{-jn\omega_0 t} \, dt $$

Now, we use the **sifting (or sampling) property** of the Dirac delta function. The property states that for any function $f(t)$ continuous at $t=0$:
$$ \int_{-\infty}^{\infty} \delta(t) f(t) \, dt = f(0) $$
Since our integral's limits include $t=0$, the property applies perfectly. Our function is $f(t) = e^{-jn\omega_0 t}$. We just need to evaluate this function at $t=0$.

$$ c_n = \frac{1}{T_0} \left( e^{-jn\omega_0 \cdot 0} \right) $$
$$ c_n = \frac{1}{T_0} \left( e^0 \right) $$
$$ c_n = \frac{1}{T_0} $$

### The Result and Its Significance

This result is remarkably simple and elegant. Every single Fourier coefficient, $c_n$, is the same constant value: $1/T_0$.

Now we substitute this back into the series definition to get the final Fourier Series representation of the unit impulse train:
$$ \sum_{k=-\infty}^{\infty} \delta(t - k T_0) => \sum_{n=-\infty}^{\infty} \left( \frac{1}{T_0} \right) e^{jn\omega_0 t} $$

**Significance:**
This result is profound. It shows that a signal composed of infinitely sharp, perfectly localized spikes in the **time domain** (the impulse train) is composed of an infinite number of harmonically related complex sinusoids in the **frequency domain**, and **all of these sinusoids have the exact same amplitude**.

A signal that is perfectly localized in time is completely spread out, or "delocalized," in frequency. It contains components of every harmonic, all equally weighted. This duality is a cornerstone of Fourier analysis.
