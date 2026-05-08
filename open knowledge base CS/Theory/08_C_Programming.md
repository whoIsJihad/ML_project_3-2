# C Programming

## Course Overview
**Depth:** University undergraduate + systems programming proficiency  
**Time:** 3-4 hours focused reading  
**Prerequisites:** Basic programming concepts

---

# Part I: Language Fundamentals

---

## 1. Data Types and Memory

### Primitive Types

| Type | Size (typical) | Range | Format Specifier |
|------|----------------|-------|------------------|
| char | 1 byte | -128 to 127 | %c, %hhd |
| unsigned char | 1 byte | 0 to 255 | %hhu |
| short | 2 bytes | -32,768 to 32,767 | %hd |
| unsigned short | 2 bytes | 0 to 65,535 | %hu |
| int | 4 bytes | -2³¹ to 2³¹-1 | %d |
| unsigned int | 4 bytes | 0 to 2³²-1 | %u |
| long | 4/8 bytes | Platform-dependent | %ld |
| long long | 8 bytes | -2⁶³ to 2⁶³-1 | %lld |
| float | 4 bytes | ~7 digits precision | %f, %e, %g |
| double | 8 bytes | ~15 digits precision | %lf, %le, %lg |

### Fixed-Width Types (stdint.h)

```c
#include <stdint.h>

int8_t   i8;    // Exactly 8 bits, signed
uint8_t  u8;    // Exactly 8 bits, unsigned
int16_t  i16;   // Exactly 16 bits
uint16_t u16;
int32_t  i32;   // Exactly 32 bits
uint32_t u32;
int64_t  i64;   // Exactly 64 bits
uint64_t u64;

// For pointers
intptr_t  ptr_signed;   // Signed, can hold pointer
uintptr_t ptr_unsigned; // Unsigned, can hold pointer
size_t    size;         // Result of sizeof, unsigned
ptrdiff_t diff;         // Pointer subtraction result
```

### Type Qualifiers

```c
const int MAX = 100;           // Cannot be modified
volatile int *port;            // May change unexpectedly (hardware)
register int counter;          // Hint: Keep in register
restrict int *p;               // Pointer is only access to memory

// const pointer combinations
const int *p1;                 // Pointer to const int
int const *p2;                 // Same as above
int *const p3 = &x;            // Const pointer to int
const int *const p4 = &x;      // Const pointer to const int
```

### Storage Classes

```c
auto int x;      // Local variable (default, rarely used)
static int y;    // Persists between function calls
extern int z;    // Declared elsewhere (another file)
register int r;  // Request register storage

// Static variables
void counter() {
    static int count = 0;  // Initialized once
    count++;
    printf("%d\n", count);
}

// Static functions
static void helper() {  // File-scope only
    // ...
}
```

### sizeof Operator

```c
printf("char: %zu\n", sizeof(char));      // Always 1
printf("int: %zu\n", sizeof(int));        // Typically 4
printf("double: %zu\n", sizeof(double));  // Typically 8
printf("pointer: %zu\n", sizeof(void*));  // 4 or 8 (32/64-bit)

int arr[10];
printf("array: %zu\n", sizeof(arr));      // 40 (10 * 4)
printf("elements: %zu\n", sizeof(arr)/sizeof(arr[0]));  // 10
```

---

## 2. Operators

### Operator Precedence (High to Low)

| Precedence | Operators | Associativity |
|------------|-----------|---------------|
| 1 | `()` `[]` `->` `.` `++` `--` (postfix) | Left |
| 2 | `++` `--` (prefix) `+` `-` `!` `~` `*` `&` `sizeof` `(type)` | Right |
| 3 | `*` `/` `%` | Left |
| 4 | `+` `-` | Left |
| 5 | `<<` `>>` | Left |
| 6 | `<` `<=` `>` `>=` | Left |
| 7 | `==` `!=` | Left |
| 8 | `&` | Left |
| 9 | `^` | Left |
| 10 | `\|` | Left |
| 11 | `&&` | Left |
| 12 | `\|\|` | Left |
| 13 | `?:` | Right |
| 14 | `=` `+=` `-=` etc. | Right |
| 15 | `,` | Left |

