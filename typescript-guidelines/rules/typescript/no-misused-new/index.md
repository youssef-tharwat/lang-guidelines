
### What it does

Enforces valid definition of new and constructor. This rule prevents classes from defining
a method named `new` and interfaces from defining a method named `constructor`.

### Why is this bad?

JavaScript classes may define a constructor method that runs
when a class instance is newly created.

TypeScript allows interfaces that describe a static class object to
define a `new()` method (though this is rarely used in real world code).
Developers new to JavaScript classes and/or TypeScript interfaces may
sometimes confuse when to use constructor or new.

### Examples

Examples of **incorrect** code for this rule:

```typescript
declare class C {
  new(): C;
}
```

```typescript
interface I {
  new (): I;
  constructor(): void;
}
```

Examples of **correct** code for this rule:

```typescript
declare class C {
  constructor();
}
```

```typescript
interface I {
  new (): C;
}
```

## How to use

## References
