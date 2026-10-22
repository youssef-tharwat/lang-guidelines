# conditional-expressions

Use a conditional expression only when each of its three parts fits on one line; otherwise write an `if` statement.

**Why:** Long ternaries hide the condition.

**Sources:** G:s2.11-conditional-expressions

---

## Conditional Expressions (G:s2.11-conditional-expressions)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.11-conditional-expressions), CC BY 3.0.

Okay for simple cases.

### 2.11.1 Definition

Conditional expressions (sometimes called a “ternary operator”) are mechanisms
that provide a shorter syntax for if statements. For example: `x = 1 if cond
else 2`.

### 2.11.2 Pros

Shorter and more convenient than an if statement.

### 2.11.3 Cons

May be harder to read than an if statement. The condition may be difficult to
locate if the expression is long.

### 2.11.4 Decision

Okay to use for simple cases. Each portion must fit on one line:
true-expression, if-expression, else-expression. Use a complete if statement
when things get more complicated.

```python
Yes:
    one_line = 'yes' if predicate(value) else 'no'
    slightly_split = ('yes' if predicate(value)
                      else 'no, nein, nyet')
    the_longest_ternary_style_that_can_be_done = (
        'yes, true, affirmative, confirmed, correct'
        if predicate(value)
        else 'no, false, negative, nay')
```

```python
No:
    bad_line_breaking = ('yes' if predicate(value) else
                         'no')
    portion_too_long = ('yes'
                        if some_long_module.some_long_predicate_function(
                            really_long_variable_name)
                        else 'no, false, negative, nay')
```
