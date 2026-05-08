import matplotlib.pyplot as plt

# ------------------ DATA ------------------
bit_stream = [1, 0, 1, 1, 0, 0, 0, 1]
Tb = 1  # bit duration (normalized)

# ------------------ SIGNAL GENERATION ------------------
time = []
signal = []

current_time = 0
for bit in bit_stream:
    time.extend([current_time, current_time + Tb])
    if bit == 1:
        signal.extend([1, 1])   # +V
    else:
        signal.extend([0, 0])   # 0V
    current_time += Tb

# ------------------ PLOTTING ------------------
plt.figure(figsize=(10, 4))
plt.step(time, signal, where='post')
plt.ylim(-0.5, 1.5)
plt.xlim(0, len(bit_stream))
plt.xlabel("Time (in bit periods Tb)")
plt.ylabel("Voltage Level")
plt.title("NRZ Line Coding: 1 Signal Element per Data Element")

# Bit separators
for i in range(len(bit_stream) + 1):
    plt.axvline(i, linestyle='--', linewidth=0.8)

# Bit labels
for i, bit in enumerate(bit_stream):
    plt.text(i + 0.5, 1.2, str(bit), ha='center')

plt.tight_layout()
plt.savefig("line_coding_nrz_example.png", dpi=200)
plt.show()
