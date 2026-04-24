
### What it does

Requires or disallows parameter properties in class constructors.

### Why is this bad?

Mixing parameter properties and class property declarations can make
class style inconsistent and harder to maintain.

### Examples

#### `{ "prefer": "class-property" }` (default)

Examples of **incorrect** code for this rule:

```ts
class Foo {
  constructor(private name: string) {}
}
```

Examples of **correct** code for this rule:

```ts
class Foo {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}
```

#### `{ "prefer": "parameter-property" }`

Examples of **incorrect** code for this rule:

```ts
class Foo {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}
```

Examples of **correct** code for this rule:

```ts
class Foo {
  constructor(private name: string) {}
}
```

## Configuration

This rule accepts a configuration object with the following properties:

### allow

type: `array`

default: `[]`

Modifiers that are allowed to be used with parameter properties or class properties, depending on the `prefer` option.

#### allow\[n]

type: `"private" | "private readonly" | "protected" | "protected readonly" | "public" | "public readonly" | "readonly"`

### prefer

type: `"class-property" | "parameter-property"`

default: `"class-property"`

Whether to prefer parameter properties or class properties.

## How to use

## References
