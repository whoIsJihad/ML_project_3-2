# Sequence-to-Sequence Models (Seq2Seq)

## Problem: Many-to-Many with Variable Lengths

Standard [[RNN (Recurrent Neural Network)]] assumes fixed input and output lengths.

Real problems have variable-length sequences:
- Machine translation: English sentence → French sentence (different lengths)
- Speech recognition: audio clip (variable duration) → text (variable words)
- Question answering: question (variable length) → answer (variable length)

**Seq2Seq solves this**: two RNNs communicate through fixed-size context vector.

## Architecture: Encoder-Decoder

Seq2Seq has two main components:

### Encoder

Process input sequence, compress information into single vector.

**Structure**:
- Process input tokens one by one
- Each step: update hidden state $h_t$
- Final hidden state $h_T$: compressed representation of entire input

For sequence $x_1, x_2, ..., x_T$:

$$h_1 = f(h_0, x_1)$$
$$h_2 = f(h_1, x_2)$$
$$...$$
$$h_T = f(h_{T-1}, x_T)$$

Output: **context vector** $c = h_T$ (usually) or some function of all hidden states.

### Decoder

Generate output sequence from context vector.

**Structure**:
- Initialize decoder hidden state: $s_0 = c$ (context vector)
- At each step, generate output token
- Use token as input to next step

$$s_1 = g(s_0, y_0)$$
$$y_1 = \text{softmax}(W_o s_1)$$
$$s_2 = g(s_1, y_1)$$
$$y_2 = \text{softmax}(W_o s_2)$$

Where:
- $s_t$ is decoder hidden state
- $y_t$ is probability distribution over vocabulary
- Decoder stops when generating special `<END>` token

## Numeric Example: Machine Translation

**Task**: Translate French → English.

French: "Je suis" (I am)
English: "I am"

### Encoder Phase

**Vocabulary**:
- French: {Je=1, suis=2, `<END>`=3}
- Embeddings (2D): Je=[0.1, -0.2], suis=[0.5, 0.3]

**RNN state update**: $h_t = \tanh(W_{hh} h_{t-1} + W_{xh} e_t)$

Where $e_t$ is embedding of input token.

**Step 1** (Je):
- Embedding: $e_1 = [0.1, -0.2]$
- Hidden state: $h_1 = \tanh(W_{hh} \cdot 0 + W_{xh} e_1) = \tanh(W_{xh} [0.1, -0.2])$
- Assume: $h_1 = [0.08, -0.15]$

**Step 2** (suis):
- Embedding: $e_2 = [0.5, 0.3]$
- Hidden state: $h_2 = \tanh(W_{hh} [0.08, -0.15] + W_{xh} [0.5, 0.3])$
- Assume: $h_2 = [0.22, 0.10]$

**Context vector**: $c = h_2 = [0.22, 0.10]$

This 2D vector now contains "meaning" of "Je suis".

### Decoder Phase

**Vocabulary**:
- English: {I=1, am=2, `<END>`=3}
- Embeddings: I=[0.15, 0.05], am=[0.3, 0.2]
- Start token: `<START>` = [0.0, 0.0]

**Step 1** (Generate first word):

Initialize decoder state: $s_0 = c = [0.22, 0.10]$

Process `<START>` token:
- $s_1 = \tanh(W_{hh}^{\text{dec}} s_0 + W_{xh}^{\text{dec}} e_{\text{START}})$
- $s_1 = \tanh(W_{hh}^{\text{dec}} [0.22, 0.10] + 0)$
- Assume: $s_1 = [0.18, 0.09]$

Predict next word (softmax over vocabulary):
- $\text{logits} = W_o s_1 = [0.5, -0.3, 0.1]$ (3 vocabulary items)
- Softmax: $P(\text{word}) = \frac{e^{\text{logit}}}{\sum e^{\text{logits}}}$

Compute: $e^{0.5} = 1.65, e^{-0.3} = 0.74, e^{0.1} = 1.10$, sum = 3.49

Probabilities: $[1.65/3.49, 0.74/3.49, 1.10/3.49] = [0.47, 0.21, 0.31]$

