# Lecture 2: Signal Processing Fundamentals

## 1. Unit Impulse Function (Dirac Delta Function)

The unit impulse function, denoted $\delta(t)$, is a fundamental concept in signal processing. It represents a signal of infinite amplitude and zero duration at a specific point in time, with a total area of one. While not physically realizable, it is an incredibly useful mathematical abstraction for analyzing system responses to instantaneous events.

### Formal Definition

The unit impulse function is defined by two key properties:

1.  **Value at non-zero points:**
    $$ \delta(t) = 0 \quad \text{for } t \neq 0 $$
    This means the impulse exists only at $t=0$. For any other time, its value is zero.

2.  **Area under the curve (Unit Area Property):**
    $$ \int_{-\infty}^{\infty} \delta(t) \, dt = 1 $$
    Despite being zero everywhere except at $t=0$, the integral over all time is equal to one. This gives the impulse its "unit strength."

### The Sampling (Sifting) Property

One of the most important properties of the unit impulse function is its sampling, or sifting, property. This property states that when a function $x(t)$ is multiplied by an impulse $\delta(t - t_0)$ and then integrated, the result is the value of the function $x(t)$ at the point $t_0$.

For any function $x(t)$ that is continuous at $t = t_0$, the sampling property is given by:
$$ \int_{-\infty}^{\infty} x(t) \delta(t - t_0) \, dt = x(t_0) $$

**Interpretation:**
The impulse $\delta(t - t_0)$ is shifted to occur at time $t_0$. When it multiplies $x(t)$, it effectively "samples" the value of $x(t)$ precisely at $t_0$, discarding all other information about $x(t)$. This property is crucial for operations like convolution and system analysis.

### Sampling Property with Finite Integration Limits

When integrating the product of a function $x(t)$ and a shifted impulse $\delta(t - t_0)$ over a finite interval $[a, b]$, the outcome depends on whether the impulse falls within the integration limits:

1.  **If the impulse is within the limits ($a < t_0 < b$):**
    $$ \int_{a}^{b} x(t) \delta(t - t_0) \, dt = x(t_0) \quad \text{if } a < t_0 < b $$
    In this case, the impulse function behaves as it does with infinite limits, sampling $x(t)$ at $t_0$.

2.  **If the impulse is outside the limits ($t_0 < a$ or $t_0 > b$):**
    $$ \int_{a}^{b} x(t) \delta(t - t_0) \, dt = 0 \quad \text{if } t_0 < a \text{ or } t_0 > b $$
    If the impulse's location $t_0$ is outside the integration interval $[a, b]$, the integral is zero because the impulse function is zero across the entire integration range.
