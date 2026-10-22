# todo-format

Write TODOs as `# TODO: <issue link> - <what to do>`, never with a person as the context, and with a specific date or event when they are time-bound.

**Why:** TODOs stay searchable and actionable.

**Sources:** G:s3.12-todo-comments

---

## TODO Comments (G:s3.12-todo-comments)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s3.12-todo-comments), CC BY 3.0.

Use `TODO` comments for code that is temporary, a short-term solution, or
good-enough but not perfect.

A `TODO` comment begins with the word `TODO` in all caps, a following colon, and
a link to a resource that contains the context, ideally a bug reference. A bug
reference is preferable because bugs are tracked and have follow-up comments.
Follow this piece of context with an explanatory string introduced with a hyphen
`-`. 
The purpose is to have a consistent `TODO` format that can be searched to find
out how to get more details. 

```python
# TODO: crbug.com/192795 - Investigate cpufreq optimizations.
```

Old style, formerly recommended, but discouraged for use in new code:

```python
# TODO(crbug.com/192795): Investigate cpufreq optimizations.
# TODO(yourusername): Use a "\*" here for concatenation operator.
```

Avoid adding TODOs that refer to an individual or team as the context:

```python
# TODO: @yourusername - File an issue and use a '*' for repetition.
```

If your `TODO` is of the form "At a future date do something" make sure that you
either include a very specific date ("Fix by November 2009") or a very specific
event ("Remove this code when all clients can handle XML responses.") that
future code maintainers will comprehend. Issues are ideal for tracking this.
