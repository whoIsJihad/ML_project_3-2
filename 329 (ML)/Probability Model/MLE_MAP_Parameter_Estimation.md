# Maximum Likelihood Estimation & Maximum A Posteriori

## Why Learn This in ML?

**Core problem:** Every ML model has parameters (weights, means, variances, etc.). How do we choose them?

**Traditional approach (pre-ML):** Engineers hand-tune. Doesn't scale.

**ML approach:** Learn parameters from data. But *how*?

MLE and MAP answer this: **They're the two frameworks for parameter learning.**
- **MLE:** Use data to find the best parameters (frequentist view)
- **MAP:** Use data + prior knowledge to find best parameters (Bayesian view)
- **Gradient descent:** Numerical algorithm to actually compute them

Understanding MLE/MAP is understanding how models learn. Every neural network, logistic regression, Gaussian mixture model—they all optimize either MLE or MAP objectives (or variants).

---

## Notation Guide

| Symbol | Meaning | Example |
|--------|---------|---------|
| θ (theta) | Parameters we want to learn | weights, mean μ, variance σ² |
| D | Dataset (all observations) | {x₁, x₂, ..., xₙ} |
| x_i | Single observation/datapoint | one image, one number |
| p(x\|θ) | Likelihood: probability of data given parameters | P(height=180\|μ=175, σ=10) |
| p(θ) | Prior: belief about parameters before seeing data | "weights probably small" |
| p(θ\|D) | Posterior: belief about parameters after seeing data | Updated after training |
| L(θ) | Likelihood function (for all data) | ∏ᵢ p(xᵢ\|θ) |
| ℓ(θ) | Log-likelihood | Σᵢ log p(xᵢ\|θ) |
| argmax | "Find the value that maximizes" | argmax_θ ℓ(θ) = best parameters |

---

## Maximum Likelihood Estimation (MLE)

### The Idea

You have data. You have a model with parameters θ. **Question:** What parameters make the data most likely?

**Intuition:** If I observe height distribution that looks Gaussian with mean ~175cm, the parameters that generated this should be μ≈175, not μ≈120. The first parameters make my observations more *likely*.

**Formal definition:**
$$\theta_{MLE} = \text{argmax}_\theta \, p(D | \theta) = \text{argmax}_\theta \, \prod_{i=1}^{n} p(x_i | \theta)$$

**Why product?** Assuming observations are independent, joint probability = product of individual probabilities.

**Problem:** Product of tiny probabilities (each p(x_i) ≈ 0.001) underflows numerically. 

**Solution:** Use log-likelihood (log converts product to sum, preserves argmax):
$$\theta_{MLE} = \text{argmax}_\theta \, \ell(\theta) = \text{argmax}_\theta \, \sum_{i=1}^{n} \log p(x_i | \theta)$$

### Why Maximize Likelihood?

**Intuitive answer:** Parameters that make observed data probable are likely correct.

**Formal answer:** Under IID (independent, identically distributed) assumption, MLE is consistent (converges to true parameters as n→∞) and asymptotically efficient (achieves lowest possible variance).

### Example: Estimating Mean of Gaussian

**Setup:** n observations x₁, x₂, ..., xₙ from N(μ, σ²) with known σ²

**Likelihood for single point:**
$$p(x_i | \mu) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x_i - \mu)^2}{2\sigma^2}\right)$$

**Log-likelihood:**
$$\ell(\mu) = \sum_{i=1}^{n} \log p(x_i | \mu) = \sum_{i=1}^{n} \left[-\frac{1}{2}\log(2\pi\sigma^2) - \frac{(x_i - \mu)^2}{2\sigma^2}\right]$$

