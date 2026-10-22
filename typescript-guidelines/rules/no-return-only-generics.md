# no-return-only-generics

Don't design APIs whose type parameter appears only in the return type; when calling an existing one, pass the type argument explicitly.

**Why:** The type is otherwise an unchecked assertion.

**Sources:** G:return-type-only-generics

---

## Return type only generics (G:return-type-only-generics)

[Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html#return-type-only-generics), CC BY 3.0.

Avoid creating APIs that have return type only generics. When working with existing APIs that have return type only generics always explicitly specify the generics.
