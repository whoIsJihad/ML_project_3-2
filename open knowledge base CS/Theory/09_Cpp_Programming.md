# C++ Programming

## Course Overview
**Depth:** University undergraduate + modern C++ proficiency  
**Time:** 3-4 hours focused reading  
**Prerequisites:** C programming knowledge

---

# Part I: C++ Fundamentals

---

## 1. From C to C++

### Key Differences from C

```cpp
// Headers: <cstdio> instead of <stdio.h>
#include <iostream>    // Preferred for I/O
#include <string>      // std::string
#include <vector>      // std::vector

// Namespaces
using namespace std;   // Convenient but avoid in headers
std::cout << "Hello";  // Explicit (preferred)

// bool is a built-in type
bool flag = true;

// References
int x = 10;
int& ref = x;    // Reference to x
ref = 20;        // x is now 20

// Function overloading
int add(int a, int b);
double add(double a, double b);

// Default arguments
void print(int n = 10);

// const correctness
const int MAX = 100;   // Preferred over #define

// nullptr instead of NULL
int* ptr = nullptr;
```

### Input/Output

```cpp
#include <iostream>
#include <iomanip>

int main() {
    // Output
    std::cout << "Hello, " << "World!" << std::endl;
    std::cout << "Number: " << 42 << '\n';
    
    // Input
    int n;
    std::cout << "Enter a number: ";
    std::cin >> n;
    
    std::string name;
    std::cout << "Enter name: ";
    std::cin >> name;           // Reads one word
    std::getline(std::cin, name); // Reads whole line
    
    // Formatting
    std::cout << std::setw(10) << std::setfill('0') << 42 << '\n';
    std::cout << std::fixed << std::setprecision(2) << 3.14159 << '\n';
    std::cout << std::hex << 255 << '\n';  // ff
    
    return 0;
}
```

### Memory Management

```cpp
// C-style (avoid)
int* arr = (int*)malloc(10 * sizeof(int));
free(arr);

// C++ style
int* p = new int(42);        // Single value
int* arr = new int[10];      // Array
delete p;                     // Single value
delete[] arr;                 // Array - must match new[]!

// Modern C++: Smart pointers (preferred)
#include <memory>
auto ptr = std::make_unique<int>(42);  // Automatically deleted
auto shared = std::make_shared<int>(100);  // Reference counted
```

---

## 2. References

### Reference Basics

```cpp
int x = 10;
int& ref = x;    // ref is alias for x
ref = 20;        // x is now 20

int* ptr = &x;   // Pointer to x
*ptr = 30;       // x is now 30

// Key differences:
// - References must be initialized
// - References cannot be null
// - References cannot be reseated
// - No "reference arithmetic"
```

### Pass by Reference

```cpp
// Pass by value (copy)
void increment_copy(int n) {
    n++;  // Modifies copy only
}

// Pass by reference
void increment_ref(int& n) {
    n++;  // Modifies original
}

// Pass by const reference (read-only, no copy)
void print(const std::string& s) {
    std::cout << s << '\n';
    // s = "modified";  // Error: s is const
}

int x = 10;
increment_ref(x);  // x is now 11
```

### Lvalue vs Rvalue

```cpp
int x = 10;        // x is lvalue
int& lref = x;     // Lvalue reference

// int& lref2 = 10;  // Error: can't bind lvalue ref to rvalue

const int& cref = 10;  // OK: const ref extends lifetime

// C++11 rvalue references
int&& rref = 10;       // rvalue reference
int&& rref2 = x + 5;   // OK: expression is rvalue

// Lvalue: Has identity, can take address
// Rvalue: Temporary, no persistent identity
```

---

## 3. Strings

### std::string

```cpp
#include <string>

std::string s1 = "Hello";
std::string s2("World");
std::string s3(5, 'a');      // "aaaaa"
std::string s4 = s1 + " " + s2;  // Concatenation

// Access
char c = s1[0];              // No bounds checking (faster)
char d = s1.at(0);           // Bounds checking (throws)

// Properties
size_t len = s1.length();    // or size()
bool empty = s1.empty();

// Modification
s1.append(" there");
s1.insert(5, " world");
s1.erase(5, 6);
s1.replace(0, 5, "Hi");
s1.clear();

// Searching
size_t pos = s1.find("lo");
if (pos != std::string::npos) {
    // Found at position pos
}

// Substrings
std::string sub = s1.substr(0, 5);  // First 5 chars

// Comparison
if (s1 == s2) { }
if (s1 < s2) { }  // Lexicographic
int cmp = s1.compare(s2);
```

