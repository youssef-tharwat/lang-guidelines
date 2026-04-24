
### What it does

Disallows unnecessary standalone block statements.

### Why is this bad?

Standalone blocks can be confusing as they do not provide any meaningful purpose when used unnecessarily.
They may introduce extra nesting, reducing code readability, and can mislead readers about scope or intent.

### Examples

Examples of **incorrect** code for this rule:

```js
{
  var x = 1;
}
```

Examples of **correct** code for this rule:

```js
if (condition) {
  var x = 1;
}

{
  let x = 1; // Used to create a valid block scope.
}
```

## How to use

## References
