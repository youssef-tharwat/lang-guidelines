
### What it does

Disallows throwing literals or non-Error objects as exceptions.

::: warning
This rule has been deprecated, please instead use [typescript/only-throw-error](https://oxc.rs/docs/guide/usage/linter/rules/typescript/only-throw-error.html).
The typescript rule is more reliable than the Javascript version, as it has less false positive, and can catch more cases.
:::

### Why is this bad?

It is considered good practice to only throw the Error object itself or an object using
the Error object as base objects for user-defined exceptions. The fundamental benefit of
Error objects is that they automatically keep track of where they were built and originated.

### Examples

Examples of **incorrect** code for this rule:

```js
throw "error";

throw 0;

throw undefined;

throw null;

var err = new Error();
throw "an " + err;
// err is recast to a string literal

var err = new Error();
throw `${err}`;
```

Examples of **correct** code for this rule:

```js
throw new Error();

throw new Error("error");

var e = new Error("error");
throw e;

try {
  throw new Error("error");
} catch (e) {
  throw e;
}
```

## How to use

## References
