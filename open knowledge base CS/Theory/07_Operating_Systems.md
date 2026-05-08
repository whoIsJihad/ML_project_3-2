# Operating Systems

## Course Overview
**Depth:** University undergraduate + systems programming knowledge  
**Time:** 3-4 hours focused reading  
**Prerequisites:** C programming, basic computer architecture

---

# Part I: OS Fundamentals

---

## 1. Introduction to Operating Systems

### What is an OS?
The operating system is software that:
1. **Manages hardware resources** (CPU, memory, I/O)
2. **Provides abstractions** (processes, files, sockets)
3. **Enforces protection** (isolation between processes)

### OS Modes

**User Mode:**
- Limited instruction set
- No direct hardware access
- Used by application programs

**Kernel Mode (Supervisor Mode):**
- Full instruction set (privileged instructions)
- Direct hardware access
- Memory protection, I/O operations

**Mode Switching:**
1. System call (software interrupt)
2. Hardware interrupt
3. Exception/trap

### System Calls

```c
// User space → Kernel space
int fd = open("/file.txt", O_RDONLY);  // syscall

// What happens:
// 1. Library function sets up arguments
// 2. Software interrupt (INT 0x80 or SYSCALL instruction)
// 3. CPU switches to kernel mode
// 4. Kernel handles request
// 5. CPU returns to user mode
// 6. Result returned to program
```

**Common System Calls:**
| Category | Calls |
|----------|-------|
| Process | fork, exec, exit, wait, getpid |
| File | open, close, read, write, lseek |
| Directory | mkdir, rmdir, link, unlink |
| Memory | mmap, munmap, brk |
| IPC | pipe, socket, shmget |
| Signals | kill, signal, sigaction |

### OS Structures

**Monolithic Kernel:**
- All services in kernel space
- Fast (no mode switches for internal calls)
- Large, complex, harder to maintain
- Examples: Linux, BSD

**Microkernel:**
- Minimal kernel (IPC, scheduling, memory)
- Services run in user space
- More mode switches but more modular
- Examples: Minix, QNX, seL4

**Hybrid:**
- Mix of both approaches
- Examples: Windows NT, macOS XNU

---

# Part II: Processes and Threads

---

## 2. Processes

### Process Concept

A **process** is a program in execution, consisting of:
- Code (text section)
- Current activity (program counter, registers)
- Stack (temporary data)
- Data section (global variables)
- Heap (dynamically allocated memory)

### Process Memory Layout

```
High Address
+------------------+
|      Stack       | ← Grows downward
|        ↓         |
|       ...        |
|        ↑         |
|       Heap       | ← Grows upward
+------------------+
|       BSS        | ← Uninitialized globals (zero-filled)
+------------------+
|       Data       | ← Initialized globals
+------------------+
|       Text       | ← Code (read-only)
+------------------+
Low Address
```

### Process Control Block (PCB)

```c
struct task_struct {  // Linux
    pid_t pid;                    // Process ID
    long state;                   // Running, waiting, etc.
    struct thread_info *thread;   // CPU registers, stack pointer
    struct mm_struct *mm;         // Memory management
    struct fs_struct *fs;         // File system info
    struct files_struct *files;   // Open files
    struct signal_struct *signal; // Signal handlers
    // ... more
};
```

### Process States

```
        ┌────────────────────────────────────────┐
        │                                        │
        ↓                                        │
     ┌──────┐    admit     ┌───────┐   dispatch  ┌─────────┐
New →│Ready │─────────────→│Running│────────────→│Terminated│
     └──┬───┘              └───┬───┘             └──────────┘
        ↑                      │
        │    I/O or event      │
        │    complete          │ I/O or event wait
        │                      ↓
        │                  ┌───────┐
        └──────────────────│Waiting│
                           └───────┘
```

**States:**
- **New:** Process being created
- **Ready:** Waiting to be assigned to CPU
- **Running:** Instructions being executed
- **Waiting:** Waiting for event (I/O, signal)
- **Terminated:** Finished execution

### Process Creation (fork/exec)

```c
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();  // Create child process
    
    if (pid < 0) {
        // Error
        perror("fork failed");
        return 1;
    }
    
    if (pid == 0) {
        // Child process
        printf("Child PID: %d\n", getpid());
        
        // Replace process image
        char *args[] = {"ls", "-la", NULL};
        execvp("ls", args);
        
        // Only reached if exec fails
        perror("exec failed");
        return 1;
    }
    
    // Parent process
    printf("Parent PID: %d, Child PID: %d\n", getpid(), pid);
    
    int status;
    wait(&status);  // Wait for child to terminate
    
    if (WIFEXITED(status)) {
        printf("Child exited with status %d\n", WEXITSTATUS(status));
    }
    
    return 0;
}
```

**fork() Behavior:**
- Creates exact copy of parent process
- Returns:
  - 0 to child
  - Child's PID to parent
  - -1 on error
- Copy-on-write (COW) for efficiency

**exec() Family:**
```c
execl("/bin/ls", "ls", "-l", NULL);              // Path, args list
execv("/bin/ls", argv);                          // Path, args array
execlp("ls", "ls", "-l", NULL);                  // Search PATH
execvp("ls", argv);                              // Search PATH
execle("/bin/ls", "ls", NULL, envp);             // With environment
execve("/bin/ls", argv, envp);                   // Full control
```