**Simplify (constant terms don't affect argmax):**
$$\ell(\mu) \propto -\sum_{i=1}^{n} (x_i - \mu)^2$$

**Maximize by taking derivative:**
$$\frac{d\ell}{d\mu} = -2\sum_{i=1}^{n} (x_i - \mu)(-1) = 2\sum_{i=1}^{n} (x_i - \mu) = 0$$

**Solve:**
$$\sum_{i=1}^{n} x_i = n\mu$$
$$\mu_{MLE} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

**Result:** The sample mean! Makes sense—data looks like it came from a Gaussian centered at the sample mean.

### Example: Logistic Regression

**Setup:** Binary classification. Model: P(y=1|x) = σ(wᵀx)

**Likelihood for single example:**
$$p(y_i | x_i, w) = \sigma(w^T x_i)^{y_i} (1-\sigma(w^T x_i))^{1-y_i}$$

**Log-likelihood:**
$$\ell(w) = \sum_{i=1}^{n} \left[y_i \log\sigma(w^T x_i) + (1-y_i)\log(1-\sigma(w^T x_i))\right]$$

This is the **cross-entropy loss** that neural networks minimize! It's MLE.

**Why?** Because neural networks are learning the parameters (weights w) that maximize likelihood of training data.

---

## Maximum A Posteriori (MAP)

### The Idea

MLE ignores prior knowledge. What if we know something about θ before seeing data?

**Example:** In Gaussian parameters, we might believe μ should be small (close to 0) before seeing data. MAP incorporates this belief.

**Formal definition (Bayes' rule):**
$$p(\theta | D) = \frac{p(D|\theta) p(\theta)}{p(D)}$$

**Maximize posterior:**
$$\theta_{MAP} = \text{argmax}_\theta \, p(\theta | D) = \text{argmax}_\theta \, p(D|\theta) p(\theta)$$

(p(D) is constant w.r.t. θ, so we drop it)

**In log space:**
$$\theta_{MAP} = \text{argmax}_\theta \left[\sum_{i=1}^{n} \log p(x_i | \theta) + \log p(\theta)\right]$$

$$= \text{argmax}_\theta \left[\text{log-likelihood} + \text{log-prior}\right]$$

### Why Use MAP?

**Problem with MLE:** With little data, MLE can fit noise. Prior regularizes.

**Example:** Coin flip. Observe 2 heads, 0 tails.
- MLE: θ = 1.0 (100% heads). Obviously wrong—just unlucky!
- MAP with prior θ ~ Beta(1, 1) [uniform]: θ ≈ 0.67 (more reasonable)

**Benefits:**
1. **Regularization:** Prior prevents overfitting
2. **Principled:** Incorporates domain knowledge
3. **Works with small data:** Prior compensates for data scarcity

### Example: Gaussian with Prior

**Setup:** n observations from N(μ, σ²), unknown μ, want to estimate μ

**Prior:** Believe μ should be small: μ ~ N(0, τ²)

**Prior probability:**
$$p(\mu) = \frac{1}{\sqrt{2\pi\tau^2}} \exp\left(-\frac{\mu^2}{2\tau^2}\right)$$

**Log posterior (dropping constants):**
$$\log p(\mu|D) \propto -\sum_{i=1}^{n}\frac{(x_i-\mu)^2}{2\sigma^2} - \frac{\mu^2}{2\tau^2}$$

**Take derivative and set to 0:**
$$\frac{d}{d\mu}\log p(\mu|D) = \sum_{i=1}^{n}\frac{(x_i-\mu)}{\sigma^2} - \frac{\mu}{\tau^2} = 0$$

**Solve:**
$$\frac{n}{\sigma^2}\bar{x} = \frac{n}{\sigma^2}\mu + \frac{\mu}{\tau^2}$$

$$\mu_{MAP} = \frac{\frac{n}{\sigma^2}}{\frac{n}{\sigma^2} + \frac{1}{\tau^2}} \bar{x} = \frac{n\tau^2}{n\tau^2 + \sigma^2} \bar{x}$$

**Interpretation:**
- If τ² → ∞ (weak prior): μ_MAP → μ_MLE (data dominates)
- If τ² → 0 (strong prior): μ_MAP → 0 (prior dominates)
- If n → ∞ (lots of data): μ_MAP → μ_MLE (data dominates)

**This is weighted averaging between data and prior!**

---

## MLE vs MAP

| Aspect | MLE | MAP |
|--------|-----|-----|
| What it optimizes | ∑ᵢ log p(xᵢ\|θ) | ∑ᵢ log p(xᵢ\|θ) + log p(θ) |
| Requires prior? | No | Yes |
| With lots of data | Good | Converges to MLE |
| With little data | May overfit | Regularized by prior |
| Philosophically | "Data speaks" | "Data + prior knowledge" |
| Typical use | Large datasets | Small datasets, domain knowledge |

**Key insight:** MAP = MLE + regularization term

In neural networks:
- MLE: No weight decay
- MAP: L2 regularization (weight decay) = Gaussian prior on weights

---

## How Optimization Actually Happens

### Gradient Descent

Can't solve analytically? Use gradient descent.

**Algorithm:**
```
Initialize θ = θ₀
For each iteration:
  Compute gradient: g = ∇θ ℓ(θ)  [or ∇θ log p(θ|D) for MAP]
  Update: θ ← θ - η·g              [η = learning rate]
```

**For MLE on logistic regression:**
$$\nabla_w \ell(w) = \sum_{i=1}^{n} (\sigma(w^T x_i) - y_i) x_i$$

Each step moves w toward maximizing likelihood.

**For MAP:**
$$\nabla_w [\ell(w) + \log p(w)] = \sum_{i=1}^{n} (\sigma(w^T x_i) - y_i) x_i + \nabla_w \log p(w)$$

Extra term regularizes weights.

### Why This Matters

**Most ML training is:** "Compute likelihood/posterior, take gradient, update parameters"

- Logistic regression: MLE with gradient descent
- Neural networks: MLE (or MAP with L2) with stochastic gradient descent
- Mixture models: EM algorithm (special case of MLE)
- Variational autoencoders: Approximate posterior (Bayesian MAP idea)

Understanding MLE/MAP explains *why* these algorithms work and *what* they're optimizing.

---

## MLE for Different Models

### Linear Regression

**Model:** y = wᵀx + ε, where ε ~ N(0, σ²)

**Likelihood:** p(y|x, w) = N(wᵀx, σ²)

**Log-likelihood:**
$$\ell(w) = -\frac{1}{2\sigma^2}\sum_{i=1}^{n}(y_i - w^T x_i)^2 + \text{const}$$

**MLE:** Minimize sum of squared errors (least squares!)

**Why?** Least squares is maximum likelihood under Gaussian noise.

### Maximum Entropy Distribution

**Question:** You observe data but don't know the distribution. What distribution should you assume?

**Answer (without constraints):** Uniform (maximum entropy = least assumptions)

**Answer (with constraint: E[x] = μ):** Gaussian N(μ, σ²) (maximum entropy subject to mean constraint)

**This is MLE for unknown distribution!** MLE finds most "non-committal" distribution consistent with data.

---

## Bayesian Perspective

### Three Levels

1. **MLE:** Point estimate of θ (single best value)
2. **MAP:** Point estimate using posterior (best value given data + prior)
3. **Bayesian inference:** Full posterior distribution p(θ|D)

**Why stop at point estimate?**
- Posterior tells you uncertainty in θ
- Can make predictions accounting for parameter uncertainty
- Principled decision-making under uncertainty

**Trade-off:** Posterior intractable for most models. Use approximations (variational inference, MCMC).

---

## Concrete ML Example: Linear Regression with Regularization

**Problem:** Learn w to fit y = wᵀx

**Without regularization (MLE):**
$$\min_w \sum_{i=1}^{n}(y_i - w^T x_i)^2$$

**With L2 regularization (MAP with Gaussian prior):**
$$\min_w \sum_{i=1}^{n}(y_i - w^T x_i)^2 + \lambda ||w||^2$$

**Interpretation:**
- Data term: make predictions match observed y
- Prior term: keep weights small (Gaussian prior p(w) ~ exp(-λ||w||²))
- λ controls prior strength

**Same problem:** ML minimizes objective = maximizing log posterior!

---

## Summary: The Learning Framework

| Step | Question | Answer |
|------|----------|--------|
| **1. Model choice** | How do we represent data? | p(x\|θ) (likelihood) |
| **2. Prior** | What do we know before data? | p(θ) (prior) |
| **3. Learning objective** | How to choose θ? | Maximize log p(D\|θ) [MLE] or log p(D\|θ)p(θ) [MAP] |
| **4. Optimization** | How to actually compute? | Gradient descent on objective |
| **5. Prediction** | How to predict new x? | Use learned θ̂ in p(x\|θ̂) |

**Why ML course teaches this:**
- It's the **why** behind every supervised learning algorithm
- Explains why regularization works
- Connects to Bayesian thinking
- Foundation for probabilistic models

---

## Key Equations to Remember

**Likelihood:**
$$L(\theta) = \prod_{i=1}^{n} p(x_i|\theta)$$

**Log-likelihood:**
$$\ell(\theta) = \sum_{i=1}^{n} \log p(x_i|\theta)$$

**MLE:**
$$\theta_{MLE} = \text{argmax}_\theta \, \ell(\theta)$$

**Posterior (Bayes):**
$$p(\theta|D) = \frac{p(D|\theta)p(\theta)}{p(D)}$$

**MAP:**
$$\theta_{MAP} = \text{argmax}_\theta [\ell(\theta) + \log p(\theta)]$$

**Gradient descent:**
$$\theta_{t+1} = \theta_t - \eta \nabla_\theta [-\ell(\theta_t)]$$

(Negative gradient because we minimize loss = maximize likelihood)

---

## Questions This Answers

- **Why is squared error loss used in regression?** MLE under Gaussian noise
- **Why add L2 regularization?** MAP with Gaussian prior
- **Why does batch size affect learning?** Stochastic gradient descent approximates full gradient
- **Why do we need a validation set?** MLE overfits on training data; validation assesses generalization
- **Why Bayesian ML?** MAP/MLE are point estimates; Bayesian gives uncertainty
- **Why do neural networks work?** They fit arbitrary functions to maximize likelihood/posterior
