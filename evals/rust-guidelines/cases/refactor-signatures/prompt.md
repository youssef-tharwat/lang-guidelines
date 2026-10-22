---
description: Refactor a module with common signature, naming, cloning and string-building mistakes.
tags: [signatures, naming, ownership, style]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

Refactor this Rust module into idiomatic, well-designed Rust. Keep its behavior. `Item` lives in `crate::model` and has `name: String`, `qty: u32` and `price: f64`.

```rust
pub mod report {
    pub use crate::model::*;

    pub fn total(items: &Vec<Item>) -> f64 {
        let mut sum = 0.0;
        for i in items.clone() {
            sum += i.price;
        }
        sum
    }

    pub fn find(items: &Vec<Item>, name: &String) -> Option<(String, u32, u32)> {
        let found = items.iter().find(|i| &i.name == name);
        if found.is_some() {
            let i = found.unwrap();
            return Some((i.name.clone(), i.qty, i.price as u32));
        }
        None
    }

    pub fn render(items: &Vec<Item>, verbose: bool) -> String {
        let mut out = String::new();
        for i in items {
            out = out + &i.name + ": " + &i.qty.to_string() + "\n";
            if verbose {
                out = out + "  price " + &i.price.to_string() + "\n";
            }
        }
        out
    }

    pub struct Report {
        name: String,
    }

    impl Report {
        pub fn get_name(&self) -> &String {
            &self.name
        }
    }
}
```

Write the complete refactored module to `report.rs` in the current directory, then reply with a short list of what you changed.
