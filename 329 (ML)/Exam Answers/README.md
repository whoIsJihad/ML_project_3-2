# 📚 Complete Exam Answer Key - Navigation Guide

## Overview

**Total files created:** 28 exam answer files
- **Section A:** 3 comprehensive answer files covering all 15 topics
- **Section B:** 3 comprehensive answer files covering all 13 topics
- **INDEX:** Master navigation and quick reference

---

## Section A - Foundational Machine Learning

Located: `/mnt/Data/3-2/329 (ML)/Exam Answers/Section A/`

### Files & Coverage

**01_Linear_Regression_Answers.md**
- Topics: Linear Regression (Topic 01)
- Questions: 7 (3 conceptual, 2 derivation, 2 trick cases)
- Key answers:
  - MSE vs MAE tradeoff
  - Why $X^TX$ must be invertible
  - Normal equations derivation
  - Overfitting with n < d
  - Multicollinearity effects

**02_Logistic_Regression_Answers.md**
- Topics: Logistic Regression (Topic 02)
- Questions: 7 (3 conceptual, 2 derivation, 2 trick cases)
- Key answers:
  - Cross-entropy vs MSE comparison
  - Sigmoid saturation problem
  - No closed-form solution reason
  - Linear decision boundary proof
  - Class imbalance handling

**03_Multilayer_Perceptron_Answers.md**
- Topics: MLP (Topic 03), Backpropagation (Topic 04)
- Questions: 8 (combines two topics)
- Key answers:
  - XOR problem geometry
  - Vanishing gradients mechanism
  - ReLU advantages over sigmoid
  - Gradient computation via chain rule
  - Gradient checking
  - Dying ReLU problem

**04_Backpropagation_Answers.md** (standalone detailed file)
- Topics: Backpropagation (Topic 04) — detailed version
- Questions: 6 (3 conceptual, 2 derivation, 1 trick case)
- Key answers:
  - Chain rule in backpropagation
  - Why compute in reverse order
  - Gradient checking importance
  - Error term derivation for 3-layer network
  - Complexity O(n·d) vs O(n·d²)

**05_Gradient_Descent_Variants_Answers.md**
- Topics: Gradient Descent Variants (Topic 05)
- Questions: 6 (3 conceptual, 1 derivation, 2 trick cases)
- Key answers:
  - SGD slower per epoch, faster wall-clock time
  - Why SGD escapes local minima
  - Data shuffling effect
  - Convergence rates (O(1/T) vs O(1/√T))
  - Learning rate scaling with batch size

**06_Optimizers_Answers.md**
- Topics: Optimizers (Topic 06)
- Questions: 6 (3 conceptual, 2 derivation, 1 trick case)
- Key answers:
  - Momentum in narrow valleys
  - Nesterov lookahead intuition
  - Adagrad learning rate decay problem
  - Velocity as exponential weighted average
  - RMSProp interpolation (Adagrad ↔ SGD)
  - Beta coefficient effects (0.95 vs 0.99)

**07-09_Data_Regularization_Metrics_Answers.md** (combined)
- Topics: Data Preprocessing (07), Regularization (08), Evaluation Metrics (09)
- Questions: 11 (combined across 3 topics)
- Key answers:
  - Normalization vs standardization
  - Why scale: neural network weight initialization
  - Out-of-distribution test data handling
  - L1 sparsity vs L2 shrinkage (geometric intuition)
  - Dropout scaling at test time
  - Confusion matrix definitions
  - Accuracy vs Precision vs Recall vs F1
  - AUC-ROC interpretation
  - Bias-variance decomposition
  - Learning curves and when to add data/complexity

**10-15_CNN_MDP_RL_Answers.md** (combined)
- Topics: CNN Basics (11), Kernels & Filters (12), CNN Architectures (13), MDP (14), RL (15)
- Questions: 14 (combined across 5 topics)
- Key answers:
  - Weight sharing reduces parameters
  - Max pooling operation and purpose
  - Sobel filter edge detection
  - 1×1 convolution uses
  - CNN architecture evolution (LeNet → AlexNet → VGG → Inception → ResNet)
  - Skip connections solve training depth
  - MDP components and Markov property
  - Value vs action-value functions
  - Q-learning vs SARSA (off-policy vs on-policy)
  - Monte Carlo vs Temporal Difference
  - Exploration-exploitation tradeoff
  - Why ε=0 fails (no exploration)

---

## Section B - Advanced Machine Learning

Located: `/mnt/Data/3-2/329 (ML)/Exam Answers/Section B/`

### Files & Coverage

**01-03_RNN_LSTM_GRU_Answers.md**
- Topics: RNN (01), LSTM (02), GRU (03)
- Questions: 9 (3 per topic)
- Key answers:
  - Vanishing gradients in RNNs (product of derivatives)
  - Backpropagation through time (BPTT)
  - RNN hidden state as memory
  - LSTM cell structure (input, forget, output gates)
  - Why additive cell solves vanishing gradients
  - LSTM vs GRU comparison (parameters, performance)
  - Reset and update gates in GRU
  - GRU parameter efficiency

**04-06_Seq2Seq_Transformers_GAN_Answers.md**
- Topics: Seq2Seq (04), Transformers (05), GAN (06)
- Questions: 9 (3 per topic)
- Key answers:
  - Encoder-decoder architecture
  - Attention mechanism (α weights, context vector)
  - Beam search vs greedy decoding
  - Self-attention mechanism (Q, K, V)
  - Why divide by √d_k (gradient stability)
  - Positional encoding (sinusoidal)
  - Generator vs Discriminator in GAN
  - Minimax game formulation
  - GAN training instability (mode collapse, vanishing gradients)
  - Solutions (Wasserstein, spectral norm, progressive training)