### String Conversion

```cpp
// String to number
int n = std::stoi("42");
long l = std::stol("123456789");
double d = std::stod("3.14");

// Number to string
std::string s = std::to_string(42);
std::string f = std::to_string(3.14);

// C-string interop
std::string cpp_str = "Hello";
const char* c_str = cpp_str.c_str();
std::string from_c = std::string(c_str);
```

### string_view (C++17)

```cpp
#include <string_view>

// Non-owning view of string data
void process(std::string_view sv) {
    // Efficient: No copy, just pointer + size
    std::cout << sv << '\n';
}

std::string s = "Hello";
process(s);        // Works with string
process("World");  // Works with literal

std::string_view sv = s;
sv.remove_prefix(2);  // "llo" (doesn't modify s)
```

---

# Part II: Object-Oriented Programming

---

## 4. Classes

### Class Basics

```cpp
class Rectangle {
private:                  // Access specifier
    double width;
    double height;

public:
    // Constructor
    Rectangle(double w, double h) : width(w), height(h) {}
    
    // Default constructor
    Rectangle() : width(0), height(0) {}
    
    // Member functions
    double area() const {    // const = doesn't modify object
        return width * height;
    }
    
    double perimeter() const {
        return 2 * (width + height);
    }
    
    // Getters and setters
    double getWidth() const { return width; }
    void setWidth(double w) { width = w; }
};

// Usage
Rectangle r1(10, 20);
Rectangle r2;
double a = r1.area();
```

### Member Initializer List

```cpp
class Example {
    int a;
    const int b;
    int& c;
    std::string name;

public:
    // Initializer list - REQUIRED for const/ref members
    Example(int val, int& ref, const std::string& n)
        : a(val), b(100), c(ref), name(n)  // Order matches declaration
    {
        // Constructor body
    }
};

// Why use initializer list?
// 1. Required for const, reference, base classes
// 2. Direct initialization (more efficient)
// 3. Some types have no default constructor
```

### Special Member Functions (Rule of Zero/Three/Five)

```cpp
class Resource {
    int* data;
    size_t size;

public:
    // Constructor
    Resource(size_t n) : data(new int[n]), size(n) {}
    
    // Destructor
    ~Resource() {
        delete[] data;
    }
    
    // Copy constructor
    Resource(const Resource& other) 
        : data(new int[other.size]), size(other.size) {
        std::copy(other.data, other.data + size, data);
    }
    
    // Copy assignment operator
    Resource& operator=(const Resource& other) {
        if (this != &other) {  // Self-assignment check
            delete[] data;
            size = other.size;
            data = new int[size];
            std::copy(other.data, other.data + size, data);
        }
        return *this;
    }
    
    // Move constructor (C++11)
    Resource(Resource&& other) noexcept
        : data(other.data), size(other.size) {
        other.data = nullptr;
        other.size = 0;
    }
    
    // Move assignment operator (C++11)
    Resource& operator=(Resource&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }
};

// Rule of Zero: If you don't manage resources, don't define any
// Rule of Three: If you define destructor, copy ctor, or copy assignment,
//                define all three
// Rule of Five: Also define move constructor and move assignment
```

### Static Members

```cpp
class Counter {
    static int count;     // Shared by all instances
    int id;

public:
    Counter() : id(++count) {}
    
    static int getCount() {    // Static member function
        // Cannot access non-static members!
        return count;
    }
};

// Must define static member outside class
int Counter::count = 0;

// Usage
Counter c1, c2, c3;
std::cout << Counter::getCount();  // 3
```

### Friend Functions and Classes

```cpp
class Box {
    double width;
    friend void printWidth(const Box& b);  // Friend function
    friend class Inspector;                 // Friend class
};

void printWidth(const Box& b) {
    std::cout << b.width;  // Can access private
}

class Inspector {
public:
    void inspect(const Box& b) {
        std::cout << b.width;  // Can access private
    }
};
```

---

## 5. Operator Overloading

### Arithmetic Operators

```cpp
class Complex {
    double real, imag;

public:
    Complex(double r = 0, double i = 0) : real(r), imag(i) {}
    
    // Member operator+
    Complex operator+(const Complex& other) const {
        return Complex(real + other.real, imag + other.imag);
    }
    
    // Non-member (friend) for symmetry
    friend Complex operator-(const Complex& a, const Complex& b) {
        return Complex(a.real - b.real, a.imag - b.imag);
    }
    
    // Compound assignment
    Complex& operator+=(const Complex& other) {
        real += other.real;
        imag += other.imag;
        return *this;
    }
    
    // Unary minus
    Complex operator-() const {
        return Complex(-real, -imag);
    }
};
```

