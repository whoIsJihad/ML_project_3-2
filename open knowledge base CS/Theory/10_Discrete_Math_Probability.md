# Discrete Mathematics & Probability

## Course Overview
**Depth:** University undergraduate level  
**Time:** 2-3 hours focused reading  
**Prerequisites:** Basic algebra

---

# Part I: Logic and Proof

---

## 1. Propositional Logic

### Propositions and Connectives

| Symbol | Name | Meaning | Example |
|--------|------|---------|---------|
| ¬ | Negation | NOT | ¬p (not p) |
| ∧ | Conjunction | AND | p ∧ q |
| ∨ | Disjunction | OR | p ∨ q |
| → | Implication | IF...THEN | p → q |
| ↔ | Biconditional | IF AND ONLY IF | p ↔ q |
| ⊕ | XOR | Exclusive OR | p ⊕ q |

### Truth Tables

```
p  q  |  ¬p  p∧q  p∨q  p→q  p↔q  p⊕q
------+--------------------------------
T  T  |   F   T    T    T    T    F
T  F  |   F   F    T    F    F    T
F  T  |   T   F    T    T    F    T
F  F  |   T   F    F    T    T    F
```

**Implication** (p → q): Only false when p is true and q is false.
- Equivalent: ¬p ∨ q
- Contrapositive: ¬q → ¬p (logically equivalent)
- Converse: q → p (NOT equivalent)
- Inverse: ¬p → ¬q (NOT equivalent)

### Logical Equivalences

| Name | Equivalence |
|------|-------------|
| Identity | p ∧ T ≡ p, p ∨ F ≡ p |
| Domination | p ∨ T ≡ T, p ∧ F ≡ F |
| Idempotent | p ∨ p ≡ p, p ∧ p ≡ p |
| Double Negation | ¬(¬p) ≡ p |
| Commutative | p ∨ q ≡ q ∨ p, p ∧ q ≡ q ∧ p |
| Associative | (p ∨ q) ∨ r ≡ p ∨ (q ∨ r) |
| Distributive | p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r) |
| De Morgan's | ¬(p ∧ q) ≡ ¬p ∨ ¬q, ¬(p ∨ q) ≡ ¬p ∧ ¬q |
| Absorption | p ∨ (p ∧ q) ≡ p, p ∧ (p ∨ q) ≡ p |

---

## 2. Predicate Logic

### Quantifiers

| Symbol | Name | Meaning |
|--------|------|---------|
| ∀ | Universal | For all |
| ∃ | Existential | There exists |
| ∃! | Unique Existential | There exists exactly one |

```
∀x P(x)  - P is true for all x in domain
∃x P(x)  - There exists at least one x where P is true

Negation:
¬(∀x P(x)) ≡ ∃x ¬P(x)
¬(∃x P(x)) ≡ ∀x ¬P(x)
```

### Nested Quantifiers

```
∀x∀y P(x,y) - For all x and all y, P holds
∀x∃y P(x,y) - For all x, there exists a y such that P holds
∃x∀y P(x,y) - There exists an x such that for all y, P holds
∃x∃y P(x,y) - There exist x and y such that P holds

Order matters!
∀x∃y L(x,y) ≠ ∃y∀x L(x,y)
(Every person has a loved one) vs (Someone is loved by everyone)
```

---

## 3. Proof Techniques

### Direct Proof
To prove: p → q

1. Assume p is true
2. Use definitions and theorems
3. Conclude q is true

**Example:** If n is odd, then n² is odd.
```
Assume n is odd.
Then n = 2k + 1 for some integer k.
n² = (2k + 1)² = 4k² + 4k + 1 = 2(2k² + 2k) + 1
Let m = 2k² + 2k.
Then n² = 2m + 1, which is odd. ∎
```

### Proof by Contraposition
To prove: p → q, prove ¬q → ¬p

**Example:** If n² is even, then n is even.
```
Contrapositive: If n is odd, then n² is odd.
(Same proof as above) ∎
```

### Proof by Contradiction
To prove: p, assume ¬p and derive a contradiction.

**Example:** √2 is irrational.
```
Assume √2 = a/b where a, b are integers with no common factors.
Then 2 = a²/b², so a² = 2b².
Thus a² is even, so a is even. Let a = 2k.
Then (2k)² = 2b², so 4k² = 2b², so b² = 2k².
Thus b² is even, so b is even.
But a and b both even contradicts that they have no common factors. ∎
```

### Proof by Mathematical Induction
To prove: ∀n≥n₀ P(n)

1. **Base case:** Prove P(n₀)
2. **Inductive step:** Prove P(k) → P(k+1)
3. **Conclusion:** By induction, P(n) holds for all n ≥ n₀

**Example:** 1 + 2 + ... + n = n(n+1)/2

