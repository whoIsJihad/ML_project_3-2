## 5. Fourier Series Example: The Square Wave (with Python Code)

A concrete example is the best way to understand the power and behavior of the Fourier Series. We will derive the series for a simple square wave and then use a Python script to visualize how the sum of sinusoids approximates the wave.

### The Signal: A Square Wave

Let's define a periodic square wave $x(t)$ with the following characteristics:
*   **Amplitude:** 1
*   **Fundamental Period ($T_0$):** 2 seconds
*   **Fundamental Angular Frequency ($\omega_0$):** $2\pi / T_0 = \pi$ rad/s

The signal is defined over one period as:
$$ x(t) = \begin{cases} 1 & \text{for } 0 \le t < 1 \\ 0 & \text{for } 1 \le t < 2 \end{cases} $$

Our goal is to find the Fourier Series representation:
$$ x(t) = a_0 + \sum_{n=1}^{\infty} \left( a_n \cos(n\omega_0 t) + b_n \sin(n\omega_0 t) \right) $$

### Step 1: Calculate the DC Coefficient ($a_0$)

The DC coefficient is the average value of the signal over one period.
$$ a_0 = \frac{1}{T_0} \int_{0}^{T_0} x(t) \, dt = \frac{1}{2} \int_{0}^{2} x(t) \, dt $$
Since the signal is 0 for the second half of the period, the integral simplifies:
$$ a_0 = \frac{1}{2} \int_{0}^{1} 1 \, dt = \frac{1}{2} [t]_{0}^{1} = \frac{1}{2}(1 - 0) = \frac{1}{2} $$
The average value of the wave is 0.5.

### Step 2: Calculate the Cosine Coefficients ($a_n$)

Next, we find the coefficients for the cosine terms.
$$ a_n = \frac{2}{T_0} \int_{0}^{T_0} x(t) \cos(n\omega_0 t) \, dt = \frac{2}{2} \int_{0}^{1} 1 \cdot \cos(n\pi t) \, dt $$
$$ a_n = \left[ \frac{1}{n\pi} \sin(n\pi t) \right]_{0}^{1} = \frac{1}{n\pi}(\sin(n\pi) - \sin(0)) $$
Because $\sin(n\pi) = 0$ for any integer $n$, and $\sin(0) = 0$:
$$ a_n = 0 \quad \text{for all } n \ge 1 $$
This means there are no cosine components in the series for this particular signal.

### Step 3: Calculate the Sine Coefficients ($b_n$)

Now we find the coefficients for the sine terms.
$$ b_n = \frac{2}{T_0} \int_{0}^{T_0} x(t) \sin(n\omega_0 t) \, dt = \int_{0}^{1} 1 \cdot \sin(n\pi t) \, dt $$
$$ b_n = \left[ -\frac{1}{n\pi} \cos(n\pi t) \right]_{0}^{1} = -\frac{1}{n\pi}(\cos(n\pi) - \cos(0)) $$
We know that $\cos(0) = 1$ and $\cos(n\pi)$ alternates: it is -1 for odd $n$ and +1 for even $n$. We can write this as $\cos(n\pi) = (-1)^n$.
$$ b_n = -\frac{1}{n\pi}((-1)^n - 1) $$
Let's evaluate this for even and odd $n$:
*   If $n$ is **even** ($n=2, 4, \dots$): $b_n = -\frac{1}{n\pi}(1 - 1) = 0$.
*   If $n$ is **odd** ($n=1, 3, \dots$): $b_n = -\frac{1}{n\pi}(-1 - 1) = -\frac{1}{n\pi}(-2) = \frac{2}{n\pi}$.

So, only the sine terms of the odd harmonics are present in this signal.

### Step 4: The Final Fourier Series

We can now write the complete Fourier Series for our square wave:
$$ x(t) = a_0 + \sum_{n=1,3,5,\dots}^{\infty} b_n \sin(n\pi t) $$
$$ x(t) = \frac{1}{2} + \frac{2}{\pi}\sin(\pi t) + \frac{2}{3\pi}\sin(3\pi t) + \frac{2}{5\pi}\sin(5\pi t) + \dots $$
This demonstrates that a discontinuous square wave can be perfectly represented by a sum of continuous sine waves.

### Python Code for Visualization

The following Python script will plot the square wave and its Fourier Series approximation for an increasing number of harmonics. To run it, you need `numpy` and `matplotlib` installed (`pip install numpy matplotlib`).

```python
import numpy as np
import matplotlib.pyplot as plt

# Define the parameters
T0 = 2.0  # Period
w0 = np.pi # Fundamental angular frequency (2*pi/T0)
a0 = 0.5   # DC component

# --- Functions to build the series ---

def bn_coeff(n):
    """Calculates the b_n coefficient for a given odd n."""
    if n % 2 == 0:
        return 0
    return 2 / (n * np.pi)

def fourier_series_approximation(t, num_harmonics):
    """
    Calculates the Fourier series approximation of the square wave
    for a given time array 't' and number of harmonics 'num_harmonics'.
    """
    # Start with the DC offset
    series_sum = np.full_like(t, a0)
    # Add the sinusoidal terms
    for n in range(1, num_harmonics + 1):
        if n % 2 != 0: # Only odd harmonics
            b = bn_coeff(n)
            series_sum += b * np.sin(n * w0 * t)
    return series_sum

# --- Plotting ---

# Create the time array for plotting (2 periods)
t = np.linspace(0, 4, 1000)

# Create the ideal square wave for plotting
def ideal_square_wave(t):
    return a0 + 0.5 * np.sign(np.sin(w0 * t))

# Number of harmonics to plot
harmonics_to_plot = [1, 3, 7, 100]

plt.figure(figsize=(12, 8))

# Plot the ideal square wave
plt.plot(t, ideal_square_wave(t), 'k--', label='Ideal Square Wave', linewidth=2)

# Plot the Fourier approximations
for N in harmonics_to_plot:
    y = fourier_series_approximation(t, N)
    plt.plot(t, y, label=f'N = {N} Harmonics')

# --- Formatting the plot ---
plt.title('Fourier Series Approximation of a Square Wave', fontsize=16)
plt.xlabel('Time (t)', fontsize=12)
plt.ylabel('x(t)', fontsize=12)
plt.legend()
plt.grid(True)
plt.ylim(-0.2, 1.2)
plt.show()

```

### Visualization and Gibbs Phenomenon

When you run the script, you will see how the approximation gets closer to the ideal square wave as more harmonics are added. You will also notice that near the points of discontinuity (at $t=0, 1, 2, \dots$), the series overshoots the target value of 1 and undershoots 0. This consistent overshooting, even as the number of harmonics approaches infinity, is a famous effect known as the **Gibbs Phenomenon**.

#### Next : [[06 - Fourier Series of Impulse Train]]