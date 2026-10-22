
### What it does

Require or disallow method and property shorthand syntax for object literals

### Why is this bad?

Stylistic preference

### Example

Here are a few common examples using the ES5 syntax:

```javascript
var properties = { x: x, y: y, z: z };
var methods = { a: function () {}, b: function () {} };
```

Now here are ES6 equivalents:

```javascript
var properties = { x, y, z };
var methods = { a() {}, b() {} };
```

## Configuration

### The 1st option

type: `"always" | "methods" | "properties" | "consistent" | "consistent-as-needed" | "never"`

### The 2nd option

This option is an object with the following properties:

#### avoidExplicitReturnArrows

type: `boolean`

default: `false`

#### avoidQuotes

type: `boolean`

default: `false`

#### ignoreConstructors

type: `boolean`

default: `false`

#### methodsIgnorePattern

type: `string`

## How to use

## References
