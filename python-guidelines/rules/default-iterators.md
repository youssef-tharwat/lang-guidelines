# default-iterators

Iterate containers directly (`for key in d`, `for k, v in d.items()`, `for line in f`) and test membership with `in`; don't iterate `.keys()` or `.readlines()`, and never mutate a container while iterating it.

**Why:** Direct iteration is simpler, faster and generic.

**Sources:** G:s2.8-default-iterators-and-operators

---

## Default Iterators and Operators (G:s2.8-default-iterators-and-operators)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.8-default-iterators-and-operators), CC BY 3.0.

Use default iterators and operators for types that support them, like lists,
dictionaries, and files.

### 2.8.1 Definition

Container types, like dictionaries and lists, define default iterators and
membership test operators ("in" and "not in").

### 2.8.2 Pros

The default iterators and operators are simple and efficient. They express the
operation directly, without extra method calls. A function that uses default
operators is generic. It can be used with any type that supports the operation.

### 2.8.3 Cons

You can't tell the type of objects by reading the method names (unless the
variable has type annotations). This is also an advantage.

### 2.8.4 Decision

Use default iterators and operators for types that support them, like lists,
dictionaries, and files. The built-in types define iterator methods, too. Prefer
these methods to methods that return lists, except that you should not mutate a
container while iterating over it.

```python
Yes:  for key in adict: ...
      if obj in alist: ...
      for line in afile: ...
      for k, v in adict.items(): ...
```

```python
No:   for key in adict.keys(): ...
      for line in afile.readlines(): ...
```
