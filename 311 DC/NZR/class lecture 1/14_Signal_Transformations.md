# 14. Signal Properties (Transformations)

Understanding how simple transformations affect a signal in the time domain is a fundamental part of signal processing. These operations—shifting, scaling, and inversion—form the basis for more complex signal manipulations.

Let's consider a generic signal $x(t)$. 

---

### 1. Time Shifting

Time shifting moves the entire signal left or right along the time axis without changing its shape.

The mathematical representation is $y(t) = x(t - t_0)$.

*   **If $t_0 > 0$ (e.g., $x(t - 2)$):**
    *   The signal is shifted to the **right**.
    *   This represents a **delay**. The event at time `t=0` in the original signal now occurs at `t=t_0`.
*   **If $t_0 < 0$ (e.g., $x(t + 2)$):**
    *   The signal is shifted to the **left**.
    *   This represents an **advance**. The event at time `t=0` in the original signal now occurs at `t=-|t_0|`.

**Mnemonic:** Think about what value of `t` makes the argument of $x$ equal to zero. For $x(t-2)$, the argument is zero when $t=2$, so the origin of the signal moves to `t=2` (a right shift).

---

### 2. Time Scaling

Time scaling compresses or stretches the signal along the time axis.

The mathematical representation is $y(t) = x(at)$.

*   **If $|a| > 1$ (e.g., $x(2t)$):**
    *   The signal is **compressed** (it becomes "faster").
    *   The duration of the signal is divided by `a`. An event that happened at `t=T` in the original signal now happens at `t=T/a`.
*   **If $0 < |a| < 1$ (e.g., $x(t/2)$ or $x(0.5t)$):**
    *   The signal is **stretched** or expanded (it becomes "slower").
    *   The duration of the signal is multiplied by `1/a`. An event that happened at `t=T` in the original signal now happens at `t=T/a`.

---

### 3. Time Inversion (or Reversal)

Time inversion flips the signal around the vertical axis (the y-axis, where $t=0$). It creates a mirror image in time.

The mathematical representation is $y(t) = x(-t)$.

This is technically a special case of time scaling where $a = -1$. The part of the signal that was in the future (positive time) is now in the past (negative time), and vice versa.

---

### Combining Transformations

These operations can be combined, for example, $y(t) = x(at - b)$. It is important to perform the operations in the correct order. This can be done in two ways, with the shift amount changing depending on the order:

1.  **Shift then Scale:** $x(t) \to x(t-b) \to x(a(t-b)) = x(at - ab)$.
2.  **Scale then Shift:** $x(t) \to x(at) \to x(a(t - b/a)) = x(at - b)$.

The second method (scale first, then shift by $b/a$) is often more intuitive for finding the final position of the signal.
