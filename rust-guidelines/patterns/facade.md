# facade

Offer one simple entry point over a complex subsystem.

**Sources:** GOF:facade

---

## Facade (Gang of Four) (GOF:facade)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/facade/rust/example), CC BY-SA 4.0.

**Facade** is a structural design pattern that provides a simplified (but limited) interface to a complex system of classes, library or framework.

While Facade decreases the overall complexity of the application, it also helps to move unwanted dependencies to one place.

### Conceptual Example

`pub struct WalletFacade` hides a complex logic behind its API. A single method `add_money_to_wallet` interacts with the account, code, wallet, notification and ledger behind the scenes.

##### **wallet_facade.rs**
```rust
use crate::{
    account::Account, ledger::Ledger, notification::Notification, security_code::SecurityCode,
    wallet::Wallet,
};

/// Facade hides a complex logic behind the API.
pub struct WalletFacade {
    account: Account,
    wallet: Wallet,
    code: SecurityCode,
    notification: Notification,
    ledger: Ledger,
}

impl WalletFacade {
    pub fn new(account_id: String, code: u32) -> Self {
        println!("Starting create account");

        let this = Self {
            account: Account::new(account_id),
            wallet: Wallet::new(),
            code: SecurityCode::new(code),
            notification: Notification,
            ledger: Ledger,
        };

        println!("Account created");
        this
    }

    pub fn add_money_to_wallet(
        &mut self,
        account_id: &String,
        security_code: u32,
        amount: u32,
    ) -> Result<(), String> {
        println!("Starting add money to wallet");
        self.account.check(account_id)?;
        self.code.check(security_code)?;
        self.wallet.credit_balance(amount);
        self.notification.send_wallet_credit_notification();
        self.ledger.make_entry(account_id, "credit".into(), amount);
        Ok(())
    }

    pub fn deduct_money_from_wallet(
        &mut self,
        account_id: &String,
        security_code: u32,
        amount: u32,
    ) -> Result<(), String> {
        println!("Starting debit money from wallet");
        self.account.check(account_id)?;
        self.code.check(security_code)?;
        self.wallet.debit_balance(amount);
        self.notification.send_wallet_debit_notification();
        self.ledger.make_entry(account_id, "debit".into(), amount);
        Ok(())
    }
}
```

##### **wallet.rs**
```rust
pub struct Wallet {
    balance: u32,
}

impl Wallet {
    pub fn new() -> Self {
        Self { balance: 0 }
    }

    pub fn credit_balance(&mut self, amount: u32) {
        self.balance += amount;
    }

    pub fn debit_balance(&mut self, amount: u32) {
        self.balance
            .checked_sub(amount)
            .expect("Balance is not sufficient");
    }
}
```

##### **account.rs**
```rust
pub struct Account {
    name: String,
}

impl Account {
    pub fn new(name: String) -> Self {
        Self { name }
    }

    pub fn check(&self, name: &String) -> Result<(), String> {
        if &self.name != name {
            return Err("Account name is incorrect".into());
        }

        println!("Account verified");
        Ok(())
    }
}
```

##### **ledger.rs**
```rust
pub struct Ledger;

impl Ledger {
    pub fn make_entry(&mut self, account_id: &String, txn_type: String, amount: u32) {
        println!(
            "Make ledger entry for accountId {} with transaction type {} for amount {}",
            account_id, txn_type, amount
        );
    }
}
```

##### **notification.rs**
```rust
pub struct Notification;

impl Notification {
    pub fn send_wallet_credit_notification(&self) {
        println!("Sending wallet credit notification");
    }

    pub fn send_wallet_debit_notification(&self) {
        println!("Sending wallet debit notification");
    }
}
```

##### **security_code.rs**
```rust
pub struct SecurityCode {
    code: u32,
}

impl SecurityCode {
    pub fn new(code: u32) -> Self {
        Self { code }
    }

    pub fn check(&self, code: u32) -> Result<(), String> {
        if self.code != code {
            return Err("Security code is incorrect".into());
        }

        println!("Security code verified");
        Ok(())
    }
}
```

##### **main.rs**
```rust
mod account;
mod ledger;
mod notification;
mod security_code;
mod wallet;
mod wallet_facade;

use wallet_facade::WalletFacade;

fn main() -> Result<(), String> {
    let mut wallet = WalletFacade::new("abc".into(), 1234);
    println!();

    // Wallet Facade interacts with the account, code, wallet, notification and
    // ledger behind the scenes.
    wallet.add_money_to_wallet(&"abc".into(), 1234, 10)?;
    println!();

    wallet.deduct_money_from_wallet(&"abc".into(), 1234, 5)
}
```

#### Output
```text
Starting create account
Account created

Starting add money to wallet
Account verified
Security code verified
Sending wallet credit notification
Make ledger entry for accountId abc with transaction type credit for amount 10

Starting debit money from wallet
Account verified
Security code verified
Sending wallet debit notification
Make ledger entry for accountId abc with transaction type debit for amount 5
```