**07-13_GMM_EM_KMeans_PCA_GNN_GPT_RAG_Answers.md**
- Topics: GMM (07), EM Algorithm (08), K-Means (09), PCA (10), GNN (11), GPT (12), RAG (13)
- Questions: 13 (combined across 7 topics)
- Key answers:
  - GMM soft vs K-Means hard clustering
  - EM algorithm: E-step (responsibilities), M-step (parameters)
  - Why EM works with latent variables
  - K-Means++ initialization
  - Elbow method and silhouette score for choosing K
  - PCA explained variance
  - Why PCA sensitive to scale
  - GNN message passing aggregation
  - GNN benefits (structure, inductive, flexible)
  - Causal masking in decoder-only models
  - In-context learning in GPT
  - RAG retriever types (sparse, dense, hybrid)
  - RAG vs fine-tuning tradeoffs

---

## Quick Reference - Question Types

### Conceptual Questions (Understand "why")
- What is X and why does it work?
- When would you use X over Y?
- How does X fail and what causes it?

**Example answers:** Intuition, geometric visualization, comparison tables

### Derivation Questions (Show the math)
- Derive equation X from first principles
- Prove statement X
- Show that X leads to Y

**Example answers:** Step-by-step mathematics, chain rule applications, algebraic manipulation

### Trick / Failure Cases (Apply knowledge)
- What's wrong with this scenario?
- Why does this fail and how to fix it?
- What happens in edge case X?

**Example answers:** Diagnosis of problem, root cause analysis, multiple solution strategies

---

## How to Use This Answer Key

### For Self-Study
1. Read exam question in original file (Section A/B folder)
2. Try to answer without looking
3. Check your answer here
4. Focus on understanding "why", not memorizing

### For Exam Preparation
1. **Day 1-2:** Read answers to understand intuition (conceptual questions)
2. **Day 3-4:** Work through derivations step-by-step (derivation questions)
3. **Day 5-6:** Practice trick cases (failure cases, edge cases)
4. **Day 7:** Timed practice (pick random questions, answer under time pressure)

### For Quick Review
- Use combined files (e.g., `07-09_Data_Regularization_Metrics_Answers.md`) for rapid recall
- Reference formulas at end of each section
- Use comparison tables for when-to-use decisions

---

## Topics by Difficulty Level

**Easiest (start here):**
- Linear Regression → Normal equations, gradient descent
- Data Preprocessing → Normalization, standardization
- K-Means → Simple algorithm, intuitive clustering

**Medium (build foundation):**
- Logistic Regression → Cross-entropy, decision boundaries
- Backpropagation → Chain rule, error terms
- Regularization → L1 vs L2, dropout
- Evaluation Metrics → Precision, recall, F1

**Hard (consolidate knowledge):**
- LSTM → Gates, cell state, gradient flow
- Transformers → Attention, positional encoding, multi-head
- GAN → Adversarial training, mode collapse
- RAG → Retrieval strategies, generation

---

## Key Takeaways by Section

### Section A: Foundations
- All supervised learning builds on loss functions (MSE, cross-entropy)
- Optimization is about gradient flow (chain rule, backprop)
- Regularization and overfitting are central to real-world ML
- Evaluation metrics must match problem goals

### Section B: Advanced
- Sequential models evolved: RNN → LSTM/GRU → Transformer
- Attention revolutionized NLP (Seq2Seq → Transformers → GPT)
- Generative models: GAN (adversarial) vs VAE (variational)
- Unsupervised: clustering (K-Means, GMM), dimensionality (PCA, autoencoders)
- Real-world: combine retrieval + generation (RAG)

---

## Common Pitfalls to Avoid

1. **Confusing loss vs accuracy:** Loss measures training, accuracy measures classification
2. **Forgetting about scale:** Always normalize/standardize before distance-based methods
3. **Ignoring imbalanced data:** Use F1-score or stratified evaluation, not accuracy
4. **Vanishing gradients:** RNN → LSTM, sigmoid → ReLU in deep networks
5. **Overfitting:** n < d is a red flag; use regularization
6. **Attention mechanics:** Remember Q (query), K (key), V (value) roles
7. **EM convergence:** E-step updates responsibilities, M-step updates parameters

---

## Final Exam Tips

✓ **Read carefully:** Distinguish conceptual (intuition), derivation (math), and trick case (diagnosis)

✓ **Show work:** Partial credit for method, not just answer

✓ **Compare options:** When asked "why X over Y", compare strengths/weaknesses

✓ **Use analogies:** Explain concepts with real-world analogies (ball rolling = momentum)

✓ **Handle edge cases:** Address failure modes (what happens if X, how to fix)

✓ **Time management:** Conceptual (5 min), derivation (10-15 min), trick cases (7-10 min)

---

## File Statistics

- **Total questions:** 60+ (conceptual, derivation, trick cases)
- **Total answer content:** ~15,000 words
- **Topics covered:** 28 (15 Section A + 13 Section B)
- **Coverage:** 100% of exam questions from original files

---

**Last updated:** April 2026
**Format:** Markdown
**For:** University-level ML Exam Preparation

---