### Bitwise Operators

```c
// AND: Both bits 1
0b1010 & 0b1100  // = 0b1000 (8)

// OR: Either bit 1
0b1010 | 0b1100  // = 0b1110 (14)

// XOR: Bits differ
0b1010 ^ 0b1100  // = 0b0110 (6)

// NOT: Invert all bits
~0b1010  // = ...11110101

// Left shift: Multiply by 2^n
5 << 2   // = 20 (5 * 4)

// Right shift: Divide by 2^n
20 >> 2  // = 5 (20 / 4)

// Common patterns
x & (1 << n)      // Test bit n
x | (1 << n)      // Set bit n
x & ~(1 << n)     // Clear bit n
x ^ (1 << n)      // Toggle bit n
x & (x - 1)       // Clear lowest set bit
x & (-x)          // Isolate lowest set bit
__builtin_popcount(x)  // Count set bits (GCC)
```

### Short-Circuit Evaluation

```c
// && stops at first false
if (ptr != NULL && ptr->value > 0) {
    // Safe: ptr checked before dereference
}

// || stops at first true
if (is_valid() || fallback()) {
    // fallback() only called if is_valid() is false
}
```

### Comma Operator

```c
// Evaluates left to right, result is rightmost
int x = (a = 5, b = 10, a + b);  // x = 15

// Common in for loops
for (i = 0, j = n; i < j; i++, j--) {
    // ...
}
```

---

## 3. Control Flow

### Conditional Statements

```c
// if-else
if (condition) {
    // ...
} else if (other) {
    // ...
} else {
    // ...
}

// Ternary operator
int max = (a > b) ? a : b;

// switch
switch (value) {
    case 1:
        // ...
        break;
    case 2:
    case 3:
        // Fall through for 2 and 3
        break;
    default:
        // ...
        break;
}
```

### Loops

```c
// while
while (condition) {
    // ...
}

// do-while (executes at least once)
do {
    // ...
} while (condition);

// for
for (int i = 0; i < n; i++) {
    // ...
}

// for with multiple variables
for (int i = 0, j = n-1; i < j; i++, j--) {
    // ...
}

// Infinite loops
while (1) { }
for (;;) { }
```

### Jump Statements

```c
break;       // Exit innermost loop/switch
continue;    // Skip to next iteration
return x;    // Return from function
goto label;  // Jump to label (use sparingly!)

// goto example (cleanup pattern)
int process() {
    FILE *f1 = fopen("a.txt", "r");
    if (!f1) goto error1;
    
    FILE *f2 = fopen("b.txt", "r");
    if (!f2) goto error2;
    
    // Process...
    
    fclose(f2);
    fclose(f1);
    return 0;
    
error2:
    fclose(f1);
error1:
    return -1;
}
```

---

## 4. Functions

### Function Basics

```c
// Declaration (prototype)
int add(int a, int b);

// Definition
int add(int a, int b) {
    return a + b;
}

// void function
void print_hello(void) {  // void = no parameters
    printf("Hello\n");
}

// Inline function (hint for optimization)
inline int square(int x) {
    return x * x;
}
```

### Pass by Value vs Reference

```c
// Pass by value (copy)
void increment_value(int n) {
    n++;  // Modifies local copy only
}

// Pass by reference (pointer)
void increment_ref(int *n) {
    (*n)++;  // Modifies original
}

int x = 5;
increment_value(x);  // x still 5
increment_ref(&x);   // x is now 6
```

### Arrays as Parameters

```c
// Arrays decay to pointers when passed
void process_array(int *arr, size_t len) {
    // sizeof(arr) is sizeof(int*), NOT array size!
    for (size_t i = 0; i < len; i++) {
        arr[i] *= 2;
    }
}

// Or with array notation (equivalent)
void process_array(int arr[], size_t len) {
    // Same as above
}

// Fixed-size array (C99)
void process_fixed(int arr[static 10]) {
    // Compiler knows array has at least 10 elements
}
```

### Variadic Functions

```c
#include <stdarg.h>

int sum(int count, ...) {
    va_list args;
    va_start(args, count);  // Initialize after last named param
    
    int total = 0;
    for (int i = 0; i < count; i++) {
        total += va_arg(args, int);  // Get next argument
    }
    
    va_end(args);  // Cleanup
    return total;
}

int result = sum(4, 10, 20, 30, 40);  // = 100
```

