# The Big Picture: ML Relationships, Tradeoffs, and Exam Hacks

## 1. The Relationship Map (How Topics Connect)

To succeed in the exam, don't view these as isolated chapters. View them as a **path of improvement**:

*   **K-Means → GMM:** K-Means is a "Baby GMM." It assumes every cluster is a perfect circle and makes "hard" guesses. GMM is the "adult" version that allows for ellipses and "soft" probabilities.
*   **MLE → MAP → Bayesian:** This is the ladder of trust. 
    *   **MLE:** Only uses current data (prone to overfitting).
    *   **MAP:** Data + Prior (Regularization).
    *   **Bayesian:** Full distribution of uncertainty.
*   **PCA → Clustering:** PCA is the "Filter." We run it before clustering to remove noise and solve the "Curse of Dimensionality."
*   **EM → Latent Data:** Whenever you have a "Missing Data" problem (GMM labels or SSL unlabeled data), EM is the engine that fixes it.

---

## 2. The Core Tradeoffs (The "Which one is better?" Questions)

| Feature | K-Means | GMM |
| :--- | :--- | :--- |
| **Logic** | Distance (Geometry) | Density (Probability) |
| **Shape** | Circles only | Ellipses (Flexible) |
| **Assignment** | Hard (0 or 1) | Soft (0.1, 0.7, etc.) |
| **Speed** | Very Fast | Slower (Iterative) |

| Feature | MLE | MAP |
| :--- | :--- | :--- |
| **Input** | Observed Data only | Data + Prior Belief |
| **Risk** | High (Overfits small data) | Lower (Prior acts as a safety net) |
| **Math** | Easier (Maximize Likelihood) | Slightly harder (Includes Prior) |

---

## 3. The "Why" Trends (Modern Logic)

*   **The Trend of Softness:** We prefer GMM over K-Means when clusters overlap. If a data point is exactly between two clusters, GMM tells the truth: "It's 50/50."
*   **The Trend of Label-Efficiency:** Semi-Supervised Learning (SSL) uses a tiny bit of "Teacher" data (labeled) and a huge amount of "Self-study" data (unlabeled).
*   **The Trend of PCA Centering:** You center data because **Variance is relative**. Centering removes the "shared average" and keeps the "unique differences."

---

## 4. Exam Survival Hacks (How to Remember)

### Mnemonics
*   **EM Algorithm:** 
    *   **E**-step = **E**stimate (Guess the missing labels).
    *   **M**-step = **M**aximize (Update the model based on the guess).
*   **MAP:** **M**LE + **A** **P**rior.
*   **PCA:** **P**attern **C**larification **Axis**.

### "If-Then" Logic for Questions
*   **If** the question mentions "Hidden Variables" or "Latent Data" → **Answer: EM Algorithm.**
*   **If** the question mentions "Overlapping Clusters" or "Ellipses" → **Answer: GMM.**
*   **If** the question asks why we use PCA → **Answer: Curse of Dimensionality / Information Compression.**
*   **If** the question asks how to handle "Small Datasets" → **Answer: Bayesian/MAP (because Priors prevent overfitting).**

### The "Golden Rule" of PCA
In an exam, if they ask about PCA, always mention **Variance**. PCA thinks Variance = Information. Maximize variance to keep the most information.
