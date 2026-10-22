# loops-vs-chains

Use short combinator chains (`any`, `map`, `filter`); switch to a `for` loop when the chain branches or mutates outside state; bind a chain to a named variable before a `for` header; avoid `for_each`.

**Why:** Each form is clearest in its own niche.

**Sources:** G:dont-use-iterator-combinator-chains-when-direct-iteration-is-clearer

---

## Don’t use iterator combinator chains when direct iteration is clearer (G:dont-use-iterator-combinator-chains-when-direct-iteration-is-clearer)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#dont-use-iterator-combinator-chains-when-direct-iteration-is-clearer), CC BY 3.0.

Avoid using combinator chains in ways that hurt readability. Specifically:

*   Avoid long and complex combinator chains.

*   Don’t construct combinator chains in the header of a `for` loop. Instead, assign the combinator chain to a variable, then consume that variable in the `for` loop.

*   Avoid `Iterator::for_each` unless you’re convinced you have a good reason. A `for` loop is usually easier to read.

Combinators _are_ preferable for shorter chains and for cases where the combinator itself provides a lot of logic that would otherwise have to be written out in the corresponding `for` loop.

Examples

**Complex combinator chains**

Here’s an example of a combinator chain that is hard to read because it involves conditionals and mutates external state:

❌ Bad:

```rust
let mut error_count = 0;
let _processed_items: Vec<_> = items
    .into_iter()
    .map(transformation_that_may_fail)
    .map(|result| {
        if result.is_err() {
            error_count += 1;
        }
        result
    })
    .filter_map(Result::ok)
    .collect();
```

The corresponding `for` loop is easier to read:

✅ Good:

```rust
let mut error_count = 0;
let mut processed_items = Vec::with_capacity(items.len());

for item in items {
    match transformation_that_may_fail(item) {
        Ok(val) => processed_items.push(val),
        Err(_) => error_count += 1,
    }
}
```

**Combinator chains in for loops**

Avoid constructing a combinator chain in the header of a `for` loop:

❌ Bad:

```rust
for bug in bug_descriptions
    .iter()
    .filter_map(|description| parse_bug_description(description).ok())
    .filter(|bug| bug.priority <= Priority::P1)
{
    assign_bug(bug);
}
```

Instead, assign the combinator chain to a variable. This reduces clutter, and the variable name documents what the combinator chain does:

✅ Good:

```rust
let urgent_bugs = bug_descriptions
    .iter()
    .filter_map(|description| parse_bug_description(description).ok())
    .filter(|bug| bug.priority <= Priority::P1);

for bug in urgent_bugs {
    assign_bug(bug);
}
```

**When to prefer a combinator chain**

Here’s an example where a combinator chain is preferable:

✅ Good:

```rust
let threshold_exceeded = values.iter().any(|&v| v > threshold);
```

The corresponding for loop is harder to read and reinvents the logic contained in `any()`:

❌ Bad:

```rust
let mut threshold_exceeded = false;
for v in values {
  if v > threshold {
    threshold_exceeded = true;
    break;
  }
}
```
