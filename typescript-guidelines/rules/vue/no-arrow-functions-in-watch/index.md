
### What it does

This rule disallows using arrow functions when defining a watcher.

### Why is this bad?

Arrow functions bind `this` lexically, which means they don't have access to the Vue component instance.
In Vue watchers, you often need access to `this` to interact with component data, methods, or other properties.
Using regular functions or method shorthand ensures proper `this` binding.

### Examples

Examples of **incorrect** code for this rule:

```vue
<script>
export default {
  watch: {
    foo: () => {},
    bar: {
      handler: () => {},
    },
    baz: [
      (val) => {},
      {
        handler: () => {},
      },
    ],
  },
};
</script>
```

Examples of **correct** code for this rule:

```vue
<script>
export default {
  watch: {
    foo() {},
    bar: function () {},
    baz: {
      handler: function () {},
    },
  },
};
</script>
```

## How to use

## References
