# closure-over-class

Build components from closures returning plain objects instead of classes, avoiding prototypes, unbound methods and layered lifetimes.

**Sources:** P:systemic-2-closure-over-class, P:complication-2-class-prototype, P:complication-3-class-unbound-methods, P:complication-4-class-layered-lifetime

---

## Systemic 2 Closure Over Class (P:systemic-2-closure-over-class)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/systemic-2-closure-over-class), copyright the author, redistributed with attribution.

_[Objects are poor man's closures.](https://wiki.c2.com/?ClosuresAndObjectsAreEquivalent) (Or is it [closures that are poor man's objects](https://people.csail.mit.edu/gregs/ll1-discuss-archive-html/msg03277.html) because OOP folks tend to be paid higher salaries?)_

The above alludes that classes and closures, although originating from different schools (OOP and FP respectively), fulfill a similar purpose. However, the link above talked about classes and closures at the beginning of the formulation of OOP and FP.

Nowadays, closures and classes take more advanced forms---improved by more years of language design experience and feedback from the community. And it is pretty interesting that JavaScript and TypeScript have support for [closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures) and [class](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes).

I am biased toward closure, because, in my experience, class [does not scale as well with complexity](https://valand.dev/systemic-ts/prelude-2-inherent-complexity).

You may think that I came from the background of FP due to my bias, but that cannot be further from the truth. I was molded by OOP, class, methods, etc. My discovery of closures being easier to manage a significant complexity came from experience, necessity, and limitations of resources.

### Closure

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

#### Parameters

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

#### Async Construction

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

#### Async Inner Periodical Task

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

#### Method VS Static Method VS Orphan Function

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

#### Lifetime Separation

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

### When To Use Class? Distinguish Pure Data VS Actor

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

#### Using the performance of class

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

#### Optimizing Closure (Or rather, figuring out why the former does not perform well)

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


## Complication 2 Class Prototype (P:complication-2-class-prototype)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/complication-2-class-prototype), copyright the author, redistributed with attribution.

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


## Complication 3 Class Unbound Methods (P:complication-3-class-unbound-methods)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/complication-3-class-unbound-methods), copyright the author, redistributed with attribution.

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


## Complication 4 Class Layered Lifetime (P:complication-4-class-layered-lifetime)

[Systemic TypeScript by Vincent Alandev (valand.dev)](https://valand.dev/systemic-ts/complication-4-class-layered-lifetime), copyright the author, redistributed with attribution.

This is the third time `class` has been problematic. But now `prototype` is not involved. The syntax itself is making it hard to do refactoring with it, especially when layered `lifetime` is involved.

_Did you just make up a new word?_

### Yes. Layered Lifetime, I Just Made Up That Phrase

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

### Lifetime and Type's Interesting Relationship

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

### Too Many Lines Of Codes

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
