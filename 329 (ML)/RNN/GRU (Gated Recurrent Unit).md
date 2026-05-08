# GRU (Gated Recurrent Unit)

## Motivation

[[LSTM (Long Short-Term Memory)]] has 4 gates and 2 state variables.

This adds computational overhead.

**Question**: Can we achieve similar performance with fewer parameters?

**Answer**: Yes, through GRU (Gated Recurrent Unit).

GRU simplifies LSTM by:
1. Combining cell and hidden state into single state
2. Reducing 4 gates to 2 gates
3. Removing separate cell state

Result: ~67% of LSTM parameters, similar performance.

## GRU Architecture

### Two Gates

**Reset gate** $r_t$:
$$r_t = \sigma(W_r h_{t-1} + U_r x_t + b_r)$$

Controls what fraction of previous hidden state to use.

**Update gate** $z_t$:
$$z_t = \sigma(W_z h_{t-1} + U_z x_t + b_z)$$

Controls what fraction of new candidate state to use.

### Candidate Hidden State

$$\tilde{h}_t = \tanh(W_h (r_t \odot h_{t-1}) + U_h x_t + b_h)$$

The reset gate modulates the previous hidden state **before** input.

### Hidden State Update

$$h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t$$

Linear interpolation between previous state and candidate.

This is the **only state variable** (no separate cell state).

## How It Works: Intuition

### Reset Gate Mechanism

Reset gate modulates input from previous hidden state.

- $r_t = 1$: use full previous hidden state in candidate
- $r_t = 0$: ignore previous hidden state, compute candidate from input alone

**When reset is low**: network "forgets" previous state (like opening a new context).

**When reset is high**: network uses historical information (like continuing thought).

### Update Gate Mechanism

Update gate controls balance between old and new state.

- $z_t = 0$: $h_t = h_{t-1}$ (keep previous state unchanged)
- $z_t = 1$: $h_t = \tilde{h}_t$ (use new candidate entirely)

**When update is low**: state changes slowly, retains memory.

**When update is high**: state responds immediately to new input.

## Numeric Simulation: Sentiment Tracking

**Task**: Process sentence word-by-word, track sentiment.

Sentence: "This movie is brilliant but the ending was terrible."

Words: [This, movie, is, brilliant, but, the, ending, was, terrible]

Sentiment should start neutral → increase (brilliant is positive) → decrease (terrible is negative).

### Setup
- Hidden dimension: 2 (represent sentiment + confidence)
- Initial state: $h_0 = [0, 0]$ (neutral)

### Step 1: "This"

Reset gate: $r_1 = \sigma(...)$ = 0.5 (mix old and new)
Update gate: $z_1 = \sigma(...) = 0.8$ (mostly update to new)
Candidate: $\tilde{h}_1 = \tanh(...) = [0.1, 0.2]$ (slightly positive, low confidence)

$$h_1 = (1-0.8) \times [0,0] + 0.8 \times [0.1, 0.2] = [0.08, 0.16]$$

### Step 2: "movie"

Reset gate: $r_2 = 0.6$ (keep some context)
Update gate: $z_2 = 0.3$ (slow update, maintain belief)
Candidate: $\tilde{h}_2 = [0.15, 0.3]$ (slightly positive, moderate confidence)

$$h_2 = 0.7 \times [0.08, 0.16] + 0.3 \times [0.15, 0.3] = [0.102, 0.202]$$

State barely changes. Important word "movie" doesn't shift sentiment much.

### Step 3-4: "is", "brilliant"

"is" is neutral. State remains similar.

"brilliant" is strongly positive.

Reset gate: $r_4 = 0.7$ (use context)
Update gate: $z_4 = 0.9$ (respond strongly to positive word)
Candidate: $\tilde{h}_4 = [0.95, 0.85]$ (strongly positive, high confidence)

$$h_4 = 0.1 \times h_3 + 0.9 \times [0.95, 0.85] = [0.86, 0.77]$$

State shifts significantly positive.

### Step 5: "but"

"but" signals contrast. Something negative coming.

Reset gate: $r_5 = 0.4$ (reduce previous context weight)
Update gate: $z_5 = 0.5$ (moderate update)
Candidate: $\tilde{h}_5 = [-0.2, 0.4]$ (slightly negative, uncertainty increases)

$$h_5 = 0.5 \times [0.86, 0.77] + 0.5 \times [-0.2, 0.4] = [0.33, 0.585]$$

Sentiment decreases but doesn't collapse (uncertainty increases).

### Steps 6-7: "the", "ending"

Words are building context for upcoming negative sentiment.

Reset gate stays moderate. Update gate stays low (< 0.5).

State barely changes.

### Step 8: "was"

Auxiliary verb, neutral. State unchanged.

### Step 9: "terrible"

Strongly negative word.

Reset gate: $r_9 = 0.6$ (use some context of positive sentiment from "brilliant", to measure contrast)
Update gate: $z_9 = 0.95$ (respond strongly)
Candidate: $\tilde{h}_9 = [-0.9, 0.95]$ (strongly negative, high uncertainty)

$$h_9 = 0.05 \times h_8 + 0.95 \times [-0.9, 0.95] = [-0.86, 0.92]$$

