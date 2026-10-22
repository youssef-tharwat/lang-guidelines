
### What it does

Disallow conditions that are always truthy, always falsy, or always nullish
based on TypeScript's type information.

### Why is this bad?

Conditions with no possible runtime variation make code harder to read and can
hide logic errors. They often leave dead branches and suggest that the declared
types do not match the intended behavior.

### Examples

Examples of **incorrect** code for this rule:

```ts
declare const value: null;
if (value) {
  doWork();
}

const items: string[] = [];
if (items) {
  doWork();
}

declare const status: "ready";
if (!status) {
  reportError();
}
```

Examples of **correct** code for this rule:

```ts
declare const maybeUser: User | undefined;
if (maybeUser) {
  doWork(maybeUser);
}

const items: string[] = [];
if (items.length > 0) {
  doWork();
}

declare const status: "ready" | "";
if (!status) {
  reportError();
}
```

## Configuration

This rule accepts a configuration object with the following properties:

### allowConstantLoopConditions

type: `boolean | "never" | "always" | "only-allowed-literals"`

Represents the different ways `allowConstantLoopConditions` can be specified in JSON.
Can be:

* `true` or `false`
* A string enum (`"never"`, `"always"`, `"only-allowed-literals"`)

### checkTypePredicates

type: `boolean`

default: `false`

Whether to check type predicate functions.

## How to use

## References
