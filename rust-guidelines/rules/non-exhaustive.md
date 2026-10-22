# non-exhaustive

Mark public enums, and public structs with public fields, that other teams use and that may grow `#[non_exhaustive]` (not fixed ontologies or struct-update option structs). When matching another crate's non-exhaustive enum, name every known variant and put the rest beside `_`.

**Why:** Adding a variant or field stays non-breaking.

**Binding in:** libraries (code other packages depend on); a strong recommendation in application-only code.

**Sources:** G:apply-non_exhaustive-to-publicly-exposed-enums, G:apply-non_exhaustive-to-public-structs-with-public-fields, G:dont-omit-patterns-on-non_exhaustive-enums-when-matching, P:idioms/priv-extend

---

## Apply `#[non_exhaustive]` to publicly-exposed enums (G:apply-non_exhaustive-to-publicly-exposed-enums)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#apply-non_exhaustive-to-publicly-exposed-enums), CC BY 3.0.

If an enum is part of a public API used by other teams, mark it `#[non_exhaustive]`.

Exceptions:

*   The enum will never change. For example:

    *   Enums describing an existing ontology (e.g., `enum Color { Red, Green, Blue }`).

    *   Enums with two states that could be Booleans (e.g., `enum Visibility { Visible, Hidden }`)

*   The enum _may_ change in the future, but you are committed to fixing resulting breakages via an LSC.

