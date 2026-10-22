
### What it does

Prefer `RegExp#exec()` over `String#match()` when extracting a regex match.

### Why is this bad?

`exec()` is more explicit about matching with a regular expression and avoids the
overloaded behavior of `String#match()`.

### Examples

Examples of **incorrect** code for this rule:

```ts
const text = "value";
text.match(/v/);
```

Examples of **correct** code for this rule:

```ts
const text = "value";
/v/.exec(text);
```

## How to use

## References