### Process Termination

**Normal Exit:**
```c
exit(0);           // C library, runs atexit handlers
_exit(0);          // Direct syscall, no cleanup
return 0;          // From main()
```

**Abnormal Termination:**
- Kill signal: `kill(pid, SIGKILL)`
- Exception (segfault, etc.)

**Zombie Process:**
- Child has exited
- Parent hasn't called wait()
- Entry remains in process table

**Orphan Process:**
- Parent has exited before child
- Child adopted by init (PID 1)

### Inter-Process Communication (IPC)

**Pipes:**
```c
int pipefd[2];
pipe(pipefd);  // pipefd[0] = read, pipefd[1] = write

if (fork() == 0) {
    // Child: read from pipe
    close(pipefd[1]);
    char buf[100];
    read(pipefd[0], buf, sizeof(buf));
    close(pipefd[0]);
} else {
    // Parent: write to pipe
    close(pipefd[0]);
    write(pipefd[1], "Hello", 5);
    close(pipefd[1]);
}
```

**Named Pipes (FIFO):**
```c
mkfifo("/tmp/myfifo", 0666);
int fd = open("/tmp/myfifo", O_WRONLY);
write(fd, "data", 4);
close(fd);
```

**Message Queues:**
```c
key_t key = ftok("/tmp", 'A');
int msgid = msgget(key, IPC_CREAT | 0666);

struct {
    long mtype;
    char mtext[100];
} msg;

msg.mtype = 1;
strcpy(msg.mtext, "Hello");
msgsnd(msgid, &msg, sizeof(msg.mtext), 0);

msgrcv(msgid, &msg, sizeof(msg.mtext), 1, 0);
```

**Shared Memory:**
```c
key_t key = ftok("/tmp", 'B');
int shmid = shmget(key, 1024, IPC_CREAT | 0666);

char *data = shmat(shmid, NULL, 0);
strcpy(data, "Hello from shared memory");

// In another process
char *data = shmat(shmid, NULL, 0);
printf("%s\n", data);

shmdt(data);
shmctl(shmid, IPC_RMID, NULL);  // Delete
```

---

## 3. Threads

### Process vs Thread

| Aspect | Process | Thread |
|--------|---------|--------|
| Address space | Separate | Shared |
| Creation cost | High (fork) | Low |
| Context switch | Expensive | Cheaper |
| Communication | IPC needed | Shared memory |
| Failure isolation | Yes | No (one crash affects all) |

### Thread Memory Model

```
Process Address Space
+------------------+
|      Stack T1    |  ← Thread 1's stack
+------------------+
|      Stack T2    |  ← Thread 2's stack
+------------------+
|      Stack T3    |  ← Thread 3's stack
+------------------+
|       ...        |
+------------------+
|       Heap       |  ← SHARED
+------------------+
|       Data       |  ← SHARED
+------------------+
|       Text       |  ← SHARED
+------------------+
```

**Per-thread:**
- Stack
- Registers (including PC, SP)
- Thread-local storage

**Shared:**
- Code, data, heap
- Open files
- Signal handlers

### POSIX Threads (pthreads)

```c
#include <pthread.h>

void* thread_func(void* arg) {
    int* num = (int*)arg;
    printf("Thread received: %d\n", *num);
    
    int* result = malloc(sizeof(int));
    *result = (*num) * 2;
    return result;
}

int main() {
    pthread_t tid;
    int arg = 42;
    
    // Create thread
    if (pthread_create(&tid, NULL, thread_func, &arg) != 0) {
        perror("pthread_create");
        return 1;
    }
    
    // Wait for thread to finish
    void* retval;
    pthread_join(tid, &retval);
    
    printf("Thread returned: %d\n", *(int*)retval);
    free(retval);
    
    return 0;
}
```

**Compile:** `gcc -pthread program.c`

### Thread Creation Options

```c
pthread_attr_t attr;
pthread_attr_init(&attr);

// Set stack size
pthread_attr_setstacksize(&attr, 2 * 1024 * 1024);

// Set detached (can't join)
pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

pthread_create(&tid, &attr, func, arg);
pthread_attr_destroy(&attr);
```

### Thread Synchronization

**Mutex (Mutual Exclusion):**
```c
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void* critical_section(void* arg) {
    pthread_mutex_lock(&lock);
    
    // Only one thread at a time here
    shared_counter++;
    
    pthread_mutex_unlock(&lock);
    return NULL;
}
```

**Condition Variables:**
```c
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
int ready = 0;

// Producer
void* producer(void* arg) {
    pthread_mutex_lock(&lock);
    ready = 1;
    pthread_cond_signal(&cond);
    pthread_mutex_unlock(&lock);
    return NULL;
}

// Consumer
void* consumer(void* arg) {
    pthread_mutex_lock(&lock);
    while (!ready) {
        pthread_cond_wait(&cond, &lock);  // Releases lock, waits, reacquires
    }
    // Process data
    pthread_mutex_unlock(&lock);
    return NULL;
}
```

