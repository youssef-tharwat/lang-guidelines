
### What it does

Prefer using `Array#toReversed()` over `Array#reverse()`.

### Why is this bad?

`Array#reverse()` modifies the original array in place, which can lead to unintended side effects—especially
when the original array is used elsewhere in the code.

### Examples

Examples of **incorrect** code for this rule:

```js
const reversed = [...array].reverse();
```

Examples of **correct** code for this rule:

```js
const reversed = [...array].toReversed();
```

## Configuration

This rule accepts a configuration object with the following properties:

### allowExpressionStatement

type: `boolean`

default: `true`

This rule allows `array.reverse()` as an expression statement by default.
Set to `false` to forbid `Array#reverse()` even if it's an expression statement.

Examples of **incorrect** code for this rule with this option set to `false`:

```js
array.reverse();
```

## How to use

## References
