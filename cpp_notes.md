### Some things I should remember about C/C++

Info mainly from 109 video C++ playlist from The Cherno:
https://www.youtube.com/watch?v=18c3MTX0PK0&list=PLlrATfBNZ98dudnM48yfGUldqGD0S4FFb

Also added additional examples/comments/sections.

<details>
<summary>Preprocessor commands/macros</summary>
Preprocessor commands start with # and are processed before compilation. The preprocessor essentially does text manipulation on your source code.
Basically it does a find and replace, and it also can be with parameters, conditions etc. and get complicated quickly.

Common Preprocessor Commands
1. #pragma once - Header Guards
```cpp
// myheader.h
#pragma once  // Tells preprocessor: "Only include this file once per translation unit"

class MyClass {
    // Class definition...
};

// Without #pragma once, if this header is included multiple times,
// you'd get "redefinition" errors during compilation
```

Traditional alternative (still used):
```cpp
// myheader.h
#ifndef MYHEADER_H  // If not defined...
#define MYHEADER_H  // Define it now

class MyClass {
    // Class definition...
};

#endif // MYHEADER_H  // End of guard
```

2. `#include` - File Inclusion
```cpp
#include <iostream>    // System headers - compiler searches system paths
#include "myheader.h"  // Local headers - searches current directory first

// What happens:
// The preprocessor literally COPY-PASTES the entire content of iostream
// and myheader.h into this file before compilation
```

3. `#define` - Macros
```cpp
// Simple constants
#define MAX_CONNECTIONS 1000
#define BUFFER_SIZE 1500

// Macros with parameters (use cautiously!)
#define SQUARE(x) ((x) * (x))
#define MAX(a, b) ((a) > (b) ? (a) : (b))

int main() {
    int connections = MAX_CONNECTIONS;
    int buffer[BUFFER_SIZE];
    int squared = SQUARE(5);      // Becomes: ((5) * (5))
    int larger = MAX(10, 20);     // Becomes: ((10) > (20) ? (10) : (20))
}
```

4. `#ifdef` / `#ifndef` / `#endif` - Conditional Compilation
```cpp
#define DEBUG_MODE  // Comment this out to disable debug code

#ifdef DEBUG_MODE
    #define DEBUG_LOG(x) std::cout << "DEBUG: " << x << std::endl
#else
    #define DEBUG_LOG(x)  // Becomes empty - no code generated
#endif

int main() {
    DEBUG_LOG("Starting router...");  // Only compiled if DEBUG_MODE is defined
}
```

5. `#if` / `#elif` / `#else` - Conditional Compilation with Expressions
```cpp
#define VERSION 3

#if VERSION == 1
    #define PROTOCOL "HTTP/1.0"
#elif VERSION == 2
    #define PROTOCOL "HTTP/1.1"
#elif VERSION == 3
    #define PROTOCOL "HTTP/2.0"
#else
    #define PROTOCOL "UNKNOWN"
#endif
```

Key Takeaways
* Preprocessor runs before compilation - it's text substitution
* `#pragma` once prevents multiple inclusion of headers
* Use #define sparingly - prefer constexpr and templates in modern C++
* Conditional compilation (`#ifdef`, `#if`) is essential for cross-platform code
* Macros can be dangerous - use parentheses and prefer inline functions

</details>

<details>
<summary>Pointers and references</summary>

Pointer is a memory address. A simple example using `int nums[5]`:
```cpp
// Method 1: Array subscript (recommended)
nums[2] = 7;

// Method 2: Pointer arithmetic without cast
*(nums + 2) = 7;

// Method 3: Your way with unnecessary cast  
*(int*)(nums + 2) = 7;  // Same as above but verbose

// Method 4: Using address-of and dereference
*(&nums[0] + 2) = 7;
```

When Would You Need the Cast?
The cast is needed in some cases:

Case 1: void* Pointers
```cpp
void* buffer = malloc(100);
*(int*)((char*)buffer + 8) = 42;  // Need casts here!
```

Case 2: Byte-level Manipulation
```cpp
char data[100];
*(int*)(data + 10) = 0x12345678;  // Write 4 bytes as integer
```

`void*`  is a "pointer to anything" - it's a generic pointer type that can point to any data type, but doesn't know what type it's pointing to.
```cpp
void* ptr;  // Can point to ANYTHING - int, char, struct, etc.
```

It must be cast to a specific type to be used:
```cpp
int x = 10;
void* ptr = &x;

// Cast back to int* before using
int* int_ptr = (int*)ptr;
*int_ptr = 20;  // ✅ Now works!
cout << *int_ptr;  // Prints 20
```

It is a cool thing to use `nullptr` because:
Case 1: Uninitialized void* - Garbage Address
```cpp
void* ptr;  // ⚠️ DANGEROUS! Contains random garbage address

// If this garbage address happens to point to system memory:
// processPacket(packet_buffer);  // ❌ Could corrupt system!
```

Case 2: Initialized to nullptr - Safe
```cpp
void* ptr = nullptr;  // ✅ SAFE! Points to nothing (address 0)

// You can safely check if it's valid:
if (ptr == nullptr) {
    cout << "Pointer is not pointing to anything" << endl;
}
```

Reference is just a reference to a variable:
```cpp
void addOne(int& number) {  // number is a REFERENCE to startNumber
    number++;  // Modifies the original variable in main()
}

int main() {
    int startNumber = 5;
    addOne(startNumber);
    cout << startNumber << endl;  // Output: 6 (was modified!)
}
```


</details>

<details>
<summary><code>static</code> keyword</summary>

What happens with `static` in Header Files

When you have this:

```cpp
// config.h
static int s_var = 1;
static void foo() { cout << s_var << endl; }
```

And include it in multiple files:
```cpp
// main.cpp
#include "config.h"
int main() {
    s_var = 2;  // This modifies main.cpp's COPY of s_var
    foo();      // This calls main.cpp's COPY of foo()
}
```

```cpp
// other.cpp
#include "config.h"
void someFunction() {
    s_var = 5;  // This modifies other.cpp's SEPARATE COPY of s_var
    foo();      // This calls other.cpp's COPY of foo()
}
```

Each .cpp file gets its own separate copy of s_var and foo(). If we would print `s_var` address in main and other, we would get different addresses.
Memory Layout After Compilation:
```log
 main.cpp's world:
[main.cpp::s_var] = 2 (initially 1, then set to 2)
[main.cpp::foo()] - function that prints main.cpp's s_var

 other.cpp's world:
[other.cpp::s_var] = 5 (completely separate variable!)
[other.cpp::foo()] - function that prints other.cpp's s_var
```
Generally, it is recommended to use static keyword, so the variables and functions are copied over and not global - the safe way.

The interesting thing is when we have a situation, where in `config.h` we define a `static int s_var = 5`, and we include the `.h` file in `main.cpp`
```cpp
#include "config.h"

int s_var = 10;
int main() {
    cout << s_var << endl; // this will print 10
}
```

after preprocessing, we get this:
```cpp
static int s_var = 5;
int s_var = 10;
int main() {
    cout << s_var << endl; // this will print 10
}
```
`static` is trated as a different variable, so there is no compilation errors. But if we print the `s_var`, we will get the value of 10.


We can use the same variable everywhere (a globally defined variable in a header file) if we define variable without static:
```cpp
// config.h
int s_var = 1;
```

and refer to it as extern - meaning that this variable is defined in some other translation unit:
```cpp
#include "config.h"
extern s_var;
int main() {
    cout << s_var;
}
```
If some other function includes the header with `s_var` and prints the address, we would get the same address if `s_var` as in `main()`.
If we do not refer to `s_var` as `extern` and include it multiple cpp files, there will be a linking error because of multiple `s_var` definitions.
To solve this, we could:

Option 1: extern (Recommended)
```cpp
// config.h
extern int s_var;  // DECLARATION only (no memory allocated)

// config.cpp
int s_var = 5;     // DEFINITION (only once!)

// main.cpp
#include "config.h"
int main() {
    s_var = 10;  // Uses the shared s_var from config.cpp
}

// other.cpp
#include "config.h"
void someFunction() {
    s_var = 20;  // Uses the SAME shared s_var
}
```

Option 2: inline (C++17+)
```cpp
// config.h
inline int s_var = 5;  // inline allows multiple definitions

// main.cpp
#include "config.h"
int main() {
    s_var = 10;
}

// other.cpp
#include "config.h"
void someFunction() {
    s_var = 20;  // All use the same variable
}

// s_var shares the same memory address in main.cpp and other.cpp - a global variable
```

Option 3: static (But Creates Copies)
```cpp
// config.h
static int s_var = 5;  // Each file gets its own copy

// main.cpp
#include "config.h"
int main() {
    s_var = 10;  // Changes main.cpp's copy
}

// other.cpp
#include "config.h"
void someFunction() {
    s_var = 20;  // Changes other.cpp's SEPARATE copy
    // main.cpp still sees s_var = 10!
}
```

The Golden Rule
You need to dereference when you have a POINTER but you want to work with the VALUE it points to.
```cpp
int nums[5];

// Array subscript - NO dereference
nums[2] = 10;           // ✅ Direct access

// Pointer arithmetic - NEED dereference  
*(nums + 2) = 10;       // ✅ nums+2 is an address, * gets the value

// Why? Because:
// nums → address of first element
// nums + 2 → address of third element  
// *(nums + 2) → value at that address

/*
Memory:
[0x1000: nums[0]] = ?
[0x1004: nums[1]] = ?  
[0x1008: nums[2]] = ?  ← We want to put 10 here

nums → 0x1000
nums + 2 → 0x1008 (address)
*(nums + 2) → value at 0x1008
*/

// ==================
int* num = new int;

// Pointer itself - just an address
cout << num << endl;    // Prints address like 0x1000

// Value it points to - NEED dereference
*num = 10;              // ✅ Store 10 at the allocated memory
cout << *num << endl;   // ✅ Prints 10 (the value)

// Common mistake:
// num = 10;            // ❌ WRONG! Changes the pointer, not the value

/*
Memory:
[0x2000: some memory] = ?  ← We want to put 10 here

num → 0x2000 (pointer variable stores this address)
*num → value at 0x2000
*/
```

</details>




<details>
<summary><code>static</code> keyword (in classes and structs)</summary>

1. Shared Across All Instances
```cpp
class Entity {
public:
    static int s_var;
    int instance_var;
    
    Entity(int val) : instance_var(val) {}
};

int Entity::s_var = 5;  // Definition

int main() {
    Entity e1(1), e2(2), e3(3);
    
    e1.s_var = 10;  // Change via e1
    
    std::cout << e2.s_var << std::endl;  // 10 - e2 sees the change!
    std::cout << e3.s_var << std::endl;  // 10 - e3 also sees it!
    
    std::cout << e1.instance_var << std::endl;  // 1 (unique to e1)
    std::cout << e2.instance_var << std::endl;  // 2 (unique to e2)
}
```

2. Can Access Without Objects
```cpp
class MathUtils {
public:
    static const double PI;
    static double circleArea(double radius) {
        return PI * radius * radius;
    }
};

const double MathUtils::PI = 3.14159;

int main() {
    // No objects needed!
    double area = MathUtils::circleArea(5.0);
    std::cout << MathUtils::PI << std::endl;
}
```

3. Static Members Don't Affect sizeof()
```cpp
class Entity {
public:
    static int s_var;  // Not in object memory
    int instance_var;  // In object memory
};

int Entity::s_var = 0;

int main() {
    Entity e;
    std::cout << sizeof(e) << std::endl;  // Size of int (4 bytes)
    // static s_var is NOT included in object size!
}
```


4. Static Member Functions Limitations

Static member functions:

✅ Can access static members

❌ Cannot access non-static members

❌ Cannot use this pointer

```cpp
class Entity {
public:
    static int s_var;
    int instance_var;
    
    static void staticMethod() {
        s_var = 10;        // ✅ OK - static member
        // instance_var = 5; // ❌ Error - non-static member
        // this->instance_var = 5; // ❌ Error - no 'this'
    }
    
    void regularMethod() {
        s_var = 10;        // ✅ OK
        instance_var = 5;  // ✅ OK
    }
};
```
5. Static const Members Can Be In-Class Initialized
```cpp
class Constants {
public:
    static const int MAX_SIZE = 100;  // OK for integral types
    static const double PI;           // Need external definition
};

const int Constants::MAX_SIZE;  // Definition (no initializer needed)
const double Constants::PI = 3.14159;
```

6. Static Members in Inheritance
```cpp
class Base {
public:
    static int base_var;
};

class Derived : public Base {
    // Inherits base_var, but it's still the SAME variable
};

int Base::base_var = 10;

int main() {
    Base::base_var = 20;
    std::cout << Derived::base_var << std::endl;  // 20 - same variable!
}
```

Key Takeaways
* Static members belong to the class, not instances
* All instances share the same static variables
* Can use without creating objects (ClassName::member)
* Must be defined exactly once outside the class
* Perfect for counters, configuration, utilities

</details>


<details>
<summary><code>inline</code> keyword</summary>

What inline Originally Meant (Hinting)
```cpp
// Regular function - typical compilation
void regularFoo() {
    std::cout << "Hello" << std::endl;
}
// Call: regularFoo(); → compiler generates function call

// Inline function - compiler hint
inline void inlineFoo() {
    std::cout << "Hello" << std::endl;  
}
// Call: inlineFoo(); → compiler MAY copy the function body here
```

Modern Reality: inline is About Linkage
The optimization hint is mostly ignored by modern compilers (they inline automatically). The main purpose today is to allow multiple definitions:
```cpp
// utils.h
inline void printMessage() {  // Can be defined in header
    std::cout << "Message" << std::endl;
}

// main.cpp
#include "utils.h"
int main() {
    printMessage();  // ✅ OK
}

// other.cpp
#include "utils.h" 
void test() {
    printMessage();  // ✅ OK - no linker error!
}
```
Without inline in header:
```cpp
// utils.h
void printMessage() {  // ❌ Multiple definitions!
    std::cout << "Message" << std::endl;
}
```


Inline Variables (C++17+)
The Problem inline Solves
```cpp
// config.h
constexpr int MAX_SIZE = 100;  // OK in C++17 (implicitly inline)
std::string app_name = "MyApp";  // ❌ Multiple definitions!

// Before C++17, you had to do:
extern const int MAX_SIZE;  // header
const int MAX_SIZE = 100;   // .cpp file
```

The Solution: inline Variables
```cpp
// config.h
inline int max_connections = 100;  // ✅ One shared variable
inline std::string app_name = "MyRouter";  // ✅ Works with non-const too!
inline std::vector<std::string> protocols = {"TCP", "UDP"};

// Now include in multiple files - no linker errors!
// works as global variables - all TUs share the same memory address of the variable
```

Key Differences: Regular vs Inline
Regular Function in Header
```cpp
// utils.h
void utility() { /* ... */ }  // ❌ Linker error if included in multiple .cpp files

// You'd need to do:
void utility();  // Declaration in header
void utility() { /* ... */ }  // Definition in .cpp file
```

Inline Function in Header
```cpp
// utils.h
inline void utility() { /* ... */ }  // ✅ OK in multiple .cpp files

// Every .cpp gets its own "copy" but linker merges them
```

When to Use inline
Use inline for:
* Small utility functions in headers
* Global variables defined in headers (C++17+)
* Template functions (implicitly inline)
* constexpr variables (implicitly inline in C++17+)

Don't use inline for:
* Large functions (code bloat)
* Functions with complex logic
* Functions called from single location

Important Notes
* inline is a request - compiler may ignore it for optimization
* Modern compilers auto-inline small functions anyway
* The main benefit is avoiding One Definition Rule violations
* All template functions are implicitly inline when defined in headers

</details>


<details>
<summary><code>virtual</code> keyword</summary>

Virtual functions enable **runtime polymorphism** - the ability to call the appropriate function based on the actual object type, not the pointer/reference type.

Basic Virtual Function
```cpp
class Entity {
public:
    virtual void getName() {  // Virtual function
        std::cout << "Entity" << std::endl;
    }
};

class Tree : public Entity {
public:
    void getName() override {  // Override base class function
        std::cout << "Tree" << std::endl;
    }
};
```

Pure Virtual Functions act like templates:
```cpp
class Entity {
public:
    virtual void doSomething() = 0;  // Pure virtual - MUST be implemented
    // Makes Entity an "abstract class" - cannot be instantiated
};

class Tree : public Entity {
public:
    void doSomething() override {  // MUST implement this
        std::cout << "Tree is growing" << std::endl;
    }
};

// Entity e;  // ❌ Error - abstract class
Tree t;       // ✅ OK - implemented pure virtual function
```

Behind the scenes, C++ creates a virtual function table (vtable) for each class with virtual functions:
```log
Entity vtable:
[0] → Entity::getName()

Tree vtable:
[0] → Tree::getName()
```
Each object has a hidden pointer to its class's vtable.

The Power of virtual functions - Runtime Polymorphism:
```cpp
// the good stuff is that we dont need to redifine the printName() function for each derived Entity class (Tree, Rock, whatever),
// we can just pass it here
void printName(Entity* entity) {
    entity->getName();  // Calls the RIGHT function based on actual object
}

int main() {
    Tree tree;
    Entity* entityPtr = &tree;  // Base class pointer to derived object
    
    entityPtr->getName();  // Outputs "Tree" NOT "Entity"!
    printName(&tree);      // Also outputs "Tree"
}
```

Virtual Destructors - CRITICAL!
```cpp
class Entity {
public:
    virtual ~Entity() {  // Virtual destructor
        std::cout << "Entity destroyed" << std::endl;
    }
};

class Tree : public Entity {
public:
    ~Tree() override {
        std::cout << "Tree destroyed" << std::endl;
    }
};

int main() {
    Entity* entity = new Tree();
    delete entity;  // ✅ Calls Tree::~Tree() then Entity::~Entity()
}
```

Without virtual destructor:
```cpp
class Entity {
public:
    ~Entity() {  // Non-virtual destructor ❌
        std::cout << "Entity destroyed" << std::endl;
    }
};

Entity* entity = new Tree();
delete entity;  // ❌ Only calls Entity::~Entity() - Tree destructor skipped!
// Memory leak if Tree allocated resources!
```

Key Rules Summary:
* Virtual functions enable runtime polymorphism
* Pure virtual functions (= 0) make class abstract
* Abstract classes cannot be instantiated
* Derived classes must implement all pure virtual functions
* Always make destructors virtual in base classes
* Use override keyword for clarity and safety
* Virtual functions have small performance cost (vtable lookup)
* When to Use Virtual Functions

Use them when:
* You have a hierarchy of related classes
* You want to call methods without knowing the exact type
* You need runtime polymorphism
* You're designing interfaces (all pure virtual)