### Function Pointers

```c
// Declaration
int (*func_ptr)(int, int);

// Assignment
func_ptr = add;
func_ptr = &add;  // Same

// Calling
int result = func_ptr(3, 4);
int result = (*func_ptr)(3, 4);  // Same

// Typedef for clarity
typedef int (*Operation)(int, int);
Operation op = add;

// Array of function pointers
Operation ops[] = {add, subtract, multiply};
int result = ops[0](5, 3);  // Calls add(5, 3)

// Callback pattern
void sort(int *arr, int n, int (*compare)(int, int)) {
    // Use compare function
}

int ascending(int a, int b) { return a - b; }
sort(arr, n, ascending);
```

---

# Part II: Pointers and Memory

---

## 5. Pointers

### Pointer Basics

```c
int x = 42;
int *p = &x;     // p holds address of x

printf("%p\n", (void*)p);   // Print address
printf("%d\n", *p);         // Dereference: print 42

*p = 100;        // Change x through pointer
```

### Pointer Arithmetic

```c
int arr[] = {10, 20, 30, 40, 50};
int *p = arr;    // Points to arr[0]

p++;             // Now points to arr[1]
p += 2;          // Now points to arr[3]
p--;             // Now points to arr[2]

// Pointer difference
int *start = arr;
int *end = &arr[4];
ptrdiff_t diff = end - start;  // = 4 (elements, not bytes)

// Comparison
if (p < end) { }  // Valid for same array
```

### Arrays and Pointers

```c
int arr[5] = {1, 2, 3, 4, 5};

// These are equivalent:
arr[i]        // Array subscript
*(arr + i)    // Pointer arithmetic
*(i + arr)    // Commutative
i[arr]        // Yes, this works!

// But arr is NOT a pointer
&arr          // Type: int (*)[5] (pointer to array)
&arr[0]       // Type: int*
sizeof(arr)   // Size of whole array
sizeof(&arr[0])  // Size of pointer
```

### Pointers to Pointers

```c
int x = 5;
int *p = &x;
int **pp = &p;

printf("%d\n", **pp);  // 5

// Dynamically allocated 2D array
int **matrix = malloc(rows * sizeof(int*));
for (int i = 0; i < rows; i++) {
    matrix[i] = malloc(cols * sizeof(int));
}

matrix[i][j] = value;

// Free in reverse order
for (int i = 0; i < rows; i++) {
    free(matrix[i]);
}
free(matrix);
```

### Void Pointers

```c
void *generic;

int x = 5;
generic = &x;                   // Any pointer can convert to void*
int *ip = (int*)generic;        // Must cast back before dereference

// Cannot dereference void*
// *generic;  // ERROR

// Common use: Generic functions
void swap(void *a, void *b, size_t size) {
    char temp[size];  // VLA
    memcpy(temp, a, size);
    memcpy(a, b, size);
    memcpy(b, temp, size);
}

int a = 5, b = 10;
swap(&a, &b, sizeof(int));
```

### NULL Pointer

```c
int *p = NULL;
int *q = 0;       // Same as NULL
int *r = (void*)0;  // Same

// Always check before dereferencing
if (p != NULL) {
    *p = 10;
}

// Modern C: Better practice
if (p) {
    *p = 10;
}
```

---

## 6. Dynamic Memory

### Memory Functions

```c
#include <stdlib.h>

// Allocate uninitialized memory
void *malloc(size_t size);

// Allocate and zero-initialize
void *calloc(size_t num, size_t size);

// Resize allocation
void *realloc(void *ptr, size_t new_size);

// Free memory
void free(void *ptr);
```

### Usage Patterns

```c
// Single variable
int *p = malloc(sizeof(int));
if (p == NULL) {
    // Handle allocation failure
    perror("malloc");
    exit(1);
}
*p = 42;
free(p);
p = NULL;  // Prevent dangling pointer

// Array
int *arr = malloc(n * sizeof(int));
// Or safer:
int *arr = malloc(n * sizeof(*arr));

// Zeroed array
int *arr = calloc(n, sizeof(int));

// Resize
int *new_arr = realloc(arr, new_size * sizeof(int));
if (new_arr == NULL) {
    // realloc failed, original arr still valid
    free(arr);
    exit(1);
}
arr = new_arr;
```

