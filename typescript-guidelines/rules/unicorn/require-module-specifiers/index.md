
### What it does

Enforce non-empty specifier list in `import` and `export` statements.

### Why is this bad?

Empty `import`/`export` specifiers add no value and can be confusing.
If you want to import a module for side effects, use `import 'module'` instead.

### Examples

Examples of **incorrect** code for this rule:

```js
import {} from "foo";
import foo from "foo";
export {} from "foo";
export {};
```

Examples of **correct** code for this rule:

```js
import "foo";
import foo from "foo";
```

## How to use

## References
