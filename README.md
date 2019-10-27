Some guidelines for the project just moved from c++03 to c++17
# Table of contents
[General considerations]
[Toward a better code: quick wins]
[Toward a better code: steady improvement]
[Toward a better delivery: tooling]

# General considerations

## When to C++
C++ is a general-purpose language but nowadays it exclusively took a niche to provide the best possible performance (CPU load wise, size-wise, battery usage wise, core load wise etc). C++ developer considered to be a professional and to know what exactly he doing. If you have a choice and your tasks are not demanding, **you better stop using C++ and use Python instead**.

## Best code
* C++ core and compiler code optimizers working, as a rule of thumb, in a way that the **simplest code you write**, the best results you get. 
** Exception: operations that known to be a pessimization of code, like an unnecessary copy of input parameters or unnecessary heap allocations. (Even in this case, optimizing compiler will try to lend you a hand if your code is simple and obvious.)
* Make code as readable as rationally possible. Mind the rule that "code is written one time, but read a hundred times", so optimize for readers.

## On coding styles
C++ is not one language but **a collection of different languages** under one roof. You have to choose a coding style properly for a given task.
* `Smalltalk/OOP`: classic style OOP based virtual inheritance. To achieve a goal, you abstract domain into a series of class hierarchies, widely employing inheritance, polymorphism, and encapsulation. The focus is on a tight coupling data and behavior in a class(es). (This considered to be too wordy and too slow to be a perfect solution for everything.)
* `Metaprogramming`: you focus on behavior and use templates to abstract from exact data processed. A good library implemented in templates (e.g. STL, Boost) is precious. The main problem is the slightest mistakes producing an unreadable waterfall of errors. Despite that, true professionals dare to walk the dangerous waters and often got back the best performance-critical and optimizer-friendly code out there. 
  * We could join the train soon, after moving to VS2019 which already supports C++20 Concepts (v16.3). Simply speaking, Concepts is a method to greatly improve templates behavior and most importantly produce user-friendly error codes. https://devblogs.microsoft.com/cppblog/c20-concepts-are-here-in-visual-studio-2019-version-16-3/ . Without Concepts support, I do not recommend metaprogramming daily.
  * Macros also jumps into the metaprogramming category, as not everything could be expressed in templates up to date, and we still using them even when shouldn't as macros are **addictive**. C++20 will provide **std::source_location** to cover some logging use cases.
* `Generic programming`: metaprogramming but not with templates and not with macros. In each new C++ version you could do more and more just employing `auto` in code, function declarations and lambdas. Also, consider the possibility to calculate things in compile time with `constexpr`. This code easy to read, easy to maintain and error logs are readable.
  * Each C++ release things you could do with auto and constexpr become wider and more powerful. (In C++20 if, for, all STL algorithms, dynamic allocations, smart pointers are supporting constexpr. Additionally added `consteval`.) https://youtu.be/9YWzXSr2onY
  * std::variant and std::any now available to store data generically and easier implement such algorithms as state machines.
* `Functional programming`: writing functions that never mutate existing data (but optionally producing new data as output) you make code extremely testable, composable and reusable, and resulting program behavior stable and predictable. This approach elevates your code as close as possible to a pure elegance of mathematics.
* `Hardware explicit`: modern C++ made a leap forward to embrace actual hardware. Memory barriers, allocators, alignment, [[likely]], threads and more. You could use all the tricks to produce extremely performant code, like vectorization, static dispatch, lock-free containers, hardware_constructive_interference_size, etc. Most importantly, tools are matured to assess, diagnose and test such code, including compiler introspection (godbolt.org), benchmarks (like google bench), and other tools to extract such information like missed branch predictions.

The only addition to classic OOP code style with virtual functions (but extremely valuable) is the `override` keyword.
On the other hand, hundreds of large and small features are added to other code styles over the years.
Modern C++ encourages the developer to take compile-time decisions whenever possible. This is connected to the narrow modern niche of C++ to be the most performant high-level programming language.

### Which coding style to choose? 
Which you feel is most elegant, short and readable for the given task.
But beware that you have been able to cover it with unit tests.

In most cases, this means to skip metaprogramming (unless it reduces code repetition) and skip hardware explicit style (unless you measured other approaches with profiler first).

