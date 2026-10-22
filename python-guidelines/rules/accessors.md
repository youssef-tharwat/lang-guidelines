# accessors

Write `get_x()`/`set_x()` only when access is costly or has effects (such as invalidating state); otherwise expose the attribute. When access becomes costly, replace the property rather than hiding the cost behind it.

**Why:** A function call signals that real work happens.

**Sources:** G:s3.15-accessors

---

## Getters and Setters (G:s3.15-accessors)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s3.15-accessors), CC BY 3.0.

Getter and setter functions (also called accessors and mutators) should be used
when they provide a meaningful role or behavior for getting or setting a
variable's value.

In particular, they should be used when getting or setting the variable is
complex or the cost is significant, either currently or in a reasonable future.

If, for example, a pair of getters/setters simply read and write an internal
attribute, the internal attribute should be made public instead. By comparison,
if setting a variable means some state is invalidated or rebuilt, it should be a
setter function. The function invocation hints that a potentially non-trivial
operation is occurring. Alternatively, properties may be an
option when simple logic is needed, or refactoring to no longer need getters and
setters.

Getters and setters should follow the Naming guidelines, such
as `get_foo()` and `set_foo()`.

If the past behavior allowed access through a property, do not bind the new
getter/setter functions to the property. Any code still attempting to access the
variable by the old method should break visibly so they are made aware of the
change in complexity.
