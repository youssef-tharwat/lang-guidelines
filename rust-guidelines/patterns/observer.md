# observer

Let subscribers register for events and get notified of changes.

**Sources:** GOF:observer

---

## Observer (Gang of Four) (GOF:observer)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/observer/rust/example), CC BY-SA 4.0.

**Observer** is a behavioral design pattern that allows some objects to notify other objects about changes in their state.

The Observer pattern provides a way to subscribe and unsubscribe to and from these events for any object that implements a subscriber interface.
### Conceptual example

In Rust, a convenient way to define a subscriber is to have a function as a callable object with complex logic passing it to a event publisher.

In this Observer example, Subscribers are either _a lambda function_ or _an explicit function_ subscribed to the event. Explicit function objects could be also unsubscribed (although, there could be limitations for some function types).

##### **editor.rs**
```rust
use crate::observer::{Event, Publisher};

/// Editor has its own logic and it utilizes a publisher
/// to operate with subscribers and events.
#[derive(Default)]
pub struct Editor {
    publisher: Publisher,
    file_path: String,
}

impl Editor {
    pub fn events(&mut self) -> &mut Publisher {
        &mut self.publisher
    }

    pub fn load(&mut self, path: String) {
        self.file_path = path.clone();
        self.publisher.notify(Event::Load, path);
    }

    pub fn save(&self) {
        self.publisher.notify(Event::Save, self.file_path.clone());
    }
}
```

##### **observer.rs**
```rust
use std::collections::HashMap;

/// An event type.
#[derive(PartialEq, Eq, Hash, Clone)]
pub enum Event {
    Load,
    Save,
}

/// A subscriber (listener) has type of a callable function.
pub type Subscriber = fn(file_path: String);

/// Publisher sends events to subscribers (listeners).
#[derive(Default)]
pub struct Publisher {
    events: HashMap<Event, Vec<Subscriber>>,
}

impl Publisher {
    pub fn subscribe(&mut self, event_type: Event, listener: Subscriber) {
        self.events.entry(event_type.clone()).or_default();
        self.events.get_mut(&event_type).unwrap().push(listener);
    }

    pub fn unsubscribe(&mut self, event_type: Event, listener: Subscriber) {
        self.events
            .get_mut(&event_type)
            .unwrap()
            .retain(|&x| x != listener);
    }

    pub fn notify(&self, event_type: Event, file_path: String) {
        let listeners = self.events.get(&event_type).unwrap();
        for listener in listeners {
            listener(file_path.clone());
        }
    }
}
```

##### **main.rs**
```rust
use editor::Editor;
use observer::Event;

mod editor;
mod observer;

fn main() {
    let mut editor = Editor::default();

    editor.events().subscribe(Event::Load, |file_path| {
        let log = "/path/to/log/file.txt".to_string();
        println!("Save log to {}: Load file {}", log, file_path);
    });

    editor.events().subscribe(Event::Save, save_listener);

    editor.load("test1.txt".into());
    editor.load("test2.txt".into());
    editor.save();

    editor.events().unsubscribe(Event::Save, save_listener);
    editor.save();
}

fn save_listener(file_path: String) {
    let email = "admin@example.com".to_string();
    println!("Email to {}: Save file {}", email, file_path);
}
```

#### Output
```text
Save log to /path/to/log/file.txt: Load file test1.txt
Save log to /path/to/log/file.txt: Load file test2.txt
Email to admin@example.com: Save file test2.txt
```
