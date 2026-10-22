# named-exports

Use named exports only, never `export default`; export only what other modules use; never `export let` (expose mutable state through a getter function); don't build container classes of statics for namespacing, export the constants and functions themselves.

**Why:** Every import names the same thing the same way.

**Sources:** G:exports

---

## Exports (G:exports)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#exports), CC BY 3.0.

Use named exports in all code:

✅ Good:

```ts
// Use named exports:
export class Foo { ... }
```

Do not use default exports. This ensures that all imports follow a uniform pattern.

❌ Bad:

```ts
// Do not use default exports:
export default class Foo { ... } // BAD!
```

**Why?**

Default exports provide no canonical name, which makes central maintenance difficult with relatively little benefit to code owners, including potentially decreased readability:

❌ Bad:

```ts
import Foo from './bar';  // Legal.
import Bar from './bar';  // Also legal.
```

Named exports have the benefit of erroring when import statements try to import something that hasn't been declared. In `foo.ts`:

❌ Bad:

```ts
const foo = 'blah';
export default foo;
```

And in `bar.ts`:

❌ Bad:

```ts
import {fizz} from './foo';
```

Results in `error TS2614: Module '"./foo"' has no exported member 'fizz'.` While `bar.ts`:

❌ Bad:

```ts
import fizz from './foo';
```

Results in `fizz === foo`, which is probably unexpected and difficult to debug.

Additionally, default exports encourage people to put everything into one big object to namespace it all together:

❌ Bad:

```ts
export default class Foo {
  static SOME_CONSTANT = ...
  static someHelpfulFunction() { ... }
  ...
}
```

With the above pattern, we have file scope, which can be used as a namespace. We also have a perhaps needless second scope (the class `Foo`) that can be ambiguously used as both a type and a value in other files.

Instead, prefer use of file scope for namespacing, as well as named exports:

✅ Good:

```ts
export const SOME_CONSTANT = ...
export function someHelpfulFunction()
export class Foo {
  // only class stuff here
}
```

### Export visibility

TypeScript does not support restricting the visibility for exported symbols. Only export symbols that are used outside of the module. Generally minimize the exported API surface of modules.

### Mutable exports

Regardless of technical support, mutable exports can create hard to understand and debug code, in particular with re-exports across multiple modules. One way to paraphrase this style point is that `export let` is not allowed.

❌ Bad:

```ts
export let foo = 3;
// In pure ES6, foo is mutable and importers will observe the value change after a second.
// In TS, if foo is re-exported by a second file, importers will not see the value change.
window.setTimeout(() => {
  foo = 4;
}, 1000 /* ms */);
```

If one needs to support externally accessible and mutable bindings, they _should_ instead use explicit getter functions.

✅ Good:

```ts
let foo = 3;
window.setTimeout(() => {
  foo = 4;
}, 1000 /* ms */);
// Use an explicit getter to access the mutable export.
export function getFoo() { return foo; };
```

For the common pattern of conditionally exporting either of two values, first do the conditional check, then the export. Make sure that all exports are final after the module's body has executed.

✅ Good:

```ts
function pickApi() {
  if (useOtherApi()) return OtherApi;
  return RegularApi;
}
export const SomeApi = pickApi();
```

### Container classes

Do not create container classes with static methods or properties for the sake of namespacing.

❌ Bad:

```ts
export class Container {
  static FOO = 1;
  static bar() { return 1; }
}
```

Instead, export individual constants and functions:

✅ Good:

```ts
export const FOO = 1;
export function bar() { return 1; }
```
