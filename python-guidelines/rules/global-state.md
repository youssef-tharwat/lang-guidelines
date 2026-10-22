# global-state

Avoid mutable global state; when it is unavoidable, make it module-internal (`_name`), reach it through functions, and comment why. Module-level constants (`MAX_RETRIES = 3`) are encouraged.

**Why:** Global state breaks encapsulation and runs at import.

**Sources:** G:s2.5-global-variables

---

## Mutable Global State (G:s2.5-global-variables)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.5-global-variables), CC BY 3.0.

Avoid mutable global state.

### 2.5.1 Definition

Module-level values or class attributes that can get mutated during program
execution.

### 2.5.2 Pros

Occasionally useful.

### 2.5.3 Cons

*   Breaks encapsulation: Such design can make it hard to achieve valid
    objectives. For example, if global state is used to manage a database
    connection, then connecting to two different databases at the same time
    (such as for computing differences during a migration) becomes difficult.
    Similar problems easily arise with global registries.

*   Has the potential to change module behavior during the import, because
    assignments to global variables are done when the module is first imported.

### 2.5.4 Decision

Avoid mutable global state.

In those rare cases where using global state is warranted, mutable global
entities should be declared at the module level or as a class attribute and made
internal by prepending an `_` to the name. If necessary, external access to
mutable global state must be done through public functions or class methods. See
Naming below. Please explain the design reasons why mutable
global state is being used in a comment or a doc linked to from a comment.

Module-level constants are permitted and encouraged. For example:
`_MAX_HOLY_HANDGRENADE_COUNT = 3` for an internal use constant or
`SIR_LANCELOTS_FAVORITE_COLOR = "blue"` for a public API constant. Constants
must be named using all caps with underscores. See Naming
below.
