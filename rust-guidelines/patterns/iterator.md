# iterator

Traverse a collection without exposing its internals; in Rust, implement `Iterator`.

**Sources:** GOF:iterator

---

## Iterator (Gang of Four) (GOF:iterator)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/iterator/rust/example), CC BY-SA 4.0.

**Iterator** is a behavioral design pattern that allows sequential traversal through a complex data structure without exposing its internal details.

Thanks to the Iterator, clients can go over elements of different collections in a similar fashion using a single iterator interface.

### Standard Iterator

Iterators are heavily used in idiomatic Rust code. This is how to use iterators over a standard array collection.

let array = &[1, 2, 3];
let iterator = array.iter();

// Traversal over each element of the vector.
iterator.for_each(|e| print!("{}, ", e));

### Custom Iterator

In Rust, the recommended way to define your _custom_ iterator is to use a standard `Iterator` trait. The example doesn’t contain a synthetic iterator interface, because it is really recommended to use the idiomatic Rust way.

let users = UserCollection::new();
let mut iterator = users.iter();

iterator.next();

A `next` method is the only `Iterator` trait method which is mandatory to be implemented. It makes accessible a huge range of standard methods, e.g. `fold`, `map`, `for_each`.

impl Iterator for UserIterator<'_> {
    fn next(&mut self) -> Option<Self::Item>;
}

##### **users.rs:** Collection & Iterator
```rust
pub struct UserCollection {
    users: [&'static str; 3],
}

/// A custom collection contains an arbitrary user array under the hood.
impl UserCollection {
    /// Returns a custom user collection.
    pub fn new() -> Self {
        Self {
            users: ["Alice", "Bob", "Carl"],
        }
    }

    /// Returns an iterator over a user collection.
    ///
    /// The method name may be different, however, `iter` is used as a de facto
    /// standard in a Rust naming convention.
    pub fn iter(&self) -> UserIterator {
        UserIterator {
            index: 0,
            user_collection: self,
        }
    }
}

/// UserIterator allows sequential traversal through a complex user collection
/// without exposing its internal details.
pub struct UserIterator<'a> {
    index: usize,
    user_collection: &'a UserCollection,
}

/// `Iterator` is a standard interface for dealing with iterators
/// from the Rust standard library.
impl Iterator for UserIterator<'_> {
    type Item = &'static str;

    /// A `next` method is the only `Iterator` trait method which is mandatory to be
    /// implemented. It makes accessible a huge range of standard methods,
    /// e.g. `fold`, `map`, `for_each`.
    fn next(&mut self) -> Option<Self::Item> {
        if self.index < self.user_collection.users.len() {
            let user = Some(self.user_collection.users[self.index]);
            self.index += 1;
            return user;
        }

        None
    }
}
```

##### **main.rs:** Client code
```rust
use crate::users::UserCollection;

mod users;

fn main() {
    print!("Iterators are widely used in the standard library: ");

    let array = &[1, 2, 3];
    let iterator = array.iter();

    // Traversal over each element of the array.
    iterator.for_each(|e| print!("{} ", e));

    println!("\n\nLet's test our own iterator.\n");

    let users = UserCollection::new();
    let mut iterator = users.iter();

    println!("1nd element: {:?}", iterator.next());
    println!("2nd element: {:?}", iterator.next());
    println!("3rd element: {:?}", iterator.next());
    println!("4th element: {:?}", iterator.next());

    print!("\nAll elements in user collection: ");
    users.iter().for_each(|e| print!("{} ", e));

    println!();
}
```

#### Output
```text
Iterators are widely used in the standard library: 1 2 3

Let's test our own iterator.

1nd element: Some("Alice")
2nd element: Some("Bob")
3rd element: Some("Carl")
4th element: None

All elements in user collection: Alice Bob Carl
```
