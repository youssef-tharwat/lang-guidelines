# factory-method

Let implementors choose which concrete type a shared algorithm creates.

**Sources:** GOF:factory-method

---

## Factory Method (Gang of Four) (GOF:factory-method)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/factory-method/rust/example), CC BY-SA 4.0.

**Factory method** is a creational design pattern which solves the problem of creating product objects without specifying their concrete classes.

The Factory Method defines a method, which should be used for creating objects instead of using a direct constructor call (`new` operator). Subclasses can override this method to change the class of objects that will be created.

> If you can’t figure out the difference between various factory patterns and concepts, then read our [Factory Comparison](https://refactoring.guru/design-patterns/factory-comparison).

### Dialog Rendering

This example illustrates how to organize a GUI framework into independent modules using **dynamic dispatch**:

1.   The `gui` module defines interfaces for all the components.

 It has no external dependencies.
2.   The `html_gui` module provides HTML implementation of the base GUI.

 Depends on `gui`.
3.   The `windows_gui` module provides Windows implementation of the base GUI.

 Depends on `gui`.

The `app` is a client application that can use several implementations of the GUI framework, depending on the current environment or configuration. However, most of the app code doesn’t depend on specific types of GUI elements. All client code works with GUI elements through abstract interfaces defined by the `gui` module.

The [Abstract Factory example](https://refactoring.guru/design-patterns/abstract-factory/rust/example) demonstrates an even greater separation of a factory interface and its implementations.

##### **gui.rs:** Product & Creator
```rust
pub trait Button {
    fn render(&self);
    fn on_click(&self);
}

/// Dialog has a factory method `create_button`.
///
/// It creates different buttons depending on a factory implementation.
pub trait Dialog {
    /// The factory method. It must be overridden with a concrete implementation.
    fn create_button(&self) -> Box<dyn Button>;

    fn render(&self) {
        let button = self.create_button();
        button.render();
    }

    fn refresh(&self) {
        println!("Dialog - Refresh");
    }
}
```

##### **html_gui.rs:** Concrete creator
```rust
use crate::gui::{Button, Dialog};

pub struct HtmlButton;

impl Button for HtmlButton {
    fn render(&self) {
        println!("<button>Test Button</button>");
        self.on_click();
    }

    fn on_click(&self) {
        println!("Click! Button says - 'Hello World!'");
    }
}

pub struct HtmlDialog;

impl Dialog for HtmlDialog {
    /// Creates an HTML button.
    fn create_button(&self) -> Box<dyn Button> {
        Box::new(HtmlButton)
    }
}
```

##### **windows_gui.rs:** Another concrete creator
```rust
use crate::gui::{Button, Dialog};

pub struct WindowsButton;

impl Button for WindowsButton {
    fn render(&self) {
        println!("Drawing a Windows button");
        self.on_click();
    }

    fn on_click(&self) {
        println!("Click! Hello, Windows!");
    }
}

pub struct WindowsDialog;

impl Dialog for WindowsDialog {
    /// Creates a Windows button.
    fn create_button(&self) -> Box<dyn Button> {
        Box::new(WindowsButton)
    }
}
```

##### **init.rs:** Initialization code
```rust
use crate::gui::Dialog;
use crate::html_gui::HtmlDialog;
use crate::windows_gui::WindowsDialog;

pub fn initialize() -> &'static dyn Dialog {
    // The dialog type is selected depending on the environment settings or configuration.
    if cfg!(windows) {
        println!("-- Windows detected, creating Windows GUI --");
        &WindowsDialog
    } else {
        println!("-- No OS detected, creating the HTML GUI --");
        &HtmlDialog
    }
}
```

##### **main.rs:** Client code
```rust
mod gui;
mod html_gui;
mod init;
mod windows_gui;

use init::initialize;

fn main() {
    // The rest of the code doesn't depend on specific dialog types, because
    // it works with all dialog objects via the abstract `Dialog` trait
    // which is defined in the `gui` module.
    let dialog = initialize();
    dialog.render();
    dialog.refresh();
}
```

#### Output
```text
<button>Test Button</button>
Click! Button says - 'Hello World!'
Dialog - Refresh
```

### Maze Game

This example illustrates how to implement the Factory Method pattern using **static dispatch** (generics).

_Inspired by the Factory Method [example from the GoF book](https://en.wikipedia.org/wiki/Factory\_method\_pattern)._

##### **game.rs**
```rust
/// Maze room that is going to be instantiated with a factory method.
pub trait Room {
    fn render(&self);
}

/// Maze game has a factory method producing different rooms.
pub trait MazeGame {
    type RoomImpl: Room;

    /// A factory method.
    fn rooms(&self) -> Vec<Self::RoomImpl>;

    fn play(&self) {
        for room in self.rooms() {
            room.render();
        }
    }
}

/// The client code initializes resources and does other preparations
/// then it uses a factory to construct and run the game.
pub fn run(maze_game: impl MazeGame) {
    println!("Loading resources...");
    println!("Starting the game...");

    maze_game.play();
}
```

##### **magic_maze.rs**
```rust
use super::game::{MazeGame, Room};

#[derive(Clone)]
pub struct MagicRoom {
    title: String,
}

impl MagicRoom {
    pub fn new(title: String) -> Self {
        Self { title }
    }
}

impl Room for MagicRoom {
    fn render(&self) {
        println!("Magic Room: {}", self.title);
    }
}

pub struct MagicMaze {
    rooms: Vec<MagicRoom>,
}

impl MagicMaze {
    pub fn new() -> Self {
        Self {
            rooms: vec![
                MagicRoom::new("Infinite Room".into()),
                MagicRoom::new("Red Room".into()),
            ],
        }
    }
}

impl MazeGame for MagicMaze {
    type RoomImpl = MagicRoom;

    fn rooms(&self) -> Vec<Self::RoomImpl> {
        self.rooms.clone()
    }
}
```

##### **ordinary_maze.rs**
```rust
use super::game::{MazeGame, Room};

#[derive(Clone)]
pub struct OrdinaryRoom {
    id: u32,
}

impl OrdinaryRoom {
    pub fn new(id: u32) -> Self {
        Self { id }
    }
}

impl Room for OrdinaryRoom {
    fn render(&self) {
        println!("Ordinary Room: #{}", self.id);
    }
}

pub struct OrdinaryMaze {
    rooms: Vec<OrdinaryRoom>,
}

impl OrdinaryMaze {
    pub fn new() -> Self {
        Self {
            rooms: vec![OrdinaryRoom::new(1), OrdinaryRoom::new(2)],
        }
    }
}

impl MazeGame for OrdinaryMaze {
    type RoomImpl = OrdinaryRoom;

    fn rooms(&self) -> Vec<Self::RoomImpl> {
        let mut rooms = self.rooms.clone();
        rooms.reverse();
        rooms
    }
}
```

##### **main.rs:** Client code
```rust
mod game;
mod magic_maze;
mod ordinary_maze;

use magic_maze::MagicMaze;
use ordinary_maze::OrdinaryMaze;

/// The game runs with different mazes depending on the concrete factory type:
/// it's either an ordinary maze or a magic maze.
///
/// For demonstration purposes, both mazes are used to construct the game.
fn main() {
    // Option 1: The game starts with an ordinary maze.
    let ordinary_maze = OrdinaryMaze::new();
    game::run(ordinary_maze);

    // Option 2: The game starts with a magic maze.
    let magic_maze = MagicMaze::new();
    game::run(magic_maze);
}
```

#### Output
```text
Loading resources...
Starting the game...
Magic Room: Infinite Room
Magic Room: Red Room
Loading resources...
Starting the game...
Ordinary Room: #2
Ordinary Room: #1
```
