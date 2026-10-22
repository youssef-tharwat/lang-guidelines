
### What it does

Enforces explicit `type` attribute for all the `button` HTML elements.

### Why is this bad?

The default value of `type` attribute for `button` HTML element is
`"submit"` which is often not the desired behavior and may lead to
unexpected page reloads.

### Examples

Examples of **incorrect** code for this rule:

```jsx
<button />
<button type="foo" />
```

Examples of **correct** code for this rule:

```jsx
<button type="button" />
<button type="submit" />
```

## Configuration

This rule accepts a configuration object with the following properties:

### button

type: `boolean`

default: `true`

If true, allow `type="button"`.

### reset

type: `boolean`

default: `true`

If true, allow `type="reset"`.

### submit

type: `boolean`

default: `true`

If true, allow `type="submit"`.

## How to use

## References
