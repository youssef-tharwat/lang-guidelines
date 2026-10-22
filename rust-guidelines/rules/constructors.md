# constructors

Construct with an inherent `new()` (`try_new()` when it returns `Result`, `new_with_x()` for alternatives, `from_x()` beside an important `From` impl); also implement `Default` when there is a default state, keeping `new()`.

**Why:** Constructors live where users look for them.

**Sources:** G:naming-initialization-functions, G:pair-important-from-impls-with-explicit-constructor-methods, P:idioms/ctor, P:idioms/default, M-UPSTREAM-GUIDELINES

---

## Naming initialization functions (G:naming-initialization-functions)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#naming-initialization-functions), CC BY 3.0.

Follow these guidelines when naming initialization functions:

*   Constructors: Use `new()`, or `new_with_foo()` if there is more than one. If the constructor returns a `Result`, use `try_new()`.

*   Value-to-value conversions: Use `from_foo()` with an associated `From` impl. See [here](https://doc.rust-lang.org/std/convert/trait.From.html#when-to-implement-from) for details on when an operation can be considered to be a value-to-value conversion.


## Pair important `From` impls with explicit constructor methods (G:pair-important-from-impls-with-explicit-constructor-methods)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#pair-important-from-impls-with-explicit-constructor-methods), CC BY 3.0.

If a type has an important `From` impl that is expected to be one of the primary ways of constructing it, add an inherent `::new()`, `::new_from_foo()`, or `::from_foo()` method.


## Constructors (P:idioms/ctor)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/idioms/ctor.html), MPL-2.0.

### Description

Rust does not have constructors as a language construct. Instead, the convention
is to use an associated function `new` to create an
object:

````rust
/// Time in seconds.
///
/// # Example
///
/// ```
/// let s = Second::new(42);
/// assert_eq!(42, s.value());
/// ```
pub struct Second {
    value: u64,
}

impl Second {
    // Constructs a new instance of [`Second`].
    // Note this is an associated function - no self.
    pub fn new(value: u64) -> Self {
        Self { value }
    }

    /// Returns the value in seconds.
    pub fn value(&self) -> u64 {
        self.value
    }
}
````

### Default Constructors

Rust supports default constructors with the `Default` trait:

````rust
/// Time in seconds.
///
/// # Example
///
/// ```
/// let s = Second::default();
/// assert_eq!(0, s.value());
/// ```
pub struct Second {
    value: u64,
}

impl Second {
    /// Returns the value in seconds.
    pub fn value(&self) -> u64 {
        self.value
    }
}

impl Default for Second {
    fn default() -> Self {
        Self { value: 0 }
    }
}
````

`Default` can also be derived if all types of all fields implement `Default`,
like they do with `Second`:

````rust
/// Time in seconds.
///
/// # Example
///
/// ```
/// let s = Second::default();
/// assert_eq!(0, s.value());
/// ```
#[derive(Default)]
pub struct Second {
    value: u64,
}

impl Second {
    /// Returns the value in seconds.
    pub fn value(&self) -> u64 {
        self.value
    }
}
````

**Note:** It is common and expected for types to implement both `Default` and an
empty `new` constructor. `new` is the constructor convention in Rust, and users
expect it to exist, so if it is reasonable for the basic constructor to take no
arguments, then it should, even if it is functionally identical to default.

**Hint:** The advantage of implementing or deriving `Default` is that your type
can now be used where a `Default` implementation is required, most prominently,
any of the `*or_default` functions in the standard library.

### See also

- The default idiom for a more in-depth description of the
  `Default` trait.

- The builder pattern for constructing
  objects where there are multiple configurations.

- API Guidelines/C-COMMON-TRAITS for
  implementing both, `Default` and `new`.


## The `Default` Trait (P:idioms/default)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/idioms/default.html), MPL-2.0.

### Description

Many types in Rust have a constructor. However, this is *specific* to the
type; Rust cannot abstract over "everything that has a `new()` method". To allow
this, the `Default` trait was conceived, which can be used with containers and
other generic types (e.g. see `Option::unwrap_or_default()`). Notably, some
containers already implement it where applicable.

Not only do one-element containers like `Cow`, `Box` or `Arc` implement
`Default` for contained `Default` types, one can automatically
`#[derive(Default)]` for structs whose fields all implement it, so the more
types implement `Default`, the more useful it becomes.

On the other hand, constructors can take multiple arguments, while the
`default()` method does not. There can even be multiple constructors with
different names, but there can only be one `Default` implementation per type.

### Example

```rust
use std::{path::PathBuf, time::Duration};

// note that we can simply auto-derive Default here.
#[derive(Default, Debug, PartialEq)]
struct MyConfiguration {
    // Option defaults to None
    output: Option<PathBuf>,
    // Vecs default to empty vector
    search_path: Vec<PathBuf>,
    // Duration defaults to zero time
    timeout: Duration,
    // bool defaults to false
    check: bool,
}

impl MyConfiguration {
    // add setters here
}

fn main() {
    // construct a new instance with default values
    let mut conf = MyConfiguration::default();
    // do something with conf here
    conf.check = true;
    println!("conf = {conf:#?}");

    // partial initialization with default values, creates the same instance
    let conf1 = MyConfiguration {
        check: true,
        ..Default::default()
    };
    assert_eq!(conf, conf1);
}
```

### See also

- The constructor idiom is another way to generate instances that may or may
  not be "default"
- The `Default` documentation (scroll down for the list of implementors)
- `Option::unwrap_or_default()`
- `derive(new)`


## Follow the upstream guidelines (M-UPSTREAM-GUIDELINES)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

The guidelines in this book complement existing Rust guidelines, in particular:

- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/checklist.html)
- [Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/)
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns//intro.html)
- [Rust Reference - Undefined Behavior](https://doc.rust-lang.org/reference/behavior-considered-undefined.html)

We recommend you read through these as well, and apply them in addition to this book's items. Pay special attention to the ones below, as they are frequently forgotten:

- [ ] [C-CONV](https://rust-lang.github.io/api-guidelines/naming.html#ad-hoc-conversions-follow-as_-to_-into_-conventions-c-conv) - Ad-hoc conversions
  follow  `as_`, `to_`, `into_` conventions
- [ ] [C-GETTER](https://rust-lang.github.io/api-guidelines/naming.html#getter-names-follow-rust-convention-c-getter) - Getter names follow Rust convention
- [ ] [C-COMMON-TRAITS](https://rust-lang.github.io/api-guidelines/interoperability.html#c-common-traits) - Types eagerly implement common traits
  - `Copy`, `Clone`, `Eq`, `PartialEq`, `Ord`, `PartialOrd`, `Hash`, `Default`, `Debug`
  - `Display` where type wants to be displayed
- [ ] [C-CTOR](https://rust-lang.github.io/api-guidelines/predictability.html?highlight=new#constructors-are-static-inherent-methods-c-ctor) -
  Constructors are static, inherent methods
  - In particular, have `Foo::new()`, even if you have `Foo::default()`
- [ ] [C-FEATURE](https://rust-lang.github.io/api-guidelines/naming.html#feature-names-are-free-of-placeholder-words-c-feature) - Feature names
  are free of placeholder words
