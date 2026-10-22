# string-scale

Treat large or frequently copied strings as a performance concern; prefer references and structured data.

**Sources:** P:complication-9-string-scales-easily

---

## Complication 9 String Scales Easily (P:complication-9-string-scales-easily)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/complication-9-string-scales-easily), copyright the author, redistributed with attribution.

Assignments and function calls involving [primitives](https://developer.mozilla.org/en-US/docs/Glossary/Primitive) are pass-by-copy. This means, that each time you assign a variable or call a function, your primitive value is copied.

```
// roughly 39 bytes
const s: string = "veryloooooooooooooooooooooooooongstring";
// s is copied 3 times here
NOOPString(s);
NOOPString(s);
NOOPString(s);
// copied 3 times more
const s1 = s;
const s2 = s;
const s3 = s;
// here, 273 bytes are used
```

In contrast, non-primitives (e.g. array and objects) are pass-by-reference.

```
// let this be x bytes
const o = {};
NOOP(o);
NOOP(o);
NOOP(o);
const o1 = o;
const o2 = o;
const o3 = o;
// here, x bytes + (6 * size_of_reference_in_bytes) are used
```

`string` is special because, unlike the others (except `BigInt`), it can scale almost indefinitely depending on the JavaScript implementation. [This page](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/length) shows that in V8/Node, Firefox, and Safari, a string can scale to 1GB.

The engines should have implemented [interning](https://en.wikipedia.org/wiki/String_interning). This means one large string copied many times in JS takes significantly less memory than when it is done in languages without interning. But interning can be broken by just adding a string with a random letter to one of the strings.

In the worst case, memory usage can jump from 1GB to 2GB through 1 assignment Nevermind the worst case, this single command below takes around 60MB.

```
const a = new Array(1000000)
  .fill("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
  .map((x, i) => x + i);
```

### More careful approach should be taken around string

The string scaling problem is detrimental on large scale (e.g. large data processing), therefore two precautions should be taken: 1.) **create unique strings sparingly**, and 2.) **not all entities should be represented as a string**.

This precaution takes many forms. One seemingly innocent operation is copying an object by stringifying and parsing it again.

The second precaution can also be taken into a more advanced version of it. Not all entities are fit to be represented as primitives at all if it does not require the traits of primitives such as non-shareability and direct comparability.

### Systemic patterns (prefer these)
