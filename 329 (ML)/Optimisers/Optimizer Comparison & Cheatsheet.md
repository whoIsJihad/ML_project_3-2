## Optimizer Comparison & Cheatsheet

A complete reference for choosing and tuning first-order optimizers in deep learning.

---

## 1. Complete Feature Comparison Table

| **Aspect** | **Vanilla SGD** | **Momentum** | **AdaGrad** | **RMSProp** | **Adam** |
|:---|:---|:---|:---|:---|:---|
| **Momentum** | ❌ No | ✅ Yes | ❌ No | ❌ No | ✅ Yes ($\\beta_1$) |
| **Adaptive LR** | ❌ No | ❌ No | ✅ Yes (Global Sum) | ✅ Yes (Moving Avg) | ✅ Yes ($\\beta_2$) |
| **Bias Correction** | N/A | N/A | N/A | N/A | ✅ Yes (Critical) |
| **Effective Memory** | 1 step | ~$\\frac{1}{1-\\beta}$ steps | Infinite | ~$\\frac{1}{1-\\beta}$ steps | ~10 (m), ~100 (v) |
| **Hyperparameters** | $\\eta$ only | $\\eta, \\beta$ | $\\eta$ only | $\\eta, \\beta$ | $\\eta, \\beta_1, \\beta_2$ |
| **Convergence Speed** | Slow | Medium | Fast (Early) | Fast | **Fastest** |
| **Memory Cost** | 1 copy | 1 copy | 1 copy | 1 copy | **2 copies** |
| **CPU/GPU Time** | 1x | 1.1x | 1.1x | 1.1x | 1.2x |
| **Default $\\eta$** | 0.01 | 0.01 | 0.1 | 0.001 | 0.001 |

---

## 2. Detailed Property Breakdown

### **Vanilla SGD**
-   **Best For:** Teaching, simple convex problems, when memory is extremely constrained.
-   **Pros:** Simplest, requires no extra memory, fast per-step.
-   **Cons:** Very slow convergence, sensitive to learning rate scaling, struggles on non-convex surfaces.
-   **Typical LR Schedule:** Decay by 0.1 every 10 epochs (e.g., $\\eta_t = \\eta_0 \times 0.1^{\\lfloor t/10 \\rfloor}$).

### **Momentum (SGD + Momentum)**
-   **Best For:** Standard supervised learning, when you want predictable, stable convergence.
-   **Pros:** Smooths gradient noise, slightly faster than SGD, escapes local minima better.
-   **Cons:** Still requires careful learning rate tuning, not adaptive.
-   **Default:** $\\beta = 0.9$ (sometimes 0.99).
-   **Typical LR Schedule:** Same as SGD or slightly more aggressive.

### **AdaGrad**
-   **Best For:** Sparse datasets (e.g., NLP embeddings, recommendation systems).
-   **Pros:** Rare features get larger updates; common features get smaller updates (natural scaling).
-   **Cons:** Learning rate shrinks indefinitely; **completely unusable after ~1000 steps** in deep learning.
-   **Intuition:** Infrequent features need to be learned from few examples, so give them preferential treatment.
-   **Rarely Used:** Replaced by RMSProp/Adam in modern deep learning.

