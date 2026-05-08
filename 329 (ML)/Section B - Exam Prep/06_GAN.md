# 📘 Generative Adversarial Networks (GAN)

## 1. Core Idea (Intuition)

**Problem:** How to generate new data (images, text) without explicit probability model?

**GAN solution:** Two networks compete:
- **Generator $G$:** Creates fake data from noise
- **Discriminator $D$:** Distinguishes real from fake

**Game theory:** Both optimize simultaneously; equilibrium produces realistic data.

---

## 2. Architecture

### Generator
Takes random noise $z \sim \mathcal{N}(0, 1)$:
$$G(z) = \text{neural network}(z) \to \text{fake image}$$

### Discriminator
Classifies real vs. fake:
$$D(x) = \text{neural network}(x) \to P(\text{real})$$

---

## 3. Training (Adversarial Loss)

### Minimax Game
$$\min_G \max_D \mathbb{E}_{x \sim p_{data}}[\log D(x)] + \mathbb{E}_{z \sim p_z}[\log(1 - D(G(z)))]$$

### Interpretation
**Discriminator maximizes:**
- $\log D(x)$ for real data (output 1)
- $\log(1 - D(G(z)))$ for fake data (output 0)

**Generator minimizes:**
- $\log(1 - D(G(z)))$ — make fake look real

### Practical Training
```
For each iteration:
  
  === Discriminator step ===
  1. Sample real batch x
  2. Sample fake batch z → G(z)
  3. Maximize: D(x) close to 1, D(G(z)) close to 0
  
  === Generator step ===
  1. Sample noise z
  2. Minimize: D(G(z)) close to 0 (or maximize: close to 1)
```

---

## 4. Nash Equilibrium

At equilibrium:
- $D$ cannot distinguish real from fake: $D(x) = 0.5$
- $G$ generates realistic data: $G(z) \sim p_{data}$

**Why it works:** Both players can't improve further.

---

## 5. Common Issues

| Problem | Why | Fix |
|---------|-----|-----|
| **Mode collapse** | Generator outputs limited variety | Minibatch discrimination, feature matching |
| **Vanishing gradients** | If $D$ too good, gradient to $G$ is zero | Use alternative loss (Wasserstein GAN) |
| **Training instability** | Simultaneous optimization is hard | Spectral normalization, gradient penalty |
| **Slow convergence** | High-dimensional generation hard | Progressive growing, style-based GAN |

---

## 6. GAN Variants

| Variant | Improvement |
|---------|-----------|
| **DCGAN** | CNN-based; convolutional for images |
| **Wasserstein GAN (WGAN)** | Better gradient flow; more stable |
| **Conditional GAN (cGAN)** | Class-conditional generation (e.g., "generate dog" not just random) |
| **StyleGAN** | Disentangled style and content |
| **Diffusion Models** | Alternative to GANs; more stable (modern trend) |

---

## 7. Applications

- **Image synthesis:** Generate realistic faces, objects
- **Style transfer:** Transfer artistic style between images
- **Data augmentation:** Generate synthetic training data
- **Domain adaptation:** Generate synthetic domain-shifted data
- **Super-resolution:** Enhance low-res images

---

## 8. Exam Questions

### Conceptual
1. Why is GAN called "adversarial"? Explain the game theory.
2. What is mode collapse? Why does it happen?
3. How is discriminator's loss different from generator's?

### Practical
1. Design cGAN for digit generation (condition on digit class 0-9).
2. GAN training oscillates (loss unstable). Suggest fixes.

### Trick Cases
1. Discriminator loss reaches zero (perfect classification). Generator learns nothing. Why?
2. Generator always produces same image (mode collapse). How to diagnose?

---

## 9. Key Takeaways

- **GAN:** Generator ($G$) vs. Discriminator ($D$) compete
- **Loss:** $\min_G \max_D \mathbb{E}[\log D(x) + \log(1 - D(G(z)))]$ (minimax game)
- **Nash equilibrium:** Discriminator cannot distinguish; generator matches data distribution
- **Mode collapse:** Generator avoids diversity; produces limited variety
- **Vanishing gradients:** If $D$ too strong, gradient to $G$ vanishes
- **Variants:** DCGAN (CNN), WGAN (stable), cGAN (conditional), StyleGAN (style)
- **Modern trend:** Diffusion models often preferred (more stable, better quality)

---