# Toward a better code: quick wins
Following are, probably, most simple things that made immediate impact on code readability and simplicity.

## auto
* Use auto to reduce typing and easy reading, like to hold the temporary iterator
```C++
//--------- Old style
bool HasAsdInAsd(const PE::XyzCalculator::AsdContainer& vec)
{
  PE::XyzCalculator::AsdContainer::const_iterator iter;
  iter = vec.find("Asd");
  if(iter != vec.end())
  {
   ...
//--------- New style
bool HasAsdInAsd(const PE::XyzCalculator::AsdContainer& vec)
{
  if(const auto iter = vec.find("Asd"); iter != vec.end())
  {
   ...
```
see also "Initializer in `if`" section.

* Use auto in lambda parameters to conserve on typing.
```C++
//--------- motivational examples
std::sort(intvec.begin(), intvec.end(),
    [](auto l, auto r){ return l >= r; });

std::sort(figigures.begin(), figigures.end(),
    [](const auto& l, const auto& r){ return l.getZIndex() < b.getZIndex(); });
```
In this case obviousely what will get into lambda parameters both for reader and for compiler, so auto is appropriate.

* Don't Repeat Yourself
If you have to repeat type again in the same line, see if `auto` is applicable instead.
```C++
// old
std::shared_ptr<UnitTestWrapper<NYCalculator>> ptrUCalc = std::shared_ptr<UnitTestWrapper<NYCalculator>>(new UnitTestWrapper<NYCalculator>());

// new
auto ptrUcalc = std::make_shared<UnitTestWrapper<NYCalculator>>();

//old
std::map<std::string, XCalculator>::value toInsert = std::map<std::string, XCalculator>::value();

// new
auto toInsert = std::map<std::string, XCalculator>::value{};
```

(!) Note: **auto** is replacing type, but not it's **traits** (constness, reference). Please don't forget to write **const** and **&** when necessary. If you don't want to think much, use **auto&&** - this means "the same const as input container" and symbol && when next to auto called "forwarding reference".

## ranged for
Instead of cumbersome and tedious specification of begin and end of container, now you could just specify container itself.
```C++
auto intvec = std::vector<int>{1, 2, 3, 4, 5};
for(auto&& x: intvec)
  cout << x << ", ";
```

## Structural bindings
* Use structural binding when iterating on maps to greatly reduce typing and improve readability
```C++
//--------- Old style
const std::map<std::string, PECalculatorConfig> m_calConfigs& = configCache[42];
std::map<std::string, PECalculatorConfig>::const_iterator iter;
for(iter = m_calConfigs.cbegin(); iter != m_calConfigs.cbegin(); ++iter)
{
  const std::string& title = iter->first;
  const PECalculatorConfig& config = iter->second;
  cout "{" << title << " region: " << config.getRegion();
}

//--------- New style
for(const auto&[title, config]: configCache.at(42))
{
  cout "{" << title << " region: " << config.getRegion();
}
```
Note: old style sample has mistake in interation which is impossible to make in new style.
Note2: In the same way you could unpack not only std::pair, but any custom structures as well, for example, `FILETIME`, but it is less practical.

* Use structural bindings with specific STL algorithms and container methods.
```C++
auto [pCfg, inserted] = m_calConfigs.insert({"Asd", PECalculatorConfig()});
if(!inserted)
   ErrorLog << "Using already existing: " << pCfg->Description();
```
Insert was used here just for demo; in actual code prefer to use emplace and try_emplace in such cases instead.

```C++
void f(std::string_view id, std::unique_ptr<Foo> foo) {
  if (auto [pos, inserted] = items.try_emplace(id, std::move(foo)); inserted) {
    pos->second->launch();
  } else {
    standby.emplace_back(std::move(foo))->wait_for_notification();
  }
}
```

## =default and =delete
In new standard you can explicitly re-use compiler default implementation for constructor, destructor or assignment operator, which will be most optimal for most data types.
```C++
// item.cpp
Myclass::Myclass() = default; // generates all constuction code for Myclass once into item.obj


// item.h
class Myclass:
{
  public:
  MyClass();
  ~MyClass() = default; // generated destructor code will be inlined into each caller obj-file
};
```
Now you can explicitly delete any default-constructed method, which is better analogue to old trick of moving it's definition into protected/private method.
```C++
class NonCopiable:
{
  public:
    NonCopiable(const NonCopiable&) = delete;
    NonCopiable& operator=(const NonCopiable&) = delete;  
};
```
Note that beside copy ctor/assignment starting from C++11 there is also move ctor/assignment operators. But usually you don't have to block it as nothing bad should happen if you move entire object (unless it is extremely exotic, which is bad).

