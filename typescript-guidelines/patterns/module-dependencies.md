# module-dependencies

Break cyclic module dependencies, which JavaScript permits but which yield half-initialized imports.

**Sources:** P:complication-7-cyclic-dependencies

---

## Complication 7 Cyclic Dependencies (P:complication-7-cyclic-dependencies)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/complication-7-cyclic-dependencies), copyright the author, redistributed with attribution.

In [NodeJS](https://nodejs.org/api/modules.html#modules_cycles) and [ES6](https://exploringjs.com/es6/ch_modules.html#sec_design-goals-es6-modules), cyclic modules are allowed.

```
// module-a.js
const b = require("./module-b.js");
console.log(b.a);
module.exports = { b };

// module-b.js
const a = require("./module-a.js");
console.log(a.b);
module.exports = { a };
```

In the code above, for example, executing one of the modules will throw a `ReferenceError`. The last `require` call in a cyclic chain of `requires` will return an unfinished copy. And by that time the last required module will not be defined yet.

The problem with cyclic modules is that it is detected at runtime, not compile time. Moreover, this subtle `throw` can be accidentally caught, causing the program to continue instead of stopping.

TypeScript does not prevent circular dependencies. Extra tools are needed to capture circular dependencies within a codebase. [This](https://github.com/aackerman/circular-dependency-plugin) is available for webpack users. Otherwise, [Madge](https://www.npmjs.com/package/madge) has a neat circular dependency detection.

### Illusion of cyclic-like

In a big codebase, there can be an unavoidable pattern that is seemingly cyclic but is not. Usually type definitions and functions of the same domain are collected into a single module. Because of that, two domain modules, let that be `A` and `B` may seem to depend on each other.

```
Module A -> Module B
Module B -> Module A
```

In reality, the pattern is that `Functions of A` depend on `Types of B`, and `Functions of B` depend on `Types of A`. Oftentimes, the functions from each module do not depend on each other.

In this case, types are better separated from the functions. Types and functions can be split by domains and then a combination of types can be made so that different functions can depend on the combined types.

In this case, it is wise to instead separate the types from the functions so that the functions can depend on the types and be separated.

```
Types All -> Types A
Types All -> Types B
Functions A -> Types All
Functions B -> Types All
```

This approach also prevents disagreement over whether an `import` should be just an [`import` or an `import type`](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-8.html).

In abstract, this approach means that programmers should **create a balance between the separation of modules by domain and by pattern**, instead of choosing one from the other.
