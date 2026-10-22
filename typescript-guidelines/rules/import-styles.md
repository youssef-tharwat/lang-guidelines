# import-styles

Use named imports for frequently used, clearly named symbols and namespace imports (`import * as ns`) for many symbols from a large API; import project files by relative path (`./foo`) with few `../` steps; rename an import only to resolve a collision or an unclear name.

**Why:** Imports stay readable and survive moving the project.

**Sources:** G:imports

---

## Imports (G:imports)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#imports), CC BY 3.0.

There are four variants of import statements in ES6 and TypeScript:

| Import type | Example | Use for |
| --- | --- | --- |
| module[module_import] | `import * as foo from '...';` | TypeScript imports |
| named[destructuring_import] | `import {SomeThing} from '...';` | TypeScript imports |
| default | `import SomeThing from '...';` | Only for other external code that requires them |
| side-effect | `import '...';` | Only to import libraries for their side-effects on load (such as custom elements) |

✅ Good:

```ts
// Good: choose between two options as appropriate (see below).
import * as ng from '@angular/core';
import {Foo} from './foo';

// Only when needed: default imports.
import Button from 'Button';

// Sometimes needed to import libraries for their side effects:
import 'jasmine';
import '@polymer/paper-button';
```

### Import paths

TypeScript code _must_ use paths to import other TypeScript code. Paths _may_ be relative, i.e. starting with `.` or `..`, or rooted at the base directory, e.g. `root/path/to/file`.

Code _should_ use relative imports (`./foo`) rather than absolute imports `path/to/foo` when referring to files within the same (logical) project as this allows to move the project around without introducing changes in these imports.

Consider limiting the number of parent steps (`../../../`) as those can make module and path structures hard to understand.

✅ Good:

```ts
import {Symbol1} from 'path/from/root';
import {Symbol2} from '../parent/file';
import {Symbol3} from './sibling';
```

### Namespace versus named imports

Both namespace and named imports can be used.

Prefer named imports for symbols used frequently in a file or for symbols that have clear names, for example Jasmine's `describe` and `it`. Named imports can be aliased to clearer names as needed with `as`.

Prefer namespace imports when using many different symbols from large APIs. A namespace import, despite using the `*` character, is not comparable to a wildcard import as seen in other languages. Instead, namespace imports give a name to all the exports of a module, and each exported symbol from the module becomes a property on the module name. Namespace imports can aid readability for exported symbols that have common names like `Model` or `Controller` without the need to declare aliases.

❌ Bad:

```ts
// Bad: overlong import statement of needlessly namespaced names.
import {Item as TableviewItem, Header as TableviewHeader, Row as TableviewRow,
  Model as TableviewModel, Renderer as TableviewRenderer} from './tableview';

let item: TableviewItem|undefined;
```

✅ Good:

```ts
// Better: use the module for namespacing.
import * as tableview from './tableview';

let item: tableview.Item|undefined;
```

❌ Bad:

```ts
import * as testing from './testing';

// Bad: The module name does not improve readability.
testing.describe('foo', () => {
  testing.it('bar', () => {
    testing.expect(null).toBeNull();
    testing.expect(undefined).toBeUndefined();
  });
});
```

✅ Good:

```ts
// Better: give local names for these common functions.
import {describe, it, expect} from './testing';

describe('foo', () => {
  it('bar', () => {
    expect(null).toBeNull();
    expect(undefined).toBeUndefined();
  });
});
```

#### Special case: Apps JSPB protos

Apps JSPB protos must use named imports, even when it leads to long import lines.

This rule exists to aid in build performance and dead code elimination since often `.proto` files contain many `message`s that are not all needed together. By leveraging destructured imports the build system can create finer grained dependencies on Apps JSPB messages while preserving the ergonomics of path based imports.

✅ Good:

```ts
// Good: import the exact set of symbols you need from the proto file.
import {Foo, Bar} from './foo.proto';

function copyFooBar(foo: Foo, bar: Bar) {...}
```

### Renaming imports

Code _should_ fix name collisions by using a namespace import or renaming the exports themselves. Code _may_ rename imports (`import {SomeThing as SomeOtherThing}`) if needed.

Three examples where renaming can be helpful:

1. If it's necessary to avoid collisions with other imported symbols.

2. If the imported symbol name is generated.

3. If importing symbols whose names are unclear by themselves, renaming can improve code clarity. For example, when using RxJS the `from` function might be more readable when renamed to `observableFrom`.
