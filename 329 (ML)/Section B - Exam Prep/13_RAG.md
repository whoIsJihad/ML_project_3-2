# 📘 RAG (Retrieval Augmented Generation)

## 1. Core Idea (Intuition)

**Problem with LLMs:** 
- No explicit access to external knowledge (e.g., recent events)
- Hallucinate facts
- Cannot reference specific documents

**RAG solution:** Retrieve relevant documents, then generate with context.

**Key idea:** Combine retrieval + generation for grounded, factual answers.

---

## 2. Architecture

### Two Components

**Retriever:** Given query, fetch relevant documents.
$$\text{docs} = \text{Retriever}(\text{query})$$

**Generator:** Generate answer conditioned on documents + query.
$$\text{answer} = \text{Generator}(\text{query}, \text{docs})$$

### Pipeline
```
User Query
    ↓
[Retrieval] Find relevant documents/passages
    ↓
[Augmentation] Append documents to query
    ↓
[Generation] LLM generates answer with context
    ↓
Answer with Sources
```

---

## 3. Retriever

### Sparse (BM25)
Traditional keyword-based retrieval.

**Pros:** Fast, interpretable

**Cons:** Misses semantic similarity (synonyms, paraphrases)

### Dense (Neural Embeddings)
Embed query and documents in same space:
$$\text{similarity} = \cos(\text{embed}(\text{query}), \text{embed}(\text{doc}))$$

**Models:**
- BERT embeddings
- Specialized dense retrievers (DPR, ColBERT, etc.)

**Pros:** Semantic matching

**Cons:** Compute-intensive (but optimized with vector databases)

### Hybrid
Combine sparse + dense for robustness.

---

## 4. Augmentation Strategies

### Document Retrieval
Retrieve full documents:
```
Query: "When was Napoleon born?"

Retrieved docs:
- Wikipedia: "Napoleon Bonaparte was born in 1769..."
- Historical archive: "August 15, 1769, Ajaccio..."

Augmented input:
"Answer based on these sources: [full docs]. Question: When was Napoleon born?"
```

### Passage Retrieval
Retrieve shorter passages (more focused):
```
Retrieved passages:
- "Napoleon Bonaparte...born in 1769"
- "Date of birth: August 15, 1769"
```

**Tradeoff:** Passages more focused; risk missing context.

---

## 5. Generator

### Standard Decoder LLM
Any language model (GPT, BART, T5, etc.):
$$P(\text{answer} | \text{query}, \text{docs})$$

**Training:**
- Supervised (question-answer-documents triplets)
- Or: Leverage pretrained LLMs without additional training

---

## 6. Applications

- **QA over documents:** Answer questions from knowledge base
- **Customer support:** Retrieve relevant docs, generate response
- **Citation:** Generate text with source attribution
- **Up-to-date facts:** Retrieve recent news, incorporate into generation

---

## 7. Advantages of RAG

| Advantage | How |
|-----------|-----|
| **Factual grounding** | Retrieval provides sources |
| **Explicit knowledge** | Can access external documents |
| **Up-to-date** | Retrieve recent documents without retraining |
| **Explainability** | Can show which documents influenced answer |
| **Scalability** | Add more documents without retraining LLM |

---

## 8. Failure Cases / Challenges

| Challenge | Why | Mitigation |
|-----------|-----|-----------|
| **Retrieval failure** | Query doesn't match document | Improve retriever; use multiple terms |
| **Long documents** | Generator overwhelmed by context | Passage-level retrieval; summarization |
| **Conflicting docs** | Retrieved docs disagree | Rank by confidence; note conflicts |
| **Irrelevant context** | Retrieved docs not useful | Better retriever; relevance filtering |

---

## 9. Vector Databases

**Key infrastructure:** Store embeddings for fast retrieval.

| Database | Feature |
|----------|---------|
| **Pinecone** | Cloud-hosted, fast |
| **Weaviate** | Open-source, flexible |
| **Milvus** | Scalable, vector-specific |
| **Faiss** | Facebook's tool, fast indexing |

**Query latency:** Milliseconds (for billion-scale documents).

---

## 10. RAG vs. Fine-tuning

| Approach | Pros | Cons |
|----------|------|------|
| **RAG** | Easy to update; explicit sources; no retraining | Retrieval can fail |
| **Fine-tuning** | Knowledge fully integrated; faster inference | Requires retraining for new knowledge; no attribution |

**Modern practice:** Combine both for best results.

---

## 11. Exam Questions

### Conceptual
1. Why is RAG better than LLMs alone for factual QA?
2. Explain retriever vs. generator. How do they interact?
3. What's difference between sparse (BM25) and dense (neural) retrieval?

### Practical
1. Design RAG system for customer support QA.
2. Retrieved documents conflict. How to handle?

### Trick Cases
1. Retriever returns 0 relevant documents. Generator hallucinates. Why?
2. Add more documents to retrieval database. Effect on generation quality?

---

## 12. Key Takeaways

- **RAG:** Retrieve documents, then generate answer with context
- **Retriever:** Find relevant documents (sparse: BM25, dense: embeddings, hybrid)
- **Generator:** LLM that conditions on retrieved documents
- **Pipeline:** Query → Retrieval → Augmentation → Generation → Answer
- **Advantages:** Factual grounding, explicit sources, updateable knowledge, scalable
- **Challenges:** Retrieval failure, long document handling, conflicting sources
- **Infrastructure:** Vector databases for efficient similarity search
- **Trade-off:** RAG (easy updates, attribution) vs. Fine-tuning (integrated knowledge, faster)
- **Modern practice:** Combine both; retrieve specialized docs, fine-tune for domain

---
