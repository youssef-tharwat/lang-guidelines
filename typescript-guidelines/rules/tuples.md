# tuples

Return a tuple (`[string, string]`) instead of a `Pair` interface, but prefer an inline object type with named fields when names add meaning.

**Why:** Names beat positions when the meaning isn't obvious.

**Sources:** G:tuple-types

---

## Tuple types (G:tuple-types)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#tuple-types), CC BY 3.0.

If you are tempted to create a Pair type, instead use a tuple type:

❌ Bad:

```ts
interface Pair {
  first: string;
  second: string;
}
function splitInHalf(input: string): Pair {
  ...
  return {first: x, second: y};
}
```

✅ Good:

```ts
function splitInHalf(input: string): [string, string] {
  ...
  return [x, y];
}

// Use it like:
const [leftHalf, rightHalf] = splitInHalf('my string');
```

However, often it's clearer to provide meaningful names for the properties.

If declaring an `interface` is too heavyweight, you can use an inline object literal type:

✅ Good:

```ts
function splitHostPort(address: string): {host: string, port: number} {
  ...
}

// Use it like:
const address = splitHostPort(userAddress);
use(address.port);

// You can also get tuple-like behavior using destructuring:
const {host, port} = splitHostPort(userAddress);
```
