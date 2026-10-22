# file-structure

Order a file as: copyright JSDoc (if any), `@fileoverview` JSDoc (if any), imports, then the implementation, with one blank line between sections.

**Why:** Every file reads the same way.

**Sources:** G:source-file-structure, G:file-copyright, G:fileoverview

---

## Source file structure (G:source-file-structure)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#source-file-structure), CC BY 3.0.

Files consist of the following, **in order**:

1. Copyright information, if present

2. JSDoc with `@fileoverview`, if present

3. Imports, if present

4. The file’s implementation

**Exactly one blank line** separates each section that is present.


## Copyright information (G:file-copyright)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#file-copyright), CC BY 3.0.

If license or copyright information is necessary in a file, add it in a JSDoc at the top of the file.


## `@fileoverview` JSDoc (G:fileoverview)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#fileoverview), CC BY 3.0.

A file may have a top-level `@fileoverview` JSDoc. If present, it may provide a description of the file's content, its uses, or information about its dependencies. Wrapped lines are not indented.

Example:

✅ Good:

```ts
/**
 * @fileoverview Description of file. Lorem ipsum dolor sit amet, consectetur
 * adipiscing elit, sed do eiusmod tempor incididunt.
 */
```