**Read-Write Locks:**
```c
pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

void* reader(void* arg) {
    pthread_rwlock_rdlock(&rwlock);
    // Multiple readers allowed
    pthread_rwlock_unlock(&rwlock);
    return NULL;
}

void* writer(void* arg) {
    pthread_rwlock_wrlock(&rwlock);
    // Only one writer, no readers
    pthread_rwlock_unlock(&rwlock);
    return NULL;
}
```

**Semaphores:**
```c
#include <semaphore.h>

sem_t sem;
sem_init(&sem, 0, 3);  // Initial value 3

sem_wait(&sem);  // Decrement (block if 0)
// Critical section
sem_post(&sem);  // Increment

sem_destroy(&sem);
```

### Thread-Local Storage

```c
// pthread TLS
pthread_key_t key;
pthread_key_create(&key, free);  // Destructor

void* thread_func(void* arg) {
    int* local = malloc(sizeof(int));
    *local = *(int*)arg;
    pthread_setspecific(key, local);
    
    // Later...
    int* value = pthread_getspecific(key);
    return NULL;
}

// C11 thread_local
thread_local int counter = 0;

// GCC __thread
__thread int counter = 0;
```

---

# Part III: CPU Scheduling

---

## 4. Scheduling Concepts

### Scheduling Criteria

- **CPU utilization:** Keep CPU busy
- **Throughput:** Processes completed per time unit
- **Turnaround time:** Total time from submission to completion
- **Waiting time:** Time spent in ready queue
- **Response time:** Time from request to first response

### Preemptive vs Non-preemptive

**Non-preemptive:**
- Process runs until completion or voluntary block
- Simple but poor response time

**Preemptive:**
- OS can interrupt running process
- Better response time but more overhead
- Requires synchronization

### Context Switch

**Steps:**
1. Save current process state (registers, PC, SP)
2. Update PCB and process state
3. Move PCB to appropriate queue
4. Select next process
5. Update memory management structures
6. Restore new process state

**Cost:** Typically 1-1000 microseconds

---

## 5. Scheduling Algorithms

### First-Come, First-Served (FCFS)

```
Process  Burst Time
P1       24
P2       3
P3       3

Order: P1, P2, P3
Gantt: |----P1----|--P2--|--P3--|
       0         24     27     30

Waiting: P1=0, P2=24, P3=27
Average waiting: (0+24+27)/3 = 17
```

**Convoy Effect:** Short processes wait behind long ones

### Shortest Job First (SJF)

```
Process  Burst Time
P1       6
P2       8
P3       7
P4       3

Order: P4, P1, P3, P2
Gantt: |--P4--|--P1--|--P3--|--P2--|
       0      3      9     16     24

Waiting: P4=0, P1=3, P3=9, P2=16
Average waiting: (0+3+9+16)/4 = 7
```

**Optimal** for minimizing average waiting time
**Problem:** Requires knowing burst time (prediction needed)

### Shortest Remaining Time First (SRTF)

Preemptive version of SJF.

```
Process  Arrival  Burst
P1       0        8
P2       1        4
P3       2        9
P4       3        5

Timeline:
0: P1 arrives, runs (remaining: 8)
1: P2 arrives, preempts P1 (P2: 4, P1: 7)
2: P3 arrives, P2 continues (shorter)
3: P4 arrives, P2 continues
5: P2 completes, P4 runs (5)
10: P4 completes, P1 runs (7)
17: P1 completes, P3 runs (9)
26: Done
```

### Priority Scheduling

```
Process  Burst  Priority (lower = higher)
P1       10     3
P2       1      1
P3       2      4
P4       1      5
P5       5      2

Order: P2, P5, P1, P3, P4
```

**Starvation:** Low priority processes may never run
**Solution:** Aging (increase priority over time)

### Round Robin (RR)

```
Time Quantum: 4

Process  Burst
P1       24
P2       3
P3       3

Timeline:
0-4:   P1 (remaining: 20)
4-7:   P2 (done)
7-10:  P3 (done)
10-14: P1 (remaining: 16)
14-18: P1 (remaining: 12)
18-22: P1 (remaining: 8)
22-26: P1 (remaining: 4)
26-30: P1 (done)
```

**Trade-off:**
- Small quantum: Good response, high overhead
- Large quantum: Approaches FCFS

### Multilevel Queue

```
Queue 1 (highest priority): Interactive processes
Queue 2: I/O-bound
Queue 3: CPU-bound
Queue 4 (lowest priority): Background

Each queue can have its own scheduling algorithm
```

### Multilevel Feedback Queue

- Multiple queues with different priorities
- Processes can move between queues
- Example: Process that uses too much CPU moved to lower queue

**Typical Configuration:**
- Queue 0: RR with q=8ms
- Queue 1: RR with q=16ms
- Queue 2: FCFS

New process → Queue 0
If doesn't complete in 8ms → Queue 1
If doesn't complete in 16ms → Queue 2

### Completely Fair Scheduler (CFS) - Linux

```c
// Simplified concept
virtual_runtime = actual_runtime × (nice_weight / weight)

// Pick process with smallest virtual runtime
// Uses red-black tree for O(log n) operations

struct sched_entity {
    u64 vruntime;
    // ...
};
```

**Key Ideas:**
- Fair share of CPU based on priority (nice value)
- O(log n) selection using red-black tree
- No fixed time slices

