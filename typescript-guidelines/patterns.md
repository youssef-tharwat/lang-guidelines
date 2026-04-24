# TypeScript Patterns

> Distilled from two canonical sources.
>
> - **Systemic TypeScript** by Vincent Alandev — <https://valand.dev/systemic-ts>
>   Architectural design decisions for TypeScript at scale: what to avoid, what
>   to prefer, how to reason about complications and systemic patterns.
> - **Design Patterns in TypeScript** by refactoring.guru —
>   <https://refactoring.guru/design-patterns/typescript>
>   The 22 Gang-of-Four patterns adapted to TypeScript, each with intent,
>   complexity/popularity, usage examples, and a conceptual TS implementation.
>
> Further reading (not inlined):
> - <https://sbcode.net/typescript/> — "Design Patterns in TypeScript" textbook with video lectures.
> - <https://github.com/torokmark/design_patterns_in_typescript> — code-only GoF implementations.

Every section below is a reusable design decision. Read sequentially:

1. **Systemic TypeScript** — start here. Establishes the TypeScript-native
   architectural baseline (no throw, closure over class, runtime validation,
   agency model). Load before choosing among any GoF pattern.
2. **GoF patterns adapted to TypeScript** — creational → structural →
   behavioral. Each pattern states its intent, usage examples, identification
   cues, complexity, and popularity in real TypeScript codebases.

---

## Part 1 — Systemic TypeScript

*by Vincent Alandev · valand.dev/systemic-ts*

The preludes establish the mental model: TypeScript as a *system*, not a *script*.
The **complications** are TypeScript features that hurt at scale — treat each as
an anti-pattern to avoid. The **systemic** patterns are positive replacements.

### Preludes

<!-- source: https://valand.dev/systemic-ts/prelude-1-system-vs-script -->

