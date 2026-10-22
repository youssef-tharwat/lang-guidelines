# lambdas

Use a lambda only for a short one-liner; prefer a generator expression to `map`/`filter` with a lambda, and `operator` functions (`operator.mul`) to trivial lambdas.

**Why:** Named functions read and debug better.

**Sources:** G:s2.10-lambda-functions

---

## Lambda Functions (G:s2.10-lambda-functions)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.10-lambda-functions), CC BY 3.0.

Okay for one-liners. Prefer generator expressions over `map()` or `filter()`
with a `lambda`.

### 2.10.1 Definition

Lambdas define anonymous functions in an expression, as opposed to a statement.

### 2.10.2 Pros

Convenient.

### 2.10.3 Cons

Harder to read and debug than local functions. The lack of names means stack
traces are more difficult to understand. Expressiveness is limited because the
function may only contain an expression.

### 2.10.4 Decision

Lambdas are allowed. If the code inside the lambda function spans multiple lines
or is longer than 60-80 chars, it might be better to define it as a regular
nested function.

For common operations like multiplication, use the functions from the `operator`
module instead of lambda functions. For example, prefer `operator.mul` to
`lambda x, y: x * y`.
