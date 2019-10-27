# cpp-code-guidelines
Some guidelines for project just moved from c++03 to c++17

# General considerations

## When to C++
C++ is a general purpose language but nowdays it exclusively took a niche to provide best possible performance (CPU load wise, size wise, battery usage wise, core load wise etc). C++ developer considered to be a professional and to know what exactly he doing. If your tasks are not demanding, **you better to stop using C++ and use like Python instead**.

## Best code
* C++ core and compiler code optimizers working, as a rule of thumb, in a way that the **simpliest code you write**, the best results you get. 
** Exception: operations that known to be a pessimisation of code, like unnecessary copy of input parameters or unnecessary heap allocations. (Even in this case, optimizing compiler will try to lend you a hand if your code is simple and obvious.)
* Make code as readable as rationaly possible. Mind the rule that "code is written one time, but read hundred times", so optimize for readers.

## On a coding style
C++ is actually not one language, but a collection of different languages under one roof. You have to choose coding style properly for a given task.
* Smalltalk/OOP: classic style OOP based virtual inheritance. To achive a goal, you abstract domain into series of class hierarchies, widely employing inheritance, polymorphism and encapsulation. The focus is on a tight coupling data and behaviour in a class(es). (This considered to be too wordy and too slow to be perfect solution for everything.)
* Metaprogramming: you focus on behaviour and use templates to abstract from exact data processed. A good library implemened in templates (e.g. STL, Boost) is precious. The main problem is slightest mistakes producing unreadable waterfall of errors. Despite of that, true professionals dare to walk the dangerous waters and often got back best performance-critical and optimizer-friendly code out there.
** We could join the train soon, after moving to VS2019 which already supports C++20 Concepts (v16.3). Basicaly concepts is a method to greatly improve templates behaviour and most importantly produce user-friendly error codes. https://devblogs.microsoft.com/cppblog/c20-concepts-are-here-in-visual-studio-2019-version-16-3/ . Without Concepts support, I do not recommend metaprogramming on a daily basis.
* Generic programming: metaprogramming but not with templates and not with macros. In each new C++ version you could do more and more just employing **auto** in code, function declarations and lambdas. Also consider possibility to calculate things in compile time with **constexpr**. This code easy to read, easy to maintain and error logs are readable.
** Each C++ release things you could do with auto and consexpr become wider and more powerful. (In C++20 if, for, all STL algorightms, dynamic allocations, smart pointers are supporting constexpr. Additionally added consteval.) https://youtu.be/9YWzXSr2onY
** std::variant and std::any now available to store data in generic way and easier implement such algorithms as state machines.
* Functional programming: writing functions that never mutate existing data (but optionally producing new data as output) you make code extremely testable, composable and reusable, and resulting program behaviour stable and predictable. This approach elevates your code as close as possible to a pure elegance of mathematics.
* Hardware explicit: modern C++ made a leap forward to embrace actual hardware. Memory barriers, allocators, alignment, [[likely]], threads and more. You could use all the tricks to produce extremely performant code, like vectorization, static dispatch, lock-free containers etc. Most importantly, tools are matured to assess, diagnose and test such code, including compiler introspection (godbolt.org), benchmarks (like google bench), and other tools to extract such information like missed branch predictions.

The only addition to classic OOP code style with virtual functions (but extremely valuable) is **override** keyword.
On the other hand, hundreds of large and small features are added to other code styles over the years.
Modern C++ encourages developer to take compile time decisions whenever possible. This is connected to narrow modern niche of C++ to be the most performant high level programming language.

Which coding style to choose? Select one where you can express your task in most elegant, short and readable form, but also able to provide unit tests. In most cases this means to skip metaprogramming (unless it reduces code repetition) and skip harware explicit style (unless you measured other approach with profiler first).

