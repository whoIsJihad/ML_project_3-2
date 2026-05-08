# The Fourier Transform Pair: Definition

Up: [[Map of Content (DC  l2)|Map of Content (DC  l2)]]
Previous: [[08 - From Fourier Series to Transform]]

The Fourier Transform is defined by a pair of equations that allow us to move between the time domain and the frequency domain. One equation analyzes the signal to find its spectrum, and the other synthesizes the signal from its spectrum.

### The Transform Pair

A time-domain signal, $x(t)$, and its frequency-domain representation, $X(f)$, are linked by the following two equations.

#### 1. The Forward Fourier Transform (Analysis Equation)

The Forward Transform takes a time-domain signal $x(t)$ and maps it to its frequency-domain representation $X(f)$. This process is called **analysis** because it breaks the signal down into its constituent frequency components.

The formula is:
$$ X(f) = \mathcal{F}\{x(t)\} = \int_{-\infty}^{\infty} x(t) e^{-j2\pi f t} \, dt $$

The output, $X(f)$, is a complex function that describes the frequency content of $x(t)$:
*   The **Magnitude Spectrum**, $|X(f)|$, tells us the amplitude of each frequency component.
*   The **Phase Spectrum**, $\angle X(f)$, tells us the phase shift of each frequency component.

#### 2. The Inverse Fourier Transform (Synthesis Equation)

The Inverse Transform takes a frequency-domain representation $X(f)$ and maps it back to the original time-domain signal $x(t)$. This process is called **synthesis** because it rebuilds the signal from its frequency components.

The formula is:
$$ x(t) = \mathcal{F}^{-1}\{X(f)\} = \int_{-\infty}^{\infty} X(f) e^{j2\pi f t} \, df $$

### Shorthand Notation

It is common to use the following notation to indicate that $x(t)$ and $X(f)$ are a Fourier Transform pair:

$$ x(t) \leftrightarrow X(f) $$

This pair of equations is the cornerstone of Fourier analysis for aperiodic signals.

---
**Next:** [[10 - FT Example Rectangular Pulse|Example: The Fourier Transform of a Rectangular Pulse]]
