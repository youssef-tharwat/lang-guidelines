# string-and-number-literals

Use single-quoted strings and template literals instead of complex concatenation; never continue a string with a trailing backslash; write number prefixes as lowercase `0x`, `0o`, `0b`.

**Why:** Line continuations hide stray whitespace.

**Sources:** G:primitive-literals

---

## Primitive literals (G:primitive-literals)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#primitive-literals), CC BY 3.0.

### String literals

#### Use single quotes

Ordinary string literals are delimited with single quotes (`'`), rather than double quotes (`"`).

Tip: if a string contains a single quote character, consider using a template string to avoid having to escape the quote.

#### No line continuations

Do not use _line continuations_ (that is, ending a line inside a string literal with a backslash) in either ordinary or template string literals. Even though ES5 allows this, it can lead to tricky errors if any trailing whitespace comes after the slash, and is less obvious to readers.

Disallowed:

❌ Bad:

```ts
const LONG_STRING = 'This is a very very very very very very very long string. \
    It inadvertently contains long stretches of spaces due to how the \
    continued lines are indented.';
```

Instead, write

✅ Good:

```ts
const LONG_STRING = 'This is a very very very very very very long string. ' +
    'It does not contain long stretches of spaces because it uses ' +
    'concatenated strings.';
const SINGLE_STRING =
    'http://it.is.also/acceptable_to_use_a_single_long_string_when_breaking_would_hinder_search_discoverability';
```

#### Template literals

Use template literals (delimited with ```) over complex string concatenation, particularly if multiple string literals are involved. Template literals may span multiple lines.

If a template literal spans multiple lines, it does not need to follow the indentation of the enclosing block, though it may if the added whitespace does not matter.

Example:

✅ Good:

```ts
function arithmetic(a: number, b: number) {
  return `Here is a table of arithmetic operations:
${a} + ${b} = ${a + b}
${a} - ${b} = ${a - b}
${a} * ${b} = ${a * b}
${a} / ${b} = ${a / b}`;
}
```

### Number literals

Numbers may be specified in decimal, hex, octal, or binary. Use exactly `0x`, `0o`, and `0b` prefixes, with lowercase letters, for hex, octal, and binary, respectively. Never include a leading zero unless it is immediately followed by `x`, `o`, or `b`.

### Type coercion

TypeScript code _may_ use the `String()` and `Boolean()` (note: no `new`!) functions, string template literals, or `!!` to coerce types.

✅ Good:

```ts
const bool = Boolean(false);
const str = String(aNumber);
const bool2 = !!str;
const str2 = `result: ${bool2}`;
```

Values of enum types (including unions of enum types and other types) _must not_ be converted to booleans with `Boolean()` or `!!`, and must instead be compared explicitly with comparison operators.

❌ Bad:

```ts
enum SupportLevel {
  NONE,
  BASIC,
  ADVANCED,
}

const level: SupportLevel = ...;
let enabled = Boolean(level);

const maybeLevel: SupportLevel|undefined = ...;
enabled = !!maybeLevel;
```

✅ Good:

```ts
enum SupportLevel {
  NONE,
  BASIC,
  ADVANCED,
}

const level: SupportLevel = ...;
let enabled = level !== SupportLevel.NONE;

const maybeLevel: SupportLevel|undefined = ...;
enabled = level !== undefined && level !== SupportLevel.NONE;
```

**Why?**

For most purposes, it doesn't matter what number or string value an enum name is mapped to at runtime, because values of enum types are referred to by name in source code. Consequently, engineers are accustomed to not thinking about this, and so situations where it _does_ matter are undesirable because they will be surprising. Such is the case with conversion of enums to booleans; in particular, by default, the first declared enum value is falsy (because it is 0) while the others are truthy, which is likely to be unexpected. Readers of code that uses an enum value may not even know whether it's the first declared value or not.

Using string concatenation to cast to string is discouraged, as we check that operands to the plus operator are of matching types.

Code _must_ use `Number()` to parse numeric values, and _must_ check its return for `NaN` values explicitly, unless failing to parse is impossible from context.

Note: `Number('')`, `Number(' ')`, and `Number('\t')` would return `0` instead of `NaN`. `Number('Infinity')` and `Number('-Infinity')` would return `Infinity` and `-Infinity` respectively. Additionally, exponential notation such as `Number('1e+309')` and `Number('-1e+309')` can overflow into `Infinity`. These cases may require special handling.

✅ Good:

```ts
const aNumber = Number('123');
if (!isFinite(aNumber)) throw new Error(...);
```

Code _must not_ use unary plus (`+`) to coerce strings to numbers. Parsing numbers can fail, has surprising corner cases, and can be a code smell (parsing at the wrong layer). A unary plus is too easy to miss in code reviews given this.

❌ Bad:

```ts
const x = +y;
```

Code also _must not_ use `parseInt` or `parseFloat` to parse numbers, except for non-base-10 strings (see below). Both of those functions ignore trailing characters in the string, which can shadow error conditions (e.g. parsing `12 dwarves` as `12`).

❌ Bad:

```ts
const n = parseInt(someString, 10);  // Error prone,
const f = parseFloat(someString);    // regardless of passing a radix.
```

Code that requires parsing with a radix _must_ check that its input contains only appropriate digits for that radix before calling into `parseInt`;

✅ Good:

```ts
if (!/^[a-fA-F0-9]+$/.test(someString)) throw new Error(...);
// Needed to parse hexadecimal.
// tslint:disable-next-line:ban
const n = parseInt(someString, 16);  // Only allowed for radix != 10
```

Use `Number()` followed by `Math.floor` or `Math.trunc` (where available) to parse integer numbers:

✅ Good:

```ts
let f = Number(someString);
if (isNaN(f)) handleError();
f = Math.floor(f);
```

#### Implicit coercion

Do not use explicit boolean coercions in conditional clauses that have implicit boolean coercion. Those are the conditions in an `if`, `for` and `while` statements.

❌ Bad:

```ts
const foo: MyInterface|null = ...;
if (!!foo) {...}
while (!!foo) {...}
```

✅ Good:

```ts
const foo: MyInterface|null = ...;
if (foo) {...}
while (foo) {...}
```

As with explicit conversions, values of enum types (including unions of enum types and other types) _must not_ be implicitly coerced to booleans, and must instead be compared explicitly with comparison operators.

❌ Bad:

```ts
enum SupportLevel {
  NONE,
  BASIC,
  ADVANCED,
}

const level: SupportLevel = ...;
if (level) {...}

const maybeLevel: SupportLevel|undefined = ...;
if (level) {...}
```

✅ Good:

```ts
enum SupportLevel {
  NONE,
  BASIC,
  ADVANCED,
}

const level: SupportLevel = ...;
if (level !== SupportLevel.NONE) {...}

const maybeLevel: SupportLevel|undefined = ...;
if (level !== undefined && level !== SupportLevel.NONE) {...}
```

Other types of values may be either implicitly coerced to booleans or compared explicitly with comparison operators:

✅ Good:

```ts
// Explicitly comparing > 0 is OK:
if (arr.length > 0) {...}
// so is relying on boolean coercion:
if (arr.length) {...}
```
