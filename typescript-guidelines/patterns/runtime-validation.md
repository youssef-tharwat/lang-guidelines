# runtime-validation

Validate untrusted data (network, files, JSON) at runtime to narrow `unknown` into a type, because compiled TypeScript keeps no types.

**Sources:** P:systemic-3-runtime-type-validation, P:complication-5-type-def-stripped, P:complication-8-non-bijective-json

---

## Systemic 3 Runtime Type Validation (P:systemic-3-runtime-type-validation)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/systemic-3-runtime-type-validation), copyright the author, redistributed with attribution.

Runtime Type Validation is the process of narrowing an object type from `unknown` into a specific type by examining the object's structure, as opposed to [type assertion](https://www.typescriptlang.org/docs/handbook/basic-types.html#type-assertions). It is not a built-in behavior, but for systems, it is essential because the result of its absence, [TypeError](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypeError) can start an [undefined behavior](https://en.wikipedia.org/wiki/Undefined_behavior).

```
// an example pattern
const maybePerson = await receivePerson();
const decoded = Person.decode(maybePerson);
if (!E.isLeft(decoded)) return;
const person = decoded.right;
```

Runtime Type Validation is typically needed on an unknown type that the system wants to operate on (e.g. accessing a property, passing it as an argument, etc). It must go hand in hand with [The Throwless Pact](https://valand.dev/systemic-ts/systemic-1-known-vs-unknown-error-throwless) in the sense that, by default, invalid data detection must not throw.

It is not necessary on type-deleted objects (asserted back into unknown) but is still stored in memory. Unless absolutely necessary, in-memory type-deleted objects are not recommended, instead a polymorphic wrapper (e.g. tagged union) is a better approach.

### Implementation

Again, we will see runtime type validation in action using my preferred tool, [io-ts](https://github.com/gcanti/io-ts) and [fp-ts](https://github.com/gcanti/fp-ts), but it should not prevent you from using other tools (e.g. [zod](https://github.com/colinhacks/zod)).

See the code below.

```
const user = JSON.parse(await fetchFromUserAPI()) as User;
// May throw `TypeError` because `user` or `user.aliases` could be `undefined`
console.log(user.aliases[0]);
```

Data that comes from the boundary (e.g. via network, storage) are unknown. However you trust the other party to send the right data, blindly asserting type is fundamentally unsafe. Your program breaks when they screw up. This is the sentiment that began the popularity of runtime validation.

Below is an implementation example of a function that calls an API and validates its returned values.

```
import * as E from "fp-ts/Either";
import * as t from "io-ts";

// define user, follow the library's docs
// https://github.com/gcanti/io-ts
const User = t.type({
  id: t.string,
  aliases: t.array(t.string),
});
type User = t.TypeOf<typeof User>;

const fetchUser = async () => {
  const maybeUserString = await fetchFromUserAPI(); // returns Either<Error, string>
  if (E.isLeft(maybeUserString)) return maybeUserString; // validate if not error from network
  const userString = maybeUserString.right;

  const maybeJSON = E.tryCatch(
    () => JSON.parse(maybeUserString),
    (e) => e
  );
  if (E.isLeft(maybeJSON)) return maybeJSON;
  const json = maybeJSON.right;

  const maybeUser = User.decode(json);
  if (E.isLeft(maybeUser)) return maybeUser;
  const user = maybeUser.right;

  return user;
};
```

The above `fetchUser` is safe and throwless so it can be called this way.

```
const maybeUser = await fetchUser();
if (E.isRight(maybeUser)) {
  const user = maybeUser.right;
  // `user` is guaranteed to be of type User in this block
}
```

### Tips: Validating Huge Array

Users usually perceive a freeze as "stop running" while it simply runs without updating the user interface.

Unfortunately, innocent validation such as below can freeze the application if the size of the array is big.

```
const maybeSomeBigArray = t.array(User).decode(json);
```

The UX trick is to split the validation steps. First, validate the outer array structure. Second, validate the array member and let the consumer control the validation steps.

The outer array structure validation is of the same procedure.

```
const maybeSomeBigArray = t.array(t.unknown).decode(json);
if (E.isLeft(maybeSomeBigArray)) return maybeSomeBigArray;
```

The inner validation is a bit tricky because we need to let the caller control its flow. We can leverage a closure to make it something iterator-like.

```
const fetchAndBatchValidateUsers = () => {
  const maybeSomeBigArray = t.array(t.unknown).decode(json);
  if (E.isLeft(maybeSomeBigArray)) return maybeSomeBigArray;

  return (() => {
    const unknownArray = maybeSomeBigArray.right;
    const initialLength = unknownArray.length;
    const errors = [] as DecodeError[];
    const values = [] as User[];

    // internal methods
    // ======

    const validateNext = () => {
      const item = unknownArray.shift();
      if (!item) return;
      const res = User.decode(item);
      if (E.isRight(res)) {
        values.push(res.right);
      } else {
        errors.push(res.left);
      }
    };

    // methods
    // ======

    // {done: true} when all members are validated, otherwise {done: false}
    const next = () => {
      validateNext();
      return { done: unknownArray.length === 0 };
    };

    // returns a number ranging from 0-1
    const progress = () =>
      initialLength === 0
        ? 1 /* avoid division by 0 error */
        : (errors.length + values.length) / initialLength;

    // Returns done validations as values and errors
    const result = () => ({ values, errors });

    return { next, result, progresss };
  })();
};
```

The closure exposes `next`, which validates one item and reports whether it has finished the entire array or not.

Then, the caller can use it this way:

```
const res = await fetchAndBatchValidateUsers();
if (E.isLeft(res)) return res;
// The closure part starts here
const batched = res.right;
while (!batched.next().done) {
  await updateProgressToUI(batched.progress());
  await sleep(0); // ensure non-blocking behavior
}
await updateProgressToUI(batched.progress());
return batched.result();
```


## Complication 5 Type Def Stripped (P:complication-5-type-def-stripped)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/complication-5-type-def-stripped), copyright the author, redistributed with attribution.

This article is a part of the[systemic-ts](https://valand.dev/systemic-ts) series.

Previous:

complication

Next:

complication

_Thankfully, now there are many solutions out there to validate type at runtime. Almost too many. But these validators are optional, so the problem remains for those who don't use them._

TypeScript code, when compiled with a pure TypeScript compiler, has all the type definitions stripped. Code that assumes `unknown` or `any` with `as` may fail.

```
type Circle = { diameter: number };
const circle = (await receiveCircle()) as Circle; // `unknown` asserted as 'Circle'

const diameter = Math.PI * circle.diameter; // possibly NaN
```

This problem often arises on the JavaScript runtime's system's boundary e.g. network call, file access, inter-process communication.

Anyway, when people start to realize, it is duct-taped with manual runtime type checking

```
if ("diameter" in circle && typeof circle.diameter === "number") {
  // valid
} else {
  // invalid
}
```

Soon after, genius folks created validators like [`zod`](https://github.com/colinhacks/zod) and [`io-ts`](https://github.com/gcanti/io-ts). With that, defining the type and validator becomes a one-step process.

```
const Circle = t.type({
  diameter: t.number,
});
const maybeCircle = await receiveCircle();
if (!Circle.is(maybeCircle)) {
  throw new Error("not circle");
}
const circle = maybeCircle;
```

The lack of a native validator isn't as depressing as other sources of complications. But the fact that TypeScript is in a way [weak-typed](https://en.wikipedia.org/wiki/Strong_and_weak_typing) forces us to treat these third-party validators as essentials.


## Complication 8 Non Bijective Json (P:complication-8-non-bijective-json)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/complication-8-non-bijective-json), copyright the author, redistributed with attribution.

This article is a part of the[systemic-ts](https://valand.dev/systemic-ts) series.

Previous:

complication

Next:

complication

`JSON` data type is limited and `JSON.stringify` has an incredibly inconsistent quirk. `undefined`, `Function`, and `Symbol` are omitted. `NaN` and `Infinity` become `null`. `Map`, `Set`, `WeakMap`, `WeakSet`, and `WeakRef` becomes `{}`. `BigInt` throws.

Not only does this quirk limit the utility of `JSON` but it also necessitates the application to manually select which type can be converted to JSON and which does not, which business object can naturally be persisted as `JSON` and which requires intermediate transformation; this manual selection is done absolutely manually and no built-in language feature can assist with it.

`JSON`-able values can be constrained with the following type:

```
export type JSONValue = string | number | boolean | null | JSONObject | JSONArray;
export type JSONArray = JSONValue[];
export type JSONObject = {
    [key: string]: SerializableValue;
} & {
    [key: symbol]: never;
};
```

Deciding to convert a previously non-`JSON`-able into a `JSON`-able one means it will never be able to not require a transformation function. However, it is a fair constraint since some data types can never be stringified anyhow (e.g. `Function`).

It only makes sense that the solution for this quirk lies in the design pattern, not the compilation phase.
