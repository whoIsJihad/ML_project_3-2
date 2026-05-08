# The Duality Property of the Fourier Transform

Up: [[Map of Content (DC  l2)]]
Previous: [[10 - FT Example Rectangular Pulse]]

The Duality property is one of the most elegant and powerful properties of the Fourier Transform. It arises from the deep structural symmetry between the forward and inverse transform equations. In essence, it states that if a certain shape in the time domain produces a corresponding shape in the frequency domain, then the reverse is also true.

### Formal Statement of Duality

The property can be stated formally as follows:

If a signal $x(t)$ has the Fourier Transform $X(f)$:
$$ x(t) \quad \leftrightarrow \quad X(f) $$
Then, a new time-domain signal created by taking the *functional form* of the transform $X(f)$ and substituting time $t$ for frequency $f$ will have a Fourier transform that takes the *functional form* of the original signal $x(t)$, but with a reversed and scaled frequency variable $-f$.

$$ X(t) \quad \leftrightarrow \quad x(-f) $$
(Note: The variable in $X(t)$ is just a placeholder; the key is that the *function* $X$ is now a function of time).

### Duality in Action: The Rect/Sinc Pair

The [[10 - FT Example Rectangular Pulse|rectangular pulse and sinc function]] pair is the perfect example to illustrate duality.

We previously established the transform pair:
$$ x(t) = \text{rect}\left(\frac{t}{\tau}\right) \quad \leftrightarrow \quad X(f) = \tau \cdot \text{sinc}(\pi f\tau) $$

Now, let's create a **new** signal in the time domain, $y(t)$, that has the same mathematical form as $X(f)$:
$$ y(t) = \tau \cdot \text{sinc}(\pi t\tau) $$

According to the duality property, the Fourier Transform of $y(t)$, which we'll call $Y(f)$, must have the form of the original time signal $x(t)$, with the variable substitution:
$$ Y(f) = x(-f) $$
Substituting the definition of $x(t) = \text{rect}(t/\tau)$:
$$ Y(f) = \text{rect}\left(\frac{-f}{\tau}\right) $$
Because the rectangular function is **even** (symmetric about the vertical axis), $\text{rect}(-z) = \text{rect}(z)$. Therefore, we arrive at the dual relationship:
$$ Y(f) = \text{rect}\left(\frac{f}{\tau}\right) $$

### The New Transform Pair and its Significance

We have discovered a new, powerful Fourier Transform pair:
$$ \tau \cdot \text{sinc}(\pi t\tau) \quad \leftrightarrow \quad \text{rect}\left(\frac{f}{\tau}\right) $$

A **sinc function in the time domain** corresponds to a **rectangular pulse in the frequency domain**.

This has profound practical implications, particularly for filter design. An **ideal low-pass filter** (or "brick-wall" filter) is defined as a rectangular function in the frequency domain—it allows frequencies below a certain cutoff to pass perfectly while blocking all higher frequencies. Duality tells us that the impulse response of such a filter must be a sinc function. Since the sinc function extends infinitely in time, this proves that a perfect, ideal filter is not physically realizable.

---
**Next:** [[12 - Properties of the Fourier Transform|Key Properties of the Fourier Transform]]