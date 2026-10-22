# group-params

When construction needs 4+ parameters, group them into semantic helper types or newtypes instead of a long argument list.

**Why:** Prevents silently swapped arguments.

**Sources:** M-INIT-CASCADED

---

## Complex type initialization hierarchies are cascaded (M-INIT-CASCADED)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Types that require 4+ parameters should cascade their initialization via helper types.

```rust
impl Deposit {
    // Easy to confuse parameters and signature generally unwieldy.
    pub fn new(bank_name: &str, customer_name: &str, currency_name: &str, currency_amount: u64) -> Self { }
}
```

Instead of providing a long parameter list, parameters should be grouped semantically. When applying this guideline,
also check if C-NEWTYPE is applicable:

```rust
impl Deposit {
    // Better, signature cleaner
    pub fn new(account: Account, amount: Currency) -> Self { }
}

impl Account {
    pub fn new_ok(bank: &str, customer: &str) -> Self { }
    pub fn new_even_better(bank: Bank, customer: Customer) -> Self { }
}
```
