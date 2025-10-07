### Some things I should remember about C/C++

<details>
<summary>Preprocessor commands</summary>

Everything that begins with a `#` in C++ is a preprocessor command and gets evaluated by the preprocessor before compiling.

`#pragma once` is a preprocessor command to "only inlcude this file once" in a single translation unit - a single C++ file. Header files just copy-paste the code, if it is done twice, we can get multiple definition errors.
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

after prorocessing, we get this:
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
<summary>lambdas</summary>

Basic overview of lambda:
```cpp
int x = 5, y = 10;

// [=] Capture everything by VALUE (copy)
auto f1 = [=]() { return x + y; };  // Gets copies of x and y

// [&] Capture everything by REFERENCE  
auto f2 = [&]() { x++; return y; };  // References to original x and y

// [x, &y] Capture x by value, y by reference
auto f3 = [x, &y]() { return x + y; };  // x is copy, y is reference

// [] Capture nothing
auto f4 = []() { return 42; };  // No access to x or y
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
```

</details>


<details>
<summary>Create/instantiate objects</summary>

In which memory are we creating out object?
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
Enitity* e = new Enitity();
Enitity* e = (*Enitity)malloc(sizeof(Enitity))
// this is actually kinda the same, the only diff is that malloc does not call the Entity() contructor

free(); // frees memory from malloc, dont mix new with free, use delete
```
You can also specify the address if needed:
```cpp
Entity* e = new(b) Entity(); // assuming b is a pointer
```

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

Smart pointers in C++ `std::unique_ptr, std::shared_ptr, std::weak_ptr`.
This automates new-delete handling - wrapper around a real raw pointer.

`std::unique_ptr` - scoped pointer, when goes out of scope, it will get destroyed and call `delete()`. Cannot be copied.
```cpp
#include <memory>

class Entity() {
  public:
    Entity() {/*...*/}
    ~Entity() {/*...*/}
    void Print() {/*...*/}
}

int main() {
    {
        // std::unique_ptr<Entity> entity(new Entity());
        // this is the prefered way, safer in case constructor throws an exception, and dont end up with a ptr with no reference 
        std::unique_ptr<Entity> entity = std::make_unique<Entity>();
        // std::unique_ptr<Entity> entity2 = entity; // we cannot do this!!!
        entity->Print();
    }
    // when this goes out of scope, delete() is automatically called
}
```

`std::shared_ptr` - uses smth called reference counting. practice where we count how many references we have to the ptr, if its 0, we free memeory.
This ptr can be copied.

```cpp
#include <memory>

class Entity() {
  public:
    Entity() {/*...*/}
    ~Entity() {/*...*/}
    void Print() {/*...*/}
}

int main() {
    {
        std::shared_ptr<Entity> e0;
        {
            // we need to use make_unique in case contructor error, shared_ptr contructs a control block, which wont be freed
            std::shared_ptr<Entity> sharedEntity = std::make_unique<Entity>();
            e0 = sharedEntity;
        }
        // when 1st cope dies, sharedEntity dies
        // but e0 lives, hold reference to Entity object
    }
    // here e0 dies, which held last reference to Entity
}
```

`std::weak_ptr` - usually used together with `shared_ptr`

```cpp
#include <memory>

class Entity() {
  public:
    Entity() {/*...*/}
    ~Entity() {/*...*/}
    void Print() {/*...*/}
}

int main() {
    {
        std::weak_ptr<Entity> e0; // weak_ptr does not increase ref count of shared_ptr
        {
            std::shared_ptr<Entity> sharedEntity = std::make_unique<Entity>();
            e0 = sharedEntity;
        }
        // entity gets destroyed and weak_ptr points to invalid memory now
    }
}
```

Should try to use them all the time, safe way, prevents you from memory leaks, automates memory management.
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

```cpp

```
</details>



<details>
<summary>Something</summary>
:)
</details>

<details>
<summary><code>Something</code> keyword</summary>

</details>


Things that i need to understand:
stack, heap, stack pointer. what even is that memory and where it exists - ram? os gives it to the program? how does it know how much
debugging in c++
compilators in c++

git, git modules
linux
networking, OSI model, everything
what good coding methods do i use in work?