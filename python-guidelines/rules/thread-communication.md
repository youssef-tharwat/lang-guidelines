# thread-communication

Don't rely on the atomicity of built-in types; pass data between threads with `queue.Queue`, or with `threading` locks, preferring `threading.Condition`.

**Why:** Built-in operations are not reliably atomic.

**Sources:** G:s2.18-threading

---

## Threading (G:s2.18-threading)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.18-threading), CC BY 3.0.

Do not rely on the atomicity of built-in types.

While Python's built-in data types such as dictionaries appear to have atomic
operations, there are corner cases where they aren't atomic (e.g. if `__hash__`
or `__eq__` are implemented as Python methods) and their atomicity should not be
relied upon. Neither should you rely on atomic variable assignment (since this
in turn depends on dictionaries).

Use the `queue` module's `Queue` data type as the preferred way to communicate
data between threads. Otherwise, use the `threading` module and its locking
primitives. Prefer condition variables and `threading.Condition` instead of
using lower-level locks.