First dimension (sentiment) becomes strongly negative.
Second dimension (uncertainty) remains high.

### Result

GRU tracked sentiment transitions:
- Neutral (start) → positive (brilliant) → mixed/uncertain (but...terrible)

The **update gate** controlled learning speed (slow for normal words, fast for sentiment adjectives).

The **reset gate** controlled context (what information to use from previous state).

## Parameter Count Comparison

### LSTM: 4 gates + 2 states

Per gate/state: $n_h \times n_h + n_x \times n_h + n_h$ (multiply by weights matrix + bias)

Total: $4 \times (n_h^2 + n_x n_h + n_h)$ parameters for hidden component alone.

For $n_h = 256, n_x = 100$:
$$4 \times (256^2 + 100 \times 256 + 256) = 4 \times (65536 + 25600 + 256) = 366,912 \text{ params}$$

### GRU: 2 gates + 1 state

Plus candidate state computation (similar to cell computation).

Actually: $3 \times (n_h^2 + n_x n_h + n_h)$ parameters.

For same dimensions:
$$3 \times (65536 + 25600 + 256) = 275,184 \text{ params}$$

**GRU: 75% of LSTM parameters** (not 67% when counting more carefully).

## Gradient Flow in GRU

Backward equation through update gate:

$$\frac{\partial h_t}{\partial h_{t-1}} = (1 - z_t) + z_t \frac{\partial \tilde{h}_t}{\partial h_{t-1}}$$

The $(1 - z_t)$ term creates addition path (like LSTM cell state).

When $z_t$ is low (< 0.5), first term dominates: $\frac{\partial h_t}{\partial h_{t-1}} \approx 1 - z_t > 0.5$

Gradients don't vanish as quickly as standard RNN.

**Comparison**:
- Standard RNN: $\frac{\partial h_t}{\partial h_{t-1}} = W_{hh} \tanh'(...) < 0.5$ (product of small values)
- GRU: $\frac{\partial h_t}{\partial h_{t-1}} = (1-z_t) + \text{other terms}$, can be close to 1

GRU doesn't fix vanishing gradients as completely as LSTM (because $z_t$ is not always optimal).

But the improvement over standard RNN is substantial.

## Computational Efficiency

### Per Time Step

**Standard RNN**: 1 matrix multiply for hidden state update + 1 for output

**GRU**: 3 matrix multiplies (2 gates + candidate) + 1 for output = 3× more

**LSTM**: 4 matrix multiplies + 1 for output = 4× more

In wall-clock time:
- RNN: 1 unit
- GRU: 2.5-3 units
- LSTM: 3.5-4 units

GRU is ~25% faster than LSTM.

### Sequence Processing (Truncated BPTT)

For sequence length $T = 100$:

**RNN**: $T = 100$ multiplies
**GRU**: $3T = 300$ multiplies
**LSTM**: $4T = 400$ multiplies

GRU is 25% faster per sequence.

Speed doesn't scale linearly (memory bandwidth, GPU utilization matter).

In practice, LSTM might be only 10-20% slower than GRU on GPU.

## When to Use GRU vs LSTM

### Prefer GRU when:
- Computational budget is tight (mobile, real-time)
- Dataset is small (fewer parameters = less overfitting)
- Sequence length < 50 steps (vanishing gradient less severe)
- Implementation simplicity matters

### Prefer LSTM when:
- Sequence length > 100 steps
- Maximum performance needed (LSTM slightly better on hard tasks)
- Computational resources available
- Existing codebase uses LSTM (consistency matters)

### In Practice:
Most practitioners default to LSTM as it's more established.

GRU performance is often within 5% of LSTM.

Modern trend: Replace both with [[Transformers]] for long sequences.

## Hybrid Approaches

### Stacking Multiple Layers

Both GRU and LSTM can be stacked:

Layer 1 output $h^{(1)}_t$ → Layer 2 input.

Stack 2-3 layers for better capacity.

Each layer has its own set of gates and parameters.

### Bidirectional GRU

Forward: process sequence left-to-right
Backward: process sequence right-to-left

$$h_t = [h^{\text{forward}}_t; h^{\text{backward}}_t]$$

Doubles parameters. Requires full sequence (can't use for real-time).

Example: Named entity recognition can use context from both sides of word.

## LSTM vs GRU: Empirical Comparison

**On machine translation**:
- LSTM: BLEU score 24.3
- GRU: BLEU score 24.1
- Difference: < 1% (not significant)

**On sentiment analysis** (small dataset):
- LSTM: 89.5% accuracy
- GRU: 88.8% accuracy
- GRU: 25% fewer parameters, similar performance

**On language modeling** (Penn Treebank):
- LSTM: perplexity 82.0
- GRU: perplexity 82.8
- LSTM: slightly better, but GRU is competitive

Real experiments show GRU within 2-5% of LSTM on most tasks.

## Summary

GRU is simplified LSTM:
- 2 gates instead of 4
- 1 state instead of 2
- ~75% of LSTM parameters
- ~75-90% of LSTM performance
- ~20-25% faster

Both solve vanishing gradients through gating.

Choose GRU for efficiency, LSTM for maximum performance.

Modern alternative: [[Transformers]] for very long sequences or parallel training.
