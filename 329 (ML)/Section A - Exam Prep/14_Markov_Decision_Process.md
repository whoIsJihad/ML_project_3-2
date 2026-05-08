# 📘 Markov Decision Process (MDP)

## 1. Core Idea (Intuition)

**MDP** is a mathematical framework for modeling sequential decision-making under uncertainty.

**Key idea:** Current state and action fully determine future transitions (Markov property).

**Applications:**
- Robot control
- Game AI
- Resource allocation
- Autonomous vehicles

---

## 2. Mathematical Formulation

### Components
An MDP is a tuple $\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$:

- $\mathcal{S}$: State space (all possible states $s$)
- $\mathcal{A}$: Action space (all possible actions $a$)
- $\mathcal{P}(s'|s,a)$: Transition probability (probability of reaching state $s'$ from $s$ taking action $a$)
- $\mathcal{R}(s,a,s')$: Reward (immediate reward for transition)
- $\gamma \in [0,1]$: Discount factor (importance of future rewards)

### Markov Property
The future depends only on current state and action, not history:

$$P(s_{t+1} | s_t, a_t, s_{t-1}, a_{t-1}, \ldots) = P(s_{t+1} | s_t, a_t) = \mathcal{P}(s_{t+1}|s_t, a_t)$$

---

## 3. Policy & Value Functions

### Policy
A policy $\pi(a|s)$ maps state $s$ to action $a$ (or probability distribution over actions).

$$\pi(a|s) = P(a|s)$$

**Deterministic policy:** $\pi(a|s) \in \{0, 1\}$ (always same action)

**Stochastic policy:** $\pi(a|s) \in (0, 1)$ (randomized)

### Value Function (Expected Discounted Return)
$$V^\pi(s) = \mathbb{E}[R_t | s_t = s, \pi] = \mathbb{E}\left[\sum_{k=0}^{\infty} \gamma^k r_{t+k+1} \Big| s_t = s\right]$$

where:
- $r_{t+k+1}$: reward at time $t+k+1$
- $\gamma^k$: discount factor applied to future rewards

**Interpretation:** Expected sum of discounted future rewards starting from state $s$, following policy $\pi$.

### Q-Function (Action-Value Function)
$$Q^\pi(s,a) = \mathbb{E}[R_t | s_t = s, a_t = a, \pi] = \mathbb{E}\left[\sum_{k=0}^{\infty} \gamma^k r_{t+k+1} \Big| s_t = s, a_t = a\right]$$

**Interpretation:** Expected discounted return starting from state $s$, taking action $a$, then following policy $\pi$.

### Relationship
$$V^\pi(s) = \sum_{a} \pi(a|s) Q^\pi(s,a)$$

---

## 4. Bellman Equations

### Bellman Expectation Equation (for evaluation)

For value function:
$$V^\pi(s) = \sum_{a} \pi(a|s) \sum_{s'} \mathcal{P}(s'|s,a) \left[ \mathcal{R}(s,a,s') + \gamma V^\pi(s') \right]$$

For Q-function:
$$Q^\pi(s,a) = \sum_{s'} \mathcal{P}(s'|s,a) \left[ \mathcal{R}(s,a,s') + \gamma \sum_{a'} \pi(a'|s') Q^\pi(s',a') \right]$$

**Intuition:** Value at state $s$ = immediate reward + discounted value at next state.

### Bellman Optimality Equation

Optimal value function $V^*(s)$ satisfies:
$$V^*(s) = \max_a \sum_{s'} \mathcal{P}(s'|s,a) \left[ \mathcal{R}(s,a,s') + \gamma V^*(s') \right]$$

Optimal Q-function $Q^*(s,a)$:
$$Q^*(s,a) = \sum_{s'} \mathcal{P}(s'|s,a) \left[ \mathcal{R}(s,a,s') + \gamma \max_{a'} Q^*(s',a') \right]$$

Optimal policy (greedy w.r.t. optimal Q):
$$\pi^*(a|s) = \begin{cases} 1 & \text{if } a = \arg\max_a Q^*(s,a) \\ 0 & \text{otherwise} \end{cases}$$

---

## 5. Discount Factor $\gamma$

| $\gamma$ | Effect |
|----------|--------|
| $\gamma = 0$ | Only immediate reward matters; no lookahead |
| $\gamma = 0.5$ | Balance immediate and near-future rewards |
| $\gamma = 0.99$ | Care about distant future (long-horizon) |
| $\gamma \to 1$ | Infinite horizon; all future rewards weighted equally |

**Practical choice:** $\gamma \in [0.9, 0.99]$ for most problems.

---

## 6. Finite vs. Infinite Horizon

### Finite Horizon
Episode ends after $T$ steps. Value depends on time remaining.

$$V_t(s) = \mathbb{E}[r_{t+1} + r_{t+2} + \cdots + r_T | s_t = s]$$

### Infinite Horizon
No terminal state; agent acts forever.

Convergence requires $\gamma < 1$ to ensure $\sum_{k=0}^{\infty} \gamma^k r_k$ converges.

---

## 7. State Representation

### Discrete States
$|\mathcal{S}|$ is finite. Transition matrix $\mathcal{P} \in \mathbb{R}^{|S| \times |S|}$.

**Example:** Chess (finite positions), gridworld.

### Continuous States
$\mathcal{S} = \mathbb{R}^d$. Transitions given by dynamics function $s_{t+1} = f(s_t, a_t)$.

**Example:** Robot control, autonomous driving.

---

## 8. Assumptions & Limitations

### Markov Assumption
Current state contains all information needed to predict future. Violated if:
- Observable state is noisy / partial
- System has hidden state

**Fix:** History encoding, POMDP (Partially Observable MDP).

### Known Model Assumption
$\mathcal{P}(s'|s,a)$ and $\mathcal{R}(s,a,s')$ are known. Often violated:
- Real-world environments unknown
- Model learning required (sample inefficient)

---

## 9. Exam Questions

### Conceptual
1. Define Markov property. When is it violated?
2. What's the difference between $V(s)$ and $Q(s,a)$?
3. Why is the discount factor $\gamma$ needed in infinite-horizon problems?

### Derivation-Based
1. **Derive** Bellman expectation equation for $V^\pi(s)$ from first principles.
2. **Show** that the optimal policy $\pi^*$ is greedy w.r.t. $Q^*$.

### Trick/Failure Cases
1. $\gamma = 1$ in infinite horizon: what happens? Why is it problematic?
2. A Markov assumption is violated (state is partially observable). How does it affect value function?

---

## 10. Key Takeaways

- **MDP:** Tuple $\langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$; framework for sequential decision-making
- **Markov property:** Future depends only on current state and action
- **Value function:** $V^\pi(s) = \mathbb{E}[\sum_k \gamma^k r_{t+k+1} | s_t = s]$
- **Q-function:** $Q^\pi(s,a) = \mathbb{E}[\sum_k \gamma^k r_{t+k+1} | s_t = s, a_t = a]$
- **Bellman equations:** Recursive relationship; foundation for RL algorithms
- **Optimal policy:** Greedy w.r.t. $Q^*(s,a) = \max_a \sum_{s'} \mathcal{P}(s'|s,a)[r + \gamma \max_{a'} Q^*(s',a')]$
- **Discount factor:** $\gamma \in [0,1]$; controls horizon importance

---
