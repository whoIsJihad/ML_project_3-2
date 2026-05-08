# 📘 Reinforcement Learning: Q-Learning, SARSA, Monte Carlo

## 1. Core Idea (Intuition)

**Problem:** Model $\mathcal{P}(s'|s,a)$ and $\mathcal{R}(s,a,s')$ unknown. Must learn from experience.

**Solution:** Learn $Q^*(s,a)$ by trial and error.

Three families of algorithms:
- **Value-based:** Learn $Q(s,a)$ or $V(s)$
- **Policy-based:** Learn policy $\pi(a|s)$ directly
- **Model-based:** Learn model $\mathcal{P}, \mathcal{R}$, then plan

This section covers **value-based methods**.

---

## 2. Q-Learning (Off-Policy)

### Idea
Learn optimal $Q^*(s,a)$ using Bellman optimality equation:

$$Q^*(s,a) = \sum_{s'} \mathcal{P}(s'|s,a) \left[ r + \gamma \max_{a'} Q^*(s',a') \right]$$

Cannot compute sum (model unknown), so **sample from experience**.

### Algorithm

```
Initialize Q(s, a) = 0 for all states and actions

For each episode:
  s ← initial state
  While s is not terminal:
    a ← ε-greedy(Q(s, ·))  [explore with probability ε, else greedy]
    
    Take action a; observe (r, s')
    
    α ← learning rate
    Q(s, a) ← Q(s, a) + α [r + γ·max_a' Q(s', a') - Q(s, a)]
                    ↑ target ↑           ↑ old estimate ↑
    
    s ← s'
```

### Update Rule Breakdown

**TD Error (Temporal Difference):**
$$\delta_t = r + \gamma \max_{a'} Q(s', a') - Q(s,a)$$

**Update:**
$$Q(s,a) \leftarrow Q(s,a) + \alpha \delta_t$$

**Intuition:** 
- If $\delta_t > 0$: Target is higher than estimate; increase $Q(s,a)$
- If $\delta_t < 0$: Target is lower; decrease $Q(s,a)$

### Off-Policy Meaning
**Behavior policy:** $\epsilon$-greedy (exploration)

**Target policy:** Greedy w.r.t. $Q$ (exploitation)

**Off-policy:** Learn optimal policy while following exploratory policy.

### Convergence
**Theorem:** Q-learning converges to $Q^*$ under conditions:
1. All state-action pairs visited infinitely often
2. Learning rate $\alpha_t$ satisfies $\sum_t \alpha_t = \infty$ and $\sum_t \alpha_t^2 < \infty$ (e.g., $\alpha_t = 1/t$)

**In practice:** Fixed $\alpha \approx 0.01$ to $0.1$ works well.

---

## 3. SARSA (State-Action-Reward-State-Action)

### Idea
Similar to Q-learning, but uses **next action taken** instead of **best next action**.

### Algorithm

```
Initialize Q(s, a) = 0 for all states and actions

For each episode:
  s ← initial state
  a ← ε-greedy(Q(s, ·))
  
  While s is not terminal:
    Take action a; observe (r, s')
    a' ← ε-greedy(Q(s', ·))  [choose next action with ε-greedy]
    
    Q(s, a) ← Q(s, a) + α [r + γ·Q(s', a') - Q(s, a)]
    
    s ← s'
    a ← a'
```

### On-Policy vs. Off-Policy

| Aspect | Q-Learning | SARSA |
|--------|-----------|-------|
| **Next action** | Greedy $\max_a Q(s',a)$ | Actual $a' \sim \pi(s')$ |
| **Policy** | Off-policy (learns optimal while exploring) | On-policy (learns from actual behavior) |
| **Exploration** | Separate behavior policy (explore-exploit) | Uses $\epsilon$-greedy in learning |
| **Risk** | Can learn risky behavior (explored but not executed) | Conservative (only learns what it does) |
| **Convergence** | Slower (exploration bias) | Faster (less noisy) |

### Example: Cliff Walking

```
[S]....[C][C][C]
         ..............
         ..............
         [G]
```

**Scenario:** Sharp cliff; falling = -100 reward.

**Q-Learning:** Finds optimal path near cliff (high risk, high reward potential)
- Because it explores, it learns cliff is bad
- But in learning, might fall

**SARSA:** Finds safer path away from cliff
- Only learns what it actually does
- Risk-averse

---

## 4. Monte Carlo Methods

### Idea
Estimate $V(s)$ or $Q(s,a)$ by **averaging returns from complete episodes**.

$$V(s) = \frac{1}{N} \sum_{i=1}^{N} G_i(s)$$

where $G_i(s)$ is return from episode $i$ starting at state $s$.

### Algorithm: Monte Carlo for Value Estimation

```
Initialize V(s) = 0, returns(s) = []

For each episode:
  Generate full episode: s_0, a_0, r_1, s_1, a_1, r_2, ...
  
  G ← 0  [return accumulated backwards]
  For t = T-1 down to 0:  [go backwards through episode]
    G ← r_{t+1} + γ·G
    returns(s_t) ← append G
    V(s_t) ← mean(returns(s_t))
```

### Comparison: MC vs. TD-Based (Q-learning, SARSA)

| Aspect | Monte Carlo | TD (Q-learning, SARSA) |
|--------|-------------|----------------------|
| **Data needed** | Full episodes | Single transitions |
| **Variance** | High (sums full trajectories) | Low (single step) |
| **Bias** | Zero (unbiased return) | Positive (bootstrap error) |
| **Convergence** | Slower (high variance) | Faster (low variance) |
| **Early termination** | Problem (incomplete episodes) | OK (can learn from partial) |
| **Use case** | Model-free planning; games | Real-time learning |

---

## 5. Epsilon-Greedy Exploration

### Algorithm

$$a = \begin{cases}
\arg\max_a Q(s, a) & \text{with probability } 1 - \epsilon \\
\text{random action} & \text{with probability } \epsilon
\end{cases}$$

### Effect of $\epsilon$

| $\epsilon$ | Behavior |
|-----------|----------|
| $\epsilon = 0$ | Fully greedy (exploitation only; no learning) |
| $\epsilon = 0.1$ | Mostly greedy (10% random exploration) |
| $\epsilon = 0.5$ | Half exploration, half exploitation (slow) |
| $\epsilon = 1$ | Fully random (no exploitation; no convergence) |

**Best practice:** Decay $\epsilon$ over time: $\epsilon_t = \epsilon_0 \cdot 0.99^t$ (start with exploration, reduce later).

---

## 6. Function Approximation

For large/continuous state spaces, cannot store $Q(s,a)$ as table.

**Solution:** Parametrize $Q(s,a; \mathbf{w})$ with neural network.

$$Q(s,a; \mathbf{w}) = f_{\mathbf{w}}(s,a)$$

**Update (stochastic gradient descent):**
$$\mathbf{w} \leftarrow \mathbf{w} + \alpha \delta_t \nabla_{\mathbf{w}} Q(s,a; \mathbf{w})$$

where $\delta_t = r + \gamma \max_{a'} Q(s',a';\mathbf{w}) - Q(s,a;\mathbf{w})$ (Q-learning target).

### Issues
- **Non-stationary target:** $\max_{a'} Q(s',a';\mathbf{w})$ changes as $\mathbf{w}$ updates
- **Correlation:** Consecutive transitions correlated; biased gradient estimates

### Solutions (Deep Q-Learning improvements)
1. **Target network:** Separate network $\mathbf{w}^-$ (updated infrequently)
2. **Experience replay:** Store transitions; sample minibatches (breaks correlation)

---

## 7. Failure Cases & Pitfalls

| Problem | Why | Fix |
|---------|-----|-----|
| **Too much exploration** ($\epsilon$ high) | Doesn't exploit learned policy | Decay $\epsilon$ over time |
| **Too little exploration** | Sticks to bad initial policy | Increase $\epsilon$ initially |
| **Learning rate too high** | Unstable oscillations | Reduce $\alpha$ |
| **Learning rate too low** | Slow convergence | Increase $\alpha$ |
| **Tabular methods with huge state space** | Memory explosion | Use function approximation (neural network) |

---

## 8. Exam Questions

### Conceptual
1. What's the difference between Q-learning and SARSA? When would you use each?
2. Why is Q-learning off-policy while SARSA is on-policy?
3. Monte Carlo vs. TD learning: compare bias, variance, data efficiency.

### Derivation-Based
1. **Derive** the Q-learning update rule from the Bellman optimality equation.
2. **Show** that Monte Carlo returns are unbiased estimates of $V(s)$.

### Trick/Failure Cases
1. Q-learning learns a risky policy (near cliff). SARSA learns safe policy. Why?
2. You set $\epsilon = 0$ from the start. What happens?

---

## 9. Key Takeaways

- **Q-Learning:** Off-policy; learns optimal using $\max Q(s',a')$ in target
- **SARSA:** On-policy; learns from actual $Q(s',a')$ taken
- **Update rule:** $Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma Q_{\text{next}} - Q(s,a)]$
- **Exploration:** $\epsilon$-greedy; balance exploration/exploitation
- **Monte Carlo:** Average full-episode returns; high variance, zero bias
- **TD methods:** Single-step updates; low variance, biased
- **Function approximation:** Neural networks for large state spaces; needs target network + replay buffer
- **Convergence:** Requires visiting all state-action pairs sufficiently often

---
