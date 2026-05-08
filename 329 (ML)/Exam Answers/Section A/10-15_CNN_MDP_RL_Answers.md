# 📝 CNN & Reinforcement Learning - Exam Answers

## CNN Basics

### Q1: Why do CNNs need fewer parameters than fully connected?

**Fully Connected:**
- 32×32 image = 1024 inputs
- 1 hidden layer with 100 neurons = 1024×100 = 102,400 parameters

**CNN (with weight sharing):**
- 3×3 kernel = 9 weights (+ bias)
- 32 output filters = 32×9 = 288 parameters
- ~99.7% fewer parameters!

**Why:** Weight sharing. Same kernel convolved across entire image. Kernel learns universal detector (e.g., edge, corner) applicable everywhere.

---

### Q2: What is weight sharing and why does it make sense?

**Weight sharing:** Same $W$ applied to every spatial location.

**Why sensible for images:**
- Edge at (10,10) same as edge at (200,200)
- Use same detector
- Translational invariance: object detected regardless of position

**Mathematical form:**
$$Y[i,j] = \sum_{a,b,c} X[i+a,j+b,c] \cdot W[a,b,c]$$

Same $W$ for all $(i,j)$ positions.

---

### Q3: What does max pooling do? Is it learnable?

**Max pooling:** Take maximum in each region.
$$Y[i,j] = \max_{a,b} X[i \cdot s + a, j \cdot s + b]$$

**Purpose:**
- Reduce spatial dimensions (1/4 size with 2×2 pooling)
- Detect features robustly (slight shifts don't matter)
- Add nonlinearity

**Learnable?** No. Fixed operation (not parameterized).

**Alternative:** Learned pooling (convolutional pooling with stride) — has parameters.

---

## Kernels & Filters

### Sobel Edge Detector

Sobel kernel detects vertical edges:
$$K = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}$$

**Why it works:**
- Left side: negative (darker)
- Right side: positive (lighter)
- Convolution: (lighter - darker) = edge strength

**Handcrafted:** Designed manually by humans.

**Learned filters:** CNN learns from data. After training, resembles Sobel but optimized for task.

---

### 1×1 Convolution

**What:** Apply kernel of size 1×1 across channels.

**Use cases:**
1. **Dimensionality reduction:** 64 input channels → 32 output channels
2. **Feature fusion:** Mix channels without spatial mixing
3. **Nonlinearity:** Add ReLU between layers (bottleneck design)

**Example:**
```
Input:  32×32×64 (spatial + 64 channels)
1×1 conv to 32 channels: 32×32×32
Cost: 32×32×(64×1×1×32) = much cheaper than 3×3
```

---

## CNN Architectures

### LeNet (1998)
- Simple: 2 conv layers, 2 pooling, FC layer
- Use: MNIST handwritten digits
- Success: Showed CNNs work for vision

### AlexNet (2012)
- Breakthrough: 8 layers, ReLU (not sigmoid), Dropout
- Use: ImageNet classification
- Impact: Won ImageNet 2012; sparked deep learning boom

### VGG (2014)
- Simple: Stack 3×3 kernels (equivalent to 5×5 but more efficient)
- Use: ImageNet
- Feature: Showed depth matters

### Inception (2014)
- Multi-scale: Apply 1×1, 3×3, 5×5 convolutions in parallel
- Concatenate results: Multi-scale feature detection
- Efficient: 1×1 conv reduces channels before expensive operations

### ResNet (2015)
- Skip connections: $h^{(l+2)} = f(h^{(l)}) + h^{(l)}$
- Solves: Deep networks hard to train (vanishing gradients)
- Effect: Can train 100+ layer networks

---

## Markov Decision Process

### Components

$$\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$$

- **States** $\mathcal{S}$: Possible situations (e.g., chess board positions)
- **Actions** $\mathcal{A}$: Choices available (e.g., move queen)
- **Transition** $\mathcal{P}(s'|s,a)$: Probability next state is $s'$ after action $a$ in state $s$
- **Reward** $\mathcal{R}(s,a)$: Immediate reward for action $a$ in state $s$
- **Discount** $\gamma$: Weight future rewards ($\gamma=0.9$ means future 10% less valuable than present)

---

### Markov Property

**Definition:** Future depends only on current state, not history.

$$P(s_{t+1} | s_t, a_t, s_{t-1}, a_{t-1}, \ldots) = P(s_{t+1} | s_t, a_t)$$

**Violation:** Partially observable environments (poker, fog of war)

---

### Value Functions

**State value:** Expected return from state $s$
$$V(s) = \mathbb{E}[R_t + \gamma R_{t+1} + \gamma^2 R_{t+2} + \ldots | s_t = s]$$

**Action value:** Expected return from state $s$, action $a$
$$Q(s,a) = \mathbb{E}[R_t + \gamma V(s') | s_t=s, a_t=a]$$

Relationship: $V(s) = \max_a Q(s,a)$

---

## Reinforcement Learning

### Q-Learning vs SARSA

**Q-Learning (Off-Policy):**
- Learn optimal $Q^*(s,a)$ regardless of current policy
- Update: $Q(s,a) ← Q(s,a) + \alpha[r + \gamma \max_{a'} Q(s',a') - Q(s,a)]$
- Can learn from bad experiences (suboptimal actions)

**SARSA (On-Policy):**
- Learn $Q^\pi(s,a)$ for current policy $\pi$
- Update: $Q(s,a) ← Q(s,a) + \alpha[r + \gamma Q(s',a') - Q(s,a)]$
- Uses actual next action (more conservative)

**Tradeoff:**
- Q-learning: More aggressive, can learn from mistakes, but risky during learning
- SARSA: Safer, won't learn terrible policies, but slower to converge

**Example:** Cliff walking
- Q-learning: Learns to walk on cliff edge (optimal but risky during learning)
- SARSA: Walks far from cliff (safe, suboptimal)

---

### Monte Carlo vs Temporal Difference

**Monte Carlo:**
- Use complete episode return: $G_t = R_t + \gamma R_{t+1} + \ldots + \gamma^{T-1}R_T$
- Update: $V(s_t) ← V(s_t) + \alpha(G_t - V(s_t))$
- Pros: Unbiased estimate
- Cons: High variance, need complete episodes

**Temporal Difference (TD):**
- Use bootstrap: $G_t = R_t + \gamma V(s_{t+1})$
- Update: $V(s_t) ← V(s_t) + \alpha(R_t + \gamma V(s_{t+1}) - V(s_t))$
- Pros: Low variance, learn online, don't need complete episodes
- Cons: Biased (depends on $V(s_{t+1})$ estimate)

**TD error:** $\delta_t = R_t + \gamma V(s_{t+1}) - V(s_t)$ (surprise/prediction error)

---

### Exploration-Exploitation Tradeoff

**Exploration:** Try actions to learn values (taking risk)
**Exploitation:** Use best known action (greedy)

$\epsilon$-greedy:
```
With probability ε: choose random action
With probability 1-ε: choose best action
```

Too low $\epsilon$: Stuck in local optimum
Too high $\epsilon$: Never exploit learned knowledge

---

### Trick Case: $\epsilon = 0$ from Start

**Problem:** Never explore. Stuck with initial random guess of $Q$ values.

**Example:** All actions initially $Q(s,a) = 0$.
- Every action equally "good"
- Greedy: pick first action forever
- Never discover other actions' rewards

**Consequence:** Can't find optimal policy.

**Solution:** Start with $\epsilon > 0$, decay it over time.

---

