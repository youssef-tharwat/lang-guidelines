# test-util-feature

Put mocks, fake data, secret inspection and safety-check overrides behind a `test-util` feature.

**Why:** Production builds can't reach them.

**Binding in:** libraries (code other packages depend on); a strong recommendation in application-only code.

**Sources:** M-TEST-UTIL

---

## Test utilities are feature gated (M-TEST-UTIL)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Testing functionality must be guarded behind a feature flag. This includes

- mocking functionality (M-MOCKABLE-SYSCALLS),
- the ability to inspect sensitive data,
- safety check overrides,
- fake data generation.

We recommend you use a single flag only, named `test-util`. In any case, the feature(s) must clearly communicate they are for testing purposes.

```rust
impl HttpClient {
    pub fn get() { ... }

    #[cfg(feature = "test-util")]
    pub fn bypass_certificate_checks() { ... }
}
```