### Memory Errors

```c
// 1. Memory leak
int *p = malloc(100);
p = NULL;  // Lost the pointer, can't free!

// 2. Double free
int *p = malloc(100);
free(p);
free(p);  // Undefined behavior!

// 3. Use after free
int *p = malloc(sizeof(int));
free(p);
*p = 10;  // Undefined behavior!

// 4. Buffer overflow
int *arr = malloc(10 * sizeof(int));
arr[10] = 5;  // Out of bounds!

// 5. Uninitialized read
int *p = malloc(sizeof(int));
printf("%d\n", *p);  // Uninitialized value!
```

### Memory Layout

```
Stack (high address)
|  Local variables      |
|  Function parameters  |
|  Return addresses     |
|         ↓             |
|         ...           |
|         ↑             |
|  Dynamic allocations  |
Heap
|  Uninitialized data   |
BSS
|  Initialized data     |
Data
|  Program code         |
Text (low address)
```

---

## 7. Strings

### String Basics

```c
// String literal (read-only)
const char *s1 = "Hello";

// Character array (modifiable)
char s2[] = "Hello";       // Size: 6 (includes '\0')
char s3[10] = "Hello";     // Size: 10, padded with '\0'

// Manual initialization
char s4[] = {'H', 'e', 'l', 'l', 'o', '\0'};
```

### String Functions (string.h)

```c
#include <string.h>

size_t strlen(const char *s);              // Length (not including '\0')
char *strcpy(char *dest, const char *src); // Copy (unsafe!)
char *strncpy(char *dest, const char *src, size_t n);  // Copy with limit
char *strcat(char *dest, const char *src); // Concatenate (unsafe!)
char *strncat(char *dest, const char *src, size_t n);  // Concat with limit
int strcmp(const char *s1, const char *s2);  // Compare
int strncmp(const char *s1, const char *s2, size_t n); // Compare n chars
char *strchr(const char *s, int c);        // Find first char
char *strrchr(const char *s, int c);       // Find last char
char *strstr(const char *haystack, const char *needle); // Find substring
char *strtok(char *str, const char *delim); // Tokenize
void *memcpy(void *dest, const void *src, size_t n);   // Copy memory
void *memmove(void *dest, const void *src, size_t n);  // Copy (overlap safe)
void *memset(void *s, int c, size_t n);    // Fill memory
int memcmp(const void *s1, const void *s2, size_t n);  // Compare memory
```

### Safe String Handling

```c
// Always check buffer size
char dest[20];
size_t dest_size = sizeof(dest);

// Safe copy
int result = snprintf(dest, dest_size, "%s", src);
if (result >= dest_size) {
    // Truncation occurred
}

// Manual safe copy
size_t src_len = strlen(src);
if (src_len < dest_size) {
    strcpy(dest, src);
} else {
    // Handle error
}

// strlcpy (BSD, not standard but common)
strlcpy(dest, src, dest_size);  // Always null-terminates
```

### String Conversion

```c
#include <stdlib.h>

int atoi(const char *s);        // String to int
long atol(const char *s);       // String to long
double atof(const char *s);     // String to double

// Better alternatives (provide error checking)
long strtol(const char *s, char **endptr, int base);
unsigned long strtoul(const char *s, char **endptr, int base);
double strtod(const char *s, char **endptr);

char *endptr;
long val = strtol("123abc", &endptr, 10);
// val = 123, *endptr = 'a'

// Int to string
char buffer[20];
snprintf(buffer, sizeof(buffer), "%d", value);
```

---

## 8. Structures and Unions

### Structure Basics

```c
// Definition
struct Point {
    int x;
    int y;
};

// Declaration and initialization
struct Point p1;
struct Point p2 = {10, 20};
struct Point p3 = {.y = 20, .x = 10};  // Designated initializers

// Access
p1.x = 5;
p1.y = 10;

// Pointer to structure
struct Point *pp = &p1;
pp->x = 15;        // Arrow operator
(*pp).y = 25;      // Equivalent
```

