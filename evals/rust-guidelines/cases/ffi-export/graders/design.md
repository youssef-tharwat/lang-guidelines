---
type: llm
focus: {source: file, path: ffi.rs}
weight: 3
---

Judge the Rust code in `ffi.rs`. Pass when ALL of these hold:

1. The pointer is checked for null before any dereference.
2. The incoming string is borrowed through `CStr` (no needless copy), and invalid UTF-8 maps to an error code.
3. Every `unsafe` block has a `// SAFETY:` comment, and the exported function's docs include a `# Safety` section stating what the C caller must guarantee.
4. Failures return negative codes defined as named constants, not magic numbers.
5. Nothing can panic on bad input: no `unwrap()`/`expect()` on input-dependent values.
6. The export uses `extern "C"` with `#[no_mangle]` or `#[unsafe(no_mangle)]`.

Fail if any item is missing. List each item as met or not met before the verdict.
