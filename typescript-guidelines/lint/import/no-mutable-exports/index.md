
### What it does

Forbids the use of mutable exports with var or let.

### Why is this bad?

In general, we should always export constants

### Examples

Examples of **incorrect** code for this rule:

```js
export let count = 2;
export var count = 3;

let count = 4;
export { count };
```

Examples of **correct** code for this rule:

```js
export const count = 1;
export function getCount() {}
export class Counter {}
```

### Functions/Classes

Note that exported function/class declaration identifiers may be reassigned,
but are not flagged by this rule at this time. They may be in the future.

## How to use

## References
