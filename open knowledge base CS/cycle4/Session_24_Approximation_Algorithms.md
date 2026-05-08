# Session 24 – Approximation Algorithms & Hardness

**Cycle**: 4 (Expert Mastery)  
**Domain**: Algorithms & Complexity  
**Difficulty**: ⚫⚫⚫⚫

**Prerequisites**: P vs NP, reductions, linear programming basics

---

## Phase 1: Core Theory & Mental Models

### 1.1 Definitions

**Approximation Algorithm**: Algorithm that runs in polynomial time and produces a solution within a guaranteed factor of optimal.

**α-approximation**: Algorithm A is an α-approximation if for all instances:
- Minimization: `A(I) ≤ α · OPT(I)`
- Maximization: `A(I) ≥ OPT(I) / α`

**APX Class**: Problems admitting constant-factor approximations (PTAS not proven to exist)

**PTAS** (Polynomial-Time Approximation Scheme): Family of algorithms A_ε achieving (1+ε)-approximation in poly(n) time

**FPTAS** (Fully PTAS): PTAS running in time poly(n, 1/ε)

### 1.2 Core Mechanisms

**Greedy Approximation** (Vertex Cover):
```
Algorithm: 2-Approximation for Vertex Cover
Input: Graph G = (V, E)
Output: Vertex cover C

C = ∅
E' = E
while E' ≠ ∅:
    pick arbitrary edge (u,v) ∈ E'
    C = C ∪ {u, v}
    remove all edges incident to u or v from E'
return C
```

**Proof Sketch**:
- Let M = edges picked (maximal matching)
- |C| = 2|M|
- OPT must cover M, so OPT ≥ |M|
- Therefore |C| ≤ 2·OPT

**LP Rounding** (Set Cover):
- Formulate as integer program (IP)
- Relax to linear program (LP)
- Solve LP, round fractional solution
- Approximation ratio depends on rounding strategy

**Primal-Dual Method**:
- Simultaneously construct primal solution (feasible) and dual solution
- Use dual to bound primal optimality

### 1.3 Mental Models

**The Barrier Visualization**: Imagine approximation hardness as barriers:
- Below α=1: impossible (would solve NP-hard exactly)
- α=1 to hardness threshold: algorithmically feasible
- Beyond threshold: proven impossible unless P=NP

**Integrality Gap**: Gap between LP relaxation and IP optimum - bounds best LP-rounding ratio

### 1.4 Edge Cases

**Vertex Cover vs Independent Set**: VC has 2-approx, but IS has no constant approx (unless P=NP)

**Metric TSP vs General TSP**: Metric TSP admits 1.5-approx (Christofides), general TSP admits no approximation

**MAX-SAT**: (1-1/e)-approx achievable, tight threshold

### 1.5 Implementation

**Set Cover via Greedy**:
```python
def set_cover_greedy(universe, sets):
    """
    O(|U| * |S|) greedy H_n-approximation
    H_n = Σ(1/i) ≈ ln(n) is nth harmonic number
    """
    uncovered = set(universe)
    cover = []
    
    while uncovered:
        # Find set with max cost-effectiveness
        best_set = max(sets, key=lambda s: len(s & uncovered))
        cover.append(best_set)
        uncovered -= best_set
    
    return cover

# LP-Rounding approach
def set_cover_lp_rounding(universe, sets):
    """
    Solve LP: minimize Σ x_s
              s.t. Σ_{s: e∈s} x_s ≥ 1  ∀e ∈ U
                   x_s ≥ 0
    Round: include S if x_s ≥ 1/f (f = max frequency)
    Gives f-approximation
    """
    from scipy.optimize import linprog
    
    # Construct constraint matrix
    n_sets = len(sets)
    n_elements = len(universe)
    A = []  # constraint matrix
    for elem in universe:
        row = [1 if elem in s else 0 for s in sets]
        A.append(row)
    
    c = [1] * n_sets  # minimize sum of x_s
    b = [1] * n_elements  # each element covered at least once
    
    res = linprog(c, A_ub=-A, b_ub=-b, bounds=(0, None))
    x_opt = res.x
    
    # Round: include sets with x_s ≥ threshold
    f = max(sum(row) for row in A)  # max frequency
    threshold = 1.0 / f
    cover = [sets[i] for i in range(n_sets) if x_opt[i] >= threshold]
    
    return cover
```

