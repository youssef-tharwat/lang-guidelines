
### What it does

Disallows the redefining of global variables such as `undefined`, `NaN`, `Infinity`,
`eval`, `globalThis` and `arguments`.

### Why is this bad?

Value properties of the Global Object `NaN`, `Infinity`, `undefined`, `globalThis` as well as the strict
mode restricted identifiers `eval` and `arguments` are considered to be restricted names in
JavaScript. Defining them to mean something else can have unintended consequences and
confuse others reading the code. For example, there’s nothing preventing you from
writing:

```javascript
var undefined = "foo";
```

Then any code used within the same scope would not get the global `undefined`, but rather the
local version with a very different meaning.

### Examples

Examples of **incorrect** code for this rule:

```javascript
function NaN() {}

!function (Infinity) {};

var undefined = 5;

try {
} catch (eval) {}

const globalThis = "foo";
```

```javascript
import NaN from "foo";

import { undefined } from "bar";

class Infinity {}
```

Examples of **correct** code for this rule:

```javascript
var Object;

function f(a, b) {}

// Exception: `undefined` may be shadowed if the variable is never assigned a value.
var undefined;
```

```javascript
import { undefined as undef } from "bar";
```

## Configuration

This rule accepts a configuration object with the following properties:

### reportGlobalThis

type: `boolean`

default: `true`

If true, also report shadowing of `globalThis`.

## How to use

## References
