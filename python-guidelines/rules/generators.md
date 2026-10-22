# generators

Use generators freely; document them with `Yields:`, and wrap one that holds an expensive resource in a context manager so cleanup is forced.

**Why:** A suspended generator keeps its locals alive.

**Sources:** G:s2.9-generators

---

## Generators (G:s2.9-generators)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.9-generators), CC BY 3.0.

Use generators as needed.

### 2.9.1 Definition

A generator function returns an iterator that yields a value each time it
executes a yield statement. After it yields a value, the runtime state of the
generator function is suspended until the next value is needed.

### 2.9.2 Pros

Simpler code, because the state of local variables and control flow are
preserved for each call. A generator uses less memory than a function that
creates an entire list of values at once.

### 2.9.3 Cons

Local variables in the generator will not be garbage collected until the
generator is either consumed to exhaustion or itself garbage collected.

### 2.9.4 Decision

Fine. Use "Yields:" rather than "Returns:" in the docstring for generator
functions.

If the generator manages an expensive resource, make sure to force the clean up.

A good way to do the clean up is by wrapping the generator with a context
manager [PEP-0533](https://peps.python.org/pep-0533/).
