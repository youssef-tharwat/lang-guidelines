# builder

Construct complex objects step by step, optionally through a director; for API shape follow rule `builders`.

**Sources:** GOF:builder

---

## Builder (Gang of Four) (GOF:builder)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/builder/rust/example), CC BY-SA 4.0.

**Builder** is a creational design pattern, which allows constructing complex objects step by step.

Unlike other creational patterns, Builder doesn’t require products to have a common interface. That makes it possible to produce different products using the same construction process.

### Car & car manual builders

This slightly synthetic example illustrates how you can use the Builder pattern to construct totally different products using the same building process. For example, the trait `Builder` declares steps for assembling a car. However, depending on the builder implementation, a constructed object can be something different, for example, a car manual. The resulting manual will contain instructions from each building step, making it accurate and up-to-date.

The **Builder** design pattern is not the same as the **Fluent Interface** idiom (that relies on _method chaining_), although Rust developers sometimes use those terms interchangeably.

1.   **Fluent Interface** is a way to chain methods for constructing or modifying an object using the following approach:

let car = Car::default().places(5).gas(30)

It’s pretty elegant way to construct an object. Still, such a code may not be an instance of the Builder pattern.

2.   While the **Builder** pattern also suggests constructing object step by step, it also lets you build different types of products using the same construction process.

#### **builders:** Builders

##### **builders/mod.rs**
```rust
mod car;
mod car_manual;

use crate::components::{CarType, Engine, GpsNavigator, Transmission};

/// Builder defines how to assemble a car.
pub trait Builder {
    type OutputType;
    fn set_car_type(&mut self, car_type: CarType);
    fn set_seats(&mut self, seats: u16);
    fn set_engine(&mut self, engine: Engine);
    fn set_transmission(&mut self, transmission: Transmission);
    fn set_gps_navigator(&mut self, gps_navigator: GpsNavigator);
    fn build(self) -> Self::OutputType;
}

pub use car::CarBuilder;
pub use car_manual::CarManualBuilder;
```

##### **builders/car.rs**
```rust
use crate::{
    cars::Car,
    components::{CarType, Engine, GpsNavigator, Transmission},
};

use super::Builder;

pub const DEFAULT_FUEL: f64 = 5f64;

#[derive(Default)]
pub struct CarBuilder {
    car_type: Option<CarType>,
    engine: Option<Engine>,
    gps_navigator: Option<GpsNavigator>,
    seats: Option<u16>,
    transmission: Option<Transmission>,
}

impl Builder for CarBuilder {
    type OutputType = Car;

    fn set_car_type(&mut self, car_type: CarType) {
        self.car_type = Some(car_type);
    }

    fn set_engine(&mut self, engine: Engine) {
        self.engine = Some(engine);
    }

    fn set_gps_navigator(&mut self, gps_navigator: GpsNavigator) {
        self.gps_navigator = Some(gps_navigator);
    }

    fn set_seats(&mut self, seats: u16) {
        self.seats = Some(seats);
    }

    fn set_transmission(&mut self, transmission: Transmission) {
        self.transmission = Some(transmission);
    }

    fn build(self) -> Car {
        Car::new(
            self.car_type.expect("Please, set a car type"),
            self.seats.expect("Please, set a number of seats"),
            self.engine.expect("Please, set an engine configuration"),
            self.transmission.expect("Please, set up transmission"),
            self.gps_navigator,
            DEFAULT_FUEL,
        )
    }
}
```

##### **builders/car_manual.rs**
```rust
use crate::{
    cars::Manual,
    components::{CarType, Engine, GpsNavigator, Transmission},
};

use super::Builder;

#[derive(Default)]
pub struct CarManualBuilder {
    car_type: Option<CarType>,
    engine: Option<Engine>,
    gps_navigator: Option<GpsNavigator>,
    seats: Option<u16>,
    transmission: Option<Transmission>,
}

/// Builds a car manual instead of an actual car.
impl Builder for CarManualBuilder {
    type OutputType = Manual;

    fn set_car_type(&mut self, car_type: CarType) {
        self.car_type = Some(car_type);
    }

    fn set_engine(&mut self, engine: Engine) {
        self.engine = Some(engine);
    }

    fn set_gps_navigator(&mut self, gps_navigator: GpsNavigator) {
        self.gps_navigator = Some(gps_navigator);
    }

    fn set_seats(&mut self, seats: u16) {
        self.seats = Some(seats);
    }

    fn set_transmission(&mut self, transmission: Transmission) {
        self.transmission = Some(transmission);
    }

    fn build(self) -> Manual {
        Manual::new(
            self.car_type.expect("Please, set a car type"),
            self.seats.expect("Please, set a number of seats"),
            self.engine.expect("Please, set an engine configuration"),
            self.transmission.expect("Please, set up transmission"),
            self.gps_navigator,
        )
    }
}
```

#### **cars:** Products

##### **cars/mod.rs**
```rust
mod car;
mod manual;

pub use car::Car;
pub use manual::Manual;
```

##### **cars/car.rs**
```rust
use crate::components::{CarType, Engine, GpsNavigator, Transmission};

pub struct Car {
    car_type: CarType,
    seats: u16,
    engine: Engine,
    transmission: Transmission,
    gps_navigator: Option<GpsNavigator>,
    fuel: f64,
}

impl Car {
    pub fn new(
        car_type: CarType,
        seats: u16,
        engine: Engine,
        transmission: Transmission,
        gps_navigator: Option<GpsNavigator>,
        fuel: f64,
    ) -> Self {
        Self {
            car_type,
            seats,
            engine,
            transmission,
            gps_navigator,
            fuel,
        }
    }

    pub fn car_type(&self) -> CarType {
        self.car_type
    }

    pub fn fuel(&self) -> f64 {
        self.fuel
    }

    pub fn set_fuel(&mut self, fuel: f64) {
        self.fuel = fuel;
    }

    pub fn seats(&self) -> u16 {
        self.seats
    }

    pub fn engine(&self) -> &Engine {
        &self.engine
    }

    pub fn transmission(&self) -> &Transmission {
        &self.transmission
    }

    pub fn gps_navigator(&self) -> &Option<GpsNavigator> {
        &self.gps_navigator
    }
}
```

