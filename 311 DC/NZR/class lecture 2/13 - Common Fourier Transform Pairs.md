## 13 - Common Fourier Transform Pairs (With Derivations)

- **Notation:** $x(t) \leftrightarrow X(f)$
    
- **Forward FT:**
    
    $$X(f) = \int_{-\infty}^{\infty} x(t) e^{-j2\pi f t} \, dt$$
    

---

### 1. The Dirac Delta Function (Impulse)

$$\delta(t) \quad \leftrightarrow \quad 1$$

- Derivation: Apply the sifting property $\int_{-\infty}^{\infty} g(t)\delta(t)dt = g(0)$ to the FT integral:
    
    $$X(f) = \int_{-\infty}^{\infty} \delta(t) e^{-j2\pi f t} \, dt = e^{-j2\pi f \cdot 0} = 1$$
    



---

### 2. The Constant (DC) Signal

$$1 \quad \leftrightarrow \quad \delta(f)$$

- **Derivation:** Use the **Duality Property**: If $x(t) \leftrightarrow X(f)$, then $X(t) \leftrightarrow x(-f)$.
    
    - Start with $\delta(t) \leftrightarrow 1$.
        
    - Set $X(t) = 1$. The dual transform is $x(-f) = \delta(-f)$.
        
    - Since $\delta(-f) = \delta(f)$, the pair is $1 \leftrightarrow \delta(f)$.
        

---

### 3. Shifted Dirac Delta Function

$$\delta(t - t_0) \quad \leftrightarrow \quad e^{-j2\pi f t_0}$$

- Derivation: Direct application of the sifting property $\int_{-\infty}^{\infty} g(t)\delta(t-t_0)dt = g(t_0)$:
    
    $$X(f) = \int_{-\infty}^{\infty} \delta(t - t_0) e^{-j2\pi f t} \, dt = e^{-j2\pi f t_0}$$
    

---

### 4. The Complex Exponential

$$e^{j2\pi f_0 t} \quad \leftrightarrow \quad \delta(f - f_0)$$

- **Derivation:** Use **Duality** on the shifted delta pair $\delta(t - t_a) \leftrightarrow e^{-j2\pi f t_a}$.
    
    - Set $X(t) = e^{-j2\pi t_a t}$. The dual is $x(-f) = \delta(-f - t_a) = \delta(f + t_a)$.
        
    - So, $e^{-j2\pi t_a t} \leftrightarrow \delta(f + t_a)$.
        
    - Let $f_0 = -t_a$ (so $t_a = -f_0$) to get the standard form:
        
        $$e^{j2\pi f_0 t} \quad \leftrightarrow \quad \delta(f - f_0)$$
        

---

### 5. Cosine and Sine Functions

$$\cos(2\pi f_0 t) \quad \leftrightarrow \quad \frac{1}{2}[\delta(f - f_0) + \delta(f + f_0)]$$

$$\sin(2\pi f_0 t) \quad \leftrightarrow \quad \frac{1}{2j}[\delta(f - f_0) - \delta(f + f_0)]$$

- **Derivation:** Use **Euler's identity** and **Linearity**.
    
    - $\cos(2\pi f_0 t) = \frac{1}{2}(e^{j2\pi f_0 t} + e^{-j2\pi f_0 t})$.
        
    - Using $\mathcal{F}\{e^{j2\pi f_0 t}\} = \delta(f - f_0)$:
        
        $$\mathcal{F}\{\cos(2\pi f_0 t)\} = \frac{1}{2} [\mathcal{F}\{e^{j2\pi f_0 t}\} + \mathcal{F}\{e^{j2\pi (-f_0) t}\}]$$
        
        $$= \frac{1}{2} [\delta(f-f_0) + \delta(f+f_0)]$$
        
    - The sine derivation is similar, using $\sin(\theta) = \frac{1}{2j}(e^{j\theta} - e^{-j\theta})$.
        


---

### 6. Decaying Exponential

$$e^{-at}u(t) \quad \leftrightarrow \quad \frac{1}{a + j2\pi f} \quad (a > 0)$$

- Derivation: Direct integration (since $u(t)$ sets the lower limit to 0).
    
    $$X(f) = \int_{0}^{\infty} e^{-at} e^{-j2\pi f t} \, dt = \int_{0}^{\infty} e^{-(a + j2\pi f)t} \, dt$$
    
    $$= \left[ \frac{e^{-(a + j2\pi f)t}}{-(a + j2\pi f)} \right]_{0}^{\infty} = 0 - \left( \frac{1}{-(a + j2\pi f)} \right) = \frac{1}{a + j2\pi f}$$
    

---

### 7. The Signum (Sign) Function

$$\text{sgn}(t) \quad \leftrightarrow \quad \frac{1}{j\pi f}$$

- **Derivation:** Use **Duality** on the known pair $\frac{1}{\pi t} \leftrightarrow -j \, \text{sgn}(f)$.
    
    - The dual pair is $-j \, \text{sgn}(t) \leftrightarrow \frac{1}{\pi(-f)} = -\frac{1}{\pi f}$.
        
    - Multiply both sides by $j$: $\text{sgn}(t) \leftrightarrow j\left(-\frac{1}{\pi f}\right) = \frac{-j}{\pi f}$.
        
    - Since $\frac{-j}{\pi f} = \frac{1}{j\pi f}$:
        
        $$\text{sgn}(t) \leftrightarrow \frac{1}{j\pi f}$$
        

---

### 8. The Unit Step Function

$$u(t) \quad \leftrightarrow \quad \frac{1}{2}\delta(f) + \frac{1}{j2\pi f}$$

- **Derivation:** Express $u(t)$ using the constant and signum functions: $u(t) = \frac{1}{2} + \frac{1}{2}\text{sgn}(t)$.
    
    - Apply Linearity and known transforms ($1 \leftrightarrow \delta(f)$ and $\text{sgn}(t) \leftrightarrow \frac{1}{j\pi f}$):
        
        $$\mathcal{F}\{u(t)\} = \frac{1}{2}\mathcal{F}\{1\} + \frac{1}{2}\mathcal{F}\{\text{sgn}(t)\}$$
        
        $$= \frac{1}{2}\delta(f) + \frac{1}{2}\left(\frac{1}{j\pi f}\right) = \frac{1}{2}\delta(f) + \frac{1}{j2\pi f}$$
        


---

