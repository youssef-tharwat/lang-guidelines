# command

Represent actions as values (trait objects, function pointers or closures) to queue, undo or log them.

**Sources:** P:patterns/behavioural/command, GOF:command

---

## Command (P:patterns/behavioural/command)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/patterns/behavioural/command.html), MPL-2.0.

### Description

The basic idea of the Command pattern is to separate out actions into its own
objects and pass them as parameters.

### Motivation

Suppose we have a sequence of actions or transactions encapsulated as objects.
We want these actions or commands to be executed or invoked in some order later
at different time. These commands may also be triggered as a result of some
event. For example, when a user pushes a button, or on arrival of a data packet.
In addition, these commands might be undoable. This may come in useful for
operations of an editor. We might want to store logs of executed commands so
that we could reapply the changes later if the system crashes.

### Example

Define two database operations `create table` and `add field`. Each of these
operations is a command which knows how to undo the command, e.g., `drop table`
and `remove field`. When a user invokes a database migration operation then each
command is executed in the defined order, and when the user invokes the rollback
operation then the whole set of commands is invoked in reverse order.

### Approach: Using trait objects

We define a common trait which encapsulates our command with two operations
`execute` and `rollback`. All command `structs` must implement this trait.

```rust
pub trait Migration {
    fn execute(&self) -> &str;
    fn rollback(&self) -> &str;
}

pub struct CreateTable;
impl Migration for CreateTable {
    fn execute(&self) -> &str {
        "create table"
    }
    fn rollback(&self) -> &str {
        "drop table"
    }
}

pub struct AddField;
impl Migration for AddField {
    fn execute(&self) -> &str {
        "add field"
    }
    fn rollback(&self) -> &str {
        "remove field"
    }
}

struct Schema {
    commands: Vec<Box<dyn Migration>>,
}

impl Schema {
    fn new() -> Self {
        Self { commands: vec![] }
    }

    fn add_migration(&mut self, cmd: Box<dyn Migration>) {
        self.commands.push(cmd);
    }

    fn execute(&self) -> Vec<&str> {
        self.commands.iter().map(|cmd| cmd.execute()).collect()
    }
    fn rollback(&self) -> Vec<&str> {
        self.commands
            .iter()
            .rev() // reverse iterator's direction
            .map(|cmd| cmd.rollback())
            .collect()
    }
}

fn main() {
    let mut schema = Schema::new();

    let cmd = Box::new(CreateTable);
    schema.add_migration(cmd);
    let cmd = Box::new(AddField);
    schema.add_migration(cmd);

    assert_eq!(vec!["create table", "add field"], schema.execute());
    assert_eq!(vec!["remove field", "drop table"], schema.rollback());
}
```

### Approach: Using function pointers

We could follow another approach by creating each individual command as a
different function and store function pointers to invoke these functions later
at a different time. Since function pointers implement all three traits `Fn`,
`FnMut`, and `FnOnce` we could as well pass and store closures instead of
function pointers.

```rust
type FnPtr = fn() -> String;
struct Command {
    execute: FnPtr,
    rollback: FnPtr,
}

struct Schema {
    commands: Vec<Command>,
}

impl Schema {
    fn new() -> Self {
        Self { commands: vec![] }
    }
    fn add_migration(&mut self, execute: FnPtr, rollback: FnPtr) {
        self.commands.push(Command { execute, rollback });
    }
    fn execute(&self) -> Vec<String> {
        self.commands.iter().map(|cmd| (cmd.execute)()).collect()
    }
    fn rollback(&self) -> Vec<String> {
        self.commands
            .iter()
            .rev()
            .map(|cmd| (cmd.rollback)())
            .collect()
    }
}

fn add_field() -> String {
    "add field".to_string()
}

fn remove_field() -> String {
    "remove field".to_string()
}

fn main() {
    let mut schema = Schema::new();
    schema.add_migration(|| "create table".to_string(), || "drop table".to_string());
    schema.add_migration(add_field, remove_field);
    assert_eq!(vec!["create table", "add field"], schema.execute());
    assert_eq!(vec!["remove field", "drop table"], schema.rollback());
}
```

### Approach: Using `Fn` trait objects

Finally, instead of defining a common command trait we could store each command
implementing the `Fn` trait separately in vectors.

```rust
type Migration<'a> = Box<dyn Fn() -> &'a str>;

struct Schema<'a> {
    executes: Vec<Migration<'a>>,
    rollbacks: Vec<Migration<'a>>,
}

impl<'a> Schema<'a> {
    fn new() -> Self {
        Self {
            executes: vec![],
            rollbacks: vec![],
        }
    }
    fn add_migration<E, R>(&mut self, execute: E, rollback: R)
    where
        E: Fn() -> &'a str + 'static,
        R: Fn() -> &'a str + 'static,
    {
        self.executes.push(Box::new(execute));
        self.rollbacks.push(Box::new(rollback));
    }
    fn execute(&self) -> Vec<&str> {
        self.executes.iter().map(|cmd| cmd()).collect()
    }
    fn rollback(&self) -> Vec<&str> {
        self.rollbacks.iter().rev().map(|cmd| cmd()).collect()
    }
}

fn add_field() -> &'static str {
    "add field"
}

fn remove_field() -> &'static str {
    "remove field"
}

fn main() {
    let mut schema = Schema::new();
    schema.add_migration(|| "create table", || "drop table");
    schema.add_migration(add_field, remove_field);
    assert_eq!(vec!["create table", "add field"], schema.execute());
    assert_eq!(vec!["remove field", "drop table"], schema.rollback());
}
```

### Discussion

