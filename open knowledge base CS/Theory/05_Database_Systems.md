# Database Systems

## Quick Reference
**Reading Time:** ~2 hours  
**Prerequisites:** [[04_Algorithms_Complexity]], data structures  
**Cross-links:** [[Session_04_Databases_Concurrency]]

---

## 1. Database Fundamentals

### Database vs File System
**Database:**
- Data independence (schema separate from storage)
- Concurrent access control
- ACID transactions
- Query optimization
- Crash recovery

**File System:**
- Direct file manipulation
- Application handles consistency
- No built-in concurrency control

### Database Management System (DBMS)
**Components:**
- **Query Processor:** Parse, optimize, execute
- **Storage Manager:** Buffer, file, disk management
- **Transaction Manager:** Concurrency, recovery
- **Catalog/Metadata:** Schema, statistics

---

## 2. Data Models

### Relational Model
- **Tables (Relations):** Rows (tuples), columns (attributes)
- **Schema:** Structure definition
- **Primary Key:** Unique identifier for tuple
- **Foreign Key:** References primary key in another table

**Example:**
```
Students(sid, name, major)
Courses(cid, title, credits)
Enrollments(sid, cid, grade)  -- FKs: sid, cid
```

**Properties:**
- **Atomicity:** Attribute values are indivisible
- **No duplicate rows:** Set semantics
- **Unordered tuples:** No inherent order

### Entity-Relationship (ER) Model
**Entities:** Objects (e.g., Student, Course)  
**Relationships:** Associations (e.g., Enrolls)  
**Attributes:** Properties (e.g., name, age)

**Cardinality:**
- **One-to-One (1:1):** Each entity in A relates to ≤1 in B
- **One-to-Many (1:N):** Each in A relates to many in B
- **Many-to-Many (M:N):** Both can relate to many

**ER → Relational:**
- Entity → Table
- Relationship → Table (with FKs) or FK in participating table
- M:N → Separate junction table

### NoSQL Models

**Key-Value:**
- Simple: key → value
- Examples: Redis, DynamoDB
- Use: Caching, session storage

**Document:**
- Semi-structured (JSON/BSON)
- Examples: MongoDB, CouchDB
- Use: Flexible schema, nested data

**Column-Family:**
- Column-oriented storage
- Examples: Cassandra, HBase
- Use: Wide tables, time-series

**Graph:**
- Nodes, edges, properties
- Examples: Neo4j, Amazon Neptune
- Use: Social networks, recommendations

---

## 3. SQL (Structured Query Language)

### DDL (Data Definition Language)
**Create Table:**
```sql
CREATE TABLE Students (
    sid INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    major VARCHAR(50),
    gpa FLOAT CHECK (gpa >= 0.0 AND gpa <= 4.0)
);
```

**Alter Table:**
```sql
ALTER TABLE Students ADD COLUMN email VARCHAR(100);
ALTER TABLE Students DROP COLUMN major;
```

**Drop Table:**
```sql
DROP TABLE Students;
```

### DML (Data Manipulation Language)

**Insert:**
```sql
INSERT INTO Students VALUES (1, 'Alice', 'CS', 3.8);
INSERT INTO Students (sid, name) VALUES (2, 'Bob');
```

**Select:**
```sql
SELECT name, gpa FROM Students WHERE major = 'CS';
SELECT * FROM Students;
```

**Update:**
```sql
UPDATE Students SET gpa = 3.9 WHERE sid = 1;
```

**Delete:**
```sql
DELETE FROM Students WHERE gpa < 2.0;
```

### Queries

**Filtering:**
```sql
SELECT * FROM Students WHERE gpa > 3.5 AND major = 'CS';
```

**Sorting:**
```sql
SELECT * FROM Students ORDER BY gpa DESC;
```

**Aggregation:**
```sql
SELECT major, COUNT(*), AVG(gpa) 
FROM Students 
GROUP BY major 
HAVING AVG(gpa) > 3.0;
```

**Joins:**

**Inner Join:**
```sql
SELECT s.name, e.grade
FROM Students s JOIN Enrollments e ON s.sid = e.sid;
```

**Left Outer Join:**
```sql
SELECT s.name, e.grade
FROM Students s LEFT JOIN Enrollments e ON s.sid = e.sid;
-- Includes students with no enrollments (NULL grades)
```

**Right/Full Outer Joins:** Similar (right includes all from right table)

**Subqueries:**
```sql
SELECT name FROM Students 
WHERE sid IN (SELECT sid FROM Enrollments WHERE grade = 'A');
```

**Exists:**
```sql
SELECT name FROM Students s
WHERE EXISTS (SELECT * FROM Enrollments e WHERE e.sid = s.sid);
```