### Typedef

```c
typedef struct {
    char name[50];
    int age;
} Person;

Person p = {"Alice", 30};

// Or with named struct
typedef struct Node {
    int data;
    struct Node *next;  // Self-reference requires struct keyword
} Node;

Node *head = NULL;
```

### Structure Padding and Alignment

```c
struct Padded {
    char a;      // 1 byte
    // 3 bytes padding
    int b;       // 4 bytes
    char c;      // 1 byte
    // 3 bytes padding
};
// Total: 12 bytes

struct Packed {
    int b;       // 4 bytes
    char a;      // 1 byte
    char c;      // 1 byte
    // 2 bytes padding
};
// Total: 8 bytes

// Force packing (GCC)
struct __attribute__((packed)) NoPadding {
    char a;
    int b;
    char c;
};
// Total: 6 bytes (but potentially slower access)

// Check size and offset
#include <stddef.h>
offsetof(struct Padded, b)  // Offset of member b
```

### Bit Fields

```c
struct Flags {
    unsigned int read  : 1;
    unsigned int write : 1;
    unsigned int exec  : 1;
    unsigned int       : 5;  // Padding
};

struct Flags f = {1, 1, 0};
if (f.read) {
    // ...
}

// Common use: Hardware registers
struct StatusReg {
    unsigned int ready   : 1;
    unsigned int error   : 1;
    unsigned int mode    : 3;
    unsigned int reserved: 27;
};
```

### Unions

```c
// All members share same memory
union Data {
    int i;
    float f;
    char str[4];
};

union Data d;
d.i = 0x41424344;
printf("%s\n", d.str);  // "DCBA" (little-endian)

sizeof(union Data);  // Size of largest member

// Type punning (reinterpret bits)
union FloatInt {
    float f;
    uint32_t i;
};

union FloatInt fi;
fi.f = 3.14f;
printf("Bits: 0x%08X\n", fi.i);
```

### Tagged Union

```c
typedef enum { INT, FLOAT, STRING } Type;

typedef struct {
    Type type;
    union {
        int i;
        float f;
        char *s;
    } value;
} Variant;

Variant v;
v.type = INT;
v.value.i = 42;

// Or with anonymous union (C11)
typedef struct {
    Type type;
    union {
        int i;
        float f;
        char *s;
    };
} Variant2;

Variant2 v2;
v2.type = FLOAT;
v2.f = 3.14f;  // Direct access
```

---

## 9. Enumerations

```c
// Basic enum
enum Color {
    RED,      // 0
    GREEN,    // 1
    BLUE      // 2
};

enum Color c = RED;

// With explicit values
enum Status {
    OK = 0,
    ERROR = -1,
    PENDING = 100
};

// Typedef
typedef enum {
    LOW = 1,
    MEDIUM = 5,
    HIGH = 10
} Priority;

Priority p = HIGH;
```

---

# Part III: Input/Output

---

## 10. Standard I/O

### Output Functions

```c
#include <stdio.h>

// Character output
int putchar(int c);
int fputc(int c, FILE *stream);

// String output
int puts(const char *s);      // Adds newline
int fputs(const char *s, FILE *stream);  // No newline

// Formatted output
int printf(const char *format, ...);
int fprintf(FILE *stream, const char *format, ...);
int sprintf(char *str, const char *format, ...);     // Unsafe!
int snprintf(char *str, size_t size, const char *format, ...);
```

### Format Specifiers

```c
%d, %i   // Signed decimal integer
%u       // Unsigned decimal integer
%o       // Unsigned octal
%x, %X   // Unsigned hexadecimal
%f       // Floating-point (decimal)
%e, %E   // Floating-point (scientific)
%g, %G   // Shorter of %f or %e
%c       // Character
%s       // String
%p       // Pointer
%%       // Literal %

// Width and precision
%10d     // Minimum width 10
%-10d    // Left-align
%010d    // Zero-pad
%.2f     // 2 decimal places
%10.2f   // Width 10, 2 decimal places
%*d      // Width from argument

printf("%*d", 10, 42);  // Same as %10d
```

### Input Functions