### Comparison Operators

```cpp
class Point {
    int x, y;

public:
    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }
    
    bool operator!=(const Point& other) const {
        return !(*this == other);
    }
    
    bool operator<(const Point& other) const {
        if (x != other.x) return x < other.x;
        return y < other.y;
    }
    
    // C++20 spaceship operator
    auto operator<=>(const Point& other) const = default;
};
```

### Stream Operators

```cpp
class Point {
    int x, y;

public:
    // Output
    friend std::ostream& operator<<(std::ostream& os, const Point& p) {
        return os << "(" << p.x << ", " << p.y << ")";
    }
    
    // Input
    friend std::istream& operator>>(std::istream& is, Point& p) {
        return is >> p.x >> p.y;
    }
};

Point p(3, 4);
std::cout << p << '\n';  // (3, 4)
std::cin >> p;
```

### Subscript and Function Call

```cpp
class Array {
    int* data;
    size_t size;

public:
    // Subscript operator
    int& operator[](size_t index) {
        return data[index];
    }
    
    const int& operator[](size_t index) const {
        return data[index];
    }
};

// Function call operator (functor)
class Multiplier {
    int factor;

public:
    Multiplier(int f) : factor(f) {}
    
    int operator()(int x) const {
        return x * factor;
    }
};

Multiplier times3(3);
int result = times3(5);  // 15
```

### Type Conversion

```cpp
class Fraction {
    int num, denom;

public:
    // Conversion to double
    explicit operator double() const {
        return static_cast<double>(num) / denom;
    }
    
    // Conversion to bool
    explicit operator bool() const {
        return num != 0;
    }
};

Fraction f(3, 4);
double d = static_cast<double>(f);  // 0.75 (explicit required)
if (f) { }  // explicit allows in boolean context
```

---

## 6. Inheritance

### Basic Inheritance

```cpp
class Animal {
protected:
    std::string name;

public:
    Animal(const std::string& n) : name(n) {}
    
    void eat() {
        std::cout << name << " is eating\n";
    }
    
    virtual void speak() {  // Virtual for polymorphism
        std::cout << name << " makes a sound\n";
    }
    
    virtual ~Animal() = default;  // Virtual destructor!
};

class Dog : public Animal {
public:
    Dog(const std::string& n) : Animal(n) {}
    
    void speak() override {  // override keyword (C++11)
        std::cout << name << " barks: Woof!\n";
    }
    
    void fetch() {
        std::cout << name << " fetches the ball\n";
    }
};
```

### Access Specifiers

```cpp
class Base {
public:
    int pub;
protected:
    int prot;
private:
    int priv;
};

class PublicDerived : public Base {
    // pub is public
    // prot is protected
    // priv is not accessible
};

class ProtectedDerived : protected Base {
    // pub is protected
    // prot is protected
    // priv is not accessible
};

class PrivateDerived : private Base {
    // pub is private
    // prot is private
    // priv is not accessible
};
```

### Virtual Functions and Polymorphism

```cpp
class Shape {
public:
    virtual double area() const = 0;  // Pure virtual (abstract)
    virtual ~Shape() = default;
};

class Circle : public Shape {
    double radius;

public:
    Circle(double r) : radius(r) {}
    
    double area() const override {
        return 3.14159 * radius * radius;
    }
};

class Rectangle : public Shape {
    double width, height;

public:
    Rectangle(double w, double h) : width(w), height(h) {}
    
    double area() const override {
        return width * height;
    }
};

// Polymorphism in action
void printArea(const Shape& shape) {
    std::cout << "Area: " << shape.area() << '\n';
}

Circle c(5);
Rectangle r(4, 6);
printArea(c);  // Calls Circle::area()
printArea(r);  // Calls Rectangle::area()
```

### Virtual Destructor

```cpp
class Base {
public:
    virtual ~Base() {
        std::cout << "Base destructor\n";
    }
};

class Derived : public Base {
    int* data;

public:
    Derived() : data(new int[100]) {}
    
    ~Derived() override {
        delete[] data;
        std::cout << "Derived destructor\n";
    }
};

Base* ptr = new Derived();
delete ptr;  // Without virtual: Only Base destructor called (memory leak!)
             // With virtual: Derived then Base destructor called
```

