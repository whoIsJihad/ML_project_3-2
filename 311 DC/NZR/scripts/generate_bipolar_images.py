import matplotlib.pyplot as plt
import numpy as np

# Example bitstream
bits = [1,0,1,1,0,0,0,1]
T = 1.0  # duration per bit

# AMI encoding
def ami_wave(bits, V=1.0):
    last = -V
    levels = []
    for b in bits:
        if b==0:
            levels.append(0.0)
        else:
            # alternate polarity
            last = -last
            levels.append(last)
    return levels

# Pseudoternary encoding (0s alternate)
def pseudoternary_wave(bits, V=1.0):
    last = -V
    levels = []
    for b in bits:
        if b==1:
            levels.append(0.0)
        else:
            last = -last
            levels.append(last)
    return levels

# plotting helper
def plot_wave(levels, bits, title, fname):
    n = len(bits)
    t = np.arange(0, n*T, 0.001)
    y = np.zeros_like(t)
    for i, level in enumerate(levels):
        mask = (t >= i*T) & (t < (i+1)*T)
        y[mask] = level
    plt.figure(figsize=(8,2))
    plt.step(np.concatenate([np.arange(0,n+1)*T]), np.concatenate([levels+[levels[-1]]]), where='post')
    # annotate bits
    for i,b in enumerate(bits):
        plt.text(i*T + 0.2*T, 1.1*max(1.0, abs(max(levels))) if levels[i]!=0 else 0.2, str(b), fontsize=12)
    plt.ylim(-1.5,1.5)
    plt.xlim(0, n*T)
    plt.yticks([-1,0,1])
    plt.xlabel('Time (bit periods)')
    plt.title(title)
    plt.grid(False)
    plt.tight_layout()
    plt.savefig(fname, dpi=150)
    plt.close()

if __name__ == '__main__':
    ami = ami_wave(bits)
    pseudo = pseudoternary_wave(bits)
    plot_wave(ami, bits, 'AMI Encoding - example 10110001', '../images/note_ami_example.png')
    plot_wave(pseudo, bits, 'Pseudoternary Encoding - example 10110001', '../images/note_pseudoternary_example.png')
    print('Images saved to ../images/')