```
Base case: n = 1
  1 = 1(2)/2 = 1 ✓

Inductive step: Assume 1 + 2 + ... + k = k(k+1)/2
  1 + 2 + ... + k + (k+1) 
  = k(k+1)/2 + (k+1)
  = (k+1)(k/2 + 1)
  = (k+1)(k+2)/2 ✓
  
By induction, the formula holds for all n ≥ 1. ∎
```

### Strong Induction
Assume P(n₀), P(n₀+1), ..., P(k) all true, prove P(k+1).

Useful when P(k+1) depends on multiple previous cases.

---

# Part II: Sets, Relations, Functions

---

## 4. Set Theory

### Set Operations

| Operation | Notation | Definition |
|-----------|----------|------------|
| Union | A ∪ B | {x : x ∈ A or x ∈ B} |
| Intersection | A ∩ B | {x : x ∈ A and x ∈ B} |
| Difference | A - B or A \ B | {x : x ∈ A and x ∉ B} |
| Complement | Ā or A' | {x : x ∈ U and x ∉ A} |
| Symmetric Diff | A △ B | (A - B) ∪ (B - A) |
| Cartesian Product | A × B | {(a,b) : a ∈ A, b ∈ B} |
| Power Set | P(A) | {S : S ⊆ A} |

### Set Identities

| Name | Identity |
|------|----------|
| Identity | A ∪ ∅ = A, A ∩ U = A |
| Domination | A ∪ U = U, A ∩ ∅ = ∅ |
| Idempotent | A ∪ A = A, A ∩ A = A |
| Complement | A ∪ Ā = U, A ∩ Ā = ∅ |
| De Morgan's | (A ∪ B)' = A' ∩ B', (A ∩ B)' = A' ∪ B' |

### Cardinality

```
|A| = number of elements in A

Inclusion-Exclusion:
|A ∪ B| = |A| + |B| - |A ∩ B|
|A ∪ B ∪ C| = |A| + |B| + |C| - |A∩B| - |A∩C| - |B∩C| + |A∩B∩C|

Power set: |P(A)| = 2^|A|

Cartesian product: |A × B| = |A| × |B|
```

---

## 5. Relations

### Properties of Relations (on set A)

| Property | Definition |
|----------|------------|
| Reflexive | ∀a∈A: (a,a) ∈ R |
| Irreflexive | ∀a∈A: (a,a) ∉ R |
| Symmetric | (a,b) ∈ R → (b,a) ∈ R |
| Antisymmetric | (a,b) ∈ R ∧ (b,a) ∈ R → a = b |
| Transitive | (a,b) ∈ R ∧ (b,c) ∈ R → (a,c) ∈ R |

### Special Relations

**Equivalence Relation:** Reflexive, symmetric, transitive
- Partitions set into equivalence classes
- Example: ≡ (mod n)

**Partial Order:** Reflexive, antisymmetric, transitive
- Can compare some pairs but not all
- Example: ⊆ on sets, ≤ on integers

**Total Order:** Partial order where all pairs comparable
- Example: ≤ on integers (but not ⊆ on sets)

### Closures

The closure of R with respect to property P is the smallest relation containing R with property P.

```
- Reflexive closure: R ∪ {(a,a) : a ∈ A}
- Symmetric closure: R ∪ {(b,a) : (a,b) ∈ R}
- Transitive closure: R+ = R ∪ R² ∪ R³ ∪ ...
```

---

## 6. Functions

### Function Types

| Type | Definition |
|------|------------|
| Injection (one-to-one) | f(a) = f(b) → a = b |
| Surjection (onto) | ∀b∈B, ∃a∈A: f(a) = b |
| Bijection | Both injection and surjection |

```
f: A → B

Injection: Different inputs → different outputs
Surjection: Every element in B is hit
Bijection: Perfect one-to-one correspondence

If f: A → B is a bijection, then |A| = |B|
```

### Composition and Inverse

```
(g ∘ f)(x) = g(f(x))

If f: A → B is a bijection:
- f⁻¹: B → A exists
- f⁻¹(f(a)) = a for all a ∈ A
- f(f⁻¹(b)) = b for all b ∈ B
```

### Floor and Ceiling

```
⌊x⌋ = largest integer ≤ x
⌈x⌉ = smallest integer ≥ x

Examples:
⌊3.7⌋ = 3,  ⌈3.7⌉ = 4
⌊-2.3⌋ = -3,  ⌈-2.3⌉ = -2
⌊5⌋ = ⌈5⌉ = 5
```

---

# Part III: Combinatorics

---

## 7. Counting Principles

### Basic Rules

**Sum Rule:** If task can be done in n₁ ways OR n₂ ways (disjoint), total = n₁ + n₂

**Product Rule:** If task has two stages, n₁ ways × n₂ ways = total ways

### Permutations

Ordered arrangements

