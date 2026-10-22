
### What it does

Enforces that named import blocks are not empty.

### Why is this bad?

Empty named imports serve no practical purpose and often
result from accidental deletions or tool-generated code.

### Examples

Examples of **incorrect** code for this rule:

```js
import {} from "mod";
import Default from "mod";
```

Examples of **correct** code for this rule:

```js
import { mod } from "mod";
import Default, { mod } from "mod";
```

## How to use

## References
