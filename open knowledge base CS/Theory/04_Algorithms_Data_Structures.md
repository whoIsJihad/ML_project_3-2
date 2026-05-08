# Algorithms & Data Structures

## Course Overview
**Depth:** University undergraduate + interview-ready  
**Time:** 3-4 hours focused reading  
**Prerequisites:** Basic programming, discrete math fundamentals

---

# Part I: Foundational Data Structures

---

## 1. Arrays

### Memory Model
Arrays are contiguous blocks of memory. Given base address `B` and element size `S`:
```
Address of element[i] = B + (i × S)
```

**Key Insight:** This is why array indexing is O(1) - it's just arithmetic.

### Static vs Dynamic Arrays

**Static Array:**
- Fixed size at compile time
- Stack or data segment allocation
- No runtime overhead

**Dynamic Array (Vector):**
- Resizable at runtime
- Heap allocation
- Amortized O(1) append

**Dynamic Array Growth Strategy:**
When capacity is reached, allocate new array of size `k × old_capacity` (typically k=2).

**Amortized Analysis:**
- Individual append: O(n) worst case (copy all elements)
- But copying happens rarely
- Amortized cost per append: O(1)

**Proof:** After n insertions with doubling:
- Total copies: 1 + 2 + 4 + 8 + ... + n/2 = n - 1
- Average per insertion: (n-1)/n ≈ 1 = O(1)

### Multi-dimensional Arrays

**Row-major order (C/C++):**
```
A[i][j] = Base + ((i × num_cols) + j) × element_size
```

**Column-major order (Fortran, MATLAB):**
```
A[i][j] = Base + ((j × num_rows) + i) × element_size
```

**Cache Implications:**
```c
// Good: Sequential access (row-major)
for (int i = 0; i < rows; i++)
    for (int j = 0; j < cols; j++)
        sum += A[i][j];

// Bad: Strided access
for (int j = 0; j < cols; j++)
    for (int i = 0; i < rows; i++)
        sum += A[i][j];  // Cache miss every access
```

---

## 2. Linked Lists

### Node Structure
```c
struct Node {
    int data;
    struct Node* next;
};
```

### Singly Linked List Operations

**Insertion at Head: O(1)**
```c
Node* insert_head(Node* head, int value) {
    Node* new_node = malloc(sizeof(Node));
    new_node->data = value;
    new_node->next = head;
    return new_node;
}
```

**Insertion at Tail: O(n) or O(1) with tail pointer**
```c
void insert_tail(Node** head, Node** tail, int value) {
    Node* new_node = malloc(sizeof(Node));
    new_node->data = value;
    new_node->next = NULL;
    
    if (*tail == NULL) {
        *head = *tail = new_node;
    } else {
        (*tail)->next = new_node;
        *tail = new_node;
    }
}
```

**Deletion: O(n) search + O(1) removal**
```c
Node* delete_node(Node* head, int value) {
    if (head == NULL) return NULL;
    
    if (head->data == value) {
        Node* temp = head->next;
        free(head);
        return temp;
    }
    
    Node* curr = head;
    while (curr->next != NULL && curr->next->data != value) {
        curr = curr->next;
    }
    
    if (curr->next != NULL) {
        Node* temp = curr->next;
        curr->next = curr->next->next;
        free(temp);
    }
    return head;
}
```

### Doubly Linked List
```c
struct DNode {
    int data;
    struct DNode* prev;
    struct DNode* next;
};
```

**Advantages:**
- O(1) deletion given node pointer (no need to find predecessor)
- Bidirectional traversal
- Essential for LRU cache implementation

**Disadvantages:**
- More memory per node
- More complex insert/delete logic

### Circular Linked List
- Last node points to first node
- Use cases: Round-robin scheduling, circular buffers

### Classic Problems

**Reverse a Linked List:**
```c
Node* reverse(Node* head) {
    Node* prev = NULL;
    Node* curr = head;
    
    while (curr != NULL) {
        Node* next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}
```

