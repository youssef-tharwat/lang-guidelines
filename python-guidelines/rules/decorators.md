# decorators

Use a decorator only for a clear advantage: say in its docstring that it is a decorator, test it, and keep files, sockets and databases out of it. Never use `staticmethod` (write a module-level function); use `classmethod` only for named constructors or class-wide state.

**Why:** Decorators run at import time and their failures are unrecoverable.

**Sources:** G:s2.17-function-and-method-decorators

---

## Function and Method Decorators (G:s2.17-function-and-method-decorators)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.17-function-and-method-decorators), CC BY 3.0.

Use decorators judiciously when there is a clear advantage. Avoid `staticmethod`
and limit use of `classmethod`.

### 2.17.1 Definition

[Decorators for Functions and Methods](https://docs.python.org/3/glossary.html#term-decorator)
(a.k.a "the `@` notation"). One common decorator is `@property`, used for
converting ordinary methods into dynamically computed attributes. However, the
decorator syntax allows for user-defined decorators as well. Specifically, for
some function `my_decorator`, this:

```python
class C:
    @my_decorator
    def method(self):
        # method body ...
```

is equivalent to:

```python
class C:
    def method(self):
        # method body ...
    method = my_decorator(method)
```

### 2.17.2 Pros

Elegantly specifies some transformation on a method; the transformation might
eliminate some repetitive code, enforce invariants, etc.

### 2.17.3 Cons

Decorators can perform arbitrary operations on a function's arguments or return
values, resulting in surprising implicit behavior. Additionally, decorators
execute at object definition time. For module-level objects (classes, module
functions, ...) this happens at import time. Failures in decorator code are
pretty much impossible to recover from.

### 2.17.4 Decision

Use decorators judiciously when there is a clear advantage. Decorators should
follow the same import and naming guidelines as functions. A decorator docstring
should clearly state that the function is a decorator. Write unit tests for
decorators.

Avoid external dependencies in the decorator itself (e.g. don't rely on files,
sockets, database connections, etc.), since they might not be available when the
decorator runs (at import time, perhaps from `pydoc` or other tools). A
decorator that is called with valid parameters should (as much as possible) be
guaranteed to succeed in all cases.

Decorators are a special case of "top-level code" - see main for
more discussion.

Never use `staticmethod` unless forced to in order to integrate with an API
defined in an existing library. Write a module-level function instead.

Use `classmethod` only when writing a named constructor, or a class-specific
routine that modifies necessary global state such as a process-wide cache.
