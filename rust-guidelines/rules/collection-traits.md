# collection-traits

A custom collection provides `iter()`, `iter_mut()`, `IntoIter`/`Iter`/`IterMut` types, `IntoIterator` for the value and both references, `FromIterator` and `Extend`, plus `DoubleEndedIterator`/`ExactSizeIterator` where they fit, with truthful `size_hint()`.

**Why:** It then works everywhere std collections do.

**Binding in:** libraries (code other packages depend on); a strong recommendation in application-only code.

**Sources:** M-COLLECTION-TRAITS

---

## Collections implement the appropriate iter traits (M-COLLECTION-TRAITS)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Custom collections should implement the iterator-facing traits the standard library offers.

Whenever you define a new collection type `Collection<T>` for consumption by third parties, the following traits and types should also be implemented, [see here](https://cheats.rs/#iterators) for more details:

- the structs `IntoIter<T>`, `Iter<T>` and `IterMut<T>`,
- an `impl Iterator` for all of them,
- the methods `c.iter()` and `c.iter_mut()`,
- an `impl IntoIterator` for `Collection<T>`, `&Collection<T>` and `&mut Collection<T>`,
- an `impl FromIterator` for `Collection<T>`,
- an `Extend` for `Collection<T>`,
- `DoubleEndedIterator`, `ExactSizeIterator`, ... as applicable

In addition, make sure you implement `size_hint()` on all iterators and do so truthfully.
