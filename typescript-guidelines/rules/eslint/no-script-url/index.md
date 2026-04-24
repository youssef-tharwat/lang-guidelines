
### What it does

Disallow `javascript:` URLs.

### Why is this bad?

Using `javascript:` URLs is considered by some as a form of `eval`. Code
passed in `javascript:` URLs must be parsed and evaluated by the browser
in the same way that `eval` is processed. This can lead to security and
performance issues.

### Examples

Examples of **incorrect** code for this rule:

```javascript
location.href = "javascript:void(0)";

location.href = `javascript:void(0)`;
```

## How to use

## References
