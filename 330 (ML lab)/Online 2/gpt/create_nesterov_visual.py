"""Create a simple visualization for Nesterov momentum."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import os

output_dir = "/mnt/Data/3-2/330 (ML lab)/Online 2/gpt"

def create_nesterov_visualization():
    """Create a step-by-step visualization of Nesterov momentum."""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Create a simple quadratic loss landscape
    x = np.linspace(-2, 2, 100)
    y = x**2  # Simple quadratic: minimum at x=0

    # Plot 1: The loss landscape
    axes[0,0].plot(x, y, 'k-', linewidth=2)
    axes[0,0].set_title('Loss Landscape: L(w) = w²\nMinimum at w=0', fontsize=12, fontweight='bold')
    axes[0,0].set_xlabel('Parameter w')
    axes[0,0].set_ylabel('Loss')
    axes[0,0].grid(True, alpha=0.3)
    axes[0,0].axvline(x=0, color='red', linestyle='--', alpha=0.7, label='Minimum')
    axes[0,0].legend()

    # Plot 2: Standard Momentum Step-by-Step
    w_start = 1.5
    alpha = 0.1
    beta = 0.9

    # Standard momentum trajectory
    w_std = [w_start]
    velocity_std = 0

    for i in range(8):
        grad = 2 * w_std[-1]  # derivative of w² is 2w
        velocity_std = beta * velocity_std + grad
        w_new = w_std[-1] - alpha * velocity_std
        w_std.append(w_new)

    axes[0,1].plot(x, y, 'k-', linewidth=2, alpha=0.3)
    axes[0,1].plot(w_std, [w**2 for w in w_std], 'ro-', markersize=6, linewidth=2,
                   label='Standard Momentum Path')
    axes[0,1].set_title('Standard Momentum: Look at current position', fontsize=12, fontweight='bold')
    axes[0,1].set_xlabel('Parameter w')
    axes[0,1].set_ylabel('Loss')
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].legend()

    # Plot 3: Nesterov Momentum Step-by-Step
    w_nest = [w_start]
    velocity_nest = 0

    for i in range(8):
        # Look ahead: where would momentum take us?
        look_ahead = w_nest[-1] - alpha * beta * velocity_nest
        grad_ahead = 2 * look_ahead  # gradient at look-ahead position
        velocity_nest = beta * velocity_nest + grad_ahead
        w_new = w_nest[-1] - alpha * velocity_nest
        w_nest.append(w_new)

    axes[1,0].plot(x, y, 'k-', linewidth=2, alpha=0.3)
    axes[1,0].plot(w_nest, [w**2 for w in w_nest], 'bo-', markersize=6, linewidth=2,
                   label='Nesterov Momentum Path')
    axes[1,0].set_title('Nesterov Momentum: Look ahead first', fontsize=12, fontweight='bold')
    axes[1,0].set_xlabel('Parameter w')
    axes[1,0].set_ylabel('Loss')
    axes[1,0].grid(True, alpha=0.3)
    axes[1,0].legend()

    # Plot 4: Comparison
    axes[1,1].plot(range(len(w_std)), w_std, 'ro-', label='Standard Momentum', markersize=6, linewidth=2)
    axes[1,1].plot(range(len(w_nest)), w_nest, 'bo-', label='Nesterov Momentum', markersize=6, linewidth=2)
    axes[1,1].axhline(y=0, color='red', linestyle='--', alpha=0.7, label='Target (w=0)')
    axes[1,1].set_title('Comparison: Which reaches minimum faster?', fontsize=12, fontweight='bold')
    axes[1,1].set_xlabel('Iteration')
    axes[1,1].set_ylabel('Parameter w')
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)

    # Add text annotations
    axes[1,1].text(2, 0.8, 'Nesterov gets\ncloser to target\nfaster!', fontsize=10,
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    plt.suptitle('Nesterov Momentum: Look Ahead Before You Leap', fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'nesterov_explanation.png'), dpi=150, bbox_inches='tight')
    print("✓ Generated: nesterov_explanation.png")
    plt.close()


def create_nesterov_step_by_step():
    """Create a detailed step-by-step numerical example."""

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')

    # Title
    title = "Nesterov Momentum: Step-by-Step with Numbers"
    ax.text(0.5, 0.95, title, ha='center', fontsize=14, fontweight='bold',
            transform=ax.transAxes)

    # Step by step explanation
    y_pos = 0.85
    line_height = 0.05

    steps = [
        ("Starting point:", ""),
        ("  Current weight: w = 1.0", "We're at w=1.0, loss = 1.0² = 1.0"),
        ("  Current velocity: v = 0.0", "No momentum yet"),
        ("  Learning rate: α = 0.1", ""),
        ("  Momentum: β = 0.9", ""),
        ("", ""),
        ("Standard Momentum would do:", ""),
        ("  1. Look at current position: gradient = 2×1.0 = 2.0", ""),
        ("  2. Update velocity: v = 0.9×0 + 2.0 = 2.0", ""),
        ("  3. Move: w = 1.0 - 0.1×2.0 = 0.8", ""),
        ("", ""),
        ("Nesterov Momentum does:", ""),
        ("  1. Look AHEAD: where would momentum take us?", ""),
        ("     look_ahead = w - α×β×v = 1.0 - 0.1×0.9×0 = 1.0", "Since v=0, look_ahead = current position"),
        ("  2. Get gradient at look-ahead position: grad_ahead = 2×1.0 = 2.0", ""),
        ("  3. Update velocity: v = 0.9×0 + 2.0 = 2.0", ""),
        ("  4. Move: w = 1.0 - 0.1×2.0 = 0.8", "Same as standard momentum (first step)"),
        ("", ""),
        ("Now iteration 2 - where they differ:", ""),
        ("", ""),
        ("Standard Momentum (iteration 2):", ""),
        ("  Current w = 0.8, gradient = 2×0.8 = 1.6", ""),
        ("  v = 0.9×2.0 + 1.6 = 1.8 + 1.6 = 3.4", ""),
        ("  w = 0.8 - 0.1×3.4 = 0.46", ""),
        ("", ""),
        ("Nesterov Momentum (iteration 2):", ""),
        ("  Look AHEAD: look_ahead = 0.8 - 0.1×0.9×2.0 = 0.8 - 0.18 = 0.62", ""),
        ("  Gradient at look-ahead: grad_ahead = 2×0.62 = 1.24", ""),
        ("  v = 0.9×2.0 + 1.24 = 1.8 + 1.24 = 3.04", ""),
        ("  w = 0.8 - 0.1×3.04 = 0.496", ""),
        ("", ""),
        ("Key Difference:", ""),
        ("  Standard: Uses gradient at current position (1.6)", ""),
        ("  Nesterov: Uses gradient at look-ahead position (1.24)", ""),
        ("  Result: Nesterov moves less aggressively (0.496 vs 0.46)", ""),
        ("  Why? It 'sees' that moving too fast would overshoot!", ""),
    ]

    for i, (text, note) in enumerate(steps):
        y = y_pos - i * line_height

        if text == "":
            continue

        if note == "":  # Headers
            ax.text(0.05, y, text, fontsize=11, fontweight='bold',
                   transform=ax.transAxes, color='darkblue')
        else:  # Details
            ax.text(0.08, y, text, fontsize=9, transform=ax.transAxes,
                   family='monospace', bbox=dict(boxstyle='round,pad=0.3',
                   facecolor='lightyellow', alpha=0.8))
            ax.text(0.75, y, note, fontsize=8, transform=ax.transAxes,
                   color='darkred', style='italic')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'nesterov_step_by_step.png'), dpi=150, bbox_inches='tight')
    print("✓ Generated: nesterov_step_by_step.png")
    plt.close()


if __name__ == "__main__":
    print("Creating Nesterov momentum visualizations...")
    create_nesterov_visualization()
    create_nesterov_step_by_step()
    print("\n✅ Nesterov visualizations complete!")
