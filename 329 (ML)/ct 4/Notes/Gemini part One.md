# Study Guide 1: Learning Probabilistic Models & EM

## 1. Learning Paradigms

- **Maximum Likelihood (ML) Learning**:
    
    - **Goal**: Find parameters $\theta$ that make the observed data $D$ most probable.
        
    - **Philosophy**: "Which model settings are most likely to have generated this specific dataset?"
        
    - **Limitation**: Can overfit if the dataset is small (e.g., if you flip a coin once and get heads, ML says the coin is 100% heads).
        
- **Bayesian Learning**:
    
    - **Goal**: Calculate the _posterior probability_ of a hypothesis given the data: $P(h|D) \propto P(D|h)P(h)$.
        
    - **Philosophy**: We start with a "prior" belief and update it as we see more evidence.
        
    - **Outcome**: Instead of one "best" parameter, we get a distribution over all possible parameters.
        

## 2. The EM (Expectation-Maximization) Algorithm

The EM algorithm is used when we have **missing data** or **latent variables** (hidden labels).

### The Core Intuition

If we knew which data point belonged to which cluster, we could easily calculate the means/variances. If we knew the means/variances, we could easily assign data points to clusters. Since we know neither, we iterate.

### The Two Steps

1. **E-Step (Expectation)**:
    
    - **Task**: "Soft" assignment.
        
    - Using the current parameters (means, variances, weights), calculate the probability that each data point $x_j$ belongs to each component $i$.
        
    - This result is often called the **responsibility** ($p_{ij}$).
        
2. **M-Step (Maximization)**:
    
    - **Task**: Update parameters.
        
    - Recalculate the means, variances, and weights of the components using the "weighted" data points assigned in the E-step.
        
    - **Goal**: Maximize the likelihood of the data given these new assignments.
        

### Key Characteristics

- **Convergence**: Guaranteed to increase the likelihood at every step until a local maximum is reached.
    
- **Starting Point**: Sensitive to initial random values. Different starts can lead to different local optima.