### **RMSProp**
-   **Best For:** RNNs (historically popular), when you want adaptive LR without momentum, non-convex surfaces.
-   **Pros:** Prevents AdaGrad's learning rate collapse, stays responsive forever, less memory than Adam.
-   **Cons:** Two hyperparameters ($\\eta, \\beta$), slightly slower than Adam, no momentum.
-   **Default:** $\\beta = 0.9$ or $0.99$.
-   **When to Use Over Adam:** When you want simpler hyperparameter tuning (only $\\eta$ really matters after $\\beta$'s decay).

### **Adam**
-   **Best For:** Default choice for 95% of deep learning problems.
-   **Pros:** Combines momentum + adaptive LR, bias-corrected, hard to tune poorly, fast convergence.
-   **Cons:** More memory (stores 2 copies), **can overfit on small datasets**, sometimes worse generalization than SGD.
-   **Defaults:** $\\eta = 0.001$, $\\beta_1 = 0.9$, $\\beta_2 = 0.999$.
-   **When NOT to Use:** Very small datasets (< 5K), fine-tuning for production, safety-critical applications.

---

## 3. Decision Flowchart: Which Optimizer to Use?

```
START
│
├─ "Is this a RESEARCH PROTOTYPE or EXPERIMENT?"
│  ├─ YES → Use ADAM
│  │        (Fastest convergence, get results quickly)
│  │
│  └─ NO → "Is this PRODUCTION or a COMPETITION?"
│     ├─ YES → Go to STEP 2
│     └─ NO → Use ADAM (you're still experimenting)
│
STEP 2: "Is your dataset VERY SMALL (< 10K examples)?"
│
├─ YES → "Do you have COMPUTATIONAL CONSTRAINTS?"
│  ├─ YES → Use MOMENTUM
│  │        (Memory efficient, regularizing effect)
│  │
│  └─ NO → Use MOMENTUM or SGD
│          (Less prone to overfitting; slower but stable)
│
└─ NO → "Do you have SPARSE DATA (NLP embeddings, recommender systems)?"
   ├─ YES → "Are you using old code?"
   │  ├─ YES → Consider ADAGRAD
   │  └─ NO → Use ADAM (modern replacement)
   │
   └─ NO → "Is this FINE-TUNING a pretrained model?"
      ├─ YES → Use MOMENTUM or SGD
      │        (Stable, predictable; avoid Adam's aggressive adaptation)
      │
      └─ NO → Use ADAM (default choice)
              If convergence stalls → Switch to MOMENTUM
```

---

## 4. Quick-Reference Cheatsheet

### **Pick Your Optimizer in 30 Seconds**

| **Scenario** | **Optimizer** | **Learning Rate** | **Notes** |
|:---|:---|:---|:---|
| Deep Learning (CNN, Transformer, etc.) | Adam | Start: 0.001 | Tune if diverges: 0.0001 to 0.01 |
| RNN / Sequence Model | RMSProp or Adam | 0.001 | RMSProp was original choice; Adam is fine now |
| GAN Training | Adam | 0.0002 (very small!) | GANs are sensitive; use decay schedule |
| NLP Fine-tuning (BERT, GPT) | AdamW | 2e-5 | Always use **AdamW**, not Adam (weight decay!) |
| Computer Vision Fine-tuning | SGD + Momentum | 0.01 or lower | Step decay: $\times 0.1$ every 10 epochs |
| Small Dataset (< 10K) | SGD + Momentum | 0.01 | Implicit regularization; add explicit L2 if needed |
| Reinforcement Learning | Adam | 0.0003 | RL is unstable; sometimes use Momentum instead |
| Hyperparameter Search | Adam | 0.001 | Changes are less critical than architecture |
| Very Large Batch (> 10K) | SGD + Momentum | 0.1 or higher | Learning rate scales with batch size |
| Constrained Memory | SGD or Momentum | 0.01 | Only option; use learning rate scheduling |

---

## 5. Modern Variants: Beyond Adam

### **AdamW** ⭐ Recommended
-   **What:** Adam + **Decoupled Weight Decay** (instead of L2 regularization).
-   **Why:** Standard L2 in Adam doesn't work well (decays learning rate ineffectively). AdamW separates weight decay from gradient updates.
-   **When:** Always use for NLP (BERT, GPT fine-tuning). Optional but better for CNNs.
-   **Typical LR:** 1e-5 (NLP), 1e-4 (Vision).

### **AMSGrad**
-   **What:** Adam variant that uses $\max(v_1, v_2, \ldots, v_t)$ instead of $v_t$ to prevent learning rate collapse.
-   **Why:** Addresses rare case where Adam's learning rate shrinks too aggressively.
-   **When:** Almost never needed. Use if Adam's loss plateaus unexpectedly.
-   **Typical LR:** Same as Adam.

### **Adamax**
-   **What:** Adam but with $L^\\infty$ norm instead of $L^2$ (uses $\max$ instead of RMS for $v_t$).
-   **Why:** More robust to rare, large gradients.
-   **When:** Rarely used; Adam is almost always better.
-   **Typical LR:** 0.002.

### **Nadam** (Nesterov Adam)
-   **What:** Adam + Nesterov Momentum (lookahead instead of lag).
-   **Why:** Slightly faster than Adam.
-   **When:** Rarely used; marginal improvement; Adam is usually sufficient.
-   **Typical LR:** 0.002.

### **RAdam** (Rectified Adam)
-   **What:** Adam with "rectified" variance estimate to reduce variance in early training.
-   **Why:** Addresses Adam's potential instability in the first few steps.
-   **When:** Useful for very large models (> 1B parameters) or unstable training.
-   **Typical LR:** 0.001.

---

## 6. Learning Rate Scheduling: The Hidden Multiplier

Even with the "right" optimizer, **learning rate schedule** often matters more than the optimizer itself.

### **Common Schedules**

| **Schedule** | **Formula** | **Best For** |
|:---|:---|:---|
| **Constant** | $\\eta_t = \\eta_0$ | Never (almost); okay if tuned perfectly |
| **Step Decay** | $\\eta_t = \\eta_0 \cdot \\gamma^{\\lfloor t / s \\rfloor}$ (e.g., $\\gamma = 0.1$, $s$ = 30 epochs) | Supervised learning, standard choice |
| **Exponential Decay** | $\\eta_t = \\eta_0 e^{-\\lambda t}$ | Smooth decay; less common |
| **Cosine Annealing** | $\\eta_t = \\eta_0 \left( \\frac{1 + \\cos(\\pi t / T)}{2} \\right)$ | Vision (ResNets, EfficientNets); smoother than step |
| **Warmup + Cosine** | $\\eta_t = \\text{warmup}(t) \cdot \\text{cosine}(t)$ | Transformers, large batch training |
| **Linear Warmup** | $\\eta_t = \\eta_0 \cdot \min(\\frac{t}{T_{\\text{warmup}}}, 1)$ for first $T$ steps | Large batch; prevents initial divergence |

### **Practical Tips**
-   **Warmup (first 5-10% of training):** Essential for large batch sizes and Transformers.
-   **Decay Factor:** Start with 0.1 (reduce by 10x), increase to 0.5 if too aggressive.
-   **Decay Frequency:** Every 10-30 epochs for supervised learning.

---

## 7. Hyperparameter Tuning Priority

### **If You Only Have Time to Tune ONE Thing:**
1. **Learning Rate** (most important)
2. Learning Rate Schedule
3. Batch Size
4. $\\beta_1, \\beta_2$ (least important; use defaults)

### **Typical Tuning Range**

| **Parameter** | **Range** | **Try First** |
|:---|:---|:---|
| $\\eta$ | $[1e-5, 1]$ (log scale) | 0.001 or 0.01 |
| $\\beta_1$ (momentum in Adam) | $[0.8, 0.99]$ | 0.9 |
| $\\beta_2$ (RMSProp in Adam) | $[0.95, 0.9999]$ | 0.999 |
| $\\epsilon$ (numerical stability) | $[1e-8, 1e-4]$ | 1e-8 (almost never tune) |
| Batch Size | $[16, 256, 512, 1024]$ | 32 or 64 |

---

## 8. Red Flags: When Something's Wrong

| **Symptom** | **Likely Cause** | **Fix** |
|:---|:---|:---|
| Loss diverges immediately | Learning rate too high | Reduce $\\eta$ by 10x |
| Loss stagnates after few steps | Learning rate too low OR bad schedule | Increase $\\eta$ or remove decay schedule |
| Volatile loss (spikes every few batches) | Batch size too small or $\\eta$ too high | Increase batch size or reduce $\\eta$ |
| Works fine but overfits badly | Adam on small dataset | Switch to SGD + Momentum + L2 |
| Converges slow with Adam | Stuck in flat region | Try learning rate warmup |
| NLP model diverges with Adam | Missing AdamW (weight decay) | Use AdamW instead |
| Momentum runs away (loss → inf) | Accumulated gradient too large | Add gradient clipping or reduce $\\eta$ |

---

## 9. Comparison at a Glance: What Changed and Why

```
Vanilla SGD:
  θ ← θ - η·g

+ Momentum (adds direction smoothing):
  v ← β·v + g
  θ ← θ - η·v

+ AdaGrad (adds adaptive scaling per parameter):
  G ← G + g²
  θ ← θ - η·g / √G   ← Problem: G grows forever

  Fix with RMSProp (moving average instead):
  v ← β·v + (1-β)·g²
  θ ← θ - η·g / √v   ← Now it's adaptive forever

+ Adam (combine momentum + adaptive LR):
  m ← β₁·m + g
  v ← β₂·v + g²
  m̂ ← m / (1 - β₁ᵗ)     ← Bias correction
  v̂ ← v / (1 - β₂ᵗ)     ← Bias correction
  θ ← θ - η·m̂ / √v̂   ← Best of both worlds
```

---

## 10. Final Decision Tree (Production Ready)

**START:**

1. **Do you have a pretrained model?**
   - **YES → Use AdamW** with low LR ($10^{-5}$ range), step decay
   - **NO → Go to Step 2**

2. **Is your dataset < 10K examples?**
   - **YES → Use SGD + Momentum**, add L2 regularization
   - **NO → Go to Step 3**

3. **Is this a Transformer or attention-based model?**
   - **YES → Use AdamW** with warmup + cosine annealing schedule
   - **NO → Go to Step 4**

4. **Do you want fastest convergence for experiments?**
   - **YES → Use Adam** with default hyperparameters
   - **NO → Go to Step 5**

5. **Do you care about final generalization performance?**
   - **YES → Use SGD + Momentum** with step decay
   - **NO → Use Adam** (it's fine)

**Special Cases:**
- **GAN training:** Adam with very low $\\eta$ (0.0002), use learning rate schedules
- **RL:** Adam or SGD + Momentum depending on stability
- **Sparse data (NLP embeddings):** Adam or RMSProp (AdaGrad obsolete)
- **Extreme memory constraints:** SGD only

---

## 11. Cheat Sheet Summary

> **"I just want to train a neural network. What do I do?"**

1. **Try Adam first** with $\\eta = 0.001$, step decay schedule (0.1 every 30 epochs)
2. **If it overfits:** Switch to **SGD + Momentum** ($\\eta = 0.01$, $\\beta = 0.9$)
3. **If it's NLP:** Use **AdamW** ($\\eta = 2 \times 10^{-5}$)
4. **If you're stuck:** Try learning rate **warmup** (5-10% of training)

Done.
