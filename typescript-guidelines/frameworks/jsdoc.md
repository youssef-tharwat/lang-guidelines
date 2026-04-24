# Jsdoc Rules (TypeScript & JavaScript)

18 rules that apply when the project uses **jsdoc**.
Load this file only if the project's manifest imports or depends on
`jsdoc`.

---

### jsdoc/check-access
Ensure `@access` tags use one of the following values: * "package", "private", "protected", "public" Also reports: * Mixing of `@access` with `@public`, `@private`, `@protected`, or `@package` on the same doc block.
❌ 
```
/** @access private @public */
/** @access invalidlevel */
```
✅ 
```
/** @access private */
/** @private */
```

### jsdoc/check-property-names
Ensures that property names in JSDoc are not duplicated on the same block and that nested properties have defined roots.
❌ 
```
/**
 * @typedef {object} state
 * @property {number} foo
 * @property {string} foo
 */
/**
…
```
✅ 
```
/**
 * @typedef {object} state
 * @property {number} foo
 */
/**
 * @typedef {object} state
…
```

### jsdoc/check-tag-names
Avoid invalid block tag names.
❌ 
```
/** @Param */
/** @foo */
/**
 * This is redundant when typed.
 * @type {string}
 */
```
✅ `/** @param */`

### jsdoc/empty-tags
Expects the following tags to be empty of any content: * `@abstract` * `@async` * `@generator` * `@global` * `@hideconstructor` * `@ignore` * `@inner` * `@instance` * `@override` * `@readonly` * `@inheritDoc` * `@internal` * `@overload` *…
❌ 
```
/** @async foo */
/** @private bar */
```
✅ 
```
/** @async */
/** @private */
```

### jsdoc/implements-on-classes
Avoid an issue with any non-constructor function using `@implements`.
❌ 
```
/**
 * @implements {SomeClass}
 */
function quux() {}
```
✅ 
```
class Foo {
  /**
   * @implements {SomeClass}
   */
  constructor() {}
}
…
```

### jsdoc/no-defaults
This rule reports defaults being used on the relevant portion of `@param` or `@default`.
❌ 
```
/** @param {number} [foo="7"] */
function quux(foo) {}
```
✅ 
```
/** @param {number} foo */
function quux(foo) {}
/** @param foo */
function quux(foo) {}
```

### jsdoc/require-param
Require that all function parameters are documented with JSDoc `@param` tags.
❌ 
```
/** @param foo */
function quux(foo, bar) {}
```
✅ 
```
/** @param foo */
function quux(foo) {}
```

### jsdoc/require-param-description
Require that each `@param` tag has a description value.
❌ 
```
/** @param foo */
function quux(foo) {}
```
✅ 
```
/** @param foo Foo. */
function quux(foo) {}
```

### jsdoc/require-param-name
Require that all `@param` tags have names.
❌ 
```
/** @param {SomeType} */
function quux(foo) {}
```
✅ 
```
/** @param {SomeType} foo */
function quux(foo) {}
```

### jsdoc/require-param-type
Require that each `@param` tag has a type value (within curly brackets).
❌ 
```
/** @param foo */
function quux(foo) {}
```
✅ 
```
/** @param {SomeType} foo */
function quux(foo) {}
```

### jsdoc/require-property
Require that all `@typedef` and `@namespace` tags have `@property` tags when their type is a plain `object`, `Object`, or `PlainObject`.
❌ 
```
/**
 * @typedef {Object} SomeTypedef
 */
/**
 * @namespace {Object} SomeNamespace
 */
```
✅ 
```
/**
 * @typedef {Object} SomeTypedef
 * @property {SomeType} propName Prop description
 */
/**
 * @typedef {object} Foo
…
```

### jsdoc/require-property-description
Require that all `@property` tags have descriptions.
❌ 
```
/**
 * @typedef {SomeType} SomeTypedef
 * @property {number} foo
 */
```
✅ 
```
/**
 * @typedef {SomeType} SomeTypedef
 * @property {number} foo Foo.
 */
```

### jsdoc/require-property-name
Require that all `@property` tags have names.
❌ 
```
/**
 * @typedef {SomeType} SomeTypedef
 * @property {number}
 */
```
✅ 
```
/**
 * @typedef {SomeType} SomeTypedef
 * @property {number} foo
 */
```

### jsdoc/require-property-type
Require that each `@property` tag has a type value (within curly brackets).
❌ 
```
/**
 * @typedef {SomeType} SomeTypedef
 * @property foo
 */
```
✅ 
```
/**
 * @typedef {SomeType} SomeTypedef
 * @property {number} foo
 */
```

### jsdoc/require-returns
Require that return statements are documented.
❌ 
```
/** Foo. */
function quux() {
  return foo;
}
/**
 * @returns Foo!
…
```
✅ 
```
/** @returns Foo. */
function quux() {
  return foo;
}
```

### jsdoc/require-returns-description
Require that the `@returns` tag has a description value.
❌ 
```
/** @returns */
function quux(foo) {}
```
✅ 
```
/** @returns Foo. */
function quux(foo) {}
```

### jsdoc/require-returns-type
Require that `@returns` tag has a type value (in curly brackets).
❌ 
```
/** @returns */
function quux(foo) {}
```
✅ 
```
/** @returns {string} */
function quux(foo) {}
```

### jsdoc/require-yields
Require that yields are documented.
❌ 
```
function* quux(foo) {
  yield foo;
}
/**
 * @yields {undefined}
 * @yields {void}
…
```
✅ 
```
/** * @yields Foo */
function* quux(foo) {
  yield foo;
}
```