**Most likely**: Word 1 (I) with probability 0.47.

**Step 2** (Generate second word):

Use predicted word (or teacher-forcing during training):
- True word: I
- Embedding: $e_I = [0.15, 0.05]$

Update decoder state:
- $s_2 = \tanh(W_{hh}^{\text{dec}} s_1 + W_{xh}^{\text{dec}} e_I)$
- $s_2 = \tanh(W_{hh}^{\text{dec}} [0.18, 0.09] + W_{xh}^{\text{dec}} [0.15, 0.05])$
- Assume: $s_2 = [0.24, 0.11]$

Predict next word:
- Logits: $[0.3, 0.8, 0.2]$
- After softmax: $[0.23, 0.61, 0.16]$

**Most likely**: Word 2 (am) with probability 0.61.

**Step 3** (Generate end marker):

Process "am", predict next word:
- Logits: $[0.1, 0.2, 0.9]$
- After softmax: $[0.15, 0.23, 0.62]$

**Most likely**: Word 3 (`<END>`) with probability 0.62.

**Output sequence**: [I, am, `<END>`]

Decoded: "I am" ✓

## Problem: Information Bottleneck

Context vector $c$ must contain ALL information from input sequence.

For long sequences, compressing into fixed-size vector loses information.

Example: Translating 50-word document into single 256D vector.

**Result**: Decoder struggles for long outputs. Last input words matter more than early ones.

Empirical observation: Translation quality degrades for sentences > 20 words.

## Solution: Attention Mechanism

Instead of single context vector, decoder attends to all encoder hidden states.

At each decoding step:
1. Compare decoder state with each encoder hidden state
2. Compute attention weights (learned)
3. Blend encoder hidden states using weights
4. Use blended vector + decoder state to generate output

### Attention Equations

At decoder step $t$:

**Attention scores** (similarity between decoder and encoder):
$$e_{t,i} = \text{score}(s_t, h_i)$$

Common scoring functions:
- Dot product: $s_t^T h_i$
- Learned: $v^T \tanh(W_a [s_t; h_i])$

**Attention weights** (softmax over scores):
$$\alpha_{t,i} = \frac{\exp(e_{t,i})}{\sum_j \exp(e_{t,j})}$$

**Context vector** (weighted sum of encoder states):
$$c_t = \sum_i \alpha_{t,i} h_i$$

**Use for decoding**:
$$s_t = \tanh(W_c [s_{t-1}; c_t])$$
$$y_t = \text{softmax}(W_o s_t)$$

### Numeric Example: Attention

**Encoder hidden states** (after processing input):
- $h_1 = [0.5, 0.2]$ (after "Je")
- $h_2 = [0.22, 0.1]$ (after "suis")

**Decoder state** at step 2 (generating second word):
- $s_2 = [0.24, 0.11]$

**Scoring** (dot product):
- $e_{2,1} = s_2 \cdot h_1 = 0.24(0.5) + 0.11(0.2) = 0.12 + 0.022 = 0.142$
- $e_{2,2} = s_2 \cdot h_2 = 0.24(0.22) + 0.11(0.1) = 0.0528 + 0.011 = 0.0638$

**Softmax**:
- $\exp(0.142) = 1.152, \exp(0.0638) = 1.066$
- Sum: 2.218
- Weights: $\alpha_{2,1} = 1.152/2.218 = 0.519, \alpha_{2,2} = 1.066/2.218 = 0.481$

**Context**:
$$c_2 = 0.519 \times [0.5, 0.2] + 0.481 \times [0.22, 0.1]$$
$$= [0.260, 0.104] + [0.106, 0.048]$$
$$= [0.366, 0.152]$$

Decoder uses this blended vector $c_2$ (slightly weighted toward first encoder state).

## Attention Visualization

After training, attention weights reveal which encoder tokens matter for each output:

```
French input:   Je    suis
                |      |
English output: I ← ←  am ← ←
                |      |
```

Attention matrix (rows = output steps, columns = input steps):
```
I     [0.8, 0.2]  (mostly attends to "Je")
am    [0.3, 0.7]  (mostly attends to "suis")
<END> [0.5, 0.5]  (attends to both equally)
```