### Multiple Inheritance

```cpp
class A {
public:
    void fromA() {}
};

class B {
public:
    void fromB() {}
};

class C : public A, public B {
    // Inherits from both A and B
};

// Diamond problem
class Animal { };
class Mammal : virtual public Animal { };  // Virtual inheritance
class Bird : virtual public Animal { };    // Virtual inheritance
class Bat : public Mammal, public Bird {   // Only one Animal subobject
};
```

---

# Part III: Templates

---

## 7. Function Templates

```cpp
template<typename T>
T maximum(T a, T b) {
    return (a > b) ? a : b;
}

int m1 = maximum(3, 5);           // T = int (deduced)
double m2 = maximum(3.5, 2.5);    // T = double (deduced)
int m3 = maximum<int>(3.5, 2);    // T = int (explicit)

// Multiple template parameters
template<typename T, typename U>
auto add(T a, U b) -> decltype(a + b) {
    return a + b;
}

// C++14: Simplified return type
template<typename T, typename U>
auto add(T a, U b) {
    return a + b;
}

// Non-type template parameters
template<typename T, size_t N>
size_t arraySize(T (&arr)[N]) {
    return N;
}

int arr[10];
size_t n = arraySize(arr);  // N = 10
```

### Template Specialization

```cpp
// Primary template
template<typename T>
class Container {
    T data;
public:
    void print() { std::cout << data << '\n'; }
};

// Full specialization for bool
template<>
class Container<bool> {
    bool data;
public:
    void print() { std::cout << (data ? "true" : "false") << '\n'; }
};

// Partial specialization for pointers
template<typename T>
class Container<T*> {
    T* data;
public:
    void print() { std::cout << *data << '\n'; }
};
```

---

## 8. Class Templates

```cpp
template<typename T>
class Stack {
    std::vector<T> data;

public:
    void push(const T& item) {
        data.push_back(item);
    }
    
    T pop() {
        T item = data.back();
        data.pop_back();
        return item;
    }
    
    bool empty() const {
        return data.empty();
    }
};

// Usage
Stack<int> intStack;
Stack<std::string> stringStack;

intStack.push(42);
stringStack.push("Hello");

// Template with default parameter
template<typename T, typename Container = std::vector<T>>
class MyStack {
    Container data;
    // ...
};

MyStack<int> s1;                         // Uses vector
MyStack<int, std::deque<int>> s2;        // Uses deque
```

### Variadic Templates (C++11)

```cpp
// Base case
void print() {
    std::cout << '\n';
}

// Recursive case
template<typename T, typename... Args>
void print(T first, Args... rest) {
    std::cout << first << ' ';
    print(rest...);
}

print(1, 2.5, "hello", 'a');  // 1 2.5 hello a

// Fold expressions (C++17)
template<typename... Args>
auto sum(Args... args) {
    return (args + ...);  // Right fold
}

template<typename... Args>
void printAll(Args... args) {
    (std::cout << ... << args) << '\n';  // Left fold with <<
}
```

---

# Part IV: Standard Template Library (STL)

---

## 9. Containers

### Sequence Containers

```cpp
#include <vector>
#include <deque>
#include <list>
#include <array>
#include <forward_list>

// vector - Dynamic array
std::vector<int> v = {1, 2, 3, 4, 5};
v.push_back(6);
v.pop_back();
v[0] = 10;
v.at(1) = 20;              // Bounds checking
v.insert(v.begin() + 2, 100);
v.erase(v.begin());
v.resize(10);
v.reserve(100);            // Pre-allocate capacity

// array - Fixed size (C++11)
std::array<int, 5> arr = {1, 2, 3, 4, 5};
arr[0] = 10;
constexpr size_t size = arr.size();

// deque - Double-ended queue
std::deque<int> d;
d.push_front(1);
d.push_back(2);
d.pop_front();

// list - Doubly linked list
std::list<int> lst = {1, 2, 3};
lst.push_front(0);
lst.push_back(4);
lst.sort();
lst.reverse();
lst.unique();

// forward_list - Singly linked list (C++11)
std::forward_list<int> fl = {1, 2, 3};
fl.push_front(0);
fl.insert_after(fl.begin(), 5);
```

### Associative Containers

