import matplotlib.pyplot as plt

# 2B1Q Encoding mapping
encoding = {
    '00': -3,
    '01': -1,
    '10': 1,
    '11': 3
}

# Example bit stream: 10 11 00 01
bit_pairs = ['10', '11', '00', '01']
Ts = 1  # symbol duration

# Generate time and signal
time = []
signal = []
current_time = 0

for pair in bit_pairs:
    voltage = encoding[pair]
    time.extend([current_time, current_time + Ts])
    signal.extend([voltage, voltage])
    current_time += Ts

# Plotting
plt.figure(figsize=(10, 6))
plt.step(time, signal, where='post', linewidth=2)

# Set y-ticks for voltage levels
plt.yticks([-3, -1, 0, 1, 3], ['-3V', '-V', '0', '+V', '+3V'])

# Labels and title
plt.xlabel("Time (T_s)")
plt.ylabel("Voltage Level")
plt.title("2B1Q Line Coding Example: 10 11 00 01")

# Vertical lines for symbol boundaries
for i in range(len(bit_pairs) + 1):
    plt.axvline(i * Ts, linestyle='--', linewidth=0.8, color='gray')

# Label the symbols
for i, pair in enumerate(bit_pairs):
    plt.text(i * Ts + Ts / 2, 3.5, pair, ha='center', va='bottom', fontsize=12)

plt.ylim(-4, 4)
plt.xlim(0, len(bit_pairs) * Ts)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("note_04.png", dpi=200)
plt.show()