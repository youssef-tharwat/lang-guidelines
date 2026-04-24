---
name: typescript-guidelines
description: Enforce TypeScript & JavaScript lint rules (Oxlint) for all TypeScript & JavaScript code generation and edits. Rules must be applied while writing code, not only in review. Triggers on any task that writes, edits, or refactors TypeScript & JavaScript code.
---

# TypeScript & JavaScript Development Guidelines

Every rule in `guidelines.txt` is a hard constraint. Apply them **while
writing code**, not only during review. Source: Oxlint (oxc.rs) covering eslint, typescript-eslint, unicorn, react, nextjs, jsx-a11y, jest, vitest, and more.

## Reading protocol

Load files in this order; stop when the task's scope is satisfied.

1. **Always**: `guidelines.txt` — 210 correctness + security + modernization rules. Never skip.
2. **Always**: `idioms.md` — positive patterns (what to prefer, not just what to avoid).
3. **If reviewing / matching a project style guide**: `style.md` — 280 style/pedantic rules.
4. **Framework-gated**: `frameworks/<name>.md` — load only if the project's
   manifest (`package.json`) depends on or imports the named framework.

   - `frameworks/jest.md` (59 rules)
   - `frameworks/jsdoc.md` (18 rules)
   - `frameworks/nextjs.md` (21 rules)
   - `frameworks/react.md` (92 rules)
   - `frameworks/vitest.md` (23 rules)
   - `frameworks/vue.md` (17 rules)
5. **On demand for edge cases**: `rules/<slug>/index.md` — full docs with
   additional examples, configuration, and references.

## Rule format

Each rule in the compiled files follows this shape:

```
### <slug> (<code>)
<imperative rule in one sentence>
❌ <minimal bad example>
✅ <minimal good example>
```

Treat the `✅` example as the canonical pattern. When a bad snippet appears in
code under edit, rewrite to the good snippet unless the user has explicitly
documented an exception.

## Compliance marker

After producing compliant code (only when the user has explicitly asked for a
compliance check), append:

```
// TypeScript guideline compliant (Oxlint)
```

## Hard rules

- Never ship a diff containing a Tier-1 violation.
- Do not silently lower standards. If a rule must be violated, surface it
  explicitly with a one-line rationale.
- When refactoring touched code, fix violations in-flight rather than
  preserving legacy patterns.
- Prefer each rule's `✅` example as the idiomatic pattern.
