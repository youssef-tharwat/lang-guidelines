
### What it does

Enforces that no distracting elements are used.

### Why is this bad?

Elements that can be visually distracting can cause accessibility issues
with visually impaired users. Such elements are most likely deprecated,
and should be avoided. By default, `<marquee>` and `<blink>` elements
are visually distracting and can trigger vestibular disorders.

### Examples

Examples of **incorrect** code for this rule:

```jsx
<marquee />
<marquee {...props} />
<marquee lang={undefined} />
<blink />
<blink {...props} />
<blink foo={undefined} />
```

Examples of **correct** code for this rule:

```jsx
<div />
<Marquee />
<Blink />
```

## Configuration

This rule accepts a configuration object with the following properties:

### elements

type: `array`

List of distracting elements to check for.

#### elements\[n]

type: `"marquee" | "blink"`

## How to use

## References
