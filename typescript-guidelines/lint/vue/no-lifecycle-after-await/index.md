
### What it does

Disallow asynchronously registered lifecycle hooks.

### Why is this bad?

Lifecycle hooks must be registered synchronously during `setup()` execution.
If a lifecycle hook is called after an `await` statement, it may be registered
too late and might not work as expected.

### Examples

Examples of **incorrect** code for this rule:

```vue
<script>
import { onMounted } from "vue";
export default {
  async setup() {
    await doSomething();
    onMounted(() => {
      /* ... */
    }); // error
  },
};
</script>
```

Examples of **correct** code for this rule:

```vue
<script>
import { onMounted } from "vue";
export default {
  async setup() {
    onMounted(() => {
      /* ... */
    }); // ok
    await doSomething();
  },
};
</script>
```

## How to use

## References
