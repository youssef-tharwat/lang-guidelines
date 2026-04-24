---
name: rust-guidelines
description: Enforce Microsoft Rust guidelines for all Rust code generation and edits
---

# Rust Development

Apply the rules in guidelines.txt when generating or modifying Rust code.

## Instructions

- Ensure all Rust code follows guidelines.txt
- Prefer safe, idiomatic Rust
- Enforce proper error handling (Result, no panic for flow)
- Require documentation for public APIs
- If code is compliant, append:
  // Rust guideline compliant (Microsoft) 
- Reject code that violates guidelines
- Refactor non-compliant code automatically
- Explain violations briefly