## Initialization in class definition
```C++
// old.cpp
MyClass::MyClass(): m_pi(3.14), m_p(4), m_dblDelta(0.), m_dblAlpha(m_dblDelta)
{ m_finish = false;}
```
Code like above is tedious and error prone. Looking just at it you have no idea if you safe from uninitialized members or not.
Also you have no idea what is the order of initialization. 50/50 that `m_dblAlpha(m_dblDelta)` is plain error.
```C++
// new.cpp
MyClass::MyClass() = default;

// new.h
class MyClass
{
...
 bool m_start{}, m_finish{};
 double m_dblAlpha{};
 double m_pi{3.14};
 int m_p{4};
 double m_dblDelta{};
};
```
In new C++ curly brackets {} used to initialize and construct entities. Empty curly brackets will default initialize (with zero).
Construction m_p{3.14} will not compile as curly brackets also check for correct type (m_p is int, so probably you wanted to initialize m_pi with 3.14 instead).

It is very easy to see during code review if everything is initialized or not as both definitions and default initialization provided in one place.
Note: another new feature to shorten constructors code is Delegating Constructor. You can call one constructor from another if you need it. Look it up if you going to provide several constructors for a class. https://en.cppreference.com/w/cpp/language/initializer_list#Delegating_constructor

## Initialization in `if` statement
New C++ adds optional section into `if` which is indentical to first section in `for` operator. 
You could do some calculations there or declare a variable that would be visible during entire if...else... operation, but not visible outside.
```C++
// motivational examples

if(auto w = testName.find("DISABLED"); w != testName.end()) cout << testName;

if(auto shared = weakptr.lock(); shared) shared->callback(this);

if(std::lock_guard<std::mutex> lk(mx_); v.empty()) v.push_back(kInitialValue);

if(char buf[10]; std::fgets(buf, 10, stdin)) { m[0] += buf; }
```
Note: Similar section now also available for `switch` and `while` operators.

## Defining constants in class definitions
In old C++ there are several typical methods to have a class constant:
```C++

#define variable1 42

class MyClass
{

   static const int variable2;
   // in some .cpp file: const int MyClass::variable2 = 42

   const int getVariable3a() const { return 42;}

   static const int getVariable3b() { return 42;}
   
   enum SomeEnum
   {
    variable4 = 42;
   };
  
```
All variants are ugly in each unique way.

New C++ offers inline variables to the resque:
```C++
inline constexpr int val1 = 42;

inline int getVal2() { return 42; }

class MyClass
{
  static /*inline*/ constexpr int val2 = 42; // static+consexpr is implicitly inline
```
Roughly how it works is allowing the compiler to have this thing duplicated in source code; then telling the linker to eliminate duplication.

## Structural initialization
This is a part of the larger topic: "uniform initialization", see below.
In old C++ it is possible to initialize simple aggregare using `{}`, this is inherited from C:
```C++
struct Point { int x, y; };
Point pt = {10, 20};
```
In new C++ similar syntax now possible to initialize much more complex structure, as a part of global revamp of initialization in C++.
```C++
std::pair<int> pair1 = {10, 20};
std::pair<int> pair1 {10, 20};

MyClass::MyClass(std::pair<double> coords, bool flag);
MyClass my1{{10,20}, true};
auto my2 = MyClass{{10,20}, true};
auto my3 = std::make_unique<MyClass>({{10,20}, true});

const static std::vector<int> favouriteNumbers {1, 3, 5, 7, 11};

auto s = std::set<std::string>{"Hello", "World"};

const static auto staticCalculators = std::map<std::string, int>{ {"undefined", -1}, {"LDN", 1}, {"NYK", 2}, {"XCCY", 13} };
if (auto p = staticCalculators.find("LDN"); p != staticCalculators.end())
 return p->second;
else
		return staticCalculators.at("undefined");

```
You can pass curly brackets (`initializer_list`) wherever compiler allows you to create value on-the-fly. For example:
```C++
std::shared_ptr<MyClass, MyDeleter> MyClas::GetSharedInstance()
{
 if(!initialized)
  return {}; // this replaces std::shared_ptr<MyClass, MyDeleter>();
...

std::string MyClas::GetLastError() const
{
 if(!ptrError)
  return {}; // this replaces std::string();
...
```