```cpp
#include <set>
#include <map>

// set - Ordered unique elements
std::set<int> s = {3, 1, 4, 1, 5};  // {1, 3, 4, 5}
s.insert(2);
s.erase(4);
bool found = s.count(3);  // 0 or 1
auto it = s.find(3);

// multiset - Ordered, duplicates allowed
std::multiset<int> ms = {1, 1, 2, 2, 3};

// map - Ordered key-value pairs
std::map<std::string, int> ages;
ages["Alice"] = 30;
ages["Bob"] = 25;
ages.insert({"Charlie", 35});
ages.emplace("Dave", 40);

for (const auto& [name, age] : ages) {  // C++17 structured bindings
    std::cout << name << ": " << age << '\n';
}

// multimap - Duplicates keys allowed
std::multimap<std::string, int> grades;
grades.insert({"Alice", 85});
grades.insert({"Alice", 90});
```

### Unordered Containers (C++11)

```cpp
#include <unordered_set>
#include <unordered_map>

// unordered_set - Hash set
std::unordered_set<int> us = {3, 1, 4, 1, 5};

// unordered_map - Hash map
std::unordered_map<std::string, int> um;
um["key"] = 100;
um.insert({"key2", 200});

// O(1) average, O(n) worst case (vs O(log n) for ordered)
```

### Container Adaptors

```cpp
#include <stack>
#include <queue>

// stack (LIFO)
std::stack<int> stk;
stk.push(1);
stk.push(2);
int top = stk.top();  // 2
stk.pop();

// queue (FIFO)
std::queue<int> q;
q.push(1);
q.push(2);
int front = q.front();  // 1
int back = q.back();    // 2
q.pop();                // Removes front

// priority_queue (max heap)
std::priority_queue<int> pq;
pq.push(3);
pq.push(1);
pq.push(4);
int max = pq.top();  // 4
pq.pop();

// min heap
std::priority_queue<int, std::vector<int>, std::greater<int>> minPQ;
```

---

## 10. Iterators

### Iterator Types

```cpp
// Input iterator: Read forward once
// Output iterator: Write forward once
// Forward iterator: Read/write forward, multiple passes
// Bidirectional iterator: Forward + backward
// Random access iterator: Bidirectional + jump anywhere

std::vector<int> v = {1, 2, 3, 4, 5};

// Common usage
for (auto it = v.begin(); it != v.end(); ++it) {
    std::cout << *it << ' ';
}

// Reverse iteration
for (auto it = v.rbegin(); it != v.rend(); ++it) {
    std::cout << *it << ' ';
}

// Const iterators
for (auto it = v.cbegin(); it != v.cend(); ++it) {
    // *it = 10;  // Error: const iterator
}

// Iterator arithmetic (random access)
auto it = v.begin();
it += 3;               // Jump forward
auto diff = v.end() - v.begin();  // Distance
```

### Iterator Functions

```cpp
#include <iterator>

std::vector<int> v = {1, 2, 3, 4, 5};

std::advance(it, 3);           // Move forward 3
auto dist = std::distance(v.begin(), v.end());  // 5
auto nxt = std::next(v.begin(), 2);  // Iterator to [2]
auto prv = std::prev(v.end());       // Iterator to [4]

// Insert iterators
std::vector<int> dest;
std::copy(v.begin(), v.end(), std::back_inserter(dest));
```

---

## 11. Algorithms

