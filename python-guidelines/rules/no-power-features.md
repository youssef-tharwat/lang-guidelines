# no-power-features

Avoid metaclasses, bytecode access, on-the-fly compilation, dynamic inheritance, object reparenting, import hacks, reflection tricks and custom `__del__` cleanup; standard tools built on them (`dataclasses`, `enum`, `abc`) are fine.

**Why:** Clever code is hard to read, debug and type-check.

**Sources:** G:s2.19-power-features

---

## Power Features (G:s2.19-power-features)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.19-power-features), CC BY 3.0.

Avoid these features.

### 2.19.1 Definition

Python is an extremely flexible language and gives you many fancy features such
as custom metaclasses, access to bytecode, on-the-fly compilation, dynamic
inheritance, object reparenting, import hacks, reflection (e.g. some uses of
`getattr()`), modification of system internals, `__del__` methods implementing
customized cleanup, etc.

### 2.19.2 Pros

These are powerful language features. They can make your code more compact.

### 2.19.3 Cons

It's very tempting to use these "cool" features when they're not absolutely
necessary. It's harder to read, understand, and debug code that's using unusual
features underneath. It doesn't seem that way at first (to the original author),
but when revisiting the code, it tends to be more difficult than code that is
longer but is straightforward.

### 2.19.4 Decision

Avoid these features in your code.

Standard library modules and classes that internally use these features are okay
to use (for example, `abc.ABCMeta`, `dataclasses`, and `enum`).
