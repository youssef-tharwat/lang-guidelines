# module-layout

Name a leaf module after its primary item (`foo.rs` for `Foo`); keep non-leaf modules (`mod.rs`, `lib.rs`) to `mod` declarations, re-exports and minimal glue.

**Why:** Structure and contents stay separate and easy to find.

**Sources:** G:code-organization, G:name-source-files-and-leaf-modules-after-the-primary-user-defined-item, G:dont-implement-apis-in-non-leaf-modules

---

## Code organization (G:code-organization)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#code-organization), CC BY 3.0.

_Terminology:_

*   A _crate_ is a unit of compilation. A crate always contains a nameless Rust module, the “root module”.

*   A Rust _module_ is a unit of code organization within a crate. Rust modules are used to control visibility of names. Modules can be nested. They can also be used to split code across files and directories.


## Name source files and leaf modules after the primary user-defined item (G:name-source-files-and-leaf-modules-after-the-primary-user-defined-item)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#name-source-files-and-leaf-modules-after-the-primary-user-defined-item), CC BY 3.0.

When a `leaf module` has a primary user-defined item (e.g., `Foo`), the module should be named after that item (e.g., `mod foo` and `foo.rs`).

Leaf modules that are not primarily about any particular abstraction can be named as desired.

**Rationale**

This makes it easy to identify the content/purpose of a source file or leaf module at a glance.


## Don’t implement APIs in non-leaf modules (G:dont-implement-apis-in-non-leaf-modules)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#dont-implement-apis-in-non-leaf-modules), CC BY 3.0.

The only items in non-leaf modules should be module declarations (not definitions) and `re-exports`.

Note that the definition of `leaf modules` allows the following sub-modules: `mod test` and cross-language binding modules like `#[cxx::bridge]`.

Exceptions:

*   Having a small amount of core “ties things together” implementation code in a non-leaf module may be fine. The goal is to not have a lot of code in these modules.

**Rationale**

This makes it easier to find things, and avoids mixing structure and contents.
