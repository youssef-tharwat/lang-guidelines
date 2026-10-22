---
type: llm
focus: {source: file, path: rate_limiter.py}
weight: 3
---

Judge the module in `rate_limiter.py`. Pass when ALL of these hold:

1. Shared mutable state is protected by `threading` primitives (a lock or condition), not by relying on atomicity of built-in types.
2. There is no mutable module-level state reached through `global`; state lives in instances (a module-level shared instance is acceptable if internal and reached through functions).
3. Time comes from a monotonic clock (`time.monotonic`) or an injected clock, not wall-clock time.
4. The demo runs only under `if __name__ == '__main__':` and calls a `main()` function.
5. The module, public classes and public functions have docstrings, and signatures are annotated.
6. No mutable default arguments and no `staticmethod`.

Fail if any item is missing. List each item as met or not met before the verdict.
