---
name: rust-guidelines
description: Enforce Microsoft Rust guidelines (design) and community Rust patterns (rust-unofficial + 22 GoF from refactoring.guru) for all Rust code generation and edits. Rules must be applied while writing code, not only in review. Triggers on any task that writes, edits, or refactors Rust code. Mechanical / style / correctness checks are left to rustc + clippy — this skill covers design decisions only.
---

# Rust Development Guidelines

Every rule in `guidelines.txt` and `patterns.md` is a hard constraint. Apply
them **while writing code**, not only during review. Mechanical correctness,
formatting, and style are enforced by `rustc` and `clippy` — this skill adds
the design layer those tools cannot cover.

Sources:
- Design guidelines — Microsoft Pragmatic Rust Guidelines: <https://github.com/microsoft/rust-guidelines>
- Community patterns — Rust Design Patterns (rust-unofficial): <https://rust-unofficial.github.io/patterns/>
- Classical patterns — Gang-of-Four in Rust (refactoring.guru): <https://refactoring.guru/design-patterns/rust>

## Reading protocol

Load files in this order; stop when the task's scope is satisfied.

1. **Always**: `guidelines.txt` — Microsoft Pragmatic Rust Guidelines
   (~50 `M-*` design rules: API shape, errors, docs, FFI, safety, perf,
   crates, logging, construction, typestate).
2. **Always**: `patterns.md` — Rust idioms, design patterns, anti-patterns,
   and functional patterns from rust-unofficial; plus all 22 Gang-of-Four
   patterns adapted to Rust from refactoring.guru. Load before choosing
   among architectural alternatives (RAII guards vs Drop impl, newtype vs
   alias, builder vs params struct, fold vs visitor, etc.).

## Compliance marker

After producing compliant code (only when the user has explicitly asked for
a compliance check), append:

```
// Rust guideline compliant (Microsoft + rust-unofficial)
```

## Hard rules

- Never ship a diff containing a design-level violation.
- Do not silently lower standards. If a rule must be violated, surface it
  explicitly with a one-line rationale.
- When refactoring touched code, fix violations in-flight rather than
  preserving legacy patterns.
- Prefer idiomatic Rust — a pattern from rust-unofficial's idioms section
  is the canonical default unless the design guideline overrides it.
- Do **not** duplicate what `rustc` and `clippy` already enforce. This skill
  exists to layer design guidance on top of those tools, not replace them.
