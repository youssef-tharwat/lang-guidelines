
### What it does

Forbids imports that use an expression for the module argument. This includes
dynamically resolved paths in `require` or `import` statements.

### Why is this bad?

Using expressions that are resolved at runtime in import statements makes it
difficult to determine where the module is being imported from. This can complicate
code navigation and hinder static analysis tools, which rely on predictable module paths
for linting, bundling, and other optimizations.

### Examples

Examples of **incorrect** code for this rule:

```javascript
require(name);
require(`../${name}`);
```

Examples of **correct** code for this rule:

```javascript
require("../name");
require(`../name`);
```

## Configuration

This rule accepts a configuration object with the following properties:

### esmodule

type: `boolean`

default: `false`

When `true`, also check `import()` expressions for dynamic module specifiers.

## How to use

## References
