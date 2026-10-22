
### What it does

Enforces the presence of `rel="preconnect"` when using Google Fonts via `<link>` tags.

### Why is this bad?

When using Google Fonts, it's recommended to include a preconnect resource hint to establish early connections to the required origin.
Without preconnect, the browser needs to perform DNS lookups, TCP handshakes, and TLS negotiations before it can download the font files,
which can delay font loading and impact performance.

### Examples

Examples of **incorrect** code for this rule:

```javascript
<link href="https://fonts.gstatic.com" />
<link rel="preload" href="https://fonts.gstatic.com" />
```

Examples of **correct** code for this rule:

```javascript
<link rel="preconnect" href="https://fonts.gstatic.com" />
```

## How to use

## References
