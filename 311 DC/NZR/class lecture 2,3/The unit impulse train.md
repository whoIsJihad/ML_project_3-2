Here's the idea first, then we'll build it step by step.

**The unit impulse train** (also called the Dirac comb or Shah function) is an infinite series of equally-spaced delta impulses. Because it's periodic, we can represent it as a Fourier series — a sum of sinusoids.

The key insight: since the signal is periodic with period $T_0$, the Fourier series only has frequencies at multiples of $f_0 = 1/T_0$. Let's find those coefficients.

---

**Step 1 — Define the signal**

$$x(t) = \sum_{k=-\infty}^{\infty} \delta(t - kT_0)$$

A spike at $t = 0, \pm T_0, \pm 2T_0, \ldots$

**Step 2 — Recall the Fourier series formula**

For any periodic signal with period $T_0$:

$$x(t) = \sum_{n=-\infty}^{\infty} c_n , e^{j 2\pi n f_0 t}$$

The coefficients $c_n$ are found by:

$$c_n = \frac{1}{T_0} \int_{-T_0/2}^{T_0/2} x(t) , e^{-j 2\pi n f_0 t} , dt$$

**Step 3 — Plug in the impulse train**

$$c_n = \frac{1}{T_0} \int_{-T_0/2}^{T_0/2} \sum_{k} \delta(t - kT_0) \cdot e^{-j 2\pi n f_0 t} , dt$$

Over one period $[-T_0/2, T_0/2]$, only the $k=0$ impulse lives inside. So:

$$c_n = \frac{1}{T_0} \int_{-T_0/2}^{T_0/2} \delta(t) \cdot e^{-j 2\pi n f_0 t} , dt$$

**Step 4 — Use the sifting property of delta**

The sifting property says: $\int \delta(t) \cdot f(t) , dt = f(0)$

So evaluating at $t = 0$:

$$c_n = \frac{1}{T_0} \cdot e^{0} = \frac{1}{T_0}$$

**Step 5 — The result**

Every coefficient is the same: $c_n = \frac{1}{T_0}$ for all $n$.

$$\boxed{x(t) = \frac{1}{T_0} \sum_{n=-\infty}^{\infty} e^{j 2\pi n f_0 t}}$$

---

This means the impulse train is made up of **all harmonics equally** — flat spectrum. Let me show you what this looks like:---
![[Pasted image 20260413122910.png]]
**The big takeaway:**

The impulse train has a flat spectrum — every harmonic $n$ carries the same weight $1/T_0$. This is the signal-processing equivalent of "everything at once," which makes sense: a perfect spike contains all frequencies equally.

Two things worth noting:

- Wider spacing between impulses (larger $T_0$) → smaller coefficient $1/T_0$ → spectrum gets denser (harmonics pack closer since $f_0 = 1/T_0$ shrinks)
- This result is the foundation for understanding **sampling**: sampling a signal is equivalent to multiplying by an impulse train, which in frequency domain becomes convolution with this flat spectrum

