# bridge

Split an abstraction from its implementation so both can vary independently.

**Sources:** GOF:bridge

---

## Bridge (Gang of Four) (GOF:bridge)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/bridge/rust/example), CC BY-SA 4.0.

**Bridge** is a structural design pattern that divides business logic or huge class into separate class hierarchies that can be developed independently.

One of these hierarchies (often called the Abstraction) will get a reference to an object of the second hierarchy (Implementation). The abstraction will be able to delegate some (sometimes, most) of its calls to the implementations object. Since all implementations will have a common interface, they’d be interchangeable inside the abstraction.

### Devices and Remotes

This example illustrates how the Bridge pattern can help divide the monolithic code of an app that manages devices and their remote controls. The Device classes act as the implementation, whereas the Remotes act as the abstraction.

##### **remotes/mod.rs**
```rust
mod advanced;
mod basic;

pub use advanced::AdvancedRemote;
pub use basic::BasicRemote;

use crate::device::Device;

pub trait HasMutableDevice<D: Device> {
    fn device(&mut self) -> &mut D;
}

pub trait Remote<D: Device>: HasMutableDevice<D> {
    fn power(&mut self) {
        println!("Remote: power toggle");
        if self.device().is_enabled() {
            self.device().disable();
        } else {
            self.device().enable();
        }
    }

    fn volume_down(&mut self) {
        println!("Remote: volume down");
        let volume = self.device().volume();
        self.device().set_volume(volume - 10);
    }

    fn volume_up(&mut self) {
        println!("Remote: volume up");
        let volume = self.device().volume();
        self.device().set_volume(volume + 10);
    }

    fn channel_down(&mut self) {
        println!("Remote: channel down");
        let channel = self.device().channel();
        self.device().set_channel(channel - 1);
    }

    fn channel_up(&mut self) {
        println!("Remote: channel up");
        let channel = self.device().channel();
        self.device().set_channel(channel + 1);
    }
}
```

##### **remotes/basic.rs**
```rust
use crate::device::Device;

use super::{HasMutableDevice, Remote};

pub struct BasicRemote<D: Device> {
    device: D,
}

impl<D: Device> BasicRemote<D> {
    pub fn new(device: D) -> Self {
        Self { device }
    }
}

impl<D: Device> HasMutableDevice<D> for BasicRemote<D> {
    fn device(&mut self) -> &mut D {
        &mut self.device
    }
}

impl<D: Device> Remote<D> for BasicRemote<D> {}
```

##### **remotes/advanced.rs**
```rust
use crate::device::Device;

use super::{HasMutableDevice, Remote};

pub struct AdvancedRemote<D: Device> {
    device: D,
}

impl<D: Device> AdvancedRemote<D> {
    pub fn new(device: D) -> Self {
        Self { device }
    }

    pub fn mute(&mut self) {
        println!("Remote: mute");
        self.device.set_volume(0);
    }
}

impl<D: Device> HasMutableDevice<D> for AdvancedRemote<D> {
    fn device(&mut self) -> &mut D {
        &mut self.device
    }
}

impl<D: Device> Remote<D> for AdvancedRemote<D> {}
```

##### **device/mod.rs**
```rust
mod radio;
mod tv;

pub use radio::Radio;
pub use tv::Tv;

pub trait Device {
    fn is_enabled(&self) -> bool;
    fn enable(&mut self);
    fn disable(&mut self);
    fn volume(&self) -> u8;
    fn set_volume(&mut self, percent: u8);
    fn channel(&self) -> u16;
    fn set_channel(&mut self, channel: u16);
    fn print_status(&self);
}
```

##### **device/radio.rs**
```rust
use super::Device;

#[derive(Clone)]
pub struct Radio {
    on: bool,
    volume: u8,
    channel: u16,
}

impl Default for Radio {
    fn default() -> Self {
        Self {
            on: false,
            volume: 30,
            channel: 1,
        }
    }
}

impl Device for Radio {
    fn is_enabled(&self) -> bool {
        self.on
    }

    fn enable(&mut self) {
        self.on = true;
    }

    fn disable(&mut self) {
        self.on = false;
    }

    fn volume(&self) -> u8 {
        self.volume
    }

    fn set_volume(&mut self, percent: u8) {
        self.volume = std::cmp::min(percent, 100);
    }

    fn channel(&self) -> u16 {
        self.channel
    }

    fn set_channel(&mut self, channel: u16) {
        self.channel = channel;
    }

    fn print_status(&self) {
        println!("------------------------------------");
        println!("| I'm radio.");
        println!("| I'm {}", if self.on { "enabled" } else { "disabled" });
        println!("| Current volume is {}%", self.volume);
        println!("| Current channel is {}", self.channel);
        println!("------------------------------------\n");
    }
}
```

##### **device/tv.rs**
```rust
use super::Device;

#[derive(Clone)]
pub struct Tv {
    on: bool,
    volume: u8,
    channel: u16,
}

impl Default for Tv {
    fn default() -> Self {
        Self {
            on: false,
            volume: 30,
            channel: 1,
        }
    }
}

impl Device for Tv {
    fn is_enabled(&self) -> bool {
        self.on
    }

    fn enable(&mut self) {
        self.on = true;
    }

    fn disable(&mut self) {
        self.on = false;
    }

    fn volume(&self) -> u8 {
        self.volume
    }

    fn set_volume(&mut self, percent: u8) {
        self.volume = std::cmp::min(percent, 100);
    }

    fn channel(&self) -> u16 {
        self.channel
    }

    fn set_channel(&mut self, channel: u16) {
        self.channel = channel;
    }

    fn print_status(&self) {
        println!("------------------------------------");
        println!("| I'm TV set.");
        println!("| I'm {}", if self.on { "enabled" } else { "disabled" });
        println!("| Current volume is {}%", self.volume);
        println!("| Current channel is {}", self.channel);
        println!("------------------------------------\n");
    }
}
```

##### **main.rs**
```rust
mod device;
mod remotes;

use device::{Device, Radio, Tv};
use remotes::{AdvancedRemote, BasicRemote, HasMutableDevice, Remote};

fn main() {
    test_device(Tv::default());
    test_device(Radio::default());
}

fn test_device(device: impl Device + Clone) {
    println!("Tests with basic remote.");
    let mut basic_remote = BasicRemote::new(device.clone());
    basic_remote.power();
    basic_remote.device().print_status();

    println!("Tests with advanced remote.");
    let mut advanced_remote = AdvancedRemote::new(device);
    advanced_remote.power();
    advanced_remote.mute();
    advanced_remote.device().print_status();
}
```

#### Output
```text
Tests with basic remote.
Remote: power toggle
------------------------------------
| I'm TV set.
| I'm enabled
| Current volume is 30%
| Current channel is 1
------------------------------------

Tests with advanced remote.
Remote: power toggle
Remote: mute
------------------------------------
| I'm TV set.
| I'm enabled
| Current volume is 0%
| Current channel is 1
------------------------------------

Tests with basic remote.
Remote: power toggle
------------------------------------
| I'm radio.
| I'm enabled
| Current volume is 30%
| Current channel is 1
------------------------------------

Tests with advanced remote.
Remote: power toggle
Remote: mute
------------------------------------
| I'm radio.
| I'm enabled
| Current volume is 0%
| Current channel is 1
------------------------------------```
```