---

## 6. Multi-Processor Scheduling

### Symmetric Multiprocessing (SMP)

- All processors equal
- Shared ready queue or per-processor queues

### Load Balancing

**Push migration:** Periodic task pushes from overloaded to idle CPUs
**Pull migration:** Idle processor pulls from busy processor

### Processor Affinity

```c
cpu_set_t cpuset;
CPU_ZERO(&cpuset);
CPU_SET(0, &cpuset);  // Bind to CPU 0

pthread_setaffinity_np(pthread_self(), sizeof(cpuset), &cpuset);
```

**Cache Affinity:** Try to keep process on same processor for cache warmth

### NUMA Considerations

```
Node 0:           Node 1:
CPU 0-3           CPU 4-7
Memory 0-16GB     Memory 16-32GB
```

Access to local memory faster than remote.
Scheduler should prefer local memory.

---

# Part IV: Memory Management

---

## 7. Memory Management Basics

### Address Binding

**Compile time:** Absolute addresses (embedded systems)
**Load time:** Relocatable code
**Execution time:** Dynamic with hardware support (modern OS)

### Logical vs Physical Address

**Logical (Virtual) Address:** Generated by CPU, seen by program
**Physical Address:** Actual memory location

**Memory Management Unit (MMU):** Translates logical → physical

### Swapping

Move processes between main memory and disk (swap space).

```
Main Memory          Disk
+----------+         +----------+
|Process A |  swap   |          |
|          |-------->|Process A |
+----------+  out    +----------+
|          |         |          |
+----------+  swap   +----------+
|Process B |<--------|Process B |
+----------+  in     +----------+
```

### Contiguous Allocation

**Single Partition:** One process at a time
**Multiple Partitions:** Fixed or variable sized

**Fragmentation:**
- **External:** Free memory scattered in small pieces
- **Internal:** Allocated memory larger than requested

### Compaction

Move processes to eliminate external fragmentation.
Expensive: Requires moving memory and updating addresses.

---

## 8. Paging

### Concept

Divide physical memory into **frames** and logical memory into **pages** of same size (typically 4KB).

```
Virtual Address Space     Physical Memory
+-------+ Page 0          +-------+ Frame 0
|       |                 |       |
+-------+ Page 1          +-------+ Frame 1
|       |────────────────>|       |
+-------+ Page 2          +-------+ Frame 2
|       |                 |       |
+-------+ Page 3          +-------+ Frame 3
|       |────────────────>|       |
+-------+                 +-------+
```

### Page Table

Maps virtual page number to physical frame number.

```
Virtual Address (32-bit, 4KB pages):
+------------------+---------------+
|   Page Number    |    Offset     |
|     (20 bits)    |   (12 bits)   |
+------------------+---------------+

Page Table Entry:
+---+---+---+---+---+------------------------+
| P | R | M | A | U |    Frame Number        |
+---+---+---+---+---+------------------------+
  |   |   |   |   |
  |   |   |   |   +-- User/Supervisor
  |   |   |   +------ Accessed
  |   |   +---------- Modified (Dirty)
  |   +-------------- Referenced
  +------------------ Present/Valid
```

### Translation Lookaside Buffer (TLB)

Cache for page table entries.

```
CPU → Virtual Address
        |
        v
      ┌─────┐    hit    ┌──────────────┐
      │ TLB │────────────>│Frame Number│
      └──┬──┘           └──────┬───────┘
         │ miss                 │
         v                      v
    ┌────────────┐        Physical
    │ Page Table │        Address
    └────────────┘
```

**TLB Miss Handling:**
- Hardware: Page table walk by MMU
- Software: OS trap handler

**Typical TLB:**
- 64-1024 entries
- 99%+ hit rate
- Miss penalty: 10-100 cycles

### Multi-Level Paging

**Problem:** Page table too large for 64-bit address space

**Solution:** Hierarchical page tables

```
64-bit address (4KB pages, 4-level):
+--------+--------+--------+--------+----------+
|  PML4  |  PDPT  |   PD   |   PT   |  Offset  |
| 9 bits | 9 bits | 9 bits | 9 bits | 12 bits  |
+--------+--------+--------+--------+----------+

Walk:
CR3 → PML4 Entry → PDPT Entry → PD Entry → PT Entry → Frame
```

### Inverted Page Table

One entry per physical frame (not per virtual page).

```
Entry i: {pid, virtual_page} → frame i

Search: O(n) with hash table
Used in: PowerPC, IA-64
```

---

## 9. Page Replacement

### Page Fault

```
1. CPU generates virtual address
2. MMU checks page table → present bit = 0
3. Page fault exception
4. OS trap handler:
   a. Find page on disk
   b. Find free frame (or evict)
   c. Load page from disk
   d. Update page table
   e. Restart instruction
```

### Optimal (OPT)

Replace page that won't be used for longest time.
**Impossible to implement** (requires future knowledge).
**Used as benchmark**.

### First-In, First-Out (FIFO)

Replace oldest page.

