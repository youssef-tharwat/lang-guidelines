---
type: llm
focus: {source: file, path: report.rs}
weight: 3
---

Judge the refactored module in `report.rs`. Pass when ALL of these hold:

1. No function takes `&Vec<Item>` or `&String`; they take `&[Item]` and `&str`.
2. `total` does not clone the items to iterate them.
3. `find` returns a struct with named fields (or a reference to the found `Item`) instead of the tuple `(String, u32, u32)`, and uses pattern matching or combinators rather than `is_some()` followed by `unwrap()`.
4. The `verbose: bool` parameter is replaced by a two-variant enum (or an equivalent named type).
5. `render` builds its string with `format!`/`write!`/`writeln!` rather than chains of `+`.
6. The getter is named `name()` and returns `&str`.
7. The glob re-export `pub use crate::model::*` is gone (an explicit `use`/`pub use` of named items is fine).

Fail if any item is missing. List each item as met or not met before the verdict.