```
Without repetition:
P(n,r) = n!/(n-r)! = n × (n-1) × ... × (n-r+1)

With repetition:
n^r (r positions, n choices each)

Circular permutation:
(n-1)! ways to arrange n objects in circle

With indistinguishable objects:
n!/(n₁! × n₂! × ... × nₖ!)
(multinomial coefficient)
```

**Example:** Arrangements of "MISSISSIPPI"
```
11 letters: M(1), I(4), S(4), P(2)
= 11!/(1! × 4! × 4! × 2!) = 34,650
```

### Combinations

Unordered selections

```
Without repetition:
C(n,r) = n!/(r!(n-r)!) = (n choose r)

With repetition (stars and bars):
C(n+r-1, r) = C(n+r-1, n-1)
```

**Properties of Binomial Coefficients:**
```
C(n,0) = C(n,n) = 1
C(n,r) = C(n, n-r)
C(n,r) = C(n-1, r-1) + C(n-1, r)  (Pascal's identity)
C(n,0) + C(n,1) + ... + C(n,n) = 2^n
```

### Binomial Theorem

```
(x + y)^n = Σ(k=0 to n) C(n,k) × x^(n-k) × y^k
```

---

## 8. Pigeonhole Principle

**Basic:** If n+1 pigeons in n holes, at least one hole has ≥2 pigeons.

**Generalized:** If n objects in k boxes, at least one box has ⌈n/k⌉ objects.

**Examples:**
- In 13 people, at least 2 have birthday in same month
- In any 5 integers, at least 2 have same remainder mod 4

---

## 9. Inclusion-Exclusion Principle

```
|A₁ ∪ A₂ ∪ ... ∪ Aₙ| = Σ|Aᵢ| - Σ|Aᵢ ∩ Aⱼ| + Σ|Aᵢ ∩ Aⱼ ∩ Aₖ| - ... + (-1)^(n+1)|A₁ ∩ ... ∩ Aₙ|

For 3 sets:
|A ∪ B ∪ C| = |A| + |B| + |C| - |A∩B| - |A∩C| - |B∩C| + |A∩B∩C|
```

**Derangements:** Permutations where no element is in original position.
```
D(n) = n! × Σ(k=0 to n) (-1)^k / k!
     ≈ n!/e
```

---

# Part IV: Graph Theory Basics

---

## 10. Graph Fundamentals

### Definitions

```
G = (V, E) where V = vertices, E = edges

Undirected: E = {(u,v)} unordered pairs
Directed: E = {(u,v)} ordered pairs

Degree: deg(v) = number of edges incident to v
  - In directed: in-degree + out-degree

Simple graph: No self-loops, no multiple edges
Multigraph: Multiple edges allowed
Complete graph: Every pair of vertices connected (Kₙ)
Bipartite: Vertices can be partitioned into two sets with 
           edges only between sets
```

### Handshaking Lemma

```
Σ deg(v) = 2|E|

For directed graphs:
Σ in-deg(v) = Σ out-deg(v) = |E|
```

### Special Graphs

| Graph | Description | Vertices | Edges |
|-------|-------------|----------|-------|
| Kₙ | Complete | n | n(n-1)/2 |
| Kₘ,ₙ | Complete bipartite | m+n | m×n |
| Cₙ | Cycle | n | n |
| Pₙ | Path | n | n-1 |
| Qₙ | n-cube | 2ⁿ | n×2^(n-1) |

### Paths and Connectivity

```
Walk: Sequence of vertices with edges between consecutive
Path: Walk with no repeated vertices
Cycle: Path that starts and ends at same vertex

Connected graph: Path exists between every pair of vertices
Strongly connected (directed): Path in both directions

Euler path: Uses every edge exactly once
Euler circuit: Euler path that returns to start
  - Exists iff connected and all vertices have even degree

Hamilton path: Visits every vertex exactly once
Hamilton circuit: Hamilton path that returns to start
```

### Trees

```
Tree: Connected acyclic graph

Properties (equivalent for n vertices):
- Connected and n-1 edges
- Acyclic and n-1 edges
- Exactly one path between any two vertices
- Connected, removing any edge disconnects

Rooted tree: Tree with designated root vertex
- Parent, children, siblings, ancestors, descendants
- Leaf: No children
- Internal vertex: Has children
```

---

# Part V: Probability

---

## 11. Probability Basics

### Sample Space and Events

```
Sample space S: Set of all possible outcomes
Event A: Subset of S

P(A) = |A|/|S| for equally likely outcomes

Properties:
0 ≤ P(A) ≤ 1
P(S) = 1, P(∅) = 0
P(Ā) = 1 - P(A)
```

### Probability Rules

```
Addition Rule:
P(A ∪ B) = P(A) + P(B) - P(A ∩ B)

For mutually exclusive events:
P(A ∪ B) = P(A) + P(B)

Conditional Probability:
P(A|B) = P(A ∩ B) / P(B), where P(B) > 0

Multiplication Rule:
P(A ∩ B) = P(A|B) × P(B) = P(B|A) × P(A)
```

