# memento

Snapshot and restore an object's state without exposing its internals.

**Sources:** GOF:memento

---

## Memento (Gang of Four) (GOF:memento)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/memento/rust/example), CC BY-SA 4.0.

**Memento** is a behavioral design pattern that allows making snapshots of an object’s state and restoring it in future.

The Memento doesn’t compromise the internal structure of the object it works with, as well as data kept inside the snapshots.

### Conceptual example

This is a conceptual example of Memento pattern.

##### **conceptual.rs**
```rust
trait Memento<T> {
    fn restore(self) -> T;
    fn print(&self);
}

struct Originator {
    state: u32,
}

impl Originator {
    pub fn save(&self) -> OriginatorBackup {
        OriginatorBackup {
            state: self.state.to_string(),
        }
    }
}

struct OriginatorBackup {
    state: String,
}

impl Memento<Originator> for OriginatorBackup {
    fn restore(self) -> Originator {
        Originator {
            state: self.state.parse().unwrap(),
        }
    }

    fn print(&self) {
        println!("Originator backup: '{}'", self.state);
    }
}

fn main() {
    let mut history = Vec::<OriginatorBackup>::new();

    let mut originator = Originator { state: 0 };

    originator.state = 1;
    history.push(originator.save());

    originator.state = 2;
    history.push(originator.save());

    for moment in history.iter() {
        moment.print();
    }

    let originator = history.pop().unwrap().restore();
    println!("Restored to state: {}", originator.state);

    let originator = history.pop().unwrap().restore();
    println!("Restored to state: {}", originator.state);
}
```

#### Output
```text
Originator backup: '1'
Originator backup: '2'
Restored to state: 2
Restored to state: 1
```

### Serde serialization framework

A common way to make a structure serializable is to derive `Serialize` and `Deserialize` traits from the [serde serialization framework](https://crates.io/crates/serde). Then an object of serializable type can be converted to many different formats, e.g. JSON with [serde_json](https://crates.io/crates/serde_json) crate.

use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct Originator {
    state: u32,
}

##### **serde.rs**
```rust
use serde::{Deserialize, Serialize};

/// An object to be stored. It derives a default
/// `Serialize` and `Deserialize` trait implementation, which
/// allows to convert it into many different formats (e.g. JSON).
#[derive(Serialize, Deserialize)]
struct Originator {
    state: u32,
}

impl Originator {
    /// Serializes an originator into a string of JSON format.
    pub fn save(&self) -> String {
        serde_json::to_string(self).unwrap()
    }

    /// Deserializes an originator into a string of JSON format.
    pub fn restore(json: &str) -> Self {
        serde_json::from_str(json).unwrap()
    }
}

fn main() {
    // A stack of mementos.
    let mut history = Vec::<String>::new();

    let mut originator = Originator { state: 0 };

    originator.state = 1;
    history.push(originator.save());

    originator.state = 2;
    history.push(originator.save());

    for moment in history.iter() {
        println!("{}", moment);
    }

    let originator = Originator::restore(&history.pop().unwrap());
    println!("Restored to state: {}", originator.state);

    let originator = Originator::restore(&history.pop().unwrap());
    println!("Restored to state: {}", originator.state);
}
```

#### Output
```text
{"state":1}
{"state":2}
Restored to state: 2
Restored to state: 1
```
