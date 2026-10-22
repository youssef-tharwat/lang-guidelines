# import-modules

Import packages and modules, not individual classes or functions (`from sound.effects import echo`, then `echo.EchoFilter(...)`); alias with `as` only for a name clash, a too-generic or too-long name, or a standard abbreviation (`import numpy as np`). Typing symbols from `typing`, `collections.abc` and `typing_extensions` are imported directly.

**Why:** Every name says which module it comes from.

**Sources:** G:s2.2-imports, G:s3.19-type-annotations

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


## Type Annotations (G:s3.19-type-annotations)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s3.19-type-annotations), CC BY 3.0.

### 3.19.1 General Rules

*   Familiarize yourself with
    [type hints](https://docs.python.org/3/library/typing.html).

*   Annotating `self` or `cls` is generally not necessary.
    [`Self`](https://docs.python.org/3/library/typing.html#typing.Self) can be
    used if it is necessary for proper type information, e.g.

    ```python
    from typing import Self

    class BaseClass:
      @classmethod
      def create(cls) -> Self:
        ...

      def difference(self, other: Self) -> float:
        ...
    ```

*   Similarly, don't feel compelled to annotate the return value of `__init__`
    (where `None` is the only valid option).

*   If any other variable or a returned type should not be expressed, use `Any`.

*   You are not required to annotate all the functions in a module.

    -   At least annotate your public APIs.
    -   Use judgment to get to a good balance between safety and clarity on the
        one hand, and flexibility on the other.
    -   Annotate code that is prone to type-related errors (previous bugs or
        complexity).
    -   Annotate code that is hard to understand.
    -   Annotate code as it becomes stable from a types perspective. In many
        cases, you can annotate all the functions in mature code without losing
        too much flexibility.

### 3.19.2 Line Breaking

Try to follow the existing indentation rules.

After annotating, many function signatures will become "one parameter per line".
To ensure the return type is also given its own line, a comma can be placed
after the last parameter.

```python
def my_method(
    self,
    first_var: int,
    second_var: Foo,
    third_var: Bar | None,
) -> int:
  ...
```

Always prefer breaking between variables, and not, for example, between variable
names and type annotations. However, if everything fits on the same line, go for
it.

```python
def my_method(self, first_var: int) -> int:
  ...
```

If the combination of the function name, the last parameter, and the return type
is too long, indent by 4 in a new line. When using line breaks, prefer putting
each parameter and the return type on their own lines and aligning the closing
parenthesis with the `def`:

```python
Yes:
def my_method(
    self,
    other_arg: MyLongType | None,
) -> tuple[MyLongType1, MyLongType1]:
  ...
```

Optionally, the return type may be put on the same line as the last parameter:

```python
Okay:
def my_method(
    self,
    first_var: int,
    second_var: int) -> dict[OtherLongType, MyLongType]:
  ...
```

`pylint`
allows you to move the closing parenthesis to a new line and align with the
opening one, but this is less readable.

```python
No:
def my_method(self,
              other_arg: MyLongType | None,
             ) -> dict[OtherLongType, MyLongType]:
  ...
```

As in the examples above, prefer not to break types. However, sometimes they are
too long to be on a single line (try to keep sub-types unbroken).

```python
def my_method(
    self,
    first_var: tuple[list[MyLongType1],
                     list[MyLongType2]],
    second_var: list[dict[
        MyLongType3, MyLongType4]],
) -> None:
  ...
```

If a single name and type is too long, consider using an
alias for the type. The last resort is to break after the
colon and indent by 4.

```python
Yes:
def my_function(
    long_variable_name:
        long_module_name.LongTypeName,
) -> None:
  ...
```

```python
No:
def my_function(
    long_variable_name: long_module_name.
        LongTypeName,
) -> None:
  ...
```

### 3.19.3 Forward Declarations

If you need to use a class name (from the same module) that is not yet
defined -- for example, if you need the class name inside the declaration of
that class, or if you use a class that is defined later in the code -- either
use `from __future__ import annotations` or use a string for the class name.

```python
Yes:
from __future__ import annotations

class MyClass:
  def __init__(self, stack: Sequence[MyClass], item: OtherClass) -> None:

class OtherClass:
  ...
```

```python
Yes:
class MyClass:
  def __init__(self, stack: Sequence['MyClass'], item: 'OtherClass') -> None:

class OtherClass:
  ...
```

### 3.19.4 Default Values

As per [PEP-008](https://peps.python.org/pep-0008/#other-recommendations), use
spaces around the `=` *only* for arguments that have both a type annotation and
a default value.

```python
Yes:
def func(a: int = 0) -> int:
  ...
```

```python
No:
def func(a:int=0) -> int:
  ...
```

### 3.19.5 NoneType

In the Python type system, `NoneType` is a "first class" type, and for typing
purposes, `None` is an alias for `NoneType`. If an argument can be `None`, it
has to be declared! You can use `|` union type expressions (recommended in new
Python 3.10+ code), or the older `Optional` and `Union` syntaxes.

Use explicit `X | None` instead of implicit. Earlier versions of type checkers
allowed `a: str = None` to be interpreted as `a: str | None = None`, but that is
no longer the preferred behavior.

```python
Yes:
def modern_or_union(a: str | int | None, b: str | None = None) -> str:
  ...
def union_optional(a: Union[str, int, None], b: Optional[str] = None) -> str:
  ...
```

```python
No:
def nullable_union(a: Union[None, str]) -> str:
  ...
def implicit_optional(a: str = None) -> str:
  ...
```

### 3.19.6 Type Aliases

You can declare aliases of complex types. The name of an alias should be
CapWorded. If the alias is used only in this module, it should be \_Private.

Note that the `: TypeAlias` annotation is only supported in versions 3.10+.

```python
from typing import TypeAlias

_LossAndGradient: TypeAlias = tuple[tf.Tensor, tf.Tensor]
ComplexTFMap: TypeAlias = Mapping[str, _LossAndGradient]
```

### 3.19.7 Ignoring Types

You can disable type checking on a line with the special comment `# type:
ignore`.

`pytype` has a disable option for specific errors (similar to lint):

```python
# pytype: disable=attribute-error
```

### 3.19.8 Typing Variables

*Annotated Assignments*
:   If an internal variable has a type that is hard or impossible to infer,
    specify its type with an annotated assignment - use a colon and type between
    the variable name and value (the same as is done with function arguments
    that have a default value):

    ```python
    a: Foo = SomeUndecoratedFunction()
    ```

*Type Comments*
:   Though you may see them remaining in the codebase (they were necessary
    before Python 3.6), do not add any more uses of a `# type: <type name>`
    comment on the end of the line:

    ```python
    a = SomeUndecoratedFunction()  # type: Foo
    ```

### 3.19.9 Tuples vs Lists

Typed lists can only contain objects of a single type. Typed tuples can either
have a single repeated type or a set number of elements with different types.
The latter is commonly used as the return type from a function.

```python
a: list[int] = [1, 2, 3]
b: tuple[int, ...] = (1, 2, 3)
c: tuple[int, str, float] = (1, "2", 3.5)
```

### 3.19.10 Type variables

The Python type system has
[generics](https://docs.python.org/3/library/typing.html#generics). A type
variable, such as `TypeVar` and `ParamSpec`, is a common way to use them.

Example:

```python
from collections.abc import Callable
from typing import ParamSpec, TypeVar
_P = ParamSpec("_P")
_T = TypeVar("_T")
...
def next(l: list[_T]) -> _T:
  return l.pop()

def print_when_called(f: Callable[_P, _T]) -> Callable[_P, _T]:
  def inner(*args: _P.args, **kwargs: _P.kwargs) -> _T:
    print("Function was called")
    return f(*args, **kwargs)
  return inner
```

A `TypeVar` can be constrained:

```python
AddableType = TypeVar("AddableType", int, float, str)
def add(a: AddableType, b: AddableType) -> AddableType:
  return a + b
```

A common predefined type variable in the `typing` module is `AnyStr`. Use it for
multiple annotations that can be `bytes` or `str` and must all be the same type.

```python
from typing import AnyStr
def check_length(x: AnyStr) -> AnyStr:
  if len(x) <= 42:
    return x
  raise ValueError()
```

A type variable must have a descriptive name, unless it meets all of the
following criteria:

*   not externally visible
*   not constrained

```python
Yes:
  _T = TypeVar("_T")
  _P = ParamSpec("_P")
  AddableType = TypeVar("AddableType", int, float, str)
  AnyFunction = TypeVar("AnyFunction", bound=Callable)
```

```python
No:
  T = TypeVar("T")
  P = ParamSpec("P")
  _T = TypeVar("_T", int, float, str)
  _F = TypeVar("_F", bound=Callable)
```

### 3.19.11 String types

> Do not use `typing.Text` in new code. It's only for Python 2/3 compatibility.

Use `str` for string/text data. For code that deals with binary data, use
`bytes`.

```python
def deals_with_text_data(x: str) -> str:
  ...
def deals_with_binary_data(x: bytes) -> bytes:
  ...
```

If all the string types of a function are always the same, for example if the
return type is the same as the argument type in the code above, use
AnyStr.

### 3.19.12 Imports For Typing

For symbols (including types, functions, and constants) from the `typing` or
`collections.abc` modules used to support static analysis and type checking,
always import the symbol itself. This keeps common annotations more concise and
matches typing practices used around the world. You are explicitly allowed to
import multiple specific symbols on one line from the `typing` and
`collections.abc` modules. For example:

```python
from collections.abc import Mapping, Sequence
from typing import Any, Generic, cast, TYPE_CHECKING
```

Given that this way of importing adds items to the local namespace, names in
`typing` or `collections.abc` should be treated similarly to keywords, and not
be defined in your Python code, typed or not. If there is a collision between a
type and an existing name in a module, import it using `import x as y`.

```python
from typing import Any as AnyType
```

When annotating function signatures, prefer abstract container types like
`collections.abc.Sequence` over concrete types like `list`. If you need to use a
concrete type (for example, a `tuple` of typed elements), prefer built-in types
like `tuple` over the parametric type aliases from the `typing` module (e.g.,
`typing.Tuple`).

```python
from typing import List, Tuple

def transform_coordinates(original: List[Tuple[float, float]]) ->
    List[Tuple[float, float]]:
  ...
```

```python
from collections.abc import Sequence

def transform_coordinates(original: Sequence[tuple[float, float]]) ->
    Sequence[tuple[float, float]]:
  ...
```

### 3.19.13 Conditional Imports

Use conditional imports only in exceptional cases where the additional imports
needed for type checking must be avoided at runtime. This pattern is
discouraged; alternatives such as refactoring the code to allow top-level
imports should be preferred.

Imports that are needed only for type annotations can be placed within an `if
TYPE_CHECKING:` block.

-   Conditionally imported types need to be referenced as strings, to be forward
    compatible with Python 3.6 where the annotation expressions are actually
    evaluated.
-   Only entities that are used solely for typing should be defined here; this
    includes aliases. Otherwise it will be a runtime error, as the module will
    not be imported at runtime.
-   The block should be right after all the normal imports.
-   There should be no empty lines in the typing imports list.
-   Sort this list as if it were a regular imports list.
```python
import typing
if typing.TYPE_CHECKING:
  import sketch
def f(x: "sketch.Sketch"): ...
```

### 3.19.14 Circular Dependencies

Circular dependencies that are caused by typing are code smells. Such code is a
good candidate for refactoring. Although technically it is possible to keep
circular dependencies, various build systems will not let you do so
because each module has to depend on the other.

Replace modules that create circular dependency imports with `Any`. Set an
alias with a meaningful name, and use the real type name from
this module (any attribute of `Any` is `Any`). Alias definitions should be
separated from the last import by one line.

```python
from typing import Any

some_mod = Any  # some_mod.py imports this module.
...

def my_method(self, var: "some_mod.SomeType") -> None:
  ...
```

### 3.19.15 Generics

When annotating, prefer to specify type parameters for
[generic](https://docs.python.org/3/library/typing.html#generics) types in a
parameter list; otherwise, the generics' parameters will be assumed to be
[`Any`](https://docs.python.org/3/library/typing.html#the-any-type).

```python
# Yes:
def get_names(employee_ids: Sequence[int]) -> Mapping[int, str]:
  ...
```

```python
# No:
# This is interpreted as get_names(employee_ids: Sequence[Any]) -> Mapping[Any, Any]
def get_names(employee_ids: Sequence) -> Mapping:
  ...
```

If the best type parameter for a generic is `Any`, make it explicit, but
remember that in many cases `TypeVar` might be more
appropriate:

```python
# No:
def get_names(employee_ids: Sequence[Any]) -> Mapping[Any, str]:
  """Returns a mapping from employee ID to employee name for given IDs."""
```

```python
# Yes:
_T = TypeVar('_T')
def get_names(employee_ids: Sequence[_T]) -> Mapping[_T, str]:
  """Returns a mapping from employee ID to employee name for given IDs."""
```