```cpp
#include <algorithm>
#include <numeric>

std::vector<int> v = {5, 2, 8, 1, 9, 3, 7, 4, 6};

// Sorting
std::sort(v.begin(), v.end());
std::sort(v.begin(), v.end(), std::greater<int>());

// Custom comparator
std::sort(v.begin(), v.end(), [](int a, int b) {
    return a > b;  // Descending
});

// Searching (sorted)
bool found = std::binary_search(v.begin(), v.end(), 5);
auto lb = std::lower_bound(v.begin(), v.end(), 5);
auto ub = std::upper_bound(v.begin(), v.end(), 5);

// Searching (unsorted)
auto it = std::find(v.begin(), v.end(), 5);
auto it2 = std::find_if(v.begin(), v.end(), [](int x) {
    return x > 5;
});

// Count
int cnt = std::count(v.begin(), v.end(), 5);
int cnt2 = std::count_if(v.begin(), v.end(), [](int x) {
    return x % 2 == 0;
});

// Transform
std::transform(v.begin(), v.end(), v.begin(), [](int x) {
    return x * 2;
});

// Accumulate
int sum = std::accumulate(v.begin(), v.end(), 0);
int product = std::accumulate(v.begin(), v.end(), 1, std::multiplies<int>());

// Min/Max
auto minIt = std::min_element(v.begin(), v.end());
auto maxIt = std::max_element(v.begin(), v.end());
auto [minIt2, maxIt2] = std::minmax_element(v.begin(), v.end());

// Fill
std::fill(v.begin(), v.end(), 0);
std::fill_n(v.begin(), 5, 1);

// Generate
std::generate(v.begin(), v.end(), []() { return rand() % 100; });

// Remove (doesn't actually remove, returns new end)
auto newEnd = std::remove(v.begin(), v.end(), 5);
v.erase(newEnd, v.end());  // Actually remove

// Remove-erase idiom
v.erase(std::remove_if(v.begin(), v.end(), [](int x) {
    return x < 5;
}), v.end());

// Unique
std::sort(v.begin(), v.end());
auto last = std::unique(v.begin(), v.end());
v.erase(last, v.end());

// Reverse
std::reverse(v.begin(), v.end());

// Rotate
std::rotate(v.begin(), v.begin() + 3, v.end());

// Partial sort
std::partial_sort(v.begin(), v.begin() + 5, v.end());

// Nth element
std::nth_element(v.begin(), v.begin() + v.size()/2, v.end());

// Partition
std::partition(v.begin(), v.end(), [](int x) { return x % 2 == 0; });

// Heap
std::make_heap(v.begin(), v.end());
std::push_heap(v.begin(), v.end());
std::pop_heap(v.begin(), v.end());
std::sort_heap(v.begin(), v.end());

// All/Any/None
bool allPositive = std::all_of(v.begin(), v.end(), [](int x) { return x > 0; });
bool anyEven = std::any_of(v.begin(), v.end(), [](int x) { return x % 2 == 0; });
bool noneNeg = std::none_of(v.begin(), v.end(), [](int x) { return x < 0; });

// Copy
std::vector<int> dest(v.size());
std::copy(v.begin(), v.end(), dest.begin());
std::copy_if(v.begin(), v.end(), std::back_inserter(dest), [](int x) {
    return x > 0;
});
```

---

# Part V: Modern C++ Features

---

## 12. Move Semantics and Perfect Forwarding

### Move Semantics

```cpp
class Buffer {
    int* data;
    size_t size;

public:
    Buffer(size_t n) : data(new int[n]), size(n) {
        std::cout << "Constructed\n";
    }
    
    ~Buffer() {
        delete[] data;
    }
    
    // Copy constructor (expensive)
    Buffer(const Buffer& other) : data(new int[other.size]), size(other.size) {
        std::copy(other.data, other.data + size, data);
        std::cout << "Copy constructed\n";
    }
    
    // Move constructor (cheap)
    Buffer(Buffer&& other) noexcept : data(other.data), size(other.size) {
        other.data = nullptr;
        other.size = 0;
        std::cout << "Move constructed\n";
    }
    
    // Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        std::cout << "Move assigned\n";
        return *this;
    }
};

Buffer createBuffer() {
    Buffer b(1000);
    return b;  // Move (or RVO)
}

Buffer b1(1000);
Buffer b2 = std::move(b1);  // Explicit move
```

### std::move and std::forward

```cpp
// std::move: Cast to rvalue reference
int x = 5;
int&& rref = std::move(x);  // x is now "moved from" (valid but unspecified)

// std::forward: Perfect forwarding
template<typename T>
void wrapper(T&& arg) {
    // Without forward: arg is lvalue (has name)
    // With forward: preserves original value category
    actual_function(std::forward<T>(arg));
}

// Universal/forwarding reference
template<typename T>
void process(T&& t) {  // T&& with template = forwarding reference
    // If passed lvalue: T = T&, T&& & = T&
    // If passed rvalue: T = T, T&& = T&&
}
```

---

## 13. Smart Pointers

```cpp
#include <memory>

// unique_ptr: Exclusive ownership
std::unique_ptr<int> p1 = std::make_unique<int>(42);
std::cout << *p1 << '\n';  // 42

// std::unique_ptr<int> p2 = p1;  // Error: cannot copy
std::unique_ptr<int> p2 = std::move(p1);  // OK: move ownership
// p1 is now null

// unique_ptr for arrays
auto arr = std::make_unique<int[]>(10);
arr[0] = 100;

// shared_ptr: Reference counting
std::shared_ptr<int> s1 = std::make_shared<int>(42);
std::shared_ptr<int> s2 = s1;  // OK: shared ownership
std::cout << s1.use_count() << '\n';  // 2

// weak_ptr: Non-owning reference to shared_ptr
std::weak_ptr<int> w = s1;
if (auto locked = w.lock()) {
    std::cout << *locked << '\n';  // 42
}

// Custom deleters
auto deleter = [](int* p) {
    std::cout << "Deleting\n";
    delete p;
};
std::unique_ptr<int, decltype(deleter)> p3(new int(5), deleter);
```

