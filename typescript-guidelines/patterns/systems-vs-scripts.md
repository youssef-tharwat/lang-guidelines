# systems-vs-scripts

Why long-running systems need different discipline than scripts, and what makes code complex versus complicated.

**Sources:** P:prelude-1-system-vs-script, P:prelude-2-inherent-complexity

---

## Prelude 1 System Vs Script (P:prelude-1-system-vs-script)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/prelude-1-system-vs-script), copyright the author, redistributed with attribution.

This article is a part of the[systemic-ts](https://valand.dev/systemic-ts) series.

Next:

prelude

A system consists of interacting and/or interrelated components. Such components interact with certain preferences, forming a **BOUNDARY** separating the system and the environment.

A system is usually long-running, needs to be durable, must self-regulate, and often have subsystems, each having a sub-purpose of the parent's. Having a boundary, it bounds to have a mechanism to interact with the environment--the interface.

Having many components, maintenance is harder, thus requiring a different strategy.

Scriptic, on the other hand, is a quality of software, code, script, etc, that is not systemic.

I derived the definition from how script errors are commonly handled by reporting and retrying. In a script, it is rare that an error or a message in general is passed to some other piece of code to be interpreted.

But it is not rare to see a collection of scripts become systemic over time and then the programmers begin to consider using another tool, and then another language. This [complexity shift is often painful](https://valand.dev/systemic-ts/inherent-complexity); when unmanaged, many have resorted to total rewrites with new languages.

Moreover, determining whether a program will be a system at first is often difficult at first because the formation of the system's boundary is continuous, not instant.

Systemic TypeScript series aims to select a particular strategy of writing TypeScript program that scales with complexity, where design pattern does not have to change often as a scriptic program becomes systemic. Therefore, when applied, the distinction between systemic and scriptic becomes less important and thus reducing the negative effect of complexity shift.


## Prelude 2 Inherent Complexity (P:prelude-2-inherent-complexity)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/prelude-2-inherent-complexity), copyright the author, redistributed with attribution.

This article is a part of the[systemic-ts](https://valand.dev/systemic-ts) series.

Previous:

prelude

Next:

complication

### Complex vs Complicated vs Hard

People often dismiss something difficult as `complex`. That word is many programmers' black sheep; the opposite `simplicity` naturally became overrated, ambiguous, and misplaced.

Look into these topics:

*   Following a recipe written not straightforwardly.
*   Understanding how time dilation relates to the speed of light.

Both are hard, but the former can be improved while the latter cannot because the idea of relativity is inherent, fundamental.

I thus name the former **complication** (or unnecessary complexity) and the latter **complexity** (or inherent complexity).

### Complexity Shift

How would a librarian organize books? Is it by genre, author, color, size, name, publication date?

Categorizing is the most common form of organization. Organization, however, needs a dimension.

The multilemma of the strategy to organize books comes from the lack of dimension. More concretely, a book has many properties---genre, author, color, etc. However, since the librarian needs to organize books within the space which only has three dimensions, the librarian needs to choose one property out of many.

The number of properties maps to complexity, while the discrepancy between the number of properties and the limited number of dimensions is the source of complication. In other words, complication can be perceived as two properties conflicting because they reside in the same dimension. In systems, it can manifest as two components clashing with each other.

To fit more properties within a limited dimension, some strategies can be applied. One simple example is the [index](https://en.wikipedia.org/wiki/Index_(publishing)) in books, which contains the important words and on which page to find them. In software development, a lot of strategies take a similar form to that of the index.

As features are added to a program, complexity grows. Proper organization must be conducted to suppress complications. It is a continuous process, hence there is the term [continuous refactoring](https://wiki.c2.com/?ContinuousRefactoring) in software development.

In other words, complication exists not because of complexity itself but because of **unorganized complexity shifts** and this is the exact phenomenon that arises when a program turns from [scriptic to systemic](https://valand.dev/systemic-ts/system-vs-script).

#### Complications (avoid these)
