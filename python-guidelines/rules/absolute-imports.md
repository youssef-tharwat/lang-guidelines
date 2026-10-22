# absolute-imports

Import every module by its full package path; no relative imports, and never assume the main script's directory is on `sys.path`.

**Why:** Imports resolve the same way everywhere.

**Sources:** G:s2.2-imports, G:s2.3-packages

---

## Imports (G:s2.2-imports)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.2-imports), CC BY 3.0.

Use `import` statements for packages and modules only, not for individual types,
classes, or functions.

### 2.2.1 Definition

Reusability mechanism for sharing code from one module to another.

### 2.2.2 Pros

The namespace management convention is simple. The source of each identifier is
indicated in a consistent way; `x.Obj` says that object `Obj` is defined in
module `x`.

### 2.2.3 Cons

Module names can still collide. Some module names are inconveniently long.

### 2.2.4 Decision

*   Use `import x` for importing packages and modules.
*   Use `from x import y` where `x` is the package prefix and `y` is the module
    name with no prefix.
*   Use `from x import y as z` in any of the following circumstances:
    -   Two modules named `y` are to be imported.
    -   `y` conflicts with a top-level name defined in the current module.
    -   `y` conflicts with a common parameter name that is part of the public
        API (e.g., `features`).
    -   `y` is an inconveniently long name.
    -   `y` is too generic in the context of your code (e.g., `from
        storage.file_system import options as fs_options`).
*   Use `import y as z` only when `z` is a standard abbreviation (e.g., `import
    numpy as np`).

For example the module `sound.effects.echo` may be imported as follows:

```python
from sound.effects import echo
...
echo.EchoFilter(input, output, delay=0.7, atten=4)
```

Do not use relative names in imports. Even if the module is in the same package,
use the full package name. This helps prevent unintentionally importing a
package twice.

#### 2.2.4.1 Exemptions

Exemptions from this rule:

*   Symbols from the following modules are used to support static analysis and
    type checking:
    *   `typing` module
    *   `collections.abc` module
    *   [`typing_extensions` module](https://github.com/python/typing_extensions/blob/main/README.md)
*   Redirects from the
    [six.moves module](https://six.readthedocs.io/#module-six.moves).


## Packages (G:s2.3-packages)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.3-packages), CC BY 3.0.

Import each module using the full pathname location of the module.

### 2.3.1 Pros

Avoids conflicts in module names or incorrect imports due to the module search
path not being what the author expected. Makes it easier to find modules.

### 2.3.2 Cons

Makes it harder to deploy code because you have to replicate the package
hierarchy. Not really a problem with modern deployment mechanisms.

### 2.3.3 Decision

All new code should import each module by its full package name.

Imports should be as follows:

```python
Yes:
  # Reference absl.flags in code with the complete name (verbose).
  import absl.flags
  from doctor.who import jodie

  _FOO = absl.flags.DEFINE_string(...)
```

```python
Yes:
  # Reference flags in code with just the module name (common).
  from absl import flags
  from doctor.who import jodie

  _FOO = flags.DEFINE_string(...)
```

*(assume this file lives in `doctor/who/` where `jodie.py` also exists)*

```python
No:
  # Unclear what module the author wanted and what will be imported.  The actual
  # import behavior depends on external factors controlling sys.path.
  # Which possible jodie module did the author intend to import?
  import jodie
```

The directory the main binary is located in should not be assumed to be in
`sys.path` despite that happening in some environments. This being the case,
code should assume that `import jodie` refers to a third-party or top-level
package named `jodie`, not a local `jodie.py`.
