
### What it does

Enforce consistent `break`/`return`/`continue`/`throw` position in `case` clauses.

### Why is this bad?

Enforce that terminating statements (`break`, `return`, `continue`, `throw`) appear inside the block statement of a `case` clause, not after it.
This can happen when refactoring — for example, removing an `if` wrapper but leaving the `break` outside the braces.

### Examples

Examples of **incorrect** code for this rule:

```js
switch (foo) {
  case 1:
    {
      doStuff();
    }
    break;
}
```

Examples of **correct** code for this rule:

```js
switch (foo) {
  case 1: {
    doStuff();
    break;
  }
}
```

## How to use

## References
