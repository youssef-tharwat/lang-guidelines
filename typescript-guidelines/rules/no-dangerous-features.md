# no-dangerous-features

Never use `eval` or `Function(...)` strings, `with`, `debugger` in production code, `const enum`, or non-standard or unfinished language features; end every statement with `;` rather than relying on automatic semicolon insertion.

**Why:** Each is a known source of bugs or security holes.

**Sources:** G:disallowed-features

---

## Disallowed features (G:disallowed-features)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#disallowed-features), CC BY 3.0.

### Wrapper objects for primitive types

TypeScript code _must not_ instantiate the wrapper classes for the primitive types `String`, `Boolean`, and `Number`. Wrapper classes have surprising behavior, such as `new Boolean(false)` evaluating to `true`.

❌ Bad:

```ts
const s = new String('hello');
const b = new Boolean(false);
const n = new Number(5);
```

The wrappers may be called as functions for coercing (which is preferred over using `+` or concatenating the empty string) or creating symbols. See type coercion for more information.

### Automatic Semicolon Insertion

Do not rely on Automatic Semicolon Insertion (ASI). Explicitly end all statements using a semicolon. This prevents bugs due to incorrect semicolon insertions and ensures compatibility with tools with limited ASI support (e.g. clang-format).

### Const enums

Code _must not_ use `const enum`; use plain `enum` instead.

**Why?**

TypeScript enums already cannot be mutated; `const enum` is a separate language feature related to optimization that makes the enum invisible to JavaScript users of the module.

### Debugger statements

Debugger statements _must not_ be included in production code.

❌ Bad:

```ts
function debugMe() {
  debugger;
}
```

### `with`

Do not use the `with` keyword. It makes your code harder to understand and [has been banned in strict mode since ES5](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/with).

### Dynamic code evaluation

Do not use `eval` or the `Function(...string)` constructor (except for code loaders). These features are potentially dangerous and simply do not work in environments using strict [Content Security Policies](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP).

### Non-standard features

Do not use non-standard ECMAScript or Web Platform features.

This includes:

*   Old features that have been marked deprecated or removed entirely from ECMAScript / the Web Platform (see [MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Deprecated_and_obsolete_features))

*   New ECMAScript features that are not yet standardized

    *   Avoid using features that are in current TC39 working draft or currently in the [proposal process](https://tc39.es/process-document/)

    *   Use only ECMAScript features defined in the current ECMA-262 specification

*   Proposed but not-yet-complete web standards:

    *   WHATWG proposals that have not completed the [proposal process](https://whatwg.org/faq#adding-new-features).

*   Non-standard language “extensions” (such as those provided by some external transpilers)

Projects targeting specific JavaScript runtimes, such as latest-Chrome-only, Chrome extensions, Node.JS, Electron, can obviously use those APIs. Use caution when considering an API surface that is proprietary and only implemented in some browsers; consider whether there is a common library that can abstract this API surface away for you.

### Modifying builtin objects

Never modify builtin types, either by adding methods to their constructors or to their prototypes. Avoid depending on libraries that do this.

Do not add symbols to the global object unless absolutely necessary (e.g. required by a third-party API).
