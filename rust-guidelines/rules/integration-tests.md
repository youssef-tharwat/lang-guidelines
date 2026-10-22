# integration-tests

Tests that only touch the public API are integration tests under `tests/`, not `mod tests`; prefer them when either would do, and give complex projects a dedicated crate for shared test helpers.

**Why:** Keeps `src/` about the code, not its tests.

**Sources:** M-INTEGRATION-TESTS, M-INTEGRATION-TEST-UTILS

---

## Integration tests live under `tests/` (M-INTEGRATION-TESTS)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Tests that only touch public API surface are _integration tests_ and belong under `tests/`, not `mod tests {}`.

In projects with coverage targets, it is not uncommon for `src/` files to contain more testing code than actual business logic. This can make browsing and understanding the code harder both in IDEs and PRs. Likewise, if a testing goal can be achieved through either an integration test or a unit test, the former is always preferred.


## Integration test utilities live in a separate crate (M-INTEGRATION-TEST-UTILS)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

For complex projects, shared helpers used by integration tests (fixtures, builders, mock servers, assertion helpers, ...) should live in a dedicated crate rather than inside the production crate or copied between individual `tests/*.rs` files.

- TODO: Define what counts as a "complex project" (e.g., number of integration tests, crates, or helpers that triggers this rule).
- TODO: Specify the recommended crate name / location convention (e.g., sibling `foo-test-utils` crate in the workspace).
- TODO: Clarify the relationship with M-TEST-UTIL (feature-gated helpers within a crate) — when to prefer which.
- TODO: Add a short example showing the crate layout and how integration tests depend on it (likely via `[dev-dependencies]`).