```c
// Character input
int getchar(void);
int fgetc(FILE *stream);

// String input (safe)
char *fgets(char *s, int size, FILE *stream);

// DO NOT USE
// gets() - No buffer size check, removed in C11

// Formatted input
int scanf(const char *format, ...);
int fscanf(FILE *stream, const char *format, ...);
int sscanf(const char *str, const char *format, ...);

// Safe string input
char buffer[100];
if (fgets(buffer, sizeof(buffer), stdin)) {
    // Remove newline
    buffer[strcspn(buffer, "\n")] = '\0';
}
```

### scanf Caveats

```c
int num;
char str[50];

// Whitespace handling
scanf("%d", &num);    // Skip leading whitespace
scanf(" %c", &ch);    // Space skips whitespace before %c
scanf("%49s", str);   // No & for arrays, limit width!

// Don't mix scanf and fgets
scanf("%d", &num);
getchar();            // Consume leftover newline
fgets(str, sizeof(str), stdin);

// Better: Use fgets + sscanf
char line[100];
fgets(line, sizeof(line), stdin);
sscanf(line, "%d", &num);
```

---

## 11. File I/O

### File Operations

```c
FILE *fopen(const char *filename, const char *mode);
int fclose(FILE *stream);
int fflush(FILE *stream);  // Flush buffer to file

// Modes
"r"   // Read (file must exist)
"w"   // Write (creates/truncates)
"a"   // Append (creates if needed)
"r+"  // Read and write (file must exist)
"w+"  // Read and write (creates/truncates)
"a+"  // Read and append

"rb"  // Binary mode (Windows)
```

### Basic File I/O

```c
// Text file writing
FILE *fp = fopen("output.txt", "w");
if (fp == NULL) {
    perror("fopen");
    return 1;
}

fprintf(fp, "Hello, %s!\n", "World");
fputs("Another line\n", fp);

fclose(fp);

// Text file reading
FILE *fp = fopen("input.txt", "r");
if (fp == NULL) {
    perror("fopen");
    return 1;
}

char line[256];
while (fgets(line, sizeof(line), fp)) {
    printf("%s", line);
}

fclose(fp);
```

### Binary I/O

```c
size_t fread(void *ptr, size_t size, size_t count, FILE *stream);
size_t fwrite(const void *ptr, size_t size, size_t count, FILE *stream);

// Writing binary data
int numbers[] = {1, 2, 3, 4, 5};
FILE *fp = fopen("data.bin", "wb");
fwrite(numbers, sizeof(int), 5, fp);
fclose(fp);

// Reading binary data
int buffer[5];
FILE *fp = fopen("data.bin", "rb");
size_t read = fread(buffer, sizeof(int), 5, fp);
fclose(fp);

// Structure I/O
typedef struct {
    int id;
    char name[50];
    float score;
} Record;

Record r = {1, "Alice", 95.5f};
fwrite(&r, sizeof(Record), 1, fp);

Record r2;
fread(&r2, sizeof(Record), 1, fp);
```

### File Positioning

```c
int fseek(FILE *stream, long offset, int whence);
long ftell(FILE *stream);
void rewind(FILE *stream);  // Same as fseek(fp, 0, SEEK_SET)

// whence values
SEEK_SET  // Beginning of file
SEEK_CUR  // Current position
SEEK_END  // End of file

// Get file size
fseek(fp, 0, SEEK_END);
long size = ftell(fp);
fseek(fp, 0, SEEK_SET);

// For large files (C99)
int fseeko(FILE *stream, off_t offset, int whence);
off_t ftello(FILE *stream);
```

### Error Handling

```c
int ferror(FILE *stream);  // Non-zero if error occurred
int feof(FILE *stream);    // Non-zero if EOF reached
void clearerr(FILE *stream);  // Clear error and EOF indicators

// Proper read loop
while (!feof(fp)) {  // WRONG - feof() true AFTER failed read
    // ...
}

// Correct way
while (fgets(line, sizeof(line), fp) != NULL) {
    // Process line
}
// Now check why loop ended
if (ferror(fp)) {
    // I/O error
} else {
    // EOF reached normally
}
```

---

# Part IV: Preprocessor

