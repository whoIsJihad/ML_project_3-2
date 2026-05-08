## 2. Unit Step Function and its Relation to the Unit Impulse

### The Unit Step Function ($u(t)$)

The unit step function, denoted as $u(t)$, is a fundamental signal used to represent a signal that switches "on" at a specific time and remains on. It is conceptually simple, acting like a perfect switch.

**Formal Definition:**
The unit step function is defined as:
$$ u(t) = \begin{cases} 0 & \text{for } t < 0 \\ 1 & \text{for } t \ge 0 \end{cases} $$
Before time $t=0$, the function's value is 0. At and after $t=0$, its value is 1.

### Relationship with the Unit Impulse Function

The connection between the unit step and the unit impulse is a fundamental relationship rooted in calculus. They are derivatives/integrals of one another.

1.  **The Derivative of the Step is the Impulse**

    The derivative of the unit step function is the unit impulse function.
    $$ \frac{d}{dt}u(t) = \delta(t) $$
    **Explanation:** The unit step function $u(t)$ is constant for all $t<0$ and all $t>0$, so its derivative is 0 in these regions. At $t=0$, there is a discontinuity (an instantaneously vertical jump). The derivative captures this infinitely fast rate of change at a single point, which is precisely the nature of the unit impulse function $\delta(t)$.

2.  **The Integral of the Impulse is the Step**

    Conversely, the unit step function is the running integral of the unit impulse function.
    $$ \int_{-\infty}^{t} \delta(\tau) \, d\tau = u(t) $$
    **Explanation:** We can understand this by considering the value of the integral as the upper limit $t$ varies:
    -   If $t < 0$, the interval of integration $(-\infty, t)$ does not include the impulse at $\tau=0$. Therefore, the integral is 0.
    -   If $t \ge 0$, the interval of integration now includes the impulse at $\tau=0$. The integral accumulates the total area of the impulse, which is 1.
    This behavior, where the function is 0 for $t<0$ and 1 for $t \ge 0$, is the exact definition of the unit step function $u(t)$.

### Next : [[03 - Fourier Series]]