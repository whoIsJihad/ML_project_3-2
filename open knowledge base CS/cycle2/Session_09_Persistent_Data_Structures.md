# Session 9 – Persistent Data Structures & Functional Amortization

## Linked Domain
[[Algorithms & Complexity]]

**Cycle**: 2 (Intermediate Depth)  
**Difficulty**: ⚫⚫⚪⚪

---

## Phase 1 – Clean Theory

### Definitions

**Persistent Data Structure**: A data structure that preserves all previous versions when modified. Operations create new versions without destroying old ones.

**Ephemeral**: Standard data structures where updates destroy old versions.

**Partial Persistence**: All versions can be accessed, but only newest can be modified.

**Full Persistence**: Any version can be accessed and modified (creates branching version tree).

**Confluent Persistence**: Can combine multiple versions to create new version (rarely needed).

**Path Copying**: Create new nodes along path from root to modified node, copying unchanged structure.

**Fat Node**: Store all historical values in each node with timestamps. Node size grows over time.

**Node Splitting**: When node becomes too fat, split into multiple time-stamped nodes.

**Functional Amortized Analysis**: Amortization in persistent setting requires "banker's method" or "physicist's method" to track credit across versions.

---

### Core Mechanism

**Path Copying Example (Binary Search Tree)**:
```
Original:        After insert(7):
    5                 5' (new)
   / \               / \
  3   8             3   8' (new)
     / \               / \
    6   9             6   9
                       \
                        7 (new)
```
Only $O(\log n)$ nodes copied for balanced tree.

**Fat Node Example**:
```
Node: [key: x, values: [(t=0, left=p1, right=p2), 
                        (t=5, left=p3, right=p2),
                        (t=8, left=p3, right=p4)]]
```
To access at time $t$, find largest timestamp $\leq t$.

**Functional Amortization Problem**:
In ephemeral structures, you can "charge" expensive operations to cheap ones. In persistent structures, if you copy a version, you "copy" the accumulated debt, allowing unlimited "spending" of the same credit. Must use **banker's method** where credit is non-copyable.

---

### Mental Model

**Key Insight**: Persistence trades space for history. Every update potentially creates $O(\text{height})$ new nodes in tree structures.

**Design Choice Tradeoffs**:
```
Path Copying:
  + Simple to implement
  + Space: O(m * h) for m updates, height h
  - Worst for frequently updated nodes

Fat Node:
  + Better space when few updates per node
  + Access requires binary search in timestamps
  - Unbounded node size

Node Splitting:
  + Bounded node size
  + Access still O(log t) per node
  - More complex implementation
```

**Persistence Techniques by Access Pattern**:
- Frequent access to recent versions → Path copying
- Random access across time → Fat nodes with splitting
- Linear version history → Simple versioning with diffs

---

### Edge Cases

1. **Copying Large Structures**: If object is large (e.g., array), path copying becomes $O(n)$ per update. Need different technique (e.g., array mapped tries).

2. **Circular Links**: Path copying breaks with cycles. Must use indirection or fall back to fat nodes.

3. **Garbage Collection**: Old versions consume space indefinitely. Need explicit GC or reference counting across versions.

4. **Amortization Failure**: Can't use potential method naively. Example: Build a version, copy it $k$ times, trigger expensive operation on each copy = $k \times \text{expensive cost}$ but only paid once.

5. **Version Explosion**: $n$ updates create up to $n$ versions. If all kept, space is $O(n^2)$ worst-case.

---

### Common Mistakes

1. **Thinking persistence is "free"**: Path copying is $O(h)$ per update, not $O(1)$. For short trees or frequent updates, ephemeral can be faster.

2. **Ignoring fat node sizes**: Fat nodes grow unbounded without splitting. Can cause memory blowup.

3. **Using potential method for amortization**: Doesn't work in persistent setting. Must use banker's method with explicit "credits" that aren't copyable.

4. **Not handling version GC**: Keeping all versions forever eventually exhausts memory.

5. **Copying immutable parts**: In path copying, forgetting to share unchanged subtrees. Should only copy $O(h)$ nodes, not entire tree.

---

### Code Snippet – Persistent Binary Search Tree

