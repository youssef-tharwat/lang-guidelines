# log-not-print

Production code reports diagnostics through the telemetry framework, never `println!` or `dbg!`; stdout is only for CLIs whose interface it is.

**Why:** Console output can't be filtered, routed or correlated.

**Sources:** M-LOG-NOT-PRINT

---

## Production code uses telemetry, not println (M-LOG-NOT-PRINT)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Production code paths should emit diagnostics through the project's telemetry framework rather than via `println!` or `dbg!`. Console output is reserved for CLIs that intentionally write to stdout as their user interface.