### Set Operations
- **UNION:** Combine results, remove duplicates
- **INTERSECT:** Common rows
- **EXCEPT:** Rows in first but not second

---

## 4. Normalization

### Purpose
- Eliminate redundancy
- Avoid update anomalies
- Ensure data integrity

### Functional Dependencies
**X → Y:** Y is functionally dependent on X if X determines Y

**Example:**
- sid → name, major (student ID determines name and major)
- cid → title, credits (course ID determines title and credits)

### Normal Forms

**1NF (First Normal Form):**
- Atomic values (no multi-valued attributes)
- Each row unique

**2NF:**
- 1NF + No partial dependencies (non-key attributes fully depend on entire key, not just part)

**3NF (Third Normal Form):**
- 2NF + No transitive dependencies (non-key attributes depend only on key, not on other non-key attributes)

**BCNF (Boyce-Codd Normal Form):**
- 3NF + For every FD X → Y, X is a superkey
- Stricter than 3NF

**Example:**
**Unnormalized:**
```
Orders(order_id, customer_name, customer_addr, items)
```
**Anomalies:** Update customer address in multiple orders

**Normalized (3NF):**
```
Customers(cust_id, name, address)
Orders(order_id, cust_id, order_date)
OrderItems(order_id, item_id, quantity, price)
```

### Denormalization
- Intentionally introduce redundancy for performance
- Trade: Update complexity for read speed
- Use: Analytics, read-heavy workloads

---

## 5. Indexing

### Purpose
- Speed up queries
- Trade: Space and write overhead

### Types

**Primary Index:**
- On primary key
- Clustered: Data sorted by index key (only one per table)

**Secondary Index:**
- On non-primary key
- Multiple allowed
- Points to primary key or row

**Composite Index:**
- On multiple columns
- Example: INDEX(last_name, first_name)
- Order matters for prefix queries

### B-Tree Index
**Structure:**
- Balanced tree
- All leaves at same level
- Internal nodes: Keys + pointers
- Leaf nodes: Keys + data/pointers

**Properties:**
- Height: $O(\log n)$
- Search, insert, delete: $O(\log n)$
- Range queries efficient (leaves linked)

**B+ Tree:**
- Keys only in internal nodes
- All data in leaves
- Leaves linked (range scans)
- Most common in DBMS

**Parameters:**
- Order $d$: Min $d$ children (except root)
- Internal node: $d$ to $2d$ children
- Root: 2 to $2d$ children

### Hash Index
**Structure:**
- Hash function: key → bucket
- Fast equality lookup: $O(1)$ average

**Limitations:**
- No range queries
- No sorted order
- Resizing expensive

### Bitmap Index
- Bit vector per distinct value
- Efficient for low-cardinality columns (e.g., gender, status)
- Example: Male/Female → two bitmaps

### Full-Text Index
- For text search (LIKE '%keyword%')
- Inverted index: word → documents
- Examples: Elasticsearch, PostgreSQL GIN

---

## 6. Query Processing & Optimization

### Query Execution Pipeline
1. **Parser:** Syntax check, parse tree
2. **Optimizer:** Generate execution plans, choose best
3. **Executor:** Execute chosen plan

### Relational Algebra
**Operators:**
- **Select (σ):** Filter rows
- **Project (π):** Choose columns
- **Join (⋈):** Combine tables
- **Union (∪), Intersection (∩), Difference (−)**
- **Rename (ρ)**

**Example:**
$\pi_{name, gpa}(\sigma_{major='CS'}(Students))$

### Join Algorithms

**Nested Loop Join:**
```
for each row r in R:
    for each row s in S:
        if r.key == s.key: output (r, s)
```
- Cost: $|R| + |R| \times |S| = O(nm)$ I/Os
- Use: Small tables or when no index

**Index Nested Loop:**
- Use index on inner table
- Cost: $|R| + |R| \times \text{index lookup cost}$

**Sort-Merge Join:**
1. Sort both tables on join key
2. Merge sorted streams
- Cost: $O(n \log n + m \log m)$ for sort, $O(n + m)$ for merge
- Use: Already sorted or sort needed anyway

**Hash Join:**
1. **Build:** Hash smaller table into buckets
2. **Probe:** Hash larger table, check matching buckets
- Cost: $O(n + m)$ (two passes)
- Use: Equality joins, sufficient memory

### Query Optimization

**Cost-Based Optimization:**
- Estimate cost of each plan
- Use statistics (table size, cardinality, selectivity)
- Choose minimum cost

**Statistics:**
- **Cardinality:** Number of rows
- **Selectivity:** Fraction of rows satisfying predicate
- **Histogram:** Value distribution

**Heuristics:**
- Push selections down (reduce early)
- Push projections down (eliminate columns)
- Reorder joins (smallest intermediate results)

