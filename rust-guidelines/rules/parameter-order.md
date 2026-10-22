# parameter-order

Order recurring parameters the same way in every function: call-specific ones first, ubiquitous ones such as `&logger` last, and a closure always last (at most one closure per function).

**Why:** Callers stop checking the order at every call.

**Sources:** M-PARAMETER-CONSISTENCY

---

## Parameter ordering is consistent (M-PARAMETER-CONSISTENCY)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

When the same conceptual parameters appear in multiple functions (within a crate or across crates in the same ecosystem), they should appear in the same order everywhere:

- important or call-specific parameters should generally go first,
- ubiquitous parameters rather go last (e.g., `&logger`),
- closures always go last (functions should not accept more than one closure).

```rust
// Bad, the order of `user_id` and `tenant_id` flips between functions, and
// the logger sometimes appears first, sometimes last.
fn create_user(logger: &Logger, user_id: UserId, tenant_id: TenantId) -> Result<()> { ... }
fn delete_user(tenant_id: TenantId, user_id: UserId, logger: &Logger) -> Result<()> { ... }
fn rename_user(user_id: UserId, new_name: &str, tenant_id: TenantId, logger: &Logger) -> Result<()> { ... }

// Good, call-specific parameters first in a consistent order, ubiquitous
// `logger` always last.
fn create_user(tenant_id: TenantId, user_id: UserId, logger: &Logger) -> Result<()> { ... }
fn delete_user(tenant_id: TenantId, user_id: UserId, logger: &Logger) -> Result<()> { ... }
fn rename_user(tenant_id: TenantId, user_id: UserId, new_name: &str, logger: &Logger) -> Result<()> { ... }
```
