# throwless

Return typed results (unions of value and known error) instead of throwing, for systems with known failure modes; this departs from rule `throw-errors`, so adopt it only project-wide.

**Sources:** P:systemic-1-known-vs-unknown-error-throwless, P:complication-1-throw

---

## Systemic 1 Known Vs Unknown Error Throwless (P:systemic-1-known-vs-unknown-error-throwless)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/systemic-1-known-vs-unknown-error-throwless), copyright the author, redistributed with attribution.

This is only the solution's first sentence and yet I decree probably one of the most radical and controversial approaches in programming: **get rid of `throw`**.

"How can you communicate errors then?" you might say.

The answer: [`return`](https://en.wikipedia.org/wiki/Return_statement) and [`union`](https://en.wikipedia.org/wiki/Union_type)!

But before that, take a detour into the philosophical consideration of this approach.

### Known vs Unknown Errors

Unknown errors are, literally, unknown. Unknown's core essence involves you not knowing if it exists. If it exists at all, you have not identify what, how, when, or where it will happen.

Happening upon a previously unknown error is mystifying and often stressful. Understanding an error is dialectic, but it is only powerful if the knowledge is preserved so that someone in the future benefits from it.

Known errors are errors that you have encountered and those you have decided to not forget. An error becomes truly known when it is [signified](https://en.wikipedia.org/wiki/Sign_(semiotics)) (e.g. by being written as code).

It also makes no sense to blur a known error, particularly of when it happens. Therefore, `throwing` it is not a choice because it blurs the timing aspect of an error.

Managing knowledge of errors and communicating it are two entangled problems. Therefore, I present a solution that solves both: **The Throwless Pact**.

### The Throwless Pact

The pact's core tenets are:

*   Known errors within the codebase are well-[signified](https://en.wikipedia.org/wiki/Sign_(semiotics)) as a uniquely identified type.
*   Known errors and successes are communicated and signified as a [`returned`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/return) tagged [`union`](https://www.typescriptlang.org/docs/handbook/unions-and-intersections.html).
*   Thrown errors from outside the codebase (e.g. those thrown by third-party dependencies) are caught and converted into a `union` as early as possible.
*   Only unknown errors may be thrown, convert them once identified

What we want from this is, first, transparent and immediate information about a function's behavior in the form of [signature](https://www.typescriptlang.org/docs/handbook/2/functions.html#call-signatures). One that explies all result variants and implies all possibilities within.

With all possibilities implied, you will need less to look into the function's implementation detail. This very effectively combats [the try-catch anxiety when throws exist in a codebase](https://valand.dev/systemic-ts/complication-1-throw). As a result, the whole development process needs less cognitive burden so there is cognitive space for thinking at a higher-level.

Of course, the direct impact of not having `throw` is the robust and reliable appearance. In a React application, for example, `throw` triggers a crash. Even if caught with an [ErrorBoundary](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary) it does not beat the elegant facade of an application that does not throw.

Overall, you will be able to trust your code more.

### The Implementation

Now we will see how The Throwless Pact efficiently implements a growing requirement. We will compare the added values and also the extra price we have to pay (e.g. line of code, bootstrap code) for going against the grain. Usually, the bigger the codebase, the more the added values justify the extra price.

In this section, I will use my preferred tools/libraries. However, it should not prevent you from using other tools that achieve a similar purpose.

#### Return Communication

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

#### Error Signification

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

#### Applying The Arsenal

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

#### Exception

_Update 2023-10-16_

See the acceptable `throw` section in [this article](https://valand.dev/systemic-ts/complication-1-throw)


## Complication 1 Throw (P:complication-1-throw)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/complication-1-throw), copyright the author, redistributed with attribution.

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