**Example:**
$$\sigma_{age>30}(Students \bowtie_{sid} Enrollments)$$
Better:
$$\sigma_{age>30}(Students) \bowtie_{sid} Enrollments$$
(Filter Students first)

---

## 7. Transactions & ACID

### Transaction Concept
- Logical unit of work
- All or nothing (atomicity)
- **Example:** Bank transfer (debit A, credit B)

### ACID Properties

**Atomicity:**
- All operations succeed or all fail
- No partial transactions
- **Mechanism:** Logging, rollback

**Consistency:**
- Database moves from one valid state to another
- Integrity constraints maintained
- **Mechanism:** Constraint checking

**Isolation:**
- Concurrent transactions don't interfere
- Appear to execute serially
- **Mechanism:** Concurrency control (locks, MVCC)

**Durability:**
- Committed changes persist despite crashes
- **Mechanism:** Write-ahead logging (WAL)

---

## 8. Concurrency Control

### Anomalies Without Concurrency Control

**Lost Update:**
- T1 and T2 read X, both update, one overwrites the other

**Dirty Read:**
- T1 reads uncommitted change from T2
- If T2 aborts, T1 has invalid data

**Non-Repeatable Read:**
- T1 reads X twice
- T2 updates X between reads
- T1 sees different values

**Phantom Read:**
- T1 queries range
- T2 inserts row in range
- T1 re-queries, sees new row

### Isolation Levels

| Level | Dirty Read | Non-Repeatable | Phantom |
|-------|------------|----------------|---------|
| **Read Uncommitted** | Possible | Possible | Possible |
| **Read Committed** | Not Possible | Possible | Possible |
| **Repeatable Read** | Not Possible | Not Possible | Possible |
| **Serializable** | Not Possible | Not Possible | Not Possible |

**Default:** Often Read Committed

### Lock-Based Concurrency Control

**Two-Phase Locking (2PL):**
1. **Growing Phase:** Acquire locks, no releases
2. **Shrinking Phase:** Release locks, no new acquisitions

**Guarantees:** Serializable schedules

**Lock Types:**
- **Shared (S):** Read lock, multiple allowed
- **Exclusive (X):** Write lock, exclusive
- **Compatibility:** S+S ok, S+X no, X+X no

**Lock Granularity:**
- **Row-level:** Fine-grained, high concurrency
- **Page-level:** Medium
- **Table-level:** Coarse, low concurrency

**Deadlock:**
- T1 waits for T2, T2 waits for T1
- **Detection:** Wait-for graph (cycle detection)
- **Prevention:** Timeout, ordering, deadlock avoidance
- **Resolution:** Abort one transaction

**Strict 2PL:**
- Hold all locks until commit/abort
- Avoids cascading aborts

### Optimistic Concurrency Control
1. **Read Phase:** Read without locks
2. **Validation Phase:** Check for conflicts
3. **Write Phase:** Commit if valid, else abort

**Use:** Low conflict workloads

### Multi-Version Concurrency Control (MVCC)
- Keep multiple versions of each row
- Readers don't block writers, writers don't block readers
- Each transaction sees snapshot at start time
- **Used in:** PostgreSQL, MySQL InnoDB, Oracle

**Snapshot Isolation:**
- Read from snapshot at transaction start
- Write to private workspace, commit if no conflicts
- Lower overhead than full serializability
- **Anomaly:** Write skew (two transactions read same, write different)

---

## 9. Crash Recovery

### Write-Ahead Logging (WAL)
**Principle:** Log changes before writing to disk

**Log Records:**
- **Update:** (txn_id, page_id, before_value, after_value)
- **Commit:** (txn_id)
- **Abort:** (txn_id)

**Guarantee:** If transaction committed, log on disk

### ARIES Algorithm
**Three Phases:**

1. **Analysis:** Identify dirty pages and active transactions at crash
2. **Redo:** Replay all actions (even aborted transactions) to restore state
3. **Undo:** Rollback uncommitted transactions

**Checkpointing:**
- Periodically write dirty pages to disk
- Record checkpoint in log
- Reduces recovery time (only redo from checkpoint)

---

## 10. Distributed Databases

### Architectures

**Replication:**
- **Master-Slave:** Master for writes, slaves for reads
- **Multi-Master:** Multiple writable replicas
- **Use:** Fault tolerance, read scalability

**Sharding (Partitioning):**
- Split data across nodes
- **Horizontal:** Rows distributed (e.g., users 1-1000 on node 1)
- **Vertical:** Columns distributed (less common)
- **Use:** Write scalability, large datasets

**Replication + Sharding:**
- Each shard replicated
- **Use:** Both read/write scalability and fault tolerance

### CAP Theorem
**Cannot have all three:**
- **Consistency:** All nodes see same data at same time
- **Availability:** Every request gets response (success or failure)
- **Partition Tolerance:** System continues despite network partition

