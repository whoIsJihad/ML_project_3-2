# 📘 Graph Neural Networks (GNN)

## 1. Core Idea (Intuition)

**Problem:** Data is graph-structured (nodes, edges) — standard NNs ignore structure.

**GNN solution:** Neural network that propagates information along graph edges.

**Key insight:** Each node's representation updated using its neighbors' representations.

---

## 2. Graph Representation

### Graph
$$G = (V, E) \quad \text{where}$$
- $V$: set of vertices (nodes)
- $E$: set of edges
- Each node has features $x_v \in \mathbb{R}^d$

### Adjacency Matrix
$$A \in \mathbb{R}^{n \times n} \quad \text{where}$$
- $A_{ij} = 1$ if edge $(i,j)$ exists
- $A_{ij} = 0$ otherwise

---

## 3. Message Passing (General GNN)

### Core Mechanism
Node $i$ updates representation by aggregating from neighbors:

$$h_i^{(l+1)} = \text{UPDATE}(h_i^{(l)}, \text{AGGREGATE}(\{h_j^{(l)} : j \in N(i)\}))$$

where:
- $N(i)$: neighbors of node $i$
- $h_i^{(l)}$: representation of node $i$ at layer $l$
- $\text{AGGREGATE}$: combine neighbor features (e.g., sum, mean, max)
- $\text{UPDATE}$: update node's own feature (e.g., neural network)

### Example (Graph Convolutional Network - GCN)

$$h_i^{(l+1)} = \sigma(W^{(l)} \cdot \text{mean}(\{h_i^{(l)}\} \cup \{h_j^{(l)} : j \in N(i)\}))$$

**Interpretation:** Combine own features with neighbor average, apply linear transform, activation.

---

## 4. Layer-wise Propagation

```
Input: Node features X (n × d)
Adjacency: A (n × n)

For each layer l = 0, 1, ..., L:
  For each node i:
    aggregated = mean([h_j^(l) for j in neighbors(i)])
    h_i^(l+1) = σ(W^(l) * [h_i^(l), aggregated])

Output: H^(L) (final node representations)
```

---

## 5. Common GNN Variants

| Variant | AGGREGATE | UPDATE | Use |
|---------|-----------|--------|-----|
| **GCN** | Mean | Concat + Linear | Standard; balanced |
| **GraphSAGE** | Mean/LSTM | Concat + Linear | Scalable; sampling |
| **GAT** | Attention | Attention-weighted | Focus on important neighbors |
| **GIN** | Sum | Non-linear | Expressive (theoretically optimal) |

---

## 6. Graph Classification

### Node-level
Predict label for each node:
$$\hat{y}_i = \text{Classifier}(h_i^{(L)})$$

**Example:** Predicting type of node in social network.

### Graph-level
Predict label for entire graph:
$$\hat{y} = \text{Classifier}(\text{POOL}(h_1^{(L)}, h_2^{(L)}, \ldots, h_n^{(L)}))$$

where $\text{POOL}$ aggregates all nodes (e.g., mean, sum, max).

**Example:** Predicting if molecule is active drug.

---

## 7. Applications

- **Social networks:** Predict missing links, recommend friends
- **Molecules:** Predict properties (toxicity, drug efficacy)
- **Knowledge graphs:** Relation extraction, link prediction
- **Traffic networks:** Traffic prediction, anomaly detection
- **Recommendation systems:** User-item graphs

---

## 8. Advantages of GNNs

- **Leverages graph structure:** Ignoring edges = losing information
- **Inductive:** Can generalize to unseen nodes (vs. spectral methods)
- **Scalable:** Sampling neighbors (GraphSAGE) scales to large graphs
- **Interpretable:** Attention weights show which neighbors matter

---

## 9. Failure Cases / Limitations

| Problem | Why |
|---------|-----|
| **Over-smoothing** | After many layers, nodes become too similar |
| **Heterophilic graphs** | Edges connect dissimilar nodes (assumption violated) |
| **Large graphs** | Memory/compute expensive for dense neighborhoods |

---

## 10. Exam Questions

### Conceptual
1. How does message passing work in GNNs? Explain AGGREGATE and UPDATE.
2. Why can GNNs handle variable-size graphs?
3. What is over-smoothing? Why does it happen?

### Practical
1. Design GCN for node classification on social network.
2. Molecule property prediction: design graph-level classifier.

### Trick Cases
1. Fully connected graph. GNN useful?
2. Each node isolated (no edges). GNN degenerates to what?

---

## 11. Key Takeaways

- **GNN:** Neural network on graph-structured data
- **Message passing:** $h_i^{(l+1)} = \text{UPDATE}(h_i^{(l)}, \text{AGGREGATE}(\text{neighbors}))$
- **Aggregation:** Combine neighbor features (mean, sum, attention)
- **Update:** Non-linear transformation (neural network)
- **Node vs. graph:** Node-level (predict per node) vs. graph-level (predict full graph)
- **Variants:** GCN, GraphSAGE, GAT, GIN; different aggregation strategies
- **Applications:** Social networks, molecules, knowledge graphs, traffic
- **Limitation:** Over-smoothing with many layers; assume homophily (similar neighbors)

---
