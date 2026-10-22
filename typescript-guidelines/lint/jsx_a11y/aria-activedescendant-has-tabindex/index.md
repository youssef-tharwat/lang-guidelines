
### What it does

Enforce elements with aria-activedescendant are tabbable.

### Why is this bad?

Elements with `aria-activedescendant` must be tabbable for users to
navigate to them using keyboard input. Without proper tabindex, screen
reader users cannot access the element through keyboard navigation,
making the functionality inaccessible.

### Examples

Examples of **incorrect** code for this rule:

```jsx
const Bad = <div aria-activedescendant={someID} />;
```

Examples of **correct** code for this rule:

```jsx
const Good = (
  <>
    <CustomComponent />
    <CustomComponent aria-activedescendant={someID} />
    <CustomComponent aria-activedescendant={someID} tabIndex={0} />
    <CustomComponent aria-activedescendant={someID} tabIndex={-1} />
    <div />
    <input />
    <div tabIndex={0} />
    <div aria-activedescendant={someID} tabIndex={0} />
    <div aria-activedescendant={someID} tabIndex="0" />
    <div aria-activedescendant={someID} tabIndex={1} />
    <div aria-activedescendant={someID} tabIndex={-1} />
    <div aria-activedescendant={someID} tabIndex="-1" />
    <input aria-activedescendant={someID} />
    <input aria-activedescendant={someID} tabIndex={0} />
    <input aria-activedescendant={someID} tabIndex={-1} />
  </>
);
```

## How to use

## References
