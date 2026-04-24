# Vue Rules (TypeScript & JavaScript)

17 rules that apply when the project uses **vue**.
Load this file only if the project's manifest imports or depends on
`vue`.

---

### vue/define-emits-declaration
This rule enforces `defineEmits` typing style which you should use `type-based`, strict `type-literal` (introduced in Vue 3.3), or `runtime` declaration.
❌ 
```
// "vue/define-emits-declaration": ["error", "type-based"]
<script setup lang="ts">
const emit = defineEmits(["change", "update"]);
const emit2 = defineEmits({
  change: (id) => typeof id === "number",
  update: (value) => typeof value === "string",
…
```
✅ 
```
// "vue/define-emits-declaration": ["error", "type-based"]
<script setup lang="ts">
const emit = defineEmits<{
  (e: "change", id: number): void;
  (e: "update", value: string): void;
}>();
…
```

### vue/define-props-declaration
This rule enforces `defineProps` typing style which you should use `type-based` or `runtime` declaration.
❌ 
```
// "vue/define-props-declaration": ["error", "type-based"]
<script setup lang="ts">
const props = defineProps({
  kind: { type: String },
});
</script>
…
```
✅ 
```
// "vue/define-props-declaration": ["error", "type-based"]
<script setup lang="ts">
const props = defineProps<{
  kind: string;
}>();
</script>
…
```

### vue/define-props-destructuring
This rule enforces a consistent style for handling Vue 3 Composition API props, allowing you to choose between requiring destructuring or prohibiting it.
❌ 
```
<script setup lang="ts">
const props = defineProps(["foo"]);
const propsWithDefaults = withDefaults(defineProps(["foo"]), { foo: "default" });
const { baz } = withDefaults(defineProps(["baz"]), { baz: "default" });
const props = defineProps<{ foo?: string }>();
const propsWithDefaults = withDefaults(defineProps<{ foo?: string }>(), { foo: "default" });
…
```
✅ 
```
<script setup lang="ts">
const { foo } = defineProps(["foo"]);
const { bar = "default" } = defineProps(["bar"]);
const { foo } = defineProps<{ foo?: string }>();
const { bar = "default" } = defineProps<{ bar?: string }>();
</script>
```

### vue/max-props
Enforce a maximum number of props defined for a given Vue component.
❌ 
```
<script setup>
defineProps({
  prop1: String,
  prop2: String,
})
</script>
```
✅ 
```
<script setup>
defineProps({
  prop1: String,
})
</script>
```

### vue/no-arrow-functions-in-watch
This rule disallows using arrow functions when defining a watcher.
❌ 
```
<script>
export default {
  watch: {
    foo: () => {},
    bar: {
      handler: () => {},
…
```
✅ 
```
<script>
export default {
  watch: {
    foo() {},
    bar: function () {},
    baz: {
…
```

### vue/no-deprecated-destroyed-lifecycle
Do not use using deprecated `destroyed` and `beforeDestroy` lifecycle hooks in Vue.js 3.0.0+.
❌ 
```
<script>
export default {
  beforeDestroy() {},
  destroyed() {},
};
</script>
```
✅ 
```
<script>
export default {
  beforeUnmount() {},
  unmounted() {},
};
</script>
```

### vue/no-export-in-script-setup
Do not use `export` in `<script setup>`
❌ 
```
<script setup>
export let msg = "Hello!";
</script>
```
✅ 
```
<script setup>
let msg = "Hello!";
</script>
```

### vue/no-import-compiler-macros
Do not use importing Vue compiler macros.
❌ 
```
<script setup>
import { defineProps, withDefaults } from "vue";
</script>
```
✅ 
```
<script setup>
import { ref } from "vue";
</script>
```

### vue/no-lifecycle-after-await
Do not use asynchronously registered lifecycle hooks.
❌ 
```
<script>
import { onMounted } from "vue";
export default {
  async setup() {
    await doSomething();
    onMounted(() => {
…
```
✅ 
```
<script>
import { onMounted } from "vue";
export default {
  async setup() {
    onMounted(() => {
      /* ... */
…
```

### vue/no-multiple-slot-args
Do not use passing multiple arguments to scoped slots.
❌ 
```
<script>
export default {
  render(h) {
    var children = this.$scopedSlots.default(foo, bar);
    var children = this.$scopedSlots.default(...foo);
  },
…
```
✅ 
```
<script>
export default {
  render(h) {
    var children = this.$scopedSlots.default();
    var children = this.$scopedSlots.default(foo);
    var children = this.$scopedSlots.default({ foo, bar });
…
```

### vue/no-required-prop-with-default
Enforce props with default values to be optional.
❌ 
```
<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    name: string | number;
    age?: number;
  }>(),
…
```
✅ 
```
<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    name?: string | number;
    age?: number;
  }>(),
…
```

### vue/no-this-in-before-route-enter
Do not use `this` usage in a `beforeRouteEnter` method.
❌ 
```
export default {
  beforeRouteEnter(to, from, next) {
    this.a; // Error: 'this' is not available
    next();
  },
};
```
✅ 
```
export default {
  beforeRouteEnter(to, from, next) {
    // anything without `this`
  },
};
```

### vue/prefer-import-from-vue
Enforce `import from 'vue'` instead of `import from '@vue/*'`.
❌ 
```
import { createApp } from "@vue/runtime-dom";
import { Component } from "@vue/runtime-core";
import { ref } from "@vue/reactivity";
```
✅ `import { createApp, ref, Component } from "vue";`

### vue/require-default-export
Require components to be the default export.
❌ 
```
<script>
const foo = "foo";
</script>
```
✅ 
```
<script>
export default {
  data() {
    return {
      foo: "foo",
    };
…
```

### vue/require-typed-ref
Require `ref` and `shallowRef` functions to be strongly typed.
❌ 
```
const count = ref();
const name = shallowRef();
```
✅ 
```
const count = ref<number>();
const a = ref(0);
```

### vue/valid-define-emits
This rule checks whether `defineEmits` compiler macro is valid.
❌ 
```
<script setup>
const def = { notify: null };
defineEmits(def);
</script>
```
✅ 
```
<script setup>
defineEmits({ notify: null });
</script>
```

### vue/valid-define-props
This rule checks whether `defineProps` compiler macro is valid.
❌ 
```
<script setup>
const def = { msg: String };
defineProps(def);
</script>
```
✅ 
```
<script setup>
defineProps({ msg: String });
</script>
```
