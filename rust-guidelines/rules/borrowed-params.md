# borrowed-params

Take parameters in their most general borrowed form (`&str`, `&[T]`, `&T`, `Option<&T>`) and keep `Rc`, `Arc`, `Box`, `RefCell` and `Mutex` out of public signatures unless the pointer is the API's purpose.

**Why:** Callers pass what they hold without copying or wrapping.

**Sources:** G:accept-flexible-references-for-immutable-data, M-AVOID-WRAPPERS, P:idioms/coercion-arguments

---

## Accept flexible references for immutable data (G:accept-flexible-references-for-immutable-data)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#accept-flexible-references-for-immutable-data), CC BY 3.0.

When functions accept borrowed, immutable data, use a reference type that affords the most flexibility. Pass references to the data itself instead of references to smart pointers, containers, or wrappers.

| Use | Instead of | Why? |
| --- | --- | --- |
| `&T` | `&Box<T>` | Borrow the data inside the box |
| `&[T]` | `&Vec<T>` | Accept any slice instead of specific containers |
| `&str` | `&String` | Accept a string slice instead of references to owned strings |
| `Option<&T>` | `&Option<T>` | Borrow the data inside the Option |

Exceptions:

*   When expecting non-linear character data such as Rope/Cord.

For context, see Clippy lints [`borrowed_box`](https://rust-lang.github.io/rust-clippy/master/index.html#borrowed_box) and [ptr_arg](https://rust-lang.github.io/rust-clippy/master/index.html#ptr_arg).

**Rationale**

Accepting reference types that don’t mention specific smart pointers, containers, or wrappers makes functions more versatile and performant: callers can pass data held in a variety of ways without copying it first.


## Avoid smart pointers and wrappers in APIs (M-AVOID-WRAPPERS)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

As a specialization of M-ABSTRACTIONS-DONT-NEST, generic wrappers and smart pointers like
`Rc<T>`, `Arc<T>`, `Box<T>`, or `RefCell<T>` should be avoided in public APIs.

From a user perspective these are mostly implementation details, and introduce infectious complexity that users have to
resolve. In fact, these might even be impossible to resolve once multiple crates disagree about the required type of wrapper.

If wrappers are needed internally, they should be hidden behind a clean API that uses simple types like `&T`, `&mut T`, or `T` directly. Compare:

```rust
// Good: simple API
pub fn process_data(data: &Data) -> State { ... }
pub fn store_config(config: Config) -> Result<(), Error> { ... }

// Bad: Exposing implementation details
pub fn process_shared(data: Arc<Mutex<Shared>>) -> Box<Processed> { ... }
pub fn initialize(config: Rc<RefCell<Config>>) -> Arc<Server> { ... }
```

Smart pointers in APIs are acceptable when:

- The smart pointer is fundamental to the API's purpose (e.g., a new container lib)

- The smart pointer, based on benchmarks, significantly improves performance and the complexity is justified.


## Use borrowed types for arguments (P:idioms/coercion-arguments)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/idioms/coercion-arguments.html), MPL-2.0.

### Description

Using a target of a deref coercion can increase the flexibility of your code
when you are deciding which argument type to use for a function argument. In
this way, the function will accept more input types.

This is not limited to slice-able or fat pointer types. In fact, you should
always prefer using the **borrowed type** over **borrowing the owned type**.
Such as `&str` over `&String`, `&[T]` over `&Vec<T>`, or `&T` over `&Box<T>`.

Using borrowed types you can avoid layers of indirection for those instances
where the owned type already provides a layer of indirection. For instance, a
`String` has a layer of indirection, so a `&String` will have two layers of
indirection. We can avoid this by using `&str` instead, and letting `&String`
coerce to a `&str` whenever the function is invoked.

### Example

For this example, we will illustrate some differences for using `&String` as a
function argument versus using a `&str`, but the ideas apply as well to using
`&Vec<T>` versus using a `&[T]` or using a `&Box<T>` versus a `&T`.

Consider an example where we wish to determine if a word contains three
consecutive vowels. We don't need to own the string to determine this, so we
will take a reference.

The code might look something like this:

```rust
fn three_vowels(word: &String) -> bool {
    let mut vowel_count = 0;
    for c in word.chars() {
        match c {
            'a' | 'e' | 'i' | 'o' | 'u' => {
                vowel_count += 1;
                if vowel_count >= 3 {
                    return true;
                }
            }
            _ => vowel_count = 0,
        }
    }
    false
}

fn main() {
    let ferris = "Ferris".to_string();
    let curious = "Curious".to_string();
    println!("{}: {}", ferris, three_vowels(&ferris));
    println!("{}: {}", curious, three_vowels(&curious));

    // This works fine, but the following two lines would fail:
    // println!("Ferris: {}", three_vowels("Ferris"));
    // println!("Curious: {}", three_vowels("Curious"));
}
```

This works fine because we are passing a `&String` type as a parameter. If we
remove the comments on the last two lines, the example will fail. This is
because a `&str` type will not coerce to a `&String` type. We can fix this by
simply modifying the type for our argument.

For instance, if we change our function declaration to:

```rust
fn three_vowels(word: &str) -> bool {
```

then both versions will compile and print the same output.

```bash
Ferris: false
Curious: true
```

But wait, that's not all! There is more to this story. It's likely that you may
say to yourself: that doesn't matter, I will never be using a `&'static str` as
an input anyways (as we did when we used `"Ferris"`). Even ignoring this special
example, you may still find that using `&str` will give you more flexibility
than using a `&String`.

Let's now take an example where someone gives us a sentence, and we want to
determine if any of the words in the sentence contain three consecutive vowels.
We probably should make use of the function we have already defined and simply
feed in each word from the sentence.

An example of this could look like this:

```rust
fn three_vowels(word: &str) -> bool {
    let mut vowel_count = 0;
    for c in word.chars() {
        match c {
            'a' | 'e' | 'i' | 'o' | 'u' => {
                vowel_count += 1;
                if vowel_count >= 3 {
                    return true;
                }
            }
            _ => vowel_count = 0,
        }
    }
    false
}

fn main() {
    let sentence_string =
        "Once upon a time, there was a friendly curious crab named Ferris".to_string();
    for word in sentence_string.split(' ') {
        if three_vowels(word) {
            println!("{word} has three consecutive vowels!");
        }
    }
}
```

Running this example using our function declared with an argument type `&str`
will yield

```bash
curious has three consecutive vowels!
```

However, this example will not run when our function is declared with an
argument type `&String`. This is because string slices are a `&str` and not a
`&String` which would require an allocation to be converted to `&String` which
is not implicit, whereas converting from `String` to `&str` is cheap and
implicit.

### See also

- [Rust Language Reference on Type Coercions](https://doc.rust-lang.org/reference/type-coercions.html)
- For more discussion on how to handle `String` and `&str` see
  [this blog series (2015)](https://web.archive.org/web/20201112023149/https://hermanradtke.com/2015/05/03/string-vs-str-in-rust-functions.html)
  by Herman J. Radtke III
- [Steve Klabnik's Blogpost on 'When should I use String vs &str?'](https://archive.ph/LBpD0)