**Implication:** Choose 2 of 3 in presence of partitions

**Examples:**
- **CP:** Traditional RDBMS (during partition, become unavailable)
- **AP:** Cassandra, DynamoDB (eventual consistency)
- **CA:** Single-node systems (no real partition tolerance)

### Distributed Transactions

**Two-Phase Commit (2PC):**
1. **Prepare Phase:** Coordinator asks all participants to prepare
2. **Commit Phase:** If all vote yes, coordinator commits; otherwise abort

**Blocking Problem:** If coordinator fails after prepare, participants blocked

**Paxos/Raft (Consensus):**
- Achieve agreement in presence of failures
- Used in distributed systems for coordination
- **Raft:** Leader election, log replication, safety

---

## 11. NoSQL Deep Dive

### MongoDB (Document Store)
**Features:**
- JSON-like documents (BSON)
- Flexible schema
- Secondary indexes, aggregation framework
- Replication (replica sets), sharding

**Query:**
```javascript
db.users.find({ age: { $gt: 30 }, status: "active" })
```

### Redis (Key-Value)
**Features:**
- In-memory data structure store
- Data types: strings, lists, sets, hashes, sorted sets
- Persistence options (RDB snapshots, AOF log)
- Pub/sub messaging

**Commands:**
```redis
SET user:1:name "Alice"
GET user:1:name
LPUSH mylist "item1"
```

### Cassandra (Column-Family)
**Features:**
- Distributed, highly available (AP)
- Tunable consistency
- CQL (SQL-like query language)
- Partition key + clustering columns

**Data Model:**
- Keyspace → Tables
- Partition key determines node placement
- Clustering columns determine sort order within partition

---

## 12. Advanced Topics

### Materialized Views
- Precomputed query results
- Updated on base table changes (or periodically)
- Trade: Storage and maintenance cost for query speed

### Triggers
- Code executed automatically on events (insert/update/delete)
- Use: Enforce business rules, audit trails

### Stored Procedures
- Precompiled SQL code stored in database
- Reduce network overhead
- Encapsulate logic

### OLTP vs OLAP

**OLTP (Online Transaction Processing):**
- Many short transactions (insert/update/delete)
- Real-time, operational data
- Normalized schema
- Row-oriented storage
- Example: E-commerce orders

**OLAP (Online Analytical Processing):**
- Complex queries, aggregations
- Historical data, analytics
- Denormalized (star/snowflake schema)
- Column-oriented storage
- Example: Business intelligence, reporting

### Data Warehouses
- Centralized repository for analytics
- ETL (Extract, Transform, Load) from multiple sources
- Star schema: Fact table + dimension tables
- Examples: Amazon Redshift, Google BigQuery, Snowflake

### NewSQL
- Combine SQL semantics with NoSQL scalability
- Distributed transactions, strong consistency
- Examples: Google Spanner, CockroachDB, VoltDB

---

## Key Concepts Summary

| Concept | Core Principle |
|---------|----------------|
| **Relational Model** | Tables, rows, columns, keys, joins |
| **Normalization** | Eliminate redundancy via functional dependencies |
| **Indexing** | Trade space/write cost for read speed (B+tree) |
| **ACID** | Atomicity, Consistency, Isolation, Durability |
| **2PL** | Two-phase locking ensures serializability |
| **MVCC** | Multiple versions avoid read-write conflicts |
| **WAL** | Log before write for crash recovery |
| **CAP Theorem** | Can't have consistency, availability, partition tolerance |

---

## Common Pitfalls

1. **Over-normalization** → Too many joins, slow queries
2. **No indexes on foreign keys** → Slow joins
3. **Wrong isolation level** → Anomalies or deadlocks
4. **N+1 query problem** → One query per row instead of batch
5. **Not using prepared statements** → SQL injection, no plan caching
6. **Full table scan when index exists** → Query optimizer issue
7. **Assuming 2PC is always correct** → Blocking on coordinator failure

---

## Cross-Links
- [[04_Algorithms_Complexity]] - B-trees, hashing, join algorithms
- [[Session_04_Databases_Concurrency]] - Concurrency practice
- [[Session_05_Networks_Distributed_Systems]] - Distributed databases
- [[02_Computer_Architecture]] - Disk I/O, caching

---

## Quick Formulas

**Nested Loop Join:** $O(|R| \times |S|)$ I/Os  
**Sort-Merge Join:** $O(|R| \log |R| + |S| \log |S|)$  
**Hash Join:** $O(|R| + |S|)$ (two passes)  
**B-Tree Height:** $O(\log_d n)$ where $d$ is order  
**Selectivity:** $\frac{\text{rows satisfying}}{\text{total rows}}$
