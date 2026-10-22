# document-exports

Document every exported symbol and any member whose purpose isn't obvious; describe methods with a third-person verb phrase; add `@param`/`@return` only when they add information beyond names and types (`@param` documents parameter properties); put JSDoc before decorators.

**Why:** Docs should say what the signature can't.

**Sources:** G:document-all-top-level-exports-of-modules, G:jsdoc-class-comments, G:method-and-function-comments, G:parameter-property-comments, G:redundant-comments, G:place-documentation-prior-to-decorators

---

## Document all top-level exports of modules (G:document-all-top-level-exports-of-modules)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#document-all-top-level-exports-of-modules), CC BY 3.0.

Use `/** JSDoc */` comments to communicate information to the users of your code. Avoid merely restating the property or parameter name. You _should_ also document all properties and methods (exported/public or not) whose purpose is not immediately obvious from their name, as judged by your reviewer.

**Exception:** Symbols that are only exported to be consumed by tooling, such as @NgModule classes, do not require comments.


## Class comments (G:jsdoc-class-comments)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#jsdoc-class-comments), CC BY 3.0.

JSDoc comments for classes should provide the reader with enough information to know how and when to use the class, as well as any additional considerations necessary to correctly use the class. Textual descriptions may be omitted on the constructor.


## Method and function comments (G:method-and-function-comments)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#method-and-function-comments), CC BY 3.0.

Method, parameter, and return descriptions may be omitted if they are obvious from the rest of the method’s JSDoc or from the method name and type signature.

Method descriptions begin with a verb phrase that describes what the method does. This phrase is not an imperative sentence, but instead is written in the third person, as if there is an implied This method ... before it.


## Parameter property comments (G:parameter-property-comments)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#parameter-property-comments), CC BY 3.0.

A [parameter property](https://www.typescriptlang.org/docs/handbook/2/classes.html#parameter-properties) is a constructor parameter that is prefixed by one of the modifiers `private`, `protected`, `public`, or `readonly`. A parameter property declares both a parameter and an instance property, and implicitly assigns into it. For example, `constructor(private readonly foo: Foo)`, declares that the constructor takes a parameter `foo`, but also declares a private readonly property `foo`, and assigns the parameter into that property before executing the remainder of the constructor.

To document these fields, use JSDoc's `@param` annotation. Editors display the description on constructor calls and property accesses.

✅ Good:

```ts
/** This class demonstrates how parameter properties are documented. */
class ParamProps {
  /**
   * @param percolator The percolator used for brewing.
   * @param beans The beans to brew.
   */
  constructor(
    private readonly percolator: Percolator,
    private readonly beans: CoffeeBean[]) {}
}
```

✅ Good:

```ts
/** This class demonstrates how ordinary fields are documented. */
class OrdinaryClass {
  /** The bean that will be used in the next call to brew(). */
  nextBean: CoffeeBean;

  constructor(initialBean: CoffeeBean) {
    this.nextBean = initialBean;
  }
}
```


## Make comments that actually add information (G:redundant-comments)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#redundant-comments), CC BY 3.0.

For non-exported symbols, sometimes the name and type of the function or parameter is enough. Code will _usually_ benefit from more documentation than just variable names though!

*   Avoid comments that just restate the parameter name and type, e.g.

    ❌ Bad:

    ```ts
    /** @param fooBarService The Bar service for the Foo application. */
    ```

*   Because of this rule, `@param` and `@return` lines are only required when they add information, and _may_ otherwise be omitted.

    ✅ Good:

    ```ts
    /**
     * POSTs the request to start coffee brewing.
     * @param amountLitres The amount to brew. Must fit the pot size!
     */
    brew(amountLitres: number, logger: Logger) {
      // ...
    }
    ```

### Comments when calling a function

“Parameter name” comments should be used whenever the method name and parameter value do not sufficiently convey the meaning of the parameter.

Before adding these comments, consider refactoring the method to instead accept an interface and destructure it to greatly improve call-site readability.

Parameter name comments go before the parameter value, and include the parameter name and a `=` suffix:

✅ Good:

```ts
someFunction(obviousParam, /* shouldRender= */ true, /* name= */ 'hello');
```

Existing code may use a legacy parameter name comment style, which places these comments ~after~ the parameter value and omits the `=`. Continuing to use this style within the file for consistency is acceptable.

```ts
someFunction(obviousParam, true /* shouldRender */, 'hello' /* name */);
```


## Place documentation prior to decorators (G:place-documentation-prior-to-decorators)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#place-documentation-prior-to-decorators), CC BY 3.0.

When a class, method, or property have both decorators like `@Component` and JsDoc, please make sure to write the JsDoc before the decorator.

*   Do not write JsDoc between the Decorator and the decorated statement.

    ❌ Bad:

    ```ts
    @Component({
      selector: 'foo',
      template: 'bar',
    })
    /** Component that prints "bar". */
    export class FooComponent {}
    ```

*   Write the JsDoc block before the Decorator.

    ✅ Good:

    ```ts
    /** Component that prints "bar". */
    @Component({
      selector: 'foo',
      template: 'bar',
    })
    export class FooComponent {}
    ```
