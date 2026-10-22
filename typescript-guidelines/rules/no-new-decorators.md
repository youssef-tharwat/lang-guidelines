# no-new-decorators

Don't define new decorators; use only framework-provided ones, placed directly before what they decorate.

**Why:** TypeScript decorators diverged from the standard.

**Sources:** G:decorators

---

## Decorators (G:decorators)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#decorators), CC BY 3.0.

Decorators are syntax with an `@` prefix, like `@MyDecorator`.

Do not define new decorators. Only use the decorators defined by frameworks:

*   Angular (e.g. `@Component`, `@NgModule`, etc.)

*   Polymer (e.g. `@property`)

**Why?**

We generally want to avoid decorators, because they were an experimental feature that have since diverged from the TC39 proposal and have known bugs that won't be fixed.

When using decorators, the decorator _must_ immediately precede the symbol it decorates, with no empty lines between:

```ts
/** JSDoc comments go before decorators */
@Component({...})  // Note: no empty line after the decorator.
class MyComp {
  @Input() myField: string;  // Decorators on fields may be on the same line...

  @Input()
  myOtherField: string;  // ... or wrap.
}
```
