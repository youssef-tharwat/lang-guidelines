# no-mutable-defaults

Never use a mutable or call-time value as a default argument (`[]`, `{}`, `time.time()`, a flag's value); default to `None` or an immutable value such as `()` and build the real value inside the function.

**Why:** Defaults are evaluated once, when the function is defined.

**Sources:** G:s2.12-default-argument-values

---

## Default Argument Values (G:s2.12-default-argument-values)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.12-default-argument-values), CC BY 3.0.

Okay in most cases.

### 2.12.1 Definition

You can specify values for variables at the end of a function's parameter list,
e.g., `def foo(a, b=0):`. If `foo` is called with only one argument, `b` is set
to 0. If it is called with two arguments, `b` has the value of the second
argument.

### 2.12.2 Pros

Often you have a function that uses lots of default values, but on rare
occasions you want to override the defaults. Default argument values provide an
easy way to do this, without having to define lots of functions for the rare
exceptions. As Python does not support overloaded methods/functions, default
arguments are an easy way of "faking" the overloading behavior.

### 2.12.3 Cons

Default arguments are evaluated once at module load time. This may cause
problems if the argument is a mutable object such as a list or a dictionary. If
the function modifies the object (e.g., by appending an item to a list), the
default value is modified.

### 2.12.4 Decision

Okay to use with the following caveat:

Do not use mutable objects as default values in the function or method
definition.

```python
Yes: def foo(a, b=None):
         if b is None:
             b = []
Yes: def foo(a, b: Sequence | None = None):
         if b is None:
             b = []
Yes: def foo(a, b: Sequence = ()):  # Empty tuple OK since tuples are immutable.
         ...
```

```python
from absl import flags
_FOO = flags.DEFINE_string(...)

No:  def foo(a, b=[]):
         ...
No:  def foo(a, b=time.time()):  # Is `b` supposed to represent when this module was loaded?
         ...
No:  def foo(a, b=_FOO.value):  # sys.argv has not yet been parsed...
         ...
No:  def foo(a, b: Mapping = {}):  # Could still get passed to unchecked code.
         ...
```
