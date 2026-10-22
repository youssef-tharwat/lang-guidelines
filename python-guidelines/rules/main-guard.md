# main-guard

Put an executable's logic in `main()`, called under `if __name__ == '__main__':`, and do nothing at import time beyond definitions; start only directly executed files with `#!/usr/bin/env python3`.

**Why:** Modules stay importable by tests and tools.

**Sources:** G:s3.17-main, G:s3.7-shebang-line

---

## Main (G:s3.17-main)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s3.17-main), CC BY 3.0.

In Python, `pydoc` as well as unit tests require modules to be importable. If a
file is meant to be used as an executable, its main functionality should be in a
`main()` function, and your code should always check `if __name__ == '__main__'`
before executing your main program, so that it is not executed when the module
is imported.

When using [absl](https://github.com/abseil/abseil-py), use `app.run`:

```python
from absl import app
...

def main(argv: Sequence[str]):
    # process non-flag arguments
    ...

if __name__ == '__main__':
    app.run(main)
```

Otherwise, use:

```python
def main():
    ...

if __name__ == '__main__':
    main()
```

All code at the top level will be executed when the module is imported. Be
careful not to call functions, create objects, or perform other operations that
should not be executed when the file is being `pydoc`ed.


## Shebang Line (G:s3.7-shebang-line)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s3.7-shebang-line), CC BY 3.0.

Most `.py` files do not need to start with a `#!` line. Start the main file of a
program with
`#!/usr/bin/env python3` (to support virtualenvs) or `#!/usr/bin/python3` per
[PEP-394](https://peps.python.org/pep-0394/).

This line is used by the kernel to find the Python interpreter, but is ignored by Python when importing modules. It is only necessary on a file intended to be executed directly.
