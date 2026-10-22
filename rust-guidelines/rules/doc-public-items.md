# doc-public-items

Document every public item (`///`) and public module (`//!`): a one-line summary of about 15 words, then `# Examples`, `# Errors`, `# Panics`, `# Safety`, `# Abort` where they apply; describe parameters in prose, not a table; never just restate the name. Use `//` for implementation notes.

**Why:** Docs are what users and agents read first.

**Sources:** M-CANONICAL-DOCS, M-FIRST-DOC-SENTENCE, M-MODULE-DOCS, G:when-and-how-to-write-documentation, M-DESIGN-FOR-AI, P:idioms/rustdoc-init

---

## Documentation has canonical sections (M-CANONICAL-DOCS)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Public library items must contain the canonical doc sections. The summary sentence must always be present. Extended documentation and examples
are strongly encouraged. The other sections must be present when applicable.

```rust
/// Summary sentence < 15 words.
///
/// Extended documentation in free form.
///
/// # Examples
/// One or more examples that show API usage like so.
///
/// # Errors
/// If fn returns `Result`, list known error conditions
///
/// # Panics
/// If fn may panic, list when this may happen
///
/// # Safety
/// If fn is `unsafe` or may otherwise cause UB, this section must list
/// all conditions a caller must uphold.
///
/// # Abort
/// If fn may abort the process, list when this may happen.
pub fn foo() {}
```

In contrast to other languages, you should not create a table of parameters. Instead parameter use is explained in plain text. In other words, do not

```rust
/// Copies a file.
///
/// # Parameters
/// - src: The source.
/// - dst: The destination.
fn copy(src: File, dst: File) {}
```

but instead:

```rust
/// Copies a file from `src` to `dst`.
fn copy(src: File, dst: File) {}
```

### Related Reading

