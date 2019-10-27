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

Which coding style to choose? Select one where you can express your task in most elegant, short and readable form, but also able to provide unit tests. In most cases this means to skip metaprogramming (unless it reduces code repetition) and skip harware explicit style (unless you measured other approach with profiler first).

# To a better code

## Quick wins

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
    InfoLog << "Not Found asd";
    return false;
  }
  else
  {
    InfoLog << "Found asd: " << *iter->second;
    return true;
  }
}

//--------- New style
bool HasAsdInAsd(const PE::XyzCalculator::AsdContainer& vec)
{
  if(const auto iter = vec.find("Asd"); iter != vec.end())
  {
    InfoLog << "Found asd: " << *iter->second;
    return true;
  }
  else
  {
    InfoLog << "Not Found asd";
    return false;
  }
}

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
