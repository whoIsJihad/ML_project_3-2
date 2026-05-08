import matplotlib.pyplot as plt

# Polar NRZ-L for DC case 2: 1111000
bit_stream = [1, 1, 1, 1, 0, 0, 0]
Tb = 1  # bit duration

# Generate time and signal
time = []
signal = []
current_time = 0

for bit in bit_stream:
    time.extend([current_time, current_time + Tb])
    voltage = 1 if bit == 1 else -1
    signal.extend([voltage, voltage])
    current_time += Tb

# Plotting
plt.figure(figsize=(10, 4))
plt.step(time, signal, where='post', linewidth=2)

# Labels
plt.xlabel("Time (T_b)")
plt.ylabel("Voltage")
plt.title("Polar NRZ-L: Unbalanced Data '1111000' (DC ≈ 0.143V)")

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
plt.savefig("note_11_dc2.png", dpi=200)
# plt.show()