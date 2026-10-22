# decorator

Add behavior by wrapping an object in another that implements the same trait.

**Sources:** GOF:decorator

---

## Decorator (Gang of Four) (GOF:decorator)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/decorator/rust/example), CC BY-SA 4.0.

**Decorator** is a structural pattern that allows adding new behaviors to objects dynamically by placing them inside special wrapper objects, called _decorators_.

Using decorators you can wrap objects countless number of times since both target objects and decorators follow the same interface. The resulting object will get a stacking behavior of all wrappers.
### Input streams decoration

There is a **_practical example_** in Rust’s standard library for input/output operations.

A buffered reader decorates a vector reader adding buffered behavior.

let mut input = BufReader::new(Cursor::new("Input data"));
input.read(&mut buf).ok();

##### **main.rs**
```rust
use std::io::{BufReader, Cursor, Read};

fn main() {
    let mut buf = [0u8; 10];

    // A buffered reader decorates a vector reader which wraps input data.
    let mut input = BufReader::new(Cursor::new("Input data"));

    input.read(&mut buf).ok();

    print!("Read from a buffered reader: ");

    for byte in buf {
        print!("{}", char::from(byte));
    }

    println!();
}
```

#### Output
```text
Read from a buffered reader: Input data
```
