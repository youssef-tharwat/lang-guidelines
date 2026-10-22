# visitor

Run several algorithms over a heterogeneous structure such as an AST without changing the node types.

**Sources:** P:patterns/behavioural/visitor, GOF:visitor

---

## Visitor (P:patterns/behavioural/visitor)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/patterns/behavioural/visitor.html), MPL-2.0.

### Description

A visitor encapsulates an algorithm that operates over a heterogeneous
collection of objects. It allows multiple different algorithms to be written
over the same data without having to modify the data (or their primary
behaviour).

Furthermore, the visitor pattern allows separating the traversal of a collection
of objects from the operations performed on each object.

### Example

```rust
// The data we will visit
mod ast {
    pub enum Stmt {
        Expr(Expr),
        Let(Name, Expr),
    }

    pub struct Name {
        value: String,
    }

    pub enum Expr {
        IntLit(i64),
        Add(Box<Expr>, Box<Expr>),
        Sub(Box<Expr>, Box<Expr>),
    }
}

// The abstract visitor
mod visit {
    use ast::*;

    pub trait Visitor<T> {
        fn visit_name(&mut self, n: &Name) -> T;
        fn visit_stmt(&mut self, s: &Stmt) -> T;
        fn visit_expr(&mut self, e: &Expr) -> T;
    }
}

use ast::*;
use visit::*;

// An example concrete implementation - walks the AST interpreting it as code.
struct Interpreter;
impl Visitor<i64> for Interpreter {
    fn visit_name(&mut self, n: &Name) -> i64 {
        panic!()
    }
    fn visit_stmt(&mut self, s: &Stmt) -> i64 {
        match *s {
            Stmt::Expr(ref e) => self.visit_expr(e),
            Stmt::Let(..) => unimplemented!(),
        }
    }

    fn visit_expr(&mut self, e: &Expr) -> i64 {
        match *e {
            Expr::IntLit(n) => n,
            Expr::Add(ref lhs, ref rhs) => self.visit_expr(lhs) + self.visit_expr(rhs),
            Expr::Sub(ref lhs, ref rhs) => self.visit_expr(lhs) - self.visit_expr(rhs),
        }
    }
}
```

One could implement further visitors, for example a type checker, without having
to modify the AST data.

### Motivation

The visitor pattern is useful anywhere that you want to apply an algorithm to
heterogeneous data. If data is homogeneous, you can use an iterator-like
pattern. Using a visitor object (rather than a functional approach) allows the
visitor to be stateful and thus communicate information between nodes.

### Discussion

It is common for the `visit_*` methods to return void (as opposed to in the
example). In that case it is possible to factor out the traversal code and share
it between algorithms (and also to provide noop default methods). In Rust, the
common way to do this is to provide `walk_*` functions for each datum. For
example,

```rust
pub fn walk_expr(visitor: &mut Visitor, e: &Expr) {
    match *e {
        Expr::IntLit(_) => {}
        Expr::Add(ref lhs, ref rhs) => {
            visitor.visit_expr(lhs);
            visitor.visit_expr(rhs);
        }
        Expr::Sub(ref lhs, ref rhs) => {
            visitor.visit_expr(lhs);
            visitor.visit_expr(rhs);
        }
    }
}
```

In other languages (e.g., Java) it is common for data to have an `accept` method
which performs the same duty.

### See also

The visitor pattern is a common pattern in most OO languages.

