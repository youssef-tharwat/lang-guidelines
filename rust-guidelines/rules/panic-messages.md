# panic-messages

Every intentional panic (`panic!`, `assert!`, `unreachable!`, `todo!`, `expect`) carries a message that says what went wrong with the relevant values and, for assertions, why the condition must hold or who is at fault; never just restate the condition. Tests may skip messages.

**Why:** The message is what shows up in logs.

**Sources:** G:use-context-strings-to-clarify-assertions, M-PANIC-MESSAGE

---

## Use context strings to clarify assertions (G:use-context-strings-to-clarify-assertions)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#use-context-strings-to-clarify-assertions), CC BY 3.0.

While some assertions are self-explanatory, many benefit from additional context that clarifies why an assertion is expected to hold, or what caused it to be violated. Use the optional format string argument for `assert!` to convey this context.

You should always consider adding context, but particularly in the following situations:

*   If you’re thinking of adding a comment to the assertion. Use a format string instead: It has the benefit that it will appear in logs.

*   If you expect failing assertions to be seen by users. In this case, a human-readable explanation is more helpful than a Rust expression.

*   If logging a value helps in understanding why the assertion failed.

*   To clarify whether a failing assertion means that

    *   The client misused an API (i.e., they should change their use of the API), or

    *   The implementation contains a bug (i.e., the client should file a bug report).

Examples

**Explaining why an assertion should hold**

✅ Good:

```rust
assert!(
    values.is_sorted(),
    "`values` is populated from a `PriorityQueue`, so we expect it to be sorted"
);
```

**Logging a value to clarify why the assertion failed**

✅ Good:

```rust
assert!(refund > 0, "Refund must be positive, got {refund:?}");
```

**Flagging misuse of an API**

✅ Good:

```rust
impl Database {
    ...

    fn execute_query(&self, query: &str) {
        assert!(self.stream.is_some(), "Call connect() before executing queries");
    }

    ...
}
```

**Don’t use the context string merely to repeat the condition**

❌ Bad:

```rust
assert!(values.is_sorted(), "values should always be sorted");
```


## Custom panics have a helpful message (M-PANIC-MESSAGE)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

When code panics intentionally (via `panic!`, `assert!`, `unreachable!`, `todo!`, or similar), a message must be present to clearly state what went wrong and, where applicable, include relevant values.

```rust
// Bad, the panic gives the developer little to act on.
assert!(buffer.len() >= HEADER_SIZE);

// Good, message contains reason and actual values.
assert!(buffer.len() >= HEADER_SIZE, "buffer too small for header: got {} bytes, need {HEADER_SIZE}", buffer.len());
```

Messages related to API misuse should be useful to the end user. Messages indicating bugs should be helpful to you-as-the-author, or whoever maintains the project after you, to quickly identify the underlying cause.

Panic messages in tests are not generally needed.
