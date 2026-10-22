
### What it does

When constructing a generic class, you can specify the type arguments on either the left-hand side (as a type annotation) or the right-hand side (as part of the constructor call).

This rule enforces consistency in the way generic constructors are used.

### Why is this bad?

Inconsistent usage of generic constructors can make the code harder to read and maintain.

### Examples

Examples of **incorrect** code for this rule:

```ts
const a: Foo<string> = new Foo();
const a = new Foo<string>(); // prefer type annotation
```

Examples of **correct** code for this rule:

```ts
const a = new Foo<string>();
const a: Foo<string> = new Foo(); // prefer type annotation
```

## Configuration

This rule accepts a configuration object with the following properties:

### option

type: `"constructor" | "type-annotation"`

default: `"constructor"`

Specifies where the generic type should be specified.

Possible values:

* `"constructor"` (default): Type arguments that only appear on the type annotation are disallowed.
* `"type-annotation"`: Type arguments that only appear on the constructor are disallowed.

#### `"constructor"`

Type arguments that only appear on the type annotation are disallowed.

#### `"type-annotation"`

Type arguments that only appear on the constructor are disallowed.

## How to use

## References
