# nested-functions

Nest a function or class only to close over a local value other than `self` or `cls`; to hide a helper, give it a leading `_` at module level instead, so tests can reach it.

**Why:** Nested functions can't be tested directly.

**Sources:** G:s2.6-nested, G:s2.16-lexical-scoping

---

## Nested/Local/Inner Classes and Functions (G:s2.6-nested)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.6-nested), CC BY 3.0.

Nested local functions or classes are fine when used to close over a local
variable. Inner classes are fine.

### 2.6.1 Definition

A class can be defined inside of a method, function, or class. A function can be
defined inside a method or function. Nested functions have read-only access to
variables defined in enclosing scopes.

### 2.6.2 Pros

Allows definition of utility classes and functions that are only used inside of
a very limited scope. Very
[ADT](https://en.wikipedia.org/wiki/Abstract_data_type)-y. Commonly used for
implementing decorators.

### 2.6.3 Cons

Nested functions and classes cannot be directly tested. Nesting can make the
outer function longer and less readable.

### 2.6.4 Decision

They are fine with some caveats. Avoid nested functions or classes except when
closing over a local value other than `self` or `cls`. Do not nest a function
just to hide it from users of a module. Instead, prefix its name with an \_ at
the module level so that it can still be accessed by tests.


## Lexical Scoping (G:s2.16-lexical-scoping)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.16-lexical-scoping), CC BY 3.0.

Okay to use.

### 2.16.1 Definition

A nested Python function can refer to variables defined in enclosing functions,
but cannot assign to them. Variable bindings are resolved using lexical scoping,
that is, based on the static program text. Any assignment to a name in a block
will cause Python to treat all references to that name as a local variable, even
if the use precedes the assignment. If a global declaration occurs, the name is
treated as a global variable.

An example of the use of this feature is:

```python
def get_adder(summand1: float) -> Callable[[float], float]:
    """Returns a function that adds numbers to a given number."""
    def adder(summand2: float) -> float:
        return summand1 + summand2

    return adder
```

### 2.16.2 Pros

Often results in clearer, more elegant code. Especially comforting to
experienced Lisp and Scheme (and Haskell and ML and ...) programmers.

### 2.16.3 Cons

Can lead to confusing bugs, such as this example based on
[PEP-0227](https://peps.python.org/pep-0227/):

```python
i = 4
def foo(x: Iterable[int]):
    def bar():
        print(i, end='')
    # ...
    # A bunch of code here
    # ...
    for i in x:  # Ah, i *is* local to foo, so this is what bar sees
        print(i, end='')
    bar()
```

So `foo([1, 2, 3])` will print `1 2 3 3`,
not `1 2 3 4`.

### 2.16.4 Decision

Okay to use.