```
Reference string: 7 0 1 2 0 3 0 4 2 3
Frames: 3

7: [7, -, -]      Fault
0: [7, 0, -]      Fault
1: [7, 0, 1]      Fault
2: [2, 0, 1]      Fault (replace 7)
0: [2, 0, 1]      Hit
3: [2, 3, 1]      Fault (replace 0)
0: [2, 3, 0]      Fault (replace 1)
4: [4, 3, 0]      Fault (replace 2)
2: [4, 2, 0]      Fault (replace 3)
3: [4, 2, 3]      Fault (replace 0)

Total faults: 9
```

**Belady's Anomaly:** More frames can cause more faults!

### Least Recently Used (LRU)

Replace page that hasn't been used for longest time.

```
Reference string: 7 0 1 2 0 3 0 4 2 3
Frames: 3

7: [7, -, -]      Fault
0: [7, 0, -]      Fault
1: [7, 0, 1]      Fault
2: [2, 0, 1]      Fault (replace 7, oldest)
0: [2, 0, 1]      Hit (0 now most recent)
3: [2, 0, 3]      Fault (replace 1)
0: [2, 0, 3]      Hit
4: [4, 0, 3]      Fault (replace 2)
2: [4, 0, 2]      Fault (replace 3)
3: [4, 3, 2]      Fault (replace 0)

Total faults: 9
```

**Implementation:**
- Counter: Update timestamp on each access
- Stack: Move page to top on access
- Both expensive in hardware

### Clock Algorithm (Second-Chance)

Approximation of LRU using reference bit.

```
Circular queue with pointer:
       ↓
[1] → [0] → [1] → [0] → [1]
 A     B     C     D     E

On page fault:
1. Check current page's reference bit
2. If 0: Replace this page
3. If 1: Clear bit, move to next
4. Repeat until finding 0
```

### Enhanced Second Chance

Use both reference and modified bits.

```
Priority:
1. (0,0): Not referenced, not modified - Best
2. (0,1): Not referenced, modified
3. (1,0): Referenced, not modified
4. (1,1): Referenced, modified - Worst
```

### Working Set Model

**Working Set:** Pages referenced in last Δ time units.

```
Reference: 2 6 1 5 7 7 7 7 5 1 6 2 3 4 1 2 3 4 4 4
                                          ↑
If Δ = 10:
Working set at this point = {1, 2, 3, 4, 6}
```

**Principle:** Keep working set in memory to avoid thrashing.

### Thrashing

**Symptom:** System spends more time paging than executing.
**Cause:** Insufficient memory for working sets.

```
CPU Utilization
     ^
     |        ____
     |      _/    \_
     |    _/        \_
     |  _/            Thrashing
     | /              ↓
     +----------------------→ Degree of Multiprogramming
```

**Solutions:**
- Reduce degree of multiprogramming
- Add more memory
- Use better page replacement

---

## 10. Virtual Memory

### Copy-on-Write (COW)

```
Parent process:
[Page 1] [Page 2] [Page 3]
    ↓         ↓        ↓
 Frame A  Frame B  Frame C (all shared, read-only)
    ↑         ↑        ↑
[Page 1] [Page 2] [Page 3]
Child process:

On write to Page 2 by child:
[Page 1] [Page 2'] [Page 3]
    ↓         ↓          ↓
 Frame A  Frame D    Frame C (Page 2' gets new frame)
    ↑         ↓          ↑  
[Page 1] [Page 2]  [Page 3]
           Frame B (still shared)
```

### Memory-Mapped Files

```c
#include <sys/mman.h>

int fd = open("file.txt", O_RDWR);
struct stat st;
fstat(fd, &st);

char* data = mmap(NULL, st.st_size, PROT_READ | PROT_WRITE,
                  MAP_SHARED, fd, 0);

// Access file as memory
data[0] = 'H';
data[1] = 'i';

munmap(data, st.st_size);
close(fd);
```

**Advantages:**
- No explicit read/write calls
- Automatic paging and caching
- Shared between processes

### Kernel Address Space

```
x86-64 Linux (48-bit virtual address):
0x0000000000000000 - 0x00007FFFFFFFFFFF : User space (128 TB)
0xFFFF800000000000 - 0xFFFFFFFFFFFFFFFF : Kernel space (128 TB)

Kernel mappings:
- Direct map of all physical memory
- vmalloc area (non-contiguous kernel allocations)
- Kernel text and data
```

---

# Part V: Synchronization

---

## 11. Synchronization Problems

### Critical Section Problem

**Requirements:**
1. **Mutual Exclusion:** Only one process in critical section
2. **Progress:** Selection of waiting process must not be postponed indefinitely
3. **Bounded Waiting:** Limit on how long a process waits

### Race Condition

```c
// Two threads incrementing counter
int counter = 0;

// Thread 1                    // Thread 2
temp1 = counter;               temp2 = counter;
temp1 = temp1 + 1;            temp2 = temp2 + 1;
counter = temp1;               counter = temp2;

// If interleaved: counter = 1, not 2
```

### Deadlock

Four conditions (all must hold):
1. **Mutual Exclusion:** Resource held exclusively
2. **Hold and Wait:** Process holds resource while waiting for another
3. **No Preemption:** Resources can't be forcibly taken
4. **Circular Wait:** Circular chain of processes waiting

```
Process A holds Resource 1, wants Resource 2
Process B holds Resource 2, wants Resource 1
→ Deadlock
```

---

## 12. Synchronization Mechanisms