# Toward a better code: steady improvement
Important new features that we also should use, but which benefit us in a longer timespan.
These changes are improving code correctness, improving performance, eliminating risks, improve readability, lessen code repetition.

## C++ Core Guideliness
http://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines contains extensive list of rules and best practices, created by prominent C++ figures (Bjarne Stroustrup, Herb Sutter, Scott Meyers, Titus Winters, Michael Park etc.) and covers most engineering choices you would want to made. Examples:
* F.7: For general use, take T* or T& arguments rather than smart pointers
* R.30: Take smart pointers as parameters only to explicitly express lifetime semantics
* F.8: Prefer pure functions
* F.9: Unused parameters should be unnamed
* F.20: For “out” output values, prefer return values to output parameters
* F.43: Never (directly or indirectly) return a pointer or a reference to a local object
* I.5: State preconditions (if any)
* I.25: Prefer abstract classes as interfaces to class hierarchies
* C.4: Make a function a member only if it needs direct access to the representation of a class
* R.1: Manage resources automatically using resource handles and RAII (Resource Acquisition Is Initialization)
* R.23: Use make_unique() to make unique_ptrs
* ES.20: Always initialize an object
* ES.21: Don’t introduce a variable (or constant) before you need to use it
* ES.22: Don’t declare a variable until you have a value to initialize it with
* ES.23: Prefer the {}-initializer syntax
* ES.71: Prefer a range-for-statement to a for-statement when there is a choice
* CPL.1: Prefer C++ to C
* SF.7: Don’t write using namespace at global scope in a header file
* SF.11: Header files should be self-contained
* Appendix B: Modernizing code

When in doubt, check Core Guideliness.

## Unit tests
* We have to protect business value of our code using different types of regression testing, and Unit Testing is important layer of it.
* Just keeping Unit Testing in mind immediately producing better modular and less entangled code.
* Allows to speed up development of separate code modules by providing a quick jump into module from unit tests.
* Having code UT-ready also could make micro-benchmarking easy.

+ mocking
+ common testing model, other layers of testing (see also Static Code Analysis)
+ replaying
+ fuzzing

## override
Keyword `override` is a must use for all overrides of virtual functions. This enables compiler to report errors in compile time when signature of function is actually not compatible with function overloaded. Old C++ just allowed unpredicted behavior of program in run-time instead (when called not the function you expected).
Note: using `clang-tidy` or similar static code analyser it is possible to automatically update our code fitting `override` whenever necessary. After that we could continue manually support this habit, while time-to-time checking any misses using the tool again.

## nullptr
`nullptr` must be used instead of NULL macro, no exception.
Note that in new C++ some STL/Boost methods are specifically overloaded against `nullptr`.

## using
Instead of `typedef` it is recomended to use new, more readable and versatile keyword `using`.
```C++
// old
typedef StrongType<std::string, struct tagStrongString> StrongString;
typedef HINSTANCE (*fpLoadLibrary)(char*);
typedef int (*func)(int, int);

//new
using StrongString = StrongType<std::string, struct tagStrongString>;
using fpLoadLibrary = HINSTANCE(*)(char*);
using func = int (*)(int x, int y);
```

## `[[nodiscard]]`
Sometimes compiler need extra tips for something, which is passed as an attributes to compiler.
Example is `__declspec(dllimport)` keyword. New C++ proposes a standardised way to pass attributes using double square brackets syntax.

One of most interesting new attributes is `[[nodiscard]]` - return value marked this way assumed to be important for user and should not be accidently discarded.
```C++
[[nodiscard]] bool CompareGraphs(Graph a, Graph b);
[[nodiscard]] void* operator new(size_t _Size);
```

