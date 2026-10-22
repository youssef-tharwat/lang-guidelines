
### What it does

This rule disallows unnecessary equality comparisons with boolean literals.

### Why is this bad?

Comparing boolean values to boolean literals is unnecessary when the comparison can be eliminated. These comparisons make code more verbose without adding value.

### Examples

Examples of **incorrect** code for this rule:

```ts
declare const someCondition: boolean;

if (someCondition === true) {
  // ...
}

if (someCondition === false) {
  // ...
}

if (someCondition !== true) {
  // ...
}

if (someCondition !== false) {
  // ...
}

const result = someCondition == true;
```

Examples of **correct** code for this rule:

```ts
declare const someCondition: boolean;

if (someCondition) {
  // ...
}

if (!someCondition) {
  // ...
}

// Comparisons with non-boolean types are allowed
declare const someValue: unknown;
if (someValue === true) {
  // ...
}
```

## Configuration

This rule accepts a configuration object with the following properties:

### allowComparingNullableBooleansToFalse

type: `boolean`

default: `true`

Whether to allow comparing nullable boolean expressions to `false`.
When false, `x === false` where x is `boolean | null` will be flagged.

### allowComparingNullableBooleansToTrue

type: `boolean`

default: `true`

Whether to allow comparing nullable boolean expressions to `true`.
When false, `x === true` where x is `boolean | null` will be flagged.

## How to use

## References
