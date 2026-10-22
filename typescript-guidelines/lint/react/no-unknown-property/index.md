
### What it does

Disallow usage of unknown DOM properties.

### Why is this bad?

DOM properties should only be used if they are valid for a given HTML element.

### Examples

Examples of **incorrect** code for this rule:

```jsx
// Unknown properties
const Hello = <div class="hello">Hello World</div>;
const Alphabet = <div abc="something">Alphabet</div>;

// Invalid aria-* attribute
const IconButton = <div aria-foo="bar" />;
```

Examples of **correct** code for this rule:

```jsx
// Unknown properties
const Hello = <div className="hello">Hello World</div>;
const Alphabet = <div>Alphabet</div>;

// Invalid aria-* attribute
const IconButton = <div aria-label="bar" />;
```

## Configuration

This rule accepts a configuration object with the following properties:

### ignore

type: `string[]`

default: `[]`

List of properties to ignore.

### requireDataLowercase

type: `boolean`

default: `false`

Require `data-*` attributes to be lowercase, e.g. `data-foobar` instead of `data-fooBar`.

## How to use

## References