This article is a part of the[systemic-ts](https://valand.dev/systemic-ts) series.

Next:

prelude

A system consists of interacting and/or interrelated components. Such components interact with certain preferences, forming a **BOUNDARY** separating the system and the environment.

A system is usually long-running, needs to be durable, must self-regulate, and often have subsystems, each having a sub-purpose of the parent's. Having a boundary, it bounds to have a mechanism to interact with the environment--the interface.

Having many components, maintenance is harder, thus requiring a different strategy.

Scriptic, on the other hand, is a quality of software, code, script, etc, that is not systemic.

I derived the definition from how script errors are commonly handled by reporting and retrying. In a script, it is rare that an error or a message in general is passed to some other piece of code to be interpreted.

But it is not rare to see a collection of scripts become systemic over time and then the programmers begin to consider using another tool, and then another language. This [complexity shift is often painful](https://valand.dev/systemic-ts/inherent-complexity); when unmanaged, many have resorted to total rewrites with new languages.

Moreover, determining whether a program will be a system at first is often difficult at first because the formation of the system's boundary is continuous, not instant.

Systemic TypeScript series aims to select a particular strategy of writing TypeScript program that scales with complexity, where design pattern does not have to change often as a scriptic program becomes systemic. Therefore, when applied, the distinction between systemic and scriptic becomes less important and thus reducing the negative effect of complexity shift.

<!-- source: https://valand.dev/systemic-ts/prelude-2-inherent-complexity -->

This article is a part of the[systemic-ts](https://valand.dev/systemic-ts) series.

Previous:

prelude

Next:

complication

## Complex vs Complicated vs Hard

People often dismiss something difficult as `complex`. That word is many programmers' black sheep; the opposite `simplicity` naturally became overrated, ambiguous, and misplaced.

Look into these topics:

*   Following a recipe written not straightforwardly.
*   Understanding how time dilation relates to the speed of light.

Both are hard, but the former can be improved while the latter cannot because the idea of relativity is inherent, fundamental.

I thus name the former **complication** (or unnecessary complexity) and the latter **complexity** (or inherent complexity).

## Complexity Shift

How would a librarian organize books? Is it by genre, author, color, size, name, publication date?

Categorizing is the most common form of organization. Organization, however, needs a dimension.

The multilemma of the strategy to organize books comes from the lack of dimension. More concretely, a book has many properties---genre, author, color, etc. However, since the librarian needs to organize books within the space which only has three dimensions, the librarian needs to choose one property out of many.

The number of properties maps to complexity, while the discrepancy between the number of properties and the limited number of dimensions is the source of complication. In other words, complication can be perceived as two properties conflicting because they reside in the same dimension. In systems, it can manifest as two components clashing with each other.

To fit more properties within a limited dimension, some strategies can be applied. One simple example is the [index](https://en.wikipedia.org/wiki/Index_(publishing)) in books, which contains the important words and on which page to find them. In software development, a lot of strategies take a similar form to that of the index.

As features are added to a program, complexity grows. Proper organization must be conducted to suppress complications. It is a continuous process, hence there is the term [continuous refactoring](https://wiki.c2.com/?ContinuousRefactoring) in software development.

In other words, complication exists not because of complexity itself but because of **unorganized complexity shifts** and this is the exact phenomenon that arises when a program turns from [scriptic to systemic](https://valand.dev/systemic-ts/system-vs-script).

### Complications (avoid these)

<!-- source: https://valand.dev/systemic-ts/complication-1-throw -->

When you meet an unhappy path, simply `throw`.

```
if (connectionFailed) 
  throw new Error("cannot connect to server");
// do some business
if (httpStatusCode < 200 || httpStatusCode >= 300)
  throw new Error("result is bad");
// do some business
if (parseResult.failed()) 
  throw new Error("parse failed");
if (parseResult.value === "operation-needs-to-be-cancelled")
  throw new Error("operation-needs-to-be-cancelled")
// do some business
```

It is convenient! Your function stops and the problem now belongs to whoever is calling it.

_But will this function throw? Should I wrap this in a `try-catch`?_

```
unfamiliarFunction();

// or:

try {
  unfamiliarFunction();
} catch (e) {}
```

Unless YOU will call it yourself, then it is technically a debt because you put away the responsibility of error handling for the future you to handle.

From the caller's site, a `throw` is much harder to anticipate because the function signature does not have any marker indicating whether it will throw or not

### Catch is Untyped

```
try {
  someThrowingFunction();
} catch (error) { /* error is of type `unknown` */ }
```

TypeScript won't know the caught object's type. It can be anything. It can be an `undefined`, `Symbol`, `BigInt`, or random class instance.

Errors can be handled this way:

```
let attempt = 0;
while (attempt < 3) {
  attempt+=1;
  try { ... }
  catch (error) {
    if (error.message !== "cannot connect to servr") {
      await sleepForAwhile();
    }
    if (error.message !== "operation-needs-to-be-cancelled") {
      await rollback();
      break;
    }
    throw error
  }
}
```

Although, first we have a typo there `"cannot connect to servr"`. Due to how `try-catch` is designed, TypeScript does not assist with type analysis of the error, thus accidents such as a typo often happen.

_What if someone throws an 'undefined' somewhere?_

Second, the `catch` block must be impervious to accidental throws. Otherwise, you need another `try-catch` block to wrap it. If `error` is somehow `undefined` or `null` then accessing a property of `error` will throw a `TypeError`.

_A thrown entity is not your problem until it becomes one._

### Implementation Detail

The uncertainty of whether a function throws induces some anxieties:

*   will this function throw?
*   what error type will this function throw?
*   will my catch block throw?

```
try {
} catch (error) {
  try {
    /* handle error here */
  } catch (error) {
    /* just in any case... */
  }
}
```

You want to avoid writing the above ridiculous pattern. For that, you need an answer to the three questions above. You peek into the implementation details of the function you call inside the try-block.

The problem with HAVING TO KNOW the implementation detail is that it is a waste of time. A separate function is often written as an abstraction (of knowledge), but it is leaky and involves unintended consequences that it cannot be fully trusted.

The more complex a codebase is the more implementation details you have to scrutiny. You need something better if your code involves more diverse error-handling mechanisms.

_On a meta-level, I enjoy this paradox where the `try-catch-throw`, which is supposed to help in reducing "complexity" fails to do so at a certain level of complexity. It is nice to see someone screwed by this because then I see a comrade-in-arms._

### Acceptable Throws

_Update 2023-10-16_

A `throw` is fine when it does not mistify the programmer. The `throw`'s timing and reason, the `try`'s scope and the `catch`'s mechanism must be obvious.

The simplest form of an obvious `throw` is when it is declared.

```
/**
 * @throws OperationException
 */
export function anOperationThatMayThrow(){
}
```

Another form of obvious `throw` is when it is allowed in a certain way.

```
import { withRetry, Retry } from "./retry"

let attempt = 0;
const result = await withRetry(async () => {
  const res = await executeSomeOps();
  if (res.shouldRetry) throw Retry
  return res;
});

// Where the usage guide of of withRetry is explicitly written like so:
/**
 * @usage
 * await withRetry(async () => {
 *   if (await notIdeal()) throw Retry;
 *   // more long lines of code
 * });
 */
```

`throw` is very convenient to stop an operation early and to tell the compiler to not care about the return type of a certain branch. However, the challenge of documentation is always documentation rot because documentation isn't checked by the compiler and may require a custom linter to ensure its correctness.

<!-- source: https://valand.dev/systemic-ts/complication-2-class-prototype -->

This article is a part of the[systemic-ts](https://valand.dev/systemic-ts) series.

Previous:

complication

Next:

complication

Have you ever transferred objects across the JavaScript boundary? e.g.

*   Backend to frontend, and vice versa
*   Main thread to [worker thread](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API)
*   Electron's [main to renderer process](https://www.electronjs.org/docs/latest/tutorial/ipc)

If what you're transferring is a "class object", it will never work smoothly.

`class`, which uses `prototype` information under the hood is static. It comes with your program. Common sense says it must not be serialized and it is not serialized by default.

But in the permissive world of TypeScript and JavaScript, no one's stopping you from doing this:

```
const something = new SomeClass();
something.someMethod();
const serialized = JSON.stringify(something);
sendSomewhere(serialized);
```

You will hope that you can reverse it by deserializing it.

```
const serialized = receiveSomething();
const something = JSON.parse(serialized) as SomeClass; // expect this to be of SomeClass
something.someMethod(); // disappointed
```

But it turns out disappointing when you call `someMethod` and the method does not exist.

Those experienced enough know that this is bad practice, but it is common to expect serialization and deserialization should be reversible.

It may be partially caused by `JSON`'s non-reversible nature (and this series will later visit `JSON`'s non-reversible nature), but replace `JSON.stringify` and `JSON.parse` with any serialization/deserialization method and `prototype` and the result will just be the same.

### Insisting on Using Class

```
class SomeClass {
  static serialize(someClass: SomeClass) {
    return JSON.stringify(someClass);
  }

  static deserialize(str: string) {
    const obj = JSON.parse(str);
    const instance = new SomeClass();
    Object.entries(obj).forEach(([key, val]) => {
      instance[key] = val;
    });
    // Or more horribly, using
    // Object.setPrototypeOf()
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/setPrototypeOf
    return instance;
  }
}
```

With this somewhat "better" serialization/deserialization pair, you can expect this to work more often:

```
const something = new SomeClass();
something.someMethod();
const serialized = SomeClass.serialize(something);
const somethingCopy = SomeClass.deserialize(serialized) as SomeClass; // expect this to be of SomeClass
something.someMethod(); // disappointed
```

But to what extent?

_What if at the receiving end, they don't have the same deserialization method?_

_Must you write serialization and deserialization for every class you have? You have to write more as your codebase (i.e. the number of classes) grows._

Writing serialization and deserialization for every class just does not scale.

<!-- source: https://valand.dev/systemic-ts/complication-3-class-unbound-methods -->

The [method](https://developer.mozilla.org/en-US/docs/Glossary/Method) of [class](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes) has a particular issue for being unbound with its object.

Consider this class:

```
class Person {
  hobbies = ["cooking", "fishing", "gaming"];

  printHobbies() {
    this.hobbies.forEach(console.log);
  }
}
```

When `printHobbies` of a `Person` is called, all strings within hobbies will be printed. That much is clear.

```
new Person().printHobbies();
// "cooking"
// "fishing"
// "gaming"
```

However, when `printHobbies` is detached from the object and then is called, a curious problem arises.

```
const printHobbies = new Person().printHobbies; // detach
printHobbies(); // call
// Uncaught TypeError: Cannot read properties of undefined (reading 'hobbies')
// at printHobbies (<anonymous>:5:10)
// at <anonymous>:1:1
```

This simple problem wasted a lot of time, especially in projects that use a lot of callback parameters---which is the heart of JavaScript's reactive programming.

TypeScript does not fix this problem since its core principle is to provide a strict "superset"---writing a code in TypeScript must yield the same result as if it were written in JavaScript.

Several workarounds can be found on the internet.

```
class Person {
  hobbies = ["cooking", "fishing", "gaming"];
  printHobbies = () => {
    this.hobbies.forEach(console.log);
  };
}
// OR
class Person {
  constructor() {
    this.printHobbies = this.printHobbies.bind(this);
  }
  hobbies = ["cooking", "fishing", "gaming"];
  printHobbies() {
    this.hobbies.forEach(console.log);
  }
}
// OR when passing the method
const printHobbies = person.printHobbies.bind(person);
```

But those workarounds are tedious and beginners will make the same mistake because this is not how JS class are intended to be written per its specification.

Also, the fact that there are several workarounds will later create a _multilemma_ over which solution is the best; people will start to argue over this unimportant thing.

_The big question is: Why a partially broken feature is provided and used at all?_

<!-- source: https://valand.dev/systemic-ts/complication-4-class-layered-lifetime -->

This is the third time `class` has been problematic. But now `prototype` is not involved. The syntax itself is making it hard to do refactoring with it, especially when layered `lifetime` is involved.

_Did you just make up a new word?_

## Yes. Layered Lifetime, I Just Made Up That Phrase

[Lifetime](https://en.wikipedia.org/wiki/Object_lifetime) is literally when an object lives---the period between its creation and its deletion from the [memory](https://en.wikipedia.org/wiki/Computer_memory).

Specifically in TypeScript/JavaScript, an object's lifetime ends when nothing refers to it---when there are no references left; subsequently, non-referenced objects are removed by the [GC](https://en.wikipedia.org/wiki/Garbage_collection_(computer_science)), but the period between the reference count zeroing and the collection does not matter because nothing could be done with said objects.

"Layered lifetime" simply refers to a situation where there are objects whose lifetimes are diverse.

**A perfect example of "Layered lifetime"** would be a `Page` that has a [`Modal`](https://en.wikipedia.org/wiki/Modal_window) which is open only at times. This example will be written in [React](https://react.dev/).

```
const Page = () => {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <Layout>
      <Toggle onClick={setModalOpen((open) => !!open)} />
      {modalOpen && <Modal />}
    </Layout>
  );
};
```

The above code says:

*   "A `Page` contains a `Layout`, a `Toggle`, and optionally a `Modal`"
*   "`Toggle`, when clicked, flips `modalOpen` from `true` to `false`, and vice versa."
*   "`Modal` is open only when `modalOpen` is `true`."

Talking in terms of lifetimes:

*   `Modal` lives within the `Page`'s lifetime;
*   `Modal` lifetime is shorter than the `Page`'s;
*   `Modal` cannot exist without `Page`.
*   `Page` can exist without `Modal`.

The diversity of the lifetime is apparent here. There are two objects `Modal` and `Page`, and their lifetimes differ. Contrast this with the relationship of `Page` and `Layout` whose lifetime is the same.

## Lifetime and Type's Interesting Relationship

Above 6 PM I tend to write very dumb code such as:

```
class User {
  id?: string;
  name: string;
  address: string;
  constructor(
    name: string,
    address: string
  )                  { this.name = name; this.address = address }
  setId(id: string)  { this.id = id }
  isInvalid()        { return this.id === undefined; }
}

// On user input I want to create a "user"
function onUserInput(name: string, address: string) {
  return new User(name, address);
}

// The product manager wants to only reserve some Id
// from a centralized-badly-architectured-single-threaded-obviously-strawman-database
// ONLY WHEN the user click a confirmation to "confirm their seriousness in registering"
async function onUserConfirm(user: User) {
  user.setId(await reserveIdFromCentralizedDatabase())
  return user;
}

// When the user actually submits
async function submitUser(user: User) {
  // setId should be called before this
  if(user.isInvalid()) throw new Error()
  return await submitEntity("user", user);
}
```

The next morning, logic comes back to me. I realized that `User` without `id` does not make sense.

So I refactored the code into:

```
class UserData {
  public name: string;
  public address: string;
  constructor(name: string, address: string) {
    this.name = name;
    this.address = address;
  }
}

class User extends UserData {
  id: string;
  constructor(id: string, userData: UserData) {
    this.name = userData.name;
    this.address = userData.address;
  }
}

// On user input I want to create a "user"
function onUserInput(name: string, address: string) {
  return new UserData(name, address);
}

// The product manager wants to only reserve some Id
// from a centralized-badly-architectured-single-threaded-obviously-strawman-database
// ONLY WHEN the user click a confirmation to "confirm their seriousness in registering"
async function onUserConfirm(userData: UserData) {
  return new User(await reserveIdFromCentralizedDatabase(), userData);
}

// When the user actually submits
async function submitUser(user: User) {
  // IMPORTANT: Now there's no need to call `invalid`
  await submitEntity("user", user);
}
```

What I realize is that a `User`'s lifetime can't outlive its `id`. After the refactor, `id` is not optional. `submitUser` does not need to validate the always-valid `User`.

This way, the code represents entities' lifetimes' relationships more correctly.

## Too Many Lines Of Codes

"You claim it is simpler. Why are there more lines of code now?" - some review

Whelp! Such is the price of correctness.

"Why don't you just use `type`?" - some other review.

That's actually a great idea. Well, it was written in class, so I followed. In hindsight, a `class` without [methods](https://developer.mozilla.org/en-US/docs/Glossary/Method) is wasteful.

```
type UserData = { name: string; address: string };
type User = UserData & { id: string };

const onUserInput = (name: string, address: string): UserData => ({
  name,
  address,
});
const onUserConfirm = async (data: UserData): User => ({
  ...data,
  id: await reserveIdFromCentralizedDatabase(),
});
const submitUser = (user: User) => await submitEntity("user", user);
```

There you go!

Wait! Isn't this what "Functional Programming" looks like (or at least, advertised to look like)? It is one of the "evolutionary phases" of systemic-ts.

<!-- source: https://valand.dev/systemic-ts/complication-5-type-def-stripped -->

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

<!-- source: https://valand.dev/systemic-ts/complication-6-no-destructor -->

Some languages have [destructors](https://en.wikipedia.org/wiki/Destructor_(computer_programming)), but not JavaScript/TypeScript. Some argue that it is unnecessary for scripts.

If you must write a system that juggles around file and socket handles, chances are, you will forget to close some of them. So I argue that it has been necessary even since NodeJS.

```
// https://nodejs.org/api/fs.html#fscreatewritestreampath-options
const writeStream = fs.createWriteStream(somePath, {
  autoClose: false,
});
```

If you open enough of these kind of non-auto-closing streams and forget them, it will cause you "too many open file errors", for example. In a simple script, it is dismissable as a beginner's mistake. In a long-running system, resource leaks can cause contentions (i.e. different parts of the same system competing for a resource) and unnecessary context switches.

By not having a destructor, we cannot tell the runtime to close a file handle, socket handle, and any other side-effect-ish constructs whenever there is no more reference pointing to it.

### Relation to layered lifetime

_Related: [class vs layered lifetime](https://valand.dev/systemic-ts/class-layered-lifetime)_

Destructor not existing correlates with the lifetime management. The common fix to this problem is separating resource owners (e.g. who makes and destroys streams) from resource operators (who pump bytes into the streams).

```
const withStream = async (somePath: string, fns: ((stream: WritableStream) => Promise<unknown>)[]) => {
  // initialize resource
  const writeStream = fs.createWriteStream(somePath, {
    autoClose: false;
  });
  // do whatever you want with it
  await Promise.all(fns.map(() => fn(stream)))
  writeStream.close()
}
```

Separating users from ownership follows a similar pattern as GC.

```
// A total oversimplification!
const SystemWithGC = async () => {
  // initialize resource management system
  const resourceContext = createResourceContext();
  const instructionAndSoOn = createInstructionsQueue();
  while (true) {
    // operate on resource
    await instructionAndSoOn.run(resourceContext, {
      parkAfterInMilliseconds: 500,
    });
    // manage resource
    await resourceContext.markAndSweep();
  }
};
```

_"Can I Copy Your Homework? Yeah just change it up a bit so it doesn't look obvious you copied."_

If you squint your eyes, the pattern looks similar to [data-oriented design](https://en.wikipedia.org/wiki/Data-oriented_design), although it has a different purpose and details.

```
// Another total oversimplification!
const fn = async () => {
  const uniformData1 = [...]
  const uniformData2 = [...]
  const uniformData3 = [...]

  await instruction1(uniformData1)
  await instruction2(uniformData2)
  await instruction3(uniformData3)
}
```

#### Footnote:

_At the time of writing, there are a [proposal](https://github.com/tc39/proposal-explicit-resource-management) and a [solution](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global\_Objects/FinalizationRegistry). The latter is hard to use because of how the rest of the language has been designed. You can tell by the many red warnings that approximately say "Don't touch unless you're absolutely sure."_

<!-- source: https://valand.dev/systemic-ts/complication-7-cyclic-dependencies -->

In [NodeJS](https://nodejs.org/api/modules.html#modules_cycles) and [ES6](https://exploringjs.com/es6/ch_modules.html#sec_design-goals-es6-modules), cyclic modules are allowed.

```
// module-a.js
const b = require("./module-b.js");
console.log(b.a);
module.exports = { b };

// module-b.js
const a = require("./module-a.js");
console.log(a.b);
module.exports = { a };
```

In the code above, for example, executing one of the modules will throw a `ReferenceError`. The last `require` call in a cyclic chain of `requires` will return an unfinished copy. And by that time the last required module will not be defined yet.

The problem with cyclic modules is that it is detected at runtime, not compile time. Moreover, this subtle `throw` can be accidentally caught, causing the program to continue instead of stopping.

TypeScript does not prevent circular dependencies. Extra tools are needed to capture circular dependencies within a codebase. [This](https://github.com/aackerman/circular-dependency-plugin) is available for webpack users. Otherwise, [Madge](https://www.npmjs.com/package/madge) has a neat circular dependency detection.

### Illusion of cyclic-like

In a big codebase, there can be an unavoidable pattern that is seemingly cyclic but is not. Usually type definitions and functions of the same domain are collected into a single module. Because of that, two domain modules, let that be `A` and `B` may seem to depend on each other.

```
Module A -> Module B
Module B -> Module A
```

In reality, the pattern is that `Functions of A` depend on `Types of B`, and `Functions of B` depend on `Types of A`. Oftentimes, the functions from each module do not depend on each other.

In this case, types are better separated from the functions. Types and functions can be split by domains and then a combination of types can be made so that different functions can depend on the combined types.

In this case, it is wise to instead separate the types from the functions so that the functions can depend on the types and be separated.

```
Types All -> Types A
Types All -> Types B
Functions A -> Types All
Functions B -> Types All
```

This approach also prevents disagreement over whether an `import` should be just an [`import` or an `import type`](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-3-8.html).

In abstract, this approach means that programmers should **create a balance between the separation of modules by domain and by pattern**, instead of choosing one from the other.

<!-- source: https://valand.dev/systemic-ts/complication-8-non-bijective-json -->

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

<!-- source: https://valand.dev/systemic-ts/complication-9-string-scales-easily -->

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

<!-- source: https://valand.dev/systemic-ts/systemic-1-known-vs-unknown-error-throwless -->

This is only the solution's first sentence and yet I decree probably one of the most radical and controversial approaches in programming: **get rid of `throw`**.

"How can you communicate errors then?" you might say.

The answer: [`return`](https://en.wikipedia.org/wiki/Return_statement) and [`union`](https://en.wikipedia.org/wiki/Union_type)!

But before that, take a detour into the philosophical consideration of this approach.

## Known vs Unknown Errors

Unknown errors are, literally, unknown. Unknown's core essence involves you not knowing if it exists. If it exists at all, you have not identify what, how, when, or where it will happen.

Happening upon a previously unknown error is mystifying and often stressful. Understanding an error is dialectic, but it is only powerful if the knowledge is preserved so that someone in the future benefits from it.

Known errors are errors that you have encountered and those you have decided to not forget. An error becomes truly known when it is [signified](https://en.wikipedia.org/wiki/Sign_(semiotics)) (e.g. by being written as code).

It also makes no sense to blur a known error, particularly of when it happens. Therefore, `throwing` it is not a choice because it blurs the timing aspect of an error.

Managing knowledge of errors and communicating it are two entangled problems. Therefore, I present a solution that solves both: **The Throwless Pact**.

## The Throwless Pact

The pact's core tenets are:

*   Known errors within the codebase are well-[signified](https://en.wikipedia.org/wiki/Sign_(semiotics)) as a uniquely identified type.
*   Known errors and successes are communicated and signified as a [`returned`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/return) tagged [`union`](https://www.typescriptlang.org/docs/handbook/unions-and-intersections.html).
*   Thrown errors from outside the codebase (e.g. those thrown by third-party dependencies) are caught and converted into a `union` as early as possible.
*   Only unknown errors may be thrown, convert them once identified

What we want from this is, first, transparent and immediate information about a function's behavior in the form of [signature](https://www.typescriptlang.org/docs/handbook/2/functions.html#call-signatures). One that explies all result variants and implies all possibilities within.

With all possibilities implied, you will need less to look into the function's implementation detail. This very effectively combats [the try-catch anxiety when throws exist in a codebase](https://valand.dev/systemic-ts/complication-1-throw). As a result, the whole development process needs less cognitive burden so there is cognitive space for thinking at a higher-level.

Of course, the direct impact of not having `throw` is the robust and reliable appearance. In a React application, for example, `throw` triggers a crash. Even if caught with an [ErrorBoundary](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary) it does not beat the elegant facade of an application that does not throw.

Overall, you will be able to trust your code more.

## The Implementation

Now we will see how The Throwless Pact efficiently implements a growing requirement. We will compare the added values and also the extra price we have to pay (e.g. line of code, bootstrap code) for going against the grain. Usually, the bigger the codebase, the more the added values justify the extra price.

In this section, I will use my preferred tools/libraries. However, it should not prevent you from using other tools that achieve a similar purpose.

### Return Communication

For result variants to be `return`-ed and interpreted unambiguously, we need a tagged `union`. My favorite tool is [`fp-ts`](https://github.com/gcanti/fp-ts). The `Either` data structure can represent two mutually exclusive states `Left` and `Right`. As a convention, we will use `Left` for failures and `Right` for successes.

Let us dive into the example.

You must write a function that connects to a target, ping-pong (ping and then let the recipient ping back) the target using the connection ten times, and then return the connection to the call site.

```
import * as E from "fp-ts/Either";
import { pingPong, connect, Target } from "./some-connection-module";

type Errors = E.LeftOfRet<typeof connect> | E.LeftOfRet<typeof pingPong>;

// Returns either the accumulated error type of `connect` and `pingPong`
// or the success type which is `Connection`
type Result = E.Either<Errors, Connection>;

const connectAndWaitForTenPings = async (target: Target): Promise<Result> => {
  const connectRes = await connect(); // Return Either<ConnectionsError, Connections>
  if (E.isLeft(connectRes)) return connectRes; // connection failure, return
  const connection = connectRes.right;

  // ping pong 10 times
  let count = 0;
  while (count < 10) {
    const res = await pingPong(connection);
    if (E.isLeft(res)) return res; // pingPong failure, return
    count += 1;
  }

  return E.right(connection); // success, return
};

// type utilities, should be put in a common module

type LeftOf<T> = T extends E.Left<infer x> ? x : never;
type LeftOfRet<T extends Function> = LeftOf<ReturnType<T>>;
```

From the code:

*   `connectAndWaitForTenPings` is a function that receives `Target` and returns `Promise<Result>`
*   `Result` is `Either<Errors, Connection>`
*   `Errors` is `LeftOfRet<typeof connect> | LeftOfRet<typeof pingPong>`, or in other words, "errors of `connect`" and "errors of `pingPong`".

In natural language, `connectAndWaitForTenPings` is a function that receives a `Target` and returns `Either` a `Connection` if successful or the errors of either `connect` or `pingPong` if failing.

The type signature and the natural language shares a lot of similarity!

We can also be sure that there will be no unaccounted possibilities except unknown errors, which we know we can't predict in any way.

### Error Signification

If you don't need serialization, [`Error`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/Error). Otherwise, for inter-process errors, I prefer a custom error factory utilizing [`io-ts`](https://github.com/gcanti/io-ts).

The factory is simple and does only three things: 1.) make an error instance, 2.) expose `codec` and `sign` for pattern matching.

```
// file: s-error.ts
import * as t from "io-ts";

type SignedError<T extends string, P extends unknown> = {
  sign: T;
  data: P;
  stack: string | undefined;
};
type Factory<T extends string, P extends unknown> = {
  readonly sign: T;
  readonly codec: t.Type<SignedError<T, P>>;
  readonly make: (p: P) => SignedError<T, P>;
};

const Stack = t.union([t.string, t.undefined]);

export const design = <T extends string, P extends unknown>(
  sign: T,
  Payload: t.Type<P>,
): Factory<T, P> => {
  const codec = t.type({ sign: t.literal(sign), data: Payload, stack: Stack });

  const make = (data: P): SignedError<T, P> => {
    const error = new Error();
    error.name = sign;
    const stack = error.stack;
    return { sign, data, stack };
  };

  return { sign, codec, make };
};

export type TypeOf<F extends Factory<any, any>> = F extends Factory<
  infer T,
  infer P
>
  ? SignedError<T, P>
  : never;
```

With the factory, we can create many error "classes".

```
import { design, TypeOf } from "path/to/serror.ts";

const ConnectionError = design("ConnectionError", t.null);
type ConnectionError = TypeOf<typeof ConnectionError>;

const PingPongError = design("PingPongError", t.null);
type PingPongError = TypeOf<typeof PingPongError>;
```

With these errors "classes" you can now do several things:

First, obviously, you can create an error:

```
ConnectionError.make(null); // null maps to the type we inputted in the design phase
```

Second, on a union of errors, you can do pattern matching:

```
const error: ConnectionError | PingPongError = receiveSomeError();
if (error.sign === ConnectionError.sign) {
  // error type is narrowed into ConnectionError | PingPongError
}
```

Third, on an unknown data, the factory codec can be used to determine its structure.

```
const maybeError: unknown = receiveExternalError();
if (ConnectionError.codec.is(maybeError)) {
  // maybeError is narrowed into ConnectionError
}
```

Fourth, codec combinations can narrow variables into a wider type of errors.

```
const ConnectionOrPingPongError = t.union([
  ConnectionError,
  PingPongError
])

const maybeError: unknown = receiveExternalError();

if (ConnectionOrPingPongError.is(maybeError)) {
  // maybeError is narrowed into ConnectionError | PingPongError
}
```

TypeScript and `io-ts` do the heavy lifting of structure validation and narrowing for all these features. Additionally, IDEs and editors that supports TypeScript will provide useful type hints for variables inside these `if` blocks.

### Applying The Arsenal

Let us assume, in the first example, that `connectAndWaitForTenPings` forwards `ConnectionError` and `PingPongError` from `connect` and `pingPong` respectively.

Now, let there be a new requirement. We must write a function that connects and waits for ten pings. But if `connect` fails, the program must retry several times before failing.

For the retry mechanism, a `while` and an `attempt` counter suffice. To detect errors, we can use the explicitly returned error type. We know that one possibility from `connectAndWaitForTenPings` is `Left<ConnectionError>`. We can target that possibility specifically from outside the function.

```
const connectWithRetry = async (
  target: Target
): ReturnType<typeof connectAndWaitForTenPings> => {
  let attempt = 0;
  while (true) {
    const res = await connectAndWaitForTenPings(target);
    if (
      attempt < 3 &&
      E.isLeft(res) &&
      res.left.sign === ConnectionError.sign
    ) {
      attempt += 1;
      continue;
    }
    return res;
  }
};
```

You can almost hear what the code says: "Keep repeating, if `ConnectionError` and `attempt` is not 3, otherwise return whatever result you receive."

The narrative and [self-documenting](https://en.wikipedia.org/wiki/Self-documenting_code) feel of the snippet will justify the little noise---e.g. `res.left.sign`, `ConnectionError.sign`, `E.isLeft(res)`---that is caused by how `Either` and our error is structured.

### Exception

_Update 2023-10-16_

See the acceptable `throw` section in [this article](https://valand.dev/systemic-ts/complication-1-throw)

<!-- source: https://valand.dev/systemic-ts/systemic-2-closure-over-class -->

_[Objects are poor man's closures.](https://wiki.c2.com/?ClosuresAndObjectsAreEquivalent) (Or is it [closures that are poor man's objects](https://people.csail.mit.edu/gregs/ll1-discuss-archive-html/msg03277.html) because OOP folks tend to be paid higher salaries?)_

The above alludes that classes and closures, although originating from different schools (OOP and FP respectively), fulfill a similar purpose. However, the link above talked about classes and closures at the beginning of the formulation of OOP and FP.

Nowadays, closures and classes take more advanced forms---improved by more years of language design experience and feedback from the community. And it is pretty interesting that JavaScript and TypeScript have support for [closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures) and [class](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes).

I am biased toward closure, because, in my experience, class [does not scale as well with complexity](https://valand.dev/systemic-ts/prelude-2-inherent-complexity).

You may think that I came from the background of FP due to my bias, but that cannot be further from the truth. I was molded by OOP, class, methods, etc. My discovery of closures being easier to manage a significant complexity came from experience, necessity, and limitations of resources.

## Closure

Let there be a class of `Person` that encapsulate `hobbies` and expose a method `addHobby`.

```
/**
 * @usage
 * const person = new Person();
 * person.addHobby(hobby);
 */
class Person {
  private hobbies: = new Set<string>()
  addHobby (hobby: string) {
    this.hobbies.add(hobby);
  }
}
```

Written in closure, the above class becomes:

```
/**
 * @usage
 * const person = makePerson();
 * person.addHobby(hobby);
 */
const makePerson = () => {
  const hobbies = new Set<string>();
  const addHobby = (hobby: string) => { hobbies.add(hobby); };
  return { addHobby };
};
type Person = ReturnType<typeof makePerson>;
```

Syntax-wise both look the same.

Readability-wise, it will be subjective; OOP-accustomed people will say that class is better; FP-accustomed people will say that closure is better. It is like comparing whether English is more readable than Korean or is it the other way around, and then asking people whose native language is English and some other people whose native language is Korean.

Because of the subjectivity of readability, I will treat the readability aspect of class vs closure as of lower importance compared to other effects.

But, one clear benefit of closure over class here is that, unlike class, it does not suffer from the [unbound method problem](https://valand.dev/systemic-ts/complication-3-class-unbound-methods).

### Parameters

Now we are going to add parameters to the previous code. Look at how class and closure work with added parameters.

```
// CLASS
class Person {
  private hobbies: Set<string>;
  constructor(hobbies: Set<string>) {
    this.hobbies = new Set(hobbies);
  }
  addHobby (hobby: string) {
    this.hobbies.add(hobby);
  }
}
// CLOSURE
const makePerson = (initialHobbies: Set<string>) => {
  const hobbies = new Set(initialHobbies);
  const addHobby = (hobby: string) => { hobbies.add(hobby); };
  return { addHobby };
};
type Person = ReturnType<typeof makePerson>;
```

Bringing a parameter into the fold requires several lines for the [constructor](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/constructor); in a closure, modifications in two lines will suffice.

The only problem in the closure version is a name clash between `hobbies` and `initialHobbies`. Subjectively, the name clash in the bigger picture is not without merit since it forces more clarity toward which variable is for which purpose; compare that to `hobbies` vs `this.hobbies`.

### Async Construction

A caveat: async construction rarely prevails in a mature codebase because the async processes often fit better in another module; but for the sake of argument, let us pretend that we need an async construction.

```
// CLASS
class Person {
  private hobbies: Set<string>;
  static async create(hobbiesPromise: Promise<Set<string>>) {
    return new Person(await hobbiesPromise);
  }
  constructor(hobbies: Set<string>) {
    this.hobbies = new Set(hobbies);
  }
  addHobby (hobby: string) {
    this.hobbies.add(hobby);
  }
}
// CLOSURE
const makePerson = async (hobbiesPromise: Promise<Set<string>>) => {
  const hobbies = new Set(await hobbiesPromise);
  const addHobby = (hobby: string) => { hobbies.add(hobby); };
  return { addHobby };
};
type Person = ReturnType<typeof makePerson>;
```

JavaScript does not offer async constructor. Static async function is usually used as the workaround.

Closure, benefitting from the fact that it is a function, requires only `async` prefix. Thus only a minimum amount of change is required to achieve the same.

### Async Inner Periodical Task

Suppose we need a class that has a certain explicit "lifetime"--- ended when `destroy` is called---where within that "lifetime" it must run a certain code periodically.

With class, the problem is that every bootstrap code must be inside `constructor`, making it very bulky.

```
// prettier-ignore
class Worker {
  static async work1(isAlive: () => boolean) {
    while (isAlive()) { /* lots of LOC */ }
  }
  static async work2(isAlive: () => boolean) {
    while (isAlive()) { /* lots of LOC */ }
  }
  alive = true;
  constructor() {
    Worker.work1(this.isAlive);
    Worker.work2(this.isAlive);
  }
  private isAlive = () => this.alive
  destroy() { this.alive = false; }
}
```

In contrast to the conventional class where the constructor is always at the top, a closure is theoretically a constructor. Inside the function body, the programmer is free to arrange the internal objects and functions so they are well-organized according to their logical categories.

Look how organizing variables and functions within closure is easier. Comments, for example, can be used as a categorization tool.

```
const makeWorker = () => {
  // lifetime attributes
  // ==========
  let alive = true;
  const isAlive = () => alive;
  const destroy = () => { alive = false; };
  // Start workers 
  // ==========
  work1(isAlive);
  work2(isAlive);

  return { destroy };
};

const work1 = (isAlive: () => boolean) => {
  while (isAlive()) { /* lots of LOC */ }
};
const work2 = (isAlive: () => boolean) => {
  while (isAlive()) { /* lots of LOC */ }
};
```

### Method VS Static Method VS Orphan Function

Refactoring a method in a class often involves extracting a part of the method body that is used in other methods, or even a distant part of the codebase.

Suppose there is a function to compare the hobbies of two `Person` (this is not a good design, but please bear with me because this is the simplest I can think of).

```
class Person {
  private hobbies: Set<string>;
  constructor(hobbies: Set<string>) {
    this.hobbies = new Set(hobbies);
  }
  getHobbies() { return new Set(this.hobbies); }
  addHobbies(hobby: string) { this.hobbies.add(hobby); }
  intersectHobbies(otherPerson: Person) {
    const otherHobbies = otherPerson.getHobbies();
    const myHobbies = this.getHobbies();

    /**
     * Pretend that this operation is a very long and complex
     * algorithm that requires one to meditate and scroll up and down
     * for several tens of minutes to understand and then
     * you want to get this out because it messes with the readability of this method
     */
    const intersection = new Set<string>();
    Array.from(myHobbies)
      .filter((hobby) => otherHobbies.has(hobby))
      .forEach((hobby) => intersection.add(hobby));

    return intersection;
  }
}
```

Pretend that the commented section above is a long and complex algorithm and you want to move it out so that `intersectHobbies` are more readable.

My old inexperienced self would think that the most obvious solution was to move it to another method.

```
class Person {
  intersectHobbies(otherPerson: Person) {
    return this.implIntersectHobbies(
      this.getHobbies(),
      otherPerson.getHobbies()
    );
  }

  static implIntersectHobbies(hobbyA: Set<string>, hobbyB: Set<string>) {
    const intersection = new Set<string>();
    Array.from(myHobbies)
      .filter((hobby) => otherHobbies.has(hobby))
      .forEach((hobby) => intersection.add(hobby));
  }
}
```

After re-examining the code, then the realization comes that `implIntersectHobbies` does not call `this`. Therefore, it might fit more as a static function.

```
class Person {
  // ... rest of properties
  intersectHobbies(otherPerson: Person) {
    return Person.implIntersectHobbies(
      this.getHobbies(),
      otherPerson.getHobbies()
    );
  }

  static implIntersectHobbies(hobbyA: Set<string>, hobbyB: Set<string>) {
    const intersection = new Set<string>();
    Array.from(myHobbies)
      .filter((hobby) => otherHobbies.has(hobby))
      .forEach((hobby) => intersection.add(hobby));
  }
}
```

On another thought, `intersectHobbies` is just a set operation. It makes less sense to put it under `Person` than to put it under a `Set`-related module.

So the final code becomes:

```
class Person {
  // ... rest of properties
  intersectHobbies(otherPerson: Person) {
    return SetOperation.intersect(this.getHobbies(), otherPerson.getHobbies());
  }
}

// in another file
export namespace SetOperation {
  export const intersect = <T extends unkown>(
    aSet: Set<T>,
    bSet: Set<T>
  ): Set<T> => new Set(Array.from(aSet).filter((a) => bSet.has(a)));

  // ... rest of functions e.g. union, etc
}
```

Now the code looks good, but that is not the point. Look back on how the various features of `class` have different keywords and different callsigns, which makes refactoring hard.

**With closure**, the change will be less expensive because what will change is just the scope. Here is how the evolution will be with closures:

Iteration 0:

```
type Person = {
  addHobby: (hobby: string) => void;
  intersectHobby: (person: Person)
};
const makePerson = (initialHobbies: Set<string>) => {
  const hobbies = new Set(initialHobbies);
  const addHobby = (hobby: string) => { hobbies.add(hobby); };
  const getHobbies = () => new Set(hobbies);
  const intersectHobby = (otherPerson: Person) => {
    const otherHobbies = otherPerson.getHobbies();
    const myHobbies = getHobbies();

    /**
     * Pretend that this operation is a very long and complex
     * algorithm that requires one to meditate and scroll up and down
     * for several tens of minutes to understand and then
     * you want to get this out because it messes with the readability of this method
     */
    const intersection = new Set<string>();
    Array.from(myHobbies)
      .filter((hobby) => otherHobbies.has(hobby))
      .forEach((hobby) => intersection.add(hobby));

    return intersection;
  }
  return { addHobby, getHobbies, intersectHobby };
};
```

Iteration 1: Equivalent to moving the bulk of calculation into another method.

```
const makePerson = (initialHobbies: Set<string>) => {
  const hobbies = new Set(initialHobbies);
  const addHobby = (hobby: string) => { hobbies.add(hobby); };
  const getHobbies = () => new Set(hobbies);
  const intersectHobby = (otherPerson: Person) =>
    implIntersectHobbies(getHobbies(), otherPerson.getHobbies());

  const implIntersectHobbies = (hobbyA: Set<string>, hobbyB: Set<string>) => {
    const intersection = new Set<string>();
    Array.from(myHobbies)
      .filter((hobby) => otherHobbies.has(hobby))
      .forEach((hobby) => intersection.add(hobby));
  };
  return { addHobby, getHobbies, intersectHobby };
};
```

Iteration 2: Equivalent to converting the method into a static method

```
const makePerson = (initialHobbies: Set<string>) => {
  const hobbies = new Set(initialHobbies);
  const addHobby = (hobby: string) => { hobbies.add(hobby); };
  const getHobbies = () => new Set(hobbies);
  const intersectHobby = (otherPerson: Person) =>
    implIntersectHobbies(getHobbies(), otherPerson.getHobbies());
  return { addHobby, getHobbies, intersectHobby };
};

const implIntersectHobbies = (hobbyA: Set<string>, hobbyB: Set<string>) => {
    const intersection = new Set<string>();
    Array.from(myHobbies)
      .filter((hobby) => otherHobbies.has(hobby))
      .forEach((hobby) => intersection.add(hobby));
  };
```

Iteration 3: Equivalent to converting the method into a static method

```
const makePerson = (initialHobbies: Set<string>) => {
  const hobbies = new Set(initialHobbies);
  const addHobby = (hobby: string) => { hobbies.add(hobby); };
  const getHobbies = () => new Set(hobbies);
  const intersectHobby = (otherPerson: Person) =>
    SetOperation.intersect(getHobbies(), otherPerson.getHobbies());
  return { addHobby, getHobbies, intersectHobby };
};

// in another file
export namespace SetOperation {
  export const intersect = <T extends unkown>(
    aSet: Set<T>,
    bSet: Set<T>
  ): Set<T> => new Set(Array.from(aSet).filter((a) => bSet.has(a)));

  // ... rest of functions e.g. union, etc
}
```

_Never mind the lack of space in the closures. I recommend separating functions, variables, etc by their domain problem and/or their signature pattern. Comments also help a lot. However, I'm omitting comments and spacing for the sake of conciseness in terms of line of code so that the snippet does not fill up the screen._

### Lifetime Separation

Some refactors are motivated by [lifetime differences of its properties or parameters](https://valand.dev/systemic-ts/complication-4-class-layered-lifetime).

Take an example of this awkwardly made class.

```
class MetaExtractorTool {
  constructor(config: Config) {}
  generateMeta(rootDir: string) {}
  readMetaAsArray(rootDir: string) {}
  // ...other methods requiring `rootDir`
}
```

This class is used to extract metadata. The challenge with this class is that `config` is designed to be static (living indefinitely) and hardcoded. Meanwhile, `rootDir` is a value retrieved asynchronously.

So more or less it is used this way.

```
const BlogMetaExtractorTool = new MetaExtractorTool({ source: "./blog/posts" /*...other config*/ });

// and then later in other files
onRootDirReady.then((rootDir) => {
  BlogMetaExtractorTool.generateMeta(rootDir);
  BlogMetaExtractorTool.readMetaAsArray(rootDir);
  // ...other method calls passing `rootDir`
})
```

Then, it occurs to me that passing `rootDir` all over again does not make sense. It will be convenient when somehow `rootDir` is injected into `MetaExtractorTool`.

```
// BAD solution, introduces an invalid state
class MetaExtractorTool {
  rootDir: string;
  setRootDir(rootDir: string) { this.rootDir = rootDir; }
}
```

But, done this way, we will introduce an invalid state, which is when other methods are called before `setRootDir`.

Another solution comes to mind:

```
// This config is to be used with MetaExtractorTool
const BlogMetaExtractorToolConfig: Config = { source: "./blog/posts" /*...other config*/ };

// and then later in other files
onRootDirReady.then((rootDir) => {
  const tool = new MetaExtractorTool(BlogMetaExtractorToolConfig, rootDir);
  tool.generateMeta();
  tool.readMetaAsArray();
})
```

This presents another problem where `BlogMetaExtractorToolConfig` needs a comment saying that it is used together with `MetaExtractorTool`.

I need this knowledge of `MetaExtractorTool`, `Config`, and `rootDir` somehow organized closely. So, an intermediate `MetaExtractorToolIntermediate` is created to mend the fragmented code.

```
class MetaExtractorToolIntermediate {
  constructor(private config: Config) { }
  withRootDir(rootDir: string) { return new MetaExtractorTool(config,rootDir) }
}
class MetaExtractorTool {
  constructor(
    private config: Config,
    private rootDir: string
  ) {}
  generateMeta() {}
  readMetaAsArray() {}
}

// This config is to be used with MetaExtractorTool
const BlogMetaExtractorTool = new MetaExtractorToolIntermediate({ source: "./blog/posts" /*...other config*/ });

// and then later in other files
onRootDirReady.then((rootDir) => {
  const tool = BlogMetaExtractorTool.withRootDir(rootDir);
  tool.generateMeta();
  tool.readMetaAsArray();
})
```

That is much better, but pay attention closely: `MetaExtractorToolIntermediate` does not have any method or static method. A function fits more in this case.

```
const MetaExtractorToolIntermediate = (config: Config) => (rootDir: string) =>
  new MetaExtractorTool(config, rootDir);

// This config is to be used with MetaExtractorTool
const BlogMetaExtractorTool = MetaExtractorToolIntermediate({ source: "./blog/posts" /*...other config*/, });

// and then later in other files
onRootDirReady.then((rootDir) => {
  const tool = BlogMetaExtractorTool(rootDir);
  tool.generateMeta();
  tool.readMetaAsArray();
});
```

_Aside: It turns out that that pattern is called [currying](https://javascript.info/currying-partials)._

Pay attention to the class-to-function conversion of `MetaExtractorToolIntermediate`. The resulting function is a closure that returns a function instead of an object. The conversion is done because `MetaExtractorToolIntermediate` does not have any properties and methods.

But recall that refactoring---organizing complexity---[isn't commonly finalized within a single iteration](https://valand.dev/systemic-ts/systemic-ts/prelude-2-inherent-complexity). **What if in the future it will need a method?****Should it need to be converted into a class again?**

That very argument is why I encourage everyone to **use closure from the beginning to the end**.

## When To Use Class? Distinguish Pure Data VS Actor

With OOP, almost everything is modeled as an object. Semantically, this means they may act, because they have methods.

That notion is confusing because, between the entity that can act and cannot act blurs, the distinction blurs. It causes further problems with [serialization problem](https://valand.dev/systemic-ts/complication-2-class-prototype).

If you insist on using class then, before programming takes place, a distinction must be made: pure data vs actor.

For actors, I will use a loose definition as described in [this wikipedia page](https://en.wikipedia.org/wiki/Actor_model), microprocessors with their own local memory that can make local decisions, send and receive messages, and create more actors. However my point is exactly the opposite, not everything must be modeled as actors.

While figuring out a program's essential entities, classify them into actors or pure data. The most distinctive feature is whether an entity is serializable or not. Pure data is simple to serialize; an actor isn't.

Hold off the urge to determine that an entity is an actor. An entity must be an actor (those who act) mostly when it also needs to be an agent (those who work on behalf of someone else). An agent is usually long-running and concurrent.

Here are the two guidelines for using class:

*   Only apply class to actors.
*   Avoid inheritance (either inheriting other class or implementing an interface); [composition](https://en.wikipedia.org/wiki/Composition_over_inheritance) is capable of method sharing; [union](https://www.typescriptlang.org/docs/handbook/unions-and-intersections.html) is capable of polymorphism.

And again, all the above can be done with closures.

### Using the performance of class

[u/7Geordi](https://www.reddit.com/user/7Geordi/) made a [remark](https://www.reddit.com/r/typescript/comments/17721ht/comment/k4rb9ij/?utm_source=reddit&utm_medium=web2x&context=3) that `class`/`prototype` is an optimization over `closures`. It is somewhat true because theoretically (without looking into the implementation detail of the JS engine) for each unbound method in a `class` there is only one instance of a class. A method call looks up the `prototype` property of an object, grabs the prototype function with a matching name, and then calls `apply` or `call` with the object as `thisArg`.

The remark makes me feel obliged to run a simple benchmark.

For each `class` without bound methods, `class` with bound methods, and closure "class", I want to see the scores of:

*   How many construction operations can run in a second?
*   How much memory is used after creating 1 million instances?
*   How many method calls can run in a second?

The benchmark code is as follows.

```
// Class with bound method
class A {
	i = 0
	x = () => { this.i+=1 };
	y = () => { this.i+=1 };
};
// Class without bound method
class B {
	i = 0
	x(){ this.i+=1 };
	y(){ this.i+=1 }
};
// Equivalent closure
const makeC = () => {
	let i = 0;
	const x = () => { i+=1 };
	const y = () => { i+=1 };
	const self = { x,y };
	return self
};
```

The benchmark uses [https://jsbench.me/](https://jsbench.me/) so all its caveats are the benchmark's caveats as well, e.g. the benchmark is run in the browser and I am using chrome, thus can be slightly affected by background activities.

First, the results of construction operations are unexpected. The code of the benchmark is as follows.

```
// A
new A()

// B
new B()

// C
makeC()
```

The number of operations per second is respectively 934M (class + bound method), 973M (class), and 1B (closure). Second run yields 950M, 993M, and 985M respectively. Third run yields 936M, 931M, and 945M respectively. Subsequent runs always yield a similar number, with sometimes differing winning order.

The second test involves an array, creating a million instances, and then inspecting the `usedJSHeapSize`. Of course, usedJSHeapSize may have a small inaccuracy because some other things can affect the score.

```
// A
const vec = []
for (let i = 0; i < 1000000; i++) { vec.push(new A()) }
console.log("a", performance.memory.usedJSHeapSize)

// B
const vec = []
for (let i = 0; i < 1000000; i++) { vec.push(new B()) }
console.log("b", performance.memory.usedJSHeapSize)

// C
const vec = []
for (let i = 0; i < 1000000; i++) { vec.push(makeC()) }
console.log("c", performance.memory.usedJSHeapSize)
```

The results are then listed with a simple statistic, average, max, and min.

```
//avg
a 208086022
b  93690827
c 231439383

//max
a 375007395
b 216611803
c 461230603

//min
a 142267130
b  58161184
c 138307884
```

Approach `B`, class without method, wins by a landslide in all cases. It is not surprising simply because in `B` there is no duplicated method body for every instance. `A` and `C` score similarly.

Now to the last part, calling a method of a constructed object. The test is simple, it involves calling a method that modifies a property. But, in addition, I will also add another test case, which is a similar direct operation (without a method) to a function.

```
// a 
a.x()
// b
b.x()
// c
c.x()
// d = { i: 0 }
d.i+=1;
// i = 0
i+=1
```

Closure method call is the slowest, with almost half operations per second. Class with and without bound methods perform similarly, as well as direct operation to an object. Direct operation to a variable performs almost 3 times better than class. It seems there is a cost to the indirection within an in-method closure.

```
A: 588M ops/s ± 1.95%
B: 593M ops/s ± 1.23%
C: 263M ops/s ± 8.49%
D: 593M ops/s ± 1.75%
i: 1.5B ops/s ± 1.22%
```

### Optimizing Closure (Or rather, figuring out why the former does not perform well)

After doing the benchmark that shows closure's method call performance issue, I am curious whether the optimization done for a class is opaque from the userland.

Then I found some marking mechanisms for objects, namely [seal](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/seal) and [freeze](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze). The former prevents an object extension, prevents prototype reassignment, prevents enumerability changes, and fixes the size of the properties. The latter does what the former does and in addition, prevents any modification to the properties. I tinkered with the mechanisms and data structure and ran another set of benchmarks.

```
class B {
	i = 0
	x(){ this.i+=1 };
};

const makeE = () => { // object property
	const data = { i: 0 }
	const x = () => { data.i+=1 };
	const self = { x };
	return self
};

const makeF = () => { // object property, frozen
	const data = { i: 0 } 
	const x = () => { data.i+=1 };
	const self = { x };
	Object.freeze(self)
	return self
};

const makeG = () => { // object property, sealed, frozen
	const data = { i: 0 }
	const x = () => { data.i+=1 };
	const self = { x };
	Object.seal(data)
	Object.freeze(self)
	return self
};

const makeH = () => { // standalone variable
	let i = 0;
	const x = () => { i+=1 };
	const self = { x };
	Object.freeze(self)
	return self
}

const a = new A();
const e = makeE();
const f = makeF();
const g = makeG();
const h = makeH();

/// Test cases
// b
b.x();
// e
e.x();
// f
f.x();
// g
g.x();
// h
h.x();
```

The result is satisfying because now we know what happened with the closure from the previous benchmark.

```
B: 571M ops/s ± 1.76%
E: 557M ops/s ± 2.21%
F: 545M ops/s ± 4.3%
G: 569M ops/s ± 1.89%
H: 177M ops/s ± 3.48%
```

The benchmark shows modifying a member of an object is faster than modifying a standalone variable. There seems to be a hiccup with this engine's particular implementation with modifying an encapsulated standalone variable. Freezing and sealing don't seem to have a significant boost (if there is any at all).

When the closure method modifies a property within an object, it somehow performs almost similarly to a class. This is a good sign because there is no major difference that matters with using closure, except to avoid direct modification to standalone variables.

That is if you care about a small performance optimization that may happen only in a certain JS engine. However, as I previously recommended, the use of class or closure should be reduced as much as possible within the scope of the requirement. This will make the phenomenon less of a problem, considering non-method operations perform 1-3 times better than in-method operations.

<!-- source: https://valand.dev/systemic-ts/systemic-3-runtime-type-validation -->

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

<!-- source: https://valand.dev/systemic-ts/systemic-4-agency -->

Approaching system design with agency in mind is crucial. Agency is the various aspects of an agent, something that works on behalf of the other. In the computer program context, an agent works on behalf of the user.

An agent within a program is usually a long-running and concurrent process that has a part (or sometimes the whole) of the user's purpose.

While crucial, agency cannot be explained clearly because there is no single implementation that can fulfill all its aspects.

*   [Modern OOP](https://en.wikipedia.org/wiki/Object-oriented_programming) (as opposed to [Alan Kay's OOP](https://wiki.c2.com/?AlanKaysDefinitionOfObjectOriented)) tried to imply and activeness of an object by enabling [methods](https://en.wikipedia.org/wiki/Method_(computer_programming)).
*   [Multithreading](https://en.wikipedia.org/wiki/Multithreading_(computer_architecture)) tried to allow two sub-programs to run concurrently, allowing programmers to assume an active role within a system of several active roles. Messaging between agents would later take the form of [Mutex](https://en.wikipedia.org/wiki/Mutual_exclusion), [Channels](https://en.wikipedia.org/wiki/Channel_(programming)), [Semaphore](https://en.wikipedia.org/wiki/Semaphore_(programming)), etc.
*   [Agent-oriented programming](https://en.wikipedia.org/wiki/Agent-oriented_programming) essentially is a pattern to capture and synthesize the aspects of agents and agency.
*   Beliefs (e.g. over the meaning of signals, environment), capabilities, commitments, and message passing are partially fulfilled by the likes of interface, [typings](https://en.wikipedia.org/wiki/Datatyp), [serialization/deserialization](https://en.wikipedia.org/wiki/Serialization), etc, network.

A more concretely refined definition of agent I prefer is the independent multithreading-enabled self-centered code style combined with its outer shell interface definition reinforced with static typing, which looks like:

```
// pseudocode
thread.spawn(() => {
  // I'll do my own stuff here
  // regardless of my parent's state
});
```

## Merits of Previous Tips

If you have not visited the previous three articles, I suggest doing so:

*   [The Throwless Pact](https://valand.dev/systemic-ts/systemic-1-known-vs-unknown-error-throwless)
*   [Closure Over Class](https://valand.dev/systemic-ts/systemic-2-closure-over-class)
*   [Runtime Type Validation](https://valand.dev/systemic-ts/systemic-3-runtime-type-validation)

The merits of the three previous articles, the complication articles, and possibly the next articles culminate here. In building systems, the concept of agents eventually arises to combat the growing scale of the purpose of a system.

An agent, or more specifically the maintainer of a program-agent, the programmer, can only fit a number of symbols in one's memory at a time (i.e. name and meaning of types, functions, modules, routines, development processes, etc). One has to wrap a part of the purpose of the whole program into an agent, a sub-process that enacts tasks without direct supervision, and either report back or be examined at a lower intensity and frequency.

"Too complex" is a common complaint indicating that a new agent is required to bear a part of the purpose. Isn't it convenient, the idea of being able to specifically "Please take care of this stuff for me". Fire and forget.

```
// "Please take care of OSNotification for me"
const osNotificationWorker = OSNotificationWorker.make();
```

The main point of systemic-ts is to design agents that work well and are easily maintained. The Throwless Pact's absence of `throw`, combined with runtime type validation provides the reliability of agents. The signature transparency of The Throwless Pact aids by quickening the process of understanding agents' essence, and purpose, without having to scrutinize the implementation detail. Last, but not least, closure over class provides a quicker way to iterate while developing and maturing an agent.

In the end, an agent is a system that may reside within another bigger system. It is by principle must not be [scriptic](https://valand.dev/systemic-ts/prelude-1-system-vs-script).

## Agent as Cybernetic Loop

The good news is: JavaScript has a simple yet powerful [async function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function) that allows modeling concurrent agents. TypeScript completes the static typing part.

But before we dive into the core idea of this article, have you ever seen the pattern below?

```
function doStuffIndefinitely() {
  doStuff();
  setTimeout(doStuffIndefinitely, 100);
}
```

That pattern is a prototype of what I prefer to call the cybernetic loop--this article's core idea.

[Cybernetic](https://en.wikipedia.org/wiki/Cybernetics) is about circular repeating processes. [Norbert Wiener](https://en.wikipedia.org/wiki/Norbert_Wiener) named it _kubernētikēs_ (meaning steering) inspired by the phenomenon where a helmsman's steering behavior is affected by his observation of the effect of his own past steering on the current ship's course.

The helmsman's cybernetic loop is a loop containing the routine of: observe, steer, observe, steer, observe, steer, and so on. Put abstractly, a cybernetic loop contains the routine of its agent.

Let's cut to the chase and convert the above "prototype" code into a loop.

```
const doStuffIndefinitely = async () => {
  while (true) {
    doStuff();
    await sleep(100);
  }
};

// helper
const sleep = (dur: number) => new Promise((res) => setTimeout(res, dur));
```

In a high-level language such as JavaScript, this loop is not as common of a pattern as it is in lower-level languages (e.g. C, C++, Rust). In JavaScript, functionalities that require such a loop have been enabled by [its internal event loop](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop).

However, JavaScript's event loop's capability is limited, so people start to form the loop's "prototype" to make up for the missing features.

The cybernetic loop is a powerful model for long-running processes such as:

*   a game engine's main loop
*   an HTTP server
*   a controller within a pipeline
*   [fiber](https://en.wikipedia.org/wiki/Fiber_(computer_science)) processor.

Let us see how easy to add a feature to a cybernetic loop.

External and internal termination can be added just in several lines.

```
const QuittableAgent = async (externalKillSignal: () => bool) => {
  while (!externalKillSignal()) {
    const res = await work();
    if (res === QUIT) break;
    await sleep(0);
  }
};
```

Adding a state would allow advanced mechanisms such as self-regulation.

```
const SelfRegulatingAgent = async (externalKillSignal: () => bool) => {
  const state = makeState();
  while (!externalKillSignal()) {
    const res = await work(state);
    if (res === QUIT) break;
    await sleep(0);
  }
};
```

Finally, an external could be established by means of an input buffer. Add a bit of an `end`-related feature (e.g. waiting for the agent to shut down).

```
const InteractibleAgent = (externalKillSignal: () => bool) => {
  const input = makeInputBuffer();
  const state = makeState();

  const end = (async () => {
    while (!input.externalKillSignal() && !externalKillSignal()) {
      const res = await work(state, input);
      if (res === QUIT) break;
      await sleep(0);
    }
  })();

  let endFlag = false;
  const isEnded = () => endFlag;

  end.finally(() => (ended = true));

  return { input, end, isEnded };
};
```

The above agent is interactible this way.

```
const agent = InteractibleAgent();
// issue command on agent
await agent.input.someCommand();
// retrieve data from agent
const agent = input.getSomeValue();
// end agent
agent.input.kill();
// wait for the agent to end
await agent.end;
```

Keep note that these forms are simplifications.

For example, `input`, `state`, and `work(state, input)` will be more complex in the real world. `input` for example should be properly typed so that parties that interact with the agent can know the agent's capability.

Another important point is that this pattern naturally leads the programmer to program `input` (or any externally available methods) as a buffer or a cache. This makes the agent more resilient toward mischievous external parties (e.g. if one of the methods is spammed)

## Sub agents

Cybernetic loop pattern is compatible with a hierarchical structure. Let us take an example of a parallel processing hub, a small machine that reroutes requests to other powerful processors. The processors work at different paces so the hub needs to communicate with each processor asynchronously.

```
const Hub = (params: {
  processorsAddresses: string[];
  requestPort: Port;
  offloadPort: Port;
  externalKillSignal: () => bool;
}) => {
  // Generate an agent for each processorsAddresses
  // 'agents' variable is a container of agents with helper
  // methods to find agents of various statuses
  const agents = ProcessorAgents.makeBulk(
    params.processorsAddresses,
    params.externalKillSignal
  );

  while (!params.externalKillSignal()) {
    // Offload done work to offload port
    const doneWorkings = agents.findAwaitingForOffload();
    doneWorkings.forEach((agent) => agent.offloadFrom(params.offloadPort));

    // For each idle agent, supply it with a request
    const readyForWorks = agents.findIdleAgents();
    readyForWorks.forEach((agent) => agent.startWorkFrom(params.requestPort));

    await sleep(500);
  }
};
```

This setup is nice, the hub is not blocked by neither the `Ports` nor the `ProcessorAgents`--no bottlenecks.

It does not have to worry about the `ProcessorAgents` timing because we assume that these processors self-regulate. For example, 1.) they signal their state accurately, whether they are ready to take another request or ready to offload so that `findAwaitingForOffload` and `findIdleAgents` filters the correct agents, or 2.) that malicious calls to `startWorkFrom` or `offloadFrom` are handled well internally.

## Explicit Lifetime Management and Agents

The idea of explicit lifetime management has been briefly visited in the [closure-over-class](https://valand.dev/systemic-ts/systemic-2-closure-over-class), but now let us revisit the idea and relate it to agents and sub-agents.

Unless demanded by exotic requirement, generally and by default the sub-agents must not outlive their parent. This reasoning spans from the top-level or root-level agent to all leaves (if the hierarchical agents are perceived as a tree) so that the root lives the longest and encompasses all agents' lifetimes.

However, since an agent's control flow is detached from its ancestors, each parent is responsible for explicitly stopping its children and waiting for their lifetime to end before ending their own lifetime. Therefore it is necessary for each agent to have a `destroy` method that is only exposed to the parent.

Poetically, the root-level `destroy` "method" of a GUI application is the close (X) button that the user, its parent, can click before the user turns off the PC and continues with life.

## Illusion of Task

Since an agent is long-running and concurrent, it must also be asynchronous in TypeScript/JavaScript world. This notion is not limited to the TypeScript/JavaScript world and is often the primary cause of confusing an agent with a task.

To counter-argue my previous point that "sub-agents" must not outlive their parent, I am tempted to say that nowadays in the cloud-pervasive world, we often spawn a remote agent that works for us while its parent is sleeping. Particularly, I am talking about spawning in-cloud rent computers e.g. AWS, Azure, and Google's virtual machines.

But a computer we issue remotely is not purely an agent of us. In a way, what we do is issue a task to a third-party provider, which is put into practice by spawning an agent of theirs as an agent of ours.

I encourage you to meditate on this phenomenon and put it back in the context of agents within programs, or even within a TypeScript-based program.

**For an entity that could be an agent, could it be represented as a task instead?**

This question is important because agents need explicit lifetime management and manually managing lifetime isn't an easy task. Thus, a program could be modeled as agents passing tasks (and messages in general) to one another. This brings us back to the [first inspiration of OOP](https://wiki.c2.com/?AlanKaysDefinitionOfObjectOriented), but not having to develop a whole new language and falling into the traps such as prematurely [marrying inheritance to the language](https://en.wikipedia.org/wiki/Composition_over_inheritance), or prematurely marrying module visibility with data encapsulation, or deciding that [everything is an object!](https://en.wikipedia.org/wiki/Object-oriented_programming)

## Part 2 — Gang-of-Four Patterns in TypeScript

*by refactoring.guru · conceptual examples adapted for TypeScript*

### Creational patterns

<!-- source: https://refactoring.guru/design-patterns/abstract-factory/typescript/example -->

# Abstract Factory in TypeScript / Design Patterns

# **Abstract Factory** in TypeScript

**Abstract Factory** is a creational design pattern, which solves the problem of creating entire product families without specifying their concrete classes.

Abstract Factory defines an interface for creating all distinct products but leaves the actual product creation to concrete factory classes. Each factory type corresponds to a certain product variety.

The client code calls the creation methods of a factory object instead of creating products directly with a constructor call (`new` operator). Since a factory corresponds to a single product variant, all its products will be compatible.

Client code works with factories and products only through their abstract interfaces. This lets the client code work with any product variants, created by the factory object. You just create a new concrete factory class and pass it to the client code.

> If you can’t figure out the difference between various factory patterns and concepts, then read our [Factory Comparison](https://refactoring.guru/design-patterns/factory-comparison).
**Usage examples:** The Abstract Factory pattern is pretty common in TypeScript code. Many frameworks and libraries use it to provide a way to extend and customize their standard components.

**Identification:** The pattern is easy to recognize by methods, which return a factory object. Then, the factory is used for creating specific sub-components.

## Conceptual Example

This example illustrates the structure of the **Abstract Factory** design pattern. It focuses on answering these questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Abstract Factory interface declares a set of methods that return
 * different abstract products. These products are called a family and are
 * related by a high-level theme or concept. Products of one family are usually
 * able to collaborate among themselves. A family of products may have several
 * variants, but the products of one variant are incompatible with products of
 * another.
 */
interface AbstractFactory {
    createProductA(): AbstractProductA;

    createProductB(): AbstractProductB;
}

/**
 * Concrete Factories produce a family of products that belong to a single
 * variant. The factory guarantees that resulting products are compatible. Note
 * that signatures of the Concrete Factory's methods return an abstract product,
 * while inside the method a concrete product is instantiated.
 */
class ConcreteFactory1 implements AbstractFactory {
    public createProductA(): AbstractProductA {
        return new ConcreteProductA1();
    }

    public createProductB(): AbstractProductB {
        return new ConcreteProductB1();
    }
}

/**
 * Each Concrete Factory has a corresponding product variant.
 */
class ConcreteFactory2 implements AbstractFactory {
    public createProductA(): AbstractProductA {
        return new ConcreteProductA2();
    }

    public createProductB(): AbstractProductB {
        return new ConcreteProductB2();
    }
}

/**
 * Each distinct product of a product family should have a base interface. All
 * variants of the product must implement this interface.
 */
interface AbstractProductA {
    usefulFunctionA(): string;
}

/**
 * These Concrete Products are created by corresponding Concrete Factories.
 */
class ConcreteProductA1 implements AbstractProductA {
    public usefulFunctionA(): string {
        return 'The result of the product A1.';
    }
}

class ConcreteProductA2 implements AbstractProductA {
    public usefulFunctionA(): string {
        return 'The result of the product A2.';
    }
}

/**
 * Here's the base interface of another product. All products can interact with
 * each other, but proper interaction is possible only between products of the
 * same concrete variant.
 */
interface AbstractProductB {
    /**
     * Product B is able to do its own thing...
     */
    usefulFunctionB(): string;

    /**
     * ...but it also can collaborate with the ProductA.
     *
     * The Abstract Factory makes sure that all products it creates are of the
     * same variant and thus, compatible.
     */
    anotherUsefulFunctionB(collaborator: AbstractProductA): string;
}

/**
 * These Concrete Products are created by corresponding Concrete Factories.
 */
class ConcreteProductB1 implements AbstractProductB {

    public usefulFunctionB(): string {
        return 'The result of the product B1.';
    }

    /**
     * The variant, Product B1, is only able to work correctly with the variant,
     * Product A1. Nevertheless, it accepts any instance of AbstractProductA as
     * an argument.
     */
    public anotherUsefulFunctionB(collaborator: AbstractProductA): string {
        const result = collaborator.usefulFunctionA();
        return `The result of the B1 collaborating with the (${result})`;
    }
}

class ConcreteProductB2 implements AbstractProductB {

    public usefulFunctionB(): string {
        return 'The result of the product B2.';
    }

    /**
     * The variant, Product B2, is only able to work correctly with the variant,
     * Product A2. Nevertheless, it accepts any instance of AbstractProductA as
     * an argument.
     */
    public anotherUsefulFunctionB(collaborator: AbstractProductA): string {
        const result = collaborator.usefulFunctionA();
        return `The result of the B2 collaborating with the (${result})`;
    }
}

/**
 * The client code works with factories and products only through abstract
 * types: AbstractFactory and AbstractProduct. This lets you pass any factory or
 * product subclass to the client code without breaking it.
 */
function clientCode(factory: AbstractFactory) {
    const productA = factory.createProductA();
    const productB = factory.createProductB();

    console.log(productB.usefulFunctionB());
    console.log(productB.anotherUsefulFunctionB(productA));
}

/**
 * The client code can work with any concrete factory class.
 */
console.log('Client: Testing client code with the first factory type...');
clientCode(new ConcreteFactory1());

console.log('');

console.log('Client: Testing the same client code with the second factory type...');
clientCode(new ConcreteFactory2());

#### **Output.txt:** Execution result

Client: Testing client code with the first factory type...
The result of the product B1.
The result of the B1 collaborating with the (The result of the product A1.)

Client: Testing the same client code with the second factory type...
The result of the product B2.
The result of the B2 collaborating with the (The result of the product A2.)

<!-- source: https://refactoring.guru/design-patterns/builder/typescript/example -->

# Builder in TypeScript / Design Patterns

# **Builder** in TypeScript

**Builder** is a creational design pattern, which allows constructing complex objects step by step.

Unlike other creational patterns, Builder doesn’t require products to have a common interface. That makes it possible to produce different products using the same construction process.
**Usage examples:** The Builder pattern is a well-known pattern in TypeScript world. It’s especially useful when you need to create an object with lots of possible configuration options.

**Identification:** The Builder pattern can be recognized in a class, which has a single creation method and several methods to configure the resulting object. Builder methods often support chaining (for example, `someBuilder.setValueA(1).setValueB(2).create()`).

## Conceptual Example

This example illustrates the structure of the **Builder** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Builder interface specifies methods for creating the different parts of
 * the Product objects.
 */
interface Builder {
    producePartA(): void;
    producePartB(): void;
    producePartC(): void;
}

/**
 * The Concrete Builder classes follow the Builder interface and provide
 * specific implementations of the building steps. Your program may have several
 * variations of Builders, implemented differently.
 */
class ConcreteBuilder1 implements Builder {
    private product: Product1;

    /**
     * A fresh builder instance should contain a blank product object, which is
     * used in further assembly.
     */
    constructor() {
        this.reset();
    }

    public reset(): void {
        this.product = new Product1();
    }

    /**
     * All production steps work with the same product instance.
     */
    public producePartA(): void {
        this.product.parts.push('PartA1');
    }

    public producePartB(): void {
        this.product.parts.push('PartB1');
    }

    public producePartC(): void {
        this.product.parts.push('PartC1');
    }

    /**
     * Concrete Builders are supposed to provide their own methods for
     * retrieving results. That's because various types of builders may create
     * entirely different products that don't follow the same interface.
     * Therefore, such methods cannot be declared in the base Builder interface
     * (at least in a statically typed programming language).
     *
     * Usually, after returning the end result to the client, a builder instance
     * is expected to be ready to start producing another product. That's why
     * it's a usual practice to call the reset method at the end of the
     * `getProduct` method body. However, this behavior is not mandatory, and
     * you can make your builders wait for an explicit reset call from the
     * client code before disposing of the previous result.
     */
    public getProduct(): Product1 {
        const result = this.product;
        this.reset();
        return result;
    }
}

/**
 * It makes sense to use the Builder pattern only when your products are quite
 * complex and require extensive configuration.
 *
 * Unlike in other creational patterns, different concrete builders can produce
 * unrelated products. In other words, results of various builders may not
 * always follow the same interface.
 */
class Product1 {
    public parts: string[] = [];

    public listParts(): void {
        console.log(`Product parts: ${this.parts.join(', ')}\n`);
    }
}

/**
 * The Director is only responsible for executing the building steps in a
 * particular sequence. It is helpful when producing products according to a
 * specific order or configuration. Strictly speaking, the Director class is
 * optional, since the client can control builders directly.
 */
class Director {
    private builder: Builder;

    /**
     * The Director works with any builder instance that the client code passes
     * to it. This way, the client code may alter the final type of the newly
     * assembled product.
     */
    public setBuilder(builder: Builder): void {
        this.builder = builder;
    }

    /**
     * The Director can construct several product variations using the same
     * building steps.
     */
    public buildMinimalViableProduct(): void {
        this.builder.producePartA();
    }

    public buildFullFeaturedProduct(): void {
        this.builder.producePartA();
        this.builder.producePartB();
        this.builder.producePartC();
    }
}

/**
 * The client code creates a builder object, passes it to the director and then
 * initiates the construction process. The end result is retrieved from the
 * builder object.
 */
function clientCode(director: Director) {
    const builder = new ConcreteBuilder1();
    director.setBuilder(builder);

    console.log('Standard basic product:');
    director.buildMinimalViableProduct();
    builder.getProduct().listParts();

    console.log('Standard full featured product:');
    director.buildFullFeaturedProduct();
    builder.getProduct().listParts();

    // Remember, the Builder pattern can be used without a Director class.
    console.log('Custom product:');
    builder.producePartA();
    builder.producePartC();
    builder.getProduct().listParts();
}

const director = new Director();
clientCode(director);

#### **Output.txt:** Execution result

Standard basic product:
Product parts: PartA1

Standard full featured product:
Product parts: PartA1, PartB1, PartC1

Custom product:
Product parts: PartA1, PartC1

<!-- source: https://refactoring.guru/design-patterns/factory-method/typescript/example -->

# Factory Method in TypeScript / Design Patterns

# **Factory Method** in TypeScript

**Factory method** is a creational design pattern which solves the problem of creating product objects without specifying their concrete classes.

The Factory Method defines a method, which should be used for creating objects instead of using a direct constructor call (`new` operator). Subclasses can override this method to change the class of objects that will be created.

> If you can’t figure out the difference between various factory patterns and concepts, then read our [Factory Comparison](https://refactoring.guru/design-patterns/factory-comparison).
**Usage examples:** The Factory Method pattern is widely used in TypeScript code. It’s very useful when you need to provide a high level of flexibility for your code.

**Identification:** Factory methods can be recognized by creation methods that construct objects from concrete classes. While concrete classes are used during the object creation, the return type of the factory methods is usually declared as either an abstract class or an interface.

## Conceptual Example

This example illustrates the structure of the **Factory Method** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Creator class declares the factory method that is supposed to return an
 * object of a Product class. The Creator's subclasses usually provide the
 * implementation of this method.
 */
abstract class Creator {
    /**
     * Note that the Creator may also provide some default implementation of the
     * factory method.
     */
    public abstract factoryMethod(): Product;

    /**
     * Also note that, despite its name, the Creator's primary responsibility is
     * not creating products. Usually, it contains some core business logic that
     * relies on Product objects, returned by the factory method. Subclasses can
     * indirectly change that business logic by overriding the factory method
     * and returning a different type of product from it.
     */
    public someOperation(): string {
        // Call the factory method to create a Product object.
        const product = this.factoryMethod();
        // Now, use the product.
        return `Creator: The same creator's code has just worked with ${product.operation()}`;
    }
}

/**
 * Concrete Creators override the factory method in order to change the
 * resulting product's type.
 */
class ConcreteCreator1 extends Creator {
    /**
     * Note that the signature of the method still uses the abstract product
     * type, even though the concrete product is actually returned from the
     * method. This way the Creator can stay independent of concrete product
     * classes.
     */
    public factoryMethod(): Product {
        return new ConcreteProduct1();
    }
}

class ConcreteCreator2 extends Creator {
    public factoryMethod(): Product {
        return new ConcreteProduct2();
    }
}

/**
 * The Product interface declares the operations that all concrete products must
 * implement.
 */
interface Product {
    operation(): string;
}

/**
 * Concrete Products provide various implementations of the Product interface.
 */
class ConcreteProduct1 implements Product {
    public operation(): string {
        return '{Result of the ConcreteProduct1}';
    }
}

class ConcreteProduct2 implements Product {
    public operation(): string {
        return '{Result of the ConcreteProduct2}';
    }
}

/**
 * The client code works with an instance of a concrete creator, albeit through
 * its base interface. As long as the client keeps working with the creator via
 * the base interface, you can pass it any creator's subclass.
 */
function clientCode(creator: Creator) {
    // ...
    console.log('Client: I\'m not aware of the creator\'s class, but it still works.');
    console.log(creator.someOperation());
    // ...
}

/**
 * The Application picks a creator's type depending on the configuration or
 * environment.
 */
console.log('App: Launched with the ConcreteCreator1.');
clientCode(new ConcreteCreator1());
console.log('');

console.log('App: Launched with the ConcreteCreator2.');
clientCode(new ConcreteCreator2());

#### **Output.txt:** Execution result

App: Launched with the ConcreteCreator1.
Client: I'm not aware of the creator's class, but it still works.
Creator: The same creator's code has just worked with {Result of the ConcreteProduct1}

App: Launched with the ConcreteCreator2.
Client: I'm not aware of the creator's class, but it still works.
Creator: The same creator's code has just worked with {Result of the ConcreteProduct2}

<!-- source: https://refactoring.guru/design-patterns/prototype/typescript/example -->

# Prototype in TypeScript / Design Patterns

# **Prototype** in TypeScript

**Prototype** is a creational design pattern that allows cloning objects, even complex ones, without coupling to their specific classes.

All prototype classes should have a common interface that makes it possible to copy objects even if their concrete classes are unknown. Prototype objects can produce full copies since objects of the same class can access each other’s private fields.
**Usage examples:** The Prototype pattern is available in TypeScript out of the box with a JavaScript’s native `Object.assign()` method.

**Identification:** The prototype can be easily recognized by a `clone` or `copy` methods,etc.

## Conceptual Example

This example illustrates the structure of the **Prototype** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The example class that has cloning ability. We'll see how the values of field
 * with different types will be cloned.
 */
class Prototype {
    public primitive: any;
    public component: object;
    public circularReference: ComponentWithBackReference;

    public clone(): this {
        const clone = Object.create(this);

        clone.component = Object.create(this.component);

        // Cloning an object that has a nested object with backreference
        // requires special treatment. After the cloning is completed, the
        // nested object should point to the cloned object, instead of the
        // original object. Spread operator can be handy for this case.
        clone.circularReference = new ComponentWithBackReference(clone);

        return clone;
    }
}

class ComponentWithBackReference {
    public prototype;

    constructor(prototype: Prototype) {
        this.prototype = prototype;
    }
}

/**
 * The client code.
 */
function clientCode() {
    const p1 = new Prototype();
    p1.primitive = 245;
    p1.component = new Date();
    p1.circularReference = new ComponentWithBackReference(p1);

    const p2 = p1.clone();
    if (p1.primitive === p2.primitive) {
        console.log('Primitive field values have been carried over to a clone. Yay!');
    } else {
        console.log('Primitive field values have not been copied. Booo!');
    }
    if (p1.component === p2.component) {
        console.log('Simple component has not been cloned. Booo!');
    } else {
        console.log('Simple component has been cloned. Yay!');
    }

    if (p1.circularReference === p2.circularReference) {
        console.log('Component with back reference has not been cloned. Booo!');
    } else {
        console.log('Component with back reference has been cloned. Yay!');
    }

    if (p1.circularReference.prototype === p2.circularReference.prototype) {
        console.log('Component with back reference is linked to original object. Booo!');
    } else {
        console.log('Component with back reference is linked to the clone. Yay!');
    }
}

clientCode();

#### **Output.txt:** Execution result

Primitive field values have been carried over to a clone. Yay!
Simple component has been cloned. Yay!
Component with back reference has been cloned. Yay!
Component with back reference is linked to the clone. Yay!

<!-- source: https://refactoring.guru/design-patterns/singleton/typescript/example -->

# Singleton in TypeScript / Design Patterns

# **Singleton** in TypeScript

**Singleton** is a creational design pattern, which ensures that only one object of its kind exists and provides a single point of access to it for any other code.

Singleton has almost the same pros and cons as global variables. Although they’re super-handy, they break the modularity of your code.

You can’t just use a class that depends on a Singleton in some other context, without carrying over the Singleton to the other context. Most of the time, this limitation comes up during the creation of unit tests.
**Usage examples:** A lot of developers consider the Singleton pattern an antipattern. That’s why its usage is on the decline in TypeScript code.

**Identification:** Singleton can be recognized by a static creation method, which returns the same cached object.

## Conceptual Example

This example illustrates the structure of the **Singleton** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Singleton class defines an `instance` getter, that lets clients access
 * the unique singleton instance.
 */
class Singleton {
    static #instance: Singleton;

    /**
     * The Singleton's constructor should always be private to prevent direct
     * construction calls with the `new` operator.
     */
    private constructor() { }

    /**
     * The static getter that controls access to the singleton instance.
     *
     * This implementation allows you to extend the Singleton class while
     * keeping just one instance of each subclass around.
     */
    public static get instance(): Singleton {
        if (!Singleton.#instance) {
            Singleton.#instance = new Singleton();
        }

        return Singleton.#instance;
    }

    /**
     * Finally, any singleton can define some business logic, which can be
     * executed on its instance.
     */
    public someBusinessLogic() {
        // ...
    }
}

/**
 * The client code.
 */
function clientCode() {
    const s1 = Singleton.instance;
    const s2 = Singleton.instance;

    if (s1 === s2) {
        console.log(
            'Singleton works, both variables contain the same instance.'
        );
    } else {
        console.log('Singleton failed, variables contain different instances.');
    }
}

clientCode();

#### **Output.txt:** Execution result

Singleton works, both variables contain the same instance.

<!-- source: https://refactoring.guru/design-patterns/adapter/typescript/example -->

# Adapter in TypeScript / Design Patterns

# **Adapter** in TypeScript

**Adapter** is a structural design pattern, which allows incompatible objects to collaborate.

The Adapter acts as a wrapper between two objects. It catches calls for one object and transforms them to format and interface recognizable by the second object.
**Usage examples:** The Adapter pattern is pretty common in TypeScript code. It’s very often used in systems based on some legacy code. In such cases, Adapters make legacy code work with modern classes.

**Identification:** Adapter is recognizable by a constructor which takes an instance of a different abstract/interface type. When the adapter receives a call to any of its methods, it translates parameters to the appropriate format and then directs the call to one or several methods of the wrapped object.

## Conceptual Example

This example illustrates the structure of the **Adapter** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Target defines the domain-specific interface used by the client code.
 */
class Target {
    public request(): string {
        return 'Target: The default target\'s behavior.';
    }
}

/**
 * The Adaptee contains some useful behavior, but its interface is incompatible
 * with the existing client code. The Adaptee needs some adaptation before the
 * client code can use it.
 */
class Adaptee {
    public specificRequest(): string {
        return '.eetpadA eht fo roivaheb laicepS';
    }
}

/**
 * The Adapter makes the Adaptee's interface compatible with the Target's
 * interface.
 */
class Adapter extends Target {
    private adaptee: Adaptee;

    constructor(adaptee: Adaptee) {
        super();
        this.adaptee = adaptee;
    }

    public request(): string {
        const result = this.adaptee.specificRequest().split('').reverse().join('');
        return `Adapter: (TRANSLATED) ${result}`;
    }
}

/**
 * The client code supports all classes that follow the Target interface.
 */
function clientCode(target: Target) {
    console.log(target.request());
}

console.log('Client: I can work just fine with the Target objects:');
const target = new Target();
clientCode(target);

console.log('');

const adaptee = new Adaptee();
console.log('Client: The Adaptee class has a weird interface. See, I don\'t understand it:');
console.log(`Adaptee: ${adaptee.specificRequest()}`);

console.log('');

console.log('Client: But I can work with it via the Adapter:');
const adapter = new Adapter(adaptee);
clientCode(adapter);

#### **Output.txt:** Execution result

Client: I can work just fine with the Target objects:
Target: The default target's behavior.

Client: The Adaptee class has a weird interface. See, I don't understand it:
Adaptee: .eetpadA eht fo roivaheb laicepS

Client: But I can work with it via the Adapter:
Adapter: (TRANSLATED) Special behavior of the Adaptee.

<!-- source: https://refactoring.guru/design-patterns/bridge/typescript/example -->

# Bridge in TypeScript / Design Patterns

# **Bridge** in TypeScript

**Bridge** is a structural design pattern that divides business logic or huge class into separate class hierarchies that can be developed independently.

One of these hierarchies (often called the Abstraction) will get a reference to an object of the second hierarchy (Implementation). The abstraction will be able to delegate some (sometimes, most) of its calls to the implementations object. Since all implementations will have a common interface, they’d be interchangeable inside the abstraction.
**Usage examples:** The Bridge pattern is especially useful when dealing with cross-platform apps, supporting multiple types of database servers or working with several API providers of a certain kind (for example, cloud platforms, social networks,etc.)

**Identification:** Bridge can be recognized by a clear distinction between some controlling entity and several different platforms that it relies on.

## Conceptual Example

This example illustrates the structure of the **Bridge** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Abstraction defines the interface for the "control" part of the two class
 * hierarchies. It maintains a reference to an object of the Implementation
 * hierarchy and delegates all of the real work to this object.
 */
class Abstraction {
    protected implementation: Implementation;

    constructor(implementation: Implementation) {
        this.implementation = implementation;
    }

    public operation(): string {
        const result = this.implementation.operationImplementation();
        return `Abstraction: Base operation with:\n${result}`;
    }
}

/**
 * You can extend the Abstraction without changing the Implementation classes.
 */
class ExtendedAbstraction extends Abstraction {
    public operation(): string {
        const result = this.implementation.operationImplementation();
        return `ExtendedAbstraction: Extended operation with:\n${result}`;
    }
}

/**
 * The Implementation defines the interface for all implementation classes. It
 * doesn't have to match the Abstraction's interface. In fact, the two
 * interfaces can be entirely different. Typically the Implementation interface
 * provides only primitive operations, while the Abstraction defines higher-
 * level operations based on those primitives.
 */
interface Implementation {
    operationImplementation(): string;
}

/**
 * Each Concrete Implementation corresponds to a specific platform and
 * implements the Implementation interface using that platform's API.
 */
class ConcreteImplementationA implements Implementation {
    public operationImplementation(): string {
        return 'ConcreteImplementationA: Here\'s the result on the platform A.';
    }
}

class ConcreteImplementationB implements Implementation {
    public operationImplementation(): string {
        return 'ConcreteImplementationB: Here\'s the result on the platform B.';
    }
}

/**
 * Except for the initialization phase, where an Abstraction object gets linked
 * with a specific Implementation object, the client code should only depend on
 * the Abstraction class. This way the client code can support any abstraction-
 * implementation combination.
 */
function clientCode(abstraction: Abstraction) {
    // ..

    console.log(abstraction.operation());

    // ..
}

/**
 * The client code should be able to work with any pre-configured abstraction-
 * implementation combination.
 */
let implementation = new ConcreteImplementationA();
let abstraction = new Abstraction(implementation);
clientCode(abstraction);

console.log('');

implementation = new ConcreteImplementationB();
abstraction = new ExtendedAbstraction(implementation);
clientCode(abstraction);

#### **Output.txt:** Execution result

Abstraction: Base operation with:
ConcreteImplementationA: Here's the result on the platform A.

ExtendedAbstraction: Extended operation with:
ConcreteImplementationB: Here's the result on the platform B.

<!-- source: https://refactoring.guru/design-patterns/composite/typescript/example -->

# Composite in TypeScript / Design Patterns

# **Composite** in TypeScript

**Composite** is a structural design pattern that lets you compose objects into tree structures and then work with these structures as if they were individual objects.

Composite became a pretty popular solution for the most problems that require building a tree structure. Composite’s great feature is the ability to run methods recursively over the whole tree structure and sum up the results.
**Usage examples:** The Composite pattern is pretty common in TypeScript code. It’s often used to represent hierarchies of user interface components or the code that works with graphs.

**Identification:** If you have an object tree, and each object of a tree is a part of the same class hierarchy, this is most likely a composite. If methods of these classes delegate the work to child objects of the tree and do it via the base class/interface of the hierarchy, this is definitely a composite.

## Conceptual Example

This example illustrates the structure of the **Composite** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The base Component class declares common operations for both simple and
 * complex objects of a composition.
 */
abstract class Component {
    protected parent!: Component | null;

    /**
     * Optionally, the base Component can declare an interface for setting and
     * accessing a parent of the component in a tree structure. It can also
     * provide some default implementation for these methods.
     */
    public setParent(parent: Component | null) {
        this.parent = parent;
    }

    public getParent(): Component | null {
        return this.parent;
    }

    /**
     * In some cases, it would be beneficial to define the child-management
     * operations right in the base Component class. This way, you won't need to
     * expose any concrete component classes to the client code, even during the
     * object tree assembly. The downside is that these methods will be empty
     * for the leaf-level components.
     */
    public add(component: Component): void { }

    public remove(component: Component): void { }

    /**
     * You can provide a method that lets the client code figure out whether a
     * component can bear children.
     */
    public isComposite(): boolean {
        return false;
    }

    /**
     * The base Component may implement some default behavior or leave it to
     * concrete classes (by declaring the method containing the behavior as
     * "abstract").
     */
    public abstract operation(): string;
}

/**
 * The Leaf class represents the end objects of a composition. A leaf can't have
 * any children.
 *
 * Usually, it's the Leaf objects that do the actual work, whereas Composite
 * objects only delegate to their sub-components.
 */
class Leaf extends Component {
    public operation(): string {
        return 'Leaf';
    }
}

/**
 * The Composite class represents the complex components that may have children.
 * Usually, the Composite objects delegate the actual work to their children and
 * then "sum-up" the result.
 */
class Composite extends Component {
    protected children: Component[] = [];

    /**
     * A composite object can add or remove other components (both simple or
     * complex) to or from its child list.
     */
    public add(component: Component): void {
        this.children.push(component);
        component.setParent(this);
    }

    public remove(component: Component): void {
        const componentIndex = this.children.indexOf(component);
        this.children.splice(componentIndex, 1);

        component.setParent(null);
    }

    public isComposite(): boolean {
        return true;
    }

    /**
     * The Composite executes its primary logic in a particular way. It
     * traverses recursively through all its children, collecting and summing
     * their results. Since the composite's children pass these calls to their
     * children and so forth, the whole object tree is traversed as a result.
     */
    public operation(): string {
        const results = [];
        for (const child of this.children) {
            results.push(child.operation());
        }

        return `Branch(${results.join('+')})`;
    }
}

/**
 * The client code works with all of the components via the base interface.
 */
function clientCode(component: Component) {
    // ...

    console.log(`RESULT: ${component.operation()}`);

    // ...
}

/**
 * This way the client code can support the simple leaf components...
 */
const simple = new Leaf();
console.log('Client: I\'ve got a simple component:');
clientCode(simple);
console.log('');

/**
 * ...as well as the complex composites.
 */
const tree = new Composite();
const branch1 = new Composite();
branch1.add(new Leaf());
branch1.add(new Leaf());
const branch2 = new Composite();
branch2.add(new Leaf());
tree.add(branch1);
tree.add(branch2);
console.log('Client: Now I\'ve got a composite tree:');
clientCode(tree);
console.log('');

/**
 * Thanks to the fact that the child-management operations are declared in the
 * base Component class, the client code can work with any component, simple or
 * complex, without depending on their concrete classes.
 */
function clientCode2(component1: Component, component2: Component) {
    // ...

    if (component1.isComposite()) {
        component1.add(component2);
    }
    console.log(`RESULT: ${component1.operation()}`);

    // ...
}

console.log('Client: I don\'t need to check the components classes even when managing the tree:');
clientCode2(tree, simple);

#### **Output.txt:** Execution result

Client: I've got a simple component:
RESULT: Leaf

Client: Now I've got a composite tree:
RESULT: Branch(Branch(Leaf+Leaf)+Branch(Leaf))

Client: I don't need to check the components classes even when managing the tree:
RESULT: Branch(Branch(Leaf+Leaf)+Branch(Leaf)+Leaf)

<!-- source: https://refactoring.guru/design-patterns/decorator/typescript/example -->

# Decorator in TypeScript / Design Patterns

# **Decorator** in TypeScript

**Decorator** is a structural pattern that allows adding new behaviors to objects dynamically by placing them inside special wrapper objects, called _decorators_.

Using decorators you can wrap objects countless number of times since both target objects and decorators follow the same interface. The resulting object will get a stacking behavior of all wrappers.
**Usage examples:** The Decorator is pretty standard in TypeScript code, especially in code related to streams.

**Identification:** Decorator can be recognized by creation methods or constructors that accept objects of the same class or interface as a current class.

## Conceptual Example

This example illustrates the structure of the **Decorator** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The base Component interface defines operations that can be altered by
 * decorators.
 */
interface Component {
    operation(): string;
}

/**
 * Concrete Components provide default implementations of the operations. There
 * might be several variations of these classes.
 */
class ConcreteComponent implements Component {
    public operation(): string {
        return 'ConcreteComponent';
    }
}

/**
 * The base Decorator class follows the same interface as the other components.
 * The primary purpose of this class is to define the wrapping interface for all
 * concrete decorators. The default implementation of the wrapping code might
 * include a field for storing a wrapped component and the means to initialize
 * it.
 */
class Decorator implements Component {
    protected component: Component;

    constructor(component: Component) {
        this.component = component;
    }

    /**
     * The Decorator delegates all work to the wrapped component.
     */
    public operation(): string {
        return this.component.operation();
    }
}

/**
 * Concrete Decorators call the wrapped object and alter its result in some way.
 */
class ConcreteDecoratorA extends Decorator {
    /**
     * Decorators may call parent implementation of the operation, instead of
     * calling the wrapped object directly. This approach simplifies extension
     * of decorator classes.
     */
    public operation(): string {
        return `ConcreteDecoratorA(${super.operation()})`;
    }
}

/**
 * Decorators can execute their behavior either before or after the call to a
 * wrapped object.
 */
class ConcreteDecoratorB extends Decorator {
    public operation(): string {
        return `ConcreteDecoratorB(${super.operation()})`;
    }
}

/**
 * The client code works with all objects using the Component interface. This
 * way it can stay independent of the concrete classes of components it works
 * with.
 */
function clientCode(component: Component) {
    // ...

    console.log(`RESULT: ${component.operation()}`);

    // ...
}

/**
 * This way the client code can support both simple components...
 */
const simple = new ConcreteComponent();
console.log('Client: I\'ve got a simple component:');
clientCode(simple);
console.log('');

/**
 * ...as well as decorated ones.
 *
 * Note how decorators can wrap not only simple components but the other
 * decorators as well.
 */
const decorator1 = new ConcreteDecoratorA(simple);
const decorator2 = new ConcreteDecoratorB(decorator1);
console.log('Client: Now I\'ve got a decorated component:');
clientCode(decorator2);

#### **Output.txt:** Execution result

Client: I've got a simple component:
RESULT: ConcreteComponent

Client: Now I've got a decorated component:
RESULT: ConcreteDecoratorB(ConcreteDecoratorA(ConcreteComponent))

<!-- source: https://refactoring.guru/design-patterns/facade/typescript/example -->

# Facade in TypeScript / Design Patterns

# **Facade** in TypeScript

**Facade** is a structural design pattern that provides a simplified (but limited) interface to a complex system of classes, library or framework.

While Facade decreases the overall complexity of the application, it also helps to move unwanted dependencies to one place.
**Usage examples:** The Facade pattern is commonly used in apps written in TypeScript. It’s especially handy when working with complex libraries and APIs.

**Identification:** Facade can be recognized in a class that has a simple interface, but delegates most of the work to other classes. Usually, facades manage the full life cycle of objects they use.

## Conceptual Example

This example illustrates the structure of the **Facade** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Facade class provides a simple interface to the complex logic of one or
 * several subsystems. The Facade delegates the client requests to the
 * appropriate objects within the subsystem. The Facade is also responsible for
 * managing their lifecycle. All of this shields the client from the undesired
 * complexity of the subsystem.
 */
class Facade {
    protected subsystem1: Subsystem1;

    protected subsystem2: Subsystem2;

    /**
     * Depending on your application's needs, you can provide the Facade with
     * existing subsystem objects or force the Facade to create them on its own.
     */
    constructor(subsystem1?: Subsystem1, subsystem2?: Subsystem2) {
        this.subsystem1 = subsystem1 || new Subsystem1();
        this.subsystem2 = subsystem2 || new Subsystem2();
    }

    /**
     * The Facade's methods are convenient shortcuts to the sophisticated
     * functionality of the subsystems. However, clients get only to a fraction
     * of a subsystem's capabilities.
     */
    public operation(): string {
        let result = 'Facade initializes subsystems:\n';
        result += this.subsystem1.operation1();
        result += this.subsystem2.operation1();
        result += 'Facade orders subsystems to perform the action:\n';
        result += this.subsystem1.operationN();
        result += this.subsystem2.operationZ();

        return result;
    }
}

/**
 * The Subsystem can accept requests either from the facade or client directly.
 * In any case, to the Subsystem, the Facade is yet another client, and it's not
 * a part of the Subsystem.
 */
class Subsystem1 {
    public operation1(): string {
        return 'Subsystem1: Ready!\n';
    }

    // ...

    public operationN(): string {
        return 'Subsystem1: Go!\n';
    }
}

/**
 * Some facades can work with multiple subsystems at the same time.
 */
class Subsystem2 {
    public operation1(): string {
        return 'Subsystem2: Get ready!\n';
    }

    // ...

    public operationZ(): string {
        return 'Subsystem2: Fire!';
    }
}

/**
 * The client code works with complex subsystems through a simple interface
 * provided by the Facade. When a facade manages the lifecycle of the subsystem,
 * the client might not even know about the existence of the subsystem. This
 * approach lets you keep the complexity under control.
 */
function clientCode(facade: Facade) {
    // ...

    console.log(facade.operation());

    // ...
}

/**
 * The client code may have some of the subsystem's objects already created. In
 * this case, it might be worthwhile to initialize the Facade with these objects
 * instead of letting the Facade create new instances.
 */
const subsystem1 = new Subsystem1();
const subsystem2 = new Subsystem2();
const facade = new Facade(subsystem1, subsystem2);
clientCode(facade);

#### **Output.txt:** Execution result

Facade initializes subsystems:
Subsystem1: Ready!
Subsystem2: Get ready!
Facade orders subsystems to perform the action:
Subsystem1: Go!
Subsystem2: Fire!

<!-- source: https://refactoring.guru/design-patterns/flyweight/typescript/example -->

# Flyweight in TypeScript / Design Patterns

# **Flyweight** in TypeScript

**Flyweight** is a structural design pattern that allows programs to support vast quantities of objects by keeping their memory consumption low.

The pattern achieves it by sharing parts of object state between multiple objects. In other words, the Flyweight saves RAM by caching the same data used by different objects.
**Usage examples:** The Flyweight pattern has a single purpose: minimizing memory intake. If your program doesn’t struggle with a shortage of RAM, then you might just ignore this pattern for a while.

**Identification:** Flyweight can be recognized by a creation method that returns cached objects instead of creating new.

## Conceptual Example

This example illustrates the structure of the **Flyweight** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Flyweight stores a common portion of the state (also called intrinsic
 * state) that belongs to multiple real business entities. The Flyweight accepts
 * the rest of the state (extrinsic state, unique for each entity) via its
 * method parameters.
 */
class Flyweight {
    private sharedState: any;

    constructor(sharedState: any) {
        this.sharedState = sharedState;
    }

    public operation(uniqueState): void {
        const s = JSON.stringify(this.sharedState);
        const u = JSON.stringify(uniqueState);
        console.log(`Flyweight: Displaying shared (${s}) and unique (${u}) state.`);
    }
}

/**
 * The Flyweight Factory creates and manages the Flyweight objects. It ensures
 * that flyweights are shared correctly. When the client requests a flyweight,
 * the factory either returns an existing instance or creates a new one, if it
 * doesn't exist yet.
 */
class FlyweightFactory {
    private flyweights: {[key: string]: Flyweight} = <any>{};

    constructor(initialFlyweights: string[][]) {
        for (const state of initialFlyweights) {
            this.flyweights[this.getKey(state)] = new Flyweight(state);
        }
    }

    /**
     * Returns a Flyweight's string hash for a given state.
     */
    private getKey(state: string[]): string {
        return state.join('_');
    }

    /**
     * Returns an existing Flyweight with a given state or creates a new one.
     */
    public getFlyweight(sharedState: string[]): Flyweight {
        const key = this.getKey(sharedState);

        if (!(key in this.flyweights)) {
            console.log('FlyweightFactory: Can\'t find a flyweight, creating new one.');
            this.flyweights[key] = new Flyweight(sharedState);
        } else {
            console.log('FlyweightFactory: Reusing existing flyweight.');
        }

        return this.flyweights[key];
    }

    public listFlyweights(): void {
        const count = Object.keys(this.flyweights).length;
        console.log(`\nFlyweightFactory: I have ${count} flyweights:`);
        for (const key in this.flyweights) {
            console.log(key);
        }
    }
}

/**
 * The client code usually creates a bunch of pre-populated flyweights in the
 * initialization stage of the application.
 */
const factory = new FlyweightFactory([
    ['Chevrolet', 'Camaro2018', 'pink'],
    ['Mercedes Benz', 'C300', 'black'],
    ['Mercedes Benz', 'C500', 'red'],
    ['BMW', 'M5', 'red'],
    ['BMW', 'X6', 'white'],
    // ...
]);
factory.listFlyweights();

// ...

function addCarToPoliceDatabase(
    ff: FlyweightFactory, plates: string, owner: string,
    brand: string, model: string, color: string,
) {
    console.log('\nClient: Adding a car to database.');
    const flyweight = ff.getFlyweight([brand, model, color]);

    // The client code either stores or calculates extrinsic state and passes it
    // to the flyweight's methods.
    flyweight.operation([plates, owner]);
}

addCarToPoliceDatabase(factory, 'CL234IR', 'James Doe', 'BMW', 'M5', 'red');

addCarToPoliceDatabase(factory, 'CL234IR', 'James Doe', 'BMW', 'X1', 'red');

factory.listFlyweights();

#### **Output.txt:** Execution result

FlyweightFactory: I have 5 flyweights:
Chevrolet_Camaro2018_pink
Mercedes Benz_C300_black
Mercedes Benz_C500_red
BMW_M5_red
BMW_X6_white

Client: Adding a car to database.
FlyweightFactory: Reusing existing flyweight.
Flyweight: Displaying shared (["BMW","M5","red"]) and unique (["CL234IR","James Doe"]) state.

Client: Adding a car to database.
FlyweightFactory: Can't find a flyweight, creating new one.
Flyweight: Displaying shared (["BMW","X1","red"]) and unique (["CL234IR","James Doe"]) state.

FlyweightFactory: I have 6 flyweights:
Chevrolet_Camaro2018_pink
Mercedes Benz_C300_black
Mercedes Benz_C500_red
BMW_M5_red
BMW_X6_white
BMW_X1_red

<!-- source: https://refactoring.guru/design-patterns/proxy/typescript/example -->

# Proxy in TypeScript / Design Patterns

# **Proxy** in TypeScript

**Proxy** is a structural design pattern that provides an object that acts as a substitute for a real service object used by a client. A proxy receives client requests, does some work (access control, caching,etc.) and then passes the request to a service object.

The proxy object has the same interface as a service, which makes it interchangeable with a real object when passed to a client.
**Usage examples:** While the Proxy pattern isn’t a frequent guest in most TypeScript applications, it’s still very handy in some special cases. It’s irreplaceable when you want to add some additional behaviors to an object of some existing class without changing the client code.

**Identification:** Proxies delegate all of the real work to some other object. Each proxy method should, in the end, refer to a service object unless the proxy is a subclass of a service.

## Conceptual Example

This example illustrates the structure of the **Proxy** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Subject interface declares common operations for both RealSubject and the
 * Proxy. As long as the client works with RealSubject using this interface,
 * you'll be able to pass it a proxy instead of a real subject.
 */
interface Subject {
    request(): void;
}

/**
 * The RealSubject contains some core business logic. Usually, RealSubjects are
 * capable of doing some useful work which may also be very slow or sensitive -
 * e.g. correcting input data. A Proxy can solve these issues without any
 * changes to the RealSubject's code.
 */
class RealSubject implements Subject {
    public request(): void {
        console.log('RealSubject: Handling request.');
    }
}

/**
 * The Proxy has an interface identical to the RealSubject.
 */
class Proxy implements Subject {
    private realSubject: RealSubject;

    /**
     * The Proxy maintains a reference to an object of the RealSubject class. It
     * can be either lazy-loaded or passed to the Proxy by the client.
     */
    constructor(realSubject: RealSubject) {
        this.realSubject = realSubject;
    }

    /**
     * The most common applications of the Proxy pattern are lazy loading,
     * caching, controlling the access, logging, etc. A Proxy can perform one of
     * these things and then, depending on the result, pass the execution to the
     * same method in a linked RealSubject object.
     */
    public request(): void {
        if (this.checkAccess()) {
            this.realSubject.request();
            this.logAccess();
        }
    }

    private checkAccess(): boolean {
        // Some real checks should go here.
        console.log('Proxy: Checking access prior to firing a real request.');

        return true;
    }

    private logAccess(): void {
        console.log('Proxy: Logging the time of request.');
    }
}

/**
 * The client code is supposed to work with all objects (both subjects and
 * proxies) via the Subject interface in order to support both real subjects and
 * proxies. In real life, however, clients mostly work with their real subjects
 * directly. In this case, to implement the pattern more easily, you can extend
 * your proxy from the real subject's class.
 */
function clientCode(subject: Subject) {
    // ...

    subject.request();

    // ...
}

console.log('Client: Executing the client code with a real subject:');
const realSubject = new RealSubject();
clientCode(realSubject);

console.log('');

console.log('Client: Executing the same client code with a proxy:');
const proxy = new Proxy(realSubject);
clientCode(proxy);

#### **Output.txt:** Execution result

Client: Executing the client code with a real subject:
RealSubject: Handling request.

Client: Executing the same client code with a proxy:
Proxy: Checking access prior to firing a real request.
RealSubject: Handling request.
Proxy: Logging the time of request.

<!-- source: https://refactoring.guru/design-patterns/chain-of-responsibility/typescript/example -->

# Chain of Responsibility in TypeScript / Design Patterns

# **Chain of Responsibility** in TypeScript

**Chain of Responsibility** is behavioral design pattern that allows passing request along the chain of potential handlers until one of them handles request.

The pattern allows multiple objects to handle the request without coupling sender class to the concrete classes of the receivers. The chain can be composed dynamically at runtime with any handler that follows a standard handler interface.
**Usage examples:** The Chain of Responsibility is pretty common in TypeScript. It’s mostly relevant when your code operates with chains of objects, such as filters, event chains,etc.

**Identification:** The pattern is recognizable by behavioral methods of one group of objects that indirectly call the same methods in other objects, while all the objects follow the common interface.

## Conceptual Example

This example illustrates the structure of the **Chain of Responsibility** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Handler interface declares a method for building the chain of handlers.
 * It also declares a method for executing a request.
 */
interface Handler<Request = string, Result = string> {
    setNext(handler: Handler<Request, Result>): Handler<Request, Result>;

    handle(request: Request): Result;
}

/**
 * The default chaining behavior can be implemented inside a base handler class.
 */
abstract class AbstractHandler implements Handler
{
    private nextHandler: Handler;

    public setNext(handler: Handler): Handler {
        this.nextHandler = handler;
        // Returning a handler from here will let us link handlers in a
        // convenient way like this:
        // monkey.setNext(squirrel).setNext(dog);
        return handler;
    }

    public handle(request: string): string {
        if (this.nextHandler) {
            return this.nextHandler.handle(request);
        }

        return null;
    }
}

/**
 * All Concrete Handlers either handle a request or pass it to the next handler
 * in the chain.
 */
class MonkeyHandler extends AbstractHandler {
    public handle(request: string): string {
        if (request === 'Banana') {
            return `Monkey: I'll eat the ${request}.`;
        }
        return super.handle(request);

    }
}

class SquirrelHandler extends AbstractHandler {
    public handle(request: string): string {
        if (request === 'Nut') {
            return `Squirrel: I'll eat the ${request}.`;
        }
        return super.handle(request);
    }
}

class DogHandler extends AbstractHandler {
    public handle(request: string): string {
        if (request === 'MeatBall') {
            return `Dog: I'll eat the ${request}.`;
        }
        return super.handle(request);
    }
}

/**
 * The client code is usually suited to work with a single handler. In most
 * cases, it is not even aware that the handler is part of a chain.
 */
function clientCode(handler: Handler) {
    const foods = ['Nut', 'Banana', 'Cup of coffee'];

    for (const food of foods) {
        console.log(`Client: Who wants a ${food}?`);

        const result = handler.handle(food);
        if (result) {
            console.log(`  ${result}`);
        } else {
            console.log(`  ${food} was left untouched.`);
        }
    }
}

/**
 * The other part of the client code constructs the actual chain.
 */
const monkey = new MonkeyHandler();
const squirrel = new SquirrelHandler();
const dog = new DogHandler();

monkey.setNext(squirrel).setNext(dog);

/**
 * The client should be able to send a request to any handler, not just the
 * first one in the chain.
 */
console.log('Chain: Monkey > Squirrel > Dog\n');
clientCode(monkey);
console.log('');

console.log('Subchain: Squirrel > Dog\n');
clientCode(squirrel);

#### **Output.txt:** Execution result

Chain: Monkey > Squirrel > Dog

Client: Who wants a Nut?
  Squirrel: I'll eat the Nut.
Client: Who wants a Banana?
  Monkey: I'll eat the Banana.
Client: Who wants a Cup of coffee?
  Cup of coffee was left untouched.

Subchain: Squirrel > Dog

Client: Who wants a Nut?
  Squirrel: I'll eat the Nut.
Client: Who wants a Banana?
  Banana was left untouched.
Client: Who wants a Cup of coffee?
  Cup of coffee was left untouched.

<!-- source: https://refactoring.guru/design-patterns/command/typescript/example -->

# Command in TypeScript / Design Patterns

# **Command** in TypeScript

**Command** is behavioral design pattern that converts requests or simple operations into objects.

The conversion allows deferred or remote execution of commands, storing command history,etc.
**Usage examples:** The Command pattern is pretty common in TypeScript code. Most often it’s used as an alternative for callbacks to parameterizing UI elements with actions. It’s also used for queueing tasks, tracking operations history,etc.

**Identification:** The Command pattern is recognizable by behavioral methods in an abstract/interface type (sender) which invokes a method in an implementation of a different abstract/interface type (receiver) which has been encapsulated by the command implementation during its creation. Command classes are usually limited to specific actions.

## Conceptual Example

This example illustrates the structure of the **Command** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Command interface declares a method for executing a command.
 */
interface Command {
    execute(): void;
}

/**
 * Some commands can implement simple operations on their own.
 */
class SimpleCommand implements Command {
    private payload: string;

    constructor(payload: string) {
        this.payload = payload;
    }

    public execute(): void {
        console.log(`SimpleCommand: See, I can do simple things like printing (${this.payload})`);
    }
}

/**
 * However, some commands can delegate more complex operations to other objects,
 * called "receivers."
 */
class ComplexCommand implements Command {
    private receiver: Receiver;

    /**
     * Context data, required for launching the receiver's methods.
     */
    private a: string;

    private b: string;

    /**
     * Complex commands can accept one or several receiver objects along with
     * any context data via the constructor.
     */
    constructor(receiver: Receiver, a: string, b: string) {
        this.receiver = receiver;
        this.a = a;
        this.b = b;
    }

    /**
     * Commands can delegate to any methods of a receiver.
     */
    public execute(): void {
        console.log('ComplexCommand: Complex stuff should be done by a receiver object.');
        this.receiver.doSomething(this.a);
        this.receiver.doSomethingElse(this.b);
    }
}

/**
 * The Receiver classes contain some important business logic. They know how to
 * perform all kinds of operations, associated with carrying out a request. In
 * fact, any class may serve as a Receiver.
 */
class Receiver {
    public doSomething(a: string): void {
        console.log(`Receiver: Working on (${a}.)`);
    }

    public doSomethingElse(b: string): void {
        console.log(`Receiver: Also working on (${b}.)`);
    }
}

/**
 * The Invoker is associated with one or several commands. It sends a request to
 * the command.
 */
class Invoker {
    private onStart: Command;

    private onFinish: Command;

    /**
     * Initialize commands.
     */
    public setOnStart(command: Command): void {
        this.onStart = command;
    }

    public setOnFinish(command: Command): void {
        this.onFinish = command;
    }

    /**
     * The Invoker does not depend on concrete command or receiver classes. The
     * Invoker passes a request to a receiver indirectly, by executing a
     * command.
     */
    public doSomethingImportant(): void {
        console.log('Invoker: Does anybody want something done before I begin?');
        if (this.isCommand(this.onStart)) {
            this.onStart.execute();
        }

        console.log('Invoker: ...doing something really important...');

        console.log('Invoker: Does anybody want something done after I finish?');
        if (this.isCommand(this.onFinish)) {
            this.onFinish.execute();
        }
    }

    private isCommand(object): object is Command {
        return object.execute !== undefined;
    }
}

/**
 * The client code can parameterize an invoker with any commands.
 */
const invoker = new Invoker();
invoker.setOnStart(new SimpleCommand('Say Hi!'));
const receiver = new Receiver();
invoker.setOnFinish(new ComplexCommand(receiver, 'Send email', 'Save report'));

invoker.doSomethingImportant();

#### **Output.txt:** Execution result

Invoker: Does anybody want something done before I begin?
SimpleCommand: See, I can do simple things like printing (Say Hi!)
Invoker: ...doing something really important...
Invoker: Does anybody want something done after I finish?
ComplexCommand: Complex stuff should be done by a receiver object.
Receiver: Working on (Send email.)
Receiver: Also working on (Save report.)

<!-- source: https://refactoring.guru/design-patterns/iterator/typescript/example -->

# Iterator in TypeScript / Design Patterns

# **Iterator** in TypeScript

**Iterator** is a behavioral design pattern that allows sequential traversal through a complex data structure without exposing its internal details.

Thanks to the Iterator, clients can go over elements of different collections in a similar fashion using a single iterator interface.
**Usage examples:** The pattern is very common in TypeScript code. Many frameworks and libraries use it to provide a standard way for traversing their collections.

**Identification:** Iterator is easy to recognize by the navigation methods (such as `next`, `previous` and others). Client code that uses iterators might not have direct access to the collection being traversed.

## Conceptual Example

This example illustrates the structure of the **Iterator** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * Iterator Design Pattern
 *
 * Intent: Lets you traverse elements of a collection without exposing its
 * underlying representation (list, stack, tree, etc.).
 */

interface Iterator<T> {
    // Return the current element.
    current(): T;

    // Return the current element and move forward to next element.
    next(): T;

    // Return the key of the current element.
    key(): number;

    // Checks if current position is valid.
    valid(): boolean;

    // Rewind the Iterator to the first element.
    rewind(): void;
}

interface Aggregator {
    // Retrieve an external iterator.
    getIterator(): Iterator<string>;
}

/**
 * Concrete Iterators implement various traversal algorithms. These classes
 * store the current traversal position at all times.
 */

class AlphabeticalOrderIterator implements Iterator<string> {
    private collection: WordsCollection;

    /**
     * Stores the current traversal position. An iterator may have a lot of
     * other fields for storing iteration state, especially when it is supposed
     * to work with a particular kind of collection.
     */
    private position: number = 0;

    /**
     * This variable indicates the traversal direction.
     */
    private reverse: boolean = false;

    constructor(collection: WordsCollection, reverse: boolean = false) {
        this.collection = collection;
        this.reverse = reverse;

        if (reverse) {
            this.position = collection.getCount() - 1;
        }
    }

    public rewind() {
        this.position = this.reverse ?
            this.collection.getCount() - 1 :
            0;
    }

    public current(): string {
        return this.collection.getItems()[this.position];
    }

    public key(): number {
        return this.position;
    }

    public next(): string {
        const item = this.collection.getItems()[this.position];
        this.position += this.reverse ? -1 : 1;
        return item;
    }

    public valid(): boolean {
        if (this.reverse) {
            return this.position >= 0;
        }

        return this.position < this.collection.getCount();
    }
}

/**
 * Concrete Collections provide one or several methods for retrieving fresh
 * iterator instances, compatible with the collection class.
 */
class WordsCollection implements Aggregator {
    private items: string[] = [];

    public getItems(): string[] {
        return this.items;
    }

    public getCount(): number {
        return this.items.length;
    }

    public addItem(item: string): void {
        this.items.push(item);
    }

    public getIterator(): Iterator<string> {
        return new AlphabeticalOrderIterator(this);
    }

    public getReverseIterator(): Iterator<string> {
        return new AlphabeticalOrderIterator(this, true);
    }
}

/**
 * The client code may or may not know about the Concrete Iterator or Collection
 * classes, depending on the level of indirection you want to keep in your
 * program.
 */
const collection = new WordsCollection();
collection.addItem('First');
collection.addItem('Second');
collection.addItem('Third');

const iterator = collection.getIterator();

console.log('Straight traversal:');
while (iterator.valid()) {
    console.log(iterator.next());
}

console.log('');
console.log('Reverse traversal:');
const reverseIterator = collection.getReverseIterator();
while (reverseIterator.valid()) {
    console.log(reverseIterator.next());
}

#### **Output.txt:** Execution result

Straight traversal:
First
Second
Third

Reverse traversal:
Third
Second
First

<!-- source: https://refactoring.guru/design-patterns/mediator/typescript/example -->

# Mediator in TypeScript / Design Patterns

# **Mediator** in TypeScript

**Mediator** is a behavioral design pattern that reduces coupling between components of a program by making them communicate indirectly, through a special mediator object.

The Mediator makes it easy to modify, extend and reuse individual components because they’re no longer dependent on the dozens of other classes.
**Usage examples:** The most popular usage of the Mediator pattern in TypeScript code is facilitating communications between GUI components of an app. The synonym of the Mediator is the Controller part of MVC pattern.

## Conceptual Example

This example illustrates the structure of the **Mediator** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Mediator interface declares a method used by components to notify the
 * mediator about various events. The Mediator may react to these events and
 * pass the execution to other components.
 */
interface Mediator {
    notify(sender: object, event: string): void;
}

/**
 * Concrete Mediators implement cooperative behavior by coordinating several
 * components.
 */
class ConcreteMediator implements Mediator {
    private component1: Component1;

    private component2: Component2;

    constructor(c1: Component1, c2: Component2) {
        this.component1 = c1;
        this.component1.setMediator(this);
        this.component2 = c2;
        this.component2.setMediator(this);
    }

    public notify(sender: object, event: string): void {
        if (event === 'A') {
            console.log('Mediator reacts on A and triggers following operations:');
            this.component2.doC();
        }

        if (event === 'D') {
            console.log('Mediator reacts on D and triggers following operations:');
            this.component1.doB();
            this.component2.doC();
        }
    }
}

/**
 * The Base Component provides the basic functionality of storing a mediator's
 * instance inside component objects.
 */
class BaseComponent {
    protected mediator: Mediator;

    constructor(mediator?: Mediator) {
        this.mediator = mediator!;
    }

    public setMediator(mediator: Mediator): void {
        this.mediator = mediator;
    }
}

/**
 * Concrete Components implement various functionality. They don't depend on
 * other components. They also don't depend on any concrete mediator classes.
 */
class Component1 extends BaseComponent {
    public doA(): void {
        console.log('Component 1 does A.');
        this.mediator.notify(this, 'A');
    }

    public doB(): void {
        console.log('Component 1 does B.');
        this.mediator.notify(this, 'B');
    }
}

class Component2 extends BaseComponent {
    public doC(): void {
        console.log('Component 2 does C.');
        this.mediator.notify(this, 'C');
    }

    public doD(): void {
        console.log('Component 2 does D.');
        this.mediator.notify(this, 'D');
    }
}

/**
 * The client code.
 */
const c1 = new Component1();
const c2 = new Component2();
const mediator = new ConcreteMediator(c1, c2);

console.log('Client triggers operation A.');
c1.doA();

console.log('');
console.log('Client triggers operation D.');
c2.doD();

#### **Output.txt:** Execution result

Client triggers operation A.
Component 1 does A.
Mediator reacts on A and triggers following operations:
Component 2 does C.

Client triggers operation D.
Component 2 does D.
Mediator reacts on D and triggers following operations:
Component 1 does B.
Component 2 does C.

<!-- source: https://refactoring.guru/design-patterns/memento/typescript/example -->

# Memento in TypeScript / Design Patterns

# **Memento** in TypeScript

**Memento** is a behavioral design pattern that allows making snapshots of an object’s state and restoring it in future.

The Memento doesn’t compromise the internal structure of the object it works with, as well as data kept inside the snapshots.
**Usage examples:** The Memento’s principle can be achieved using serialization, which is quite common in TypeScript. While it’s not the only and the most efficient way to make snapshots of an object’s state, it still allows storing state backups while protecting the originator’s structure from other objects.

## Conceptual Example

This example illustrates the structure of the **Memento** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Originator holds some important state that may change over time. It also
 * defines a method for saving the state inside a memento and another method for
 * restoring the state from it.
 */
class Originator {
    /**
     * For the sake of simplicity, the originator's state is stored inside a
     * single variable.
     */
    private state: string;

    constructor(state: string) {
        this.state = state;
        console.log(`Originator: My initial state is: ${state}`);
    }

    /**
     * The Originator's business logic may affect its internal state. Therefore,
     * the client should backup the state before launching methods of the
     * business logic via the save() method.
     */
    public doSomething(): void {
        console.log('Originator: I\'m doing something important.');
        this.state = this.generateRandomString(30);
        console.log(`Originator: and my state has changed to: ${this.state}`);
    }

    private generateRandomString(length: number = 10): string {
        const charSet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';

        return Array
            .apply(null, { length })
            .map(() => charSet.charAt(Math.floor(Math.random() * charSet.length)))
            .join('');
    }

    /**
     * Saves the current state inside a memento.
     */
    public save(): Memento {
        return new ConcreteMemento(this.state);
    }

    /**
     * Restores the Originator's state from a memento object.
     */
    public restore(memento: Memento): void {
        this.state = memento.getState();
        console.log(`Originator: My state has changed to: ${this.state}`);
    }
}

/**
 * The Memento interface provides a way to retrieve the memento's metadata, such
 * as creation date or name. However, it doesn't expose the Originator's state.
 */
interface Memento {
    getState(): string;

    getName(): string;

    getDate(): string;
}

/**
 * The Concrete Memento contains the infrastructure for storing the Originator's
 * state.
 */
class ConcreteMemento implements Memento {
    private state: string;

    private date: string;

    constructor(state: string) {
        this.state = state;
        this.date = new Date().toISOString().slice(0, 19).replace('T', ' ');
    }

    /**
     * The Originator uses this method when restoring its state.
     */
    public getState(): string {
        return this.state;
    }

    /**
     * The rest of the methods are used by the Caretaker to display metadata.
     */
    public getName(): string {
        return `${this.date} / (${this.state.substr(0, 9)}...)`;
    }

    public getDate(): string {
        return this.date;
    }
}

/**
 * The Caretaker doesn't depend on the Concrete Memento class. Therefore, it
 * doesn't have access to the originator's state, stored inside the memento. It
 * works with all mementos via the base Memento interface.
 */
class Caretaker {
    private mementos: Memento[] = [];

    private originator: Originator;

    constructor(originator: Originator) {
        this.originator = originator;
    }

    public backup(): void {
        console.log('\nCaretaker: Saving Originator\'s state...');
        this.mementos.push(this.originator.save());
    }

    public undo(): void {
        if (!this.mementos.length) {
            return;
        }
        const memento = this.mementos.pop();

        console.log(`Caretaker: Restoring state to: ${memento.getName()}`);
        this.originator.restore(memento);
    }

    public showHistory(): void {
        console.log('Caretaker: Here\'s the list of mementos:');
        for (const memento of this.mementos) {
            console.log(memento.getName());
        }
    }
}

/**
 * Client code.
 */
const originator = new Originator('Super-duper-super-puper-super.');
const caretaker = new Caretaker(originator);

caretaker.backup();
originator.doSomething();

caretaker.backup();
originator.doSomething();

caretaker.backup();
originator.doSomething();

console.log('');
caretaker.showHistory();

console.log('\nClient: Now, let\'s rollback!\n');
caretaker.undo();

console.log('\nClient: Once more!\n');
caretaker.undo();

#### **Output.txt:** Execution result

Originator: My initial state is: Super-duper-super-puper-super.

Caretaker: Saving Originator's state...
Originator: I'm doing something important.
Originator: and my state has changed to: qXqxgTcLSCeLYdcgElOghOFhPGfMxo

Caretaker: Saving Originator's state...
Originator: I'm doing something important.
Originator: and my state has changed to: iaVCJVryJwWwbipieensfodeMSWvUY

Caretaker: Saving Originator's state...
Originator: I'm doing something important.
Originator: and my state has changed to: oSUxsOCiZEnohBMQEjwnPWJLGnwGmy

Caretaker: Here's the list of mementos:
2019-02-17 15:14:05 / (Super-dup...)
2019-02-17 15:14:05 / (qXqxgTcLS...)
2019-02-17 15:14:05 / (iaVCJVryJ...)

Client: Now, let's rollback!

Caretaker: Restoring state to: 2019-02-17 15:14:05 / (iaVCJVryJ...)
Originator: My state has changed to: iaVCJVryJwWwbipieensfodeMSWvUY

Client: Once more!

Caretaker: Restoring state to: 2019-02-17 15:14:05 / (qXqxgTcLS...)
Originator: My state has changed to: qXqxgTcLSCeLYdcgElOghOFhPGfMxo

<!-- source: https://refactoring.guru/design-patterns/observer/typescript/example -->

# Observer in TypeScript / Design Patterns

# **Observer** in TypeScript

**Observer** is a behavioral design pattern that allows some objects to notify other objects about changes in their state.

The Observer pattern provides a way to subscribe and unsubscribe to and from these events for any object that implements a subscriber interface.
**Usage examples:** The Observer pattern is pretty common in TypeScript code, especially in the GUI components. It provides a way to react to events happening in other objects without coupling to their classes.

**Identification:** The pattern can be recognized by subscription methods, that store objects in a list and by calls to the update method issued to objects in that list.

## Conceptual Example

This example illustrates the structure of the **Observer** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Subject interface declares a set of methods for managing subscribers.
 */
interface Subject {
    // Attach an observer to the subject.
    attach(observer: Observer): void;

    // Detach an observer from the subject.
    detach(observer: Observer): void;

    // Notify all observers about an event.
    notify(): void;
}

/**
 * The Subject owns some important state and notifies observers when the state
 * changes.
 */
class ConcreteSubject implements Subject {
    /**
     * @type {number} For the sake of simplicity, the Subject's state, essential
     * to all subscribers, is stored in this variable.
     */
    public state: number;

    /**
     * @type {Observer[]} List of subscribers. In real life, the list of
     * subscribers can be stored more comprehensively (categorized by event
     * type, etc.).
     */
    private observers: Observer[] = [];

    /**
     * The subscription management methods.
     */
    public attach(observer: Observer): void {
        const isExist = this.observers.includes(observer);
        if (isExist) {
            return console.log('Subject: Observer has been attached already.');
        }

        console.log('Subject: Attached an observer.');
        this.observers.push(observer);
    }

    public detach(observer: Observer): void {
        const observerIndex = this.observers.indexOf(observer);
        if (observerIndex === -1) {
            return console.log('Subject: Nonexistent observer.');
        }

        this.observers.splice(observerIndex, 1);
        console.log('Subject: Detached an observer.');
    }

    /**
     * Trigger an update in each subscriber.
     */
    public notify(): void {
        console.log('Subject: Notifying observers...');
        for (const observer of this.observers) {
            observer.update(this);
        }
    }

    /**
     * Usually, the subscription logic is only a fraction of what a Subject can
     * really do. Subjects commonly hold some important business logic, that
     * triggers a notification method whenever something important is about to
     * happen (or after it).
     */
    public someBusinessLogic(): void {
        console.log('\nSubject: I\'m doing something important.');
        this.state = Math.floor(Math.random() * (10 + 1));

        console.log(`Subject: My state has just changed to: ${this.state}`);
        this.notify();
    }
}

/**
 * The Observer interface declares the update method, used by subjects.
 */
interface Observer {
    // Receive update from subject.
    update(subject: Subject): void;
}

/**
 * Concrete Observers react to the updates issued by the Subject they had been
 * attached to.
 */
class ConcreteObserverA implements Observer {
    public update(subject: Subject): void {
        if (subject instanceof ConcreteSubject && subject.state < 3) {
            console.log('ConcreteObserverA: Reacted to the event.');
        }
    }
}

class ConcreteObserverB implements Observer {
    public update(subject: Subject): void {
        if (subject instanceof ConcreteSubject && (subject.state === 0 || subject.state >= 2)) {
            console.log('ConcreteObserverB: Reacted to the event.');
        }
    }
}

/**
 * The client code.
 */

const subject = new ConcreteSubject();

const observer1 = new ConcreteObserverA();
subject.attach(observer1);

const observer2 = new ConcreteObserverB();
subject.attach(observer2);

subject.someBusinessLogic();
subject.someBusinessLogic();

subject.detach(observer2);

subject.someBusinessLogic();

#### **Output.txt:** Execution result

Subject: Attached an observer.
Subject: Attached an observer.

Subject: I'm doing something important.
Subject: My state has just changed to: 6
Subject: Notifying observers...
ConcreteObserverB: Reacted to the event.

Subject: I'm doing something important.
Subject: My state has just changed to: 1
Subject: Notifying observers...
ConcreteObserverA: Reacted to the event.
Subject: Detached an observer.

Subject: I'm doing something important.
Subject: My state has just changed to: 5
Subject: Notifying observers...

<!-- source: https://refactoring.guru/design-patterns/state/typescript/example -->

# State in TypeScript / Design Patterns

# **State** in TypeScript

**State** is a behavioral design pattern that allows an object to change the behavior when its internal state changes.

The pattern extracts state-related behaviors into separate state classes and forces the original object to delegate the work to an instance of these classes, instead of acting on its own.
**Usage examples:** The State pattern is commonly used in TypeScript to convert massive `switch`-base state machines into objects.

**Identification:** State pattern can be recognized by methods that change their behavior depending on the objects’ state, controlled externally.

## Conceptual Example

This example illustrates the structure of the **State** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Context defines the interface of interest to clients. It also maintains a
 * reference to an instance of a State subclass, which represents the current
 * state of the Context.
 */
class Context {
    /**
     * @type {State} A reference to the current state of the Context.
     */
    private state: State;

    constructor(state: State) {
        this.transitionTo(state);
    }

    /**
     * The Context allows changing the State object at runtime.
     */
    public transitionTo(state: State): void {
        console.log(`Context: Transition to ${(<any>state).constructor.name}.`);
        this.state = state;
        this.state.setContext(this);
    }

    /**
     * The Context delegates part of its behavior to the current State object.
     */
    public request1(): void {
        this.state.handle1();
    }

    public request2(): void {
        this.state.handle2();
    }
}

/**
 * The base State class declares methods that all Concrete State should
 * implement and also provides a backreference to the Context object, associated
 * with the State. This backreference can be used by States to transition the
 * Context to another State.
 */
abstract class State {
    protected context: Context;

    public setContext(context: Context) {
        this.context = context;
    }

    public abstract handle1(): void;

    public abstract handle2(): void;
}

/**
 * Concrete States implement various behaviors, associated with a state of the
 * Context.
 */
class ConcreteStateA extends State {
    public handle1(): void {
        console.log('ConcreteStateA handles request1.');
        console.log('ConcreteStateA wants to change the state of the context.');
        this.context.transitionTo(new ConcreteStateB());
    }

    public handle2(): void {
        console.log('ConcreteStateA handles request2.');
    }
}

class ConcreteStateB extends State {
    public handle1(): void {
        console.log('ConcreteStateB handles request1.');
    }

    public handle2(): void {
        console.log('ConcreteStateB handles request2.');
        console.log('ConcreteStateB wants to change the state of the context.');
        this.context.transitionTo(new ConcreteStateA());
    }
}

/**
 * The client code.
 */
const context = new Context(new ConcreteStateA());
context.request1();
context.request2();

#### **Output.txt:** Execution result

Context: Transition to ConcreteStateA.
ConcreteStateA handles request1.
ConcreteStateA wants to change the state of the context.
Context: Transition to ConcreteStateB.
ConcreteStateB handles request2.
ConcreteStateB wants to change the state of the context.
Context: Transition to ConcreteStateA.

<!-- source: https://refactoring.guru/design-patterns/strategy/typescript/example -->

# Strategy in TypeScript / Design Patterns

# **Strategy** in TypeScript

**Strategy** is a behavioral design pattern that turns a set of behaviors into objects and makes them interchangeable inside original context object.

The original object, called context, holds a reference to a strategy object. The context delegates executing the behavior to the linked strategy object. In order to change the way the context performs its work, other objects may replace the currently linked strategy object with another one.
**Usage examples:** The Strategy pattern is very common in TypeScript code. It’s often used in various frameworks to provide users a way to change the behavior of a class without extending it.

**Identification:** Strategy pattern can be recognized by a method that lets a nested object do the actual work, as well as a setter that allows replacing that object with a different one.

## Conceptual Example

This example illustrates the structure of the **Strategy** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Context defines the interface of interest to clients.
 */
class Context {
    /**
     * @type {Strategy} The Context maintains a reference to one of the Strategy
     * objects. The Context does not know the concrete class of a strategy. It
     * should work with all strategies via the Strategy interface.
     */
    private strategy: Strategy;

    /**
     * Usually, the Context accepts a strategy through the constructor, but also
     * provides a setter to change it at runtime.
     */
    constructor(strategy: Strategy) {
        this.strategy = strategy;
    }

    /**
     * Usually, the Context allows replacing a Strategy object at runtime.
     */
    public setStrategy(strategy: Strategy) {
        this.strategy = strategy;
    }

    /**
     * The Context delegates some work to the Strategy object instead of
     * implementing multiple versions of the algorithm on its own.
     */
    public doSomeBusinessLogic(): void {
        // ...

        console.log('Context: Sorting data using the strategy (not sure how it\'ll do it)');
        const result = this.strategy.doAlgorithm(['a', 'b', 'c', 'd', 'e']);
        console.log(result.join(','));

        // ...
    }
}

/**
 * The Strategy interface declares operations common to all supported versions
 * of some algorithm.
 *
 * The Context uses this interface to call the algorithm defined by Concrete
 * Strategies.
 */
interface Strategy {
    doAlgorithm(data: string[]): string[];
}

/**
 * Concrete Strategies implement the algorithm while following the base Strategy
 * interface. The interface makes them interchangeable in the Context.
 */
class ConcreteStrategyA implements Strategy {
    public doAlgorithm(data: string[]): string[] {
        return data.sort();
    }
}

class ConcreteStrategyB implements Strategy {
    public doAlgorithm(data: string[]): string[] {
        return data.reverse();
    }
}

/**
 * The client code picks a concrete strategy and passes it to the context. The
 * client should be aware of the differences between strategies in order to make
 * the right choice.
 */
const context = new Context(new ConcreteStrategyA());
console.log('Client: Strategy is set to normal sorting.');
context.doSomeBusinessLogic();

console.log('');

console.log('Client: Strategy is set to reverse sorting.');
context.setStrategy(new ConcreteStrategyB());
context.doSomeBusinessLogic();

#### **Output.txt:** Execution result

Client: Strategy is set to normal sorting.
Context: Sorting data using the strategy (not sure how it'll do it)
a,b,c,d,e

Client: Strategy is set to reverse sorting.
Context: Sorting data using the strategy (not sure how it'll do it)
e,d,c,b,a

<!-- source: https://refactoring.guru/design-patterns/template-method/typescript/example -->

# Template Method in TypeScript / Design Patterns

# **Template Method** in TypeScript

**Template Method** is a behavioral design pattern that allows you to define a skeleton of an algorithm in a base class and let subclasses override the steps without changing the overall algorithm’s structure.
**Usage examples:** The Template Method pattern is quite common in TypeScript frameworks. Developers often use it to provide framework users with a simple means of extending standard functionality using inheritance.

**Identification:** Template Method can be recognized if you see a method in base class that calls a bunch of other methods that are either abstract or empty.

## Conceptual Example

This example illustrates the structure of the **Template Method** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Abstract Class defines a template method that contains a skeleton of some
 * algorithm, composed of calls to (usually) abstract primitive operations.
 *
 * Concrete subclasses should implement these operations, but leave the template
 * method itself intact.
 */
abstract class AbstractClass {
    /**
     * The template method defines the skeleton of an algorithm.
     */
    public templateMethod(): void {
        this.baseOperation1();
        this.requiredOperations1();
        this.baseOperation2();
        this.hook1();
        this.requiredOperation2();
        this.baseOperation3();
        this.hook2();
    }

    /**
     * These operations already have implementations.
     */
    protected baseOperation1(): void {
        console.log('AbstractClass says: I am doing the bulk of the work');
    }

    protected baseOperation2(): void {
        console.log('AbstractClass says: But I let subclasses override some operations');
    }

    protected baseOperation3(): void {
        console.log('AbstractClass says: But I am doing the bulk of the work anyway');
    }

    /**
     * These operations have to be implemented in subclasses.
     */
    protected abstract requiredOperations1(): void;

    protected abstract requiredOperation2(): void;

    /**
     * These are "hooks." Subclasses may override them, but it's not mandatory
     * since the hooks already have default (but empty) implementation. Hooks
     * provide additional extension points in some crucial places of the
     * algorithm.
     */
    protected hook1(): void { }

    protected hook2(): void { }
}

/**
 * Concrete classes have to implement all abstract operations of the base class.
 * They can also override some operations with a default implementation.
 */
class ConcreteClass1 extends AbstractClass {
    protected requiredOperations1(): void {
        console.log('ConcreteClass1 says: Implemented Operation1');
    }

    protected requiredOperation2(): void {
        console.log('ConcreteClass1 says: Implemented Operation2');
    }
}

/**
 * Usually, concrete classes override only a fraction of base class' operations.
 */
class ConcreteClass2 extends AbstractClass {
    protected requiredOperations1(): void {
        console.log('ConcreteClass2 says: Implemented Operation1');
    }

    protected requiredOperation2(): void {
        console.log('ConcreteClass2 says: Implemented Operation2');
    }

    protected hook1(): void {
        console.log('ConcreteClass2 says: Overridden Hook1');
    }
}

/**
 * The client code calls the template method to execute the algorithm. Client
 * code does not have to know the concrete class of an object it works with, as
 * long as it works with objects through the interface of their base class.
 */
function clientCode(abstractClass: AbstractClass) {
    // ...
    abstractClass.templateMethod();
    // ...
}

console.log('Same client code can work with different subclasses:');
clientCode(new ConcreteClass1());
console.log('');

console.log('Same client code can work with different subclasses:');
clientCode(new ConcreteClass2());

#### **Output.txt:** Execution result

Same client code can work with different subclasses:
AbstractClass says: I am doing the bulk of the work
ConcreteClass1 says: Implemented Operation1
AbstractClass says: But I let subclasses override some operations
ConcreteClass1 says: Implemented Operation2
AbstractClass says: But I am doing the bulk of the work anyway

Same client code can work with different subclasses:
AbstractClass says: I am doing the bulk of the work
ConcreteClass2 says: Implemented Operation1
AbstractClass says: But I let subclasses override some operations
ConcreteClass2 says: Overridden Hook1
ConcreteClass2 says: Implemented Operation2
AbstractClass says: But I am doing the bulk of the work anyway

<!-- source: https://refactoring.guru/design-patterns/visitor/typescript/example -->

# Visitor in TypeScript / Design Patterns

# **Visitor** in TypeScript

**Visitor** is a behavioral design pattern that allows adding new behaviors to existing class hierarchy without altering any existing code.

> Read why Visitors can’t be simply replaced with method overloading in our article [Visitor and Double Dispatch](https://refactoring.guru/design-patterns/visitor-double-dispatch).
**Usage examples:** Visitor isn’t a very common pattern because of its complexity and narrow applicability.

## Conceptual Example

This example illustrates the structure of the **Visitor** design pattern and focuses on the following questions:

*   What classes does it consist of?
*   What roles do these classes play?
*   In what way the elements of the pattern are related?

#### **index.ts:** Conceptual example

/**
 * The Component interface declares an `accept` method that should take the base
 * visitor interface as an argument.
 */
interface Component {
    accept(visitor: Visitor): void;
}

/**
 * Each Concrete Component must implement the `accept` method in such a way that
 * it calls the visitor's method corresponding to the component's class.
 */
class ConcreteComponentA implements Component {
    /**
     * Note that we're calling `visitConcreteComponentA`, which matches the
     * current class name. This way we let the visitor know the class of the
     * component it works with.
     */
    public accept(visitor: Visitor): void {
        visitor.visitConcreteComponentA(this);
    }

    /**
     * Concrete Components may have special methods that don't exist in their
     * base class or interface. The Visitor is still able to use these methods
     * since it's aware of the component's concrete class.
     */
    public exclusiveMethodOfConcreteComponentA(): string {
        return 'A';
    }
}

class ConcreteComponentB implements Component {
    /**
     * Same here: visitConcreteComponentB => ConcreteComponentB
     */
    public accept(visitor: Visitor): void {
        visitor.visitConcreteComponentB(this);
    }

    public specialMethodOfConcreteComponentB(): string {
        return 'B';
    }
}

/**
 * The Visitor Interface declares a set of visiting methods that correspond to
 * component classes. The signature of a visiting method allows the visitor to
 * identify the exact class of the component that it's dealing with.
 */
interface Visitor {
    visitConcreteComponentA(element: ConcreteComponentA): void;

    visitConcreteComponentB(element: ConcreteComponentB): void;
}

/**
 * Concrete Visitors implement several versions of the same algorithm, which can
 * work with all concrete component classes.
 *
 * You can experience the biggest benefit of the Visitor pattern when using it
 * with a complex object structure, such as a Composite tree. In this case, it
 * might be helpful to store some intermediate state of the algorithm while
 * executing visitor's methods over various objects of the structure.
 */
class ConcreteVisitor1 implements Visitor {
    public visitConcreteComponentA(element: ConcreteComponentA): void {
        console.log(`${element.exclusiveMethodOfConcreteComponentA()} + ConcreteVisitor1`);
    }

    public visitConcreteComponentB(element: ConcreteComponentB): void {
        console.log(`${element.specialMethodOfConcreteComponentB()} + ConcreteVisitor1`);
    }
}

class ConcreteVisitor2 implements Visitor {
    public visitConcreteComponentA(element: ConcreteComponentA): void {
        console.log(`${element.exclusiveMethodOfConcreteComponentA()} + ConcreteVisitor2`);
    }

    public visitConcreteComponentB(element: ConcreteComponentB): void {
        console.log(`${element.specialMethodOfConcreteComponentB()} + ConcreteVisitor2`);
    }
}

/**
 * The client code can run visitor operations over any set of elements without
 * figuring out their concrete classes. The accept operation directs a call to
 * the appropriate operation in the visitor object.
 */
function clientCode(components: Component[], visitor: Visitor) {
    // ...
    for (const component of components) {
        component.accept(visitor);
    }
    // ...
}

const components = [
    new ConcreteComponentA(),
    new ConcreteComponentB(),
];

console.log('The client code works with all visitors via the base Visitor interface:');
const visitor1 = new ConcreteVisitor1();
clientCode(components, visitor1);
console.log('');

console.log('It allows the same client code to work with different types of visitors:');
const visitor2 = new ConcreteVisitor2();
clientCode(components, visitor2);

#### **Output.txt:** Execution result

The client code works with all visitors via the base Visitor interface:
A + ConcreteVisitor1
B + ConcreteVisitor1

It allows the same client code to work with different types of visitors:
A + ConcreteVisitor2
B + ConcreteVisitor2

#### Return

[Template Method in TypeScript](https://refactoring.guru/design-patterns/template-method/typescript/example)