Avoid when:
* Performance is critical (embedded systems, real-time (usually this is not so heavy, noone ever notices the performance change here)
* You don't need polymorphism
* You're using templates instead

</details>

<details>
<summary>Classes, structs</summary>

By default all elements in classes are private. In structs they are public. Nothing much to add.
Classes have conctructors and decontructors:

```cpp
class Entity {
private:
    int& x;  // Reference member - MUST be initialized
    int& y;  // Reference member - MUST be initialized

public:
    // References MUST be initialized in member initializer list
    Entity(int& x_val, int& y_val) : x(x_val), y(y_val) {
        // x and y are now references to external variables
    }

    ~Entity() {
        cout << "Free memory and stuff" << endl;
    }

    void print() {
        cout << "x: " << x << ", y: " << y << endl;
    }

    void updateValues() {
        x = 100;  // This modifies the original variables!
        y = 200;
    }
};

// Usage:
int main() {
    int a = 10, b = 20;
    Entity e(a, b);  // e.x refers to a, e.y refers to b

    e.print();  // Output: x: 10, y: 20
    e.updateValues();

    cout << "a: " << a << ", b: " << b << endl;  // Output: a: 100, b: 200
}
```

Friend classes are a C++ feature that allows one class to access the private and protected members of another class. It's like giving a "friendship pass" to bypass normal access restrictions.
```cpp
class SecretKeeper {
private:
    int secret_number = 42;
    string secret_message = "Classified!";
    
    // Declare FriendClass as a friend
    friend class FriendClass;
};

class FriendClass {
public:
    void revealSecrets(SecretKeeper& keeper) {
        // Can access private members of SecretKeeper!
        cout << "The secret number is: " << keeper.secret_number << endl;
        cout << "The secret message is: " << keeper.secret_message << endl;
    }
};
```
What Friends Can and Cannot Do
What Friends CAN Do:
* Access private and protected members of the friend class
* Use private/protected methods and variables

What Friends CANNOT Do:
* Inherit from the friend class (unless also derived)
* Override access rules for other classes
* Make the friendship mutual (must be declared separately)
* Be inherited (friendship isn't transitive)

</details>

<details>
<summary>strings</summary>

```cpp
const char* name = "Austris"; // alocates 7 bytes for text +1 byte for NULL, so it looks like: "Austris\0" or "Austris"0 - 8 bytes.
cout << name << endl; // this will result with "Austris", because last element of name is NULL (0x00, \0), to escape

char name2[5] = {'A','u', 's', 't', 'r'};
cout << name2 << endl; // this ill print Austr + garbage until it hits \0 somewhere in memory. If we add [5] element as '\0' or 0, then works fine.
```

Fun thing this does:
```cpp
const char name[8] = "Che\0rno";
std::cout << strlen(name) << std::endl; // this returns length of 3!!!! it counts chars until \0

const char name2[] = "Cherno";
std::cout << strlen(name2) << std::endl; // this returns length of 6
```

For performance reasons, best to pass references of strings to functions, if the not needed otherwise:
```cpp
void printString(const std::string& msg) {
    cout << msg << endl;
}
```

To concatinate 2 strings:
```cpp
std::string name = "Cherno"s + " hello"; // introduced in C++14
```

To ingore escape characers, usually when we want to write stuff in multiple lines:
```cpp
std::string statement = R"(
    SELECT *
    FROM somewhere sm
    WHERE ...
)";
```

Wide characters (never used these):
```cpp
const char* name = u8"Cherno"; // a normal char, 1 byte per char, to adhere with UTF-8
// stuff introduced in C++11:
const wchar_t* name2 = L"Cherno";  // 16 bits per char (2 bytes), to adhere with UTF-16
const char16_t* name2 = u"Cherno"; // 16 bits per char (2 bytes), to adhere with UTF-16
const char32_t* name2 = U"Cherno"; // 32 bits per char (4 bytes), to adhere with UTF-32
```
`char16_t` will always be 2 bytes, `wchar_t` may differ on OS.


</details>


<details>
<summary><code>const</code> keyword</summary>

These things mean the same:
```cpp
int const* a = new int(5);    // Same as:
const int* b = new int(5);    // These are IDENTICAL

// What it means:
// The DATA is constant, but the POINTER can change

*a = 10;    // ❌ ERROR! Cannot change the data
a = nullptr; // ✅ OK! Can change where pointer points

cout << *a << endl;  // ✅ OK! Can read the data
```

But this is that we cannot reassign the pointer:
```cpp
int* const a = new int(5);

// What it means:
// The POINTER is constant, but the DATA can change

*a = 10;     // ✅ OK! Can change the data
a = nullptr; // ❌ ERROR! Cannot change where pointer points

cout << *a << endl;  // ✅ OK! Can read the data
```

Cannot change the contents of pointer and the pointer itself:
```cpp
const int* const a = new int(5);

// What it means:
// BOTH the pointer AND the data are constant

*a = 10;     // ❌ ERROR! Cannot change the data
a = nullptr; // ❌ ERROR! Cannot change where pointer points

cout << *a << endl;  // ✅ OK! Can read the data
```

Rule to remember: Read from right to left
```cpp
const int* ptr;         // "ptr is a pointer to an int that's const"
int* const ptr;         // "ptr is a const pointer to an int"
const int* const ptr;   // "ptr is a const pointer to an int that's const"
```

You can declare `const` methods:
```cpp
class Entity {
  private:
    int* m_X, m_Y;
    mutable int num;
  public:
    const int* const GetX() const {
        num = 2; // you can modify something you really want in a const method, when the var is mutable
        return m_X;
    }
    // here we say that: this method promises to return a * that cannot be modified,
    // contents of * cannot be modified 
    // promisies to not modify entity class
};
```

</details>


<details>
<summary><code>mutable</code> keyword</summary>

Marking a class member mutable enables const functions to edit it:

```cpp
class Entity {
  private:
    std::string m_Name;
    mutable int m_debugCount 0;
  public:
    const std::string& GetName() const {
        m_DebugCount++; // editing a class member, because it is mutable
        return m_Name;
    }
};

int main() {
    const Entity e
    e.GetName(); // if Entity e would not be defined as const, we could not call non-const functions

    int x = 8;
    // this is a lambda - little throw away function we can assing to a variable
    auto f = [=]() mutable { // [=] captures x by VALUE (copy)
        x++;                 // Modifies the COPY, not original
        std::cout << x << std::endl;
    }
    f(); // Output: 9
    std::cout << x << std::endl;  // Output: 8 (original unchanged!)
}
```
</details>

<details>
<summary>Member initializer lists</summary>

```cpp
class Entity {
  private:
    int m_Score;
    std::string m_Name;
    Example exp;
  public:
    Entity()
        : m_Score(0), m_Name("Unknown"), exp(8) // needs to be in exact order
    {}

    Entity(const std::string& name)
        : m_Name(name)
    {} // do smth else if u want
};
```
</details>

<details>
<summary>Ternary operators</summary>

```cpp
if (level > 5)
    speed = 10;
else
    speed = 5;
// is the same as:
speed = level > 5 ? 10 : 5
```

```cpp
speed = level > 5 ? level > 10 ? 15 : 10 : 5; // usually people do not nest their ternary operators

// same as:
int speed;
if (level > 5) {
    if (level > 10) {
        speed = 15;
    } else {
        speed = 10;
    }
} else {
    speed = 5;
}
```

</details>


<details>
<summary>Create/instantiate objects</summary>

In which memory are we creating our object?
When you can, always create objects in stack, instead of heap.
You want heap when you need the object outside of the scope of function or the object is too big (stack has 1-2Mb or smth around that memory available, depends on platform or compiler).

```cpp
namespace String = std::string;
class Entity {
  public:
    Entity() { /* ... */ }
    Entity(const String& name) {/*...*/}
    const String& getName() const { /*...*/}

};

int main() {
    Entity entity0("Cherno");                       // allocated in stack
    std::cout << entity0.getName(); << std::endl;

    Entity* entity1 = new Entity("Cherno");         // allocated on heap
    std::cout << entity1->getName() << std::endl;
    std::cout << (*entity1).getName() << std::endl;
    delete entity1;                                  // need to free heap memory ourselves
}
```
</details>

<details>
<summary><code>new</code> keyword</summary>

Using `new` keyword (it is just a operator), it always returns a pointer to the memory allocated:
```cpp
int* b = new int;          // allocated 4 bytes on the heap
int* b = new int[50];      // allocated 200 bytes on the heap
Entity* e = new Entity();  // we also call the contructor, which initializes stuff for the class

delete e;    // frees the memory, also runs the Entity class destructor ~Entity()
delete[] b;  // [] for arrays needed
```

Behind the scenes, `new` usually in standard library calls `malloc`:
```cpp
Enitity* e1 = new Enitity();

Enitity* e = (*Enitity)malloc(sizeof(Enitity)) // this is actually kinda the same, the only diff is that malloc does not call the Entity() contructor
new (e) Entity(); // constructs Entity at the memory location pointed to by e

e->~Entity(); // manually call destructor
free(e); // frees memory from malloc, dont mix new with free, use delete
```

You can also specify the address if needed:
```cpp
Entity* e = new(b) Entity(); // assuming b is a pointer
```

Key rule: Don't mix new with free, or malloc with delete — always match them properly.

| Allocation method | Deallocation method |
|-------------------|---------------------|
| `malloc()`        | `free()`            |
| `new`             | `delete`            |
| `new[]`           | `delete[]`          |

</details>

<details>
<summary>Implicit/explicit</summary>

Implicit:
```cpp
class Entity {
  private:
    std::string name;
    int age;
  public:
    Entity(const std::string& name) {/*...*/}
    Entity(int age) {/*...*/}
};

void PrintEntity(const Entity& entity) {
    // Printing
}

// implicit conversion/implicit construction
int main() {
    PrintEntity(22); // 22 can be converted to entity
    PrintEnitity("Austris") // "Austris" is a const char array [7], not std::string, so this does not do Entity(std::string name)
    // but this PrintEnitity(std::string("Austris")) and this PrintEnitity(Entity("Austris")) works

    Entity a = "Austris"; // this will call the Entity(std::string name) constructor
    Entity b = 24;        // this will call the Entity(int age) constructor
}
```

Explicit:
```cpp
class Entity {
  /* ... */
  public:
    explicit Entity(const std::string& name) {/*...*/}
    explicit Entity(int age) {/*...*/}
};

// when contructors are explicit, we need to explicitly tell cast it to Entity
int main() {
    Entity b = (Entity)22; // casting 22 to Entity
    // or just normally call the contructor
    Entity b = Entity(22);
}
```

This is sometimes used in math libraries, when you dont want numbers or something converted to other things you dont want.
But this is not really used often.
</details>


<details>
<summary>Operators and operator overloading</summary>

```cpp
struct Vector2 {
    float x, y;
    Vector2(float x, float y)
        : x(x), y(y) {}
    Vector2 Add(const Vector2& other) const {
        return Vector2(x + other.x, y + other.y);
        // we cal also do this:
        // return *this + other; // using the overloaded + operator
    }
    Vector2 Multiply(const Vector2& other) const { // use const, bc we dont modify the class
        return Vector2(x * other.x, y * other.y);
    }
    // we overloaded the + operator
    Vector2 operator+(const Vector2& other) const {
        return Add(other);
    }
    // we overloaded the * operator
    Vector2 operator*(const Vector2& other) const {
        return Multiply(other);
    }
};

// here we overloaded the << operator, so we could print formated Vecotor2 on console
std::ostream& operator<<(std::ostream& stream, const Vector2& other) {
    stream << other.x << ", " << other.y;
    return stream;
}

// we can also overload == operator, and do similar stuff for any operator
bool operator==(const Vector2& other) const {
    return x == other.x && y == other.y;
}

int main() {
    Vector2 position(1.0f, 2.0f);
    Vector2 speed(1.2f, 2.2f);
    Vector2 powerup(1.2f, 2.2f);

    // we can run multiply and add like this using methods:
    Vector2 result1 = position.Add(speed.Multiply(powerup));

    // or use operator overloading, looks cleaner:
    Vector result2 = position + speed; // * poweriup

    std::cout << result2 << std::endl; // we are using overloaded << operator for Vector2
}
```

Not used so much, because it turns hard to read sometimes.
</details>

<details>
<summary><code>this</code> keyword</summary>

`this` keyword is available only to methods, that belongs to the object.
`this` is a pointer to the object.

```cpp
class Entity {
  public:
    int x,y;
    Entity(int x, int y) {
        // Entity* const e = this; // this is this, this can be reassigned, thats why const is there
        this->x = x; // or (*this).x, we need to deference this pointer
        this->y = y; // we cant just x=x or y=y, we need to say that we are assinging value to x in the object
        PrintEntity(this);
        PrintEntity2(*this);
    }

    int GetX() const {
        // const Entity* e = this; // this is this

    }
}

void PrintEntity(Entity* e) { /* do printing stuff */ }
void PrintEntity2(const Entity& e) { /* do printing stuff */ }
```
</details>

<details>
<summary>Object lifetime</summary>

This is something like a smart pointer would work:
```cpp
class Entity {
  public:
    Entity() { /*...*/}
    ~Entity() { /*...*/}
}

class ScopedPtr {
  private:
    Entity* m_Ptr;
  public:
    ScopedPtr(Entity* ptr)
        : m_Ptr(ptr)
    {}
    ~ScopedPtr() {
        delete m_Ptr;
    }
}

int main() {
    {
        ScopedPtr e = new Entity(); // ScopedPtr is allocated on stack, it gets deleted after {} and calls delete for Entity
        Enitity* e2 = new Entity(); // this will not get detroyed when going out {} scope
    }
}
```
</details>

<details>
<summary>Smart pointers</summary>

Smart pointers automate `new/delete` handling - they're wrapper classes around raw pointers that manage memory automatically.

`std::unique_ptr` - Exclusive Ownership
```cpp
#include <memory>

class Entity {
public:
    Entity() { std::cout << "Entity created\n"; }
    ~Entity() { std::cout << "Entity destroyed\n"; }
    void Print() { std::cout << "Hello from Entity!\n"; }
};

int main() {
    {
        // PREFERRED: std::make_unique (exception-safe)
        /*
        void safeFunction(int size) {
            auto entity = std::make_unique<Entity>();  // Memory allocated
            processData(size);                         // ✅ If this throws, entity automatically deletes itself!
            // No manual delete needed - RAII handles it
        }
        */
        std::unique_ptr<Entity> entity = std::make_unique<Entity>();
        
        // ❌ This WON'T compile - unique_ptr cannot be copied
        // std::unique_ptr<Entity> entity2 = entity;
        
        // ✅ This WORKS - transfers ownership (move semantics)
        std::unique_ptr<Entity> entity2 = std::move(entity);
        // Now entity is nullptr, entity2 owns the object
        
        entity2->Print();  // Use like a regular pointer
    }
    // When scope ends, Entity is automatically destroyed
    // Output: "Entity destroyed"
}
```

Key Points:

* One owner only - cannot be copied
* Zero overhead - same performance as raw pointer
* Automatic cleanup - no memory leaks
* Use std::make_unique for exception safety

`std::shared_ptr` - Shared Ownership
```cpp
#include <memory>

class Entity {
public:
    Entity() { std::cout << "Entity created\n"; }
    ~Entity() { std::cout << "Entity destroyed\n"; }
};

int main() {
    std::shared_ptr<Entity> e0;  // Empty shared_ptr
    
    {
        std::shared_ptr<Entity> sharedEntity = std::make_shared<Entity>();
        // Reference count = 1
        
        e0 = sharedEntity;  // Copy increases reference count to 2
        std::cout << "Reference count: " << e0.use_count() << std::endl;  // 2
        
    }  // sharedEntity goes out of scope → reference count decreases to 1
    // Entity NOT destroyed because e0 still holds a reference
    
    std::cout << "Reference count: " << e0.use_count() << std::endl;  // 1
    
}  // e0 goes out of scope → reference count = 0 → Entity destroyed
```

Key Points:
* Multiple owners - uses reference counting
* Overhead - small performance cost for reference counting
* Use std::make_shared - more efficient memory allocation
* Circular references can cause memory leaks (use weak_ptr to break)

`std::weak_ptr` - Non-Owning Reference

```cpp
#include <memory>

class Entity {
public:
    Entity() { std::cout << "Entity created\n"; }
    ~Entity() { std::cout << "Entity destroyed\n"; }
};

int main() {
    std::weak_ptr<Entity> weakEntity;  // Does NOT increase reference count
    
    {
        std::shared_ptr<Entity> sharedEntity = std::make_shared<Entity>();
        // Reference count = 1
        
        weakEntity = sharedEntity;  // Reference count STAYS 1
        
        // To use weak_ptr, must convert to shared_ptr temporarily
        if (auto tempShared = weakEntity.lock()) {
            // tempShared is a valid shared_ptr while in this scope
            std::cout << "Entity is still alive\n";
        }
        
    }  // sharedEntity destroyed → reference count = 0 → Entity destroyed
    
    // Now weakEntity points to destroyed object
    if (auto tempShared = weakEntity.lock()) {
        // This WON'T execute - object is already destroyed
        std::cout << "Entity is still alive\n";
    } else {
        std::cout << "Entity has been destroyed\n";
    }
}
```
Key Points:
* No ownership - doesn't keep object alive
* Prevents circular references between shared_ptrs
* Must check validity before use with .lock()
* Use case: Observers, caches, breaking circular dependencies

Always prefer smart pointers over raw pointers for modern C++ development!
</details>


<details>
<summary>copying and copy contructors</summary>

Little stuff about memcpy and string+char arrays:
```cpp
char* buffer;
unsigned int size;

std::string text = "Austris";
size = strlen(text);
buffer = new char[size+1]; // strlen returns 7, so here we allocated 7 bytes of memory 0-6, need +1byte for null terminator

memcpy(buffer, text, size);
buffer[size] = 0; // added /0 terminating character
```

Copying a class that has `char*` - shallow copy/deep copy:
```cpp
class Entity {
public:
    char* buffer;
    unsigned int size;

    Entity(const char* string) {
        size = strlen(string);
        buffer = new char[size+1];
        memcpy(buffer, string, size);
        buffer[size] = 0;
    }
    
    ~Entity() {
        delete[] buffer;
    }

    // Copy constructor
    Entity(const Entity& other) : size(other.size) {
        buffer = new char[size + 1];             // Allocate new memory
        memcpy(buffer, other.buffer, size + 1);  // Copy the actual string data
    }
    
    // Option: Disallow copying (if you don't want it)
    // Entity(const Entity& other) = delete;
};

int main() {
    Entity test = "Austris";     // test.buffer points to 0x1000
    Entity test2 = test;         // test2.buffer points to NEW memory 0x2000

    // Now safe - each has its own memory
    // ~test2 deletes 0x2000 ✅
    // ~test deletes 0x1000  ✅
}
```
</details>

<details>
<summary>Arrow operator</summary>

```cpp
#include <iostream>
using namespace std;

class Entity {
public:
    int x = 1;
    void Print() const { 
        cout << "Hello! x = " << x << endl; 
    }
};

class ScopedPtr {
private:
    Entity* m_Obj;
public:
    ScopedPtr(Entity* entity) : m_Obj(entity) {}
    ~ScopedPtr() {
        delete m_Obj;
    }

    // Overload the arrow operator to provide direct access
    Entity* operator->() {
        return m_Obj;
    }

    // Const version for const objects
    const Entity* operator->() const {
        return m_Obj;
    }
};

int main() {
    // Regular object access
    Entity e;
    e.Print();    // Direct method call
    e.x = 2;      // Direct member access

    // Pointer access
    Entity* ptr = &e;
    (*ptr).Print();  // Dereference then call (clunky)
    ptr->Print();    // Arrow operator (clean)
    ptr->x = 2;      // Arrow for member access

    // Smart pointer with overloaded arrow
    ScopedPtr entity = new Entity();
    entity->Print();  // Calls our overloaded ->, then Entity::Print()
    entity->x = 5;    // Access members through our smart pointer
}
```

Using arrow operator, we can also get offsets, useful when serializing data:
```cpp
struct Vector3 {
    float x, y, z;  // Each float = 4 bytes
};

int main() {
    // The "wild beast" - getting member offsets without an actual object
    int offset_x = (int)&((Vector3*)nullptr)->x;  // Result: 0
    int offset_y = (int)&((Vector3*)nullptr)->y;  // Result: 4
    int offset_z = (int)&((Vector3*)nullptr)->z;  // Result: 8
}

// Step 1: (Vector3*)nullptr
// Create a NULL pointer of type Vector3*
// We're NOT dereferencing it yet!

// Step 2: ((Vector3*)nullptr)->x
// Use arrow operator to access member 'x'
// This doesn't actually dereference memory!
// It just calculates: base_pointer + offset_of_x

// Step 3: &((Vector3*)nullptr)->x
// Take the address of the member 'x'
// This gives us: nullptr + offset_of_x

// Step 4: (int)&((Vector3*)nullptr)->x
// Cast the address to integer
// Since we started with nullptr (address 0), we get the pure offset!

// Visual memory layout:
// Vector3 object in memory:
// [0-3]:   x (offset 0)
// [4-7]:   y (offset 4) 
// [8-11]:  z (offset 8)
```

Safer Modern Alternative:
```cpp
#include <cstddef>  // for offsetof

struct Vector3 {
    float x, y, z;
};

int main() {
    // Standard library way - does the same thing safely
    size_t offset_x = offsetof(Vector3, x);  // 0
    size_t offset_y = offsetof(Vector3, y);  // 4
    size_t offset_z = offsetof(Vector3, z);  // 8
    
    cout << "Offsets - x: " << offset_x 
         << ", y: " << offset_y 
         << ", z: " << offset_z << endl;
}
```
</details>

<details>
<summary>Dynamic arrays</summary>

`std::vector` is a resizable array that manages its own memory. Unlike C-style arrays, vectors can grow and shrink dynamically.

Basic Vector Usage
```cpp
#include <vector>
#include <iostream>

struct Vertex {
    float x, y, z;
    
    // Constructor for convenience
    Vertex(float x, float y, float z) : x(x), y(y), z(z) {}
};

// Overload << for easy printing
std::ostream& operator<<(std::ostream& stream, const Vertex& vertex) {
    stream << vertex.x << ", " << vertex.y << ", " << vertex.z;
    return stream;
}

// Important: Pass by const reference to avoid copying
void Function(const std::vector<Vertex>& vertices) {
    for (const Vertex& v : vertices) {
        std::cout << v << std::endl;
    }
}

int main() {
    std::vector<Vertex> vertices;
    
    // Add elements
    vertices.push_back(Vertex(1, 2, 3));
    vertices.push_back(Vertex(4, 5, 6));
    vertices.push_back(Vertex(7, 8, 9));

    // Method 1: Index-based loop
    for (size_t i = 0; i < vertices.size(); i++) {
        std::cout << vertices[i] << std::endl;
    }

    // Method 2: Range-based loop (PREFERRED)
    for (const Vertex& v : vertices) {  // Use reference to avoid copying!
        std::cout << v << std::endl;
    }

    // Remove elements
    vertices.erase(vertices.begin() + 1);  // Remove 2nd element
    vertices.clear();  // Remove all elements
}
```

Optimizing Vector Performance:
```cpp
#include <vector>
#include <iostream>

struct Vertex {
    float x, y, z;
    
    Vertex(float x, float y, float z) : x(x), y(y), z(z) {
        std::cout << "Constructed at " << this << std::endl;
    }
    
    // Copy constructor
    Vertex(const Vertex& other) : x(other.x), y(other.y), z(other.z) {
        std::cout << "Copied from " << &other << " to " << this << std::endl;
    }
    
    // Move constructor (C++11)
    Vertex(Vertex&& other) noexcept : x(other.x), y(other.y), z(other.z) {
        std::cout << "Moved from " << &other << " to " << this << std::endl;
    }
};

int main() {
    std::cout << "=== INEFFICIENT WAY ===" << std::endl;
    {
        std::vector<Vertex> vertices;
        
        // This creates temporary Vertex objects, then COPIES them into vector
        vertices.push_back(Vertex(1, 2, 3));  // Construct + Copy
        vertices.push_back(Vertex(4, 5, 6));  // Construct + Copy + possible reallocation
        vertices.push_back(Vertex(7, 8, 9));  // Construct + Copy + possible reallocation
    }
    
    std::cout << "\n=== EFFICIENT WAY ===" << std::endl;
    {
        std::vector<Vertex> vertices;
        vertices.reserve(3);  // Pre-allocate memory for 3 elements
        
        // emplace_back constructs objects IN PLACE - no copies!
        vertices.emplace_back(1, 2, 3);  // Direct construction in vector memory
        vertices.emplace_back(4, 5, 6);  // Direct construction
        vertices.emplace_back(7, 8, 9);  // Direct construction
    }
    
    std::cout << "\n=== EVEN BETTER: C++11 MOVE ===" << std::endl;
    {
        std::vector<Vertex> vertices;
        vertices.reserve(3);
        
        // If you already have objects, use std::move
        Vertex v1(1, 2, 3);
        Vertex v2(4, 5, 6);
        Vertex v3(7, 8, 9);
        
        vertices.push_back(std::move(v1));  // Move instead of copy
        vertices.push_back(std::move(v2));
        vertices.push_back(std::move(v3));
    }
}
```
</details>

<details>
<summary>Local static in C++</summary>

```cpp
#include <iostream>

void Function() {
    // Static local variable - initialized ONLY on first function call
    // Lifetime: entire program duration
    // Scope: only within this function
    static int i = 0;  // Initialization happens ONCE
    i++;
    std::cout << i << std::endl;
}

int main() {
    Function();  // Output: 1 (i initialized to 0, then incremented to 1)
    Function();  // Output: 2 (i remembered as 1, incremented to 2)  
    Function();  // Output: 3 (i remembered as 2, incremented to 3)
    // Without 'static' it would output: 1, 1, 1
    // With 'static' it outputs: 1, 2, 3
}
```

Key Characteristics of Local Static Variables
1. Initialization Happens Once:
```cpp
void expensiveInitialization() {
    static std::vector<int> data = []() {
        std::cout << "Initializing expensive data..." << std::endl;
        std::vector<int> result;
        // Simulate expensive setup
        for (int i = 0; i < 1000; i++) {
            result.push_back(i);
        }
        return result;
    }();  // This lambda is called ONLY on first invocation
    
    std::cout << "Data size: " << data.size() << std::endl;
}

int main() {
    expensiveInitialization();  // "Initializing expensive data..."
    expensiveInitialization();  // No initialization message
    expensiveInitialization();  // No initialization message
}
```

2. Thread-Safe in C++11+
```cpp
#include <thread>
#include <vector>

void counter() {
    static int count = 0;  // Thread-safe initialization in C++11+
    count++;
    std::cout << "Count: " << count << std::endl;
}

int main() {
    std::vector<std::thread> threads;
    for (int i = 0; i < 5; i++) {
        threads.emplace_back(counter);
    }
    for (auto& t : threads) {
        t.join();
    }
}
```

Singleton Pattern with Local Static
```cpp
#include <iostream>
#include <string>

class Singleton {
private:
    std::string name;
    
    // Private constructor - cannot create instances directly
    Singleton() : name("DefaultSingleton") {
        std::cout << "Singleton constructed!" << std::endl;
    }
    
public:
    // Delete copy operations to prevent duplication
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
    
    // Static method to get the single instance
    static Singleton& Get() {
        static Singleton instance;  // Created on first call only
        return instance;
    }
    
    void Hello() {
        std::cout << "Hello from " << name << std::endl;
    }
    
    void setName(const std::string& newName) {
        name = newName;
    }
};

int main() {
    Singleton::Get().Hello();  // Output: "Singleton constructed!" then "Hello from DefaultSingleton"
    
    Singleton::Get().setName("MyRouter");
    Singleton::Get().Hello();  // Output: "Hello from MyRouter"
    
    // All these refer to the SAME instance:
    Singleton& s1 = Singleton::Get();
    Singleton& s2 = Singleton::Get();
    
    std::cout << "Same instance? " << (&s1 == &s2) << std::endl;  // Output: 1 (true)
}
```
</details>

<details>
<summary>Using static libraries (Static Linking)</summary>

Static vs Dynamic Linking
*Static Linking:*
* Library code is embedded directly into your executable
* Linking happens at compile time
* Result: Single .exe file, no external dependencies needed
* Advantages: Faster, compiler can optimize across library boundaries
* Disadvantages: Larger executable size, harder to update libraries

*Dynamic Linking:*
* Library code stays in separate files (.dll on Windows, .so on Linux)
* Linking happens at runtime
* Result: Smaller executable, but requires library files to be present
* Advantages: Smaller executables, easier library updates
* Disadvantages: Slower (runtime lookup), deployment complexity

Project structure:
```bash
MyProject/
├── src/
│   └── main.cpp
├── dependencies/
│   └── GLFW/
│       ├── include/
│       │   └── GLFW/
│       │       └── glfw3.h
│       └── lib/
│           ├── Windows/
│           │   ├── x64/
│           │   │   ├── glfw3.lib    # Static library
│           │   │   └── glfw3.dll    # Dynamic library (if dynamic linking)
│           │   └── x86/
│           └── Linux/
│               └── x64/
│                   └── libglfw3.a   # Linux static library
└── build/                           # Build output directory
```

Code usage:
```cpp
#include <GLFW/glfw3.h>  // Use <> for external dependencies
// Convention:
// - <> = system/external headers (compiler searches system paths first)
// - "" = project-local headers (searches current directory first)

extern "C" int glfwInit();
// This tells C++ compiler: "This function uses C linkage, not C++ name mangling"
// Most libraries already handle this in their headers, so you usually don't need it

int main() {
    int a = glfwInit();
}
```

Multiple ways to add link the dependency:
CMake: `include_directories(dependencies/GLFW/include)`
Make: 
```makefile
# ....
CXXFLAGS = -std=c++17 -Idependencies/GLFW/include
LDFLAGS = -Ldependencies/GLFW/lib/Linux/x64 -lglfw3
# ....
```
</details>


<details>
<summary>Using dynamic libraries</summary>

Dynamic libraries are external binary files that get linked to your program at runtime, not compile time.

File Types by Platform

| Platform | Dynamic Library File        | Import Library (Windows)     |
|----------|-----------------------------|------------------------------|
| Windows  | .dll (Dynamic Link Library) | .lib (Import library)        |
| Linux    | .so (Shared Object)         | (No separate import library) |
| macOS    | .dylib (Dynamic Library)    | (No separate import library) |


How Dynamic Linking Works
Compile Time:
* Your code compiles against header files and import libraries (.lib on Windows)
* The import library contains "stubs" that know how to load the DLL at runtime

Runtime:
* Your program starts
* Operating system loads your .exe + required .dll files
* Function calls are redirected to the DLL


Dynamic vs Static: When to Use Each
Use Dynamic Linking When:
* Multiple programs use the same library (saves disk/memory)
* Frequent updates to the library
* Large libraries that would bloat your executable
* Plugin systems where libraries can be swapped

Use Static Linking When:
* Single executable deployment
* Performance critical applications
* Avoiding DLL hell (dependency issues)
* Embedded systems with limited resources
</details>


<details>
<summary>Multiple return values and types</summary>

1. Output Parameters (Reference)
```cpp
// Modify variables passed by reference - simple but not obvious from caller side
void ParseShader(std::string& outVertex, std::string& outFragment) {
    outVertex = "vertex shader code";
    outFragment = "fragment shader code";
}

int main() {
    std::string vertex, fragment;
    ParseShader(vertex, fragment); // Values are modified directly
}
```

2. Output Parameters (Pointer)
```cpp
// Pointer version allows optional outputs with null checks
void ParseShader(std::string* outVertex, std::string* outFragment) {
    if (outVertex)   *outVertex = "vertex shader code";
    if (outFragment) *outFragment = "fragment shader code";
}

int main() {
    std::string fragment;
    ParseShader(nullptr, &fragment); // Only get fragment, skip vertex
}
```

3. Return Array/Vector
```cpp
#include <array>
#include <vector>

// Fixed-size array return
std::array<std::string, 2> ParseShader() {
    return {"vertex code", "fragment code"}; // C++11 uniform initialization
}

// Dynamic vector return  
std::vector<std::string> ParseShaderDynamic() {
    return {"vertex", "fragment"};
}
```

4. Return Pair/Tuple
```cpp
#include <tuple>
#include <utility>

// Using std::pair for exactly 2 values
std::pair<std::string, std::string> ParseShaderPair() {
    return std::make_pair("vertex", "fragment");
    // Or in C++17: return {"vertex", "fragment"};
}

// Using std::tuple for multiple values
std::tuple<std::string, std::string, int> ParseShaderTuple() {
    return std::make_tuple("vertex", "fragment", 200);
}
```

5. Accessing Pair/Tuple Values
```cpp
int main() {
    // Method 1: std::get with index (works for both pair and tuple)
    auto results = ParseShaderTuple();
    std::string vs = std::get<0>(results);
    std::string fs = std::get<1>(results);
    int status = std::get<2>(results);
    
    // Method 2: .first/.second (pair only)
    auto pairResults = ParseShaderPair();
    std::string vertex = pairResults.first;
    std::string fragment = pairResults.second;
    
    // Method 3: Structured bindings (C++17 - RECOMMENDED)
    auto [vert, frag] = ParseShaderPair(); // Clean and readable!
}
```

6. Best Practice: Use Struct (Recommended)
```cpp
// Most readable and self-documenting approach
struct ShaderSource {
    std::string vertex;
    std::string fragment;
    int compileStatus;
};

ShaderSource ParseShader() {
    return {"vertex code", "fragment code", 200};
}

int main() {
    ShaderSource source = ParseShader();
    std::cout << source.vertex; // Clear what you're accessing
}
```

*Summary:*
* References/Pointers: Simple but implicit behavior
* Arrays/Vectors: Good for homogeneous data
* Pairs/Tuples: Standard library solution, but .first/.second lack meaning
* Structs: Most recommended - self-documenting, clear field names, best maintainability

Modern C++ Tip: Use structured bindings (C++17) with structs for the cleanest syntax:
```cpp
auto [vertex, fragment, status] = ParseShader(); // Clean and readable!
```
</details>


<details>
<summary>Templates</summary>

Templates are a C++ feature that lets you write generic code where the compiler generates specific versions based on the types you use. It's like "programming the compiler" to write code for you. 
Templates are similar to generics in Java/C# but more powerful and flexible, allowing both type and value parameters.

Basic Function Template
```cpp
template<typename T>
void Print(T value) {
    std::cout << value << std::endl;
}
// Usage: Print(5); Print("Hello"); Print(5.5f);
```

* The compiler creates different Print functions for each type used
* If not called, the template function doesn't get compiled
* You can explicitly specify types: Print<int>(5)

Class Template with Multiple Parameters:
```cpp
template<typename T, int N>
class Array {
private:
    T m_Array[N];
public:
    int GetSize() const { return N; }
};
```

* Creates type-safe containers: `Array<int, 5>`, `Array<std::string, 10>` or other.
* Both types AND values can be template parameters

Key Points
* Eliminates code duplication - write once, use with any type
* Compile-time generation - templates are instantiated when used
* Type safety - maintains type checking while being generic
* Can get complex - should be kept simple for readability
</details>


<details>
<summary>Stack vs Heap memory</summary>

These are the two main memory areas in RAM when your application runs. They have very different allocation strategies and performance characteristics.

```cpp
#include <iostream>

struct Vector3 {
    float x, y, z;
    Vector3() : x(10), y(11), z(12) {
        std::cout << "Vector3 constructed" << std::endl;
    }
    ~Vector3() {
        std::cout << "Vector3 destroyed" << std::endl;
    }
};

int main() {
    // STACK ALLOCATION - Automatic, fast
    int value = 5;          // 4 bytes on stack
    int array[5];           // 20 bytes on stack
    array[0] = 1;
    array[1] = 2;
    array[2] = 3;
    array[3] = 4; 
    array[4] = 5;
    Vector3 vector;         // 12 bytes on stack
    // When main() ends, ALL stack variables are automatically freed
}
```
Stack Characteristics:
* Fixed size (typically 1-8MB per thread)
* Very fast allocation/deallocation (1 CPU instruction)
* Automatic cleanup when scope ends
* LIFO (Last-In-First-Out) order
* Memory is contiguous

Stack Memory Layout:
```
High Addresses
┌─────────────────┐
│ main() frame    │
│   - value = 5   │ ← Stack grows
│   - array[5]    │   DOWNWARD
│   - vector      │
└─────────────────┘
Low Addresses
```

Heap Memory:
```cpp
#include <iostream>

int main() {
    // HEAP ALLOCATION - Manual, slower but flexible
    // Single value
    int* hvalue = new int;      // Allocates 4 bytes on heap
    *hvalue = 5;                // Assign value

    // Array
    int* harray = new int[5];   // Allocates 20 bytes on heap
    harray[0] = 1;
    harray[1] = 2;
    harray[2] = 3;
    harray[3] = 4;
    harray[4] = 5;

    // Object
    Vector3* hvector = new Vector3();  // Allocates object on heap

    // MUST manually free heap memory
    delete hvalue;              // Free single value
    delete[] harray;            // Free array (use delete[])
    delete hvector;             // Free object
    // Forgetting to delete causes MEMORY LEAKS!
}
```
Heap Characteristics:
* Dynamic size (can grow/shrink)
* Slower allocation (complex bookkeeping)
* Manual memory management (you must free)
* Memory can be fragmented
* Global access (not tied to scope)


Key Differences Summary:
| Aspect        | Stack                | Heap                          |
|---------------|----------------------|-------------------------------|
| Speed         | ⚡ Very Fast         | 🐢 Slow                      |
| Size          | Fixed (~2MB)         | Dynamic (GBs)                 |
| Management    | Automatic            | Manual                        |
| Access        | Local scope          | Global                        |
| Fragmentation | No                   | Yes                           |
| Allocation    | Move stack pointer   | Search free list + OS calls   |


When to Use Each
Use Stack For:
* Small, fixed-size arrays
* Local variables
* Temporary objects
* Performance-critical code
* Objects with short lifetime

Use Heap For:
* Large data buffers
* Objects that outlive their creation scope
* Dynamic arrays where size isn't known at compile time
* Shared ownership between objects

Best practice: Prefer stack allocation when possible, and use smart pointers when you need heap:
```cpp
// GOOD - Stack + smart pointers
std::vector<uint8_t> packet_data(1500);  // Heap managed by vector
std::unique_ptr<LargeObject> obj = std::make_unique<LargeObject>();

// BAD - Manual heap management
uint8_t* packet_data = new uint8_t[1500];  // Don't forget to delete!
```
</details>


<details>
<summary><code>auto</code> keyword</summary>

The auto keyword tells the compiler: "You figure out the type based on the initializer."
Basic Usage:
```cpp
#include <iostream>
#include <string>

std::string GetName() {
    return "Austris";
}

int main() {
    // Compiler deduces 'a' is std::string (from return type of GetName())
    auto a = GetName();
    std::cout << a << std::endl;  // Output: Austris
    
    // Other examples:
    auto x = 5;           // int
    auto y = 3.14;        // double  
    auto z = "Hello";     // const char*
    auto flag = true;     // bool
}
```

Why Use auto?
1. Simplifies Complex Types
```cpp
#include <unordered_map>
#include <vector>

class Device {
    // Device class definition...
};

class DeviceManager {
private:
    std::unordered_map<std::string, std::vector<Device*>> m_Devices;
    
public:
    // Very long return type!
    const std::unordered_map<std::string, std::vector<Device*>>& GetDevices() const {
        return m_Devices;
    }
};

int main() {
    DeviceManager dm;
    
    // ❌ Verbose and error-prone:
    const std::unordered_map<std::string, std::vector<Device*>>& devices1 = dm.GetDevices();
    
    // ✅ Clean and maintainable:
    const auto& devices2 = dm.GetDevices();  // Compiler deduces the exact type
}
```

2. Cleaner Iterators
```cpp
#include <vector>
#include <string>

int main() {
    std::vector<std::string> fruits = {"Apple", "Orange", "Banana"};
    
    // ❌ Verbose iterator syntax:
    for (std::vector<std::string>::iterator it = fruits.begin(); it != fruits.end(); ++it) {
        std::cout << *it << std::endl;
    }
    
    // ✅ Clean with auto:
    for (auto it = fruits.begin(); it != fruits.end(); ++it) {
        std::cout << *it << std::endl;
    }
    
    // ✅ Even better with range-based for loop:
    for (const auto& fruit : fruits) {
        std::cout << fruit << std::endl;
    }
}
```

Reference and Const Qualifiers with auto
Important: auto strips references and const qualifiers by default!
```cpp
#include <string>

std::string GetName() {
    return "Austris";
}

const std::string& GetNameRef() {
    static std::string name = "Austris";
    return name;
}

int main() {
    // Case 1: By value
    auto name1 = GetName();       // Type: std::string (copy)
    
    // Case 2: By reference - BUT auto strips reference!
    auto name2 = GetNameRef();    // Type: std::string (COPY, not reference!)
    
    // Case 3: Explicit reference
    auto& name3 = GetNameRef();   // Type: const std::string& (reference)
    
    // Case 4: Explicit const reference  
    const auto& name4 = GetNameRef();  // Type: const std::string&
}
```

Best Practices for auto
When to Use auto:
```cpp
// ✅ Good uses:

// 1. Iterators
for (auto it = container.begin(); it != container.end(); ++it)

// 2. Complex template types
auto result = some_template_function<int, std::string>();

// 3. Lambda expressions
auto lambda = [](int x) { return x * 2; };

// 4. Range-based for loops
for (const auto& item : container)

// 5. When the type is obvious from context
auto manager = std::make_unique<DeviceManager>();
```

When to Avoid auto:
```cpp
// ❌ Potentially confusing:

// 1. When the type isn't clear from context
auto result = ProcessData();  // What type is result?

// 2. With numeric literals (might not be the type you expect)
auto size = CalculateSize();  // int? size_t? long?

// 3. When you need a specific type for overload resolution
auto value = GetValue();  // Might not match function overloads
```

auto with Different Initialization Styles
```cpp
#include <memory>
#include <vector>

int main() {
    // Direct initialization
    auto x = 42;                    // int
    
    // Copy initialization  
    auto y = {1, 2, 3};             // std::initializer_list<int>
    
    // Uniform initialization (be careful!)
    auto z{42};                     // int (C++17), was initializer_list in C++11
    auto w = std::vector<int>{1, 2, 3};  // std::vector<int>
    
    // With smart pointers
    auto device = std::make_unique<Device>();  // std::unique_ptr<Device>
}
```

Key Takeaways:
* Use auto when the type is obvious from context
* Be explicit with & and const when needed
* Great for iterators and complex template types
* Avoid when type clarity is important for readability
* Combines well with range-based for loops and lambdas
* Remember: auto strips references/const by default!

</details>

<details>
<summary>Static Arrays<code>std::array</code></summary>

`std::array` overview:
```cpp
#include <array>
#include <iostream>

// Fixed version using templates
template<typename T, size_t N>
void PrintArray(const std::array<T, N>& data) {
    std::cout << "Array size: " << data.size() << std::endl;
    std::cout << "Array type: " << typeid(T).name() << std::endl;
    
    for(size_t i = 0; i < data.size(); i++) {
        std::cout << "data[" << i << "] = " << data[i] << std::endl;
    }
}

int main() {
    // Different sizes and types
    std::array<int, 5> data5 = {1, 2, 3, 4, 5};
    std::array<double, 3> data3 = {1.1, 2.2, 3.3};
    std::array<std::string, 2> strings = {"Hello", "World"};
    
    PrintArray(data5);     // Works with int, size 5
    PrintArray(data3);     // Works with double, size 3
    PrintArray(strings);   // Works with string, size 2
}
```

Key Differences: C-style vs std::array
```cpp
#include <array>
#include <iostream>

void demonstrateDifferences() {
    // C-style array
    int c_array[5] = {1, 2, 3, 4, 5};
    
    // std::array
    std::array<int, 5> std_array = {1, 2, 3, 4, 5};

    // 1. Bounds Checking
    std::cout << "=== Bounds Checking ===" << std::endl;
    
    // C-array: No bounds checking - UNDEFINED BEHAVIOR!
    // c_array[10] = 100;  // ❌ Might crash, might corrupt memory
    
    // std::array: Safe access with .at()
    try {
        std_array.at(10) = 100;  // ✅ Throws std::out_of_range exception
    } catch (const std::out_of_range& e) {
        std::cout << "Caught exception: " << e.what() << std::endl;
    }
    
    // 2. Size Information
    std::cout << "\n=== Size Information ===" << std::endl;
    
    // C-array: sizeof gives bytes, not elements
    std::cout << "C-array sizeof: " << sizeof(c_array) << " bytes" << std::endl;  // 20 bytes
    // std::cout << "C-array element count: " << sizeof(c_array)/sizeof(c_array[0]) << std::endl;  // Hack needed
    
    // std::array: Direct size method
    std::cout << "std::array size: " << std_array.size() << " elements" << std::endl;  // 5 elements
    
    // 3. Assignment and Copying
    std::cout << "\n=== Assignment ===" << std::endl;
    
    std::array<int, 5> another_array = {10, 20, 30, 40, 50};
    std_array = another_array;  // ✅ Deep copy works!
    
    // C-arrays cannot be directly assigned
    // c_array = {10, 20, 30, 40, 50};  // ❌ Error!
    
    // 4. Iterators and Algorithms
    std::cout << "\n=== Algorithms ===" << std::endl;
    
    // std::array works with STL algorithms
    std::sort(std_array.begin(), std_array.end());
    for (const auto& val : std_array) {
        std::cout << val << " ";
    }
    std::cout << std::endl;
}
```
</details>


<details>
<summary>Function pointers</summary>

Function pointers allow you to store and pass functions as variables, enabling powerful patterns like callbacks and strategy patterns.

Basic synthax:
```cpp
#include <iostream>

void HelloWorld(int a) {
    std::cout << "Hello world! Value: " << a << std::endl;
}

int main() {
    // Method 1: Using auto (easiest)
    auto function = HelloWorld;  // Implicit conversion to function pointer
    function(5);  // Output: Hello world! Value: 5

    // Method 2: Explicit function pointer syntax
    void(*cherno)(int) = HelloWorld;
    cherno(10);  // Output: Hello world! Value: 10

    // Method 3: Using typedef/using (cleanest for complex types)
    typedef void(*HelloWorldFunction)(int);
    HelloWorldFunction func = HelloWorld;
    func(15);  // Output: Hello world! Value: 15

    // Method 4: Modern using alias
    using HelloWorldFunc = void(*)(int);
    HelloWorldFunc modernFunc = HelloWorld;
    modernFunc(20);  // Output: Hello world! Value: 20
}
```

Function Pointer Syntax Explained:
```cpp
// The syntax: ReturnType(*PointerName)(ParameterTypes)

// Examples:
void(*func1)();               // Function taking no parameters, returning void
int(*func2)(int, int);        // Function taking two ints, returning int
double(*func3)(const char*);  // Function taking const char*, returning double

// With typedef/using:
typedef int(*MathOperation)(int, int);
using MathOp = int(*)(int, int);  // Modern equivalent
```

Advanced: Function Pointers in Data Structures
```cpp
#include <iostream>
#include <vector>
#include <functional>  // For std::function (better alternative)

// Calculator operations using function pointers
class Calculator {
public:
    using Operation = int(*)(int, int);
    
    static int Add(int a, int b) { return a + b; }
    static int Subtract(int a, int b) { return a - b; }
    static int Multiply(int a, int b) { return a * b; }
    static int Divide(int a, int b) { return b != 0 ? a / b : 0; }
    
private:
    std::vector<std::pair<std::string, Operation>> operations;
    
public:
    Calculator() {
        // Store operations with their names
        operations = {
            {"Add", Add},
            {"Subtract", Subtract}, 
            {"Multiply", Multiply},
            {"Divide", Divide}
        };
    }
    
    void performOperations(int x, int y) {
        for (const auto& [name, op] : operations) {
            std::cout << name << "(" << x << ", " << y << ") = " << op(x, y) << std::endl;
        }
    }
};

int main() {
    Calculator calc;
    calc.performOperations(10, 5);
}
```

Modern Alternative: std::function (Recommended)
```cpp
#include <functional>
#include <vector>
#include <iostream>

// Using std::function instead of raw function pointers
// More flexible - works with lambdas, function objects, member functions
void ForEachModern(const std::vector<int>& values, const std::function<void(int)>& callback) {
    for (int value : values) {
        callback(value);
    }
}

int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    
    // Can capture variables in lambdas (function pointers can't do this!)
    int external_value = 100;
    
    ForEachModern(numbers, [external_value](int value) {
        std::cout << value << " + " << external_value << " = " << value + external_value << std::endl;
    });
    
    // Also works with regular function pointers
    ForEachModern(numbers, PrintValue);
}
```
</details>


<details>
<summary>Lambdas</summary>

Also called anonymous functions.


Basic overview of lambda:
```cpp
int x = 5, y = 10;

// [=] Capture everything by VALUE (copy)
auto f1 = [=]() { return x + y; };  // Gets copies of x and y

// [&] Capture everything by REFERENCE
auto f2 = [&]() { x++; return y; };  // References to original x and y

// [x, &y] Capture x by value, y by reference (can specify individual variables)
auto f3 = [x, &y]() { return x + y; };  // x is copy, y is reference

// [] Capture nothing
auto f4 = []() { return 42; };  // No access to x or y
```

If we want to pass lambda as an argument in some function:
```cpp
#include <function>

void ForEach(const std::vector<int>& values, const std::function<void(int)>& func) {
    for (int value : values)
        func(value);
}

int main() {
    std::vector<int> value = {1,2,3,4,5};
    int a = 5;
    auto lambda = [=](int value) { std::cout << "Value: " << a << std::endl; };
    ForEach(values, lambda);
}
```

</details>

<details>
<summary>namespaces</summary>

```cpp
namespace apple::func {
    void print() {}
}

int main() {
    apple::func::print();
}
```

C++17 might simplify nested namespace definition:
```cpp
namespace A::B::C {
}
```
is equivalent to
```cpp
namespace A { namespace B { namespace C {
} } }
```
</details>


<details>
<summary>Threads</summary>

Threads in C++ - Example with Comments
```cpp
#include <iostream>
#include <thread>
#include <chrono>

// Shared variable between threads - needs to be volatile or atomic in real code
static bool s_Finished = false;

void DoWork() {
    using namespace std::literals::chrono_literals;  // For the 's' suffix (1s = 1 second)

    // Print the ID of this worker thread
    std::cout << "Started worker thread id=" << std::this_thread::get_id() << std::endl;

    // Worker thread loop - runs concurrently with main thread
    while (!s_Finished) {
        std::cout << "Working...\n";
        std::this_thread::sleep_for(1s);  // Pause this thread for 1 second
        // This allows other threads to run while we're sleeping
    }

    std::cout << "Worker thread finished work\n";
}

int main() {
    // Print the main thread ID
    std::cout << "Main thread id=" << std::this_thread::get_id() << std::endl;

    // Create a new thread that executes DoWork() function
    // This starts executing IMMEDIATELY in parallel with main thread
    std::thread worker(DoWork);

    // Main thread continues executing here while worker thread runs DoWork()
    std::cout << "Press Enter to stop the worker thread..." << std::endl;
    std::cin.get();  // Main thread waits for user input
    
    // Signal the worker thread to stop
    s_Finished = true;
    std::cout << "Stop signal sent to worker thread\n";

    // Wait for the worker thread to finish its current work and exit
    // This BLOCKS the main thread until worker thread completes
    worker.join();
    
    std::cout << "Worker thread has joined main thread\n";
    std::cout << "All threads finished." << std::endl;
    
    std::cin.get();  // Keep console open
}
```

Expected Output:
```log
Main thread id=140737353922432
Press Enter to stop the worker thread...
Started worker thread id=140737353918208
Working...
Working...
Working...
[User presses Enter]
Stop signal sent to worker thread
Worker thread finished work
Worker thread has joined main thread
All threads finished.
```

More Realistic Example with Thread Safety:
```cpp
#include <iostream>
#include <thread>
#include <chrono>
#include <atomic>

// Thread-safe shared variable
static std::atomic<bool> s_Finished = false;

void DoWork(const std::string& threadName) {
    using namespace std::literals::chrono_literals;

    std::cout << threadName << " started, id=" << std::this_thread::get_id() << std::endl;

    int workCount = 0;
    while (!s_Finished.load()) {  // Atomic read
        std::cout << threadName << " working... (" << ++workCount << ")\n";
        std::this_thread::sleep_for(500ms);  // 0.5 second
    }

    std::cout << threadName << " finished after " << workCount << " units of work\n";
}

int main() {
    std::cout << "=== Multi-Threading Example ===\n";
    std::cout << "Main thread id=" << std::this_thread::get_id() << std::endl;

    // Create multiple worker threads
    std::thread worker1(DoWork, "Worker-1");
    std::thread worker2(DoWork, "Worker-2");

    // Main thread does its own work
    std::cout << "Main thread is doing other tasks...\n";
    std::this_thread::sleep_for(2s);  // Main thread sleeps for 2 seconds
    
    std::cout << "Main thread signaling workers to stop...\n";
    s_Finished.store(true);  // Atomic write - signal all workers to stop

    // Wait for all threads to finish
    worker1.join();
    worker2.join();

    std::cout << "All threads completed successfully!\n";
}
```
</details>


<details>
<summary>Timing</summary>

Here we can see how much time passes for some process, platform independent:
```cpp
#include <chrono>
#include <thread>

int main() {
    using namespace std::literals::chrono_literals;

    auto start = std::chrono::high_resolution_clock::now();
    std::this_thread::sleep_for(1s);
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<float> duration = end - start;
    std::cout << duration.count() << "s" << std::endl;
}
```

There is a better way to do this, because previous example took many lines for timing:
```cpp
#include <chrono>
#include <thread>

// we can setup a struct for timing
struct Timer {
    std::chrono::time_point<std::chrono::steady_clock> start, end;
    std::chrono::duration<float> duration;

    Timer() {
        start = std::chrono::high_resolution_clock::now();
    }

    ~Timer() {
        end = std::chrono::high_resolution_clock::now();
        duration = end - start;
        float ms = duration.count() * 1000.0f;
        std::cout << "Timer took " << ms << "ms" << std::endl;
    }
}

void Function() {
    Timer timer;
    // started timer in the constructor
    for (int i = 0; i < 100; i++)
        std::cout << "Done smth\n";
    // so when going out of scope, deconstructor is called and we get the duration result then
}

int main() {
    Function();
}
```
</details>


<details>
<summary>Multidimensional Arrays</summary>

1D Array (Single Dimension):
```cpp
// Stack allocation
int array1d[50];                    // 50 integers contiguous in memory

// Heap allocation  
int* array1d = new int[50];         // 50 integers (200 bytes on 32-bit)
delete[] array1d;                   // Cleanup
```

2D Arrays (Array of Arrays):
Heap Allocation - Fragmented Memory
```cpp
// Create array of pointers (50 pointers)
int** a2d = new int*[50];           // 50 pointers (200 bytes)

// Each pointer points to its own array
for (int i = 0; i < 50; i++) {
    a2d[i] = new int[50];           // 50 arrays of 50 integers each
}

// Access elements
a2d[2][3] = 42;                     // 3rd row, 4th column

// Cleanup - MUST delete each sub-array first!
for (int i = 0; i < 50; i++) {
    delete[] a2d[i];                // Delete each integer array
}
delete[] a2d;                       // Then delete the pointer array
```
Memory Layout (Fragmented):
```
a2d → [ptr0] → [array0: int, int, int...]
      [ptr1] → [array1: int, int, int...]  ← Different memory locations
      [ptr2] → [array2: int, int, int...]
      ...
```

3D Arrays (Array of Arrays of Arrays)
```cpp
// Triple pointer - array of arrays of arrays
int*** a3d = new int**[50];         // 50 pointers to pointers

for (int i = 0; i < 50; i++) {
    a3d[i] = new int*[50];          // 50 arrays of pointers
    
    for (int j = 0; j < 50; j++) {
        a3d[i][j] = new int[50];    // 50 arrays of integers
    }
}

// Access elements
a3d[1][2][3] = 100;                 // 2nd block, 3rd row, 4th column

// Cleanup (nested loops)
for (int i = 0; i < 50; i++) {
    for (int j = 0; j < 50; j++) {
        delete[] a3d[i][j];         // Delete innermost arrays
    }
    delete[] a3d[i];                // Delete middle arrays
}
delete[] a3d;                       // Delete outer array
```

Better Approach: 1D Array Simulating Multi-Dimensional
Memory-Efficient 2D Array
```cpp
int width = 5, height = 5;
int* array2d = new int[width * height];  // Single contiguous block

// Access: array[x + y * width]
for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
        array2d[x + y * width] = (y * 10) + x;  // Calculate position
    }
}

// Access example:
int value = array2d[2 + 3 * width];  // Equivalent to array2d[3][2]

delete[] array2d;  // Single delete - much simpler!
```

Memory Layout (Contiguous):
```
[0,0] [1,0] [2,0] [3,0] [4,0] | [0,1] [1,1] [2,1] ... [4,4]
↑--- Row 0 ---↑    ↑--- Row 1 ---↑    ...    ↑--- Row 4 ---↑
```

Modern C++ Approach with std::array and std::vector
2D Array with std::array (Fixed Size)
```cpp
#include <array>

// 5x5 2D array on stack
std::array<std::array<int, 5>, 5> matrix;

// Access
matrix[2][3] = 42;

// No manual cleanup needed!
```

2D Array with std::vector (Dynamic Size)
```cpp
#include <vector>

// 5x5 2D array on heap (managed)
std::vector<std::vector<int>> matrix(5, std::vector<int>(5));

// Access
matrix[2][3] = 42;

// Automatic cleanup - no delete needed!
```

Key Takeaways
* Multi-dimensional arrays are arrays of arrays
* Fragmented approach (array of pointers) - flexible but poor cache performance
* Contiguous approach (1D array) - better performance, simpler management
* Modern C++ prefers std::vector and std::array over raw arrays
* Always clean up heap-allocated arrays properly
* For your router project: Use contiguous 1D arrays for performance-critical data

</details>

<details>
<summary>Sorting</summary>

`std::sort` is a highly optimized sorting algorithm from the C++ Standard Library with O(N log N) complexity.

Basic Usage:
```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> values = {3, 5, 1, 4, 2};
    
    // Default sorting (ascending)
    std::sort(values.begin(), values.end());
    
    for (int value : values) {
        std::cout << value << " ";  // Output: 1 2 3 4 5
    }
    std::cout << std::endl;
}
```

Different Sorting Strategies
1. Using Standard Function Objects
```cpp
#include <functional>  // For std::greater, std::less

int main() {
    std::vector<int> values = {3, 5, 1, 4, 2};
    
    // Ascending (default behavior)
    std::sort(values.begin(), values.end());                    // 1 2 3 4 5
    std::sort(values.begin(), values.end(), std::less<int>());  // Same as above
    
    // Descending
    std::sort(values.begin(), values.end(), std::greater<int>());  // 5 4 3 2 1
    
    // Output results
    for (int value : values) {
        std::cout << value << " ";
    }
    std::cout << std::endl;
}
```

2. Using Lambda Functions (Most Flexible)
```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> values = {3, 5, 1, 4, 2};
    
    // Custom sorting with lambda
    std::sort(values.begin(), values.end(), [](int a, int b) {
        return a > b;  // Descending order
    });
    // Output: 5 4 3 2 1
    
    // More complex custom sorting
    std::vector<int> values2 = {3, 5, 1, 4, 2};
    std::sort(values2.begin(), values2.end(), [](int a, int b) {
        // Sort by even numbers first, then odd
        if (a % 2 == 0 && b % 2 != 0) return true;   // a even, b odd → a comes first
        if (a % 2 != 0 && b % 2 == 0) return false;  // a odd, b even → b comes first
        return a < b;  // Both same parity → sort normally
    });
    // Output: 2 4 1 3 5 (evens first, then odds, each group sorted)
    
    for (int value : values2) {
        std::cout << value << " ";
    }
    std::cout << std::endl;
}
```

Advanced Custom Sorting Examples
Custom Object Sorting
```cpp
#include <algorithm>
#include <vector>
#include <string>
#include <iostream>

struct Person {
    std::string name;
    int age;
    double salary;
};

int main() {
    std::vector<Person> people = {
        {"Alice", 30, 50000},
        {"Bob", 25, 60000},
        {"Charlie", 35, 45000},
        {"Diana", 28, 55000}
    };
    
    // Sort by age (ascending)
    std::sort(people.begin(), people.end(), [](const Person& a, const Person& b) {
        return a.age < b.age;
    });
    
    std::cout << "Sorted by age:\n";
    for (const auto& person : people) {
        std::cout << person.name << " (" << person.age << ")\n";
    }
    
    // Sort by salary (descending)
    std::sort(people.begin(), people.end(), [](const Person& a, const Person& b) {
        return a.salary > b.salary;
    });
    
    std::cout << "\nSorted by salary (descending):\n";
    for (const auto& person : people) {
        std::cout << person.name << " ($" << person.salary << ")\n";
    }
    
    // Multi-criteria sort: by age, then by name
    std::sort(people.begin(), people.end(), [](const Person& a, const Person& b) {
        if (a.age != b.age) {
            return a.age < b.age;  // Primary: age ascending
        }
        return a.name < b.name;    // Secondary: name ascending
    });
}
```

Key Points Summary:
* `std::sort` is highly efficient (O(N log N))
* Default behavior: ascending order
* Custom sorting via function objects or lambdas
* Return true if first element should come before second
* Lambdas are most flexible for complex sorting logic
* Works with any container that provides random access iterato
</details>


<details>
<summary>Data structures</summary>

Data structures are a universal programming concept, NOT specific to C++! They exist in virtually all programming languages.

What Are Data Structures?
Data structures are ways of organizing, storing, and managing data so that it can be used efficiently. They define the relationship between data, the operations that can be performed on the data, and how the data is stored in memory.

Universal Concept Across Languages:
| Data Structure | C++                | Python          | Java        | JavaScript         |
|----------------|--------------------|-----------------|-------------|--------------------|
| Array          | int arr[5]         | list            | int[]       | Array              |
| Linked List    | Custom class       | -               | LinkedList  | -                  |
| Stack          | std::stack         | list (as stack) | Stack       | Array (as stack)   |
| Queue          | std::queue         | deque           | Queue       | Array (as queue)   |
| Hash Table     | std::unordered_map | dict            | HashMap     | Object/Map         |
| Tree           | Custom class       | -               | TreeMap     | -                  |

Common Data Structures Categories
1. Linear Data Structures
```cpp
// Array - Contiguous memory
int array[5] = {1, 2, 3, 4, 5};

// Linked List - Nodes with pointers
struct Node {
    int data;
    Node* next;
};

// Stack - LIFO (Last In First Out)
std::stack<int> s;
s.push(1); s.push(2); 
s.pop(); // Returns 2

// Queue - FIFO (First In First Out)  
std::queue<int> q;
q.push(1); q.push(2);
q.pop(); // Returns 1
```

2. Hierarchical Data Structures
```cpp
// Binary Tree
struct TreeNode {
    int data;
    TreeNode* left;
    TreeNode* right;
};

// Heap (used in priority queues)
std::priority_queue<int> max_heap;
```

3. Hash-Based Structures:
```cpp
// Hash Table / Dictionary
std::unordered_map<std::string, int> word_count;
word_count["hello"] = 5;

// Set (unique elements)
std::unordered_set<int> unique_numbers;
unique_numbers.insert(42);
```

Each data structure has different time complexities:
| Operation | Array | Linked List | Hash Table | Binary Tree |
|-----------|-------|-------------|------------|-------------|
| Access    | O(1)  | O(n)        | O(1)       | O(log n)    |
| Search    | O(n)  | O(n)        | O(1)       | O(log n)    |
| Insert    | O(n)  | O(1)        | O(1)       | O(log n)    |
| Delete    | O(n)  | O(1)        | O(1)       | O(log n)    |

C++ Standard Library Data Structures:
```cpp
#include <vector>        // Dynamic array
#include <array>         // Fixed-size array
#include <list>          // Doubly-linked list
#include <forward_list>  // Singly-linked list
#include <deque>         // Double-ended queue
#include <stack>         // LIFO stack
#include <queue>         // FIFO queue
#include <set>           // Ordered unique elements
#include <map>           // Ordered key-value pairs
#include <unordered_set> // Hash-based set
#include <unordered_map> // Hash-based map
```
</details>


<details>
<summary>RAII</summary>

RAII (Resource Acquisition Is Initialization) is a fundamental C++ programming technique where resource management is tied to object lifetime.
The Core Idea - "Resource allocation happens during object construction, and deallocation happens during object destruction."

Simple Explanation -
When you create an object, it automatically acquires resources. When the object goes out of scope, it automatically releases those resources. No manual cleanup needed!

Without RAII (The Problem):
```cpp
#include <iostream>

void riskyFunction() {
    int* array = new int[1000];  // Resource acquisition
    
    // ... use the array ...
    
    if (some_condition) {
        return;  // ❌ MEMORY LEAK! delete[] never called
    }
    
    if (another_condition) {
        throw std::runtime_error("Error!");  // ❌ MEMORY LEAK!
    }
    
    delete[] array;  // This might not be reached!
}
```

With RAII (The Solution):
```cpp
#include <vector>
#include <iostream>

void safeFunction() {
    std::vector<int> array(1000);  // Resource acquisition in constructor
    
    // ... use the array ...
    
    if (some_condition) {
        return;  // ✅ NO LEAK! array destructor automatically called
    }
    
    if (another_condition) {
        throw std::runtime_error("Error!");  // ✅ NO LEAK! destructor called during stack unwinding
    }
    
    // ✅ NO MANUAL CLEANUP! Destructor automatically called when function ends
}
```

How RAII Works
1. Constructor Acquires Resources
2. Destructor Releases Resources
3. Automatic cleanup when object goes out of scope

RAII in the Standard Library
Many STL classes use RAII:
* `std::vector`, `std::string` - Manage memory automatically
* `std::ifstream`, `std::ofstream` - Auto-close files
* `std::unique_ptr`, `std::shared_ptr` - Auto-delete memory
* `std::lock_guard`, `std::unique_lock` - Auto-unlock mutexes
* `std::thread` - Can be joined in destructor (with careful design)

RAII Benefits
* Exception Safety - Resources always cleaned up, even if exceptions occur
* No Resource Leaks - Impossible to forget cleanup
* Clean Code - No manual delete, close(), unlock() calls
* Deterministic Cleanup - You know exactly when resources are freed

RAII Rule of Thumb
* For every resource (memory, files, sockets, locks), create a class where:
* Constructor acquires the resource
* Destructor releases the resource
* Use the class instead of manual resource management

RAII is why C++ doesn't need garbage collection - the language guarantees cleanup through destructors!
</details>

<details>
<summary>Type Punning</summary>

Type punning allows you to interpret memory as different types, bypassing C++'s strict type system for low-level operations.

Example 1: Dangerous Memory Reinterpretation
```cpp
#include <iostream>

int main() {
    int a = 50;
    
    // Safe conversion - implicit type conversion
    double safe_value = a;  // int → double conversion
    std::cout << "Safe conversion: " << safe_value << std::endl;  // 50.0
    
    // DANGEROUS: Type punning - reinterpreting memory
    double& dangerous_value = *(double*)&a;  // Treat int memory as double
    std::cout << "Dangerous reinterpretation: " << dangerous_value << std::endl;
    // Output: garbage value! We're reading 8 bytes from a 4-byte int
    
    // VERY DANGEROUS: Writing past allocated memory
    dangerous_value = 0.0;  // ❌ Writes 8 bytes into 4-byte space!
    // This corrupts memory and causes undefined behavior
}
```

What's Happening in Memory:
```
Memory layout:
[0x1000: a (int)] = 50 (4 bytes)
[0x1004: ???]     = garbage (next 4 bytes)

When we do *(double*)&a:
- We read 8 bytes starting at 0x1000
- First 4 bytes: 50 (our int)
- Next 4 bytes: garbage memory
- Result: garbage double value
```

Example 2: Struct Memory Layout Access
```cpp
#include <iostream>

struct Entity {
    int x, y;  // 8 bytes total (two 4-byte integers)
};

int main() {
    Entity e = {5, 8};
    
    // Method 1: Access as array (common type punning)
    int* position = (int*)&e;  // Treat Entity memory as int array
    std::cout << "Array access: " << position[0] << ", " << position[1] << std::endl;
    // Output: 5, 8
    
    // Method 2: Manual byte offset calculation
    int y = *(int*)((char*)&e + 4);  // Go 4 bytes forward from start
    std::cout << "Manual offset: y = " << y << std::endl;
    // Output: 8
    
    // Visualize memory layout:
    std::cout << "Memory layout:\n";
    std::cout << "&e: " << &e << " (Entity start)\n";
    std::cout << "&e.x: " << &e.x << " (offset 0)\n"; 
    std::cout << "&e.y: " << &e.y << " (offset 4)\n";
}
```

Memory Layout Visualization:
```
Entity e in memory:
[0x1000: e.x] = 5    (4 bytes)
[0x1004: e.y] = 8    (4 bytes)

position[0] → reads 0x1000-0x1003 = 5
position[1] → reads 0x1004-0x1007 = 8
```

Example 3: Safe Struct Access Method
```cpp
#include <iostream>

struct Entity {
    int x, y;
    
    // Safe method to get position array
    int* getPositions() {
        return &x;  // Returns pointer to first member
    }
};

int main() {
    Entity e = {5, 8};
    
    // Safe access through method
    int* position = e.getPositions();
    std::cout << "Original: " << position[0] << ", " << position[1] << std::endl;
    
    // Modify through the pointer
    position[0] = 2;  // Changes e.x to 2
    position[1] = 3;  // Changes e.y to 3
    
    std::cout << "Modified: " << e.x << ", " << e.y << std::endl;
    // Output: 2, 3
}
```

Safe vs Unsafe Type Punning
Unsafe Type Punning (Avoid!)
```cpp
// ❌ DANGEROUS - different sizes
int a = 50;
double& d = *(double*)&a;  // Reading/writing wrong amount of memory

// ❌ DANGEROUS - aliasing violations
float f = 1.0f;
int i = *(int*)&f;  // Strict aliasing violation
```

Safe Type Punning (When Carefully Used)
```cpp
// ✅ SAFE - same size, compatible types
struct Vec2 { float x, y; };
float array[2] = {1.0f, 2.0f};
Vec2* vec = (Vec2*)array;  // Same memory layout

// ✅ SAFE - character types can alias anything
int value = 42;
char* bytes = (char*)&value;  // Examine individual bytes

// ✅ SAFE - unions for type punning (C++ specific rules)
union Converter {
    float f;
    int i;
};
```

Practical Use Cases for Type Punning
1. Network Packet Parsing
```cpp
#include <cstdint>
#include <iostream>

// Network packet header
struct EthernetHeader {
    uint8_t dest_mac[6];
    uint8_t src_mac[6];
    uint16_t ethertype;
};

void parsePacket(const char* raw_data) {
    // Type punning: treat raw bytes as structured header
    const EthernetHeader* header = (const EthernetHeader*)raw_data;

    std::cout << "Ethertype: 0x" << std::hex << header->ethertype << std::endl;

    // Safe because we know the raw data matches the struct layout
}
```

2. Performance Optimization
```cpp
#include <cstring>

// Convert float to int representation for bit manipulation
float fastInverseSquareRoot(float number) {
    // Famous Quake III algorithm using type punning
    long i;
    float x2, y;
    const float threehalfs = 1.5F;
    
    x2 = number * 0.5F;
    y = number;
    
    // Type punning: treat float as long for bit manipulation
    i = *(long*)&y;            // Evil floating point bit level hacking
    i = 0x5f3759df - (i >> 1); // What the fuck?
    y = *(float*)&i;
    
    y = y * (threehalfs - (x2 * y * y)); // 1st iteration
    return y;
}
```

Modern C++ Safe Alternatives
Using std::memcpy (Safe)
```cpp
#include <cstring>

float floatValue = 3.14f;
int intRepresentation;

// Safe: no aliasing violations
std::memcpy(&intRepresentation, &floatValue, sizeof(float));

// Manipulate bits
intRepresentation &= 0x7FFFFFFF;  // Clear sign bit

// Copy back
std::memcpy(&floatValue, &intRepresentation, sizeof(float));
```

Using std::bit_cast (C++20 - Safest)
```cpp
#include <bit>
#include <cstdint>

float floatValue = 3.14f;

// Type-safe punning
auto intRepresentation = std::bit_cast<uint32_t>(floatValue);

// Manipulate
intRepresentation &= 0x7FFFFFFF;

// Convert back
floatValue = std::bit_cast<float>(intRepresentation);
```

Key Points Summary
* Type punning = interpreting memory as different types
* Dangerous when types have different sizes or alignment
* Use carefully for low-level operations like network protocols
* Avoid strict aliasing violations - undefined behavior
* Prefer safe alternatives: std::memcpy, std::bit_cast, unions
* Common uses: protocol parsing, binary I/O, performance optimizations

</details>

<details>
<summary>Unions</summary>

Unions allow different data types to share the same memory location. Only one member can be active at a time, and they're exactly the same size in memory.

Example 1: Simple Type Punning
```cpp
#include <iostream>

struct MyUnion {
    union {
        float a;  // 4 bytes
        int b;    // 4 bytes - shares same memory as 'a'
    };
};

int main() {
    MyUnion u;

    u.a = 2.0f;  // Store as float
    std::cout << "As float: " << u.a << std::endl;        // 2.0
    std::cout << "As int: " << u.b << std::endl;          // Garbage! Bit pattern of 2.0f as int

    u.b = 42;    // Store as int (overwrites the float)
    std::cout << "As float: " << u.a << std::endl;        // Garbage! Bit pattern of 42 as float
    std::cout << "As int: " << u.b << std::endl;          // 42

    // Memory visualization:
    std::cout << "Size of union: " << sizeof(u) << " bytes" << std::endl;  // 4 bytes
    std::cout << "Address of u.a: " << &u.a << std::endl;
    std::cout << "Address of u.b: " << &u.b << std::endl;  // Same address!
}
```

Memory Layout:
```
Union Memory (4 bytes):
[Byte 0-3]: Either float OR int data

When u.a = 2.0f:
Memory: [0x40 0x00 0x00 0x00] (IEEE 754 representation of 2.0f)

When we read u.b:
We interpret [0x40 0x00 0x00 0x00] as int = 1073741824
```

Practical Union Example: Vector4 as Two Vector2s
Example 2: Structured Memory Aliasing
```cpp
#include <iostream>

struct Vector2 {
    float x, y;
    
    void print() const {
        std::cout << "(" << x << ", " << y << ")" << std::endl;
    }
};

struct Vector4 {
    union {
        // First view: as 4 separate floats
        struct {
            float x, y, z, w;
        };
        
        // Second view: as two Vector2 objects
        struct {
            Vector2 a, b;  // a = (x,y), b = (z,w)
        };
    };
    
    void print() const {
        std::cout << "As floats: " << x << ", " << y << ", " << z << ", " << w << std::endl;
        std::cout << "As Vector2s: ";
        a.print();
        std::cout << " and ";
        b.print();
    }
};

int main() {
    Vector4 vector = {1.0f, 2.0f, 3.0f, 4.0f};
    
    std::cout << "Initial state:" << std::endl;
    vector.print();
    // Output:
    // As floats: 1, 2, 3, 4
    // As Vector2s: (1, 2) and (3, 4)
    
    // Modify through float interface
    vector.x = 10.0f;
    vector.z = 30.0f;
    
    std::cout << "\nAfter modifying x and z:" << std::endl;
    vector.print();
    // Output:
    // As floats: 10, 2, 30, 4  
    // As Vector2s: (10, 2) and (30, 4)
    
    // Modify through Vector2 interface
    vector.a.x = 100.0f;  // Same as vector.x = 100.0f
    vector.b.y = 400.0f;  // Same as vector.w = 400.0f
    
    std::cout << "\nAfter modifying through Vector2:" << std::endl;
    vector.print();
    // Output:
    // As floats: 100, 2, 30, 400
    // As Vector2s: (100, 2) and (30, 400)
}
```

Memory Layout Visualization:
```
Vector4 Memory (16 bytes):
[0-3]: x / a.x
[4-7]: y / a.y  
[8-11]: z / b.x
[12-15]: w / b.y

Both views access the SAME memory, just with different type interpretations!
```

More Union Examples
Example 3: Network Protocol Data:
```cpp
#include <iostream>
#include <cstdint>

struct IPAddress {
    union {
        uint32_t as_int;           // 4-byte integer representation
        uint8_t as_bytes[4];       // 4 individual bytes
        struct {
            uint8_t a, b, c, d;    // Dotted decimal notation
        };
    };
    
    void print() const {
        std::cout << "As int: " << as_int << std::endl;
        std::cout << "As bytes: " 
                  << (int)as_bytes[0] << "." << (int)as_bytes[1] << "."
                  << (int)as_bytes[2] << "." << (int)as_bytes[3] << std::endl;
        std::cout << "As struct: "
                  << (int)a << "." << (int)b << "." << (int)c << "." << (int)d << std::endl;
    }
};

int main() {
    IPAddress ip;
    ip.as_int = 0xC0A80101;  // 192.168.1.1 in hex
    
    ip.print();
    // Output:
    // As int: 3232235777
    // As bytes: 192.168.1.1
    // As struct: 192.168.1.1
    
    // Modify through different interfaces
    ip.as_bytes[3] = 100;  // Change last octet to 100
    std::cout << "\nAfter modification: ";
    std::cout << (int)ip.a << "." << (int)ip.b << "." << (int)ip.c << "." << (int)ip.d << std::endl;
    // Output: 192.168.1.100
}
```

Example 4: Safe Float Bit Manipulation
```cpp
#include <iostream>
#include <cstdint>

struct FloatConverter {
    union {
        float as_float;
        uint32_t as_bits;
        
        struct {
            uint32_t mantissa : 23;  // Bits 0-22: mantissa
            uint32_t exponent : 8;   // Bits 23-30: exponent  
            uint32_t sign : 1;       // Bit 31: sign
        } parts;
    };
    
    void analyze(float value) {
        as_float = value;
        
        std::cout << "Float: " << as_float << std::endl;
        std::cout << "Bits: 0x" << std::hex << as_bits << std::dec << std::endl;
        std::cout << "Sign: " << parts.sign << " (0=positive, 1=negative)" << std::endl;
        std::cout << "Exponent: " << parts.exponent << " (biased)" << std::endl;
        std::cout << "Mantissa: " << parts.mantissa << std::endl;
        std::cout << "---" << std::endl;
    }
};

int main() {
    FloatConverter converter;
    
    converter.analyze(1.0f);
    converter.analyze(-2.5f);
    converter.analyze(0.0f);
}
```

Modern C++17: Type-Safe Unions
Example 5: std::variant (C++17)
```cpp
#include <variant>
#include <iostream>
#include <string>

// Type-safe union alternative
using NetworkData = std::variant<int, float, std::string>;

void processData(const NetworkData& data) {
    // Visit pattern - type-safe way to handle multiple types
    std::visit([](auto&& arg) {
        using T = std::decay_t<decltype(arg)>;
        if constexpr (std::is_same_v<T, int>) {
            std::cout << "Processing int: " << arg << std::endl;
        } else if constexpr (std::is_same_v<T, float>) {
            std::cout << "Processing float: " << arg << std::endl;
        } else if constexpr (std::is_same_v<T, std::string>) {
            std::cout << "Processing string: " << arg << std::endl;
        }
    }, data);
}

int main() {
    NetworkData data1 = 42;
    NetworkData data2 = 3.14f;
    NetworkData data3 = std::string("Hello");
    
    processData(data1);
    processData(data2); 
    processData(data3);
}
```

Key Points About Unions
1. Memory Sharing
```cpp
union MyUnion {
    int a;      // 4 bytes
    float b;    // 4 bytes
    char c[4];  // 4 bytes
};
// Total size = 4 bytes (largest member), all members share same memory
```

2. Only One Active Member
```cpp
union Data {
    int i;
    float f;
};

Data d;
d.i = 42;    // i is active
// d.f is undefined here!
d.f = 3.14f; // f is active, i is now undefined
```

3. Anonymous Unions in Structs
```cpp
struct Container {
    union {  // Anonymous union - members become struct members
        int x;
        float y;
    };
    // Can access directly: container.x or container.y
};
```

4. Limitations
* Cannot have virtual functions
* Cannot inherit or be inherited
* Cannot contain non-trivial types (like std::string) in most cases

Practical Use Cases for Router Project
Packet Header Interpretation
```cpp
#include <cstdint>

struct EthernetPacket {
    union {
        uint8_t raw_data[64];  // Raw packet bytes
        
        struct {
            uint8_t dest_mac[6];
            uint8_t src_mac[6];
            uint16_t ethertype;
            uint8_t payload[52];  // Rest of packet
        } fields;
    };
    
    bool isIPv4() const {
        return fields.ethertype == 0x0800;  // IPv4 ethertype
    }
    
    bool isARP() const {
        return fields.ethertype == 0x0806;  // ARP ethertype  
    }
};

void processPacket(const EthernetPacket& packet) {
    if (packet.isIPv4()) {
        // Process as IP packet using packet.fields
    } else if (packet.isARP()) {
        // Process as ARP packet
    }
    // Can also access raw bytes: packet.raw_data
}
```

Summary
* Unions allow multiple interpretations of the same memory
* Only one member can be active at a time
* Useful for: protocol parsing, memory optimization, type punning
* Dangerous if used incorrectly - can easily cause undefined behavior
* Modern C++ offers safer alternatives like std::variant

Use unions carefully and only when you need low-level memory control!

</details>


<details>
<summary>Virtual desctructors</summary>

Virtual destructors ensure that when you delete an object through a base class pointer, the complete destruction chain (base + derived) is executed.

The Problem: Without Virtual Destructor
```cpp
#include <iostream>

class Base {
public:
    Base() { std::cout << "Base Constructor\n"; }
    ~Base() { std::cout << "Base Destructor\n"; }  // ❌ NON-virtual destructor
};

class Derived : public Base {
private:
    int* large_array;  // Simulating resource that needs cleanup

public:
    Derived() {
        std::cout << "Derived Constructor\n";
        large_array = new int[1000];  // Allocate resource
    }

    ~Derived() {
        std::cout << "Derived Destructor\n";
        delete[] large_array;  // Cleanup resource - THIS MAY NOT BE CALLED!
    }
};

int main() {
    std::cout << "=== Case 1: Direct derived pointer ===\n";
    Derived* derived = new Derived();
    delete derived;
    // Output:
    // Base Constructor
    // Derived Constructor
    // Derived Destructor
    // Base Destructor
    // ✅ Proper cleanup - all destructors called
    
    std::cout << "\n=== Case 2: Polymorphic base pointer ===\n";
    Base* poly = new Derived();  // Polymorphic usage
    delete poly;
    // Output:
    // Base Constructor
    // Derived Constructor
    // Base Destructor
    // ❌ MEMORY LEAK! Derived destructor NOT called!
    // ❌ large_array never deleted!
}
```

The Solution: With Virtual Destructor
```cpp
#include <iostream>

class Base {
public:
    Base() { std::cout << "Base Constructor\n"; }
    virtual ~Base() { std::cout << "Base Destructor\n"; }  // ✅ VIRTUAL destructor
};

class Derived : public Base {
private:
    int* large_array;
    
public:
    Derived() { 
        std::cout << "Derived Constructor\n";
        large_array = new int[1000];
    }
    
    ~Derived() override {  // ✅ override keyword for clarity
        std::cout << "Derived Destructor\n";
        delete[] large_array;  // ✅ This WILL be called now
    }
};

int main() {
    std::cout << "=== With Virtual Destructor ===\n";
    Base* poly = new Derived();
    delete poly;
    // Output:
    // Base Constructor
    // Derived Constructor
    // Derived Destructor  ← ✅ Now called!
    // Base Destructor
    // ✅ No memory leak - proper cleanup!
}
```

How Virtual Destructors Work
Virtual Table (vtable) Mechanism:
```
Without virtual destructor:
Base* → Base::~Base()  ← Only base destructor in vtable

With virtual destructor:  
Base* → Derived::~Derived() → Base::~Base()  ← Complete chain in vtable
```

Destruction Process:
1. Virtual call to the most derived destructor
2. Derived destructor executes + calls base destructor
3. Base destructor executes
4. Memory freed

Example : Network Connection Hierarchy
```cpp
#include <iostream>
#include <memory>

class NetworkConnection {
public:
    NetworkConnection() { 
        std::cout << "NetworkConnection: Establishing connection...\n"; 
    }
    
    virtual ~NetworkConnection() {  // ✅ Virtual destructor
        std::cout << "NetworkConnection: Closing connection...\n";
    }
    
    virtual void sendData(const std::string& data) = 0;
};

class TCPConnection : public NetworkConnection {
private:
    int socket_fd;
    
public:
    TCPConnection() {
        // Simulate TCP connection setup
        socket_fd = 42;
        std::cout << "TCPConnection: Socket " << socket_fd << " created\n";
    }
    
    ~TCPConnection() override {
        // Cleanup TCP-specific resources
        std::cout << "TCPConnection: Closing socket " << socket_fd << "\n";
    }
    
    void sendData(const std::string& data) override {
        std::cout << "TCPConnection: Sending '" << data << "' via socket\n";
    }
};

class UDPConnection : public NetworkConnection {
private:
    int socket_fd;
    
public:
    UDPConnection() {
        // Simulate UDP connection setup  
        socket_fd = 99;
        std::cout << "UDPConnection: Socket " << socket_fd << " created\n";
    }
    
    ~UDPConnection() override {
        // Cleanup UDP-specific resources
        std::cout << "UDPConnection: Closing socket " << socket_fd << "\n";
    }
    
    void sendData(const std::string& data) override {
        std::cout << "UDPConnection: Sending '" << data << "' via datagram\n";
    }
};

void communicate(NetworkConnection* connection) {
    connection->sendData("Hello Network");
    delete connection;  // ✅ Correct cleanup regardless of actual type
}

int main() {
    std::cout << "=== TCP Communication ===\n";
    communicate(new TCPConnection());
    
    std::cout << "\n=== UDP Communication ===\n"; 
    communicate(new UDPConnection());
}
```

When Virtual Destructors Are Critical
Rule of Thumb:
* Use virtual destructor if your class has ANY virtual functions
* Use virtual destructor if you intend to inherit from the class
* Use virtual destructor if you delete objects through base pointers

Good Practice:
```cpp
class Base {
public:
    Base() = default;
    virtual ~Base() = default;  // Virtual destructor
    
    // Other virtual functions...
    virtual void doSomething() = 0;
};

// OR for non-polymorphic base:
class FinalClass final {  // 'final' prevents inheritance
public:
    FinalClass() = default;
    ~FinalClass() = default;  // No need for virtual
};
```

Modern C++ Best Practices
Using Smart Pointers with Virtual Destructors
```cpp
#include <memory>

class Base {
public:
    virtual ~Base() = default;
};

class Derived : public Base {
public:
    ~Derived() override = default;
};

int main() {
    // Smart pointers + virtual destructors = safe polymorphism
    std::unique_ptr<Base> obj = std::make_unique<Derived>();
    
    // When obj goes out of scope:
    // 1. Derived destructor called (virtual dispatch works)
    // 2. Base destructor called  
    // 3. Memory automatically freed
    // ✅ No manual delete, no memory leaks!
}
```

Interface Classes Must Have Virtual Destructors
```cpp
class NetworkInterface {
public:
    virtual ~NetworkInterface() = default;  // ✅ Essential for interface
    
    virtual bool connect() = 0;
    virtual void disconnect() = 0;
    virtual void sendPacket(const Packet& p) = 0;
};

class EthernetInterface : public NetworkInterface {
public:
    ~EthernetInterface() override = default;
    
    // Implement pure virtual functions...
};
```

Key Takeaways
* Virtual destructors ensure complete object destruction through base pointers
* Without virtual destructor, derived class cleanup may be skipped
* Memory/resource leaks can occur without virtual destructors
* Use virtual destructors in base classes intended for polymorphism
* Combine with smart pointers for automatic, exception-safe cleanup

The Golden Rule
If you delete an object of a derived class through a pointer to its base class, the base class must have a virtual destructor.
For router project, any base classes representing network components, connections, or handlers should have virtual destructors to ensure proper resource cleanup!
</details>


<details>
<summary>Casting</summary>

C++ provides several casting operators that are safer and more specific than C-style casts.

1. C-Style Cast vs C++ Casts
C-Style Cast (many use these more than the C++ style casts)
```cpp
#include <iostream>

int main() {
    double value = 5.25;
    
    // C-style cast - dangerous, does whatever conversion it can
    int a = (int)value + 5.3;  // Truncates 5.25 → 5, result: 10.3
    std::cout << "C-style cast result: " << a << std::endl;
    
    // Problem: C-style casts are too powerful and can do dangerous things
    const int x = 10;
    int* y = (int*)&x;  // ❌ Removes const-ness - undefined behavior!
    *y = 20;            // Modifying const variable - dangerous!
}
```

C++ Style Casts (Recommended)
```cpp
#include <iostream>

int main() {
    double value = 5.25;
    
    // static_cast - safe, explicit conversion
    int a = static_cast<int>(value) + 5.3;  // Truncates 5.25 → 5, result: 10.3
    std::cout << "static_cast result: " << a << std::endl;
    
    // const int x = 10;
    // int* y = static_cast<int*>(&x);  // ❌ Compiler error! Won't remove const
}
```

2. C++ Casting Operators
C++ provides 4 specific casting operators for different purposes:
`static_cast` - Safe, Well-Defined Conversions
```cpp
#include <iostream>

class Base {
public:
    virtual ~Base() = default;
};

class Derived : public Base {
public:
    void specificMethod() { std::cout << "Derived method\n"; }
};

int main() {
    // 1. Numeric conversions
    double d = 3.14;
    int i = static_cast<int>(d);  // 3 - explicit conversion
    std::cout << "double to int: " << i << std::endl;
    
    // 2. Pointer upcast in inheritance hierarchy
    Derived* derived = new Derived();
    Base* base = static_cast<Base*>(derived);  // Safe upcast
    
    // 3. void* to specific type
    void* void_ptr = derived;
    Derived* back = static_cast<Derived*>(void_ptr);
    
    delete derived;
}
```

`dynamic_cast` - Safe Runtime Type Checking
```cpp
#include <iostream>
#include <typeinfo>

class Base {
public:
    virtual ~Base() = default;  // Must have virtual functions for dynamic_cast
};

class Derived : public Base {
public:
    void derivedMethod() { std::cout << "Derived specific method\n"; }
};

class Unrelated {};

int main() {
    Derived* derived = new Derived();
    Base* base = derived;  // Base pointer to Derived object
    
    // Safe downcast - checks at runtime if cast is valid
    Derived* back_to_derived = dynamic_cast<Derived*>(base);
    if (back_to_derived) {
        std::cout << "Downcast successful!\n";
        back_to_derived->derivedMethod();
    } else {
        std::cout << "Downcast failed!\n";
    }
    
    // Try casting to unrelated type
    Unrelated* unrelated = dynamic_cast<Unrelated*>(base);
    if (!unrelated) {
        std::cout << "Cast to unrelated type failed (as expected)\n";
    }
    
    // With references (throws exception on failure)
    try {
        Derived& derived_ref = dynamic_cast<Derived&>(*base);
        derived_ref.derivedMethod();
    } catch (const std::bad_cast& e) {
        std::cout << "Bad cast: " << e.what() << std::endl;
    }
    
    delete derived;
}
```

`const_cast` - Add/Remove const qualifier
```cpp
#include <iostream>

void printMessage(const std::string& message) {
    // message is const - we can't modify it
    std::cout << "Message: " << message << std::endl;
    
    // But if we REALLY need to modify it (rare case):
    std::string& mutable_msg = const_cast<std::string&>(message);
    mutable_msg += " (modified)";
    // ⚠️ DANGEROUS: This is undefined behavior if original was const!
}

void legacyFunction(char* str) {
    // Old C function that doesn't use const
    std::cout << "Legacy: " << str << std::endl;
}

int main() {
    std::string msg = "Hello";
    printMessage(msg);
    
    // Safe usage: removing const from non-const object
    const std::string const_msg = "Const message";
    legacyFunction(const_cast<char*>(const_msg.c_str()));  // ⚠️ Still dangerous!
    
    // Better pattern: only use const_cast when you know the object isn't really const
    std::string non_const_msg = "Non-const";
    const std::string& const_ref = non_const_msg;  // Const reference to non-const object
    std::string& safe_mutable = const_cast<std::string&>(const_ref);
    safe_mutable += " - safely modified";
    std::cout << "Result: " << non_const_msg << std::endl;
}
```

`reinterpret_cast` - Low-Level Bit Pattern Reinterpretation
```cpp
#include <iostream>
#include <cstdint>

int main() {
    // 1. Pointer to integer and back
    int x = 42;
    std::cout << "Original value: " << x << std::endl;
    
    // Convert pointer to integer (memory address)
    uintptr_t address = reinterpret_cast<uintptr_t>(&x);
    std::cout << "Memory address as integer: " << address << std::endl;
    
    // Convert back to pointer
    int* ptr = reinterpret_cast<int*>(address);
    std::cout << "Value through reinterpreted pointer: " << *ptr << std::endl;
    
    // 2. Different pointer types (dangerous!)
    double d = 3.14159;
    int* int_ptr = reinterpret_cast<int*>(&d);
    std::cout << "Double bits as int: " << *int_ptr << " (garbage!)\n";
    
    // 3. Network packet parsing (practical use case)
    struct EthernetHeader {
        uint8_t dest_mac[6];
        uint8_t src_mac[6];
        uint16_t ethertype;
    };
    
    char packet_buffer[1500];
    // Treat raw buffer as structured header
    EthernetHeader* header = reinterpret_cast<EthernetHeader*>(packet_buffer);
    // Now we can access header->dest_mac, header->src_mac, etc.
}
```


3. Comparison of C++ Casts

| Cast Type         | Purpose                        | Safety              | Compile-time/Runtime |
|-------------------|--------------------------------|---------------------|----------------------|
| static_cast       | Well-defined conversions       | ✅ Safe             | Compile-time         |
| dynamic_cast      | Polymorphic type checking      | ✅ Very Safe        | Runtime              |
| const_cast        | Add/remove const               | ⚠️ Dangerous        | Compile-time         |
| reinterpret_cast  | Low-level bit reinterpretation | ❌ Very Dangerous   | Compile-time         |

4. Practical Examples for Router Project
Network Packet Processing
```cpp
#include <iostream>
#include <cstdint>
#include <cstring>

struct IPHeader {
    uint8_t version_ihl;
    uint8_t dscp_ecn;
    uint16_t total_length;
    uint16_t identification;
    // ... more fields
};

class PacketProcessor {
public:
    void processPacket(const char* raw_data, size_t length) {
        // reinterpret_cast for protocol parsing
        const IPHeader* ip_header = reinterpret_cast<const IPHeader*>(raw_data);
        
        // Check IP version safely
        uint8_t version = (ip_header->version_ihl >> 4) & 0x0F;
        if (version == 4) {
            processIPv4Packet(ip_header);
        } else if (version == 6) {
            processIPv6Packet(raw_data);  // Different header format
        }
    }
    
private:
    void processIPv4Packet(const IPHeader* header) {
        std::cout << "Processing IPv4 packet, length: " 
                  << ntohs(header->total_length) << std::endl;
    }
    
    void processIPv6Packet(const char* raw_data) {
        // IPv6 has different header structure
        std::cout << "Processing IPv6 packet" << std::endl;
    }
};
```
5. When to Use Each Cast
Use static_cast for:
* Numeric conversions
* Upcasts in inheritance
* Well-defined pointer conversions

Use dynamic_cast for:
* Safe downcasts in polymorphic hierarchies
* Runtime type checking
* When you need to check if cast is valid

Use const_cast for:
* Calling legacy APIs that don't use const
* Only when you're sure the object isn't really const

Use reinterpret_cast for:
* Low-level system programming
* Protocol parsing
* Only when you fully understand the memory layout

Key Takeaways
* Prefer C++ casts over C-style casts - they're safer and more explicit
* `static_cast` - general purpose, safe conversions
* `dynamic_cast` - safe runtime type checking (requires virtual functions)
* `const_cast` - remove const (use very carefully!)
* `reinterpret_cast` - low-level bit manipulation (most dangerous)

Best Practice Rule
Use the most restrictive cast that gets the job done:
```
static_cast → dynamic_cast → const_cast → reinterpret_cast
     ↑                                        ↑
  Safest                                Most Dangerous
```
</details>


<details>
<summary>Precompiled headers</summary>

Precompiled headers (PCH) are pre-processed and pre-compiled header files that dramatically reduce compilation times for large projects.

How Precompiled Headers Work
Without Precompiled Headers:
```
main.cpp → #include <vector> → Parse 10,000+ lines → Compile
other.cpp → #include <vector> → Parse 10,000+ lines → Compile
third.cpp → #include <vector> → Parse 10,000+ lines → Compile
```

With Precompiled Headers:
```
pch.h → #include <vector> → Parse once → Precompile to binary
main.cpp → #include "pch.h" → Use precompiled binary
other.cpp → #include "pch.h" → Use precompiled binary
third.cpp → #include "pch.h" → Use precompiled binary
```

Setting Up Precompiled Headers
Project Structure:
```
MyProject/
├── src/
│   ├── main.cpp
│   ├── other.cpp
│   └── third.cpp
├── include/
│   └── pch.h          // Precompiled header
└── build/
    └── pch.pch        // Generated precompiled binary
```

pch.h (Precompiled Header File)
```cpp
// pch.h - Precompiled header
#pragma once

// Standard Library Headers
#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <unordered_map>
#include <set>
#include <memory>
#include <algorithm>
#include <functional>
#include <chrono>
#include <thread>
#include <mutex>
#include <fstream>
#include <sstream>

// C Headers
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <cmath>

// Project-wide common headers
#include "common_definitions.h"
#include "logger.h"
#include "config.h"

// Third-party libraries (that don't change often)
#include <json.hpp>
// #include <boost/asio.hpp>
```

Source Files Using PCH
```cpp
// main.cpp
#include "pch.h"  // Must be FIRST include!

int main() {
    std::vector<std::string> names = {"Alice", "Bob", "Charlie"};
    std::cout << "Hello from main!\n";
    
    for (const auto& name : names) {
        std::cout << name << std::endl;
    }
    
    return 0;
}
```
```cpp
// network_manager.cpp
#include "pch.h"  // First include - gets all STL headers
#include "network_manager.h"  // Then project-specific headers

class NetworkManager {
private:
    std::unordered_map<std::string, std::shared_ptr<Connection>> connections;
    std::mutex connection_mutex;
    
public:
    void addConnection(const std::string& id, std::shared_ptr<Connection> conn) {
        std::lock_guard<std::mutex> lock(connection_mutex);
        connections[id] = conn;
    }
    
    void broadcast(const std::string& message) {
        std::lock_guard<std::mutex> lock(connection_mutex);
        for (const auto& [id, conn] : connections) {
            conn->send(message);
        }
    }
};
```

Compiler-Specific Setup
GCC/Clang:
```bash
# Generate precompiled header
g++ -std=c++17 pch.h -o pch.h.gch

# Compile with precompiled header
g++ -std=c++17 -include pch.h main.cpp -o main
```

Visual Studio:
Visual Studio automatically handles precompiled headers when you:

1. Set "Precompiled Header" to "Create" for pch.cpp
2. Set "Precompiled Header" to "Use" for other files
3. Include pch.h as first include in each .cpp file

What to Put in Precompiled Headers
```cpp
// Stable standard library headers
#include <vector>
#include <string>
#include <iostream>
#include <memory>

// Stable third-party libraries
#include <json.hpp>
#include <spdlog/spdlog.h>

// Project headers that rarely change
#include "common_types.h"
#include "definitions.h"
#include "version.h"
```

❌ Bad Candidates:
```
// Headers that change frequently
#include "experimental_feature.h"  // Changes often!
#include "debug_utils.h"           // Might change frequently

// Template-heavy headers (can bloat PCH)
#include <boost/mpl.hpp>           // Very template-heavy

// Headers with complex macros
#include "legacy_macros.h"         // Macro madness
```

Benefits of Precompiled Headers
1. Dramatically Faster Compilation
* Without PCH: 45 seconds compile time
* With PCH: 8 seconds compile time (82% faster!)

2. Consistent Include Order
Forces consistent include patterns across the project.

3. Reduced Parse Time
Eliminates redundant parsing of common headers.

Best Practices
1. Include Order
```cpp
// ✅ CORRECT
#include "pch.h"        // Precompiled header first
#include "specific.h"   // Then project headers
#include "another.h"

// ❌ WRONG
#include "specific.h"
#include "pch.h"        // PCH must be first!
```

2. Keep PCH Stable
* Don't include frequently changing headers
* Review PCH contents periodically
* Remove unused headers to reduce size

3. Use in Large Projects
* Small projects may not benefit much
* Large projects with many translation units benefit most
* Ideal for projects with 50+ source files

4. Monitor PCH Size
```bash
# Check PCH file size
ls -la pch.h.gch
# If it's too large (100MB+), consider splitting
```

When Not to Use Precompiled Headers
* Small projects with few files
* Header-only libraries (they're already fast)
* Rapid prototyping where headers change frequently
* Cross-platform projects with very different platform headers


Key Takeaways
* Precompiled headers dramatically reduce compilation times
* Include PCH first in every source file
* Put stable, frequently used headers in PCH
* Avoid frequently changing headers in PCH
* Most beneficial for large projects with many files
* Compiler-specific implementation details
</details>


<details>
<summary>Dynamic casting</summary>


`dynamic_cast` performs runtime type checking to ensure casting between polymorphic types is valid and safe.

Basic Usage
```cpp
#include <iostream>
#include <typeinfo>

class Entity {
public:
    virtual ~Entity() = default;  // Must have virtual functions for dynamic_cast
    virtual void printName() { std::cout << "Entity\n"; }
};

class Player : public Entity {
public:
    void printName() override { std::cout << "Player\n"; }
    void playerSpecific() { std::cout << "Player-specific method\n"; }
};

class Enemy : public Entity {
public:
    void printName() override { std::cout << "Enemy\n"; }
    void enemySpecific() { std::cout << "Enemy-specific method\n"; }
};

int main() {
    Player* player = new Player();
    Entity* actuallyPlayer = player;        // Entity pointer to Player object
    Entity* actuallyEnemy = new Enemy();    // Entity pointer to Enemy object
    
    // ❌ DANGEROUS: C-style cast - no safety check
    Player* dangerousCast = (Player*)actuallyEnemy;
    // dangerousCast->playerSpecific();  // ❌ UNDEFINED BEHAVIOR! May crash
    
    // ✅ SAFE: dynamic_cast with runtime checking
    Player* safeCast1 = dynamic_cast<Player*>(actuallyEnemy);  // Invalid cast
    if (safeCast1) {
        std::cout << "Cast to Player successful\n";
        safeCast1->playerSpecific();
    } else {
        std::cout << "Cast to Player failed (as expected)\n";  // This will execute
    }
    
    // ✅ VALID cast
    Player* safeCast2 = dynamic_cast<Player*>(actuallyPlayer);  // Valid cast
    if (safeCast2) {
        std::cout << "Cast to Player successful\n";  // This will execute
        safeCast2->playerSpecific();  // ✅ Safe to call
    } else {
        std::cout << "Cast to Player failed\n";
    }
    
    delete player;
    delete actuallyEnemy;
}
```

Output:
```
Cast to Player failed (as expected)
Cast to Player successful
Player-specific method
```

How `dynamic_cast` Works
Runtime Type Information (RTTI)
```cpp
#include <iostream>
#include <typeinfo>

class Base {
public:
    virtual ~Base() = default;  // Virtual functions enable RTTI
};

class Derived : public Base {};

int main() {
    Base* base = new Derived();
    
    // dynamic_cast uses RTTI to check actual object type
    std::cout << "Actual type: " << typeid(*base).name() << std::endl;
    
    if (Derived* derived = dynamic_cast<Derived*>(base)) {
        std::cout << "Successful dynamic_cast to Derived\n";
    }
    
    delete base;
}
```

Example: Network Protocol Handler
```cpp
#include <iostream>
#include <memory>
#include <vector>

class NetworkPacket {
public:
    virtual ~NetworkPacket() = default;
    virtual void process() = 0;
};

class DHCPPacket : public NetworkPacket {
public:
    void process() override {
        std::cout << "Processing DHCP packet\n";
    }
    
    void offerIP() {
        std::cout << "Offering IP address to client\n";
    }
};

class DNSPacket : public NetworkPacket {
public:
    void process() override {
        std::cout << "Processing DNS query\n";
    }
    
    void resolveDomain() {
        std::cout << "Resolving domain name\n";
    }
};

class HTTPPacket : public NetworkPacket {
public:
    void process() override {
        std::cout << "Processing HTTP request\n";
    }
    
    void sendResponse() {
        std::cout << "Sending HTTP response\n";
    }
};

class PacketProcessor {
private:
    std::vector<std::unique_ptr<NetworkPacket>> packetQueue;
    
public:
    void addPacket(std::unique_ptr<NetworkPacket> packet) {
        packetQueue.push_back(std::move(packet));
    }
    
    void processQueue() {
        for (auto& packet : packetQueue) {
            packet->process();  // Common processing
            
            // Type-specific processing
            if (auto* dhcp = dynamic_cast<DHCPPacket*>(packet.get())) {
                dhcp->offerIP();  // DHCP-specific logic
            } else if (auto* dns = dynamic_cast<DNSPacket*>(packet.get())) {
                dns->resolveDomain();  // DNS-specific logic
            } else if (auto* http = dynamic_cast<HTTPPacket*>(packet.get())) {
                http->sendResponse();  // HTTP-specific logic
            }
        }
        
        packetQueue.clear();
    }
};

int main() {
    PacketProcessor processor;
    
    processor.addPacket(std::make_unique<DHCPPacket>());
    processor.addPacket(std::make_unique<DNSPacket>());
    processor.addPacket(std::make_unique<HTTPPacket>());
    
    processor.processQueue();
}
```

Performance Considerations
`dynamic_cast` has runtime cost:
```cpp
// Fast: static_cast (compile-time)
Derived* derived = static_cast<Derived*>(base);  // No runtime check

// Slow: dynamic_cast (runtime type checking)  
Derived* derived = dynamic_cast<Derived*>(base);  // Runtime lookup
```

When to Use Each:
```
// Use dynamic_cast when:
// - You're not sure about the actual type
// - Safety is more important than performance
// - Dealing with polymorphic hierarchies

// Use static_cast when:
// - You're certain about the type relationship  
// - Performance is critical
// - Dealing with non-polymorphic types
```

Key Points Summary
* `dynamic_cast` performs runtime type checking
* Returns `nullptr` for pointers when cast fails
* Throws `std::bad_cast` for references when cast fails
* Requires virtual functions in base class (RTTI)
* Safer but slower than `static_cast`
* Use for downcasting in polymorphic hierarchies
* Always check result before using casted pointe

When to Use `dynamic_cast`:

✅ Polymorphic type checking

✅ Safe downcasting when type is unknown

✅ Plugin systems where types are determined at runtime

✅ When safety is more important than performance

When to Avoid dynamic_cast:

❌ Performance-critical code

❌ Non-polymorphic types (won't work)

❌ When you know the exact type (use static_cast)

❌ Frequent operations in tight loops

</details>


<details>
<summary>Benchmarking in C++</summary>

Benchmarking helps measure code performance to identify bottlenecks and optimize critical sections.

Complete Timer Class
```cpp
#include <iostream>
#include <chrono>
#include <string>

class Timer {
public:
    Timer(const std::string& name = "Timer") 
        : m_Name(name), m_Stopped(false) {
        m_StartTimePoint = std::chrono::high_resolution_clock::now();
    }
    
    ~Timer() {
        if (!m_Stopped) { // if timer.stop() is not called, then the destructor will call it
            Stop();
        }
    }
    
    void Stop() {
        auto endTimePoint = std::chrono::high_resolution_clock::now();
        auto start = std::chrono::time_point_cast<std::chrono::microseconds>(m_StartTimePoint).time_since_epoch().count();
        auto end = std::chrono::time_point_cast<std::chrono::microseconds>(endTimePoint).time_since_epoch().count();
        
        auto duration = end - start;
        double ms = duration * 0.001;
        
        std::cout << m_Name << ": " << duration << "us (" << ms << "ms)\n";
        m_Stopped = true;
    }

private:
    std::chrono::time_point<std::chrono::high_resolution_clock> m_StartTimePoint;
    std::string m_Name;
    bool m_Stopped;
};
```

Basic Benchmarking Usage
```cpp
#include <iostream>
#include <vector>

void simpleBenchmark() {
    int value = 0;
    
    {
        Timer timer("Simple Loop");
        for (int i = 0; i < 1000000; i++) {
            value += 2;
        }
    }
    
    std::cout << "Value: " << value << std::endl;
}
```

Preventing Compiler Optimization
The Problem:
```cpp
// Compiler might optimize this entire loop away!
{
    Timer timer("Optimized Away");
    int result = 0;
    for (int i = 0; i < 1000000; i++) {
        result += i;  // Result never used - compiler removes loop!
    }
    // No output of result = loop eliminated
}
```

Solutions:
```cpp
#include <iostream>

void preventOptimization() {
    // Method 1: Use the result
    {
        Timer timer("Method 1 - Use Result");
        int result = 0;
        for (int i = 0; i < 1000000; i++) {
            result += i;
        }
        std::cout << "Result: " << result << std::endl;  // Force usage
    }
    
    // Method 2: volatile keyword
    {
        Timer timer("Method 2 - volatile");
        volatile int result = 0;  // Prevents some optimizations
        for (int i = 0; i < 1000000; i++) {
            result += i;
        }
    }
    
    // Method 3: External function
    {
        Timer timer("Method 3 - External Function");
        int result = 0;
        for (int i = 0; i < 1000000; i++) {
            result += i;
        }
        // Assume doSomething prevents optimization
        // doSomething(result);
    }
}
```

Key Takeaways
* Use RAII timers for automatic measurement
* Prevent compiler optimization of benchmarked code
* Run multiple iterations for statistical significance
* Measure in release mode with optimizations enabled
* Control testing environment for consistent results
* Use `__debugbreak()` for debugging during benchmarking (Visual Studio Code specific instruction)

</details>


<details>
<summary>Structured bindings</summary>

Structured bindings provide a clean, readable way to unpack tuples, pairs, and other structured data.

Before C++17: The Verbose Ways
Method 1: `std::get` with Indexes
```cpp
#include <tuple>
#include <string>
#include <iostream>

std::tuple<std::string, int, std::string> CreatePerson() {
    return {"Cherno", 24, "Game Developer"};
}

int main() {
    auto person = CreatePerson();
    
    // ❌ Verbose and error-prone
    std::string& name = std::get<0>(person);     // Hard to remember indexes
    int age = std::get<1>(person);               // What if order changes?
    std::string& job = std::get<2>(person);      // Easy to mix up indexes
    
    std::cout << name << " is " << age << " years old and works as a " << job << std::endl;
}
```

Method 2: std::tie (Slightly Better)
```cpp
#include <tuple>
#include <string>
#include <iostream>

std::tuple<std::string, int, std::string> CreatePerson() {
    return {"Cherno", 24, "Game Developer"};
}

int main() {
    // ❌ Still verbose - need to pre-declare variables
    std::string name;
    int age;
    std::string job;
    
    std::tie(name, age, job) = CreatePerson();  // Bind to existing variables
    
    std::cout << name << " is " << age << " years old and works as a " << job << std::endl;
}
```

C++17: Structured Bindings (The Modern Way)
Basic Usage
```cpp
#include <tuple>
#include <string>
#include <iostream>

std::tuple<std::string, int, std::string> CreatePerson() {
    return {"Cherno", 24, "Game Developer"};
}

int main() {
    // ✅ Clean and readable - auto-declares variables
    auto [name, age, job] = CreatePerson();
    
    std::cout << name << " is " << age << " years old and works as a " << job << std::endl;
    // Output: Cherno is 24 years old and works as a Game Developer
}
```

What Structured Bindings Work With
1. `std::tuple`, `std::pair`
```cpp
#include <tuple>
#include <pair>
#include <iostream>

auto GetUserStats() {
    return std::make_tuple("Alice", 85.5, 42);  // name, score, level
}

auto GetConnectionInfo() {
    return std::make_pair("192.168.1.1", 8080);  // ip, port
}

int main() {
    // Tuple unpacking
    auto [username, score, level] = GetUserStats();
    std::cout << username << ": Level " << level << ", Score " << score << std::endl;
    
    // Pair unpacking  
    auto [ip, port] = GetConnectionInfo();
    std::cout << "Connecting to " << ip << ":" << port << std::endl;
}
```

2. Arrays
```cpp
#include <iostream>

int main() {
    int coordinates[3] = {10, 20, 30};
    
    auto [x, y, z] = coordinates;  // Unpack array elements
    
    std::cout << "Position: (" << x << ", " << y << ", " << z << ")" << std::endl;
    // Output: Position: (10, 20, 30)
}
```

3. Structs and Classes
```cpp
#include <iostream>
#include <string>

struct Person {
    std::string name;
    int age;
    std::string occupation;
};

struct Point3D {
    double x, y, z;
};

Person CreatePerson() {
    return {"Bob", 30, "Engineer"};
}

Point3D GetPosition() {
    return {5.5, 10.2, 15.8};
}

int main() {
    // Struct unpacking
    auto [name, age, job] = CreatePerson();
    std::cout << name << " is a " << age << "-year-old " << job << std::endl;
    
    auto [x, y, z] = GetPosition();
    std::cout << "3D Position: (" << x << ", " << y << ", " << z << ")" << std::endl;
}
```


Practical Examples:
```cpp
#include <tuple>
#include <string>
#include <iostream>
#include <utility>

// Function returning multiple network settings
auto GetNetworkConfig() {
    return std::make_tuple("192.168.1.1", "255.255.255.0", "8.8.8.8", 1500);
    // ip, subnet, gateway, mtu
}

int main() {
    auto [ip_address, subnet_mask, gateway, mtu] = GetNetworkConfig();
    
    std::cout << "Network Configuration:\n";
    std::cout << "IP: " << ip_address << "\n";
    std::cout << "Subnet: " << subnet_mask << "\n"; 
    std::cout << "Gateway: " << gateway << "\n";
    std::cout << "MTU: " << mtu << "\n";
}
```
</details>

<details>
<summary>How to deal with optional data</summary>

`std::optional` is new in C++17.

Before:
```cpp
#include <iostream>
#include <fstream>

std::string ReadFileAsString(const std::string& filepath, bool& outSuccess) {
    std::ifstream stream(filepath);
    if (stream) {
        std::string result;
        // read file
        stream.close();
        outSuccess = true;
        return result;
    } 
    // what to return if file reading was succesfull?
    outSuccess = false;
    return std::string();
}

int main() {
    bool fileOpenedSuccessfully;
    std::string data = ReadFileAsString("data.txt", fileOpenedSuccessfully);
    if (data != "") {
        // do smth if no data
    }
}
```

After:
```cpp
#include <iostream>
#include <fstream>
#include <optional>

std::optional<std::string> ReadFileAsString(const std::string& filepath) {
    std::ifstream stream(filepath);
    if (stream) {
        std::string result;
        // read file
        stream.close();
        return result;
    } 
    // what to return if file reading was succesfull?
    return {};
}

int main() {
    std::optional<std::string> data = ReadFileAsString("data.txt"); // or use auto for type
    std::string value = data.value_or("Not present"); // if data not present, "Not present" is added as data

    // std::optional<int> count;
    // int c = count.value_or(100);

    if (data) { // or this data.has_value() 
        std::cout << "File read successfully\n";
        // std::string& string = *data; // we can access it like this ?
    } else {
        std::cout << "File read unsuccessfully\n";
    }
}
```
</details>



<details>
<summary>Multiple types of data in a single variable</summary>

This is new in C++17: `std::variant`

```cpp
#include <iostream>
#include <variant>

int main() {
    std::variant<std::string, int> data;
    data = "Cherno";
    // to get data:
    std::cout << std::get<std::string>(data) << "\n";
    data = 2;
    std::cout << std::get<std::int>(data) << "\n";

    // what happens if we mess up and try to access an invalid type? variant returns std::bad_variant_access exception, we can try catch
    // but a better way is to check the mapped index to variant
    data.index() // string returns 0, int returns 1

    // another way:
    auto value = std::get_if<std::string>(&data); // if invalid, returns NULL, valid returns pointer to string
}
```
</details>

<details>
<summary>How to store any data in C++</summary>

`std::any` - new in C++17
`std::variant` - we needed to list the types, for any we do not.

```cpp
#include <any>

int main() {
    std::any data;
    // it can be set to anything
    data = 2;
    data = "Cherno";
    data = std::string("Cherno");

    // if you want to get the data, you need to know the type:
    std::string what = std::any_cast<std::string>(data); // this would throw an exception, because data is const char*, not string
}
```
</details>

<details>
<summary><code>std::async</code></summary>

`std::async` is used for asynchronous task execution and simple parallel processing. It runs a function asynchronously (potentially in a separate thread) and returns a `std::future` that will hold the result.

Basic Syntax
```cpp
#include <iostream>
#include <future>
#include <chrono>

// Example 1: Simple async function
int simpleTask(int x, int y) {
    std::this_thread::sleep_for(std::chrono::seconds(1)); // Simulate work
    return x + y;
}

int main() {
    // Launch async task - may execute in separate thread
    std::future<int> result = std::async(std::launch::async, simpleTask, 10, 20);
    
    // Do other work here while async task runs...
    std::cout << "Doing other work...\n";
    
    // Get the result (blocks until ready)
    int value = result.get();
    std::cout << "Result: " << value << std::endl; // Output: Result: 30
    
    return 0;
}
```

Launch Policies
```cpp
#include <future>
#include <iostream>

int compute(int n) {
    int sum = 0;
    for (int i = 0; i < n; ++i) {
        sum += i;
    }
    return sum;
}

int main() {
    // Option 1: std::launch::async - Run in separate thread
    auto future1 = std::async(std::launch::async, compute, 1000000);
    
    // Option 2: std::launch::deferred - Run lazily when get() is called
    auto future2 = std::async(std::launch::deferred, compute, 1000000);
    
    // Option 3: Let implementation decide (default)
    auto future3 = std::async(compute, 1000000);
    
    std::cout << "Async task launched\n";
    
    // future1 might be running concurrently
    // future2 will only run when we call get()
    int result = future1.get();
    std::cout << "Result: " << result << std::endl;
    
    return 0;
}
```
</details>


<details>
<summary>Singletons</summary>

A Singleton ensures a class has only one instance and provides global access to that instance.
It's useful for organizing global data and functions into a single managed instance.

Basic Singleton Implementation
```cpp
#include <iostream>

class Singleton {
public:
    // Delete copy constructor to prevent creating new instances
    Singleton(Singleton&) = delete;
    
    // Static method to access the single instance
    static Singleton& Get() {
        return s_Instance;  // Returns reference to the static instance
    }
    
    void Function() {
        std::cout << "Singleton function called\n";
    }

private:
    Singleton() {}  // Private constructor prevents external instantiation
    float m_Member = 0.0f;
    static Singleton s_Instance;  // Static instance member
};

// Define the static member (required)
Singleton Singleton::s_Instance;

int main() {
    // Access the singleton instance and call its method
    Singleton::Get().Function();
    return 0;
}
```

Practical Example: Random Number Generator
```cpp
#include <iostream>
#include <random>

class Random {
public:
    Random(Random&) = delete;  // Prevent copying
    
    static Random& Get() {
        return s_Instance;
    }
    
    // Public interface for random number generation
    int Int(int min, int max) {
        std::uniform_int_distribution distribution(min, max);
        return distribution(m_RandomEngine);
    }
    
    float Float(float min, float max) {
        std::uniform_real_distribution distribution(min, max);
        return distribution(m_RandomEngine);
    }

private:
    Random() {
        // Seed with proper random device
        std::random_device rd;
        m_RandomEngine.seed(rd());
    }
    
    std::mt19937 m_RandomEngine;
    static Random s_Instance;
};

Random Random::s_Instance;

int main() {
    // Use the singleton random generator
    std::cout << "Random int: " << Random::Get().Int(1, 100) << std::endl;
    std::cout << "Random float: " << Random::Get().Float(0.0f, 1.0f) << std::endl;
    
    return 0;
}
```

Alternative Implementation (Meyer's Singleton)
```cpp
class MeyerSingleton {
public:
    MeyerSingleton(MeyerSingleton&) = delete;
    
    // Instance created on first call (lazy initialization)
    static MeyerSingleton& Get() {
        static MeyerSingleton instance;
        return instance;
    }
    
    void DoSomething() {
        std::cout << "Meyer's singleton\n";
    }

private:
    MeyerSingleton() = default;
};

int main() {
    MeyerSingleton::Get().DoSomething();
}
```

Key Characteristics
* Private Constructor: Prevents external object creation
* Deleted Copy Constructor: Prevents creating new instances via copying
* Static Instance: Single instance stored as static member
* Static Access Method: Global point of access via Get() method

When to Use Singletons
* Global configuration settings
* Logging systems
* Resource managers (database connections, thread pools)
* Hardware access (printers, audio devices)

Advantages
* Controlled access to single instance
* Reduced global variables by encapsulating related functionality
* Lazy initialization (with Meyer's approach)
* Thread-safe (with proper implementation)

Disadvantages
* Global state can make testing difficult
* Hidden dependencies
* Potential threading issues if not implemented carefully

Important Notes
* Use references (Singleton&) not pointers to prevent null issues
* Consider Meyer's singleton for thread safety in C++11+
* Be cautious of static initialization order issues
* Singletons are essentially fancy global variables - use sparingly
</details>

<details>
<summary>Small string optimization (SSO)</summary>

std::string Memory Allocation
It uses both stack and heap, but the actual character data is typically on the heap.

Small String Optimization (SSO)
Most modern C++ implementations use Small String Optimization:
```cpp
#include <iostream>
#include <string>

int main() {
    std::string short_str = "Austris";  // 7 characters
    std::string long_str = "AustrisAustrisAustrisAustris";  // 28 characters

    std::cout << "Short string capacity: " << short_str.capacity() << std::endl;
    std::cout << "Long string capacity: " << long_str.capacity() << std::endl;

    return 0;
}
```

How It Works
For Small Strings (typically ≤ 15 chars):
```cpp
std::string data = "Austris";  // 7 characters
```
* Stack: The entire string object (including character data) fits in a small buffer within the std::string object itself
* No heap allocation occurs
* Fast construction/destruction

For Large Strings:
```cpp
data = "AustrisAustrisAustrisAustris";  // 28 characters
```
* Stack: The std::string object itself (contains pointer, size, capacity)
* Heap: The actual character data is allocated on the heap
* The stack object contains a pointer to the heap memory

Memory Layout Example
```cpp
#include <iostream>
#include <string>

void analyze_string(const std::string& str, const std::string& name) {
    std::cout << name << ":\n";
    std::cout << "  Content: " << str << "\n";
    std::cout << "  Size: " << str.size() << "\n";
    std::cout << "  Capacity: " << str.capacity() << "\n";
    std::cout << "  Address of string object: " << &str << "\n";
    std::cout << "  Address of data: " << (void*)str.data() << "\n";
    std::cout << "  Is likely on heap: " 
              << ((void*)str.data() < (void*)&str ? "Probably" : "Probably not") 
              << std::endl;
}

int main() {
    std::string short_str = "Hi";
    std::string long_str = "This is a very long string that definitely exceeds SSO buffer";
    
    analyze_string(short_str, "Short string");
    std::cout << "---\n";
    analyze_string(long_str, "Long string");
    
    return 0;
}
```

Resizing Behavior
```cpp
#include <iostream>
#include <string>

int main() {
    std::string data = "Austris";  // Likely SSO - no heap allocation
    
    std::cout << "Initial - Size: " << data.size() 
              << ", Capacity: " << data.capacity() << std::endl;
    
    // This may trigger heap allocation
    data = "AustrisAustrisAustrisAustris";
    
    std::cout << "After reassignment - Size: " << data.size() 
              << ", Capacity: " << data.capacity() << std::endl;
    
    // Growing beyond current capacity
    data += "MoreAndMoreTextToForceReallocation";
    
    std::cout << "After growth - Size: " << data.size() 
              << ", Capacity: " << data.capacity() << std::endl;
    
    return 0;
}
```

What Happens During Resize
1. If new size ≤ current capacity:
* Just update the size and null terminator
* No reallocation needed

2. If new size > current capacity:
* Allocate new, larger buffer on heap
* Copy existing characters to new buffer
* Copy new characters to new buffer
* Delete old buffer (if it was on heap)
* Update pointer, size, and capacity

Demonstration of Resize
```cpp
#include <iostream>
#include <string>

int main() {
    std::string str;
    
    for (int i = 0; i < 10; ++i) {
        size_t old_capacity = str.capacity();
        str += "Chunk";  // Add 5 characters
        
        std::cout << "Size: " << str.size() 
                  << ", Capacity: " << str.capacity();
        
        if (str.capacity() > old_capacity) {
            std::cout << " *** REALLOCATED ***";
        }
        std::cout << std::endl;
    }
    
    return 0;
}
```

Key Points
* Small strings: Entirely on stack (thanks to SSO)
* Large strings: Object on stack, data on heap
* Resizing: May trigger heap allocation and data copying
* Capacity: Usually grows exponentially (e.g., double when needed) to amortize cost
* Implementation-dependent: Exact SSO threshold varies by compiler

So in your example, "Austris" likely uses SSO (stack), while "AustrisAustrisAustrisAustris" likely triggers heap allocation!
</details>



<details>
<summary>Tracking memory allocations</summary>

```cpp
#include <iostream>
#include <memory>

struct AllocationMetrics {
    uint32_t TotalAllocated = 0;
    uint32_t TotalFreed = 0;
    uint32_t CurrentUsage { return TotalAllocated - TotalFreed; };
}

static AlocationMetrics s_AllocationMetrics;

// overriding new operator
void* operator new(size_t size) {
    std::cout << "Allocating " << size << " bytes\n";
    s_AllocationMetrics.TotalAllocated += size;
    return malloc(size);
}

// overriding delete operator
void operator delete(void* memory, size_t size) {
    std::cout << "Freeing " << size << " bytes\n";
    s_AllocationMetrics.TotalFreed += size;
    free(memory);
}

static void PrintMemoryUsage() {
    std::cout << "Mmeory Usage: " << s_AllocationMetrics.CurrentUsage() << " bytes\n";
}

struct Object {
    int x,y,z;
}

int main() {
    std::string name = "Cherno"; // if SSO does not happen, we can see when string is allocated in heap
    PrintMemoryUsage();
    std::unique_ptr<Object> obj = std::make_unique<Object>(); // we also see then the object is allocated on the heap here
    PrintMemoryUsage();
}
```
</details>


<details>
<summary>lvalues and rvalues</summary>
Basic Definitions
* lvalue: Has a memory address, can appear on left side of assignment
* rvalue: Temporary value, no persistent memory address, appears on right side

Example 1: Basic lvalue/rvalue behavior
```cpp
int GetValue() {
    return 10;  // Returns rvalue
}

int& GetValue2() {
    static int value = 10;
    return value;  // Returns lvalue reference
}

int main() {
    int i = 10;        // i is lvalue, 10 is rvalue
    int b = GetValue(); // b is lvalue, GetValue() returns rvalue

    int a = i;         // Both lvalues (copying value)

    // GetValue() = 5;  // ERROR: Can't assign to rvalue

    GetValue2() = 5;   // WORKS: Returns lvalue reference
}
```

Example 2: Function Parameter Passing
```cpp
void SetValue(int value) {}  // Takes by value (accepts both)

void SetValueRef(int& value) {}       // Takes lvalue reference only
void SetValueConstRef(const int& value) {}  // Takes both (const reference)

int main() {
    int i = 10;
    SetValue(i);     // OK: lvalue passed by value
    SetValue(10);    // OK: rvalue passed by value
    
    SetValueRef(i);  // OK: lvalue to lvalue reference
    // SetValueRef(10); // ERROR: rvalue to non-const reference
    
    SetValueConstRef(i);  // OK: lvalue to const reference  
    SetValueConstRef(10); // OK: rvalue to const reference
}
```

Example 3: lvalue and rvalue Reference Overloads
```cpp
void PrintName(const std::string& name) {  // Accepts lvalues
    std::cout << "[lvalue] " << name << std::endl;
}

void PrintName(std::string&& name) {  // Accepts rvalues only
    std::cout << "[rvalue] " << name << std::endl;
}

int main() {
    std::string firstName = "Austris";    // lvalue
    std::string lastName = "Eglitis";     // lvalue  
    std::string fullName = firstName + lastName;  // lvalue
    
    PrintName(fullName);              // Calls lvalue version
    PrintName(firstName + lastName);  // Calls rvalue version (temporary)
    
    PrintName("Literal");             // Calls rvalue version
}
```

Key Rules
lvalues:
* Have persistent memory addresses
* Can be assigned to
* Can have their address taken with &
* Examples: variables, function returning references

rvalues:
* Temporary values
* Cannot be assigned to
* Cannot have address taken
* Examples: literals, function returning by value, temporary expressions

Reference Types:
* `Type&` - lvalue reference (binds to lvalues only)
* `const Type&` - const lvalue reference (binds to both)
* `Type&&` - rvalue reference (binds to rvalues only)

Practical Uses
```cpp
// Move semantics - efficient transfer of resources
class String {
    String(String&& other) {  // rvalue reference
        // Steal resources from 'other'
    }
};

// Perfect forwarding
template<typename T>
void Forward(T&& arg) {  // Universal reference
    // Can forward as lvalue or rvalue
}
```

Quick Reference

| Expression                   | Type    | Can Assign | Can Take Address  |
|------------------------------|---------|------------|-------------------|
| int x = 5                    | lvalue  | ✅         | ✅               |
| x = 10                       | lvalue  | ✅         | ✅               |
| 5                            | rvalue  | ❌         | ❌               |
| x + 1                        | rvalue  | ❌         | ❌               |
| func() (returns value)       | rvalue  | ❌         | ❌               |
| func() (returns reference)   | lvalue  | ✅         | ✅               |
</details>

<details>
<summary>Move semantics</summary>

Move semantics allow us to transfer resources from one object to another instead of copying them.
This is especially useful for expensive operations like memory allocations, file handles, or network connections.

**The Problem: Unnecessary Copies**

Before move semantics, this would create multiple copies:
```cpp
String CreateString() {
    String temp("Hello");
    return temp;  // Before C++11: Copy! After C++11: Move!
}

int main() {
    String s = CreateString();  // Could involve multiple copies
}
```

**The Solution: Move Constructor and Rvalue References**

Example
```cpp
#include <iostream>
#include <cstring>

class String {
public:
    String() = default;
    
    // Regular constructor
    String(const char* string) {
        printf("Created!\n");
        m_Size = strlen(string);
        m_Data = new char[m_Size + 1];  // +1 for null terminator
        memcpy(m_Data, string, m_Size);
        m_Data[m_Size] = '\0';
    }

    // Copy constructor (deep copy)
    String(const String& other) {
        printf("Copied!\n");
        m_Size = other.m_Size;
        m_Data = new char[m_Size + 1];
        memcpy(m_Data, other.m_Data, m_Size + 1);
    }

    // MOVE CONSTRUCTOR - The key to move semantics!
    String(String&& other) noexcept {  // noexcept is important for optimization - noexcept is a promise that a function won't throw exceptions. It's especially important for move operations because of how C++ handles exceptions during moves.
        printf("Moved!\n");

        // STEAL the resources from the other object
        m_Size = other.m_Size;
        m_Data = other.m_Data;  // Just copy the pointer, no new allocation!

        // IMPORTANT: Leave the other object in valid but empty state
        other.m_Size = 0;
        other.m_Data = nullptr;  // So it won't delete our stolen data
    }

    // Move assignment operator
    String& operator=(String&& other) noexcept {
        printf("Move assigned!\n");

        if (this != &other) {  // Self-assignment check - checks if we are not doing: dest = dest(std::move(dest));
            delete[] m_Data;   // Clean up our current resources

            // Steal from other
            m_Size = other.m_Size;
            m_Data = other.m_Data;

            // Reset other
            other.m_Size = 0;
            other.m_Data = nullptr;
        }
        return *this;
    }

    ~String() {
        printf("Destroyed!\n");
        delete[] m_Data;  // Use delete[] for arrays!
    }

    void Print() const {
        if (m_Data) {
            for (uint32_t i = 0; i < m_Size; i++)
                printf("%c", m_Data[i]);
            printf("\n");
        } else {
            printf("(empty string)\n");
        }
    }

private:
    char* m_Data = nullptr;
    uint32_t m_Size = 0;
};

class Entity {
public:
    // Constructor for lvalues (copies)
    Entity(const String& name) : m_Name(name) {  // Calls copy constructor
        printf("Entity created with copy\n");
    }

    // Constructor for rvalues (moves)
    Entity(String&& name) : m_Name(std::move(name)) {  // Calls move constructor (or can write m_Name(String&&(name)))
        printf("Entity created with move\n");
    }

    void PrintName() {
        m_Name.Print();
    }

private:
    String m_Name;
};

int main() {
    printf("=== Example 1: Temporary String ===\n");
    Entity entity1(String("Cherno"));  // String is temporary → moved!
    entity1.PrintName();

    printf("\n=== Example 2: Named String ===\n");
    String name("Austris");
    Entity entity2(name);  // String is named → copied!

    printf("\n=== Example 3: Explicit Move ===\n");
    String anotherName("John");
    Entity entity3(std::move(anotherName));  // Explicit move
    entity3.PrintName();
    
    printf("Original string after move: ");
    anotherName.Print();  // Will print "(empty string)"

    return 0;
}
```

Key Concepts Explained:

1. Rvalue References (`&&`)
```cpp
String(String&& other)  // && means rvalue reference
```
* Binds only to temporary objects (rvalues)
* Signals that the object can be "moved from"
* Examples of rvalues: `String("temp")`, `std::move(x)`, function returns


2. The Move Constructor
```cpp
String(String&& other) noexcept {
    // Steal resources
    m_Size = other.m_Size;
    m_Data = other.m_Data;  // No new allocation!

    // Leave other in valid state
    other.m_Size = 0;
    other.m_Data = nullptr;
}
```

3. `std::move()`
```cpp
Entity entity3(std::move(anotherName));
```
* Doesn't actually move anything - it's just a cast
* Converts lvalue to rvalue reference
* Marks object as "ready to be moved from"

4. Important Rules for Move Operations:

✅ Do:
* Steal resources instead of copying
* Leave source in valid state (usually empty)
* Use noexcept for better performance
* Check for self-assignment

❌ Don't:
* Access moved-from objects (except destruction)
* Forget to nullify source pointers
* Use delete instead of delete[] for arrays


When Move Semantics Happen Automatically:
```cpp
String CreateString() {
    String local("Hello");
    return local;  // Automatically moves (if move constructor exists)
}

String ProcessString(String input) {
    // input can be moved from here
    return input;  // Automatically moves
}

int main() {
    // These all use move semantics:
    String s1 = CreateString();           // Move from return value
    String s2 = String("Temporary");      // Move from temporary
    String s3 = std::move(s1);            // Explicit move
}
```

Summary

Move semantics allow us to:
1. Transfer ownership of resources efficiently
2. Avoid expensive copies of large objects
3. Work with temporary objects optimally
4. Write more performant code with the same safety

Key syntax:
* `Type&&` - rvalue reference
* `std::move()` - cast to rvalue
* Move constructor/assignment - implement resource transfer

Move semantics are fundamental to modern C++ performance and are used extensively in the standard library (`std::vector`, `std::string`, etc.).

</details>

<details>
<summary><code>std::move</code></summary>


```cpp
#include <iostream>
#include <string>

void printName(std::string&& name) {
    std::cout << "Name: " << name << std::endl;
}

int main() {
    std::string data = "Hello";
    
    // Method 1: C-style cast (works but not recommended)
    printName((std::string&&)data);
    
    // Method 2: std::move (recommended - cleaner and safer)
    printName(std::move(data));
    
    return 0;
}
```

`std::move` is essentially just a cast - it doesn't actually "move" anything:
```cpp
// Simplified version of what std::move does:
template<typename T>
constexpr std::remove_reference_t<T>&& move(T&& arg) noexcept {
    return static_cast<std::remove_reference_t<T>&&>(arg);
}
```

So `std::move(data)` is basically:
```cpp
static_cast<std::string&&>(data)
```

More Realistic Examples

Example 1: With Custom Class
```cpp
#include <iostream>

class String {
public:
    String(const char* str) {
        std::cout << "Created: " << str << std::endl;
    }
    
    String(String&& other) noexcept {
        std::cout << "Moved!" << std::endl;
    }
};

void processString(String&& str) {
    std::cout << "Processing rvalue string" << std::endl;
}

int main() {
    String data = "Hello";
    
    processString(std::move(data));  // Calls move constructor
    
    return 0;
}
```

Example 2: With Vector (More Practical)
```cpp
#include <iostream>
#include <vector>
#include <string>

int main() {
    std::vector<std::string> names;
    std::string largeName = "This is a very long string that we want to move";
    
    std::cout << "Before move - largeName: " << largeName << std::endl;
    
    // Move the string into the vector (no copy!)
    names.push_back(std::move(largeName));
    
    std::cout << "After move - largeName: " << largeName << std::endl;  // Likely empty!
    std::cout << "In vector: " << names[0] << std::endl;
    
    return 0;
}
```
Just remember:

After using `std::move(data)`, you shouldn't rely on data having its original value, as the function you passed it to might have "moved from" it (stolen its resources).
</details>


<details>
<summary>Maps in C++</summary>

Key Differences
`std::map`: Ordered (red-black tree), slower O(log n) operations
`std::unordered_map`: Unordered (hash table), faster O(1) operations, preferred when order doesn't matter

Example 1: Inefficient Linear Search with Vector
```cpp
#include <iostream>
#include <vector>
#include <string>

struct CityRecord {
    std::string Name;
    uint64_t Population;
    double Latitude, Longitude;

    // Constructor for easy initialization
    CityRecord(const std::string& name, uint64_t pop, double lat, double lon)
        : Name(name), Population(pop), Latitude(lat), Longitude(lon) {}
};

int main() {
    std::vector<CityRecord> cities;

    // Add cities to vector
    cities.emplace_back("Melbourne", 5000000, -37.8136, 144.9631);;
    cities.emplace_back("Berlin", 3769000, 52.5200, 13.4050);
    cities.emplace_back("Riga", 632000, 56.9496, 24.1052);
    cities.emplace_back("Lol-town", 1000, 0.0, 0.0);
    cities.emplace_back("London", 8982000, 51.5074, -0.1278);

    // INEFFICIENT: Linear search O(n)
    for (const auto& city : cities) {
        if (city.Name == "Riga") {
            std::cout << "Population of Riga: " << city.Population << std::endl;
            break;
        }
    }

    return 0;
}
```

Example 2: Efficient Lookup with std::map
```cpp
#include <iostream>
#include <map>
#include <string>

struct CityRecord {
    std::string Name;
    uint64_t Population;
    double Latitude, Longitude;
    
    CityRecord(const std::string& name, uint64_t pop, double lat, double lon)
        : Name(name), Population(pop), Latitude(lat), Longitude(lon) {}
};

int main() {
    // std::map - automatically sorts by key (city name)
    std::map<std::string, CityRecord> cityMap;
    
    // Insert cities - key is city name, value is CityRecord object
    cityMap["Melbourne"] = CityRecord{"Melbourne", 5000000, -37.8136, 144.9631};
    cityMap["Berlin"] = CityRecord{"Berlin", 3769000, 52.5200, 13.4050};
    cityMap["Riga"] = CityRecord{"Riga", 632000, 56.9496, 24.1052};
    cityMap["Lol-town"] = CityRecord{"Lol-town", 1000, 0.0, 0.0};
    cityMap["London"] = CityRecord{"London", 8982000, 51.5074, -0.1278};

    // EFFICIENT: Direct access O(log n)
    CityRecord& berlinData = cityMap["Berlin"];  // Get reference to avoid copy

    // Modify data through reference
    berlinData.Population = 4000000;  // This updates the actual map entry!
    std::cout << "Berlin population: " << cityMap["Berlin"].Population << std::endl;

    // Remove an entry
    cityMap.erase("Berlin");
    
    // Check if key exists (safer than direct access)
    if (cityMap.find("Berlin") == cityMap.end()) {
        std::cout << "Berlin was removed from the map" << std::endl;
    }

    return 0;
}
```

Example 3: Even Faster with std::unordered_map
```cpp
#include <iostream>
#include <unordered_map>
#include <string>

struct CityRecord {
    std::string Name;
    uint64_t Population;
    double Latitude, Longitude;

    CityRecord(const std::string& name, uint64_t pop, double lat, double lon)
        : Name(name), Population(pop), Latitude(lat), Longitude(lon) {}
};

int main() {
    // std::unordered_map - faster hash table, no ordering
    std::unordered_map<std::string, CityRecord> cityMap;
    
    // Same syntax as std::map
    cityMap["Melbourne"] = CityRecord{"Melbourne", 5000000, -37.8136, 144.9631};
    cityMap["Berlin"] = CityRecord{"Berlin", 3769000, 52.5200, 13.4050};
    cityMap["Riga"] = CityRecord{"Riga", 632000, 56.9496, 24.1052};

    // FASTEST: O(1) average case access
    CityRecord& rigaData = cityMap["Riga"];
    std::cout << "Riga latitude: " << rigaData.Latitude << std::endl;

    // Iterate (order is arbitrary)
    std::cout << "\nAll cities in unordered_map:" << std::endl;
    for (const auto& [name, city] : cityMap) {
        std::cout << name << ": " << city.Population << std::endl;
    }

    return 0;
}
```

Example 4: Custom Hash for Unordered Map
```cpp
#include <iostream>
#include <unordered_map>
#include <string>

struct CityRecord {
    std::string Name;
    uint64_t Population;
    double Latitude, Longitude;
    
    CityRecord(const std::string& name, uint64_t pop, double lat, double lon)
        : Name(name), Population(pop), Latitude(lat), Longitude(lon) {}
};

// Custom hash specialization for CityRecord
namespace std {
    template<>
    struct hash<CityRecord> {
        size_t operator()(const CityRecord& key) {
            // Use city name as hash basis
            return hash<std::string>()(key.Name);
        }
    };
}

int main() {
    // Can use CityRecord as key with custom hash
    std::unordered_map<CityRecord, std::string> cityDescriptions;
    
    CityRecord melbourne("Melbourne", 5000000, -37.8136, 144.9631);
    cityDescriptions[melbourne] = "Cultural capital of Australia";
    
    // Access using CityRecord key
    auto it = cityDescriptions.find(melbourne);
    if (it != cityDescriptions.end()) {
        std::cout << "Description: " << it->second << std::endl;
    }
    
    return 0;
}
```

Key Points
* Use `std::unordered_map` when order doesn't matter and you want maximum speed
* Use `std::map` when you need sorted iteration
* References allow direct modification of map elements without copying
* `operator[]` creates entries if they don't exist, `find()` is safer for lookup
* Custom types as keys require hash function for `unordered_map`

Best Practices
```cpp
// Safe lookup without creating entries
auto it = cityMap.find("Paris");
if (it != cityMap.end()) {
    // Use it->first (key) and it->second (value)
}

// Range-based for loops with structured binding
for (const auto& [cityName, cityData] : cityMap) {
    std::cout << cityName << ": " << cityData.Population << std::endl;
}

// Use references to avoid copies when modifying
auto& cityRef = cityMap["London"];
cityRef.Population += 1000;
```

Recommendation: Use `std::unordered_map` by default unless you need ordering!
</details>

<details>
<summary>What is NULL</summary>

NULL is a macro that typically equals 0 in C++. It represents a null pointer - a pointer that doesn't point to any valid memory address.

Example Code with Explanation
```cpp
#include <iostream>
#include <string>

class Entity {
public:
    Entity() = default;

    const std::string& GetName() const { return m_Name; }

    void PrintType() {
        std::cout << "Entity\n";
    }

private:
    Entity* m_Parent;
    std::string m_Name;
};

int main() {
    // Setting a pointer to nullptr (modern C++)
    Entity* entity = nullptr;
    // Memory layout: entity = 0x0000000000000000 (8 bytes of zeros on 64-bit systems)

    // ❌ DANGEROUS: Calling member function on null pointer
    // entity->GetName(); // CRASH: Read access violation
    // This tries to access m_Name through a null 'this' pointer

    // ✅ WORKS: Calling non-virtual member function that doesn't access member variables
    entity->PrintType(); // Output: "Entity"
    // This works because PrintType() doesn't access any member variables
    // The function call happens, but 'this' pointer is invalid inside the function

    // Void pointer can point to anything
    void* value = nullptr; // Generic pointer with no type information

    // NULL macro (old C style)
    void* value2 = NULL; // NULL is typically #define NULL 0

    return 0;
}
```

Why Some Calls Work and Others Crash

❌ Crashes: entity->GetName()
```cpp
entity->GetName(); // CRASH!
```
* Reason: The function accesses m_Name member variable
* What happens: The compiler passes this pointer (which is nullptr) to the function
* Inside function: return this->m_Name tries to access memory at address 0
* Result: Access violation - trying to read from invalid memory

✅ Works: entity->PrintType()
```cpp
entity->PrintType(); // Output: "Entity"
```
* Reason: Function doesn't access any member variables
* What happens: Function call succeeds because no member access occurs
* However: This is undefined behavior! The program could still crash

Modern C++ Null Pointers - Prefer nullptr over NULL
```cpp
// Old C style (avoid)
Entity* e1 = NULL;     // #define NULL 0
Entity* e2 = 0;        // Literal zero

// Modern C++ style (preferred)
Entity* e3 = nullptr;  // Type-safe null pointer constant

// nullptr has a specific type (std::nullptr_t)
std::nullptr_t null_value = nullptr;
```

Safe Null Pointer Usage
```cpp
int main() {
    Entity* entity = nullptr;
    
    // ✅ SAFE: Always check before using
    if (entity != nullptr) {
        entity->GetName(); // Safe to call
        entity->PrintType();
    }
    
    // ✅ SAFE: Shorthand null check
    if (entity) {
        entity->GetName();
    }
    
    // ✅ SAFE: Using references (cannot be null)
    Entity realEntity;
    Entity& entityRef = realEntity; // References must be valid
    entityRef.GetName(); // Always safe
    
    // ❌ DANGEROUS: No checks
    // entity->GetName(); // Potential crash
    
    return 0;
}
```

Undefined Behavior Example
```cpp
class Calculator {
public:
    int Add(int a, int b) {  // Doesn't use 'this'
        return a + b;
    }
    
    int GetValue() {  // Uses 'this' implicitly
        return value;  // this->value
    }
    
private:
    int value = 42;
};

int main() {
    Calculator* calc = nullptr;
    
    // ✅ Might work (but still undefined behavior)
    int result = calc->Add(5, 3); // Output: 8
    // Works because Add() doesn't access member variables
    
    // ❌ Will likely crash
    // int val = calc->GetValue(); // CRASH!
    // Tries to access this->value where this is null
    
    return 0;
}
```

Key Points
* `nullptr` is the modern, type-safe way to represent null pointers
* `NULL` is a legacy macro that equals 0
* Calling methods on null pointers is undefined behavior
* Some calls may appear to work if they don't access member variables, but it's still unsafe
* Always check for null before dereferencing pointers
* References are safer than pointers because they can't be null

Best Practices
```cpp
// ✅ Good
Entity* entity = getEntity();
if (entity) {
    entity->GetName();
}

// ✅ Better - use references when possible
Entity& entityRef = getEntityRef(); // Function returns reference
entityRef.GetName(); // No null check needed

// ❌ Bad - assuming pointer is valid
entity->GetName(); // Potential crash
```
Remember: Just because a method call on a null pointer doesn't immediately crash doesn't mean it's safe - it's still undefined behavior!
</details>

<details>
<summary>Empty</summary>

```cpp

```

</details>
Things that i need to understand:
debugging in c++ (walgrind, gdb)
compilators in c++
Design Patterns (Singleton, Factory, Observer) what is this
merge sort, bubble sort, quick sort - sorting
memory segments, how program is loaded in to memory, what linux does
 
git, git submodules, package managers used for library linking
linux
networking, OSI model, everything
what good coding methods do i use in work?
makefile, cmake