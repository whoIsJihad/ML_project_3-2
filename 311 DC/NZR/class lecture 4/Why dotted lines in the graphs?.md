
### 1. The Mathematical Origin: Time Shifting Property

The dotted line comes directly from the **Time Shifting Property** of the Fourier Transform.

- **Goal:** You want the filter to pass certain frequencies but eventually output the signal with a simple time delay $t_d$ (e.g., it takes $t_d$ seconds for electricity to travel through the circuit).
    
- Time Domain:
    
    $$y(t) = x(t - t_d)$$
    
- Frequency Domain (Fourier Transform):
    
    Applying the shift property:
    
    $$Y(f) = X(f) \cdot e^{-j 2\pi f t_d}$$
    

### 2. Deriving the Phase Equation

An LTI system is described by $Y(f) = X(f) H(f)$.

Comparing this to the equation above, the Transfer Function $H(f)$ for a pure delay is:

$$H(f) = 1 \cdot e^{-j 2\pi f t_d}$$

This complex number $H(f)$ has two parts:

- **Magnitude $|H(f)| = 1$:** The gain is 1 (signal doesn't get louder or quieter).
    
- **Phase $\theta(f) = -2\pi f t_d$:** This is the exponent term.
    

### 3. Interpreting the Graph (The "Dotted Line")

Your class note plots $\theta(f)$ on the y-axis vs $f$ on the x-axis. Look at the phase equation again:

$$\theta(f) = \underbrace{(-2\pi t_d)}_{\text{slope } m} \cdot f$$

- This is the equation of a straight line $y = mx$.
    
- **Variable:** $f$ (Frequency).
    
- **Slope:** $-2\pi t_d$ (Constant, because delay $t_d$ is constant).
    
- **Result:** A straight diagonal line passing through the origin.
    

### 4. Why "Linear" Matters (Group Delay)

Why do we demand a straight line?

- Group Delay Definition: The time delay experienced by a specific frequency is the negative derivative of the phase:
    
    $$\text{Delay}(\tau_g) = -\frac{1}{2\pi} \frac{d\theta(f)}{df}$$
    
- **If $\theta(f)$ is Linear:** The derivative is constant ($t_d$). Every frequency component of your signal (fundamental, harmonics, etc.) is delayed by the **exact same amount**. The signal shape remains identical.
    
- **If $\theta(f)$ is Non-Linear (Curved):** The derivative varies with $f$. High frequencies might be delayed more than low frequencies. The output signal becomes distorted (dispersed) because its components arrive at different times.
    

**Summary:** The dotted line represents the requirement for **Linear Phase**, which guarantees that the filter is **distortionless** in the time domain. It shifts the entire signal cleanly without scrambling its internal structure.