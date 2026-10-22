# mediator

Route communication between components through one mediator so they don't reference each other.

**Sources:** GOF:mediator

---

## Mediator (Gang of Four) (GOF:mediator)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/mediator/rust/example), CC BY-SA 4.0.

**Mediator** is a behavioral design pattern that reduces coupling between components of a program by making them communicate indirectly, through a special mediator object.

The Mediator makes it easy to modify, extend and reuse individual components because they’re no longer dependent on the dozens of other classes.

### Top-Down Ownership

Top-Down Ownership approach allows to apply Mediator in Rust as it is a suitable for Rust’s ownership model with strict borrow checker rules. It’s not the only way to implement Mediator, but it’s a fundamental one.

The key point is thinking in terms of OWNERSHIP.

1.   A mediator takes ownership of all components.

2.   A component doesn’t preserve a reference to a mediator. Instead, it gets the reference via a method call.

// A train gets a mediator object by reference.
pub trait Train {
    fn name(&self) -> &String;
    fn arrive(&mut self, mediator: &mut dyn Mediator);
    fn depart(&mut self, mediator: &mut dyn Mediator);
}

// Mediator has notification methods.
pub trait Mediator {
    fn notify_about_arrival(&mut self, train_name: &str) -> bool;
    fn notify_about_departure(&mut self, train_name: &str);
}
3.   Control flow starts from `fn main()` where the mediator receives external events/commands.

4.   `Mediator` trait for the interaction between components (`notify_about_arrival`, `notify_about_departure`) is not the same as its external API for receiving external events (`accept`, `depart` commands from the main loop).

let train1 = PassengerTrain::new("Train 1");
let train2 = FreightTrain::new("Train 2");

// Station has `accept` and `depart` methods,
// but it also implements `Mediator`.
let mut station = TrainStation::default();

// Station is taking ownership of the trains.
station.accept(train1);
station.accept(train2);

// `train1` and `train2` have been moved inside,
// but we can use train names to depart them.
station.depart("Train 1");
station.depart("Train 2");
station.depart("Train 3");

##### Extra info

There is a research and discussion of the Mediator pattern in Rust: [https://github.com/fadeevab/mediator-pattern-rust](https://github.com/fadeevab/mediator-pattern-rust)

##### **train_station.rs**
```rust
use std::collections::{HashMap, VecDeque};

use crate::trains::Train;

// Mediator has notification methods.
pub trait Mediator {
    fn notify_about_arrival(&mut self, train_name: &str) -> bool;
    fn notify_about_departure(&mut self, train_name: &str);
}

#[derive(Default)]
pub struct TrainStation {
    trains: HashMap<String, Box<dyn Train>>,
    train_queue: VecDeque<String>,
    train_on_platform: Option<String>,
}

impl Mediator for TrainStation {
    fn notify_about_arrival(&mut self, train_name: &str) -> bool {
        if self.train_on_platform.is_some() {
            self.train_queue.push_back(train_name.into());
            false
        } else {
            self.train_on_platform.replace(train_name.into());
            true
        }
    }

    fn notify_about_departure(&mut self, train_name: &str) {
        if Some(train_name.into()) == self.train_on_platform {
            self.train_on_platform = None;

            if let Some(next_train_name) = self.train_queue.pop_front() {
                let mut next_train = self.trains.remove(&next_train_name).unwrap();
                next_train.arrive(self);
                self.trains.insert(next_train_name.clone(), next_train);

                self.train_on_platform = Some(next_train_name);
            }
        }
    }
}

impl TrainStation {
    pub fn accept(&mut self, mut train: impl Train + 'static) {
        if self.trains.contains_key(train.name()) {
            println!("{} has already arrived", train.name());
            return;
        }

        train.arrive(self);
        self.trains.insert(train.name().clone(), Box::new(train));
    }

    pub fn depart(&mut self, name: &'static str) {
        let train = self.trains.remove(name);
        if let Some(mut train) = train {
            train.depart(self);
        } else {
            println!("'{}' is not on the station!", name);
        }
    }
}
```

##### **trains/mod.rs**
```rust
mod freight_train;
mod passenger_train;

pub use freight_train::FreightTrain;
pub use passenger_train::PassengerTrain;

use crate::train_station::Mediator;

// A train gets a mediator object by reference.
pub trait Train {
    fn name(&self) -> &String;
    fn arrive(&mut self, mediator: &mut dyn Mediator);
    fn depart(&mut self, mediator: &mut dyn Mediator);
}
```

##### **trains/freight_train.rs**
```rust
use super::Train;
use crate::train_station::Mediator;

pub struct FreightTrain {
    name: String,
}

impl FreightTrain {
    pub fn new(name: &'static str) -> Self {
        Self { name: name.into() }
    }
}

impl Train for FreightTrain {
    fn name(&self) -> &String {
        &self.name
    }

    fn arrive(&mut self, mediator: &mut dyn Mediator) {
        if !mediator.notify_about_arrival(&self.name) {
            println!("Freight train {}: Arrival blocked, waiting", self.name);
            return;
        }

        println!("Freight train {}: Arrived", self.name);
    }

    fn depart(&mut self, mediator: &mut dyn Mediator) {
        println!("Freight train {}: Leaving", self.name);
        mediator.notify_about_departure(&self.name);
    }
}
```

##### **trains/passenger_train.rs**
```rust
use super::Train;
use crate::train_station::Mediator;

pub struct PassengerTrain {
    name: String,
}

impl PassengerTrain {
    pub fn new(name: &'static str) -> Self {
        Self { name: name.into() }
    }
}

impl Train for PassengerTrain {
    fn name(&self) -> &String {
        &self.name
    }

    fn arrive(&mut self, mediator: &mut dyn Mediator) {
        if !mediator.notify_about_arrival(&self.name) {
            println!("Passenger train {}: Arrival blocked, waiting", self.name);
            return;
        }

        println!("Passenger train {}: Arrived", self.name);
    }

    fn depart(&mut self, mediator: &mut dyn Mediator) {
        println!("Passenger train {}: Leaving", self.name);
        mediator.notify_about_departure(&self.name);
    }
}
```

##### **main.rs:** Client code
```rust
mod train_station;
mod trains;

use train_station::TrainStation;
use trains::{FreightTrain, PassengerTrain};

fn main() {
    let train1 = PassengerTrain::new("Train 1");
    let train2 = FreightTrain::new("Train 2");

    // Station has `accept` and `depart` methods,
    // but it also implements `Mediator`.
    let mut station = TrainStation::default();

    // Station is taking ownership of the trains.
    station.accept(train1);
    station.accept(train2);

    // `train1` and `train2` have been moved inside,
    // but we can use train names to depart them.
    station.depart("Train 1");
    station.depart("Train 2");
    station.depart("Train 3");
}
```

#### Output
```text
Passenger train Train 1: Arrived
Freight train Train 2: Arrival blocked, waiting
Passenger train Train 1: Leaving
Freight train Train 2: Arrived
Freight train Train 2: Leaving
'Train 3' is not on the station!
```
