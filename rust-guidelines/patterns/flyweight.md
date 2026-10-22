# flyweight

Share common immutable state across many objects to save memory.

**Sources:** GOF:flyweight

---

## Flyweight (Gang of Four) (GOF:flyweight)

[Design Patterns in Rust (refactoring.guru)](https://refactoring.guru/design-patterns/flyweight/rust/example), CC BY-SA 4.0.

**Flyweight** is a structural design pattern that allows programs to support vast quantities of objects by keeping their memory consumption low.

The pattern achieves it by sharing parts of object state between multiple objects. In other words, the Flyweight saves RAM by caching the same data used by different objects.
### Rendering a Forest
