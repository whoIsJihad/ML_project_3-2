# 📘 Optimizers: Momentum, Nesterov Momentum, Adagrad, RMSProp

## 1. Core Idea (Intuition)

* **Problem:** Vanilla SGD has issues — oscillation in steep directions, slow progress in flat directions, same learning rate for all parameters, gets stuck at saddle points.
* **Why needed:** Real loss surfaces are not smooth bowls. They have ravines, plateaus, saddle points. We need smarter update rules.
* **Key insight:** Each optimizer modifies the basic `w = w - α·g` rule by adding memory of past gradients (momentum) or adapting learning rate per-parameter (adaptive methods).

---

## 2. Mathematical Formulation

Let `g = ∇L(w)` be the current gradient.

### Momentum

**Idea:** Accumulate a running average of past gradients (velocity). If gradients consistently point in one direction, build up speed. If they oscillate, velocity averages them out.

```
v = β·v + g                    (accumulate velocity)
w = w - α·v                    (update with velocity)
```

Where:
- `v` = velocity (same shape as w), initialized to 0
- `β` = momentum coefficient (typically 0.9)
- `α` = learning rate
- `g` = current gradient

**Why it works:**
- In the ravine direction: gradients oscillate (+/-), velocity averages to ~0 → less oscillation
- In the consistent direction: gradients add up, velocity grows → faster progress
- Think of a ball rolling downhill — it builds momentum going downhill and smooths out bumps

**Effect of β:**
- β = 0: reduces to vanilla SGD
- β = 0.9: heavy smoothing, fast convergence (standard)
- β = 0.99: very heavy, may overshoot

### Nesterov Momentum (Nesterov Accelerated Gradient — NAG)

**Idea:** "Look ahead" before computing the gradient. First take a step using the current velocity, THEN compute the gradient at that lookahead position.

```
w_lookahead = w - α·β·v        (peek ahead)
g = ∇L(w_lookahead)            (gradient at lookahead position)
v = β·v + g                    (update velocity)
w = w - α·v                    (update weights)
```

**Why better than standard momentum:**
- Standard momentum computes gradient at current position, then jumps.
- Nesterov computes gradient at where we're ABOUT to be → corrective. If we're about to overshoot, the lookahead gradient points backward → slows down.
- More responsive to changes in the loss surface.

### Adagrad (Adaptive Gradient)

**Idea:** Give each parameter its own learning rate. Parameters that have had large gradients get smaller learning rates; rare/small-gradient parameters get larger rates.

```
s = s + g²                     (accumulate squared gradients, element-wise)
w = w - α · g / (√s + ε)       (update with adapted rate)
```

Where:
- `s` = sum of squared gradients (same shape as w), initialized to 0
- `g²` = element-wise square of gradient
- `ε` = small constant (~10⁻⁸) to prevent division by zero
- Division and sqrt are element-wise

**Why it works:**
- Frequent features (large cumulative gradient) → learning rate shrinks → fine-tuning
- Rare features (small cumulative gradient) → learning rate stays large → keeps learning
- Great for sparse data (NLP, recommendations)

