
### What it does

Require components to be the default export.

### Why is this bad?

Using SFCs (Single File Components) without a default export is
not supported in Vue 3. Components should be exported as the default export.

### Examples

Examples of **incorrect** code for this rule:

```vue
<script>
const foo = "foo";
</script>
```

Examples of **correct** code for this rule:

```vue
<script>
export default {
  data() {
    return {
      foo: "foo",
    };
  },
};
</script>
```

## How to use

## References
