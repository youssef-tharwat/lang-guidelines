# simple-comprehensions

Keep comprehensions and generator expressions to one `for` clause and at most one filter; write a loop beyond that.

**Why:** Nested comprehensions are hard to read.

**Sources:** G:s2.7-comprehensions

---

## Comprehensions & Generator Expressions (G:s2.7-comprehensions)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.7-comprehensions), CC BY 3.0.

Okay to use for simple cases.

### 2.7.1 Definition

List, Dict, and Set comprehensions as well as generator expressions provide a
concise and efficient way to create container types and iterators without
resorting to the use of traditional loops, `map()`, `filter()`, or `lambda`.

### 2.7.2 Pros

Simple comprehensions can be clearer and simpler than other dict, list, or set
creation techniques. Generator expressions can be very efficient, since they
avoid the creation of a list entirely.

### 2.7.3 Cons

Complicated comprehensions or generator expressions can be hard to read.

### 2.7.4 Decision

Comprehensions are allowed, however multiple `for` clauses or filter expressions
are not permitted. Optimize for readability, not conciseness.

```python
Yes:
  result = [mapping_expr for value in iterable if filter_expr]

  result = [
      is_valid(metric={'key': value})
      for value in interesting_iterable
      if a_longer_filter_expression(value)
  ]

  descriptive_name = [
      transform({'key': key, 'value': value}, color='black')
      for key, value in generate_iterable(some_input)
      if complicated_condition_is_met(key, value)
  ]

  result = []
  for x in range(10):
    for y in range(5):
      if x * y > 10:
        result.append((x, y))

  return {
      x: complicated_transform(x)
      for x in long_generator_function(parameter)
      if x is not None
  }

  return (x**2 for x in range(10))

  unique_names = {user.name for user in users if user is not None}
```

```python
No:
  result = [(x, y) for x in range(10) for y in range(5) if x * y > 10]

  return (
      (x, y, z)
      for x in range(5)
      for y in range(5)
      if x != y
      for z in range(5)
      if y != z
  )
```
