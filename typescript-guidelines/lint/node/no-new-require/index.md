
### What it does

Warn about calling `new` on `require`.

### Why is this bad?

The `require` function is used to include modules and might return a constructor. As this
is not always the case this can be confusing.

### Examples

Examples of **incorrect** code for this rule:

```js
var appHeader = new require("app-header");
```

Examples of **correct** code for this rule:

```js
var AppHeader = require("app-header");
var appHeader = new AppHeader();
```

## How to use

## References
