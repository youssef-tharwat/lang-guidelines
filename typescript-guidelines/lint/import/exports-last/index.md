
### What it does

This rule enforces that all exports are declared at the bottom of the file.
This rule will report any export declarations that comes before any non-export statements.

### Why is this bad?

Exports scattered throughout the file can lead to poor code readability
and increase the cost of locating the export quickly

### Examples

Examples of **incorrect** code for this rule:

```js
const bool = true;
export const foo = "bar";
const str = "foo";
```

Examples of **correct** code for this rule:

```js
const arr = ["bar"];
export const bool = true;
export const str = "foo";
export function func() {
  console.log("Hello World");
}
```

## How to use

## References
