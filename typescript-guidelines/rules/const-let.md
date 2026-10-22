# const-let

Declare with `const` by default and `let` only when reassigned, one variable per declaration, never `var`, and never use a variable before its declaration.

**Why:** Block scoping avoids `var`'s function-scope bugs.

**Sources:** G:local-variable-declarations

---

## Local variable declarations (G:local-variable-declarations)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#local-variable-declarations), CC BY 3.0.

### Use const and let

Always use `const` or `let` to declare variables. Use `const` by default, unless a variable needs to be reassigned. Never use `var`.

✅ Good:

```ts
const foo = otherValue;  // Use if "foo" never changes.
let bar = someValue;     // Use if "bar" is ever assigned into later on.
```

`const` and `let` are block scoped, like variables in most other languages. `var` in JavaScript is function scoped, which can cause difficult to understand bugs. Don't use it.

❌ Bad:

```ts
var foo = someValue;     // Don't use - var scoping is complex and causes bugs.
```

Variables _must not_ be used before their declaration.

### One variable per declaration

Every local variable declaration declares only one variable: declarations such as `let a = 1, b = 2;` are not used.