### Smart Pointer Guidelines

```cpp
// Factory functions: Return unique_ptr
std::unique_ptr<Widget> createWidget() {
    return std::make_unique<Widget>();
}

// Transfer ownership: Pass unique_ptr by value
void consume(std::unique_ptr<Widget> w) {
    // Takes ownership
}

// Observe only: Pass raw pointer or reference
void observe(const Widget* w);  // May be null
void observe(const Widget& w); // Never null

// Share ownership: Pass shared_ptr by value
void share(std::shared_ptr<Widget> w) {
    // Increments reference count
}

// Potential ownereship: Pass shared_ptr by const ref
void maybeShare(const std::shared_ptr<Widget>& w) {
    if (condition) {
        member = w;  // Only copies if needed
    }
}
```

---

## 14. Lambda Expressions

```cpp
// Basic lambda
auto add = [](int a, int b) { return a + b; };
int sum = add(3, 5);  // 8

// Capture by value
int x = 10;
auto f1 = [x]() { return x; };  // Copies x

// Capture by reference
auto f2 = [&x]() { x++; };  // References x
f2();  // x is now 11

// Capture all by value
auto f3 = [=]() { return x; };

// Capture all by reference
auto f4 = [&]() { x++; };

// Mixed capture
int y = 20;
auto f5 = [=, &y]() { y = x + 1; };  // x by value, y by reference

// Mutable lambda (modify captured by value)
auto f6 = [x]() mutable { return ++x; };

// Init capture (C++14)
auto ptr = std::make_unique<int>(10);
auto f7 = [p = std::move(ptr)]() { return *p; };

// Generic lambda (C++14)
auto generic = [](auto a, auto b) { return a + b; };
generic(1, 2);      // int
generic(1.5, 2.5);  // double

// Return type specification
auto f8 = [](int x) -> double { return x; };

// Immediately invoked
int result = [](int x) { return x * x; }(5);  // 25

// Lambda in STL
std::vector<int> v = {5, 2, 8, 1, 9};
std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });
```

---

## 15. Type Deduction and auto

```cpp
// auto
auto x = 42;          // int
auto y = 3.14;        // double
auto s = "hello";     // const char*
auto& ref = x;        // int&
const auto& cref = x; // const int&
auto* ptr = &x;       // int*

// Range-based for with auto
std::vector<std::string> words = {"hello", "world"};
for (const auto& word : words) {  // Avoids copy
    std::cout << word << '\n';
}

// decltype
int a = 5;
decltype(a) b = 10;   // int
decltype((a)) c = a;  // int& (expression in parentheses)

// decltype(auto) (C++14)
template<typename T>
decltype(auto) forward_value(T&& t) {
    return std::forward<T>(t);
}

// Trailing return type
template<typename T, typename U>
auto multiply(T t, U u) -> decltype(t * u) {
    return t * u;
}

// Structured bindings (C++17)
std::pair<int, std::string> p = {1, "one"};
auto [num, str] = p;

std::map<std::string, int> m = {{"a", 1}, {"b", 2}};
for (const auto& [key, value] : m) {
    std::cout << key << ": " << value << '\n';
}
```

---

## 16. constexpr and Compile-Time Computation

```cpp
// constexpr variables
constexpr int SIZE = 100;
constexpr double PI = 3.14159265359;

// constexpr functions
constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}

constexpr int fact5 = factorial(5);  // Computed at compile time

// constexpr if (C++17)
template<typename T>
auto process(T t) {
    if constexpr (std::is_integral_v<T>) {
        return t * 2;
    } else {
        return t + t;
    }
}

// constexpr class (C++14+)
class Point {
    double x, y;
public:
    constexpr Point(double x, double y) : x(x), y(y) {}
    constexpr double getX() const { return x; }
    constexpr double getY() const { return y; }
};

constexpr Point p(3.0, 4.0);
constexpr double px = p.getX();

// consteval (C++20): Must be evaluated at compile time
consteval int must_compile_time(int x) {
    return x * x;
}
```

---

