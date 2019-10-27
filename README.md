# cpp-code-guidelines
Some guidelines for project just moved from c++03 to c++17

# General considerations

## When to C++
C++ is a general purpose language but nowadays it exclusively took a niche to provide best possible performance (CPU load wise, size wise, battery usage wise, core load wise etc). C++ developer considered to be a professional and to know what exactly he doing. If you have choice and your tasks are not demanding, **you better to stop using C++ and use Python instead**.

## Best code
* C++ core and compiler code optimizers working, as a rule of thumb, in a way that the **simpliest code you write**, the best results you get. 
** Exception: operations that known to be a pessimisation of code, like unnecessary copy of input parameters or unnecessary heap allocations. (Even in this case, optimizing compiler will try to lend you a hand if your code is simple and obvious.)
* Make code as readable as rationaly possible. Mind the rule that "code is written one time, but read hundred times", so optimize for readers.

## On a coding styles
C++ is actually not one language, but **a collection of different languages** under one roof. You have to choose coding style properly for a given task.
* Smalltalk/OOP: classic style OOP based virtual inheritance. To achive a goal, you abstract domain into series of class hierarchies, widely employing inheritance, polymorphism and encapsulation. The focus is on a tight coupling data and behaviour in a class(es). (This considered to be too wordy and too slow to be perfect solution for everything.)
* Metaprogramming: you focus on behaviour and use templates to abstract from exact data processed. A good library implemened in templates (e.g. STL, Boost) is precious. The main problem is slightest mistakes producing unreadable waterfall of errors. Despite of that, true professionals dare to walk the dangerous waters and often got back best performance-critical and optimizer-friendly code out there. 
  * We could join the train soon, after moving to VS2019 which already supports C++20 Concepts (v16.3). Basicaly concepts is a method to greatly improve templates behaviour and most importantly produce user-friendly error codes. https://devblogs.microsoft.com/cppblog/c20-concepts-are-here-in-visual-studio-2019-version-16-3/ . Without Concepts support, I do not recommend metaprogramming on a daily basis.
  * Macroes also jumps into metaprogramming category, as not everything could be expressed in templates up to date, and we still using them even when shouldn't as macroes are **addictive**. C++20 will provide **std::source_location** to cover some logging usecases.
* Generic programming: metaprogramming but not with templates and not with macros. In each new C++ version you could do more and more just employing **auto** in code, function declarations and lambdas. Also consider possibility to calculate things in compile time with **constexpr**. This code easy to read, easy to maintain and error logs are readable.
  * Each C++ release things you could do with auto and consexpr become wider and more powerful. (In C++20 if, for, all STL algorightms, dynamic allocations, smart pointers are supporting constexpr. Additionally added consteval.) https://youtu.be/9YWzXSr2onY
  * std::variant and std::any now available to store data in generic way and easier implement such algorithms as state machines.
* Functional programming: writing functions that never mutate existing data (but optionally producing new data as output) you make code extremely testable, composable and reusable, and resulting program behaviour stable and predictable. This approach elevates your code as close as possible to a pure elegance of mathematics.
* Hardware explicit: modern C++ made a leap forward to embrace actual hardware. Memory barriers, allocators, alignment, [[likely]], threads and more. You could use all the tricks to produce extremely performant code, like vectorization, static dispatch, lock-free containers etc. Most importantly, tools are matured to assess, diagnose and test such code, including compiler introspection (godbolt.org), benchmarks (like google bench), and other tools to extract such information like missed branch predictions.

The only addition to classic OOP code style with virtual functions (but extremely valuable) is **override** keyword.
On the other hand, hundreds of large and small features are added to other code styles over the years.
Modern C++ encourages developer to take compile time decisions whenever possible. This is connected to narrow modern niche of C++ to be the most performant high level programming language.

### Which coding style to choose? 
Which you feel is most elegant, short and readable for given task.
But beware that you have been able to cover it with unit tests.

In most cases this means to skip metaprogramming (unless it reduces code repetition) and skip harware explicit style (unless you measured other approach with profiler first).

# Toward a better code

## Some quick wins

### auto
* Use auto to reduce typing and easy reading, like to hold temporary iterator
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
* Use auto in lambda parameters to conserve on typing.
```C++
//--------- motivational examples
std::sort(intvec.begin(), intvec.end(),
    [](auto l, auto r){ return l >= r; });

std::sort(figigures.begin(), figigures.end(),
    [](const auto& l, const auto& r){ return l.getZIndex() < b.getZIndex(); });
```
In this case obviousely what will get into lambda parameters both for reader and for compiler, so auto is appropriate.

(!) Note: **auto** is replacing type, but not it's **traits** (constness, reference). Please don't forget to write **const** and **&** when necessary. If you don't want to think much, use **auto&&** - this means "same const as input container" and symbol && when next to auto called "forwarding reference".

### ranged for
Instead of cumbersome and tedious specification of begin and end of container, now you could just specify container itself.
```C++
auto intvec = std::vector<int>{1, 2, 3, 4, 5};
for(auto&& x: intvec)
  cout << x << ", ";
```

### Structural bindings
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

* Use structural bindings with specific STL algorithms and container methods.
```C++
//  insert is used here just for demo; in actual code prefer to use emplace and try_emplace in such cases instead

auto [pCfg, inserted] = m_calConfigs.insert({"Asd", PECalculatorConfig()});
if(!inserted)
   ErrorLog << "Using already existing: " << pCfg->Description();
else
   pCfg->Initialize();
}
```
### =default and =delete
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

### Initialization in class definition
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

It is very easy to see during code review if everything is initialized or not as both definition and default initialization provided in one place.
Note: another new feature to shorten constructors code is Delegating Constructor. Basically, you can call one constructor from another if you need. Look it up if you going to provide several constructors for a class. https://en.cppreference.com/w/cpp/language/initializer_list#Delegating_constructor

