
### What it does

Disallow unnecessary constraints on generic types.

### Why is this bad?

Generic type parameters (`<T>`) in TypeScript may be "constrained" with an `extends`
keyword. When no `extends` is provided, type parameters default a constraint to `unknown`.
It is therefore redundant to `extend` from `any` or `unknown`.

### Examples

Examples of **incorrect** code for this rule:

```typescript
interface FooAny<T extends any> {}
interface FooUnknown<T extends unknown> {}

type BarAny<T extends any> = {};
type BarUnknown<T extends unknown> = {};

const QuuxAny = <T extends any>() => {};

function QuuzAny<T extends any>() {}
```

```typescript
class BazAny<T extends any> {
  quxAny<U extends any>() {}
}
```

Examples of **correct** code for this rule:

```typescript
interface Foo<T> {}

type Bar<T> = {};

const Quux = <T>() => {};

function Quuz<T>() {}
```

```typescript
class Baz<T> {
  qux<U>() {}
}
```

## How to use

## References
