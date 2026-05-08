"""Generate professional visualizations for optimizer documentation."""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import os

output_dir = "/mnt/Data/3-2/330 (ML lab)/Online 2/gpt"

# ============================================================================
# 1. MOMENTUM EFFECT: Showing how velocity accumulates with concrete numbers
# ============================================================================
def generate_momentum_effect():
    """Show momentum accumulating: gradient bounces, velocity smooths."""
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Iteration count
    iterations = np.arange(0, 20)
    
    # Simulate gradient bouncing around
    np.random.seed(42)
    true_gradient = -0.1  # downhill direction
    gradient_noise = np.random.normal(0, 0.15, len(iterations))
    gradients = true_gradient + gradient_noise
    
    # Vanilla SGD: just follow gradient
    w_vanilla = np.zeros(len(iterations))
    w_vanilla[0] = 10.0
    for i in range(1, len(iterations)):
        w_vanilla[i] = w_vanilla[i-1] - 0.5 * gradients[i-1]
    
    # Momentum: accumulate direction
    velocity = 0
    w_momentum = np.zeros(len(iterations))
    w_momentum[0] = 10.0
    beta = 0.9
    for i in range(1, len(iterations)):
        velocity = beta * velocity + gradients[i-1]
        w_momentum[i] = w_momentum[i-1] - 0.5 * velocity
    
    # Plot 1: The actual gradients (noisy)
    ax1.plot(iterations, gradients, 'o-', label='Actual gradient (noisy)', 
             color='red', linewidth=2, markersize=6, alpha=0.7)
    ax1.axhline(y=true_gradient, color='darkred', linestyle='--', 
                label='True direction', linewidth=2)
    ax1.set_xlabel('Iteration', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Gradient value', fontsize=12, fontweight='bold')
    ax1.set_title('Problem: Gradient bounces around (noisy batches)', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Parameter values
    ax2.plot(iterations, w_vanilla, 'o-', label='Vanilla SGD (follows noisy gradient)', 
             color='red', linewidth=2.5, markersize=5, alpha=0.8)
    ax2.plot(iterations, w_momentum, 's-', label='Momentum (remembers direction)', 
             color='green', linewidth=2.5, markersize=5, alpha=0.8)
    ax2.set_xlabel('Iteration', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Parameter value', fontsize=12, fontweight='bold')
    ax2.set_title('Result: Momentum path is smoother and reaches minimum faster', 
                  fontsize=13, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # Annotate the effect
    ax2.annotate('Bouncy path\n(loses time)', xy=(8, w_vanilla[8]), xytext=(12, 6),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=10, color='red', fontweight='bold')
    ax2.annotate('Smooth path\n(faster descent)', xy=(8, w_momentum[8]), xytext=(12, 8),
                arrowprops=dict(arrowstyle='->', color='green', lw=2),
                fontsize=10, color='green', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'momentum_effect.png'), dpi=150, bbox_inches='tight')
    print("✓ Generated: momentum_effect.png")
    plt.close()


# ============================================================================
# 2. CONCRETE NUMERICAL EXAMPLE: Step-by-step gradient descent
# ============================================================================
def generate_numerical_example():
    """Show step-by-step numbers: w_old=5, grad=0.2, alpha=0.1, then w_new=4.98"""
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    
    # Title
    title = "Concrete Numerical Example: One Step of Gradient Descent"
    ax.text(0.5, 0.95, title, ha='center', fontsize=14, fontweight='bold',
            transform=ax.transAxes)
    
    # Step by step
    y_pos = 0.85
    line_height = 0.08
    
    steps = [
        ("Iteration 5:", ""),
        ("  Current weight: w = 5.234", "The parameter we're trying to optimize"),
        ("  Current loss: L(w) = 2.156", "How wrong the model is"),
        ("", ""),
        ("Compute gradient:", ""),
        ("  ∂L/∂w = 0.347", "Loss increases when w increases (slope upward)"),
        ("", ""),
        ("Update rule: w_new = w_old - α × (∂L/∂w)", "Move OPPOSITE to gradient (downhill)"),
        ("", ""),
        ("Plug in numbers:", ""),
        ("  w_new = 5.234 - 0.1 × 0.347", "α=0.1 is our learning rate"),
        ("  w_new = 5.234 - 0.0347", "Multiply 0.1 × 0.347"),
        ("  w_new = 5.1993", "Subtract from current weight"),
        ("", ""),
        ("Result:", ""),
        ("  Weight changed from 5.234 → 5.1993 (decreased by 0.0347)", "Movement direction matches gradient sign"),
        ("  Loss should decrease slightly on next iteration", "If α is chosen well"),
    ]
    
    for i, (text, note) in enumerate(steps):
        y = y_pos - i * line_height
        
        if text == "":
            continue
        
        if note == "":  # Headers
            ax.text(0.05, y, text, fontsize=11, fontweight='bold', 
                   transform=ax.transAxes, color='darkblue')
        else:  # Details
            ax.text(0.08, y, text, fontsize=10, transform=ax.transAxes,
                   family='monospace', bbox=dict(boxstyle='round,pad=0.5', 
                   facecolor='lightyellow', alpha=0.8))
            ax.text(0.52, y, note, fontsize=9, transform=ax.transAxes,
                   color='darkred', style='italic')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'numerical_example.png'), dpi=150, bbox_inches='tight')
    print("✓ Generated: numerical_example.png")
    plt.close()


# ============================================================================
# 3. LEARNING RATE EFFECT: Too small, just right, too large (with numbers)
# ============================================================================
def generate_learning_rate_comparison():
    """Show three learning rates with actual convergence curves."""
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Simulate loss curves for different learning rates
    iterations = np.arange(0, 50)
    
    # Loss landscape: quadratic with some curvature
    loss_lr_small = 1.0 + 0.5 * np.exp(-0.05 * iterations)
    loss_lr_good = 1.0 + 0.5 * np.exp(-0.15 * iterations)
    loss_lr_large = 1.0 + 2.0 * np.sin(iterations * 0.2) * np.exp(-0.05 * iterations)
    
    # Plot 1: Too small
    axes[0].plot(iterations, loss_lr_small, 'o-', color='red', linewidth=2.5, markersize=4)
    axes[0].fill_between(iterations, loss_lr_small, alpha=0.2, color='red')
    axes[0].set_title('Learning Rate = 0.001\n(Too Small)', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Loss', fontsize=11, fontweight='bold')
    axes[0].set_xlabel('Iteration', fontsize=11, fontweight='bold')
    axes[0].text(25, 1.4, 'Problem: Takes forever\nto reach minimum', 
                ha='center', fontsize=10, color='red', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Just right
    axes[1].plot(iterations, loss_lr_good, 'o-', color='green', linewidth=2.5, markersize=4)
    axes[1].fill_between(iterations, loss_lr_good, alpha=0.2, color='green')
    axes[1].set_title('Learning Rate = 0.01\n(Just Right)', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Loss', fontsize=11, fontweight='bold')
    axes[1].set_xlabel('Iteration', fontsize=11, fontweight='bold')
    axes[1].text(25, 1.4, 'Perfect: Fast descent\nand stable', 
                ha='center', fontsize=10, color='green', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    axes[1].grid(True, alpha=0.3)
    
    # Plot 3: Too large
    axes[2].plot(iterations, loss_lr_large, 'o-', color='darkred', linewidth=2.5, markersize=4)
    axes[2].fill_between(iterations, loss_lr_large, alpha=0.2, color='darkred')
    axes[2].set_title('Learning Rate = 0.1\n(Too Large)', fontsize=12, fontweight='bold')
    axes[2].set_ylabel('Loss', fontsize=11, fontweight='bold')
    axes[2].set_xlabel('Iteration', fontsize=11, fontweight='bold')
    axes[2].text(25, 2.5, 'Problem: Bounces around\nor diverges', 
                ha='center', fontsize=10, color='darkred', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    axes[2].grid(True, alpha=0.3)
    
    # Align y-axes
    max_loss = max(loss_lr_small.max(), loss_lr_good.max(), loss_lr_large.max())
    for ax in axes:
        ax.set_ylim([0.5, max_loss * 1.1])
    
    plt.suptitle('Learning Rate Impact on Training', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'learning_rate_comparison.png'), dpi=150, bbox_inches='tight')
    print("✓ Generated: learning_rate_comparison.png")
    plt.close()


# ============================================================================
# 4. CONVERGENCE PATHS: Showing vanilla SGD vs Momentum on 2D loss landscape
# ============================================================================
def generate_convergence_paths():
    """Show how different optimizers navigate the loss landscape."""
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Create a simple 2D loss landscape
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = (X - 1)**2 + 3 * (Y - 1)**2  # Quadratic loss with minimum at (1, 1)
    
    # Plot contours
    contours = ax.contour(X, Y, Z, levels=15, colors='gray', alpha=0.5, linewidths=0.8)
    ax.clabel(contours, inline=True, fontsize=8)
    ax.contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.3)
    
    # Simulate paths
    np.random.seed(42)
    
    # Vanilla SGD path (bouncy)
    w_vanilla = np.array([[-2.5, -2.5]])
    for _ in range(30):
        grad_noise = np.random.normal(0, 0.15, 2)
        grad = 2 * (w_vanilla[-1] - np.array([1, 1])) + grad_noise
        w_vanilla = np.vstack([w_vanilla, w_vanilla[-1] - 0.3 * grad])
    
    # Momentum path (smooth)
    w_momentum = np.array([[-2.5, -2.5]])
    velocity = np.zeros(2)
    beta = 0.9
    for _ in range(30):
        grad_noise = np.random.normal(0, 0.15, 2)
        grad = 2 * (w_momentum[-1] - np.array([1, 1])) + grad_noise
        velocity = beta * velocity + grad
        w_momentum = np.vstack([w_momentum, w_momentum[-1] - 0.3 * velocity])
    
    # Plot paths
    ax.plot(w_vanilla[:, 0], w_vanilla[:, 1], 'o-', label='Vanilla SGD (bouncy)', 
           color='red', linewidth=2, markersize=4, alpha=0.8)
    ax.plot(w_momentum[:, 0], w_momentum[:, 1], 's-', label='Momentum (smooth)', 
           color='green', linewidth=2, markersize=4, alpha=0.8)
    
    # Mark start and minimum
    ax.plot(-2.5, -2.5, 'o', color='orange', markersize=15, label='Start', zorder=5)
    ax.plot(1, 1, '*', color='gold', markersize=25, label='Minimum', zorder=5)
    
    ax.set_xlabel('Parameter w₁', fontsize=12, fontweight='bold')
    ax.set_ylabel('Parameter w₂', fontsize=12, fontweight='bold')
    ax.set_title('How Optimizers Navigate Loss Landscape', fontsize=13, fontweight='bold')
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_xlim([-3, 2])
    ax.set_ylim([-3, 2])
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'convergence_paths.png'), dpi=150, bbox_inches='tight')
    print("✓ Generated: convergence_paths.png")
    plt.close()


# ============================================================================
# 5. ADAPTIVE LEARNING RATES: How Adam adjusts per-parameter
# ============================================================================
def generate_adam_adaptive_lr():
    """Show how Adam gives different step sizes to different parameters."""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    iterations = np.arange(1, 21)
    
    # Parameter 1: Large gradients
    grads_large = np.random.normal(-0.5, 0.1, len(iterations))
    
    # Parameter 2: Small gradients
    grads_small = np.random.normal(-0.05, 0.01, len(iterations))
    
    # Plot 1: Gradient magnitudes
    axes[0].bar(iterations - 0.2, np.abs(grads_large), width=0.4, 
               label='Parameter 1 (large gradients)', color='red', alpha=0.7)
    axes[0].bar(iterations + 0.2, np.abs(grads_small), width=0.4, 
               label='Parameter 2 (small gradients)', color='blue', alpha=0.7)
    axes[0].set_xlabel('Iteration', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('|Gradient|', fontsize=11, fontweight='bold')
    axes[0].set_title('Gradients: Different scales', fontsize=12, fontweight='bold')
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Effective learning rates (Adam)
    # Simulate squared gradient moving average
    v_large = np.zeros(len(iterations))
    v_small = np.zeros(len(iterations))
    beta2 = 0.999
    
    for i in range(len(iterations)):
        v_large[i] = beta2 * (v_large[i-1] if i > 0 else 0) + (1 - beta2) * grads_large[i]**2
        v_small[i] = beta2 * (v_small[i-1] if i > 0 else 0) + (1 - beta2) * grads_small[i]**2
    
    alpha_eff_large = 0.001 / (np.sqrt(v_large) + 1e-8)
    alpha_eff_small = 0.001 / (np.sqrt(v_small) + 1e-8)
    
    axes[1].plot(iterations, alpha_eff_large, 'o-', label='Parameter 1 (adaptive lr)', 
                color='red', linewidth=2.5, markersize=5)
    axes[1].plot(iterations, alpha_eff_small, 's-', label='Parameter 2 (adaptive lr)', 
                color='blue', linewidth=2.5, markersize=5)
    axes[1].set_xlabel('Iteration', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('Effective Learning Rate', fontsize=11, fontweight='bold')
    axes[1].set_title('Adam: Different step sizes per parameter', fontsize=12, fontweight='bold')
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    # Add annotation
    axes[1].text(10, max(alpha_eff_large) * 0.9, 
                'Large gradient → small lr\n(avoid overshoot)',
                fontsize=9, color='red', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    axes[1].text(10, min(alpha_eff_small) * 1.3,
                'Small gradient → large lr\n(faster descent)',
                fontsize=9, color='blue', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
    
    plt.suptitle('How Adam Adapts Learning Rate Per Parameter', 
                fontsize=13, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'adam_adaptive_lr.png'), dpi=150, bbox_inches='tight')
    print("✓ Generated: adam_adaptive_lr.png")
    plt.close()


# ============================================================================
# Generate all visualizations
# ============================================================================
if __name__ == "__main__":
    print("Generating professional visualizations...")
    generate_momentum_effect()
    generate_numerical_example()
    generate_learning_rate_comparison()
    generate_convergence_paths()
    generate_adam_adaptive_lr()
    print("\n✅ All visualizations generated successfully!")
