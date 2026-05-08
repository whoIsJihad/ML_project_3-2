# 13. Signal Energy and Power Formulas

The classification of signals into energy or power signals is based on the formal mathematical definitions of signal energy and signal power. These definitions are derived by considering the signal's amplitude (often a voltage or current) across a standard 1-ohm resistor.

---

### 1. Signal Energy ($E$)

**Signal Energy** is the total energy of a signal $x(t)$ integrated over all time, from negative infinity to positive infinity.

For a continuous-time signal $x(t)$, the formula is:
$$
E = \int_{-\infty}^{\infty} |x(t)|^2 dt
$$

*   **$|x(t)|^2$**: This term represents the **instantaneous power** of the signal at time `t`. By squaring the amplitude, we ensure the value is always positive and proportional to power (since Power $\propto$ Voltage²). The absolute value is used to handle complex-valued signals, but for real signals, it is equivalent to $x(t)^2$.
*   $\int_{-\infty}^{\infty} \dots dt$ : This integral sums up the instantaneous power over all time to give the total energy.

**For a signal to be an Energy Signal, the result of this integral must be a finite, positive number ($0 < E < \infty$).**

---

### 2. Signal Power ($P$)

**Signal Power** is the *average* power of a signal $x(t)$ calculated over an infinite time duration. To compute this, we first find the energy of the signal over a large interval from $-T$ to $T$, and then we divide by the duration of that interval ($2T$). Finally, we take the limit as the interval becomes infinitely large.

For a continuous-time signal $x(t)$, the formula is:
$$
P = \lim_{T \to \infty} \frac{1}{2T} \int_{-T}^{T} |x(t)|^2 dt
$$

*   $\int_{-T}^{T} |x(t)|^2 dt$ : This is the energy of the signal over the interval $[-T, T]$.
*   **$\frac{1}{2T}$**: This is the division by the duration of the interval, which gives the *average power* within that interval.
*   $\lim_{T \to \infty}$ : This finds the average power over all time.

**For a signal to be a Power Signal, the result of this limit must be a finite, positive number ($0 < P < \infty$).**

For periodic signals, this calculation simplifies. The average power can be calculated over a single period ($T_0$) instead of over all time:
$$
P = \frac{1}{T_0} \int_{0}^{T_0} |x(t)|^2 dt
$$

### Next : [[14_Signal_Transformations]]