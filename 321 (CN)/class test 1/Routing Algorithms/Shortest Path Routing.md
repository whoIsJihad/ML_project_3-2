

[[Shortest Path Routing]] is the most common form of [[Routing Algorithm]]. The goal is to find a path between a source and destination that minimizes a specific cost metric.

## 1. Graph Representation

The network is modeled as a graph $G = (V, E)$.

- **Nodes (**$V$**)**: Represent routers.
    
- **Edges (**$E$**)**: Represent communication links.
    
- **Weight (**$w$**)**: A value assigned to each link.
    

## 2. Metric Selection

The "shortest" path depends on the definition of the link weight $w$:

- **Hop Count**: $w=1$ for all links. The shortest path has the fewest routers.
    
- **Distance**: $w=$ physical length in kilometers.
    
- **Bandwidth**: $w \propto 1/\text{capacity}$.
    
- **Delay**: $w=$ measured queuing and transmission time.
    

## 3. Dijkstra's Algorithm

The standard algorithm for computing the shortest path from a single source to all other nodes.

### Algorithm Steps:

1. **Initialization**:
    
    - Set distance to source = 0.
        
    - Set distance to all other nodes = $\infty$.
        
    - Mark all nodes as unvisited.
        
2. **Selection**: Choose the unvisited node $u$ with the smallest distance.
    
3. **Relaxation**: For each neighbor $v$ of $u$:
    
    - Calculate $new\_dist = dist(u) + weight(u, v)$.
        
    - If $new\_dist < dist(v)$, update $dist(v) = new\_dist$.
        
4. **Finalization**: Mark $u$ as visited. Repeat until all nodes are visited.
    

Related: [[Routing Algorithms]], [[Dijkstra Algorithm]]