This learned attention makes model interpretable.

## Teacher Forcing During Training

During training, decoder has access to true output tokens (not predictions).

**Without teacher forcing**:
- Step 1: Predict first word (might be wrong)
- Step 2: Use predicted word as input (error propagates)
- Training is slow, unstable

**With teacher forcing**:
- Step 1: Use true first word as input
- Step 2: Use true second word as input
- Training is fast, stable

**Trade-off**: Model sees inputs it never sees at test time (distribution mismatch).

**Solution**: Scheduled sampling (gradually transition from teacher forcing to prediction during training).

## Beam Search Decoding

At test time, don't just pick highest-probability word at each step.

Use **beam search**: keep top K hypotheses (beams) at each step.

Example: Beam size K=3

**Step 1**: Generate first word, keep top 3 probabilities:
- I: 0.47
- am: 0.23
- `<END>`: 0.30

**Step 2**: For each beam, generate next word:

From "I" (prob 0.47):
- I am: 0.47 × 0.61 = 0.287
- I I: 0.47 × 0.15 = 0.070
- I `<END>`: 0.47 × 0.24 = 0.113

From "am" (prob 0.23):
- am I: 0.23 × 0.40 = 0.092
- am am: 0.23 × 0.50 = 0.115
- am `<END>`: 0.23 × 0.10 = 0.023

From "`<END>`" (prob 0.30):
- Can't continue (end token)

Keep top 3 paths:
1. "I am" (0.287)
2. "I" (0.47 from step 1; incomplete)
3. "am am" (0.115)

Continue until all beams end.

Choose path with highest total probability.

**Result**: Better translations than greedy (pick max at each step).

## Bidirectional Encoders

Encode in both directions, concatenate:

$$h^{\text{fwd}}_t = \text{RNN}_{\text{fwd}}(...)$$
$$h^{\text{bwd}}_t = \text{RNN}_{\text{bwd}}(...)$$
$$h_t = [h^{\text{fwd}}_t; h^{\text{bwd}}_t]$$

Allows decoder to use context from both sides of each input word.

Works well for tasks like tagging (where full sequence is available at test time).

Cannot use for real-time applications.

## Modern Variants

### Multi-Head Attention

Compute multiple attention heads in parallel:
- Head 1: Attends to nouns
- Head 2: Attends to verb arguments
- Head 3: Attends to long-range dependencies

Each head learns different patterns.

Outputs concatenated and passed to next layer.

### [[Transformers]]

Replace RNNs entirely with self-attention.

Advantages:
- Fully parallelizable (no sequential dependencies)
- Better for long sequences
- Easier to train at scale

Disadvantages:
- More parameters
- Slower for short sequences

## BLEU Score: Evaluation Metric

How to measure translation quality?

**BLEU** (Bilingual Evaluation Understudy): Compare generated translation to reference.

$$\text{BLEU} = 0.25 \sum_{n=1}^{4} w_n \log p_n$$

Where $p_n$ = fraction of n-grams in output that appear in reference.

Example:
- Reference: "The cat sat on the mat"
- Generated: "The cat sat on a mat"

1-grams: The(✓) cat(✓) sat(✓) on(✓) a(✗) mat(✓) → 5/6 = 0.833
2-grams: The-cat(✓) cat-sat(✓) sat-on(✓) on-a(✗) a-mat(✗) → 3/5 = 0.6
3-grams: The-cat-sat(✓) cat-sat-on(✓) sat-on-a(✗) on-a-mat(✗) → 2/4 = 0.5
4-grams: 0/3 = 0

BLEU ≈ 0.25 × ln(0.833 × 0.6 × 0.5 × 0) = undefined (0 n-grams match)

In practice: BLEU ranges 0-100. Good translation: > 30.

## Summary

Seq2Seq uses encoder to compress input, decoder to generate output.

Attention mechanism allows decoder to focus on relevant encoder parts.

Works well for translation, summarization, question answering.

Modern approach: [[Transformers]] (faster, scales better).