```python
class Node:
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

class PersistentBST:
    """Persistent BST using path copying."""
    
    def __init__(self, root=None):
        self.root = root
    
    def insert(self, key, value):
        """Returns NEW tree with key inserted."""
        new_root = self._insert(self.root, key, value)
        return PersistentBST(new_root)
    
    def _insert(self, node, key, value):
        if node is None:
            return Node(key, value)
        
        # Path copying: create new node
        if key < node.key:
            new_left = self._insert(node.left, key, value)
            return Node(node.key, node.value, new_left, node.right)
        elif key > node.key:
            new_right = self._insert(node.right, key, value)
            return Node(node.key, node.value, node.left, new_right)
        else:
            # Update: still creates new node
            return Node(key, value, node.left, node.right)
    
    def find(self, key):
        """Search in this version."""
        node = self.root
        while node:
            if key == node.key:
                return node.value
            node = node.left if key < node.key else node.right
        return None

# Usage demonstrating persistence
v0 = PersistentBST()
v1 = v0.insert(5, "a")
v2 = v1.insert(3, "b")
v3 = v2.insert(7, "c")

# All versions still accessible
print(v1.find(5))  # "a"
print(v1.find(3))  # None (not in v1)
print(v2.find(3))  # "b"
print(v3.find(7))  # "c"

# v1, v2, v3 share structure (only modified paths differ)
```

---

## Phase 2 – Conceptual Stress Questions

**Q1**: Prove that the standard amortized analysis for (ephemeral) red-black tree insertions ($O(1)$ amortized rotations per insert) does NOT hold for persistent red-black trees. Construct a sequence of insertions where the persistent version requires $\Omega(\log n)$ rotations per insert, even amortized. How does this change the asymptotic complexity?

**Q2**: You implement a persistent array using path copying on a balanced binary tree (array indices map to leaves). Show that:
- Get/set operations are $O(\log n)$
- Space per version is $O(\log n)$ per update

Now your colleague suggests: "Use a 32-way tree instead of binary for better cache locality." Analyze: Does this improve performance? What's the critical tree arity $k$ that minimizes $\text{copies} + \text{cache-misses}$ per update?

**Q3**: Design a **retroactive** data structure: not just access past versions, but *modify* past versions. When you update version $t$, all versions $t' > t$ must be recomputed. Give an example data structure where retroactive updates are:
- Efficient: $O(\log n)$ per retroactive update
- Expensive: $\Omega(n)$ per retroactive update

What property distinguishes the two cases?

---

## Phase 3 – Applied Problem

**Problem Statement**:

You're implementing a **version control system** (like Git) for a large codebase. Files are represented as persistent data structures to support:
- **Commit**: Create new version with some files modified
- **Checkout**: Access any historical version
- **Merge**: Combine two versions
- **Diff**: Find changes between versions

**Part A – Data Structure Design**:
Files are represented as strings up to 1MB. Naive approach: store full copy per version. Space: $O(n \cdot m)$ for $n$ versions, $m$ = file size.

Design a persistent string data structure using:
- Balanced binary tree where leaves are chunks (1KB each)
- Path copying for modifications

Compute:
- Space per version after $k$ edits (each edit modifies one chunk)
- Time complexity for edit, diff, merge
- Compare with Git's approach (delta compression + Merkle DAG)

**Part B – Amortized Analysis**:
Your persistent string supports:
- `insert(pos, char)`: $O(\log n)$
- `delete(pos)`: $O(\log n)$
- Rebalancing cost amortized using red-black tree

In persistent setting, prove or disprove: rebalancing is still $O(1)$ amortized per operation across all versions.

Hint: Consider this attack: Create version $v$, copy it $k$ times to get $v_1, \ldots, v_k$, then perform an operation on each that triggers rebalancing. What's the total cost?

**Part C – Garbage Collection**:
After 10,000 commits, you have 10,000 versions. Most are never accessed. Design a GC scheme:
- Keep only versions with "tags" (e.g., releases) + last $N$ commits
- Reachability: any version reachable from kept versions must be retained

Prove that your GC is correct (never deletes reachable data). Compute space complexity after GC as function of:
- Number of tags $t$
- Window size $N$
- Edit distance between versions

---

## Phase 4 – Feedback & Weakness Log Update

**Awaiting your responses to Phase 2 and Phase 3.**

Critique will focus on:
- Understanding why standard amortization fails
- Space-time tradeoffs in persistent structures
- Correctness of retroactive/GC algorithms
- Comparison with real systems (Git)

---

## Cross-Links for Reinforcement
- [[Session 2: Amortized Analysis]] (prerequisite)
- [[Functional Data Structures (Okasaki)]]
- [[Git Internals & Merkle DAG]]
- [[Retroactive Data Structures]]
- [[Confluent Persistence]]

---

**Status**: Awaiting Phase 2 & 3 responses.