[Wikipedia article](https://en.wikipedia.org/wiki/Visitor_pattern)

The fold pattern is similar to visitor but produces a
new version of the visited data structure.


## Visitor (Gang of Four) (GOF:visitor)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/visitor/rust/example), CC BY-SA 4.0.

**Visitor** is a behavioral design pattern that allows adding new behaviors to existing class hierarchy without altering any existing code.

> Read why Visitors can’t be simply replaced with method overloading in our article [Visitor and Double Dispatch](https://refactoring.guru/design-patterns/visitor-double-dispatch).
### Deserialization

A real-world example of the Visitor pattern is [serde serialization framework](https://serde.rs/) and its deserialization model (see [Serde data model](https://serde.rs/data-model.html)).

1.   `Visitor` should be implemented for a deserializable type.
2.   `Visitor` is passed to a `Deserializer` (an “Element” in terms of the Visitor Pattern), which accepts and drives the `Visitor` in order to construct a desired type.

Let’s reproduce this deserializing model in our example.

##### **visitor.rs**
```rust
use crate::{TwoValuesArray, TwoValuesStruct};

/// Visitor can visit one type, do conversions, and output another type.
///
/// It's not like all visitors must return a new type, it's just an example
/// that demonstrates the technique.
pub trait Visitor {
    type Value;

    /// Visits a vector of integers and outputs a desired type.
    fn visit_vec(&self, v: Vec<i32>) -> Self::Value;
}

/// Visitor implementation for a struct of two values.
impl Visitor for TwoValuesStruct {
    type Value = TwoValuesStruct;

    fn visit_vec(&self, v: Vec<i32>) -> Self::Value {
        TwoValuesStruct { a: v[0], b: v[1] }
    }
}

/// Visitor implementation for a struct of values array.
impl Visitor for TwoValuesArray {
    type Value = TwoValuesArray;

    fn visit_vec(&self, v: Vec<i32>) -> Self::Value {
        let mut ab = [0i32; 2];

        ab[0] = v[0];
        ab[1] = v[1];

        TwoValuesArray { ab }
    }
}
```

##### **main.rs**
```rust
#![allow(unused)]

mod visitor;

use visitor::Visitor;

/// A struct of two integer values.
///
/// It's going to be an output of `Visitor` trait which is defined for the type
/// in `visitor.rs`.
#[derive(Default, Debug)]
pub struct TwoValuesStruct {
    a: i32,
    b: i32,
}

/// A struct of values array.
///
/// It's going to be an output of `Visitor` trait which is defined for the type
/// in `visitor.rs`.
#[derive(Default, Debug)]
pub struct TwoValuesArray {
    ab: [i32; 2],
}

/// `Deserializer` trait defines methods that can parse either a string or
/// a vector, it accepts a visitor which knows how to construct a new object
/// of a desired type (in our case, `TwoValuesArray` and `TwoValuesStruct`).
trait Deserializer<V: Visitor> {
    fn create(visitor: V) -> Self;
    fn parse_str(&self, input: &str) -> Result<V::Value, &'static str> {
        Err("parse_str is unimplemented")
    }
    fn parse_vec(&self, input: Vec<i32>) -> Result<V::Value, &'static str> {
        Err("parse_vec is unimplemented")
    }
}

struct StringDeserializer<V: Visitor> {
    visitor: V,
}

impl<V: Visitor> Deserializer<V> for StringDeserializer<V> {
    fn create(visitor: V) -> Self {
        Self { visitor }
    }

    fn parse_str(&self, input: &str) -> Result<V::Value, &'static str> {
        // In this case, in order to apply a visitor, a deserializer should do
        // some preparation. The visitor does its stuff, but it doesn't do everything.
        let input_vec = input
            .split_ascii_whitespace()
            .map(|x| x.parse().unwrap())
            .collect();

        Ok(self.visitor.visit_vec(input_vec))
    }
}

struct VecDeserializer<V: Visitor> {
    visitor: V,
}

impl<V: Visitor> Deserializer<V> for VecDeserializer<V> {
    fn create(visitor: V) -> Self {
        Self { visitor }
    }

    fn parse_vec(&self, input: Vec<i32>) -> Result<V::Value, &'static str> {
        Ok(self.visitor.visit_vec(input))
    }
}

fn main() {
    let deserializer = StringDeserializer::create(TwoValuesStruct::default());
    let result = deserializer.parse_str("123 456");
    println!("{:?}", result);

    let deserializer = VecDeserializer::create(TwoValuesStruct::default());
    let result = deserializer.parse_vec(vec![123, 456]);
    println!("{:?}", result);

    let deserializer = VecDeserializer::create(TwoValuesArray::default());
    let result = deserializer.parse_vec(vec![123, 456]);
    println!("{:?}", result);

    println!(
        "Error: {}",
        deserializer.parse_str("123 456").err().unwrap()
    )
}
```

#### Output
```text
Ok(TwoValuesStruct { a: 123, b: 456 })
Ok(TwoValuesStruct { a: 123, b: 456 })
Ok(TwoValuesArray { ab: [123, 456] })
Error: parse_str unimplemented
```
