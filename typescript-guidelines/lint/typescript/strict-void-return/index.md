
### What it does

Disallow returning non-void values where a `void` return is expected.

### Why is this bad?

Returning values from `void` contexts can hide logic errors and make callback APIs
behave unexpectedly.

### Examples

Examples of **incorrect** code for this rule:

```ts
declare function run(cb: () => void): void;

run(() => "value");
run(async () => 123);
```

Examples of **correct** code for this rule:

```ts
declare function run(cb: () => void): void;

run(() => {
  doWork();
});

run(() => undefined);
```

## Configuration

This rule accepts a configuration object with the following properties:

### allowReturnAny

type: `boolean`

default: `false`

Allow callbacks that return `any` in places that expect a `void` callback.

## How to use

## References
