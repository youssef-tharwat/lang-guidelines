
### What it does

Enforce iframe elements have a title attribute.

### Why is this bad?

Screen reader users rely on a iframe title to describe the contents of
the iframe. Navigating through iframe and iframe elements quickly
becomes difficult and confusing for users of this technology if the
markup does not contain a title attribute.

### Examples

Examples of **incorrect** code for this rule:

```jsx
<iframe />
<iframe {...props} />
<iframe title="" />
<iframe title={''} />
<iframe title={``} />
<iframe title={undefined} />
<iframe title={false} />
<iframe title={true} />
<iframe title={42} />
```

Examples of **correct** code for this rule:

```jsx
<iframe title="This is a unique title" />
<iframe title={uniqueTitle} />
```

## How to use

## References
