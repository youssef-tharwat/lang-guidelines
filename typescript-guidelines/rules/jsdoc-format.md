# jsdoc-format

Write JSDoc in Markdown (real lists, not indented text), one tag per line with wrapped tag text indented four spaces, and never JSDoc type annotations in TypeScript (`@param {T}`, `@private`, `@override`).

**Why:** Tools parse JSDoc; TypeScript already holds the types.

**Sources:** G:jsdoc-general-form, G:jsdoc-markdown, G:jsdoc-tags, G:jsdoc-line-wrapping, G:jsdoc-type-annotations

---

## JSDoc general form (G:jsdoc-general-form)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#jsdoc-general-form), CC BY 3.0.

The basic formatting of JSDoc comments is as seen in this example:

✅ Good:

```ts
/**
 * Multiple lines of JSDoc text are written here,
 * wrapped normally.
 * @param arg A number to do something to.
 */
function doSomething(arg: number) { … }
```

or in this single-line example:

✅ Good:

```ts
/** This short jsdoc describes the function. */
function doSomething(arg: number) { … }
```

If a single-line comment overflows into multiple lines, it _must_ use the multi-line style with `/**` and `*/` on their own lines.

Many tools extract metadata from JSDoc comments to perform code validation and optimization. As such, these comments _must_ be well-formed.


## Markdown (G:jsdoc-markdown)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#jsdoc-markdown), CC BY 3.0.

JSDoc is written in Markdown, though it _may_ include HTML when necessary.

This means that tooling parsing JSDoc will ignore plain text formatting, so if you did this:

❌ Bad:

```ts
/**
 * Computes weight based on three factors:
 *   items sent
 *   items received
 *   last timestamp
 */
```

it will be rendered like this:

```
Computes weight based on three factors: items sent items received last timestamp
```

Instead, write a Markdown list:

✅ Good:

```ts
/**
 * Computes weight based on three factors:
 *
 * - items sent
 * - items received
 * - last timestamp
 */
```


## JSDoc tags (G:jsdoc-tags)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#jsdoc-tags), CC BY 3.0.

Google style allows a subset of JSDoc tags. Most tags must occupy their own line, with the tag at the beginning of the line.

✅ Good:

```ts
/**
 * The "param" tag must occupy its own line and may not be combined.
 * @param left A description of the left param.
 * @param right A description of the right param.
 */
function add(left: number, right: number) { ... }
```

❌ Bad:

```ts
/**
 * The "param" tag must occupy its own line and may not be combined.
 * @param left @param right
 */
function add(left: number, right: number) { ... }
```


## Line wrapping (G:jsdoc-line-wrapping)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#jsdoc-line-wrapping), CC BY 3.0.

Line-wrapped block tags are indented four spaces. Wrapped description text _may_ be lined up with the description on previous lines, but this horizontal alignment is discouraged.

✅ Good:

```ts
/**
 * Illustrates line wrapping for long param/return descriptions.
 * @param foo This is a param with a particularly long description that just
 *     doesn't fit on one line.
 * @return This returns something that has a lengthy description too long to fit
 *     in one line.
 */
exports.method = function(foo) {
  return 5;
};
```

Do not indent when wrapping a `@desc` or `@fileoverview` description.


## JSDoc type annotations (G:jsdoc-type-annotations)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#jsdoc-type-annotations), CC BY 3.0.

JSDoc type annotations are redundant in TypeScript source code. Do not declare types in `@param` or `@return` blocks, do not write `@implements`, `@enum`, `@private`, `@override` etc. on code that uses the `implements`, `enum`, `private`, `override` etc. keywords.
