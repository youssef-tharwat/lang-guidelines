# ffi-crates

Keep business logic in a safe, idiomatic core crate `foo` with no interop types; a `foo-ffi` crate (exporting to C) or `foo-sys` crate (binding to C) only translates between the two worlds, even if that repeats signatures.

**Why:** FFI ownership and data models don't belong in Rust APIs.

**Sources:** M-FFI-NAMING, M-FFI-TRANSLATES

---

## FFI crates follow established naming conventions (M-FFI-NAMING)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Crates used for FFI should follow established naming practices:

- `-sys` for crates defining items to call into existing (C-style) libraries
- `-ffi` for crates defining (C-style) items when called from existing applications

There are slight variations of this scheme (e.g., `-sys2` when a previous `-sys` crate was abandoned and using `-` vs `_`), but overall `-ffi` clearly defines 'export' libraries, and `-sys` 'import' ones.


## Business logic belongs in core crates, FFI only translates (M-FFI-TRANSLATES)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

When Rust is used to create FFI libraries, there should be a clear separation of concerns between the core _business logic_ crate `foo` and the glue crate `foo-ffi`.

Any operational functionality belongs in the core crate and should be expressed as idiomatic, safe, testable Rust. The FFI crate exists only to translate between native Rust and C constructs, and the core crate must not be infected with interop concerns, even if this means repeating, and slightly adjusting, type and function signatures. For example, given the following type in the core crate `foo`:

```rust
pub struct Message {
    destination: [u8; 8],
    data: Vec<u8>,
}

impl Message {
    pub fn new(destination: [u8; 8], data: Vec<u8>) -> Self { /* ... */ }
    pub fn transmit(&self) -> Result<(), TransmitError> { /* ... */ }
}
```

A proper separation of concerns might collapse construction and transmission into a single FFI entry point in `foo-ffi`:

```rust
#[no_mangle]
pub unsafe extern "C" fn transmit_message(
    destination: *const [u8; 8],
    data: *const u8,
    data_len: usize,
) -> u8 {
    let data = std::slice::from_raw_parts(data, data_len).to_vec();
    match Message::new(*destination, data).transmit() {
        Ok(()) => 0,
        Err(_) => 1,
    }
}
```

However, it would be improper to leak FFI requirements into `foo` itself: ownership, data models and signatures do not translate seamlessly between the two worlds. Any time _saved_ by skipping a clean split will have to be paid back many times over during refactorings down the line.

```rust
#[repr(C)]
pub struct Message {
    pub destination: [u8; 8],
    pub data_ptr: *mut u8,
    pub data_len: usize,
    pub data_cap: usize,
}
```
