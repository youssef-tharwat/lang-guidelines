# dont-leak-types

Keep third-party types out of public signatures unless behind a feature (such as `serde`) or the interop benefit is substantial; `std` types are always fine.

**Why:** A leaked type ties your semver to theirs.

**Binding in:** libraries (code other packages depend on); a strong recommendation in application-only code.

**Sources:** M-DONT-LEAK-TYPES

---

## Don't leak external types (M-DONT-LEAK-TYPES)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Where possible, you should prefer `std`^1 types in public APIs over types coming from external crates. Exceptions should be carefully considered.

Any type in any public API will become part of that API's contract. Since `std` and constituents are the only crates
shipped by default, and since they come with a permanent stability guarantee, their types are the only ones that come without an interoperability risk.

A crate that exposes another crate's type is said to _leak_ that type.

For maximal long term stability your crate should, theoretically, not leak any types. Practically, some leakage
is unavoidable, sometimes even beneficial. We recommend you follow this heuristic:

- [ ] if you can avoid it, do not leak third-party types
- [ ] if you are part of an umbrella crate,^2 you may freely leak types from sibling crates.
- [ ] behind a relevant feature flag, types may be leaked (e.g., `serde`)
- [ ] without a feature _only_ if they give a _substantial benefit_. Most commonly that is interoperability with significant
      other parts of the Rust ecosystem based around these types.

^1 In rare instances, e.g., high performance libraries used from embedded, you might even want to limit yourself to `core` only.

^2 For example, a `runtime` crate might be the umbrella of `runtime_rt`, `runtime_app` and `runtime_clock` As users are
expected to only interact with the umbrella, siblings may leak each others types.
