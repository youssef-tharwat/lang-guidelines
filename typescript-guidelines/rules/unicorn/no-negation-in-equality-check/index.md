
### What it does

Disallow negated expressions on the left of (in)equality checks.

### Why is this bad?

A negated expression on the left of an (in)equality check is likely a mistake from trying to negate the whole condition.

### Examples

Examples of **incorrect** code for this rule:

```javascript
if (!foo === bar) {
}

if (!foo !== bar) {
}
```

Examples of **correct** code for this rule:

```javascript
if (foo !== bar) {
}

if (!(foo === bar)) {
}
```

## How to use

## References
