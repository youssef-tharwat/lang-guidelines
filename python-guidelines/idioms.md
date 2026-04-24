# Python Idioms

Positive patterns to favor while writing Python. Complement to the lint-rule
prohibitions in `guidelines.txt` — these are things a correct program **does**,
not just things it avoids.

## Paths & filesystem
- Prefer `pathlib.Path` over `os.path` for all path manipulation.
- Use `Path.read_text() / write_text()` over `open() + read() / write()` for
  whole-file I/O.
- Use `with open(...)` (context manager) for streaming I/O.

## Strings
- Prefer f-strings (`f"{x}"`) over `%` formatting or `.format()`.
- Use `str.removeprefix` / `str.removesuffix` (3.9+) over slicing.
- `"".join(parts)` over repeated `+=` on strings inside loops.

## Comparisons & booleans
- Use `is None` / `is not None`, never `== None`.
- `if not x:` only when falsy collections are intended; otherwise `if x is None:`
  or `if len(x) == 0:`.

## Collections
- Use comprehensions (`[x for x in …]`, `{k: v for …}`) when the transformation
  fits on one or two lines.
- `enumerate(iter)` over manual index tracking; `zip(a, b)` over parallel indexing.
- `dict.get(k, default)` over `if k in d: d[k] else: default`.
- `collections.defaultdict` / `collections.Counter` when building histograms.

## Types
- Type-hint all public function signatures.
- On Python ≥ 3.10: use `X | None` over `Optional[X]`, `list[X]` over
  `List[X]`, `dict[K, V]` over `Dict[K, V]`.
- Use `typing.Final` for module-level constants, `typing.Literal` for enum-like
  string params, `typing.TypedDict` or `@dataclass` for structured records.
- `Protocol` over `abc.ABC` when duck-typing is enough.

## Errors
- Raise with `raise X("…") from err` to preserve causal chain.
- Never `except:` bare; always `except SpecificError:` or `except Exception:`
  with re-raise.
- Prefer guard clauses over deeply nested conditionals.

## Data classes
- Use `@dataclass(slots=True, frozen=True)` for value objects.
- Use `pydantic.BaseModel` for I/O validation (API request/response, CLI
  input). Don't use it for internal DTOs.

## Concurrency
- `asyncio.TaskGroup` (3.11+) over manual `asyncio.gather` for structured
  concurrency.
- Never block the event loop; wrap sync I/O in `asyncio.to_thread`.

## Subprocess / OS
- `subprocess.run(args, check=True, capture_output=True, text=True)` — never
  `shell=True` with user input.

## Structural dispatch
- Use `match` / `case` (3.10+) for structural dispatch on sum types instead of
  `isinstance` ladders.

## Imports
- Absolute imports in application code; relative (`.`) only within libraries.
- One import per line for `from X import Y, Z` only if the list is short;
  otherwise split.
