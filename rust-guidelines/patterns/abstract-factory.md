# abstract-factory

Create families of related objects behind one factory trait, with static or dynamic dispatch.

**Sources:** GOF:abstract-factory

---

## Abstract Factory (Gang of Four) (GOF:abstract-factory)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/abstract-factory/rust/example), CC BY-SA 4.0.

**Abstract Factory** is a creational design pattern, which solves the problem of creating entire product families without specifying their concrete classes.

Abstract Factory defines an interface for creating all distinct products but leaves the actual product creation to concrete factory classes. Each factory type corresponds to a certain product variety.

The client code calls the creation methods of a factory object instead of creating products directly with a constructor call (`new` operator). Since a factory corresponds to a single product variant, all its products will be compatible.

Client code works with factories and products only through their abstract interfaces. This lets the client code work with any product variants, created by the factory object. You just create a new concrete factory class and pass it to the client code.

> If you can’t figure out the difference between various factory patterns and concepts, then read our [Factory Comparison](https://refactoring.guru/design-patterns/factory-comparison).
gui 

macos-gui 

windows-gui 

app 

app-dyn 

### GUI Elements Factory

This example illustrates how a GUI framework can organize its classes into independent libraries:

1.   The `gui` library defines interfaces for all the components.

 It has no external dependencies.
2.   The `windows-gui` library provides Windows implementation of the base GUI.

 Depends on `gui`.
3.   The `macos-gui` library provides Mac OS implementation of the base GUI.

 Depends on `gui`.

The `app` is a client application that can use several implementations of the GUI framework, depending on the current environment or configuration. However, most of the `app` code _doesn’t depend on specific types of GUI elements_. All the client code works with GUI elements through abstract interfaces (traits) defined by the `gui` lib.

There are two approaches to implementing abstract factories in Rust:

*   using generics (_static dispatch_)
*   using dynamic allocation (_dynamic dispatch_)

When you’re given a choice between static and dynamic dispatch, there is rarely a clear-cut correct answer. You’ll want to use static dispatch in your libraries and dynamic dispatch in your binaries. In a library, you want to allow your users to decide what kind of dispatch is best for them since you don’t know what their needs are. If you use dynamic dispatch, they’re forced to do the same, whereas if you use static dispatch, they can choose whether to use dynamic dispatch or not.

#### **gui:** Abstract Factory and Abstract Products

##### **gui/lib.rs**
```rust
pub trait Button {
    fn press(&self);
}

pub trait Checkbox {
    fn switch(&self);
}

/// Abstract Factory defined using generics.
pub trait GuiFactory {
    type B: Button;
    type C: Checkbox;

    fn create_button(&self) -> Self::B;
    fn create_checkbox(&self) -> Self::C;
}

/// Abstract Factory defined using Box pointer.
pub trait GuiFactoryDynamic {
    fn create_button(&self) -> Box<dyn Button>;
    fn create_checkbox(&self) -> Box<dyn Checkbox>;
}
```

#### **macos-gui:** One family of products

##### **macos-gui/lib.rs**
```rust
pub mod button;
pub mod checkbox;
pub mod factory;
```

#### **windows-gui:** Another family of products

##### **windows-gui/lib.rs**
```rust
pub mod button;
pub mod checkbox;
pub mod factory;
```

##### Static dispatch

Here, the abstract factory is implemented via **generics** which lets the compiler create a code that does NOT require dynamic dispatch in runtime.

#### **app:** Client code with static dispatch

##### **app/main.rs**
```rust
mod render;

use render::render;

use macos_gui::factory::MacFactory;
use windows_gui::factory::WindowsFactory;

fn main() {
    let windows = true;

    if windows {
        render(WindowsFactory);
    } else {
        render(MacFactory);
    }
}
```

##### **app/render.rs**
```rust
//! The code demonstrates that it doesn't depend on a concrete
//! factory implementation.

use gui::GuiFactory;

// Renders GUI. Factory object must be passed as a parameter to such the
// generic function with factory invocation to utilize static dispatch.
pub fn render(factory: impl GuiFactory) {
    let button1 = factory.create_button();
    let button2 = factory.create_button();
    let checkbox1 = factory.create_checkbox();
    let checkbox2 = factory.create_checkbox();

    use gui::{Button, Checkbox};

    button1.press();
    button2.press();
    checkbox1.switch();
    checkbox2.switch();
}
```

##### Dynamic dispatch

If a concrete type of abstract factory is not known at the compilation time, then is should be implemented using `Box` pointers.

#### **app-dyn:** Client code with dynamic dispatch

##### **app-dyn/main.rs**
```rust
mod render;

use render::render;

use gui::GuiFactoryDynamic;
use macos_gui::factory::MacFactory;
use windows_gui::factory::WindowsFactory;

fn main() {
    let windows = false;

    // Allocate a factory object in runtime depending on unpredictable input.
    let factory: &dyn GuiFactoryDynamic = if windows {
        &WindowsFactory
    } else {
        &MacFactory
    };

    // Factory invocation can be inlined right here.
    let button = factory.create_button();
    button.press();

    // Factory object can be passed to a function as a parameter.
    render(factory);
}
```

##### **app-dyn/render.rs**
```rust
//! The code demonstrates that it doesn't depend on a concrete
//! factory implementation.

use gui::GuiFactoryDynamic;

/// Renders GUI.
pub fn render(factory: &dyn GuiFactoryDynamic) {
    let button1 = factory.create_button();
    let button2 = factory.create_button();
    let checkbox1 = factory.create_checkbox();
    let checkbox2 = factory.create_checkbox();

    button1.press();
    button2.press();
    checkbox1.switch();
    checkbox2.switch();
}
```

#### Output
```text
Windows button has pressed
Windows button has pressed
Windows checkbox has switched
Windows checkbox has switched
```
