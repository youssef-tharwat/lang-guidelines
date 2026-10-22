
### What it does

This rule can enforce or disallow the use of braces around arrow function body.
Arrow functions can use either:

* a block body `() => { ... }`
* or a concise body `() => expression` with an implicit return.

### Why is this bad?

Inconsistent use of block vs. concise bodies makes code harder to read.
Concise bodies are limited to a single expression, whose value is implicitly returned.

### Options

First option:

* Type: `string`
* Enum: `"always"`, `"as-needed"`, `"never"`
* Default: `"as-needed"`

Possible values:

* `never` enforces no braces around the function body (constrains arrow functions to the role of returning an expression)
* `always` enforces braces around the function body
* `as-needed` enforces no braces where they can be omitted (default)

Second option:

* Type: `object`
* Properties:
  * `requireReturnForObjectLiteral`: `boolean` (default: `false`) - requires braces and an explicit return for object literals.

Note: This option only applies when the first option is `"as-needed"`.

Example configuration:

```json
{
  "arrow-body-style": ["error", "as-needed", { "requireReturnForObjectLiteral": true }]
}
```

### Examples

#### `"never"`

Examples of **incorrect** code for this rule with the `never` option:

```js
/* arrow-body-style: ["error", "never"] */

/* ✘ Bad: */
const foo = () => {
  return 0;
};
```

Examples of **correct** code for this rule with the `never` option:

```js
/* arrow-body-style: ["error", "never"] */

/* ✔ Good: */
const foo = () => 0;
const bar = () => ({ foo: 0 });
```

#### `"always"`

Examples of **incorrect** code for this rule with the `always` option:

```js
/* arrow-body-style: ["error", "always"] */

/* ✘ Bad: */
const foo = () => 0;
```

Examples of **correct** code for this rule with the `always` option:

```js
/* arrow-body-style: ["error", "always"] */

/* ✔ Good: */
const foo = () => {
  return 0;
};
```

#### `"as-needed"` (default)

Examples of **incorrect** code for this rule with the `as-needed` option:

```js
/* arrow-body-style: ["error", "as-needed"] */

/* ✘ Bad: */
const foo = () => {
  return 0;
};
```

Examples of **correct** code for this rule with the `as-needed` option:

```js
/* arrow-body-style: ["error", "as-needed"] */

/* ✔ Good: */
const foo1 = () => 0;

const foo2 = (retv, name) => {
  retv[name] = true;
  return retv;
};

const foo3 = () => {
  bar();
};
```

#### `"as-needed"` with `requireReturnForObjectLiteral`

Examples of **incorrect** code for this rule with the `{ "requireReturnForObjectLiteral": true }` option:

```js
/* arrow-body-style: ["error", "as-needed", { "requireReturnForObjectLiteral": true }] */

/* ✘ Bad: */
const foo = () => ({});
const bar = () => ({ bar: 0 });
```

Examples of **correct** code for this rule with the `{ "requireReturnForObjectLiteral": true }` option:

```js
/* arrow-body-style: ["error", "as-needed", { "requireReturnForObjectLiteral": true }] */

/* ✔ Good: */
const foo = () => {};
const bar = () => {
  return { bar: 0 };
};
```

## Configuration

### The 1st option

type: `"as-needed" | "always" | "never"`

### The 2nd option

This option is an object with the following properties:

#### requireReturnForObjectLiteral

type: `boolean`

default: `false`

## How to use

## References