### Spinlock

```c
// Test-and-set implementation
typedef struct {
    int locked;
} spinlock_t;

void spin_lock(spinlock_t* lock) {
    while (__sync_lock_test_and_set(&lock->locked, 1)) {
        // Busy wait
    }
}

void spin_unlock(spinlock_t* lock) {
    __sync_lock_release(&lock->locked);
}
```

**When to use:** Short critical sections, multiprocessor systems

### Mutex (Blocking Lock)

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

pthread_mutex_lock(&mutex);   // Block if locked
// Critical section
pthread_mutex_unlock(&mutex);
```

**When to use:** Longer critical sections, when blocking is acceptable

### Semaphore

```c
// Counting semaphore
sem_t sem;
sem_init(&sem, 0, N);  // N resources

sem_wait(&sem);  // P() operation: decrement, block if 0
// Use resource
sem_post(&sem);  // V() operation: increment

// Binary semaphore (mutex)
sem_t binary;
sem_init(&binary, 0, 1);
```

### Producer-Consumer with Semaphores

```c
#define BUFFER_SIZE 10

sem_t empty, full;
pthread_mutex_t mutex;
int buffer[BUFFER_SIZE];
int in = 0, out = 0;

void init() {
    sem_init(&empty, 0, BUFFER_SIZE);  // Empty slots
    sem_init(&full, 0, 0);             // Full slots
    pthread_mutex_init(&mutex, NULL);
}

void* producer(void* arg) {
    int item;
    while (1) {
        item = produce_item();
        
        sem_wait(&empty);              // Wait for empty slot
        pthread_mutex_lock(&mutex);
        
        buffer[in] = item;
        in = (in + 1) % BUFFER_SIZE;
        
        pthread_mutex_unlock(&mutex);
        sem_post(&full);               // Signal full slot
    }
}

void* consumer(void* arg) {
    int item;
    while (1) {
        sem_wait(&full);               // Wait for full slot
        pthread_mutex_lock(&mutex);
        
        item = buffer[out];
        out = (out + 1) % BUFFER_SIZE;
        
        pthread_mutex_unlock(&mutex);
        sem_post(&empty);              // Signal empty slot
        
        consume_item(item);
    }
}
```

### Readers-Writers Problem

```c
// Writers have priority variation
pthread_mutex_t mutex, write_lock;
pthread_cond_t can_read;
int readers = 0;
int writers = 0;
int waiting_writers = 0;

void reader_enter() {
    pthread_mutex_lock(&mutex);
    while (writers > 0 || waiting_writers > 0) {
        pthread_cond_wait(&can_read, &mutex);
    }
    readers++;
    pthread_mutex_unlock(&mutex);
}

void reader_exit() {
    pthread_mutex_lock(&mutex);
    readers--;
    if (readers == 0) {
        pthread_cond_signal(&write_lock);
    }
    pthread_mutex_unlock(&mutex);
}

void writer_enter() {
    pthread_mutex_lock(&mutex);
    waiting_writers++;
    while (readers > 0 || writers > 0) {
        pthread_cond_wait(&write_lock, &mutex);
    }
    waiting_writers--;
    writers++;
    pthread_mutex_unlock(&mutex);
}

void writer_exit() {
    pthread_mutex_lock(&mutex);
    writers--;
    pthread_cond_broadcast(&can_read);
    pthread_cond_signal(&write_lock);
    pthread_mutex_unlock(&mutex);
}
```

### Dining Philosophers

```c
#define N 5
pthread_mutex_t forks[N];

void philosopher(int id) {
    int left = id;
    int right = (id + 1) % N;
    
    while (1) {
        think();
        
        // Prevent deadlock: lowest-numbered fork first
        if (id % 2 == 0) {
            pthread_mutex_lock(&forks[left]);
            pthread_mutex_lock(&forks[right]);
        } else {
            pthread_mutex_lock(&forks[right]);
            pthread_mutex_lock(&forks[left]);
        }
        
        eat();
        
        pthread_mutex_unlock(&forks[left]);
        pthread_mutex_unlock(&forks[right]);
    }
}
```

---

# Part VI: File Systems

---

## 13. File System Interface

### File Operations

```c
// Create and open
int fd = open("file.txt", O_CREAT | O_RDWR, 0644);

// Write
write(fd, buffer, count);

// Read
read(fd, buffer, count);

// Seek
lseek(fd, offset, SEEK_SET);  // From beginning
lseek(fd, offset, SEEK_CUR);  // From current
lseek(fd, offset, SEEK_END);  // From end

// Get info
struct stat st;
fstat(fd, &st);

// Close
close(fd);

// Delete
unlink("file.txt");
```

### Directory Operations

```c
// Create directory
mkdir("dirname", 0755);

// Open and read directory
DIR* dir = opendir(".");
struct dirent* entry;
while ((entry = readdir(dir)) != NULL) {
    printf("%s\n", entry->d_name);
}
closedir(dir);

// Remove directory
rmdir("dirname");

// Change directory
chdir("/path");

// Hard link
link("oldname", "newname");

