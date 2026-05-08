import numpy as np
import matplotlib.pyplot as plt

# Generate a random bit stream for Polar NRZ-L
np.random.seed(42)  # For reproducibility
num_bits = 100
bit_stream = np.random.randint(0, 2, num_bits)

# Parameters
Tb = 1  # bit duration
fs = 100  # sampling frequency (samples per second)
samples_per_bit = int(fs * Tb)
total_samples = num_bits * samples_per_bit

# Generate signal for Polar NRZ-L: 1 -> +1, 0 -> -1
signal = np.zeros(total_samples)
for i, bit in enumerate(bit_stream):
    start = i * samples_per_bit
    end = (i + 1) * samples_per_bit
    signal[start:end] = 1 if bit == 1 else -1  # +1 or -1

# Compute FFT
fft = np.fft.fft(signal)
freqs = np.fft.fftfreq(total_samples, 1/fs)
power = np.abs(fft)**2

# Only positive frequencies
positive_freqs = freqs[:total_samples//2]
positive_power = power[:total_samples//2]

# Normalize
positive_power /= np.max(positive_power)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(positive_freqs, 10 * np.log10(positive_power + 1e-10), linewidth=2)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density (dB)')
plt.title('Polar NRZ-L Frequency Spectrum (Random Data)')
plt.grid(True, alpha=0.3)
plt.xlim(0, 2 / Tb)  # Up to 2 * bit rate
plt.axvline(1/Tb, linestyle='--', color='red', label='Bit Rate')
plt.axvline(0.5/Tb, linestyle='--', color='blue', label='Bit Rate / 2')
plt.legend()
plt.tight_layout()
plt.savefig("note_11_spectrum.png", dpi=200)
# plt.show()  # Commented out to avoid display issues