**Fatal flaw:** `s` only grows (it's a sum of squares). Learning rate monotonically decreases → eventually becomes infinitesimally small → learning stops entirely. Adagrad effectively dies.

### RMSProp (Root Mean Square Propagation)

**Idea:** Fix Adagrad's dying learning rate by using an exponential moving average of squared gradients instead of the total sum.

```
s = β·s + (1-β)·g²             (exponential moving average of squared gradients)
w = w - α · g / (√s + ε)       (update)
```

Where:
- `β` = decay rate (typically 0.9 or 0.99)
- Rest same as Adagrad

**Why it fixes Adagrad:**
- Old squared gradients gradually decay (forgotten) → learning rate doesn't shrink to zero
- Recent gradient magnitudes matter more → adapts to current terrain
- Effectively "rescales" the gradient per-parameter based on recent history

---

## 3. Algorithm / Training Procedure

All optimizers follow the same outer loop — only the update step differs:

```
Initialize w, set hyperparameters
Initialize optimizer state (v=0 for momentum, s=0 for adaptive)

For each epoch:
  For each mini-batch:
    g = compute_gradient(batch)
    [optimizer-specific update]
    w = w - α · [adjusted gradient]
```

### Summary of update rules:

| Optimizer | Update Rule | Key State |
|---|---|---|
| SGD | `w -= α·g` | None |
| Momentum | `v = β·v + g; w -= α·v` | Velocity v |
| Nesterov | Lookahead then `v = β·v + g; w -= α·v` | Velocity v |
| Adagrad | `s += g²; w -= α·g/(√s+ε)` | Squared grad sum s |
| RMSProp | `s = β·s + (1-β)·g²; w -= α·g/(√s+ε)` | EMA of squared grads s |

**Note:** Adam (not in this syllabus) combines Momentum + RMSProp. It's the most popular optimizer in practice.

---

## 4. Optimization / Learning Dynamics

### Momentum:
- Accelerates convergence in consistent-gradient directions by 1/(1-β) factor
- With β=0.9, effective amplification ≈ 10× in consistent direction
- Dampens oscillation in high-curvature directions

### Nesterov:
- Converges faster than standard momentum on convex problems (provably)
- The "correction" effect: if about to overshoot, gradient at lookahead corrects the velocity
- Theoretically optimal for smooth convex functions: O(1/T²) vs O(1/T) for vanilla GD

### Adagrad:
- Automatically adjusts learning rate per parameter → no manual tuning per feature
- Convergence rate for convex: O(1/√T), same as SGD, but with per-feature adaptation
- Dies after many iterations → not suitable for deep learning training

### RMSProp:
- Non-stationary adaptation (forgets old gradients) → works throughout long training
- Effectively normalizes the gradient by its recent RMS magnitude
- Default choice for RNN training (Hinton's recommendation)

---

## 5. Failure Cases / Limitations

| Optimizer | Failure | Why |
|---|---|---|
| Momentum | Overshooting | Too much momentum (high β) carries past minimum |
| Momentum | Doesn't adapt per-parameter | Same α for all weights |
| Nesterov | Overhead | Two gradient-like evaluations per step |
| Adagrad | Learning rate decay to zero | s grows unboundedly → 1/√s → 0 |
| Adagrad | Poor for non-sparse problems | Conservative in all directions |
| RMSProp | Sensitive to β | Wrong decay rate → unstable or too conservative |
| All | Still need good initial α | Bad learning rate breaks everything |

---

## 6. Where It Works Well

| Optimizer | Best For |
|---|---|
| Momentum | Most neural network training, convex and non-convex |
| Nesterov | When you want faster convergence, theoretical guarantees matter |
| Adagrad | Sparse data (NLP, click-through prediction), short training runs |
| RMSProp | RNNs, non-stationary problems, deep learning in general |

---

## 7. Variants / Extensions

| Variant | What it does |
|---|---|
| **Adam** | Combines Momentum (1st moment) + RMSProp (2nd moment) + bias correction. Most popular optimizer. |
| **AdamW** | Adam with weight decay decoupled from gradient updates. Better generalization. |
| **Adadelta** | Like RMSProp but removes need for initial learning rate. |
| **LAMB/LARS** | Layer-wise adaptive learning rates for large-batch training. |
| **SGD + Momentum + LR schedule** | Often matches or beats Adam on final accuracy with good tuning. |

---

## 8. Comparison Table

| Optimizer | Adaptive LR? | Memory | Handles Sparse Data | Handles Ravines | Risk |
|---|---|---|---|---|---|
| SGD | No | O(0) | Poor | Poor | Oscillation |
| Momentum | No | O(n) for v | Poor | Good (smooths) | Overshooting |
| Nesterov | No | O(n) for v | Poor | Better | Slight overhead |
| Adagrad | Yes (per-param) | O(n) for s | Excellent | Good | LR dies |
| RMSProp | Yes (per-param) | O(n) for s | Good | Good | Sensitive to β |

---

## 9. Exam Questions

### Conceptual:
1. Explain why momentum reduces oscillation in ravine-shaped loss surfaces. Use a diagram or example.
2. What is the key difference between Nesterov and standard momentum? Why is the "lookahead" helpful?
3. Why does Adagrad's learning rate go to zero, and how does RMSProp fix this?

### Derivation-based:
4. Write out the momentum update equations. Show that for constant gradient g, the velocity converges to g/(1-β), giving an effective learning rate of α/(1-β).
5. Show mathematically why Adagrad's per-parameter learning rate is α/√(Σgₜ²). What happens as t → ∞?

### Trick / Failure-case:
6. You're training with Adagrad and loss plateaus after 50 epochs. Switching to RMSProp with same α makes loss decrease again. Explain.
7. You increase momentum β from 0.9 to 0.999 and training loss starts oscillating wildly. Why?

---

## 10. Key Takeaways

* Momentum builds up speed in consistent directions, dampens oscillations. β=0.9 is standard.
* Nesterov is momentum with a correction: compute gradient at lookahead position. Provably faster convergence.
* Adagrad adapts learning rate per parameter based on historical gradients. Great for sparse data but dies over time.
* RMSProp fixes Adagrad by using exponential moving average → learning rate stays alive.
* Adam = Momentum + RMSProp (the most popular optimizer in practice, not in your syllabus but know it).
* No single optimizer is best for all problems. SGD+Momentum often wins with good tuning. Adam wins with default hyperparameters.
