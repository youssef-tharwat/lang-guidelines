# state

Change behavior with internal state by delegating to state objects.

**Sources:** GOF:state

---

## State (Gang of Four) (GOF:state)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/state/rust/example), CC BY-SA 4.0.

**State** is a behavioral design pattern that allows an object to change the behavior when its internal state changes.

The pattern extracts state-related behaviors into separate state classes and forces the original object to delegate the work to an instance of these classes, instead of acting on its own.

The **State** pattern is related to a finite-state machine (FSM) concept, however, instead of implementing a lot of conditional statements, each state is represented by a separate type that implements a common state trait. Transitions between states depend on the particular trait implementation for each state type.

The State Pattern in Rust is described in detail in [The Rust Book](https://doc.rust-lang.org/book/ch17-03-oo-design-patterns.html).

### Music Player

Let’s build a music player with the following state transitions:

There is a base trait `State` with `play` and `stop` methods which make state transitions:

pub trait State {
    fn play(self: Box<Self>, player: &mut Player) -> Box<dyn State>;
    fn stop(self: Box<Self>, player: &mut Player) -> Box<dyn State>;
}

`next` and `prev` don’t change state, there are default implementations in a separate `impl dyn State` block that cannot be overridden.

impl dyn State {
    pub fn next(self: Box<Self>, player: &mut Player) -> Box<dyn State> {
        self
    }

    pub fn prev(self: Box<Self>, player: &mut Player) -> Box<dyn State> {
        self
    }
}

Every state is a type implementing the `trait State`:

pub struct StoppedState;
pub struct PausedState;
pub struct PlayingState;

impl State for StoppedState {
    ...
}

impl State for PausedState {
    ...
}

Anyways, it works as follows:

let state = Box::new(StoppedState);   // StoppedState.
let state = state.play(&mut player);  // StoppedState -> PlayingState.
let state = state.play(&mut player);  // PlayingState -> PausedState.

Here, the same action `play` makes a transition to different states depending on where it’s called from:

1.   `StoppedState`'s implementation of `play` starts playback and returns `PlayingState`.

fn play(self: Box<Self>, player: &mut Player) -> Box<dyn State> {
    player.play();

    // Stopped -> Playing.
    Box::new(PlayingState)
}
2.   `PlayingState` pauses playback after hitting the “play” button again:

fn play(self: Box<Self>, player: &mut Player) -> Box<dyn State> {
    player.pause();

    // Playing -> Paused.
    Box::new(PausedState)
}

The methods are defined with a special `self: Box<Self>` notation.

Why is that?

1.   First, `self` is not a reference, it means that the method is a “one shot”, it consumes `self` and exchanges onto another state returning `Box<dyn State>`.
2.   Second, the method consumes the boxed object like `Box<dyn State>` and not an object of a concrete type like `PlayingState`, because the concrete state is unknown at compile time.

##### **player.rs**
```rust
/// A music track.
pub struct Track {
    pub title: String,
    pub duration: u32,
    cursor: u32,
}

impl Track {
    pub fn new(title: &'static str, duration: u32) -> Self {
        Self {
            title: title.into(),
            duration,
            cursor: 0,
        }
    }
}

/// A music player holds a playlist and it can do basic operations over it.
pub struct Player {
    playlist: Vec<Track>,
    current_track: usize,
    _volume: u8,
}

impl Default for Player {
    fn default() -> Self {
        Self {
            playlist: vec![
                Track::new("Track 1", 180),
                Track::new("Track 2", 165),
                Track::new("Track 3", 197),
                Track::new("Track 4", 205),
            ],
            current_track: 0,
            _volume: 25,
        }
    }
}

impl Player {
    pub fn next_track(&mut self) {
        self.current_track = (self.current_track + 1) % self.playlist.len();
    }

    pub fn prev_track(&mut self) {
        self.current_track = (self.playlist.len() + self.current_track - 1) % self.playlist.len();
    }

    pub fn play(&mut self) {
        self.track_mut().cursor = 10; // Playback imitation.
    }

    pub fn pause(&mut self) {
        self.track_mut().cursor = 43; // Paused at some moment.
    }

    pub fn rewind(&mut self) {
        self.track_mut().cursor = 0;
    }

    pub fn track(&self) -> &Track {
        &self.playlist[self.current_track]
    }

    fn track_mut(&mut self) -> &mut Track {
        &mut self.playlist[self.current_track]
    }
}
```

##### **state.rs**
```rust
use cursive::views::TextView;

use crate::player::Player;

pub struct StoppedState;
pub struct PausedState;
pub struct PlayingState;

/// There is a base `State` trait with methods `play` and `stop` which make
/// state transitions. There are also `next` and `prev` methods in a separate
/// `impl dyn State` block below, those are default implementations
/// that cannot be overridden.
///
/// What is the `self: Box<Self>` notation? We use the state as follows:
/// ```rust
///   let prev_state = Box::new(PlayingState);
///   let next_state = prev_state.play(&mut player);
/// ```
/// A method `play` receives a whole `Box<PlayingState>` object,
/// and not just `PlayingState`. The previous state "disappears" in the method,
/// in turn, it returns a new `Box<PausedState>` state object.
pub trait State {
    fn play(self: Box<Self>, player: &mut Player) -> Box<dyn State>;
    fn stop(self: Box<Self>, player: &mut Player) -> Box<dyn State>;
    fn render(&self, player: &Player, view: &mut TextView);
}

impl State for StoppedState {
    fn play(self: Box<Self>, player: &mut Player) -> Box<dyn State> {
        player.play();

        // Stopped -> Playing.
        Box::new(PlayingState)
    }

    fn stop(self: Box<Self>, _: &mut Player) -> Box<dyn State> {
        // Change no state.
        self
    }

    fn render(&self, _: &Player, view: &mut TextView) {
        view.set_content("[Stopped] Press 'Play'")
    }
}

impl State for PausedState {
    fn play(self: Box<Self>, player: &mut Player) -> Box<dyn State> {
        player.pause();

        // Paused -> Playing.
        Box::new(PlayingState)
    }

    fn stop(self: Box<Self>, player: &mut Player) -> Box<dyn State> {
        player.pause();
        player.rewind();

        // Paused -> Stopped.
        Box::new(StoppedState)
    }

    fn render(&self, player: &Player, view: &mut TextView) {
        view.set_content(format!(
            "[Paused] {} - {} sec",
            player.track().title,
            player.track().duration
        ))
    }
}

impl State for PlayingState {
    fn play(self: Box<Self>, player: &mut Player) -> Box<dyn State> {
        player.pause();

        // Playing -> Paused.
        Box::new(PausedState)
    }

    fn stop(self: Box<Self>, player: &mut Player) -> Box<dyn State> {
        player.pause();
        player.rewind();

        // Playing -> Stopped.
        Box::new(StoppedState)
    }

    fn render(&self, player: &Player, view: &mut TextView) {
        view.set_content(format!(
            "[Playing] {} - {} sec",
            player.track().title,
            player.track().duration
        ))
    }
}

// Default "next" and "prev" implementations for the trait.
impl dyn State {
    pub fn next(self: Box<Self>, player: &mut Player) -> Box<dyn State> {
        player.next_track();

        // Change no state.
        self
    }

    pub fn prev(self: Box<Self>, player: &mut Player) -> Box<dyn State> {
        player.prev_track();

        // Change no state.
        self
    }
}
```

##### **main.rs**
```rust
mod player;
mod state;

use cursive::{
    event::Key,
    view::Nameable,
    views::{Dialog, TextView},
    Cursive,
};
use player::Player;
use state::{State, StoppedState};

// Application context: a music player and a state.
struct PlayerApplication {
    player: Player,
    state: Box<dyn State>,
}

fn main() {
    let mut app = cursive::default();

    app.set_user_data(PlayerApplication {
        player: Player::default(),
        state: Box::new(StoppedState),
    });

    app.add_layer(
        Dialog::around(TextView::new("Press Play").with_name("Player Status"))
            .title("Music Player")
            .button("Play", |s| execute(s, "Play"))
            .button("Stop", |s| execute(s, "Stop"))
            .button("Prev", |s| execute(s, "Prev"))
            .button("Next", |s| execute(s, "Next")),
    );

    app.add_global_callback(Key::Esc, |s| s.quit());

    app.run();
}

fn execute(s: &mut Cursive, button: &'static str) {
    let PlayerApplication {
        mut player,
        mut state,
    } = s.take_user_data().unwrap();

    let mut view = s.find_name::<TextView>("Player Status").unwrap();

    // Here is how state mechanics work: the previous state
    // executes an action and returns a new state.
    // Each state has all 4 operations but reacts differently.
    state = match button {
        "Play" => state.play(&mut player),
        "Stop" => state.stop(&mut player),
        "Prev" => state.prev(&mut player),
        "Next" => state.next(&mut player),
        _ => unreachable!(),
    };

    state.render(&player, &mut view);

    s.set_user_data(PlayerApplication { player, state });
}
```

#### Screenshots
