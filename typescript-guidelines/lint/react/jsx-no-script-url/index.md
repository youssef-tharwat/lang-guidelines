
### What it does

Disallow usage of `javascript:` URLs.

### Why is this bad?

URLs starting with `javascript:` are a dangerous attack surface because it’s easy to accidentally
include unsanitized output in a tag like `<a href>` and create a security hole.

Starting in React 16.9, any URLs starting with `javascript:` log a warning.

In React 19, `javascript:` URLs are
[disallowed entirely](https://react.dev/blog/2024/04/25/react-19-upgrade-guide#other-breaking-changes).

### Examples

Examples of **incorrect** code for this rule:

```jsx
<a href="javascript:void(0)">Test</a>
```

Examples of **correct** code for this rule:

```jsx
<Foo test="javascript:void(0)" />
```

## Configuration

This rule accepts a configuration object with the following properties:

### components

type: `Record<string, array>`

default: `{}`

Additional components to check.

### includeFromSettings

type: `boolean`

default: `false`

Whether to include components from settings.

## How to use

## References