---

## 12. Preprocessor Directives

### Macros

```c
// Object-like macro
#define PI 3.14159
#define MAX_SIZE 1024

// Function-like macro
#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define SQUARE(x) ((x) * (x))

// Parentheses are critical!
#define BAD_SQUARE(x) x * x
BAD_SQUARE(1 + 2);  // 1 + 2 * 1 + 2 = 5, not 9!

// Multi-line macro
#define SWAP(a, b) do { \
    typeof(a) temp = (a); \
    (a) = (b); \
    (b) = temp; \
} while (0)

// Stringification
#define STRINGIFY(x) #x
STRINGIFY(hello);  // "hello"

// Token pasting
#define CONCAT(a, b) a##b
CONCAT(var, 1);  // var1
```

### Conditional Compilation

```c
#if CONDITION
    // ...
#elif OTHER_CONDITION
    // ...
#else
    // ...
#endif

#ifdef DEBUG
    #define LOG(msg) printf("DEBUG: %s\n", msg)
#else
    #define LOG(msg)
#endif

#ifndef HEADER_H
#define HEADER_H
    // Header contents
#endif

// Or modern #pragma once
#pragma once
```

### Predefined Macros

```c
__FILE__      // Current file name
__LINE__      // Current line number
__func__      // Current function name (C99)
__DATE__      // Compilation date
__TIME__      // Compilation time
__STDC__      // 1 if standard C
__STDC_VERSION__  // C standard version (199901L for C99)

// Debug macro example
#define DEBUG_LOG(fmt, ...) \
    fprintf(stderr, "[%s:%d] " fmt "\n", __FILE__, __LINE__, ##__VA_ARGS__)
```

### Include Guards

```c
// myheader.h
#ifndef MYHEADER_H
#define MYHEADER_H

// Declarations...

#endif // MYHEADER_H

// Or simpler (non-standard but widely supported)
#pragma once
```

### System-Specific Code

```c
#ifdef _WIN32
    #include <windows.h>
    void platform_sleep(int ms) { Sleep(ms); }
#elif defined(__linux__)
    #include <unistd.h>
    void platform_sleep(int ms) { usleep(ms * 1000); }
#elif defined(__APPLE__)
    #include <unistd.h>
    void platform_sleep(int ms) { usleep(ms * 1000); }
#else
    #error "Unsupported platform"
#endif
```

---

# Part V: Advanced Topics

---

## 13. Common Idioms and Patterns

### Error Handling

```c
// Return error codes
#define SUCCESS 0
#define ERR_INVALID_INPUT -1
#define ERR_NO_MEMORY -2

int process(const char *input, int *result) {
    if (input == NULL || result == NULL) {
        return ERR_INVALID_INPUT;
    }
    
    char *buffer = malloc(100);
    if (buffer == NULL) {
        return ERR_NO_MEMORY;
    }
    
    // Process...
    
    free(buffer);
    return SUCCESS;
}

// Using errno
#include <errno.h>

FILE *fp = fopen("file.txt", "r");
if (fp == NULL) {
    fprintf(stderr, "Error: %s\n", strerror(errno));
    return -1;
}
```

### Cleanup Pattern

```c
int complex_function() {
    int result = -1;
    FILE *fp = NULL;
    char *buffer = NULL;
    
    fp = fopen("file.txt", "r");
    if (fp == NULL) goto cleanup;
    
    buffer = malloc(1024);
    if (buffer == NULL) goto cleanup;
    
    // Do work...
    result = 0;
    
cleanup:
    free(buffer);
    if (fp) fclose(fp);
    return result;
}
```

### Opaque Pointers

```c
// In header (public interface)
typedef struct Handle* Handle;

Handle handle_create(void);
void handle_destroy(Handle h);
int handle_process(Handle h, int data);

// In source (implementation hidden)
struct Handle {
    int internal_data;
    void *private_state;
};

Handle handle_create(void) {
    Handle h = malloc(sizeof(struct Handle));
    // Initialize...
    return h;
}
```

### Container_of Pattern

