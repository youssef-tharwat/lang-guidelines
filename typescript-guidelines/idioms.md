# TypeScript & JavaScript Idioms

Positive patterns to favor while writing TS/JS. Complement to the lint-rule
prohibitions in `guidelines.txt` — these are things a correct program **does**,
not just things it avoids.

## Declarations
- `const` by default; `let` only when re-assigned; never `var`.
- Prefer `readonly` on properties that don't mutate post-construction.

## Equality & nullish
- `===` / `!==` exclusively. `==` / `!=` only for intentional `== null`
  nullish-or-undefined checks (and even then, prefer `x == null`).
- Use `??` (nullish coalescing) over `||` when falsy values (`0`, `""`) are
  valid.
- Use `?.` (optional chaining) over chained `&&` guards.

## Types
- Never `any`. Use `unknown` + narrowing, or a precise union.
- Return types on exported functions. Infer internal ones.
- Use discriminated unions (`{ kind: "ok", … } | { kind: "err", … }`) for sum
  types, never a flat interface with optional fields.
- `Record<K, V>` over index signatures (`{ [k: string]: V }`) for map-like
  dictionaries.
- Exhaustiveness check: `const _exhaustive: never = x;` in the default arm of
  a discriminant switch.

## Immutability
- Prefer `readonly T[]` / `ReadonlyArray<T>` on parameters you don't mutate.
- Prefer spread / `Object.freeze` over in-place mutation when building new
  values.

## Async
- `async` / `await` over `.then()` chains except at the very edge of the app.
- `Promise.all` for independent awaits; never `await` in a loop when the
  iterations are independent.
- `AbortController` / `AbortSignal` for cancellation; never orphan promises.

## Destructuring
- Destructure props/params when accessing ≥ 2 fields.
- Rename on destructure when it improves clarity: `const { data: user } = …`.

## Strings
- Template literals over concatenation.
- `String.raw` for regex / path literals.

## Arrays & objects
- `.map / .filter / .flatMap / .reduce` over `for` when the body is a pure
  transform.
- `for…of` over `.forEach` when you need `break` / `continue` / `await`.
- `Array.from({ length: n }, (_, i) => …)` for fixed-length generation.
- `Object.entries / keys / values` + destructuring over manual key iteration.

## Imports
- Named imports over default imports in application code (better for
  refactoring, tree-shaking, and editor tooling).
- Group: std / external / internal / sibling — blank lines between groups.
- Avoid `import * as X`; prefer named imports.

## Errors
- `throw new Error(msg, { cause: err })` to preserve cause (ES2022+).
- Always `catch (err)` typed as `unknown`; narrow with `instanceof` before use.
- Never catch-and-swallow. If catching is valid, log / wrap / rethrow.

## React / components (if applicable)
- Functional components only. Hooks over class components.
- `useMemo` / `useCallback` only when profiler or render-boundary actually
  demands memoization — not prophylactically.
- `useEffect` for external synchronization only; derive state synchronously.

## Non-null assertion
- `x!` is never allowed without a comment explaining the invariant that
  guarantees non-null. Prefer a type guard or `throw` instead.
