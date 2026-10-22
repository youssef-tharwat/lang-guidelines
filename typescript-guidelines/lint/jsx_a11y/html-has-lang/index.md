
### What it does

Ensures that every HTML document has a lang attribute.

### Why is this bad?

If the language of a webpage is not specified,
the screen reader assumes the default language set by the user.
Language settings become an issue for users who speak multiple languages
and access website in more than one language.

### Examples

Examples of **incorrect** code for this rule:

```jsx
<html />
```

Examples of **correct** code for this rule:

```jsx
<html lang="en" />
```

## How to use

## References
