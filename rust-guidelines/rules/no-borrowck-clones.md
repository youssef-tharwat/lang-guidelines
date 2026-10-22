# no-borrowck-clones

Don't `.clone()` to silence the borrow checker: borrow, split the struct so fields borrow independently, or move with `mem::take`; clone only when you need an independent copy.

**Why:** Hidden deep copies cost time and mask design problems.

**Sources:** G:prefer-borrows-over-deep-copies, P:anti/patterns/borrow/clone, P:patterns/structural/compose-structs

---

## Prefer borrows over deep copies (G:prefer-borrows-over-deep-copies)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#prefer-borrows-over-deep-copies), CC BY 3.0.

Use `.clone()` when you genuinely need a deep copy of an object.

Avoid using `.clone()` as a substitute for borrowing. Design code that works naturally with Rust’s ownership and borrowing rules. However, if the borrowing relationships become excessively complex, `.clone()` can be a pragmatic choice.

Consider the performance needs of the code while choosing between cloning and borrowing.

Note: This advice does not apply to cloning `Rc` or `Arc` pointers. Cloning reference-counted pointers does not create a deep copy, and is an expected way to use them.

**Rationale**

Deep copies can be expensive to make due to memory allocation and data copying.


## Clone to satisfy the borrow checker (P:anti/patterns/borrow/clone)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/anti/patterns/borrow/clone.html), MPL-2.0.

### Description

The borrow checker prevents Rust users from developing otherwise unsafe code by
ensuring that either: only one mutable reference exists, or potentially many but
all immutable references exist. If the code written does not hold true to these
conditions, this anti-pattern arises when the developer resolves the compiler
error by cloning the variable.

### Example

```rust
// define any variable
let mut x = 5;

// Borrow `x` -- but clone it first
let y = &mut (x.clone());

// without the x.clone() two lines prior, this line would fail on compile as
// x has been borrowed
// thanks to x.clone(), x was never borrowed, and this line will run.
println!("{x}");

// perform some action on the borrow to prevent rust from optimizing this
//out of existence
*y += 1;
```

### Motivation

It is tempting, particularly for beginners, to use this pattern to resolve
confusing issues with the borrow checker. However, there are serious
consequences. Using `.clone()` causes a copy of the data to be made. Any changes
between the two are not synchronized -- as if two completely separate variables
exist.

There are special cases -- `Rc<T>` is designed to handle clones intelligently.
It internally manages exactly one copy of the data. Invoking `.clone()` on `Rc`
produces a new `Rc` instance, which points to the same data as the source `Rc`,
while increasing a reference count. The same applies to `Arc`, the thread-safe
counterpart of `Rc`.

In general, clones should be deliberate, with full understanding of the
consequences. If a clone is used to make a borrow checker error disappear,
that's a good indication this anti-pattern may be in use.

Even though `.clone()` is an indication of a bad pattern, sometimes **it is fine
to write inefficient code**, in cases such as when:

- the developer is still new to ownership
- the code doesn't have great speed or memory constraints (like hackathon
  projects or prototypes)
- satisfying the borrow checker is really complicated, and you prefer to
  optimize readability over performance

If an unnecessary clone is suspected, The
[Rust Book's chapter on Ownership](https://doc.rust-lang.org/book/ownership.html)
should be understood fully before assessing whether the clone is required or
not.

Also be sure to always run `cargo clippy` in your project, which will detect
some cases in which `.clone()` is not necessary.

### See also

- `mem::{take(_), replace(_)}` to keep owned values in changed enums
- [`Rc<T>` documentation, which handles .clone() intelligently](http://doc.rust-lang.org/std/rc/)
- [`Arc<T>` documentation, a thread-safe reference-counting pointer](https://doc.rust-lang.org/std/sync/struct.Arc.html)
- [Tricks with ownership in Rust](https://web.archive.org/web/20210120233744/https://xion.io/post/code/rust-borrowchk-tricks.html)


## Struct decomposition for independent borrowing (P:patterns/structural/compose-structs)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/patterns/structural/compose-structs.html), MPL-2.0.

### Description

Sometimes a large struct will cause issues with the borrow checker - although
fields can be borrowed independently, sometimes the whole struct ends up being
used at once, preventing other uses. A solution might be to decompose the struct
into several smaller structs. Then compose these together into the original
struct. Then each struct can be borrowed separately and have more flexible
behaviour.

This will often lead to a better design in other ways: applying this design
pattern often reveals smaller units of functionality.

### Example

Here is a contrived example of where the borrow checker foils us in our plan to
use a struct:

```rust
struct Database {
    connection_string: String,
    timeout: u32,
    pool_size: u32,
}

fn print_database(database: &Database) {
    println!("Connection string: {}", database.connection_string);
    println!("Timeout: {}", database.timeout);
    println!("Pool size: {}", database.pool_size);
}

fn main() {
    let mut db = Database {
        connection_string: "initial string".to_string(),
        timeout: 30,
        pool_size: 100,
    };

    let connection_string = &mut db.connection_string;
    print_database(&db);
    *connection_string = "new string".to_string();
}
```

The compiler throws following errors:

```ignore
let connection_string = &mut db.connection_string;
                        ------------------------- mutable borrow occurs here
print_database(&db);
               ^^^ immutable borrow occurs here
*connection_string = "new string".to_string();
------------------ mutable borrow later used here
```

We can apply this design pattern and refactor `Database` into three smaller
structs, thus solving the borrow checking issue:

```rust
// Database is now composed of three structs - ConnectionString, Timeout and PoolSize.
// Let's decompose it into smaller structs
#[derive(Debug, Clone)]
struct ConnectionString(String);

#[derive(Debug, Clone, Copy)]
struct Timeout(u32);

#[derive(Debug, Clone, Copy)]
struct PoolSize(u32);

// We then compose these smaller structs back into `Database`
struct Database {
    connection_string: ConnectionString,
    timeout: Timeout,
    pool_size: PoolSize,
}

// print_database can then take ConnectionString, Timeout and Poolsize struct instead
fn print_database(connection_str: ConnectionString, timeout: Timeout, pool_size: PoolSize) {
    println!("Connection string: {connection_str:?}");
    println!("Timeout: {timeout:?}");
    println!("Pool size: {pool_size:?}");
}

fn main() {
    // Initialize the Database with the three structs
    let mut db = Database {
        connection_string: ConnectionString("localhost".to_string()),
        timeout: Timeout(30),
        pool_size: PoolSize(100),
    };

    let connection_string = &mut db.connection_string;
    print_database(connection_string.clone(), db.timeout, db.pool_size);
    *connection_string = ConnectionString("new string".to_string());
}
```

### Motivation

This pattern is most useful, when you have a struct that ended up with a lot of
fields that you want to borrow independently. Thus having a more flexible
behaviour in the end.

### Advantages

Decomposition of structs lets you work around limitations in the borrow checker.
And it often produces a better design.

### Disadvantages

It can lead to more verbose code. And sometimes, the smaller structs are not
good abstractions, and so we end up with a worse design. That is probably a
'code smell', indicating that the program should be refactored in some way.

### Discussion

This pattern is not required in languages that don't have a borrow checker, so
in that sense is unique to Rust. However, making smaller units of functionality
often leads to cleaner code: a widely acknowledged principle of software
engineering, independent of the language.

This pattern relies on Rust's borrow checker to be able to borrow fields
independently of each other. In the example, the borrow checker knows that `a.b`
and `a.c` are distinct and can be borrowed independently, it does not try to
borrow all of `a`, which would make this pattern useless.