**Detect Cycle (Floyd's Tortoise and Hare):**
```c
bool has_cycle(Node* head) {
    Node* slow = head;
    Node* fast = head;
    
    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}
```

**Find Cycle Start:**
When slow and fast meet, reset slow to head. Move both one step at a time. They meet at cycle start.

**Why it works:** Let:
- Distance to cycle start = F
- Cycle length = C
- Meeting point distance from cycle start = a

When they meet: slow traveled F + a, fast traveled F + a + nC (for some n)
Since fast travels 2× speed: 2(F + a) = F + a + nC → F + a = nC → F = nC - a

So starting from head, after F steps, you reach cycle start.
Starting from meeting point (a steps into cycle), after F = nC - a steps, you also reach cycle start.

---

## 3. Stacks

### Abstract Data Type
- **Push(x):** Add element to top
- **Pop():** Remove and return top element
- **Peek()/Top():** Return top element without removing
- **IsEmpty():** Check if stack is empty

**LIFO:** Last In, First Out

### Array-based Implementation
```c
#define MAX_SIZE 1000

typedef struct {
    int data[MAX_SIZE];
    int top;
} Stack;

void init(Stack* s) { s->top = -1; }
bool is_empty(Stack* s) { return s->top == -1; }
bool is_full(Stack* s) { return s->top == MAX_SIZE - 1; }

void push(Stack* s, int value) {
    if (is_full(s)) return;  // Handle overflow
    s->data[++s->top] = value;
}

int pop(Stack* s) {
    if (is_empty(s)) return -1;  // Handle underflow
    return s->data[s->top--];
}

int peek(Stack* s) {
    if (is_empty(s)) return -1;
    return s->data[s->top];
}
```

### Linked List Implementation
- Push: Insert at head O(1)
- Pop: Remove from head O(1)
- Advantage: No fixed size limit
- Disadvantage: Memory overhead per element

### Applications

**1. Function Call Stack:**
- Local variables, return addresses
- Stack overflow from deep recursion

**2. Expression Evaluation:**

**Infix to Postfix (Shunting Yard Algorithm):**
```
Input: 3 + 4 * 2
Output: 3 4 2 * +

Rules:
- Number → output
- Operator → pop higher/equal precedence to output, then push
- ( → push
- ) → pop until (
- End → pop all to output
```

**Evaluate Postfix:**
```c
int evaluate_postfix(char* expr) {
    Stack s;
    init(&s);
    
    for (int i = 0; expr[i]; i++) {
        if (isdigit(expr[i])) {
            push(&s, expr[i] - '0');
        } else {
            int b = pop(&s);
            int a = pop(&s);
            switch(expr[i]) {
                case '+': push(&s, a + b); break;
                case '-': push(&s, a - b); break;
                case '*': push(&s, a * b); break;
                case '/': push(&s, a / b); break;
            }
        }
    }
    return pop(&s);
}
```

**3. Parentheses Matching:**
```c
bool is_balanced(char* expr) {
    Stack s;
    init(&s);
    
    for (int i = 0; expr[i]; i++) {
        if (expr[i] == '(' || expr[i] == '[' || expr[i] == '{') {
            push(&s, expr[i]);
        } else if (expr[i] == ')' || expr[i] == ']' || expr[i] == '}') {
            if (is_empty(&s)) return false;
            char top = pop(&s);
            if ((expr[i] == ')' && top != '(') ||
                (expr[i] == ']' && top != '[') ||
                (expr[i] == '}' && top != '{'))
                return false;
        }
    }
    return is_empty(&s);
}
```

**4. Monotonic Stack:**
For "next greater element" type problems.

```c
// Find next greater element for each position
void next_greater(int arr[], int n, int result[]) {
    Stack s;
    init(&s);
    
    for (int i = n - 1; i >= 0; i--) {
        while (!is_empty(&s) && peek(&s) <= arr[i]) {
            pop(&s);
        }
        result[i] = is_empty(&s) ? -1 : peek(&s);
        push(&s, arr[i]);
    }
}
```

---

## 4. Queues

### Abstract Data Type
- **Enqueue(x):** Add element to rear
- **Dequeue():** Remove and return front element
- **Front():** Return front element
- **IsEmpty():** Check if queue is empty

**FIFO:** First In, First Out

### Circular Array Implementation
```c
typedef struct {
    int data[MAX_SIZE];
    int front;
    int rear;
    int size;
} Queue;

void init(Queue* q) {
    q->front = 0;
    q->rear = -1;
    q->size = 0;
}

bool is_empty(Queue* q) { return q->size == 0; }
bool is_full(Queue* q) { return q->size == MAX_SIZE; }

void enqueue(Queue* q, int value) {
    if (is_full(q)) return;
    q->rear = (q->rear + 1) % MAX_SIZE;
    q->data[q->rear] = value;
    q->size++;
}

int dequeue(Queue* q) {
    if (is_empty(q)) return -1;
    int value = q->data[q->front];
    q->front = (q->front + 1) % MAX_SIZE;
    q->size--;
    return value;
}
```

### Deque (Double-ended Queue)
- Insert/remove from both ends
- Used to implement both stack and queue
- Key structure for sliding window maximum

### Priority Queue
- Elements have priorities
- Dequeue returns highest priority element
- Implemented efficiently with heaps (see Heap section)

### Applications

**1. BFS (Breadth-First Search)**
**2. Task Scheduling (Round-robin)**
**3. Buffer Management**

---

## 5. Hash Tables

### Core Concept
Map keys to array indices using a hash function.

**Ideal Properties of Hash Function:**
1. Deterministic (same key → same hash)
2. Uniform distribution
3. Fast to compute

### Hash Functions

**Division Method:**
```
h(k) = k mod m
```
Choose m as prime not close to power of 2.

**Multiplication Method:**
```
h(k) = floor(m × (k × A mod 1))
```
A ≈ 0.6180339887 (golden ratio - 1) works well.

**String Hashing (Polynomial Rolling Hash):**
```c
unsigned long hash_string(char* str) {
    unsigned long hash = 0;
    int p = 31;  // prime
    long p_pow = 1;
    
    for (int i = 0; str[i]; i++) {
        hash += (str[i] - 'a' + 1) * p_pow;
        p_pow *= p;
    }
    return hash;
}
```

### Collision Resolution

**1. Chaining (Separate Chaining):**
Each bucket contains a linked list of entries.

```c
#define TABLE_SIZE 1000

typedef struct Entry {
    char* key;
    int value;
    struct Entry* next;
} Entry;

typedef struct {
    Entry* buckets[TABLE_SIZE];
} HashMap;

void put(HashMap* map, char* key, int value) {
    unsigned long idx = hash_string(key) % TABLE_SIZE;
    
    // Check if key exists
    Entry* curr = map->buckets[idx];
    while (curr != NULL) {
        if (strcmp(curr->key, key) == 0) {
            curr->value = value;  // Update
            return;
        }
        curr = curr->next;
    }
    
    // Insert new entry at head
    Entry* new_entry = malloc(sizeof(Entry));
    new_entry->key = strdup(key);
    new_entry->value = value;
    new_entry->next = map->buckets[idx];
    map->buckets[idx] = new_entry;
}

int get(HashMap* map, char* key) {
    unsigned long idx = hash_string(key) % TABLE_SIZE;
    Entry* curr = map->buckets[idx];
    
    while (curr != NULL) {
        if (strcmp(curr->key, key) == 0) {
            return curr->value;
        }
        curr = curr->next;
    }
    return -1;  // Not found
}
```

**2. Open Addressing:**
All elements stored in the table itself. On collision, probe for next empty slot.

**Linear Probing:**
```
h(k, i) = (h(k) + i) mod m
```
Problem: Primary clustering (long runs of occupied slots)

**Quadratic Probing:**
```
h(k, i) = (h(k) + c₁×i + c₂×i²) mod m
```
Problem: Secondary clustering (keys with same hash follow same probe sequence)

**Double Hashing:**
```
h(k, i) = (h₁(k) + i × h₂(k)) mod m
```
Best distribution, but slower.

### Load Factor and Rehashing

**Load Factor:** α = n/m (entries / table size)

**Performance:**
- Chaining: Expected O(1 + α) per operation
- Open addressing: Expected O(1/(1-α)) for unsuccessful search

**Rehashing:** When α exceeds threshold (often 0.75):
1. Allocate larger table (typically 2×)
2. Reinsert all elements
3. Amortized O(1)

### Time Complexity Summary

| Operation | Average | Worst |
|-----------|---------|-------|
| Insert | O(1) | O(n) |
| Delete | O(1) | O(n) |
| Search | O(1) | O(n) |

Worst case occurs with pathological hash collisions.

---

## 6. Trees

### Binary Tree Basics

```c
typedef struct TreeNode {
    int data;
    struct TreeNode* left;
    struct TreeNode* right;
} TreeNode;
```

### Tree Traversals

**Preorder (Root, Left, Right):**
```c
void preorder(TreeNode* root) {
    if (root == NULL) return;
    printf("%d ", root->data);
    preorder(root->left);
    preorder(root->right);
}
```

**Inorder (Left, Root, Right):**
```c
void inorder(TreeNode* root) {
    if (root == NULL) return;
    inorder(root->left);
    printf("%d ", root->data);
    inorder(root->right);
}
```

**Postorder (Left, Right, Root):**
```c
void postorder(TreeNode* root) {
    if (root == NULL) return;
    postorder(root->left);
    postorder(root->right);
    printf("%d ", root->data);
}
```

**Level Order (BFS):**
```c
void level_order(TreeNode* root) {
    if (root == NULL) return;
    
    Queue q;
    init(&q);
    enqueue(&q, root);
    
    while (!is_empty(&q)) {
        TreeNode* node = dequeue(&q);
        printf("%d ", node->data);
        
        if (node->left) enqueue(&q, node->left);
        if (node->right) enqueue(&q, node->right);
    }
}
```

**Iterative Inorder (using stack):**
```c
void inorder_iterative(TreeNode* root) {
    Stack s;
    init(&s);
    TreeNode* curr = root;
    
    while (curr != NULL || !is_empty(&s)) {
        while (curr != NULL) {
            push(&s, curr);
            curr = curr->left;
        }
        curr = pop(&s);
        printf("%d ", curr->data);
        curr = curr->right;
    }
}
```

### Binary Search Tree (BST)

**Property:** For every node, all left descendants < node < all right descendants

**Search: O(h)**
```c
TreeNode* search(TreeNode* root, int key) {
    if (root == NULL || root->data == key)
        return root;
    
    if (key < root->data)
        return search(root->left, key);
    else
        return search(root->right, key);
}
```

**Insert: O(h)**
```c
TreeNode* insert(TreeNode* root, int key) {
    if (root == NULL) {
        TreeNode* node = malloc(sizeof(TreeNode));
        node->data = key;
        node->left = node->right = NULL;
        return node;
    }
    
    if (key < root->data)
        root->left = insert(root->left, key);
    else if (key > root->data)
        root->right = insert(root->right, key);
    
    return root;
}
```

**Delete: O(h)**
Three cases:
1. **Leaf node:** Simply remove
2. **One child:** Replace with child
3. **Two children:** Replace with inorder successor (or predecessor)

```c
TreeNode* find_min(TreeNode* root) {
    while (root->left != NULL)
        root = root->left;
    return root;
}

TreeNode* delete_node(TreeNode* root, int key) {
    if (root == NULL) return NULL;
    
    if (key < root->data) {
        root->left = delete_node(root->left, key);
    } else if (key > root->data) {
        root->right = delete_node(root->right, key);
    } else {
        // Found node to delete
        if (root->left == NULL) {
            TreeNode* temp = root->right;
            free(root);
            return temp;
        } else if (root->right == NULL) {
            TreeNode* temp = root->left;
            free(root);
            return temp;
        }
        
        // Two children: get inorder successor
        TreeNode* successor = find_min(root->right);
        root->data = successor->data;
        root->right = delete_node(root->right, successor->data);
    }
    return root;
}
```

**BST Complexity:**
- Balanced: O(log n) for all operations
- Skewed (worst case): O(n)

### AVL Trees

**Balance Factor:** height(left) - height(right)
**AVL Property:** |Balance Factor| ≤ 1 for all nodes

**Rotations:**

```
Left Rotation (when right-heavy):

    x                y
     \              / \
      y     →      x   z
       \
        z

Right Rotation (when left-heavy):

      x            y
     /            / \
    y      →     z   x
   /
  z
```

**Left-Right (LR) Rotation:**
```
    x              x            z
   /              /            / \
  y      →       z      →     y   x
   \            /
    z          y
```

**Right-Left (RL) Rotation:**
```
  x            x              z
   \            \            / \
    y    →       z    →     x   y
   /              \
  z                y
```

**After each insert/delete:**
1. Update heights bottom-up
2. Check balance factors
3. Rotate if needed

### Red-Black Trees

**Properties:**
1. Every node is red or black
2. Root is black
3. All leaves (NIL) are black
4. Red node has black children (no red-red)
5. All paths from node to leaves have same number of black nodes

**Guarantees:** Height ≤ 2 log(n+1)

**Comparison with AVL:**
- AVL: Stricter balance, faster lookups
- Red-Black: Faster insertions/deletions, less rotations
- Red-Black used in: std::map, Linux kernel

---

## 7. Heaps

### Binary Heap Properties
1. **Complete binary tree:** All levels full except last (filled left to right)
2. **Heap property:** 
   - Max-heap: parent ≥ children
   - Min-heap: parent ≤ children

### Array Representation
```
Parent(i) = (i - 1) / 2
Left(i) = 2i + 1
Right(i) = 2i + 2
```

### Operations

**Heapify (Sift Down): O(log n)**
```c
void max_heapify(int arr[], int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    
    if (left < n && arr[left] > arr[largest])
        largest = left;
    if (right < n && arr[right] > arr[largest])
        largest = right;
    
    if (largest != i) {
        swap(&arr[i], &arr[largest]);
        max_heapify(arr, n, largest);
    }
}
```

**Build Heap: O(n)**
```c
void build_heap(int arr[], int n) {
    // Start from last non-leaf node
    for (int i = n / 2 - 1; i >= 0; i--) {
        max_heapify(arr, n, i);
    }
}
```

**Why O(n)?** Most nodes are near bottom with small heapify cost.
Mathematical analysis: Sum of work at each level = O(n).

**Insert: O(log n)**
```c
void insert(int arr[], int* n, int key) {
    // Add at end
    arr[*n] = key;
    int i = (*n)++;
    
    // Bubble up
    while (i > 0 && arr[(i-1)/2] < arr[i]) {
        swap(&arr[i], &arr[(i-1)/2]);
        i = (i - 1) / 2;
    }
}
```

**Extract Max: O(log n)**
```c
int extract_max(int arr[], int* n) {
    if (*n <= 0) return INT_MIN;
    
    int max = arr[0];
    arr[0] = arr[--(*n)];
    max_heapify(arr, *n, 0);
    
    return max;
}
```

### Heap Sort: O(n log n)
```c
void heap_sort(int arr[], int n) {
    build_heap(arr, n);  // O(n)
    
    for (int i = n - 1; i > 0; i--) {
        swap(&arr[0], &arr[i]);  // Move max to end
        max_heapify(arr, i, 0);  // Restore heap property
    }
}
```

### Priority Queue with Heaps

Standard library typically uses heap-based priority queue.
- Insert: O(log n)
- Get/Remove max (or min): O(log n)
- Peek: O(1)

### Applications
1. **Dijkstra's algorithm**
2. **Huffman coding**
3. **K largest elements**
4. **Median maintenance** (one max-heap, one min-heap)

---

## 8. Graphs

### Representations

**Adjacency Matrix:**
```c
int graph[V][V];  // graph[i][j] = 1 if edge i→j exists
```
- Space: O(V²)
- Check edge: O(1)
- Find neighbors: O(V)
- Good for dense graphs

**Adjacency List:**
```c
typedef struct {
    int* neighbors;
    int count;
} AdjList;

AdjList graph[V];
```
- Space: O(V + E)
- Check edge: O(degree)
- Find neighbors: O(degree)
- Good for sparse graphs

### Graph Traversals

**Depth-First Search (DFS):**
```c
bool visited[V];

void dfs(int v) {
    visited[v] = true;
    printf("%d ", v);
    
    for (int i = 0; i < graph[v].count; i++) {
        int u = graph[v].neighbors[i];
        if (!visited[u]) {
            dfs(u);
        }
    }
}
```

**Iterative DFS using Stack:**
```c
void dfs_iterative(int start) {
    Stack s;
    push(&s, start);
    
    while (!is_empty(&s)) {
        int v = pop(&s);
        
        if (visited[v]) continue;
        visited[v] = true;
        printf("%d ", v);
        
        for (int i = 0; i < graph[v].count; i++) {
            int u = graph[v].neighbors[i];
            if (!visited[u]) {
                push(&s, u);
            }
        }
    }
}
```

**Breadth-First Search (BFS):**
```c
void bfs(int start) {
    Queue q;
    enqueue(&q, start);
    visited[start] = true;
    
    while (!is_empty(&q)) {
        int v = dequeue(&q);
        printf("%d ", v);
        
        for (int i = 0; i < graph[v].count; i++) {
            int u = graph[v].neighbors[i];
            if (!visited[u]) {
                visited[u] = true;
                enqueue(&q, u);
            }
        }
    }
}
```

**BFS Properties:**
- Finds shortest path in unweighted graphs
- Level-order traversal
- Time: O(V + E)

### Shortest Paths

**Dijkstra's Algorithm (non-negative weights):**
```c
int dijkstra(int src, int dst) {
    int dist[V];
    bool done[V] = {false};
    
    for (int i = 0; i < V; i++) dist[i] = INT_MAX;
    dist[src] = 0;
    
    // Priority Queue (min-heap)
    PriorityQueue pq;
    pq_insert(&pq, src, 0);
    
    while (!pq_empty(&pq)) {
        int u = pq_extract_min(&pq);
        
        if (done[u]) continue;
        done[u] = true;
        
        for (each neighbor v of u) {
            int weight = edge_weight(u, v);
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq_insert(&pq, v, dist[v]);
            }
        }
    }
    
    return dist[dst];
}
```

**Complexity:** O((V + E) log V) with binary heap

**Bellman-Ford (handles negative weights):**
```c
bool bellman_ford(int src, int dist[]) {
    for (int i = 0; i < V; i++) dist[i] = INT_MAX;
    dist[src] = 0;
    
    // Relax all edges V-1 times
    for (int i = 0; i < V - 1; i++) {
        for (each edge (u, v, w)) {
            if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
            }
        }
    }
    
    // Check for negative cycle
    for (each edge (u, v, w)) {
        if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
            return false;  // Negative cycle exists
        }
    }
    return true;
}
```

**Complexity:** O(VE)

**Floyd-Warshall (all pairs):**
```c
void floyd_warshall(int dist[V][V]) {
    // dist[i][j] initialized to edge weight or INF
    
    for (int k = 0; k < V; k++) {
        for (int i = 0; i < V; i++) {
            for (int j = 0; j < V; j++) {
                if (dist[i][k] != INF && dist[k][j] != INF) {
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
                }
            }
        }
    }
}
```

**Complexity:** O(V³)

### Minimum Spanning Tree

**Prim's Algorithm:**
```c
int prim() {
    bool inMST[V] = {false};
    int key[V];
    
    for (int i = 0; i < V; i++) key[i] = INT_MAX;
    key[0] = 0;
    
    int totalWeight = 0;
    
    for (int count = 0; count < V; count++) {
        // Pick minimum key vertex not in MST
        int u = min_key_vertex(key, inMST);
        inMST[u] = true;
        totalWeight += key[u];
        
        // Update keys of adjacent vertices
        for (each neighbor v of u) {
            int w = edge_weight(u, v);
            if (!inMST[v] && w < key[v]) {
                key[v] = w;
            }
        }
    }
    
    return totalWeight;
}
```

**Complexity:** O(V²) or O(E log V) with heap

**Kruskal's Algorithm (Union-Find):**
```c
// Sort edges by weight
sort(edges, E);

int mst_weight = 0;
int edges_added = 0;

for (int i = 0; i < E && edges_added < V - 1; i++) {
    int u = edges[i].u;
    int v = edges[i].v;
    int w = edges[i].weight;
    
    if (find(u) != find(v)) {
        union(u, v);
        mst_weight += w;
        edges_added++;
    }
}
```

**Complexity:** O(E log E)

### Topological Sort

**For Directed Acyclic Graph (DAG):**

**DFS-based:**
```c
void topo_sort_util(int v, bool visited[], Stack* stack) {
    visited[v] = true;
    
    for (each neighbor u of v) {
        if (!visited[u]) {
            topo_sort_util(u, visited, stack);
        }
    }
    
    push(stack, v);  // Add after all descendants
}

void topological_sort() {
    bool visited[V] = {false};
    Stack stack;
    
    for (int v = 0; v < V; v++) {
        if (!visited[v]) {
            topo_sort_util(v, visited, &stack);
        }
    }
    
    // Stack contains vertices in topological order
    while (!is_empty(&stack)) {
        printf("%d ", pop(&stack));
    }
}
```

**Kahn's Algorithm (BFS-based):**
```c
void kahn_topological_sort() {
    int in_degree[V] = {0};
    
    // Calculate in-degrees
    for (int v = 0; v < V; v++) {
        for (each neighbor u of v) {
            in_degree[u]++;
        }
    }
    
    Queue q;
    for (int v = 0; v < V; v++) {
        if (in_degree[v] == 0) {
            enqueue(&q, v);
        }
    }
    
    int count = 0;
    
    while (!is_empty(&q)) {
        int v = dequeue(&q);
        printf("%d ", v);
        count++;
        
        for (each neighbor u of v) {
            if (--in_degree[u] == 0) {
                enqueue(&q, u);
            }
        }
    }
    
    if (count != V) {
        printf("Graph has cycle!");
    }
}
```

### Cycle Detection

**Undirected Graph (DFS):**
```c
bool has_cycle_undirected(int v, int parent) {
    visited[v] = true;
    
    for (each neighbor u of v) {
        if (!visited[u]) {
            if (has_cycle_undirected(u, v)) return true;
        } else if (u != parent) {
            return true;  // Back edge found
        }
    }
    return false;
}
```

**Directed Graph (DFS with colors):**
```c
#define WHITE 0  // Unvisited
#define GRAY 1   // In progress
#define BLACK 2  // Done

int color[V];

bool has_cycle_directed(int v) {
    color[v] = GRAY;
    
    for (each neighbor u of v) {
        if (color[u] == GRAY) return true;  // Back edge
        if (color[u] == WHITE && has_cycle_directed(u)) return true;
    }
    
    color[v] = BLACK;
    return false;
}
```

### Strongly Connected Components (Kosaraju's)

```c
// Step 1: DFS on original graph, push to stack by finish time
void dfs_fill_order(int v, bool visited[], Stack* stack) {
    visited[v] = true;
    for (each neighbor u of v) {
        if (!visited[u]) dfs_fill_order(u, visited, stack);
    }
    push(stack, v);
}

// Step 2: Transpose graph
// Step 3: DFS on transposed graph in order from stack

void kosaraju() {
    Stack stack;
    bool visited[V] = {false};
    
    // Fill vertices in stack by finish time
    for (int v = 0; v < V; v++) {
        if (!visited[v]) {
            dfs_fill_order(v, visited, &stack);
        }
    }
    
    // Create transposed graph
    transpose_graph();
    
    // Mark all vertices as not visited
    memset(visited, false, sizeof(visited));
    
    // Process vertices in order from stack
    while (!is_empty(&stack)) {
        int v = pop(&stack);
        if (!visited[v]) {
            dfs(v, visited);  // Each DFS call is one SCC
            printf("\n");
        }
    }
}
```

---

# Part II: Algorithm Design Paradigms

---

## 9. Recursion and Divide & Conquer

### Recursion Fundamentals

**Key Components:**
1. **Base case:** Terminates recursion
2. **Recursive case:** Reduces problem size
3. **Progress:** Must move toward base case

**Example - Factorial:**
```c
int factorial(int n) {
    if (n <= 1) return 1;        // Base case
    return n * factorial(n - 1);  // Recursive case
}
```

**Stack Space:** O(depth of recursion)

### Divide and Conquer Pattern

1. **Divide:** Break problem into subproblems
2. **Conquer:** Solve subproblems recursively
3. **Combine:** Merge solutions

**Master Theorem:**
For T(n) = aT(n/b) + f(n):

Let c = log_b(a)

Case 1: f(n) = O(n^(c-ε)) → T(n) = Θ(n^c)
Case 2: f(n) = Θ(n^c) → T(n) = Θ(n^c log n)
Case 3: f(n) = Ω(n^(c+ε)) → T(n) = Θ(f(n))

### Merge Sort: O(n log n)

```c
void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1;
    int n2 = r - m;
    
    int L[n1], R[n2];
    
    for (int i = 0; i < n1; i++) L[i] = arr[l + i];
    for (int i = 0; i < n2; i++) R[i] = arr[m + 1 + i];
    
    int i = 0, j = 0, k = l;
    
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k++] = L[i++];
        } else {
            arr[k++] = R[j++];
        }
    }
    
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

void merge_sort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        merge_sort(arr, l, m);
        merge_sort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}
```

**Recurrence:** T(n) = 2T(n/2) + O(n)
**Solution:** O(n log n)

### Quick Sort

```c
int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    
    swap(&arr[i + 1], &arr[high]);
    return i + 1;
}

void quick_sort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quick_sort(arr, low, pi - 1);
        quick_sort(arr, pi + 1, high);
    }
}
```

**Best/Average:** O(n log n)
**Worst:** O(n²) when pivot always smallest/largest

**Optimization - Random Pivot:**
```c
int randomized_partition(int arr[], int low, int high) {
    int random = low + rand() % (high - low + 1);
    swap(&arr[random], &arr[high]);
    return partition(arr, low, high);
}
```

### Binary Search: O(log n)

```c
int binary_search(int arr[], int n, int target) {
    int low = 0, high = n - 1;
    
    while (low <= high) {
        int mid = low + (high - low) / 2;  // Avoid overflow
        
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    
    return -1;  // Not found
}
```

**Variations:**
- Lower bound: First element ≥ target
- Upper bound: First element > target
- Search in rotated sorted array

### Counting Inversions: O(n log n)

An inversion is a pair (i, j) where i < j but arr[i] > arr[j].

```c
long long merge_count(int arr[], int temp[], int l, int m, int r) {
    int i = l, j = m + 1, k = l;
    long long inv_count = 0;
    
    while (i <= m && j <= r) {
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
        } else {
            temp[k++] = arr[j++];
            inv_count += (m - i + 1);  // All remaining in left are inversions
        }
    }
    
    while (i <= m) temp[k++] = arr[i++];
    while (j <= r) temp[k++] = arr[j++];
    
    for (int i = l; i <= r; i++) arr[i] = temp[i];
    
    return inv_count;
}
```

---

## 10. Dynamic Programming

### Core Concepts

1. **Optimal Substructure:** Optimal solution contains optimal solutions to subproblems
2. **Overlapping Subproblems:** Same subproblems solved multiple times

**Two Approaches:**
- **Top-down (Memoization):** Recursion + cache
- **Bottom-up (Tabulation):** Iterative, fill table

### Fibonacci: The Classic Example

**Naive Recursion: O(2^n)**
```c
int fib(int n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);
}
```

**Memoization: O(n)**
```c
int memo[100] = {-1};

int fib_memo(int n) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    return memo[n] = fib_memo(n-1) + fib_memo(n-2);
}
```

**Tabulation: O(n)**
```c
int fib_tab(int n) {
    int dp[n + 1];
    dp[0] = 0;
    dp[1] = 1;
    
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i-1] + dp[i-2];
    }
    
    return dp[n];
}
```

**Space Optimized: O(1)**
```c
int fib_opt(int n) {
    if (n <= 1) return n;
    
    int prev2 = 0, prev1 = 1;
    for (int i = 2; i <= n; i++) {
        int curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

### 0/1 Knapsack

**Problem:** Given items with weights and values, maximize value within weight capacity.

**Recurrence:**
```
dp[i][w] = max(
    dp[i-1][w],                          // Don't take item i
    dp[i-1][w - weight[i]] + value[i]    // Take item i
)
```

**Implementation:**
```c
int knapsack(int W, int wt[], int val[], int n) {
    int dp[n + 1][W + 1];
    
    for (int i = 0; i <= n; i++) {
        for (int w = 0; w <= W; w++) {
            if (i == 0 || w == 0) {
                dp[i][w] = 0;
            } else if (wt[i-1] <= w) {
                dp[i][w] = max(
                    val[i-1] + dp[i-1][w - wt[i-1]],
                    dp[i-1][w]
                );
            } else {
                dp[i][w] = dp[i-1][w];
            }
        }
    }
    
    return dp[n][W];
}
```

**Time:** O(nW)
**Space:** O(nW) or O(W) with optimization

### Longest Common Subsequence (LCS)

**Recurrence:**
```
if (s1[i-1] == s2[j-1])
    dp[i][j] = dp[i-1][j-1] + 1
else
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

```c
int lcs(char* s1, char* s2) {
    int m = strlen(s1), n = strlen(s2);
    int dp[m + 1][n + 1];
    
    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= n; j++) {
            if (i == 0 || j == 0) {
                dp[i][j] = 0;
            } else if (s1[i-1] == s2[j-1]) {
                dp[i][j] = dp[i-1][j-1] + 1;
            } else {
                dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
            }
        }
    }
    
    return dp[m][n];
}
```

**Time:** O(mn)

### Longest Increasing Subsequence (LIS)

**O(n²) DP:**
```c
int lis_n2(int arr[], int n) {
    int dp[n];
    for (int i = 0; i < n; i++) dp[i] = 1;
    
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (arr[j] < arr[i]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
    }
    
    int max_len = 0;
    for (int i = 0; i < n; i++) {
        max_len = max(max_len, dp[i]);
    }
    return max_len;
}
```

**O(n log n) with Binary Search:**
```c
int lis_nlogn(int arr[], int n) {
    int tail[n];  // tail[i] = smallest tail element for LIS of length i+1
    int len = 0;
    
    for (int i = 0; i < n; i++) {
        // Binary search for position
        int pos = lower_bound(tail, len, arr[i]);
        tail[pos] = arr[i];
        if (pos == len) len++;
    }
    
    return len;
}
```

### Edit Distance (Levenshtein Distance)

**Operations:** Insert, Delete, Replace

**Recurrence:**
```
if (s1[i-1] == s2[j-1])
    dp[i][j] = dp[i-1][j-1]
else
    dp[i][j] = 1 + min(dp[i-1][j-1],  // Replace
                       dp[i-1][j],     // Delete
                       dp[i][j-1])     // Insert
```

```c
int edit_distance(char* s1, char* s2) {
    int m = strlen(s1), n = strlen(s2);
    int dp[m + 1][n + 1];
    
    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;
    
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1[i-1] == s2[j-1]) {
                dp[i][j] = dp[i-1][j-1];
            } else {
                dp[i][j] = 1 + min3(
                    dp[i-1][j-1],  // Replace
                    dp[i-1][j],    // Delete
                    dp[i][j-1]     // Insert
                );
            }
        }
    }
    
    return dp[m][n];
}
```

### Coin Change

**Minimum coins to make amount:**
```c
int coin_change(int coins[], int n, int amount) {
    int dp[amount + 1];
    dp[0] = 0;
    
    for (int i = 1; i <= amount; i++) {
        dp[i] = INT_MAX;
        for (int j = 0; j < n; j++) {
            if (coins[j] <= i && dp[i - coins[j]] != INT_MAX) {
                dp[i] = min(dp[i], dp[i - coins[j]] + 1);
            }
        }
    }
    
    return dp[amount] == INT_MAX ? -1 : dp[amount];
}
```

**Number of ways to make amount:**
```c
int coin_ways(int coins[], int n, int amount) {
    int dp[amount + 1];
    memset(dp, 0, sizeof(dp));
    dp[0] = 1;
    
    for (int i = 0; i < n; i++) {
        for (int j = coins[i]; j <= amount; j++) {
            dp[j] += dp[j - coins[i]];
        }
    }
    
    return dp[amount];
}
```

### Matrix Chain Multiplication

**Problem:** Find optimal parenthesization to minimize scalar multiplications.

```c
int matrix_chain(int dims[], int n) {
    // dims[i-1] x dims[i] is dimension of matrix i
    // n matrices: dims has n+1 elements
    
    int dp[n][n];
    memset(dp, 0, sizeof(dp));
    
    // l = chain length
    for (int l = 2; l < n; l++) {
        for (int i = 1; i < n - l + 1; i++) {
            int j = i + l - 1;
            dp[i][j] = INT_MAX;
            
            for (int k = i; k < j; k++) {
                int cost = dp[i][k] + dp[k+1][j] + dims[i-1] * dims[k] * dims[j];
                dp[i][j] = min(dp[i][j], cost);
            }
        }
    }
    
    return dp[1][n-1];
}
```

**Time:** O(n³)

---

## 11. Greedy Algorithms

### Greedy Choice Property
Make locally optimal choice at each step, hoping for global optimum.

**Key:** Must prove greedy works for specific problem.

### Activity Selection

```c
typedef struct {
    int start, finish;
} Activity;

int cmp(const void* a, const void* b) {
    return ((Activity*)a)->finish - ((Activity*)b)->finish;
}

int activity_selection(Activity acts[], int n) {
    qsort(acts, n, sizeof(Activity), cmp);
    
    int count = 1;
    int last_finish = acts[0].finish;
    
    for (int i = 1; i < n; i++) {
        if (acts[i].start >= last_finish) {
            count++;
            last_finish = acts[i].finish;
        }
    }
    
    return count;
}
```

### Huffman Coding

Build optimal prefix-free binary code for data compression.

```c
typedef struct Node {
    char ch;
    int freq;
    struct Node *left, *right;
} Node;

Node* build_huffman(char chars[], int freq[], int n) {
    // Use min-heap (priority queue)
    MinHeap heap;
    
    for (int i = 0; i < n; i++) {
        Node* node = create_node(chars[i], freq[i]);
        insert_heap(&heap, node);
    }
    
    while (heap.size > 1) {
        Node* left = extract_min(&heap);
        Node* right = extract_min(&heap);
        
        Node* merged = create_node('\0', left->freq + right->freq);
        merged->left = left;
        merged->right = right;
        
        insert_heap(&heap, merged);
    }
    
    return extract_min(&heap);  // Root of Huffman tree
}
```

### Fractional Knapsack

```c
double fractional_knapsack(int W, int wt[], int val[], int n) {
    // Sort by value/weight ratio (descending)
    double ratio[n];
    int idx[n];
    for (int i = 0; i < n; i++) {
        ratio[i] = (double)val[i] / wt[i];
        idx[i] = i;
    }
    // Sort idx by ratio descending
    
    double total_value = 0;
    int remaining = W;
    
    for (int i = 0; i < n && remaining > 0; i++) {
        int j = idx[i];
        if (wt[j] <= remaining) {
            total_value += val[j];
            remaining -= wt[j];
        } else {
            total_value += ratio[j] * remaining;
            remaining = 0;
        }
    }
    
    return total_value;
}
```

### Job Scheduling with Deadlines

Maximize profit by scheduling jobs before their deadlines.

```c
typedef struct {
    int id, deadline, profit;
} Job;

int compare(const void* a, const void* b) {
    return ((Job*)b)->profit - ((Job*)a)->profit;
}

int job_scheduling(Job jobs[], int n) {
    qsort(jobs, n, sizeof(Job), compare);
    
    int max_deadline = 0;
    for (int i = 0; i < n; i++) {
        max_deadline = max(max_deadline, jobs[i].deadline);
    }
    
    int slots[max_deadline + 1];
    memset(slots, -1, sizeof(slots));
    
    int total_profit = 0;
    
    for (int i = 0; i < n; i++) {
        // Find latest available slot before deadline
        for (int j = jobs[i].deadline; j > 0; j--) {
            if (slots[j] == -1) {
                slots[j] = jobs[i].id;
                total_profit += jobs[i].profit;
                break;
            }
        }
    }
    
    return total_profit;
}
```

---

## 12. Backtracking

### General Pattern
```c
void backtrack(state) {
    if (is_solution(state)) {
        process_solution(state);
        return;
    }
    
    for (each candidate c) {
        if (is_valid(c, state)) {
            make_choice(c, state);
            backtrack(state);
            undo_choice(c, state);  // Backtrack
        }
    }
}
```

### N-Queens Problem

```c
bool is_safe(int board[], int row, int col) {
    for (int i = 0; i < row; i++) {
        if (board[i] == col ||               // Same column
            abs(board[i] - col) == row - i)  // Same diagonal
            return false;
    }
    return true;
}

void solve_n_queens(int board[], int row, int n) {
    if (row == n) {
        print_solution(board, n);
        return;
    }
    
    for (int col = 0; col < n; col++) {
        if (is_safe(board, row, col)) {
            board[row] = col;
            solve_n_queens(board, row + 1, n);
            // Backtracking happens implicitly
        }
    }
}
```

### Sudoku Solver

```c
bool find_empty(int grid[9][9], int* row, int* col) {
    for (*row = 0; *row < 9; (*row)++) {
        for (*col = 0; *col < 9; (*col)++) {
            if (grid[*row][*col] == 0) return true;
        }
    }
    return false;
}

bool is_valid(int grid[9][9], int row, int col, int num) {
    // Check row
    for (int x = 0; x < 9; x++)
        if (grid[row][x] == num) return false;
    
    // Check column
    for (int x = 0; x < 9; x++)
        if (grid[x][col] == num) return false;
    
    // Check 3x3 box
    int startRow = row - row % 3, startCol = col - col % 3;
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            if (grid[i + startRow][j + startCol] == num) return false;
    
    return true;
}

bool solve_sudoku(int grid[9][9]) {
    int row, col;
    
    if (!find_empty(grid, &row, &col))
        return true;  // Solved
    
    for (int num = 1; num <= 9; num++) {
        if (is_valid(grid, row, col, num)) {
            grid[row][col] = num;
            if (solve_sudoku(grid)) return true;
            grid[row][col] = 0;  // Backtrack
        }
    }
    
    return false;
}
```

### Subsets and Permutations

**Generate All Subsets:**
```c
void subsets(int arr[], int n, int subset[], int k, int start) {
    print_array(subset, k);
    
    for (int i = start; i < n; i++) {
        subset[k] = arr[i];
        subsets(arr, n, subset, k + 1, i + 1);
    }
}
```

**Generate All Permutations:**
```c
void permutations(int arr[], int n, int start) {
    if (start == n) {
        print_array(arr, n);
        return;
    }
    
    for (int i = start; i < n; i++) {
        swap(&arr[start], &arr[i]);
        permutations(arr, n, start + 1);
        swap(&arr[start], &arr[i]);  // Backtrack
    }
}
```

---

# Part III: Advanced Data Structures

---

## 13. Disjoint Set Union (Union-Find)

### Basic Structure
```c
int parent[MAX_N];
int rank[MAX_N];

void init(int n) {
    for (int i = 0; i < n; i++) {
        parent[i] = i;
        rank[i] = 0;
    }
}
```

### Find with Path Compression
```c
int find(int x) {
    if (parent[x] != x) {
        parent[x] = find(parent[x]);  // Path compression
    }
    return parent[x];
}
```

### Union by Rank
```c
void unite(int x, int y) {
    int px = find(x);
    int py = find(y);
    
    if (px == py) return;
    
    if (rank[px] < rank[py]) {
        parent[px] = py;
    } else if (rank[px] > rank[py]) {
        parent[py] = px;
    } else {
        parent[py] = px;
        rank[px]++;
    }
}
```

### Complexity
With path compression + union by rank:
- Nearly O(1) per operation
- Technically O(α(n)) where α is inverse Ackermann function

### Applications
1. Kruskal's MST
2. Connected components
3. Cycle detection in undirected graph
4. Equivalence classes

---

## 14. Segment Trees

### Structure
Binary tree for range queries and point updates.

```c
int tree[4 * MAX_N];  // 4n is safe size
int arr[MAX_N];

void build(int node, int start, int end) {
    if (start == end) {
        tree[node] = arr[start];
    } else {
        int mid = (start + end) / 2;
        build(2 * node, start, mid);
        build(2 * node + 1, mid + 1, end);
        tree[node] = tree[2 * node] + tree[2 * node + 1];  // Sum
    }
}
```

### Point Update: O(log n)
```c
void update(int node, int start, int end, int idx, int val) {
    if (start == end) {
        arr[idx] = val;
        tree[node] = val;
    } else {
        int mid = (start + end) / 2;
        if (idx <= mid) {
            update(2 * node, start, mid, idx, val);
        } else {
            update(2 * node + 1, mid + 1, end, idx, val);
        }
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }
}
```

### Range Query: O(log n)
```c
int query(int node, int start, int end, int l, int r) {
    if (r < start || end < l) {
        return 0;  // Out of range
    }
    if (l <= start && end <= r) {
        return tree[node];  // Fully in range
    }
    
    int mid = (start + end) / 2;
    int left_sum = query(2 * node, start, mid, l, r);
    int right_sum = query(2 * node + 1, mid + 1, end, l, r);
    return left_sum + right_sum;
}
```

### Lazy Propagation (Range Updates)
```c
int lazy[4 * MAX_N];

void push_down(int node, int start, int end) {
    if (lazy[node] != 0) {
        tree[node] += (end - start + 1) * lazy[node];
        if (start != end) {
            lazy[2 * node] += lazy[node];
            lazy[2 * node + 1] += lazy[node];
        }
        lazy[node] = 0;
    }
}

void range_update(int node, int start, int end, int l, int r, int val) {
    push_down(node, start, end);
    
    if (r < start || end < l) return;
    
    if (l <= start && end <= r) {
        lazy[node] += val;
        push_down(node, start, end);
        return;
    }
    
    int mid = (start + end) / 2;
    range_update(2 * node, start, mid, l, r, val);
    range_update(2 * node + 1, mid + 1, end, l, r, val);
    tree[node] = tree[2 * node] + tree[2 * node + 1];
}
```

---

## 15. Tries (Prefix Trees)

### Structure
```c
#define ALPHABET_SIZE 26

typedef struct TrieNode {
    struct TrieNode* children[ALPHABET_SIZE];
    bool is_end;
} TrieNode;

TrieNode* create_node() {
    TrieNode* node = malloc(sizeof(TrieNode));
    node->is_end = false;
    for (int i = 0; i < ALPHABET_SIZE; i++) {
        node->children[i] = NULL;
    }
    return node;
}
```

### Insert: O(m) where m = word length
```c
void insert(TrieNode* root, char* word) {
    TrieNode* curr = root;
    
    for (int i = 0; word[i]; i++) {
        int idx = word[i] - 'a';
        if (curr->children[idx] == NULL) {
            curr->children[idx] = create_node();
        }
        curr = curr->children[idx];
    }
    
    curr->is_end = true;
}
```

### Search: O(m)
```c
bool search(TrieNode* root, char* word) {
    TrieNode* curr = root;
    
    for (int i = 0; word[i]; i++) {
        int idx = word[i] - 'a';
        if (curr->children[idx] == NULL) {
            return false;
        }
        curr = curr->children[idx];
    }
    
    return curr->is_end;
}
```

### Prefix Search
```c
bool starts_with(TrieNode* root, char* prefix) {
    TrieNode* curr = root;
    
    for (int i = 0; prefix[i]; i++) {
        int idx = prefix[i] - 'a';
        if (curr->children[idx] == NULL) {
            return false;
        }
        curr = curr->children[idx];
    }
    
    return true;  // Don't need is_end check
}
```

### Applications
1. Autocomplete
2. Spell checker
3. IP routing (longest prefix match)
4. Word games (Boggle, Scrabble)

---

## 16. String Algorithms

### KMP (Knuth-Morris-Pratt): O(n + m)

**Failure Function:**
```c
void compute_lps(char* pattern, int m, int lps[]) {
    int len = 0;
    lps[0] = 0;
    int i = 1;
    
    while (i < m) {
        if (pattern[i] == pattern[len]) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0) {
                len = lps[len - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }
}
```

**Search:**
```c
void kmp_search(char* text, char* pattern) {
    int n = strlen(text);
    int m = strlen(pattern);
    int lps[m];
    
    compute_lps(pattern, m, lps);
    
    int i = 0, j = 0;
    while (i < n) {
        if (pattern[j] == text[i]) {
            i++;
            j++;
        }
        
        if (j == m) {
            printf("Found at index %d\n", i - j);
            j = lps[j - 1];
        } else if (i < n && pattern[j] != text[i]) {
            if (j != 0) {
                j = lps[j - 1];
            } else {
                i++;
            }
        }
    }
}
```

### Rabin-Karp (Rolling Hash): O(n + m) average

```c
#define d 256  // Number of characters
#define q 101  // A prime number

void rabin_karp(char* text, char* pattern) {
    int n = strlen(text);
    int m = strlen(pattern);
    int h = 1;  // d^(m-1) % q
    int p = 0;  // Hash of pattern
    int t = 0;  // Hash of current text window
    
    for (int i = 0; i < m - 1; i++)
        h = (h * d) % q;
    
    // Initial hash values
    for (int i = 0; i < m; i++) {
        p = (d * p + pattern[i]) % q;
        t = (d * t + text[i]) % q;
    }
    
    for (int i = 0; i <= n - m; i++) {
        if (p == t) {
            // Hash match, verify character by character
            bool match = true;
            for (int j = 0; j < m; j++) {
                if (text[i + j] != pattern[j]) {
                    match = false;
                    break;
                }
            }
            if (match) printf("Found at index %d\n", i);
        }
        
        // Compute next hash
        if (i < n - m) {
            t = (d * (t - text[i] * h) + text[i + m]) % q;
            if (t < 0) t += q;
        }
    }
}
```

---

# Part IV: Complexity Theory

---

## 17. Computational Complexity

### Time Complexity Classes

**P (Polynomial Time):**
Problems solvable in O(n^k) for some constant k.
Examples: Sorting, shortest path, MST

**NP (Nondeterministic Polynomial):**
Problems verifiable in polynomial time.
Examples: SAT, Hamiltonian path, subset sum

**NP-Complete:**
Hardest problems in NP. If any has polynomial solution, P = NP.
Examples: 3-SAT, Vertex Cover, TSP (decision version)

**NP-Hard:**
At least as hard as NP-complete. May not be in NP.
Examples: Halting problem, optimization TSP

### Key NP-Complete Problems

**Boolean Satisfiability (SAT):**
Given Boolean formula, is there assignment making it true?

**3-SAT:**
SAT where each clause has exactly 3 literals.

**Vertex Cover:**
Given graph G and integer k, is there set of ≤k vertices covering all edges?

**Traveling Salesman (Decision):**
Given weighted graph and bound B, is there tour visiting all vertices exactly once with total weight ≤ B?

### Reductions

To show problem X is NP-hard:
1. Take known NP-complete problem Y
2. Show Y reduces to X in polynomial time
3. If we could solve X efficiently, we could solve Y efficiently

### Approximation Algorithms

For NP-hard optimization problems, find solution within factor of optimal.

**Example: 2-Approximation for Vertex Cover**
```c
Set vertex_cover_approx(Graph G) {
    Set C = empty;
    while (G has edges) {
        Pick arbitrary edge (u, v);
        Add u and v to C;
        Remove all edges incident to u or v;
    }
    return C;
}
```

This returns cover at most 2× optimal size.

---

## Summary Tables

### Data Structure Complexities

| Structure | Access | Search | Insert | Delete |
|-----------|--------|--------|--------|--------|
| Array | O(1) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1)* | O(1)* |
| Stack | O(n) | O(n) | O(1) | O(1) |
| Queue | O(n) | O(n) | O(1) | O(1) |
| Hash Table | N/A | O(1) avg | O(1) avg | O(1) avg |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) |
| Heap | N/A | O(n) | O(log n) | O(log n) |
| Trie | N/A | O(m) | O(m) | O(m) |

*With pointer to position

### Sorting Algorithm Complexities

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |
| Radix Sort | O(d(n+k)) | O(d(n+k)) | O(d(n+k)) | O(n+k) | Yes |

### Graph Algorithm Complexities

| Algorithm | Time | Space |
|-----------|------|-------|
| BFS | O(V+E) | O(V) |
| DFS | O(V+E) | O(V) |
| Dijkstra (heap) | O((V+E) log V) | O(V) |
| Bellman-Ford | O(VE) | O(V) |
| Floyd-Warshall | O(V³) | O(V²) |
| Prim (heap) | O((V+E) log V) | O(V) |
| Kruskal | O(E log E) | O(V) |
| Topological Sort | O(V+E) | O(V) |

---

## Cross-References

- [[02_Computer_Architecture]] - Memory hierarchy affects algorithm performance
- [[05_Database_Systems]] - B-trees, indexing, query optimization
- [[07_Operating_Systems]] - Scheduling algorithms, memory management
- [[08_C_Programming]] - Implementation details
- [[09_Cpp_Programming]] - STL containers and algorithms
