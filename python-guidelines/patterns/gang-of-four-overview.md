# gang-of-four-overview

Why most Gang of Four patterns shrink or vanish in a language with first-class functions and classes.

**Sources:** P:gang-of-four

---

## Gang of Four (P:gang-of-four)

[Python Design Patterns by Brandon Rhodes (python-patterns.guide)](https://python-patterns.guide/gang-of-four/), copyright Brandon Rhodes, redistributed with attribution.

It can be hard to remember, but object oriented programming was all the rage back in the roaring 1990s. Instead of talking about the power of first-class functions and general-purpose data structures, many programmers were festooning their code with virtual methods, superclasses, subclasses, and clever mixins. Programmers often found that language limitations and static types were locking them out of improvements they later wanted to make to their code.

The “Gang of Four” rode to the rescue. Their book’s first and most fundamental pattern, blazoned across the page in italics, would — if practiced consistently — break programmers free of code that was hard-wired to concrete classes:

> _“Program to an interface, not an implementation.”_

At the expense of more code, this practice moved programmers one step towards the freedom we enjoy in a dynamic language like Python. Each of the book’s further chapters tackled a different design conundrum posed by the era’s limited programming languages and solved it. Most of the solutions introduced new classes to cleverly decouple code that would otherwise be too tightly linked.

This site examines the old patterns from the Gang of Four in the context of a modern dynamic programming language in which classes and functions are first-class objects, to see which patterns are still useful and which ones disappear. You can start working through the patterns back on this site’s [front page](https://python-patterns.guide/).

---
