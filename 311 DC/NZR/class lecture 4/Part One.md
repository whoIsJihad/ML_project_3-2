

### 1. 🎛️ Linear Time-Invariant (LTI) System Properties

The top block diagram illustrates the two core properties that define an LTI system:

- **Linearity (Superposition):** If input $x_1(t)$ gives output $y_1(t)$ and $x_2(t)$ gives $y_2(t)$, then a combined input $a_1x_1(t) + a_2x_2(t)$ produces a combined output $a_1y_1(t) + a_2y_2(t)$.
    
- **Time-Invariance:** If you delay the input by time $t_a$ (i.e., $x(t-t_a)$), the output is simply delayed by the same amount $y(t-t_a)$ without changing shape.
    

### 2. 🌊 Impulse Response $h(t)$

- **Definition:** $h(t)$ is the output of the LTI system when the input is a unit impulse function $\delta(t)$ (a momentary "kick" at $t=0$).
    
- **Role:** $h(t)$ completely characterizes the LTI system. If you know $h(t)$, you can calculate the response to _any_ input.
    

### 3. 🌀 Convolution in Time Domain

The notes show the relationship between input $x(t)$, impulse response $h(t)$, and output $y(t)$:

- **Formula:** $y(t) = x(t) * h(t)$
    
- Integral Definition: The handwritten math defines the convolution integral:
    
    $$g_1(t) * g_2(t) = \int_{-\infty}^{\infty} g_1(\tau) g_2(t-\tau) d\tau$$
    
    This operation effectively "slides" one function over the other, multiplies them, and integrates the area.
    

### 4. 🔄 Commutative Property (Proof)

The notes demonstrate that the order of convolution doesn't matter (i.e., $g_1 * g_2 = g_2 * g_1$).

- **The Proof shown:**
    
    1. Start with $\int_{-\infty}^{\infty} g_1(\tau) g_2(t-\tau) d\tau$.
        
    2. Apply a variable change (likely $u = t - \tau$).
        
    3. The result becomes $\int_{-\infty}^{\infty} g_2(u) g_1(t-u) du$.
        
    4. This proves that $g_1(t) * g_2(t) = g_2(t) * g_1(t)$.
        

### 5. 📉 Frequency Domain & Transfer Function

The diagram shows that convolution in time becomes simple multiplication in frequency:

- Transfer Function $H(f)$: This is the Fourier Transform of the impulse response $h(t)$.
    
    $$Y(f) = H(f) \times X(f)$$
    
- Magnitude & Phase: Since $H(f)$ is complex, it is split into polar form:
    
    $$H(f) = |H(f)| e^{j\theta(f)}$$
    
    - $|H(f)|$: **Amplitude Response** (or Gain). Shows how much the system amplifies/attenuates each frequency.
        
    - $\theta(f)$ (or $\angle H(f)$): **Phase Response**. Shows the phase shift applied to each frequency.
        

