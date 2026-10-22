
### What it does

Disallows using variables before they are defined.

### Why is this bad?

Referencing identifiers before their declarations can hide bugs and
make code order-dependent and difficult to reason about.

### Examples

Examples of **incorrect** code for this rule:

```ts
new A();
var A = class {};
```

Examples of **correct** code for this rule:

```ts
var A = class {};
new A();
```

## Configuration

This rule accepts a configuration object with the following properties:

### allowNamedExports

type: `boolean`

default: `false`

Allow named exports that appear before declaration.

### classes

type: `boolean`

default: `true`

Check class declarations.

### enums

type: `boolean`

default: `true`

Check enum declarations.

### functions

type: `boolean`

default: `true`

Check function declarations.

### ignoreTypeReferences

type: `boolean`

default: `true`

Ignore usages that are type-only references.

### typedefs

type: `boolean`

default: `true`

Check type aliases, interfaces, and type parameters.

### variables

type: `boolean`

default: `true`

Check variable declarations.

## How to use

## References
