import matplotlib.pyplot as plt

# Polar NRZ-L Encoding for bit stream 10110001
bit_stream = [1, 0, 1, 1, 0, 0, 0, 1]
Tb = 1  # bit duration

# Generate time and signal
time = []
signal = []
current_time = 0

for bit in bit_stream:
    time.extend([current_time, current_time + Tb])
    voltage = 1 if bit == 1 else -1  # +1 for 1, -1 for 0
    signal.extend([voltage, voltage])
    current_time += Tb

# Plotting
plt.figure(figsize=(12, 4))
plt.step(time, signal, where='post', linewidth=2)

# Labels
plt.xlabel("Time (T_b)")
plt.ylabel("Voltage")
plt.title("Polar NRZ-L Encoding: Bit Stream 10110001")

# Voltage levels
plt.yticks([-1, 0, 1], ['-V', '0V', '+V'])

# Bit separators
for i in range(len(bit_stream) + 1):
    plt.axvline(i * Tb, linestyle='--', linewidth=0.8, color='gray')

# Bit labels
for i, bit in enumerate(bit_stream):
    plt.text(i * Tb + Tb / 2, 1.2, str(bit), ha='center', va='bottom', fontsize=12)

plt.ylim(-1.5, 1.5)
plt.xlim(0, len(bit_stream) * Tb)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("note_11.png", dpi=200)
# plt.show()  # Commented out to avoid display issues