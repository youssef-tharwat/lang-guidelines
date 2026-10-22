# adapter

Wrap a type so it satisfies an interface it doesn't implement.

**Sources:** GOF:adapter

---

## Adapter (Gang of Four) (GOF:adapter)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/adapter/rust/example), CC BY-SA 4.0.

**Adapter** is a structural design pattern, which allows incompatible objects to collaborate.

The Adapter acts as a wrapper between two objects. It catches calls for one object and transforms them to format and interface recognizable by the second object.
### Adapter in Rust

In this example, the `trait SpecificTarget` is incompatible with a `call` function which accepts `trait Target` only.

fn call(target: impl Target);

The adapter helps to pass the incompatible interface to the `call` function.

let target = TargetAdapter::new(specific_target);
call(target);

##### **adapter.rs**
```rust
use crate::{adaptee::SpecificTarget, Target};

/// Converts adaptee's specific interface to a compatible `Target` output.
pub struct TargetAdapter {
    adaptee: SpecificTarget,
}

impl TargetAdapter {
    pub fn new(adaptee: SpecificTarget) -> Self {
        Self { adaptee }
    }
}

impl Target for TargetAdapter {
    fn request(&self) -> String {
        // Here's the "adaptation" of a specific output to a compatible output.
        self.adaptee.specific_request().chars().rev().collect()
    }
}
```

##### **adaptee.rs**
```rust
pub struct SpecificTarget;

impl SpecificTarget {
    pub fn specific_request(&self) -> String {
        ".tseuqer cificepS".into()
    }
}
```

##### **target.rs**
```rust
pub trait Target {
    fn request(&self) -> String;
}

pub struct OrdinaryTarget;

impl Target for OrdinaryTarget {
    fn request(&self) -> String {
        "Ordinary request.".into()
    }
}
```

##### **main.rs**
```rust
mod adaptee;
mod adapter;
mod target;

use adaptee::SpecificTarget;
use adapter::TargetAdapter;
use target::{OrdinaryTarget, Target};

/// Calls any object of a `Target` trait.
///
/// To understand the Adapter pattern better, imagine that this is
/// a client code, which can operate over a specific interface only
/// (`Target` trait only). It means that an incompatible interface cannot be
/// passed here without an adapter.
fn call(target: impl Target) {
    println!("'{}'", target.request());
}

fn main() {
    let target = OrdinaryTarget;

    print!("A compatible target can be directly called: ");
    call(target);

    let adaptee = SpecificTarget;

    println!(
        "Adaptee is incompatible with client: '{}'",
        adaptee.specific_request()
    );

    let adapter = TargetAdapter::new(adaptee);

    print!("But with adapter client can call its method: ");
    call(adapter);
}
```

#### Output
```text
A compatible target can be directly called: 'Ordinary request.'
Adaptee is incompatible with client: '.tseuqer cificepS'
But with adapter client can call its method: 'Specific request.'
```
