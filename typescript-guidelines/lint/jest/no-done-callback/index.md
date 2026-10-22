
### What it does

This rule checks the function parameter of hooks & tests for use of the done argument, suggesting you return a promise instead.

### Why is this bad?

When calling asynchronous code in hooks and tests, jest needs to know when the asynchronous work is complete to progress the current run.
Originally the most common pattern to achieve this was to use callbacks:

```javascript
test("the data is peanut butter", (done) => {
  function callback(data) {
    try {
      expect(data).toBe("peanut butter");
      done();
    } catch (error) {
      done(error);
    }
  }

  fetchData(callback);
});
```

This can be very error-prone however, as it requires careful understanding of how assertions work in tests or otherwise tests won't behave as expected.

### Examples

Examples of **incorrect** code for this rule:

```javascript
beforeEach((done) => {
  // ...
});

test("myFunction()", (done) => {
  // ...
});

test("myFunction()", function (done) {
  // ...
});
```

## How to use

## References
