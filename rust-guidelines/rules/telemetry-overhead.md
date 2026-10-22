# telemetry-overhead

Keep library telemetry out of hot inner loops; events that must be there are cheap and allocation-free (no `format!`), or summarize the batch instead.

**Why:** Assume telemetry is always on, under load.

**Binding in:** libraries (code other packages depend on); a strong recommendation in application-only code.

**Sources:** M-LOG-OVERHEAD

---

## Library telemetry does not tank performance (M-LOG-OVERHEAD)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Library code that emits telemetry should ensure that doing so does not meaningfully impact throughput or latency on the hot path.

Crates offered to 3rd parties emitting logs or metrics should assume telemetry will be permanently enabled, or under load. Care should therefore be taken that the volume and overhead of emitted events is reasonable, and will not cause excessive performance degradation.

Hot, inner loops should preferably stay free of telemetry emission entirely. If it can't be avoided, the events emitted should be lightweight and avoid allocations (e.g., `format!` string concatenation).

```rust
// Bad, logs each message and invokes allocation-based formatting.
for m in messages {
    log(format!("Emitting message {}", m.id()))
}

// Better, avoids per-message allocations.
for m in messages {
    log(("Emitting message", m.id()))
}

// Best: If possible, let telemetry users reconstruct what happened offline 
log(("Processing message batch", messages.batch_id()))
for m in messages { ... }
```
