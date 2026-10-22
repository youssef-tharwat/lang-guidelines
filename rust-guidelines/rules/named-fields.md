# named-fields

Use named fields instead of tuples or multi-field tuple structs, except one-field newtypes and very local code.

**Why:** `.0` and `.1` stop meaning anything quickly.

**Sources:** G:prefer-named-fields-over-tuples-and-non-newtype-tuple-structs

---

## Prefer named fields over tuples and non-newtype tuple structs (G:prefer-named-fields-over-tuples-and-non-newtype-tuple-structs)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#prefer-named-fields-over-tuples-and-non-newtype-tuple-structs), CC BY 3.0.

Prefer types with named fields over tuples, as tuple indexes (`.0`, `.1`, …) quickly become confusing.

Exceptions:

*   Newtype tuple structs (tuple structs with only one field).

*   In very local contexts where there is unlikely to be any confusion.