- Function docs include error, panic, and safety considerations ([C-FAILURE](https://rust-lang.github.io/api-guidelines/documentation.html#c-failure))


## First sentence is one line; approx. 15 words (M-FIRST-DOC-SENTENCE)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

When you document your item, the first sentence becomes the "summary sentence" that is extracted and shown in the module summary:

```rust
/// This is the summary sentence, shown in the module summary.
///
/// This is other documentation. It is only shown in that item's detail view.
/// Sentences here can be as long as you like and it won't cause any issues.
fn some_item() { }
```

Since Rust API documentation is rendered with a fixed max width, there is a naturally preferred sentence length you should not
exceed to keep things tidy on most screens.

If you keep things in a line, your docs will become easily skimmable. Compare, for example, the standard library:

Otherwise, you might end up with _widows_ and a generally unpleasant reading flow:

As a rule of thumb, the first sentence should not exceed **15 words**.


## Has comprehensive module documentation (M-MODULE-DOCS)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Any public library module must have `//!` module documentation, and the first sentence must follow M-DOC-FIRST-SENTENCE.

```rust
pub mod ffi {
    //! Contains FFI abstractions.

    pub struct String {};
}
```

The rest of the module documentation should be comprehensive, i.e., cover the most relevant technical aspects of the contained items, including

- what the module contains
- when it should be used, possibly when not
- examples
- subsystem specifications (e.g., `std::fmt` [also describes its formatting language](https://doc.rust-lang.org/stable/std/fmt/index.html#formatting-parameters))
- observable side effects, including what guarantees are made about these, if any
- relevant implementation details, e.g., the used system APIs

 Great examples include:

- [`std::fmt`](https://doc.rust-lang.org/stable/std/fmt/index.html)
- [`std::pin`](https://doc.rust-lang.org/stable/std/pin/index.html)
- [`std::option`](https://doc.rust-lang.org/stable/std/option/index.html)

This does not mean every module should contain all of these items. But if there is something to say about the interaction of the contained types,
their module documentation is the right place.


## When and how to write documentation (G:when-and-how-to-write-documentation)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#when-and-how-to-write-documentation), CC BY 3.0.

Add documentation comments to public APIs, potentially using the `missing_docs` lint to help with this.

Best practices for documentation comments:

*   Consider including examples: It is not necessary for every function to have examples, but enough functionality should be covered in examples _somewhere_ to give an idea of how the crate works.

*   Always document panic cases for functions which may panic due to malformed input.

*   Clearly document invariants for unsafe functions and traits.

*   Use capitalization and punctuation.

*   Don’t explain the basics of the programming language. For example, don’t do the following:

    ```rust
    struct MockFileSystem { ... }

    /// A mock implementation of the FileSystem trait, intended to be used in unit tests.
    impl FileSystem for MockFileSystem
    ```

Exceptions:

*   Comments should say something that the code does not already say. If there’s nothing insightful to say, it is better to omit the comment than to repeat the function name in a trivial way. For example, don’t do the following (it’s fine to `allow` the lint in that case):

    ```rust
    /// Removes an element.
    pub fn remove_element() -> Element {}
    ```

*   It is generally okay to omit documentation on individual enum variants, especially if their name is self-explanatory.

**How to format documentation comments**

Follow these guidelines when writing documentation comments:

*   Use `///` comments to document items following the comment, such as functions, structs, enums, traits, and type aliases.

*   Use `//!` comments to document the module or the library itself. These comments should be placed at the top of the file.

*   Follow the rules laid out in [the official Rust style guide on doc comments](https://doc.rust-lang.org/nightly/style-guide/#doc-comments).

*   Use Markdown syntax.

*   Use ordinary comment syntax (`//`) for non-documentation comments, such as implementation comments, TODOs that are not interesting for users, commented out source code, etc.

*   Prefer to document things in a straightforward manner, using `///` and `//!` comments, rather than generating documentation from macros. This makes the documentation directly readable when viewing or modifying the source code.

It is acceptable, and even encouraged, to mix doc comments (`///` and `//!`) and ordinary comments (`//`). If you have one thing you wish to document publicly, and another thing you want to note as an implementation comment, then use both! For example:

✅ Good:

```rust
/// Finds the first `FooItem` with the given `name`, or `None` if not present.
// TODO: crbug.com/12345 - `name` should be &str, not String.
pub fn get_named(items: &[FooItem], name: String) -> Option<&FooItem> {...}
```

**Rationale**

Many, though not all, languages have a different commenting convention (such as extra `*` characters) for doc comments as opposed to implementation comments. Rust and Python are notable for not just having different commenting conventions, but an actual different syntax entirely. This has concrete benefits to the Rust ecosystem:

*   Doc comments can be consumed by tooling, including documentation generators like `rustdoc`, IDE features, and Kythe.

*   Doc comments have a standard structure and formatting rules (Markdown), allowing for rich text in those contexts.

*   Errors in applying doc comment syntax (e.g., applying it to an expression instead of a documentable item) are linted against, catching documentation errors early. If there are no lint errors, the doc comments are guaranteed to be visible to documentation tooling, removing a degree of flakiness and unpredictability from the documentation process.

*   Doc comments are a part of the AST, and so can be produced and consumed by macros, including both `macro_rules!` macros and procedural macros.


## Design with AI use in mind (M-DESIGN-FOR-AI)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

As a general rule, making APIs easier to use for humans also makes them easier to use by AI.
If you follow the guidelines in this book, you should be in good shape.

Rust's strong type system is a boon for agents, as their lack of genuine understanding can often be
counterbalanced by comprehensive compiler checks, which Rust provides in abundance.

With that said, there are a few guidelines which are particularly important to help make AI coding in Rust more effective:

* **Create Idiomatic Rust API Patterns**. The more your APIs, whether public or internal, look and feel like the majority of
Rust code in the world, the better it is for AI. Follow the [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/checklist.html)
along with the guidelines from Library / UX.

* **Provide Thorough Docs**. Agents love good detailed docs. Include docs for all of your modules and public items in your crate.
Assume the reader has a solid, but not expert, level of understanding of Rust, and that the reader understands the standard library.
Follow
[C-CRATE-DOC](https://rust-lang.github.io/api-guidelines/checklist.html#c-crate-doc),
[C-FAILURE](https://rust-lang.github.io/api-guidelines/checklist.html#c-failure),
[C-LINK](https://rust-lang.github.io/api-guidelines/checklist.html#c-link), and
M-MODULE-DOCS
M-CANONICAL-DOCS.

* **Provide Thorough Examples**. Your documentation should have directly usable examples, the repository should include more elaborate ones.
Follow
[C-EXAMPLE](https://rust-lang.github.io/api-guidelines/checklist.html#c-example)
[C-QUESTION-MARK](https://rust-lang.github.io/api-guidelines/checklist.html#c-question-mark).

* **Use Strong Types**. Avoid [primitive obsession](https://refactoring.guru/smells/primitive-obsession) by using strong types with strict well-documented semantics.
Follow
[C-NEWTYPE](https://rust-lang.github.io/api-guidelines/checklist.html#c-newtype).

* **Make Your APIs Testable**. Design APIs which allow your customers to test their use of your API in unit tests. This might involve introducing some mocks, fakes,
or cargo features. AI agents need to be able to iterate quickly to prove that the code they are writing that calls your API is working
correctly.

* **Ensure Test Coverage**. Your own code should have good test coverage over observable behavior.
This enables agents to work in a mostly hands-off mode when refactoring.


## Easy doc initialization (P:idioms/rustdoc-init)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/idioms/rustdoc-init.html), MPL-2.0.

### Description

If a struct takes significant effort to initialize when writing docs, it can be
quicker to wrap your example with a helper function which takes the struct as an
argument.

### Motivation

Sometimes there is a struct with multiple or complicated parameters and several
methods. Each of these methods should have examples.

For example:

````rust
struct Connection {
    name: String,
    stream: TcpStream,
}

impl Connection {
    /// Sends a request over the connection.
    ///
    /// # Example
    /// ```no_run
    /// # // Boilerplate are required to get an example working.
    /// # let stream = TcpStream::connect("127.0.0.1:34254");
    /// # let connection = Connection { name: "foo".to_owned(), stream };
    /// # let request = Request::new("RequestId", RequestType::Get, "payload");
    /// let response = connection.send_request(request);
    /// assert!(response.is_ok());
    /// ```
    fn send_request(&self, request: Request) -> Result<Status, SendErr> {
        // ...
    }

    /// Oh no, all that boilerplate needs to be repeated here!
    fn check_status(&self) -> Status {
        // ...
    }
}
````

### Example

Instead of typing all of this boilerplate to create a `Connection` and
`Request`, it is easier to just create a wrapping helper function which takes
them as arguments:

````rust
struct Connection {
    name: String,
    stream: TcpStream,
}

impl Connection {
    /// Sends a request over the connection.
    ///
    /// # Example
    /// ```
    /// # fn call_send(connection: Connection, request: Request) {
    /// let response = connection.send_request(request);
    /// assert!(response.is_ok());
    /// # }
    /// ```
    fn send_request(&self, request: Request) -> Result<Status, SendErr> {
        // ...
    }
}
````

**Note** in the above example the line `assert!(response.is_ok());` will not
actually run while testing because it is inside a function which is never
invoked.

### Advantages

This is much more concise and avoids repetitive code in examples.

### Disadvantages

As example is in a function, the code will not be tested. Though it will still
be checked to make sure it compiles when running a `cargo test`. So this pattern
is most useful when you need `no_run`. With this, you do not need to add
`no_run`.

### Discussion

If assertions are not required this pattern works well.

If they are, an alternative can be to create a public method to create a helper
instance which is annotated with `#[doc(hidden)]` (so that users won't see it).
Then this method can be called inside of rustdoc because it is part of the
crate's public API.
