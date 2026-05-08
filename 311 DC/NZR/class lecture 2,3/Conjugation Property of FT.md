# Conjugation Property of Fourier Transform

The **conjugate symmetry property** states that if a signal $x(t)$ is real-valued and has Fourier Transform $X(\omega)$, then:

$$
X(-\omega) = X^*(\omega)
$$

This is called **conjugate symmetry**.

---

## 1. ⚙️ Meaning of Terms

- $X(\omega)$: Fourier Transform (complex-valued)
- $X(-\omega)$: spectrum at negative frequency
- $X^*(\omega)$: complex conjugate (flips sign of imaginary part)

---

## 2. 📝 Derivation Sketch

CTFT definition:

$$
X(\omega) = \int_{-\infty}^{\infty} x(t)e^{-j\omega t} dt
$$

### Step 1: Negative frequency

$$
X(-\omega) = \int_{-\infty}^{\infty} x(t)e^{j\omega t} dt
$$

---

### Step 2: Complex conjugate

$$
X^*(\omega) =
\left(\int_{-\infty}^{\infty} x(t)e^{-j\omega t} dt\right)^*
$$

Taking conjugate inside:

$$
X^*(\omega) = \int_{-\infty}^{\infty} x^*(t)e^{j\omega t} dt
$$

Since $x(t)$ is real:

$$
x^*(t) = x(t)
$$

So:

$$
X^*(\omega) = \int_{-\infty}^{\infty} x(t)e^{j\omega t} dt
$$

---

### Step 3: Compare

$$
X(-\omega) = X^*(\omega)
$$

---

## 3. ✨ Implications

### Magnitude (Even)

$$
|X(-\omega)| = |X(\omega)|
$$

---

### Phase (Odd)

$$
\angle X(-\omega) = -\angle X(\omega)
$$

---

### Real Part (Even)

$$
\mathrm{Re}\{X(-\omega)\} = \mathrm{Re}\{X(\omega)\}
$$

---

### Imaginary Part (Odd)

$$
\mathrm{Im}\{X(-\omega)\} = -\mathrm{Im}\{X(\omega)\}
$$

---

## 🔑 Key Insight

For real-valued signals, the negative-frequency spectrum contains no new information. It is completely determined by the positive-frequency spectrum.