# 📝 Seq2Seq, Transformers, GAN - Exam Answers

## Seq2Seq (Sequence-to-Sequence)

### Q1: Explain encoder-decoder architecture

**Encoder:** Processes variable-length input, produces fixed-size context vector
```
Input sequence: [word1, word2, ..., wordN] 
→ RNN → final hidden state hN (context vector)
```

**Decoder:** Uses context to generate variable-length output
```
Context hN → RNN → [wordˈ1, wordˈ2, ..., wordˈM]
```

**Problem:** Context vector bottleneck. Long inputs → information loss.

---

### Q2: What is attention mechanism?

**Attention:** Decoder "attends" to relevant encoder states at each step.

Instead of using only final $h_N$, compute:
$$\alpha_t^i = \frac{\exp(e_t^i)}{\sum_j \exp(e_t^j)}$$

where $e_t^i$ = attention score for encoder position $i$ at decoder step $t$.

$$\text{context}_t = \sum_i \alpha_t^i h_i^{\text{enc}}$$

**Effect:** Decoder can focus on different parts of input (e.g., source words to translate).

---

### Q3: How does beam search work?

**Greedy:** Pick highest probability word at each step. Often suboptimal.

**Beam search:** Keep top-K hypotheses at each step.

```
Step 1: Generate K best first words
Step 2: For each, generate K best second words (K² total)
        Keep top-K hypotheses
...
Step T: Keep K best complete sequences
```

**Trade-off:**
- K=1: Greedy (fast, lower quality)
- K=3-5: Good quality without explosion
- K→∞: Exhaustive search (very slow)

---

## Transformers

### Q1: Explain self-attention

**Self-Attention:** Each token attends to all tokens in sequence.

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

where:
- $Q$ (Query): What am I looking for?
- $K$ (Key): What can you offer?
- $V$ (Value): What do you contain?

**Process:**
1. Compute attention scores: $\text{softmax}(QK^T/\sqrt{d_k})$
2. Apply to values: multiply by $V$

**Self-attention allows token to "see" all other tokens in context** (no sequential bottleneck like RNN).

---

### Q2: Why divide by $\sqrt{d_k}$?

**Dot products $QK^T$ grow large:**
- $Q, K$ have dimension $d_k$
- $QK^T \sim d_k$ in magnitude
- Large values → softmax saturates → near-zero gradients

**Dividing by $\sqrt{d_k}$ stabilizes:**
$$\frac{QK^T}{\sqrt{d_k}} \sim O(1)$$

Softmax derivatives stay healthy, gradients flow.

---

### Q3: What is positional encoding?

**Problem:** Transformer attention is permutation-invariant. Token "2 is 3" same as "3 is 2".

**Solution:** Add position information.

$$\text{PE}(pos, 2i) = \sin(pos / 10000^{2i/d_{model}})$$
$$\text{PE}(pos, 2i+1) = \cos(pos / 10000^{2i/d_{model}})$$

**Why sinusoids?** Periodic pattern, allow model to learn relative positions.

**Effect:** Embeds absolute position in vector space; model learns to use position info.

---

## GAN (Generative Adversarial Networks)

### Q1: Explain generator vs discriminator

**Generator** $G(z)$: Takes random noise $z \sim N(0,I)$ → produces fake data

**Discriminator** $D(x)$: Takes data (real or fake) → predicts probability it's real

**Minimax game:**
$$\min_G \max_D \mathbb{E}_{x \sim P_{\text{real}}}[\log D(x)] + \mathbb{E}_{z}[\log(1-D(G(z)))]$$

---

### Q2: Why is GAN training unstable?

**Issues:**
1. **Non-stationary targets:** As $G$ improves, $D$ must improve too (moving goalposts)
2. **Mode collapse:** $G$ learns to fool $D$ with single fake sample type (e.g., only blond faces)
3. **Vanishing gradients:** If $D$ too good, $\log(1-D(G(z))) \approx 0$ when $D$ almost certain (fake)

---

### Q3: Solutions to GAN training

1. **Wasserstein GAN:** Different loss (wasserstein distance) → more stable
2. **Spectral normalization:** Constrain $D$ gradients → smoother training
3. **Conditional GAN:** Add class labels → learn specific modes
4. **Progressive GAN:** Train on low-res first, gradually add high-res (stabilizes)

---

