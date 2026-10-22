# null-and-optional

Use `undefined` or `null` to match the surrounding APIs; never put `|null` or `|undefined` inside a type alias, add it where the alias is used; prefer optional fields and parameters (`?`) to `|undefined`, and initialize class fields.

**Why:** Absence is handled close to where it arises.

**Sources:** G:undefined-and-null

---

## Undefined and null (G:undefined-and-null)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#undefined-and-null), CC BY 3.0.

TypeScript supports `undefined` and `null` types. Nullable types can be constructed as a union type (`string|null`); similarly with `undefined`. There is no special syntax for unions of `undefined` and `null`.

TypeScript code can use either `undefined` or `null` to denote absence of a value, there is no general guidance to prefer one over the other. Many JavaScript APIs use `undefined` (e.g. `Map.get`), while many DOM and Google APIs use `null` (e.g. `Element.getAttribute`), so the appropriate absent value depends on the context.

### Nullable/undefined type aliases

Type aliases _must not_ include `|null` or `|undefined` in a union type. Nullable aliases typically indicate that null values are being passed around through too many layers of an application, and this clouds the source of the original issue that resulted in `null`. They also make it unclear when specific values on a class or interface might be absent.

Instead, code _must_ only add `|null` or `|undefined` when the alias is actually used. Code _should_ deal with null values close to where they arise, using the above techniques.

❌ Bad:

```ts
// Bad
type CoffeeResponse = Latte|Americano|undefined;

class CoffeeService {
  getLatte(): CoffeeResponse { ... };
}
```

✅ Good:

```ts
// Better
type CoffeeResponse = Latte|Americano;

class CoffeeService {
  getLatte(): CoffeeResponse|undefined { ... };
}
```

### Prefer optional over `|undefined`

In addition, TypeScript supports a special construct for optional parameters and fields, using `?`:

✅ Good:

```ts
interface CoffeeOrder {
  sugarCubes: number;
  milk?: Whole|LowFat|HalfHalf;
}

function pourCoffee(volume?: Milliliter) { ... }
```

Optional parameters implicitly include `|undefined` in their type. However, they are different in that they can be left out when constructing a value or calling a method. For example, `{sugarCubes: 1}` is a valid `CoffeeOrder` because `milk` is optional.

Use optional fields (on interfaces or classes) and parameters rather than a `|undefined` type.

For classes preferably avoid this pattern altogether and initialize as many fields as possible.

✅ Good:

```ts
class MyClass {
  field = '';
}
```
