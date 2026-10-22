
### What it does

Enforce using `export type` for exports that are only used as types.

### Why is this bad?

Mixing type-only exports with value exports without `export type` makes module intent
harder to read and can cause unnecessary runtime export surface.

### Examples

Examples of **incorrect** code for this rule:

```ts
type Foo = { bar: string };
export { Foo };

export { TypeOnly, value } from "./mod";
```

Examples of **correct** code for this rule:

```ts
type Foo = { bar: string };
export type { Foo };

export type { TypeOnly } from "./mod";
export { value } from "./mod";
```

## Configuration

This rule accepts a configuration object with the following properties:

### fixMixedExportsWithInlineTypeSpecifier

type: `boolean`

default: `false`

Enables an autofix strategy that rewrites mixed exports using inline `type` specifiers.

## How to use

## References
