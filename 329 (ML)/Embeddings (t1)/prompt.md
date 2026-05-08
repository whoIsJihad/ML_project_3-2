Act as a direct, no-nonsense expert AI educator. Create a comprehensive, beginner-friendly set of notes based on the two provided documents ("The Illustrated Word2vec" and the "Cornell Deep Learning Week 02 Slides"). The target audience is an absolute beginner to Machine Learning.

Cut the fluff. Output the notes strictly in clean Markdown (.md) format so I can drop them straight into my knowledge base. Break the explanation down into logical, bite-sized micro-topics.

Structure the notes using this exact flow:

Topic Index: A bulleted table of contents.

The Old Way (Pre-Word2Vec): Explain N-grams and Bag of Words in simple terms. Clearly list their fatal flaws (e.g., high dimensionality, loss of context).

Enter Vectors: Explain what word embeddings are. Use the "Big Five Personality Traits" analogy. Explain how Cosine Similarity measures distance/meaning.

Word2Vec Architectures: Break down how the models learn. Contrast Continuous Bag of Words (CBOW) vs. Skip-gram in very simple terms.

The Bottleneck & The Fix: Explain the Softmax computational bottleneck. Explain the solution: Negative Sampling (switching the task to a simple Yes/No "Are these words neighbors?").

The Flaws of Word2Vec: Summarize the limitations covered in the slides (societal biases, time-dependence, and the polysemy/multiple-meaning problem like the word 'bank').

Teaser - Why we need RNNs: A tiny conceptual step explaining why we eventually move to Recurrent Neural Networks (to handle sequences of varying lengths).

Keep the formatting heavily structured with ## headings, bullet lists, and bold text for core terminology. Do not use childish analogies; just explain the mechanics simply and directly."