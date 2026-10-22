
### What it does

This rule bans specific types and can suggest alternatives. Note that it does not ban the corresponding runtime objects from being used.

::: warning
This rule is deprecated and will be removed in a future release.

Prefer these replacement rules:

* `typescript/no-empty-object-type`
* `typescript/no-unsafe-function-type`
* `typescript/no-wrapper-object-types`
* `typescript/no-restricted-types` (for custom type bans)
  :::

### Why is this bad?

Some built-in types have aliases, while some types are considered dangerous or harmful. It's often a good idea to ban certain types to help with consistency and safety.

### Examples

Examples of **incorrect** code for this rule:

```typescript
let foo: String = "foo";

let bar: Boolean = true;
```

Examples of **correct** code for this rule:

```typescript
let foo: string = "foo";

let bar: boolean = true;
```

## How to use

## References