### Independence

```
A and B are independent iff:
P(A ∩ B) = P(A) × P(B)

Equivalently:
P(A|B) = P(A)
P(B|A) = P(B)
```

### Bayes' Theorem

```
P(A|B) = P(B|A) × P(A) / P(B)

With total probability:
P(A|B) = P(B|A) × P(A) / [P(B|A)P(A) + P(B|Ā)P(Ā)]
```

**Example: Medical Test**
```
Disease prevalence: P(D) = 0.01
Test accuracy: P(+|D) = 0.99, P(-|D̄) = 0.95

P(D|+) = P(+|D)P(D) / [P(+|D)P(D) + P(+|D̄)P(D̄)]
       = (0.99 × 0.01) / (0.99 × 0.01 + 0.05 × 0.99)
       = 0.167

Only 16.7% chance of disease given positive test!
```

---

## 12. Random Variables

### Discrete Random Variables

```
X: S → ℝ, assigns number to each outcome

Probability Mass Function (PMF):
p(x) = P(X = x)
Σ p(x) = 1

Cumulative Distribution Function (CDF):
F(x) = P(X ≤ x) = Σ p(k) for k ≤ x
```

### Expected Value (Mean)

```
E[X] = Σ x × P(X = x)

Properties:
E[c] = c (constant)
E[cX] = c × E[X]
E[X + Y] = E[X] + E[Y] (always true)
E[XY] = E[X] × E[Y] (if independent)
```

### Variance and Standard Deviation

```
Var(X) = E[(X - E[X])²] = E[X²] - (E[X])²

Properties:
Var(c) = 0
Var(cX) = c² × Var(X)
Var(X + Y) = Var(X) + Var(Y) (if independent)

Standard Deviation: σ = √Var(X)
```

---

## 13. Common Distributions

### Bernoulli (Single trial)

```
X ∈ {0, 1}, P(X=1) = p, P(X=0) = 1-p = q

E[X] = p
Var(X) = pq
```

### Binomial (n independent Bernoulli trials)

```
X = number of successes in n trials

P(X = k) = C(n,k) × p^k × (1-p)^(n-k)

E[X] = np
Var(X) = np(1-p)
```

**Example:** Flip fair coin 10 times, probability of exactly 6 heads?
```
P(X=6) = C(10,6) × 0.5^6 × 0.5^4 = 210/1024 ≈ 0.205
```

### Geometric (Trials until first success)

```
P(X = k) = (1-p)^(k-1) × p,  k = 1, 2, ...

E[X] = 1/p
Var(X) = (1-p)/p²
```

### Poisson (Counting rare events)

```
P(X = k) = (λ^k × e^(-λ)) / k!,  k = 0, 1, 2, ...

λ = average rate

E[X] = λ
Var(X) = λ
```

### Uniform (Continuous)

```
f(x) = 1/(b-a) for a ≤ x ≤ b

E[X] = (a+b)/2
Var(X) = (b-a)²/12
```

### Normal (Gaussian)

```
f(x) = (1/(σ√(2π))) × e^(-(x-μ)²/(2σ²))

E[X] = μ (mean)
Var(X) = σ² (variance)

Standard Normal: Z ~ N(0,1)
Z = (X - μ)/σ

68-95-99.7 Rule:
P(|X - μ| < σ) ≈ 0.68
P(|X - μ| < 2σ) ≈ 0.95
P(|X - μ| < 3σ) ≈ 0.997
```

---

## 14. Summary Tables

### Counting Summary

| Scenario | Ordered? | Repetition? | Formula |
|----------|----------|-------------|---------|
| Permutation | Yes | No | n!/(n-r)! |
| Permutation | Yes | Yes | n^r |
| Combination | No | No | n!/(r!(n-r)!) |
| Combination | No | Yes | (n+r-1)!/(r!(n-1)!) |

### Distribution Summary

| Distribution | PMF/PDF | E[X] | Var(X) |
|--------------|---------|------|--------|
| Bernoulli(p) | p^x(1-p)^(1-x) | p | p(1-p) |
| Binomial(n,p) | C(n,k)p^k(1-p)^(n-k) | np | np(1-p) |
| Geometric(p) | (1-p)^(k-1)p | 1/p | (1-p)/p² |
| Poisson(λ) | λ^k e^(-λ)/k! | λ | λ |
| Uniform(a,b) | 1/(b-a) | (a+b)/2 | (b-a)²/12 |
| Normal(μ,σ²) | ... | μ | σ² |

---

## Cross-References

- [[04_Algorithms_Data_Structures]] - Graph algorithms, complexity
- [[01_Digital_Logic_Design]] - Boolean algebra applications