## 17. RAII and Resource Management

### RAII Principle

```cpp
// Resource Acquisition Is Initialization
// - Acquire resource in constructor
// - Release resource in destructor
// - Guarantees cleanup even with exceptions

class FileHandle {
    FILE* fp;

public:
    FileHandle(const char* filename, const char* mode) 
        : fp(fopen(filename, mode)) {
        if (!fp) throw std::runtime_error("Cannot open file");
    }
    
    ~FileHandle() {
        if (fp) fclose(fp);
    }
    
    // Non-copyable
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;
    
    // Movable
    FileHandle(FileHandle&& other) noexcept : fp(other.fp) {
        other.fp = nullptr;
    }
    
    FILE* get() const { return fp; }
};

void processFile() {
    FileHandle f("data.txt", "r");
    // Use f...
}  // Automatically closed, even if exception thrown
```

### Standard RAII Types

```cpp
// Smart pointers
std::unique_ptr<Widget> widget;
std::shared_ptr<Resource> resource;

// Containers (manage their memory)
std::vector<int> v;
std::string s;

// Lock guard
std::mutex mtx;
{
    std::lock_guard<std::mutex> lock(mtx);
    // Critical section
}  // Automatically unlocked

// Scoped lock (C++17)
std::mutex m1, m2;
{
    std::scoped_lock lock(m1, m2);  // Locks both, avoids deadlock
}

// Unique lock (more flexible)
std::unique_lock<std::mutex> lock(mtx, std::defer_lock);
lock.lock();    // Manual lock
lock.unlock();  // Manual unlock
```

---

## 18. Exceptions

```cpp
#include <stdexcept>

// Throwing exceptions
void validate(int x) {
    if (x < 0) {
        throw std::invalid_argument("x must be non-negative");
    }
    if (x > 100) {
        throw std::out_of_range("x must be <= 100");
    }
}

// Catching exceptions
try {
    validate(-5);
} catch (const std::invalid_argument& e) {
    std::cerr << "Invalid argument: " << e.what() << '\n';
} catch (const std::exception& e) {
    std::cerr << "Error: " << e.what() << '\n';
} catch (...) {
    std::cerr << "Unknown error\n";
}

// Exception hierarchy
// std::exception
// ├── std::logic_error
// │   ├── std::invalid_argument
// │   ├── std::domain_error
// │   ├── std::length_error
// │   └── std::out_of_range
// └── std::runtime_error
//     ├── std::range_error
//     ├── std::overflow_error
//     └── std::underflow_error

// Custom exception
class MyException : public std::runtime_error {
public:
    MyException(const std::string& msg) : std::runtime_error(msg) {}
};

// noexcept specifier
void safe_function() noexcept {
    // Must not throw (std::terminate if it does)
}

void maybe_throws() noexcept(false) {
    // May throw
}
```

---

## 19. Concurrency (C++11)

```cpp
#include <thread>
#include <mutex>
#include <condition_variable>
#include <future>
#include <atomic>

// Basic thread
void worker(int id) {
    std::cout << "Worker " << id << '\n';
}

std::thread t1(worker, 1);
std::thread t2(worker, 2);
t1.join();   // Wait for completion
t2.join();

// Lambda thread
std::thread t3([]() {
    std::cout << "Lambda thread\n";
});
t3.detach();  // Don't wait, run in background

// Mutex
std::mutex mtx;
int shared_data = 0;

void increment() {
    std::lock_guard<std::mutex> lock(mtx);
    shared_data++;
}

// Condition variable
std::condition_variable cv;
bool ready = false;

void producer() {
    {
        std::lock_guard<std::mutex> lock(mtx);
        ready = true;
    }
    cv.notify_one();
}

void consumer() {
    std::unique_lock<std::mutex> lock(mtx);
    cv.wait(lock, []{ return ready; });
    // Process...
}

// Atomic
std::atomic<int> counter{0};
counter++;           // Thread-safe
counter.load();      // Read
counter.store(10);   // Write

// Futures and promises
std::future<int> fut = std::async(std::launch::async, []() {
    return 42;
});
int result = fut.get();  // Blocks until ready

// Thread-safe initialization
void init() {
    static std::once_flag flag;
    std::call_once(flag, []() {
        // Initialize once
    });
}
```

---

## Cross-References

- [[04_Algorithms_Data_Structures]] - STL implementations
- [[07_Operating_Systems]] - Threads, synchronization
- [[08_C_Programming]] - C foundation
