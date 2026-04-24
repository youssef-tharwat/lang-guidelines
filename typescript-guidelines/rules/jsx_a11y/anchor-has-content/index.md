
### What it does

Enforce that anchors have content and that the content is accessible to screen readers.
Accessible means that it is not hidden using the `aria-hidden` prop.

Alternatively, you may use the `title` prop or the `aria-label` prop.

### Why is this bad?

Anchor elements without content can be confusing for users relying
on screen readers to understand.

### Examples

Examples of **correct** code for this rule:

```jsx
<a>Anchor Content!</a>
<a><TextWrapper /></a>
<a dangerouslySetInnerHTML={{ __html: 'foo' }} />
<a title='foo' />
<a aria-label='foo' />
```

Examples of **incorrect** code for this rule:

```jsx
<a />
<a><TextWrapper aria-hidden /></a>
```

## How to use

## References