**Christofides Algorithm (TSP)**:
```python
import networkx as nx

def christofides_tsp(G):
    """
    1.5-approximation for metric TSP
    1. Find MST
    2. Find minimum-weight perfect matching on odd-degree vertices
    3. Combine to form Eulerian graph
    4. Find Eulerian tour, shortcut to Hamiltonian
    """
    # Step 1: MST
    mst = nx.minimum_spanning_tree(G)
    
    # Step 2: Odd-degree vertices
    odd_vertices = [v for v in mst.nodes() if mst.degree(v) % 2 == 1]
    
    # Step 3: Min-weight perfect matching on odd vertices
    odd_subgraph = G.subgraph(odd_vertices)
    matching = nx.algorithms.matching.min_weight_matching(odd_subgraph)
    
    # Step 4: Combine MST + matching
    eulerian_graph = nx.MultiGraph(mst)
    eulerian_graph.add_edges_from(matching)
    
    # Step 5: Eulerian tour
    tour = list(nx.eulerian_circuit(eulerian_graph))
    
    # Step 6: Shortcut to Hamiltonian (visit each vertex once)
    visited = set()
    hamiltonian = []
    for u, v in tour:
        if u not in visited:
            hamiltonian.append(u)
            visited.add(u)
    hamiltonian.append(hamiltonian[0])  # close tour
    
    return hamiltonian
```

---

## Phase 2: Conceptual Stress Questions

### Q1: Hardness of Approximation
**Question**: Prove that if Vertex Cover admits a (2-ε)-approximation for any ε > 0, then P = NP.

<details>
<summary><strong>Hint</strong></summary>

Consider the reduction from Independent Set. What happens to approximation ratios under complement?
</details>

---

### Q2: Integrality Gap
**Question**: Show that the integrality gap of the linear programming relaxation for Vertex Cover can be arbitrarily close to 2.

<details>
<summary><strong>Hint</strong></summary>

Construct a family of graphs (e.g., cycles or complete bipartite graphs) where LP gives value n/2 but minimum VC is n.
</details>

---

### Q3: PTAS Impossibility
**Question**: Explain why Set Cover cannot have a PTAS unless P = NP, even though it admits an H_n-approximation.

<details>
<summary><strong>Hint</strong></summary>

Use hardness of approximation results: Set Cover is hard to approximate within (1-ε)ln(n) factor for any ε>0 under standard assumptions.
</details>

---

## Phase 3: Applied Problem

### Problem: Design Approximation Algorithm for Facility Location

**Scenario**: You have a set of cities C and potential facility locations F. Opening facility i costs f_i. Serving city j from facility i costs c_ij. Design a 3-approximation algorithm.

**Constraints**:
- Each city must be served by exactly one facility
- Minimize total cost: Σ f_i (opened facilities) + Σ c_ij (service costs)

**Skeleton Code**:
```python
def facility_location_approx(cities, facilities, opening_costs, service_costs):
    """
    3-approximation using primal-dual method
    
    Args:
        cities: list of city indices
        facilities: list of facility indices
        opening_costs: dict {facility: cost}
        service_costs: dict {(city, facility): cost}
    
    Returns:
        opened: set of opened facilities
        assignment: dict {city: facility}
    """
    opened = set()
    assignment = {}
    alpha = {}  # dual variable for city constraints
    
    # TODO: Implement primal-dual algorithm
    # 1. Initialize all dual variables to 0
    # 2. Raise dual variables until facilities become "tight"
    # 3. Open tight facilities and assign cities
    # 4. Use cost accounting to prove 3-approximation
    
    return opened, assignment

# Test case
cities = [0, 1, 2]
facilities = [0, 1]
opening_costs = {0: 10, 1: 15}
service_costs = {
    (0, 0): 2, (0, 1): 5,
    (1, 0): 4, (1, 1): 1,
    (2, 0): 3, (2, 1): 4
}

opened, assignment = facility_location_approx(cities, facilities, opening_costs, service_costs)
print(f"Opened facilities: {opened}")
print(f"City assignments: {assignment}")
```

**Expected Approach**:
1. Use primal-dual: raise dual variables for cities
2. Open facility when dual sum covers opening cost
3. Assign cities to nearest open facility
4. Prove: facility opening ≤ OPT, connection costs ≤ 2·OPT

---

## Phase 4: Self-Assessment

### Checklist
- [ ] Can explain difference between APX, PTAS, FPTAS
- [ ] Can prove 2-approximation for Vertex Cover
- [ ] Understand LP rounding and integrality gap
- [ ] Can apply primal-dual method to new problems
- [ ] Know hardness results (e.g., PCP theorem implications)

### Reflection Questions
1. Why does the same problem (e.g., VC) have both easy approximation and hard exact solution?
2. How does metric property enable Christofides but not general TSP approximation?
3. What role does LP relaxation play in approximation algorithm design?

### Next Steps
- **Deepen**: Study PCP theorem and hardness of approximation
- **Connect**: Relate to online algorithms and competitive analysis
- **Apply**: Implement approximation algorithms for practical optimization problems

**Related Sessions**:
- ← [Session 23: Cache-Oblivious Algorithms](Session_23_Cache_Oblivious_Algorithms.md)
- → [Session 25: PAC Learning](Session_25_PAC_Learning.md)

---

*Session 24 of Cycle 4 • Expert Mastery*
