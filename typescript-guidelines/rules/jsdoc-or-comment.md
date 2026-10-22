# jsdoc-or-comment

Use `/** JSDoc */` for what users of the code should read and `//` comments for implementation notes; write multi-line comments as consecutive `//` lines, not `/* */` blocks.

**Why:** Tools read JSDoc; humans read both.

**Sources:** G:comments-documentation

---

## Comments and documentation (G:comments-documentation)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#comments-documentation), CC BY 3.0.

### JSDoc versus comments

There are two types of comments, JSDoc (`/** ... */`) and non-JSDoc ordinary comments (`// ...` or `/* ... */`).

*   Use `/** JSDoc */` comments for documentation, i.e. comments a user of the code should read.

*   Use `// line comments` for implementation comments, i.e. comments that only concern the implementation of the code itself.

JSDoc comments are understood by tools (such as editors and documentation generators), while ordinary comments are only for other humans.

### Multi-line comments

Multi-line comments are indented at the same level as the surrounding code. They _must_ use multiple single-line comments (`//`-style), not block comment style (`/* */`).

✅ Good:

```ts
// This is
// fine
```

❌ Bad:

```ts
/*
 * This should
 * use multiple
 * single-line comments
 */

/* This should use // */
```

Comments are not enclosed in boxes drawn with asterisks or other characters.
