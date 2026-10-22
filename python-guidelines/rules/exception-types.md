# exception-types

Raise built-in exceptions where they fit (`ValueError` for a violated precondition); a library's own exceptions subclass an existing exception and are named with an `Error` suffix that doesn't repeat the module (`foo.Error`, not `foo.FooError`).

**Why:** Callers can catch precisely.

**Sources:** G:s2.4-exceptions

---

## Exceptions (G:s2.4-exceptions)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.4-exceptions), CC BY 3.0.

Exceptions are allowed but must be used carefully.

### 2.4.1 Definition

Exceptions are a means of breaking out of normal control flow to handle errors
or other exceptional conditions.

### 2.4.2 Pros

The control flow of normal operation code is not cluttered by error-handling
code. It also allows the control flow to skip multiple frames when a certain
condition occurs, e.g., returning from N nested functions in one step instead of
having to plumb error codes through.

### 2.4.3 Cons

May cause the control flow to be confusing. Easy to miss error cases when making
library calls.

### 2.4.4 Decision

Exceptions must follow certain conditions:

-   Make use of built-in exception classes when it makes sense. For example,
    raise a `ValueError` to indicate a programming mistake like a violated
    precondition, such as may happen when validating function arguments.

-   Do not use `assert` statements in place of conditionals or validating
    preconditions. They must not be critical to the application logic. A litmus
    test would be that the `assert` could be removed without breaking the code.
    `assert` conditionals are
    [not guaranteed](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)
    to be evaluated. For [pytest](https://pytest.org) based tests, `assert` is
    okay and expected to verify expectations. For
    example:

    
    ```python
    Yes:
      def connect_to_next_port(self, minimum: int) -> int:
        """Connects to the next available port.

        Args:
          minimum: A port value greater or equal to 1024.

        Returns:
          The new minimum port.

        Raises:
          ConnectionError: If no available port is found.
        """
        if minimum < 1024:
          # Note that this raising of ValueError is not mentioned in the doc
          # string's "Raises:" section because it is not appropriate to
          # guarantee this specific behavioral reaction to API misuse.
          raise ValueError(f'Min. port must be at least 1024, not {minimum}.')
        port = self._find_next_open_port(minimum)
        if port is None:
          raise ConnectionError(
              f'Could not connect to service on port {minimum} or higher.')
        # The code does not depend on the result of this assert.
        assert port >= minimum, (
            f'Unexpected port {port} when minimum was {minimum}.')
        return port
    ```

    ```python
    No:
      def connect_to_next_port(self, minimum: int) -> int:
        """Connects to the next available port.

        Args:
          minimum: A port value greater or equal to 1024.

        Returns:
          The new minimum port.
        """
        assert minimum >= 1024, 'Minimum port must be at least 1024.'
        # The following code depends on the previous assert.
        port = self._find_next_open_port(minimum)
        assert port is not None
        # The type checking of the return statement relies on the assert.
        return port
    ```

-   Libraries or packages may define their own exceptions. When doing so they
    must inherit from an existing exception class. Exception names should end in
    `Error` and should not introduce repetition (`foo.FooError`).

-   Never use catch-all `except:` statements, or catch `Exception` or
    `StandardError`, unless you are

    -   re-raising the exception, or
    -   creating an isolation point in the program where exceptions are not
        propagated but are recorded and suppressed instead, such as protecting a
        thread from crashing by guarding its outermost block.

    Python is very tolerant in this regard and `except:` will really catch
    everything including misspelled names, sys.exit() calls, Ctrl+C interrupts,
    unittest failures and all kinds of other exceptions that you simply don't
    want to catch.

-   Minimize the amount of code in a `try`/`except` block. The larger the body
    of the `try`, the more likely that an exception will be raised by a line of
    code that you didn't expect to raise an exception. In those cases, the
    `try`/`except` block hides a real error.

-   Use the `finally` clause to execute code whether or not an exception is
    raised in the `try` block. This is often useful for cleanup, i.e., closing a
    file.