##### **cars/manual.rs**
```rust
use crate::components::{CarType, Engine, GpsNavigator, Transmission};

pub struct Manual {
    car_type: CarType,
    seats: u16,
    engine: Engine,
    transmission: Transmission,
    gps_navigator: Option<GpsNavigator>,
}

impl Manual {
    pub fn new(
        car_type: CarType,
        seats: u16,
        engine: Engine,
        transmission: Transmission,
        gps_navigator: Option<GpsNavigator>,
    ) -> Self {
        Self {
            car_type,
            seats,
            engine,
            transmission,
            gps_navigator,
        }
    }
}

impl std::fmt::Display for Manual {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "Type of car: {:?}", self.car_type)?;
        writeln!(f, "Count of seats: {}", self.seats)?;
        writeln!(
            f,
            "Engine: volume - {}; mileage - {}",
            self.engine.volume(),
            self.engine.mileage()
        )?;
        writeln!(f, "Transmission: {:?}", self.transmission)?;
        match self.gps_navigator {
            Some(_) => writeln!(f, "GPS Navigator: Functional")?,
            None => writeln!(f, "GPS Navigator: N/A")?,
        };
        Ok(())
    }
}
```

##### **components.rs:** Product components
```rust
#[derive(Copy, Clone, Debug)]
pub enum CarType {
    CityCar,
    SportsCar,
    Suv,
}

#[derive(Debug)]
pub enum Transmission {
    SingleSpeed,
    Manual,
    Automatic,
    SemiAutomatic,
}

pub struct Engine {
    volume: f64,
    mileage: f64,
    started: bool,
}

impl Engine {
    pub fn new(volume: f64, mileage: f64) -> Self {
        Self {
            volume,
            mileage,
            started: false,
        }
    }

    pub fn on(&mut self) {
        self.started = true;
    }

    pub fn off(&mut self) {
        self.started = false;
    }

    pub fn started(&self) -> bool {
        self.started
    }

    pub fn volume(&self) -> f64 {
        self.volume
    }

    pub fn mileage(&self) -> f64 {
        self.mileage
    }

    pub fn go(&mut self, mileage: f64) {
        if self.started() {
            self.mileage += mileage;
        } else {
            println!("Cannot go(), you must start engine first!");
        }
    }
}

pub struct GpsNavigator {
    route: String,
}

impl GpsNavigator {
    pub fn new() -> Self {
        Self::from_route(
            "221b, Baker Street, London  to Scotland Yard, 8-10 Broadway, London".into(),
        )
    }

    pub fn from_route(route: String) -> Self {
        Self { route }
    }

    pub fn route(&self) -> &String {
        &self.route
    }
}
```

##### **director.rs:** Directors
```rust
use crate::{
    builders::Builder,
    components::{CarType, Engine, GpsNavigator, Transmission},
};

/// Director knows how to build a car.
///
/// However, a builder can build a car manual instead of an actual car,
/// everything depends on the concrete builder.
pub struct Director;

impl Director {
    pub fn construct_sports_car(builder: &mut impl Builder) {
        builder.set_car_type(CarType::SportsCar);
        builder.set_seats(2);
        builder.set_engine(Engine::new(3.0, 0.0));
        builder.set_transmission(Transmission::SemiAutomatic);
        builder.set_gps_navigator(GpsNavigator::new());
    }

    pub fn construct_city_car(builder: &mut impl Builder) {
        builder.set_car_type(CarType::CityCar);
        builder.set_seats(2);
        builder.set_engine(Engine::new(1.2, 0.0));
        builder.set_transmission(Transmission::Automatic);
        builder.set_gps_navigator(GpsNavigator::new());
    }

    pub fn construct_suv(builder: &mut impl Builder) {
        builder.set_car_type(CarType::Suv);
        builder.set_seats(4);
        builder.set_engine(Engine::new(2.5, 0.0));
        builder.set_transmission(Transmission::Manual);
        builder.set_gps_navigator(GpsNavigator::new());
    }
}
```

##### **main.rs:** Client code
```rust
#![allow(unused)]

mod builders;
mod cars;
mod components;
mod director;

use builders::{Builder, CarBuilder, CarManualBuilder};
use cars::{Car, Manual};
use director::Director;

fn main() {
    let mut car_builder = CarBuilder::default();

    // Director gets the concrete builder object from the client
    // (application code). That's because application knows better which
    // builder to use to get a specific product.
    Director::construct_sports_car(&mut car_builder);

    // The final product is often retrieved from a builder object, since
    // Director is not aware and not dependent on concrete builders and
    // products.
    let car: Car = car_builder.build();
    println!("Car built: {:?}\n", car.car_type());

    let mut manual_builder = CarManualBuilder::default();

    // Director may know several building recipes.
    Director::construct_city_car(&mut manual_builder);

    // The final car manual.
    let manual: Manual = manual_builder.build();
    println!("Car manual built:\n{}", manual);
}
```

#### Output
```text
Car built: SportsCar

Car manual built:
Type of car: CityCar
Count of seats: 2
Engine: volume - 1.2; mileage - 0
Transmission: Automatic
GPS Navigator: Functional
```
