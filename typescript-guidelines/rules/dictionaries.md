# dictionaries

Prefer `Map` and `Set` to objects used as dictionaries; when an index signature is needed, name its key meaningfully (`{[userName: string]: number}`).

**Why:** Objects as maps have surprising prototype behavior.

**Sources:** G:indexable-key-string-type

---

## Indexable types / index signatures (`{[key: string]: T}`) (G:indexable-key-string-type)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#indexable-key-string-type), CC BY 3.0.

In JavaScript, it's common to use an object as an associative array (aka map, hash, or dict). Such objects can be typed using an [index signature](https://www.typescriptlang.org/docs/handbook/2/objects.html#index-signatures) (`[k: string]: T`) in TypeScript:

```ts
const fileSizes: {[fileName: string]: number} = {};
fileSizes['readme.txt'] = 541;
```

In TypeScript, provide a meaningful label for the key. (The label only exists for documentation; it's unused otherwise.)

❌ Bad:

```ts
const users: {[key: string]: number} = ...;
```

✅ Good:

```ts
const users: {[userName: string]: number} = ...;
```

> Rather than using one of these, consider using the ES6 `Map` and `Set` types instead. JavaScript objects have [surprising undesirable behaviors](http://2ality.com/2012/01/objects-as-maps.html) and the ES6 types more explicitly convey your intent. Also, `Map`s can be keyed by—and `Set`s can contain—types other than `string`.

TypeScript's builtin `Record<Keys, ValueType>` type allows constructing types with a defined set of keys. This is distinct from associative arrays in that the keys are statically known. See advice on that below.