Another potentially usable attributes are [[deprecated]] (provides message for deprecated API), [[noreturn]] (no return from function) and [[maybe_unused]] (for cases when under conditions marked input parameter maybe unused). In C++20 will also appear [[likely]] and [[no_unique_address]] (for if/switch branch which you want to optimize branch predictor to and to re-use space wasted for alignment in structures for something useful).

## decltype
Sometimes you cannot use auto because you need to name type before actual assignment.
For example you need a placeholder for future value.
Or you constructing expected value in unittest for comparison.
In this case you can easily extract type from variable itself with `decltype`.
```C++
// create expected value of same type as calculated, but with predefined data
const decltype(testobj.data.m_inputs) expected = 
 {{"RIC1", {}}, {"RIC2", {}}, {"RIC3", {"RIC", 123, "AC111"}}};
// compare expected with actual result
ASSERT_EQ(expected, testobj.data.m_inputs);
```
## enum classes

## string_view

## variant, any, optional

## to_chars, from_chars

## Boost --> STL: shared_ptr and others
smart pointers (+deleters, aliases, array), unordered_map,...
regex
array, function
filesystem
chrono
random

## Literal prefixes
"String"sv

## uniform initialization and `initializer_list`
Curly brakets now can be used to initialize types.
This also allows to solve so called "most vexing parse" case in C++, where construction `C c();` cannot be a default constructor for C class but treated as a function declaration instead.

| old | new |
|----|----|
| // uninitialized built-in type| // default-initialized built-in type |
| int i;    |int i{}; |
| // initialized built-in type| |
| int j=10; | int j={10}; |
| // initialized built-in type|  |
| int k(10);| int j{10}; |
| // Aggregate initialization|  |
| int a[]={1, 2, 3, 4} | int a[]={1, 2, 3, 4}  |
| // default constructor | |
| X x1; | X x1{}; |
| // Parametrized constructor | |
| X x2(1); | X x2{1}; |
| // Parametrized constructor with single argument | |
| X x3=3;  | X x3={3}; |
| // copy-constructor | |
| X x4=x3;  | X x4{x3}; |

Note that {} will not allow narrowing (dropping of significant bits).
This will produce error:
```C++
int pi(3.14); // OK, your pi now 3
int pi{3.14}; // Error, cannot fit 3.14 into int
```
See also samples in paragraph Structural initialization.

## Better deduction for parameter types
```C++
auto ic = std::pair(1, 'x'); // type becomes std::pair<int, char> 
const auto v = std::vector{ 1,2,3,4 }; // type becomes std::vector<int>
```

## `constexpr`
+ static_assert
if constexpr

## Splicing maps and sets
In new C++ there is a way to extract, move and insert nodes in alive containers without actually copying/moving/re-allocating the data.
```C++
map<int, string> m{{1,"mango"}, {2,"papaya"}, {3,"guava"}};
auto nh = m.extract(2); // node is extracted from container and hold in a handle
nh.key() = 4; // while node is in handle, key become editable too
m.insert(move(nh)); // m == {{1,"mango"}, {3,"guava"}, {4,"papaya"}}
```

## Move semantics

## Lambda

## Ranges

## Allocators, pmr

## Threads
std::thread / std::jthread
std::mutex / std::recursive_mutex / std::timed_mutex / std::shared_mutex
std::atomic
std::condition_variable
std::future
std::lock_guard
std::unique_lock
std::async
std::future
parallel algorithms

## Templates
extern templates
variadic templates
type traits
Concepts

## Modules

## Coroutines

## other?
memory barriers
explicit X::bool()
cstdbool, cstdint, cinttypes
u8
byte
operator <=>
std::span
Signed Integers are Two’s Complement

# Toward a better delivery: tooling

## Static code analysis
clang-tidy
coverity
VS

## Sanitizers
ASan
UBSan
TSan

## Benchmarks, instrumentation

## Cross-compilation

## Containerization

## Tools know-how
VS Code as editor
.natvis
.clang-format
godbolt.org
Visual Studio sounds
TortoiseGit rebase
resharper / visual assit, refactoring
incredibuild
include-what-you-using

# Coding guidelines

## Existing major coding guidelines
TBD

## What would be the median
TBD

# References
TBD

https://youtu.be/QpFjOlzg1r4 C++ Weekly - Ep 190 - The Important Parts of C++17 in 10 Minutes
