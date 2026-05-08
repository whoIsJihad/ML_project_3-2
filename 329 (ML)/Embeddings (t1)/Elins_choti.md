
# The Illustrated Word2vec

![](https://jalammar.github.io/images/word2vec/word2vec.png)  

Word2vec is a method to efficiently create word embeddings. Word embeddings power many NLP applications: next-word prediction, machine translation, semantic search. The key insight is that words appearing in similar contexts have similar meanings — we capture this by representing each word as a vector of numbers.

# Personality Embeddings: What are you like?

The Big Five Personality Traits test scores personality along multiple dimensions. For example, on the introversion/extraversion axis, scores range from -1 (introvert) to +1 (extrovert).

![](https://jalammar.github.io/images/word2vec/introversion-extraversion-1.png)

One dimension isn't sufficient to capture personality. Adding more dimensions provides richer information:

![](https://jalammar.github.io/images/word2vec/two-traits-vector.png)  

Vectors can be compared using **cosine similarity** to find how similar two people are. Which of these two people is more similar to a given person?

![](https://jalammar.github.io/images/word2vec/personality-two-persons.png)

![](https://jalammar.github.io/images/word2vec/cosine-similarity.png)  

Using all  five personality dimensions gives us much richer comparisons:
 
![](https://jalammar.github.io/images/word2vec/big-five-vectors.png)  

Cosine similarity works for any number of dimensions:

![](https://jalammar.github.io/images/word2vec/embeddings-cosine-personality.png)  

**Key insight**: We can represent objects (people, words, items) as vectors of numbers, and easily calculate similarity between them using cosine similarity.

![](https://jalammar.github.io/images/word2vec/section-1-takeaway-vectors-cosine.png)  

# Word Embeddings

Word embeddings represent words as vectors. For example, here's a word embedding for "king" (GloVe vector trained on Wikipedia):

`[ 0.50451 , 0.68607 , -0.59517 , -0.022801, 0.60046 , -0.13498 , -0.08813 , 0.47377 , -0.61798 , -0.31012 , -0.076666, 1.493 , -0.034189, -0.98173 , 0.68229 , 0.81722 , -0.51874 , -0.31503 , -0.55809 , 0.66421 , 0.1961 , -0.13495 , -0.11476 , -0.30344 , 0.41177 , -2.223 , -1.0756 , -1.0783 , -0.34354 , 0.33505 , 1.9927 , -0.04234 , -0.64319 , 0.71125 , 0.49159 , 0.16754 , 0.34344 , -0.25663 , -0.8523 , 0.1661 , 0.40102 , 1.1685 , -1.0137 , -0.21585 , -0.15155 , 0.78321 , -0.91241 , -1.6106 , -0.64426 , -0.51042 ]`

It's a list of 50 numbers. Visualized with color coding (red = high values, blue = low values):

![](https://jalammar.github.io/images/word2vec/king-white-embedding.png)  

![](https://jalammar.github.io/images/word2vec/king-colored-embedding.png)  

Comparing embeddings for "King", "Man", and "Woman":

![](https://jalammar.github.io/images/word2vec/king-man-woman-embedding.png)  

"Man" and "Woman" are more similar to each other than either is to "king" — the embeddings capture semantic relationships.

Comparing more words:

![](https://jalammar.github.io/images/word2vec/queen-woman-girl-embeddings.png)  

Observations:
1. A red column runs through all words — they're similar along that dimension.
2. "woman" and "girl" are similar in many places; same with "man" and "boy".
3. "boy" and "girl" share some dimensions but differ from "man" and "woman" (youth dimension?).
4. Words for people vs. "water" (an object) show clear differences.
5. "king" and "queen" are similar to each other and distinct from others (royalty dimension?).

## Analogies

One remarkable property of embeddings: we can perform arithmetic on them and get meaningful results. This reveals the semantic structure the vectors have learned.

The famous example: "king" - "man" + "woman":

![](https://jalammar.github.io/images/word2vec/king-man+woman-gensim.png)  

Using Gensim, we can add/subtract word vectors and find the most similar words. The result is near "queen", showing embeddings capture analogical relationships.

![](https://jalammar.github.io/images/word2vec/king-analogy-viz.png)  

# Language Modeling

Language models predict the next word given context. They power smartphone autocomplete, machine translation, and many NLP tasks.

![](https://jalammar.github.io/images/word2vec/swiftkey-keyboard.png)  

The model takes previous words as input and outputs a probability distribution over all possible next words:

![](https://jalammar.github.io/images/word2vec/language_model_blackbox_output_vector.png)  

Early neural language models ([Bengio 2003](http://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf)) learned embeddings as a byproduct of training. The key insight: embedding matrices are naturally learned during neural network training to convert words into vectors for computation.

![](https://jalammar.github.io/images/word2vec/neural-language-model-prediction.png)  

The embedding matrix is learned during training and contains an embedding for each vocabulary word:

![](https://jalammar.github.io/images/word2vec/neural-language-model-embedding.png)  

# Language Model Training

Language models have unlimited training data — any large text corpus (Wikipedia, books, web pages) can be converted into training examples automatically.

The key technique: **sliding window** automatically generates (context, target) pairs:

![](https://jalammar.github.io/images/word2vec/wikipedia-sliding-window.png)  

The sliding window generates training samples. For the phrase "Thou shalt not make a machine...":

![](https://jalammar.github.io/images/word2vec/lm-sliding-window.png)  

The first two words are features, the third is the label:

![](https://jalammar.github.io/images/word2vec/lm-sliding-window-2.png)  

Sliding further generates more training pairs:

![](https://jalammar.github.io/images/word2vec/lm-sliding-window-3.png)  

![](https://jalammar.github.io/images/word2vec/lm-sliding-window-4.png)  

## Bidirectional Context

Knowing words after a target word is as informative as knowing words before it. Using context on both sides improves embeddings.

Instead of predicting a word from context, we can use a different approach: given a word, predict its context (neighboring words).

# Continuous Bag of Words (CBOW)

CBOW uses bidirectional context: instead of predicting a word from only 2 words before it, we use 2 words before AND 2 after:

![](https://jalammar.github.io/images/word2vec/continuous-bag-of-words-example.png)  

The training dataset:

![](https://jalammar.github.io/images/word2vec/continuous-bag-of-words-dataset.png)  

# Skipgram

Skipgram reverses the task: given a center word, predict neighboring words. Each window position creates multiple training samples (one for each neighboring word):

![](https://jalammar.github.io/images/word2vec/skipgram-sliding-window.png)  

The green slot is input, pink boxes are possible outputs. This creates four separate training samples:

![](https://jalammar.github.io/images/word2vec/skipgram-sliding-window-samples.png)  

Visualizing the window:

![](https://jalammar.github.io/images/word2vec/skipgram-sliding-window-1.png)  

Generates these samples:

![](https://jalammar.github.io/images/word2vec/skipgram-sliding-window-2.png)  

Sliding to the next position:

![](https://jalammar.github.io/images/word2vec/skipgram-sliding-window-3.png)  

More samples:

![](https://jalammar.github.io/images/word2vec/skipgram-sliding-window-4.png)  

## Training Neural Language Models

Given a training sample, the model predicts a neighboring word:

![](https://jalammar.github.io/images/word2vec/skipgram-language-model-training.png)  

Feed the input word to an untrained model:

![](https://jalammar.github.io/images/word2vec/skipgram-language-model-training-2.png)  

The model outputs a probability distribution over all vocabulary words. We compare against the target:

![](https://jalammar.github.io/images/word2vec/skipgram-language-model-training-3.png)  

Calculate error:

![](https://jalammar.github.io/images/word2vec/skipgram-language-model-training-4.png)  

Update embeddings to reduce error:

![](https://jalammar.github.io/images/word2vec/skipgram-language-model-training-5.png)  

Repeat for all training samples through multiple epochs. Then extract the embedding matrix for downstream tasks.

# Negative Sampling

Computing softmax over a 1-million-word vocabulary is expensive — each training step requires similarity scores for every word. With millions of training samples, this becomes prohibitively slow.

Word2vec solves this with **negative sampling**, a brilliant trick that speeds up training 100x.

![](https://jalammar.github.io/images/word2vec/language-model-expensive.png)  

**Solution**: Instead of predicting which word comes next (1M-way classification), use binary classification: are these two words neighbors?

![](https://jalammar.github.io/images/word2vec/are-the-words-neighbors.png)  

This reduces computation from O(vocabulary_size) to O(1) per sample. Training becomes ~100x faster.

The training dataset now has positive examples (neighbors):

![](https://jalammar.github.io/images/word2vec/word2vec-training-dataset.png)  

But if all examples are positive, a model can achieve 100% accuracy by always returning 1. We need **negative examples** — words that aren't neighbors:

![](https://jalammar.github.io/images/word2vec/word2vec-smartass-model.png)  

For each positive sample, add negative samples with random words:

![](https://jalammar.github.io/images/word2vec/word2vec-negative-sampling.png)  

![](https://jalammar.github.io/images/word2vec/word2vec-negative-sampling-2.png)  

This contrasts signal (actual neighbors) with noise (random words), inspired by noise-contrastive estimation.

# Skipgram with Negative Sampling (SGNS)

Two central ideas of word2vec:

![](https://jalammar.github.io/images/word2vec/skipgram-with-negative-sampling.png)  

# Word2vec Training Process

Before training, preprocess text to determine vocabulary size and build vocabulary.

Initialize two matrices — **Embedding** and **Context** — each with embeddings for every vocabulary word (vocab_size × embedding_size, e.g., 10,000 × 300):

![](https://jalammar.github.io/images/word2vec/word2vec-embedding-context-matrix.png)  

Start with random values. During training, take one positive example and associated negative examples:

![](https://jalammar.github.io/images/word2vec/word2vec-training-example.png)  

Look up embeddings — input word from Embedding matrix, context words from Context matrix:

![](https://jalammar.github.io/images/word2vec/word2vec-lookup-embeddings.png)  

Take dot products (similarity scores):

![](https://jalammar.github.io/images/word2vec/word2vec-training-dot-product.png)  

Apply sigmoid to convert scores to probabilities [0,1]:

![](https://jalammar.github.io/images/word2vec/word2vec-training-dot-product-sigmoid.png)  

Calculate error — difference from target (1 for neighbors, 0 for non-neighbors):

![](https://jalammar.github.io/images/word2vec/word2vec-training-error.png)  

Update embeddings to reduce error:

![](https://jalammar.github.io/images/word2vec/word2vec-training-update.png)  

Proceed to next sample. Embeddings improve iteratively:

![](https://jalammar.github.io/images/word2vec/word2vec-training-example-2.png)  

Repeat through entire dataset for multiple epochs. Extract the Embedding matrix as final word embeddings.

# Hyperparameters

## Window Size

Different window sizes learn different relationships:

![](https://jalammar.github.io/images/word2vec/word2vec-window-size.png)  

**Smaller windows (2-15)**: Words must appear in nearly identical contexts to be similar. Results in "interchangeable" words clustering — synonyms AND antonyms (both appear in the same surrounding contexts). Example: "good" and "bad" both follow similar verbs.

**Larger windows (15-50+)**: Words are similar if related to the same domain/topic, regardless of exact context. Captures broader semantic relationships. Example: "king," "queen," "prince" cluster together. Gensim default: 5.

## Number of Negative Samples

![](https://jalammar.github.io/images/word2vec/word2vec-negative-samples.png)  

More negatives = more learning signal per positive example = better quality, but slower training.

**Original word2vec paper**: 5-20 negative samples  
**Large datasets**: 2-5 is often sufficient  
**Gensim default**: 5

The tradeoff: 10 negative samples give 10x more gradient updates per example, but take 2x longer to train. In practice, 5 is a good balance.