If our commands are small and may be defined as functions or passed as a closure
then using function pointers might be preferable since it does not exploit
dynamic dispatch. But if our command is a whole struct with a bunch of functions
and variables defined as separated module then using trait objects would be more
suitable. A case of application can be found in [`actix`](https://actix.rs/),
which uses trait objects when it registers a handler function for routes. In
case of using `Fn` trait objects we can create and use commands in the same way
as we used in case of function pointers.

As performance, there is always a trade-off between performance and code
simplicity and organisation. Static dispatch gives faster performance, while
dynamic dispatch provides flexibility when we structure our application.

### See also

- [Command pattern](https://en.wikipedia.org/wiki/Command_pattern)

- [Another example for the `command` pattern](https://web.archive.org/web/20210223131236/https://chercher.tech/rust/command-design-pattern-rust)


## Command (Gang of Four) (GOF:command)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/command/rust/example), CC BY-SA 4.0.

**Command** is behavioral design pattern that converts requests or simple operations into objects.

The conversion allows deferred or remote execution of commands, storing command history,etc.

In Rust, a command instance should _NOT hold a permanent reference to global context_, instead the latter should be passed _from top to down as a mutable parameter_ of the “`execute`” method:

fn execute(&mut self, app: &mut cursive::Cursive) -> bool;

#### Text Editor: Commands and Undo

Key points:

*   Each button runs a separate command.
*   Because a command is represented as an object, it can be pushed into a `history` array in order to be undone later.
*   TUI is created with `cursive` crate.

###### **command.rs:** Command Inteface
```rust
mod copy;
mod cut;
mod paste;

pub use copy::CopyCommand;
pub use cut::CutCommand;
pub use paste::PasteCommand;

/// Declares a method for executing (and undoing) a command.
///
/// Each command receives an application context to access
/// visual components (e.g. edit view) and a clipboard.
pub trait Command {
    fn execute(&mut self, app: &mut cursive::Cursive) -> bool;
    fn undo(&mut self, app: &mut cursive::Cursive);
}
```

###### **command/copy.rs:** Copy Command
```rust
use cursive::{views::EditView, Cursive};

use super::Command;
use crate::AppContext;

#[derive(Default)]
pub struct CopyCommand;

impl Command for CopyCommand {
    fn execute(&mut self, app: &mut Cursive) -> bool {
        let editor = app.find_name::<EditView>("Editor").unwrap();
        let mut context = app.take_user_data::<AppContext>().unwrap();

        context.clipboard = editor.get_content().to_string();

        app.set_user_data(context);
        false
    }

    fn undo(&mut self, _: &mut Cursive) {}
}
```

###### **command/cut.rs:** Cut Command
```rust
use cursive::{views::EditView, Cursive};

use super::Command;
use crate::AppContext;

#[derive(Default)]
pub struct CutCommand {
    backup: String,
}

impl Command for CutCommand {
    fn execute(&mut self, app: &mut Cursive) -> bool {
        let mut editor = app.find_name::<EditView>("Editor").unwrap();

        app.with_user_data(|context: &mut AppContext| {
            self.backup = editor.get_content().to_string();
            context.clipboard = self.backup.clone();
            editor.set_content("".to_string());
        });

        true
    }

    fn undo(&mut self, app: &mut Cursive) {
        let mut editor = app.find_name::<EditView>("Editor").unwrap();
        editor.set_content(&self.backup);
    }
}
```

###### **command/paste.rs:** Paste Command
```rust
use cursive::{views::EditView, Cursive};

use super::Command;
use crate::AppContext;

#[derive(Default)]
pub struct PasteCommand {
    backup: String,
}

impl Command for PasteCommand {
    fn execute(&mut self, app: &mut Cursive) -> bool {
        let mut editor = app.find_name::<EditView>("Editor").unwrap();

        app.with_user_data(|context: &mut AppContext| {
            self.backup = editor.get_content().to_string();
            editor.set_content(context.clipboard.clone());
        });

        true
    }

    fn undo(&mut self, app: &mut Cursive) {
        let mut editor = app.find_name::<EditView>("Editor").unwrap();
        editor.set_content(&self.backup);
    }
}
```

###### **main.rs:** Client code
```rust
mod command;

use cursive::{
    traits::Nameable,
    views::{Dialog, EditView},
    Cursive,
};

use command::{Command, CopyCommand, CutCommand, PasteCommand};

/// An application context to be passed into visual component callbacks.
/// It contains a clipboard and a history of commands to be undone.
#[derive(Default)]
struct AppContext {
    clipboard: String,
    history: Vec<Box<dyn Command>>,
}

fn main() {
    let mut app = cursive::default();

    app.set_user_data(AppContext::default());
    app.add_layer(
        Dialog::around(EditView::default().with_name("Editor"))
            .title("Type and use buttons")
            .button("Copy", |s| execute(s, CopyCommand))
            .button("Cut", |s| execute(s, CutCommand::default()))
            .button("Paste", |s| execute(s, PasteCommand::default()))
            .button("Undo", undo)
            .button("Quit", |s| s.quit()),
    );

    app.run();
}

/// Executes a command and then pushes it to a history array.
fn execute(app: &mut Cursive, mut command: impl Command + 'static) {
    if command.execute(app) {
        app.with_user_data(|context: &mut AppContext| {
            context.history.push(Box::new(command));
        });
    }
}

/// Pops the last command and executes an undo action.
fn undo(app: &mut Cursive) {
    let mut context = app.take_user_data::<AppContext>().unwrap();
    if let Some(mut command) = context.history.pop() {
        command.undo(app)
    }
    app.set_user_data(context);
}
```

### Output
