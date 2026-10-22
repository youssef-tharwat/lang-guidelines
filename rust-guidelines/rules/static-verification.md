# static-verification

Run rustfmt and clippy (`lints.toml` in this skill holds the recommended tables), plus cargo-audit, cargo-hack and cargo-udeps; skip formatting with `#[rustfmt::skip]` only for manual alignment or generated code.

**Why:** Tools catch what review misses.

**Sources:** M-STATIC-VERIFICATION, G:use-the-appropriate-formatting-tool, G:opting-out-of-automatic-formatting

---

## Use static verification (M-STATIC-VERIFICATION)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Projects should use the following static verification tools to help maintain the quality of the code. These tools can be
configured to run on a developer's machine during normal work, and should be used as part of check-in gates.

* [compiler lints](https://doc.rust-lang.org/rustc/lints/index.html) offer many lints to avoid bugs and improve code quality.
* [clippy lints](https://doc.rust-lang.org/clippy/) contain hundreds of lints to avoid bugs and improve code quality.
* [rustfmt](https://github.com/rust-lang/rustfmt) ensures consistent source formatting.
* [cargo-audit](https://crates.io/crates/cargo-audit) verifies crate dependencies for security vulnerabilities.
* [cargo-hack](https://crates.io/crates/cargo-hack) validates that all combinations of crate features work correctly.
* [cargo-udeps](https://crates.io/crates/cargo-udeps) detects unused dependencies in Cargo.toml files.
* [miri](https://github.com/rust-lang/miri) validates the correctness of unsafe code.

### Compiler Lints

The Rust compiler generally produces exceptionally good diagnostics. In addition to the default set of diagnostics, projects
should explicitly enable the following set of compiler lints:

```toml
[lints.rust]
ambiguous_negative_literals = "warn"
missing_debug_implementations = "warn"
redundant_imports = "warn"
redundant_lifetimes = "warn"
trivial_numeric_casts = "warn"
unsafe_op_in_unsafe_fn = "warn"
unused_lifetimes = "warn"
```

### Clippy Lints

For clippy, projects should enable all major lint categories, and additionally enable some lints from the `restriction` lint group.
Undesired lints (e.g., numeric casts) can be opted back out of on a case-by-case basis:

```toml
[lints.clippy]
cargo = { level = "warn", priority = -1 }
complexity = { level = "warn", priority = -1 }
correctness = { level = "warn", priority = -1 }
pedantic = { level = "warn", priority = -1 }
perf = { level = "warn", priority = -1 }
style = { level = "warn", priority = -1 }
suspicious = { level = "warn", priority = -1 }
# nursery = { level = "warn", priority = -1 }  # optional, might cause more false positives

# These lints are from the `restriction` lint group and prevent specific
# constructs being used in source code in order to drive up consistency,
# quality, and brevity
allow_attributes_without_reason = "warn"
as_pointer_underscore = "warn"
assertions_on_result_states = "warn"
clone_on_ref_ptr = "warn"
deref_by_slicing = "warn"
disallowed_script_idents = "warn"
empty_drop = "warn"
empty_enum_variants_with_brackets = "warn"
empty_structs_with_brackets = "warn"
fn_to_numeric_cast_any = "warn"
if_then_some_else_none = "warn"
map_err_ignore = "warn"
redundant_type_annotations = "warn"
renamed_function_params = "warn"
semicolon_outside_block = "warn"
string_to_string = "warn"
undocumented_unsafe_blocks = "warn"
unnecessary_safety_comment = "warn"
unnecessary_safety_doc = "warn"
unneeded_field_pattern = "warn"
unused_result_ok = "warn"

# May cause issues with structured logging otherwise.
literal_string_with_formatting_args = "allow"

# Define custom opt outs here
# ...
```


## Use the appropriate formatting tool (G:use-the-appropriate-formatting-tool)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#use-the-appropriate-formatting-tool), CC BY 3.0.

Use the appropriate formatting tool (e.g., `git cl format` in Chromium).

Configuration (for style guide authors)

A codebase may choose to not apply the following `rustfmt` options if they care about building on stable and the option is unavailable on their stable Rust:

*   Maximum of 100 columns per line: [`max_width = 100`](https://rust-lang.github.io/rustfmt/?version=v1.6.0&search=#max_width)

*   Usage of lowercase alphabets in hex literals (`0xab123cdef` as opposed to `0xAB123CDEF`): [`hex_literal_case = Lower`](https://rust-lang.github.io/rustfmt/?version=v1.6.0&search=#hex_literal_case)

*   Macro matcher formatting: [`format_macro_matchers = true`](https://rust-lang.github.io/rustfmt/?version=v1.6.0&search=#format_macro_matchers)

*   Usage of escapes for invisible characters in literals. E.g., if you wish to have text containing a Zero-Width joiner, use `\u{200D}`.


## Opting out of automatic formatting (G:opting-out-of-automatic-formatting)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#opting-out-of-automatic-formatting), CC BY 3.0.

You may opt out of automatic formatting using `#[rustfmt::skip]`, but only in the following situations:

*   **Manual alignment** – If you have a situation-specific reason to have a snippet of code line up in a particular way (e.g., multiple similar lines of code that you want to remain aligned for readability, or a matrix-constructing function).

*   **Generated code** (ideally, use a genrule instead).

Important: Formatting should not be skipped for personal style choices.