For context, see Clippy lint [`exhaustive_enums`](https://rust-lang.github.io/rust-clippy/master/index.html#exhaustive_enums).

**Rationale**

Marking an enum `#[non_exhaustive]` forces users to include a wildcard arm (`_ => ...`) in `match` statements. This ensures code continues to compile when new variants are added to the enum later.

This rule is primarily important for enums used across team boundaries, because the scope of the breakage could be significant. Enums used only a small number of times can’t create a large breakage and thus may ignore this rule.


## Apply `#[non_exhaustive]` to public structs with public fields (G:apply-non_exhaustive-to-public-structs-with-public-fields)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#apply-non_exhaustive-to-public-structs-with-public-fields), CC BY 3.0.

Structs with public fields that are part of a public API used by other teams should be marked `#[non_exhaustive]`.

Exceptions:

*   The struct fields are unlikely to change, e.g., because they describe an existing ontology (e.g., a Rectangle type) or the reviewer can otherwise be confident that they will not change.

*   The struct fields _may_ change in the future, but you are committed to fixing resulting breakages via an LSC.

*   You want to enable your users to use functional record update (FRU) struct initialization syntax (`Person { name: "foo", ..Default::default() }`).

**Rationale**

Adding a new field (even a private one) to a struct with all public fields is a breaking change, because callers can no longer name all fields in a struct literal.

A `#[non_exhaustive]` struct can’t be constructed with the struct literal syntax, except for the code in the same crate. This allows new private fields to be added without breaking users.

This rule is primarily important for structs used across team boundaries, because the scope of the breakage could be significant. Structs used only a small number of times can’t create a large breakage and thus may ignore this rule.


## Don’t omit patterns on `non_exhaustive` enums when matching (G:dont-omit-patterns-on-non_exhaustive-enums-when-matching)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#dont-omit-patterns-on-non_exhaustive-enums-when-matching), CC BY 3.0.

Prefer to list all enum variants in `match` statements over `non_exhaustive` enums.

If you don’t care about specific variants, place them in the wildcard arm. If you _only_ care about specific variants, use an `if let` or a `let … else {}`.

Examples:

```rust
#[non_exhaustive]
pub enum Shape {
    Circle,
    Square,
    Triangle,
}
```

✅ Good:

```rust
fn process_shape(shape: Shape) {
  match shape {
    Shape::Circle => println!("It's a circle"),
    Shape::Square => println!("It's a square"),
    // Triangle and any future variants don't require any actions.
    Shape::Triangle | _ => {}
  }
}
```

✅ Good:

```rust
fn process_shape(shape: Shape) {
  if let Shape::Circle = shape {
    println!("It's a circle");
  }
}
```

❌ Bad:

```rust
fn process_shape(shape: Shape) {
  match shape {
    Shape::Circle => println!("It's a circle"),
    _ => {}
  }
}
```

Exceptions:

*   You only care about specific variants _and_ `match` is cleaner than `if let`.

This is covered by the built-in lint `non_exhaustive_omitted_patterns` which you can enable on your code.


## `#[non_exhaustive]` and private fields for extensibility (P:idioms/priv-extend)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/idioms/priv-extend.html), MPL-2.0.

### Description

A small set of scenarios exist where a library author may want to add public
fields to a public struct or new variants to an enum without breaking backwards
compatibility.

Rust offers two solutions to this problem:

- Use `#[non_exhaustive]` on `struct`s, `enum`s, and `enum` variants. For
  extensive documentation on all the places where `#[non_exhaustive]` can be
  used, see
  [the docs](https://doc.rust-lang.org/reference/attributes/type_system.html#the-non_exhaustive-attribute).

- You may add a private field to a struct to prevent it from being directly
  instantiated or matched against (see Alternative)

### Example

```rust
mod a {
    // Public struct.
    #[non_exhaustive]
    pub struct S {
        pub foo: i32,
    }

    #[non_exhaustive]
    pub enum AdmitMoreVariants {
        VariantA,
        VariantB,
        #[non_exhaustive]
        VariantC {
            a: String,
        },
    }
}

fn print_matched_variants(s: a::S) {
    // Because S is `#[non_exhaustive]`, it cannot be named here and
    // we must use `..` in the pattern.
    let a::S { foo: _, .. } = s;

    let some_enum = a::AdmitMoreVariants::VariantA;
    match some_enum {
        a::AdmitMoreVariants::VariantA => println!("it's an A"),
        a::AdmitMoreVariants::VariantB => println!("it's a b"),

        // .. required because this variant is non-exhaustive as well
        a::AdmitMoreVariants::VariantC { a, .. } => println!("it's a c"),

        // The wildcard match is required because more variants may be
        // added in the future
        _ => println!("it's a new variant"),
    }
}
```

### Alternative: `Private fields` for structs

`#[non_exhaustive]` only works across crate boundaries. Within a crate, the
private field method may be used.

Adding a field to a struct is a mostly backwards compatible change. However, if
a client uses a pattern to deconstruct a struct instance, they might name all
the fields in the struct and adding a new one would break that pattern. The
client could name some fields and use `..` in the pattern, in which case adding
another field is backwards compatible. Making at least one of the struct's
fields private forces clients to use the latter form of patterns, ensuring that
the struct is future-proof.

The downside of this approach is that you might need to add an otherwise
unneeded field to the struct. You can use the `()` type so that there is no
runtime overhead and prepend `_` to the field name to avoid the unused field
warning.

```rust
pub struct S {
    pub a: i32,
    // Because `b` is private, you cannot match on `S` without using `..` and `S`
    //  cannot be directly instantiated or matched against
    _b: (),
}
```

### Discussion

On `struct`s, `#[non_exhaustive]` allows adding additional fields in a backwards
compatible way. It will also prevent clients from using the struct constructor,
even if all the fields are public. This may be helpful, but it's worth
considering if you *want* an additional field to be found by clients as a
compiler error rather than something that may be silently undiscovered.

`#[non_exhaustive]` can be applied to enum variants as well. A
`#[non_exhaustive]` variant behaves in the same way as a `#[non_exhaustive]`
struct.

Use this deliberately and with caution: incrementing the major version when
adding fields or variants is often a better option. `#[non_exhaustive]` may be
appropriate in scenarios where you're modeling an external resource that may
change out-of-sync with your library, but is not a general purpose tool.

#### Disadvantages

`#[non_exhaustive]` can make your code much less ergonomic to use, especially
when forced to handle unknown enum variants. It should only be used when these
sorts of evolutions are required **without** incrementing the major version.

When `#[non_exhaustive]` is applied to `enum`s, it forces clients to handle a
wildcard variant. If there is no sensible action to take in this case, this may
lead to awkward code and code paths that are only executed in extremely rare
circumstances. If a client decides to `panic!()` in this scenario, it may have
been better to expose this error at compile time. In fact, `#[non_exhaustive]`
forces clients to handle the "Something else" case; there is rarely a sensible
action to take in this scenario.

### See also

- [RFC introducing #[non_exhaustive] attribute for enums and structs](https://github.com/rust-lang/rfcs/blob/master/text/2008-non-exhaustive.md)
