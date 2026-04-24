
### What it does

Disallow modifications to read-only global variables.

### Why is this bad?

In almost all cases, you don't want to assign a value to these global variables as doing so could result in losing access to important functionality.

### Examples

Examples of **incorrect** code for this rule:

```javascript
Object = null;
```

## Configuration

This rule accepts a configuration object with the following properties:

### exceptions

type: `string[]`

default: `[]`

List of global variable names to exclude from this rule.
Globals listed here can be assigned to without triggering warnings.

## How to use

## References
