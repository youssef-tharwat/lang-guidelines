
### What it does

Enforces that code does not include a redundant `role` property, in the
case that it's identical to the implicit `role` property of the
element type.

### Why is this bad?

Redundant roles can lead to confusion and verbosity in the codebase.

### Examples

This rule applies for the following elements and their implicit roles:

* `<nav>`: `navigation`
* `<button>`: `button`
* `<body>`: `document`

Examples of **incorrect** code for this rule:

```jsx
<nav role="navigation"></nav>
<button role="button"></button>
<body role="document"></body>
```

Examples of **correct** code for this rule:

```jsx
<nav></nav>
<button></button>
<body></body>
```

## How to use

## References