// Symbolic link
symlink("target", "linkname");
```

### File Descriptors

```
Process File Descriptor Table:
fd 0 → [stdin]  → File Table Entry → Inode
fd 1 → [stdout] → File Table Entry → Inode
fd 2 → [stderr] → File Table Entry → Inode
fd 3 → [file1]  → File Table Entry → Inode

File Table (system-wide):
- Current position (offset)
- Access mode
- Reference count
- Pointer to inode

Inode:
- File metadata
- Data block pointers
```

### I/O Redirection

```c
// Redirect stdout to file
int fd = open("output.txt", O_WRONLY | O_CREAT, 0644);
dup2(fd, STDOUT_FILENO);  // fd 1 now points to file
close(fd);

printf("This goes to file\n");
```

---

## 14. File System Implementation

### Disk Structure

```
+------------------+------------------+------------------+
|   Boot Block     |   Super Block    |   Inode Table    |
+------------------+------------------+------------------+
|                     Data Blocks                        |
+--------------------------------------------------------+
```

**Super Block:**
- File system type
- Block size
- Number of blocks
- Number of inodes
- Free block/inode lists

### Inode Structure (ext4)

```c
struct ext4_inode {
    __le16  i_mode;         // File mode
    __le16  i_uid;          // Owner UID
    __le32  i_size_lo;      // Size in bytes
    __le32  i_atime;        // Access time
    __le32  i_ctime;        // Change time
    __le32  i_mtime;        // Modification time
    __le32  i_dtime;        // Deletion time
    __le16  i_gid;          // Group ID
    __le16  i_links_count;  // Hard link count
    __le32  i_blocks_lo;    // Block count
    __le32  i_flags;        // File flags
    // ...
    __le32  i_block[15];    // Block pointers
    // ...
};
```

### Block Allocation

**Direct Blocks:** 12 block pointers
**Single Indirect:** Pointer to block of pointers
**Double Indirect:** Pointer to block of single indirect blocks
**Triple Indirect:** Pointer to block of double indirect blocks

```
For 4KB blocks, 4-byte pointers (1024 per block):

Direct:         12 × 4KB = 48 KB
Single:         1024 × 4KB = 4 MB
Double:         1024² × 4KB = 4 GB
Triple:         1024³ × 4KB = 4 TB

Max file size: 48KB + 4MB + 4GB + 4TB ≈ 4 TB
```

### Free Space Management

**Bitmap:** One bit per block
```
0 1 1 0 1 1 1 0 0 1...
Free  Used  Free  Used...
```

**Free List:** Linked list of free blocks

### Directory Implementation

**Linear List:**
```
| inode | name_len | name      |
| 17    | 5        | "file1"   |
| 23    | 6        | "subdir"  |
| 42    | 10       | "readme.txt" |
```

**Hash Table:** Better for large directories

### Virtual File System (VFS)

```
User Process
     |
  ↓ read(fd, buf, n)
     |
+----+----+----+----+
|   VFS Layer       |  ← Common interface
+----+----+----+----+
  |    |    |    |
 ext4  xfs  nfs  fat32  ← Specific implementations
```

**Key Structures:**
- `super_block`: Mounted file system info
- `inode`: File metadata
- `dentry`: Directory entry (name → inode mapping)
- `file`: Open file instance

### Journaling

**Problem:** Crash during multi-block operation → inconsistent state

**Solution:** Write-ahead logging

```
Journal:
1. Write all operations to journal
2. Write commit record
3. Perform actual operations
4. Clear journal

On recovery:
- If commit record present: Replay journal
- If no commit record: Discard incomplete transaction
```

**Types:**
- **Metadata journaling:** Only journal metadata (ext3/4 default)
- **Full journaling:** Journal data too (slower)

---

## 15. I/O Systems

### I/O Hardware

**I/O Ports:**
```c
// x86 port I/O
outb(data, port);  // Write byte to port
inb(port);         // Read byte from port
```

**Memory-Mapped I/O:**
```c
// Device registers mapped to memory addresses
volatile uint32_t* device = (uint32_t*)0xFE200000;
*device = value;  // Write to device
```

### I/O Methods

**Programmed I/O (Polling):**
```c
while (!device_ready());  // Busy wait
send_data(data);
```

**Interrupt-Driven I/O:**
```c
// Initiate I/O
send_data(data);

// Continue other work...

// Interrupt handler called when complete
void interrupt_handler() {
    // Handle completion
}
```

**DMA (Direct Memory Access):**
```
CPU                Memory              Device
 |                   |                   |
 |-- Setup DMA ---->|                   |
 |                  |<--- Transfer ---->|
 |<-- Interrupt ----|                   |
```

### Block I/O Layers

```
Application
    |
File System
    |
Block Layer (request queue)
    |
I/O Scheduler
    |
Device Driver
    |
Hardware
```

### Disk Scheduling

**FCFS:** First come, first served

**SSTF:** Shortest seek time first (like SJF)
- Greedy, may cause starvation

**SCAN (Elevator):**
```
Head moves in one direction, servicing all requests
At end, reverses direction

Requests: 98, 183, 37, 122, 14, 124, 65, 67
Head at: 53, moving up

