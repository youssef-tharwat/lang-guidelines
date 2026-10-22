# small-functions

Keep functions small and focused; past about 40 lines, look for a split that keeps the structure clear.

**Why:** Long functions breed hard-to-find bugs as they grow.

**Sources:** G:s3.18-function-length

---

## Function length (G:s3.18-function-length)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s3.18-function-length), CC BY 3.0.

Prefer small and focused functions.

We recognize that long functions are sometimes appropriate, so no hard limit is
placed on function length. If a function exceeds about 40 lines, think about
whether it can be broken up without harming the structure of the program.

Even if your long function works perfectly now, someone modifying it in a few
months may add new behavior. This could result in bugs that are hard to find.
Keeping your functions short and simple makes it easier for other people to read
and modify your code.

You could find long and complicated functions when working with
some
code. Do not be intimidated by modifying existing code: if working with such a
function proves to be difficult, you find that errors are hard to debug, or you
want to use a piece of it in several different contexts, consider breaking up
the function into smaller and more manageable pieces.
