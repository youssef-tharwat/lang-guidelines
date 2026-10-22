# implicit-false

Test emptiness with implicit truth (`if not users:`), but compare to `None` with `is`/`is not`, never compare to `False` with `==`, and compare a possibly-`None` integer to `0` explicitly; use `.size` for NumPy arrays.

**Why:** Implicit truth reads well; `None` and `0` must not be confused.

**Sources:** G:s2.14-truefalse-evaluations

---

## True/False Evaluations (G:s2.14-truefalse-evaluations)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.14-truefalse-evaluations), CC BY 3.0.

Use the "implicit" false if at all possible (with a few caveats).

### 2.14.1 Definition

Python evaluates certain values as `False` when in a boolean context. A quick
"rule of thumb" is that all "empty" values are considered false, so `0, None,
[], {}, ''` all evaluate as false in a boolean context.

### 2.14.2 Pros

Conditions using Python booleans are easier to read and less error-prone. In
most cases, they're also faster.

### 2.14.3 Cons

May look strange to C/C++ developers.

### 2.14.4 Decision

Use the "implicit" false if possible, e.g., `if foo:` rather than `if foo !=
[]:`. There are a few caveats that you should keep in mind though:

-   Always use `if foo is None:` (or `is not None`) to check for a `None` value.
    E.g., when testing whether a variable or argument that defaults to `None`
    was set to some other value. The other value might be a value that's false
    in a boolean context!

-   Never compare a boolean variable to `False` using `==`. Use `if not x:`
    instead. If you need to distinguish `False` from `None` then chain the
    expressions, such as `if not x and x is not None:`.

-   For sequences (strings, lists, tuples), use the fact that empty sequences
    are false, so `if seq:` and `if not seq:` are preferable to `if len(seq):`
    and `if not len(seq):` respectively.

-   When handling integers, implicit false may involve more risk than benefit
    (i.e., accidentally handling `None` as 0). You may compare a value which is
    known to be an integer (and is not the result of `len()`) against the
    integer 0.

    ```python
    Yes: if not users:
             print('no users')

         if i % 10 == 0:
             self.handle_multiple_of_ten()

         def f(x=None):
             if x is None:
                 x = []
    ```

    ```python
    No:  if len(users) == 0:
             print('no users')

         if not i % 10:
             self.handle_multiple_of_ten()

         def f(x=None):
             x = x or []
    ```

-   Note that `'0'` (i.e., `0` as string) evaluates to true.

-   Note that Numpy arrays may raise an exception in an implicit boolean
    context. Prefer the `.size` attribute when testing emptiness of a `np.array`
    (e.g. `if not users.size`).