```c
// Used in Linux kernel, embedded lists
#define container_of(ptr, type, member) \
    ((type *)((char *)(ptr) - offsetof(type, member)))

struct list_node {
    struct list_node *next;
    struct list_node *prev;
};

struct person {
    char name[50];
    int age;
    struct list_node node;  // Embedded in struct
};

// From node pointer, get person pointer
struct list_node *n = /* ... */;
struct person *p = container_of(n, struct person, node);
```

---

## 14. Memory-Mapped I/O

```c
#include <sys/mman.h>
#include <fcntl.h>

int fd = open("file.txt", O_RDWR);
struct stat sb;
fstat(fd, &sb);

char *mapped = mmap(NULL, sb.st_size, PROT_READ | PROT_WRITE,
                    MAP_SHARED, fd, 0);
if (mapped == MAP_FAILED) {
    perror("mmap");
    close(fd);
    return -1;
}

// Access file as memory
for (int i = 0; i < sb.st_size; i++) {
    if (mapped[i] == 'a') {
        mapped[i] = 'A';
    }
}

// Sync changes to file
msync(mapped, sb.st_size, MS_SYNC);

munmap(mapped, sb.st_size);
close(fd);
```

---

## 15. Common Pitfalls

### Buffer Overflow

```c
// WRONG
char buffer[10];
strcpy(buffer, "This is too long!");  // Overflow!

// RIGHT
char buffer[10];
strncpy(buffer, src, sizeof(buffer) - 1);
buffer[sizeof(buffer) - 1] = '\0';

// Or use snprintf
snprintf(buffer, sizeof(buffer), "%s", src);
```

### Integer Overflow

```c
// Signed overflow is undefined behavior
int x = INT_MAX;
x++;  // UB!

// Check before addition
if (a > INT_MAX - b) {
    // Would overflow
}

// Check before multiplication
if (a != 0 && b > INT_MAX / a) {
    // Would overflow
}
```

### Dangling Pointers

```c
// WRONG
int *bad_pointer() {
    int x = 42;
    return &x;  // x out of scope after return!
}

// RIGHT
int *good_pointer() {
    int *x = malloc(sizeof(int));
    *x = 42;
    return x;  // Caller must free
}
```

### Undefined Behavior

```c
// Null pointer dereference
int *p = NULL;
*p = 5;  // UB

// Division by zero
int x = 5 / 0;  // UB

// Signed overflow
int max = INT_MAX + 1;  // UB

// Uninitialized variables
int x;
printf("%d", x);  // UB

// Sequence point violations
int i = 0;
i = i++;  // UB

// Array out of bounds
int arr[5];
arr[5] = 10;  // UB

// Misaligned access
char buf[10];
int *p = (int*)(buf + 1);  // Potentially UB
```

---

## 16. Build Process

### Compilation Stages

```
Source (.c) → Preprocessor → Translation Unit
           → Compiler → Assembly (.s)
           → Assembler → Object (.o)
           → Linker → Executable

gcc -E file.c > file.i    # Preprocess only
gcc -S file.c             # Compile to assembly
gcc -c file.c             # Compile to object
gcc file.o -o program     # Link to executable
```

### Makefiles

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -std=c11 -g
LDFLAGS =
TARGET = program
SRCS = main.c utils.c
OBJS = $(SRCS:.c=.o)

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f $(OBJS) $(TARGET)
```

### Useful Compiler Flags

```bash
# Warnings
-Wall           # Enable common warnings
-Wextra         # Extra warnings
-Werror         # Treat warnings as errors
-Wpedantic      # Strict ISO C compliance

# Optimization
-O0             # No optimization (default)
-O1             # Basic optimization
-O2             # Most optimizations
-O3             # Aggressive optimization
-Os             # Optimize for size
-Ofast          # -O3 + fast-math

# Debugging
-g              # Debug symbols
-fsanitize=address   # Address Sanitizer
-fsanitize=undefined # UBSan

# Standards
-std=c99        # C99 standard
-std=c11        # C11 standard
-std=c17        # C17 standard
```

---

## Cross-References

- [[02_Computer_Architecture]] - Memory layout, cache behavior
- [[04_Algorithms_Data_Structures]] - Implementing algorithms in C
- [[07_Operating_Systems]] - System calls, process management
- [[09_Cpp_Programming]] - C++ builds on C
