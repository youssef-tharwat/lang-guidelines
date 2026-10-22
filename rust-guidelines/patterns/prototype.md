# prototype

Copy existing objects through `Clone` instead of rebuilding them.

**Sources:** GOF:prototype

---

## Prototype (Gang of Four) (GOF:prototype)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/prototype/rust/example), CC BY-SA 4.0.

**Prototype** is a creational design pattern that allows cloning objects, even complex ones, without coupling to their specific classes.

All prototype classes should have a common interface that makes it possible to copy objects even if their concrete classes are unknown. Prototype objects can produce full copies since objects of the same class can access each other’s private fields.
### Built-in _Clone_ trait

Rust has a built-in `std::clone::Clone` trait with many implementations for various types (via `#[derive(Clone)]`). Thus, the Prototype pattern is ready to use out of the box.

##### **main.rs**
```rust
#[derive(Clone)]
struct Circle {
    pub x: u32,
    pub y: u32,
    pub radius: u32,
}

fn main() {
    let circle1 = Circle {
        x: 10,
        y: 15,
        radius: 10,
    };

    // Prototype in action.
    let mut circle2 = circle1.clone();
    circle2.radius = 77;

    println!("Circle 1: {}, {}, {}", circle1.x, circle1.y, circle1.radius);
    println!("Circle 2: {}, {}, {}", circle2.x, circle2.y, circle2.radius);
}
```

#### Output
```text
Circle 1: 10, 15, 10
Circle 2: 10, 15, 77
```