Order: 65, 67, 98, 122, 124, 183 → reverse → 37, 14
```

**C-SCAN:** Only service in one direction, jump back to start
**LOOK:** Like SCAN but reverses at last request, not disk end

### Linux I/O Schedulers

**Completely Fair Queuing (CFQ):** Per-process queues, fair time
**Deadline:** Separate read/write queues with deadlines
**NOOP:** Simple FIFO (for SSDs, no seek time)
**BFQ (Budget Fair Queuing):** Improved CFQ

```bash
# Check/change scheduler
cat /sys/block/sda/queue/scheduler
echo deadline > /sys/block/sda/queue/scheduler
```

---

# Part VII: Advanced Topics

---

## 16. Signals

### Signal Handling

```c
#include <signal.h>

void handler(int sig) {
    write(STDOUT_FILENO, "Caught signal\n", 14);
}

int main() {
    // Simple handler
    signal(SIGINT, handler);
    
    // Or using sigaction (preferred)
    struct sigaction sa;
    sa.sa_handler = handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGINT, &sa, NULL);
    
    while (1) {
        pause();  // Wait for signal
    }
    
    return 0;
}
```

### Common Signals

| Signal | Number | Default | Description |
|--------|--------|---------|-------------|
| SIGHUP | 1 | Term | Hangup |
| SIGINT | 2 | Term | Interrupt (Ctrl+C) |
| SIGQUIT | 3 | Core | Quit (Ctrl+\) |
| SIGKILL | 9 | Term | Kill (can't be caught) |
| SIGSEGV | 11 | Core | Segmentation fault |
| SIGPIPE | 13 | Term | Broken pipe |
| SIGALRM | 14 | Term | Alarm clock |
| SIGTERM | 15 | Term | Termination |
| SIGCHLD | 17 | Ignore | Child stopped or terminated |
| SIGCONT | 18 | Continue | Continue if stopped |
| SIGSTOP | 19 | Stop | Stop (can't be caught) |

### Sending Signals

```c
kill(pid, SIGTERM);     // Send to specific process
raise(SIGTERM);         // Send to self
alarm(5);               // SIGALRM in 5 seconds
```

---

## 17. Boot Process

### x86 Boot Sequence

```
1. BIOS/UEFI
   - POST (Power-On Self Test)
   - Initialize hardware
   - Find bootable device

2. Bootloader (GRUB)
   - Load from MBR/GPT
   - Present boot menu
   - Load kernel and initrd

3. Kernel Initialization
   - Decompress (if compressed)
   - Initialize memory management
   - Initialize devices
   - Mount root filesystem

4. Init System (systemd/init)
   - PID 1
   - Start system services
   - Mount filesystems
   - Start login prompt
```

### Systemd

```bash
# Service management
systemctl start nginx
systemctl stop nginx
systemctl restart nginx
systemctl status nginx
systemctl enable nginx   # Start at boot
systemctl disable nginx

# System control
systemctl poweroff
systemctl reboot
systemctl suspend

# View logs
journalctl -u nginx
journalctl -f           # Follow
journalctl -b           # Since boot
```

---

## 18. Containers and Virtualization

### Virtualization Types

**Full Virtualization:**
- Hypervisor emulates hardware
- Guest OS unmodified
- Examples: VMware, VirtualBox

**Para-virtualization:**
- Guest OS modified for efficiency
- Example: Xen

**Hardware-assisted:**
- CPU support (Intel VT-x, AMD-V)
- Example: KVM

### Containers

**Linux Namespaces:**
```
- PID namespace: Process isolation
- Network namespace: Network stack isolation
- Mount namespace: File system views
- User namespace: User/group ID mapping
- UTS namespace: Hostname isolation
- IPC namespace: Inter-process communication
```

**cgroups (Control Groups):**
```bash
# Limit CPU
echo 50000 > /sys/fs/cgroup/cpu/mygroup/cpu.cfs_quota_us

# Limit memory
echo 100M > /sys/fs/cgroup/memory/mygroup/memory.limit_in_bytes
```

**Docker Basics:**
```bash
# Run container
docker run -it ubuntu bash

# List containers
docker ps -a

# Build image
docker build -t myimage .

# Common Dockerfile
FROM ubuntu:20.04
RUN apt-get update && apt-get install -y nginx
COPY index.html /var/www/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## System Calls Reference

### Process
```c
fork()      // Create child process
exec*()     // Replace process image
wait()      // Wait for child
exit()      // Terminate process
getpid()    // Get process ID
getppid()   // Get parent process ID
```

### File
```c
open()      // Open file
close()     // Close file descriptor
read()      // Read from file
write()     // Write to file
lseek()     // Reposition file offset
dup()       // Duplicate file descriptor
dup2()      // Duplicate to specific fd
fcntl()     // File control
ioctl()     // Device control
stat()      // Get file status
```

### Memory
```c
mmap()      // Map memory
munmap()    // Unmap memory
brk()       // Change data segment size
mprotect()  // Set memory protection
```

### IPC
```c
pipe()      // Create pipe
socket()    // Create socket
shmget()    // Get shared memory
semget()    // Get semaphore
msgget()    // Get message queue
```

---

## Cross-References

- [[02_Computer_Architecture]] - Hardware-software interface
- [[04_Algorithms_Data_Structures]] - Scheduling algorithms, data structures
- [[06_Computer_Networks]] - Socket programming, network stack
- [[08_C_Programming]] - System programming in C
