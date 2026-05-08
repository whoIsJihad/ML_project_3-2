import matplotlib.pyplot as plt
import numpy as np

# Manchester encoding for alternating bits: 1010
bit_stream = [1, 0, 1, 0]
Tb = 1
V = 1
samples_per_half = 100
signal = []
time = []
current_time = 0
for bit in bit_stream:
    if bit == 1:
        signal.extend([-V]*samples_per_half)
    else:
        signal.extend([V]*samples_per_half)
    time.extend(np.linspace(current_time, current_time+Tb/2, samples_per_half, endpoint=False))
    current_time += Tb/2
    if bit == 1:
        signal.extend([V]*samples_per_half)
    else:
        signal.extend([-V]*samples_per_half)
    time.extend(np.linspace(current_time, current_time+Tb/2, samples_per_half, endpoint=False))
    current_time += Tb/2
plt.figure(figsize=(8, 4))
plt.plot(time, signal, drawstyle='steps-post', linewidth=2)
plt.xlabel("Time (T_b)")
plt.ylabel("Voltage")
plt.title("Manchester Encoding: Bit Stream 1010")
plt.yticks([-1, 0, 1], ['-V', '0V', '+V'])
for i in range(len(bit_stream) + 1):
    plt.axvline(i * Tb, linestyle='--', linewidth=0.8, color='gray')
for i, bit in enumerate(bit_stream):
    plt.text(i * Tb + Tb / 2, 1.2, str(bit), ha='center', va='bottom', fontsize=12)
plt.ylim(-1.5, 1.5)
plt.xlim(0, len(bit_stream) * Tb)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("manchester_1010.png", dpi=200)
# plt.show()