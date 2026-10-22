# proxy

Stand in for a service to add access control, caching or laziness.

**Sources:** GOF:proxy

---

## Proxy (Gang of Four) (GOF:proxy)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/proxy/rust/example), CC BY-SA 4.0.

**Proxy** is a structural design pattern that provides an object that acts as a substitute for a real service object used by a client. A proxy receives client requests, does some work (access control, caching,etc.) and then passes the request to a service object.

The proxy object has the same interface as a service, which makes it interchangeable with a real object when passed to a client.
### Conceptual Example: Nginx Proxy

A web server such as Nginx can act as a proxy for your application server:

*   It provides controlled access to your application server.
*   It can do rate limiting.
*   It can do request caching.

##### **server.rs**
```rust
mod application;
mod nginx;

pub use nginx::NginxServer;

pub trait Server {
    fn handle_request(&mut self, url: &str, method: &str) -> (u16, String);
}
```

##### **server/application.rs**
```rust
use super::Server;

pub struct Application;

impl Server for Application {
    fn handle_request(&mut self, url: &str, method: &str) -> (u16, String) {
        if url == "/app/status" && method == "GET" {
            return (200, "Ok".into());
        }

        if url == "/create/user" && method == "POST" {
            return (201, "User Created".into());
        }

        (404, "Not Ok".into())
    }
}
```

##### **server/nginx.rs**
```rust
use std::collections::HashMap;

use super::{application::Application, Server};

/// NGINX server is a proxy to an application server.
pub struct NginxServer {
    application: Application,
    max_allowed_requests: u32,
    rate_limiter: HashMap<String, u32>,
}

impl NginxServer {
    pub fn new() -> Self {
        Self {
            application: Application,
            max_allowed_requests: 2,
            rate_limiter: HashMap::default(),
        }
    }

    pub fn check_rate_limiting(&mut self, url: &str) -> bool {
        let rate = self.rate_limiter.entry(url.to_string()).or_insert(1);

        if *rate > self.max_allowed_requests {
            return false;
        }

        *rate += 1;
        true
    }
}

impl Server for NginxServer {
    fn handle_request(&mut self, url: &str, method: &str) -> (u16, String) {
        if !self.check_rate_limiting(url) {
            return (403, "Not Allowed".into());
        }

        self.application.handle_request(url, method)
    }
}
```

##### **main.rs**
```rust
mod server;

use crate::server::{NginxServer, Server};

fn main() {
    let app_status = &"/app/status".to_string();
    let create_user = &"/create/user".to_string();

    let mut nginx = NginxServer::new();

    let (code, body) = nginx.handle_request(app_status, "GET");
    println!("Url: {}\nHttpCode: {}\nBody: {}\n", app_status, code, body);

    let (code, body) = nginx.handle_request(app_status, "GET");
    println!("Url: {}\nHttpCode: {}\nBody: {}\n", app_status, code, body);

    let (code, body) = nginx.handle_request(app_status, "GET");
    println!("Url: {}\nHttpCode: {}\nBody: {}\n", app_status, code, body);

    let (code, body) = nginx.handle_request(create_user, "POST");
    println!("Url: {}\nHttpCode: {}\nBody: {}\n", create_user, code, body);

    let (code, body) = nginx.handle_request(create_user, "GET");
    println!("Url: {}\nHttpCode: {}\nBody: {}\n", create_user, code, body);
}
```

#### Output
```text
Url: /app/status
HttpCode: 200
Body: Ok

Url: /app/status
HttpCode: 200
Body: Ok

Url: /app/status
HttpCode: 403
Body: Not Allowed

Url: /create/user
HttpCode: 201
Body: User Created

Url: /create/user
HttpCode: 404
Body: Not Ok
```

#### Behavioral patterns
