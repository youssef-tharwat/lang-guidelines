# React Rules (TypeScript & JavaScript)

92 rules that apply when the project uses **react**.
Load this file only if the project's manifest imports or depends on
`react`.

---

### jsx_a11y/alt-text
Enforce that all elements that require alternative text have meaningful information to relay back to the end user.
❌ 
```
<img src="flower.jpg" />
<img src="flower.jpg" alt="" />
<object />
<area />
```
✅ 
```
<img src="flower.jpg" alt="A close-up of a white daisy" />
<img src="decorative.jpg" alt="" role="presentation" />
<object aria-label="Interactive chart" />
<area alt="Navigation link" />
```

### jsx_a11y/anchor-ambiguous-text
Inspects anchor link text for the use of ambiguous words.
❌ 
```
<a>link</a>
<a>click here</a>
```
✅ 
```
<a>read this tutorial</a>
<a aria-label="oxc linter documentation">click here</a>
```

### jsx_a11y/anchor-has-content
Enforce that anchors have content and that the content is accessible to screen readers.
❌ 
```
<a />
<a><TextWrapper aria-hidden /></a>
```
✅ 
```
<a>Anchor Content!</a>
<a><TextWrapper /></a>
<a dangerouslySetInnerHTML={{ __html: 'foo' }} />
<a title='foo' />
<a aria-label='foo' />
```

### jsx_a11y/anchor-is-valid
The HTML `<a>` element, with a valid href attribute, is formally defined as representing a **hyperlink**.

### jsx_a11y/aria-activedescendant-has-tabindex
Enforce elements with aria-activedescendant are tabbable.
❌ `const Bad = <div aria-activedescendant={someID} />;`
✅ 
```
const Good = (
  <>
    <CustomComponent />
    <CustomComponent aria-activedescendant={someID} />
    <CustomComponent aria-activedescendant={someID} tabIndex={0} />
    <CustomComponent aria-activedescendant={someID} tabIndex={-1} />
…
```

### jsx_a11y/aria-props
Enforce that elements do not use invalid ARIA attributes.
❌ `<input aria-labeledby="address_label" />`
✅ `<input aria-labelledby="address_label" />`

### jsx_a11y/aria-proptypes
Enforce that elements do not use invalid ARIA state and property values.
❌ 
```
<div aria-level="yes" />
<div aria-relevant="additions removalss" />
```
✅ 
```
<div aria-label="foo" />
<div aria-labelledby="foo bar" />
<div aria-checked={false} />
<div aria-invalid="grammar" />
```

### jsx_a11y/aria-role
Elements with ARIA roles must use a valid, non-abstract ARIA role.
❌ 
```
<div role="datepicker"></div> <!-- Bad: "datepicker" is not an ARIA role -->
<div role="range"></div>      <!-- Bad: "range" is an _abstract_ ARIA role -->
<div role=""></div>           <!-- Bad: An empty ARIA role is not allowed -->
<Foo role={role}></Foo>       <!-- Bad: ignoreNonDOM is set to false or not set -->
```
✅ 
```
<div role="button"></div>     <!-- Good: "button" is a valid ARIA role -->
<div role={role}></div>       <!-- Good: role is a variable & cannot be determined until runtime. -->
<div></div>                   <!-- Good: No ARIA role -->
<Foo role={role}></Foo>       <!-- Good: ignoreNonDOM is set to true -->
```

### jsx_a11y/aria-unsupported-elements
Enforce that reserved DOM elements do not contain ARIA roles, states, or properties.
❌ `<meta charset="UTF-8" aria-hidden="false" />`
✅ `<meta charset="UTF-8" />`

### jsx_a11y/autocomplete-valid
Enforce that an element's autocomplete attribute must be a valid value.
❌ `<input autocomplete="invalid-value" />`
✅ `<input autocomplete="name" />`

### jsx_a11y/click-events-have-key-events
Enforce onClick is accompanied by at least one of the following: onKeyUp, onKeyDown, onKeyPress.
❌ `<div onClick={() => void 0} />`
✅ `<div onClick={() => void 0} onKeyDown={() => void 0} />`

### jsx_a11y/heading-has-content
Enforce that heading elements (h1, h2, etc.) have content and that the content is accessible to screen readers.
❌ `<h1 />`
✅ `<h1>Foo</h1>`

### jsx_a11y/html-has-lang
Ensures that every HTML document has a lang attribute.
❌ `<html />`
✅ `<html lang="en" />`

### jsx_a11y/iframe-has-title
Enforce iframe elements have a title attribute.
❌ 
```
<iframe />
<iframe {...props} />
<iframe title="" />
<iframe title={''} />
<iframe title={``} />
<iframe title={undefined} />
…
```
✅ 
```
<iframe title="This is a unique title" />
<iframe title={uniqueTitle} />
```

### jsx_a11y/img-redundant-alt
Enforce that `img` alt attributes do not contain redundant words like "image", "picture", or "photo".
❌ 
```
<img src="foo" alt="Photo of foo being weird." />
<img src="bar" alt="Image of me at a bar!" />
<img src="baz" alt="Picture of baz fixing a bug." />
```
✅ 
```
<img src="foo" alt="Foo eating a sandwich." />
<img src="bar" aria-hidden alt="Picture of me taking a photo of an image" /> // Will pass because it is hidden.
<img src="baz" alt={`Baz taking a ${photo}`} /> // This is valid since photo is a variable name.
```

### jsx_a11y/label-has-associated-control
Enforce that a label tag has a text label and an associated control.
❌ 
```
function Foo(props) {
    return <label {...props} />
}
<input type="text" />
<label>Surname</label>
```
✅ 
```
function Foo(props) {
  const { htmlFor, ...otherProps } = props;
  return <label htmlFor={htmlFor} {...otherProps} />;
}
<label>
  <input type="text" />
…
```

### jsx_a11y/lang
The lang prop on the `<html>` element must be a valid IETF's BCP 47 language tag.
❌ 
```
<html>
<html lang="foo">
```
✅ 
```
<html lang="en">
<html lang="en-US">
```

### jsx_a11y/media-has-caption
If `<audio>` and `<video>` elements have a `<track>` element for captions.
❌ 
```
<audio></audio>
<video></video>
```
✅ 
```
<audio><track kind="captions" src="caption_file.vtt" /></audio>
<video><track kind="captions" src="caption_file.vtt" /></video>
```

### jsx_a11y/mouse-events-have-key-events
Enforce `onMouseOver`/`onMouseOut` are accompanied by `onFocus`/`onBlur`.
❌ `<div onMouseOver={() => void 0} />`
✅ `<div onMouseOver={() => void 0} onFocus={() => void 0} />`

### jsx_a11y/no-access-key
Enforce that the `accessKey` prop is not used on any element to avoid complications with keyboard commands used by a screenreader.
❌ `<div accessKey="h" />`
✅ `<div />`

### jsx_a11y/no-aria-hidden-on-focusable
Enforce that `aria-hidden="true"` is not set on focusable elements.
❌ `<div aria-hidden="true" tabIndex="0" />`
✅ `<div aria-hidden="true" />`

### jsx_a11y/no-autofocus
Enforce that `autoFocus` prop is not used on elements.
❌ 
```
<div autoFocus />
<div autoFocus="true" />
<div autoFocus="false" />
<div autoFocus={undefined} />
```
✅ `<div />`

### jsx_a11y/no-distracting-elements
Enforce that no distracting elements are used.
❌ 
```
<marquee />
<marquee {...props} />
<marquee lang={undefined} />
<blink />
<blink {...props} />
<blink foo={undefined} />
```
✅ 
```
<div />
<Marquee />
<Blink />
```

### jsx_a11y/no-noninteractive-tabindex
This rule checks that non-interactive elements don't have a tabIndex which would make them interactive via keyboard navigation.
❌ 
```
<div tabIndex="0" />
<div role="article" tabIndex="0" />
<article tabIndex="0" />
<article tabIndex={0} />
```
✅ 
```
<div />
<MyButton tabIndex={0} />
<button />
<button tabIndex="0" />
<button tabIndex={0} />
<div />
…
```

### jsx_a11y/no-redundant-roles
Enforce that code does not include a redundant `role` property, in the case that it's identical to the implicit `role` property of the element type.
❌ 
```
<nav role="navigation"></nav>
<button role="button"></button>
<body role="document"></body>
```
✅ 
```
<nav></nav>
<button></button>
<body></body>
```

### jsx_a11y/no-static-element-interactions
Enforce that static HTML elements with event handlers must have appropriate ARIA roles.
❌ 
```
<div onClick={() => {}} />
<span onKeyDown={handleKeyDown} />
```
✅ 
```
<button onClick={() => {}} />
<div onClick={() => {}} role="button" />
<input type="text" onClick={() => {}} />
```

### jsx_a11y/prefer-tag-over-role
Enforce using semantic HTML tags over `role` attribute.
❌ `<div role="button" />`
✅ `<button />`

### jsx_a11y/role-has-required-aria-props
Enforce that elements with ARIA roles must have all required attributes for that role.
❌ `<div role="checkbox" />`
✅ `<div role="checkbox" aria-checked="false" />`

### jsx_a11y/role-supports-aria-props
Enforce that elements with explicit or implicit roles defined contain only `aria-*` properties supported by that `role`.
❌ 
```
<ul role="radiogroup" "aria-labelledby"="foo">
    <li aria-required tabIndex="-1" role="radio" aria-checked="false">Rainbow Trout</li>
    <li aria-required tabIndex="-1" role="radio" aria-checked="false">Brook Trout</li>
    <li aria-required tabIndex="0" role="radio" aria-checked="true">Lake Trout</li>
</ul>
```
✅ 
```
<ul role="radiogroup" aria-required "aria-labelledby"="foo">
    <li tabIndex="-1" role="radio" aria-checked="false">Rainbow Trout</li>
    <li tabIndex="-1" role="radio" aria-checked="false">Brook Trout</li>
    <li tabIndex="0" role="radio" aria-checked="true">Lake Trout</li>
</ul>
```

### jsx_a11y/scope
The scope prop should be used only on `<th>` elements.
❌ `<div scope />`
✅ 
```
<th scope="col" />
<th scope={scope} />
```

### jsx_a11y/tabindex-no-positive
Enforce that positive values for the `tabIndex` attribute are not used in JSX.
❌ `<span tabIndex="1">foo</span>`
✅ 
```
<span tabIndex="0">foo</span>
<span tabIndex="-1">bar</span>
```

### react/button-has-type
Enforce explicit `type` attribute for all the `button` HTML elements.
❌ 
```
<button />
<button type="foo" />
```
✅ 
```
<button type="button" />
<button type="submit" />
```

### react/checked-requires-onchange-or-readonly
This rule enforces `onChange` or `readOnly` attribute for checked property of input elements.
❌ 
```
<input type="checkbox" checked />
<input type="checkbox" checked defaultChecked />
<input type="radio" checked defaultChecked />
React.createElement('input', { checked: false });
React.createElement('input', { type: 'checkbox', checked: true });
React.createElement('input', { type: 'checkbox', checked: true, defaultChecked: true });
```
✅ 
```
<input type="checkbox" checked onChange={() => {}} />
<input type="checkbox" checked readOnly />
<input type="checkbox" checked onChange readOnly />
<input type="checkbox" defaultChecked />
React.createElement('input', { type: 'checkbox', checked: true, onChange() {} });
React.createElement('input', { type: 'checkbox', checked: true, readOnly: true });
…
```

### react/display-name
Enforce that React components have a `displayName` property.
❌ `const MyComponent = () => <div>Hello</div>;`
✅ 
```
const MyComponent = () => <div>Hello</div>;
MyComponent.displayName = "MyComponent";
```

### react/exhaustive-deps
Verifies the list of dependencies for Hooks like `useEffect` and similar.
❌ 
```
function MyComponent(props) {
  useEffect(() => {
    console.log(props.foo);
  }, []);
  // `props` is missing from the dependencies array
  return <div />;
…
```
✅ 
```
function MyComponent(props) {
  useEffect(() => {
    console.log(props.foo);
  }, [props]);
  return <div />;
}
```

### react/forbid-dom-props
This rule prevents passing of props to elements.
❌ 
```
// [1, { "forbid": ["id"] }]
<div id='Joe' />
// [1, { "forbid": ["style"] }]
<div style={{color: 'red'}} />
```
✅ 
```
// [1, { "forbid": ["id"] }]
<Hello id='foo' />
// [1, { "forbid": ["id"] }]
<Hello id={{color: 'red'}} />
```

### react/forbid-elements
Allows you to configure a list of forbidden elements and to specify their desired replacements.
❌ 
```
// ["error", { "forbid": ["button"] }]
<button />;
React.createElement("button");
// ["error", { "forbid": ["Modal"] }]
<Modal />;
React.createElement(Modal);
…
```
✅ 
```
// ["error", { "forbid": ["button"] }]
<Button />
// ["error", { "forbid": [{ "element": "button" }] }]
<Button />
```

### react/forward-ref-uses-ref
Require that components wrapped with `forwardRef` must have a `ref` parameter.
❌ 
```
var React = require("react");
var Component = React.forwardRef((props) => <div />);
```
✅ 
```
var React = require("react");
var Component = React.forwardRef((props, ref) => <div ref={ref} />);
var Component = React.forwardRef((props, ref) => <div />);
function Component(props) {
  return <div />;
}
```

### react/hook-use-state
Ensure destructuring and symmetric naming of useState hook value and setter variables.
❌ 
```
import React from "react";
export default function useColor() {
  // useState call is not destructured into value + setter pair
  const useStateResult = React.useState();
  return useStateResult;
}
```
✅ 
```
import React from "react";
export default function useColor() {
  // useState call is destructured into value + setter pair whose identifiers
  // follow the [thing, setThing] naming convention
  const [color, setColor] = React.useState();
  return [color, setColor];
…
```

### react/iframe-missing-sandbox
Enforce sandbox attribute on iframe elements.
❌ 
```
<iframe />;
<iframe sandbox="invalid-value" />;
<iframe sandbox="allow-same-origin allow-scripts" />;
```
✅ 
```
<iframe sandbox="" />;
<iframe sandbox="allow-origin" />;
```

### react/jsx-boolean-value
Enforce a consistent boolean attribute style in your code.
❌ `const Hello = <Hello personal={true} />;`
✅ 
```
const Hello = <Hello personal />;
const Foo = <Foo isSomething={false} />;
```

### react/jsx-curly-brace-presence
Do not use unnecessary JSX expressions when literals alone are sufficient or enforce JSX expressions on literals in JSX children or attributes.
❌ 
```
<App>Hello world</App>;
<App prop="Hello world">{"Hello world"}</App>;
```

### react/jsx-filename-extension
Enforce consistent use of the `.jsx` file extension.
❌ 
```
// filename: MyComponent.js
function MyComponent() {
  return <div />;
}
```
✅ 
```
// filename: MyComponent.jsx
function MyComponent() {
  return <div />;
}
```

### react/jsx-fragments
Enforce the shorthand or standard form for React Fragments.

### react/jsx-handler-names
Ensures that any component or prop methods used to handle events are correctly prefixed.
❌ 
```
<MyComponent handleChange={this.handleChange} />
<MyComponent onChange={this.componentChanged} />
```
✅ 
```
<MyComponent onChange={this.handleChange} />
<MyComponent onChange={this.props.onFoo} />
```

### react/jsx-key
Enforce `key` prop for elements in array.
❌ 
```
[1, 2, 3].map((x) => <App />);
[1, 2, 3]?.map((x) => <ListItem />);
```
✅ 
```
[1, 2, 3].map((x) => <App key={x} />);
[1, 2, 3]?.map((x) => <ListItem key={x} />);
```

### react/jsx-max-depth
Enforce a maximum depth for nested JSX elements and fragments.
❌ 
```
const Component = () => (
  <div>
    <div>
      <div>
        <span />
      </div>
…
```
✅ 
```
const Component = () => (
  <div>
    <div>
      <span />
    </div>
  </div>
…
```

### react/jsx-no-comment-textnodes
This rule prevents comment strings (e.g.
❌ 
```
const Hello = () => {
  return <div>// empty div</div>;
};
const Hello = () => {
  return <div>/* empty div */</div>;
};
```
✅ 
```
const Hello = () => {
  return <div>{/* empty div */}</div>;
};
```

### react/jsx-no-constructed-context-values
Do not use JSX context provider values from taking values that will cause needless rerenders.
❌ `return <SomeContext.Provider value={{ foo: "bar" }}>...</SomeContext.Provider>;`
✅ 
```
const foo = useMemo(() => ({ foo: "bar" }), []);
return <SomeContext.Provider value={foo}>...</SomeContext.Provider>;
```

### react/jsx-no-duplicate-props
This rule prevents duplicate props in JSX elements.
❌ 
```
<App a a />;
<App foo={2} bar baz foo={3} />;
```
✅ 
```
<App a />;
<App bar baz foo={3} />;
```

### react/jsx-no-script-url
Do not use usage of `javascript:` URLs.
❌ `<a href="javascript:void(0)">Test</a>`
✅ `<Foo test="javascript:void(0)" />`

### react/jsx-no-target-blank
This rule aims to prevent user generated link hrefs and form actions from creating security vulnerabilities by requiring `rel='noreferrer'` for external link hrefs and form actions, and optionally any dynamically generated link hrefs and f…
❌ 
```
var Hello = <a target="_blank" href="https://example.com/"></a>;
var Hello = <a target="_blank" href={dynamicLink}></a>;
```
✅ 
```
/// correct
var Hello = <p target="_blank"></p>;
var Hello = <a target="_blank" rel="noreferrer" href="https://example.com"></a>;
var Hello = <a target="_blank" rel="noopener noreferrer" href="https://example.com"></a>;
var Hello = <a target="_blank" href="relative/path/in/the/host"></a>;
var Hello = <a target="_blank" href="/absolute/path/in/the/host"></a>;
…
```

### react/jsx-no-undef
Do not use undeclared variables in JSX.
❌ 
```
const A = () => <App />;
const C = <B />;
```

### react/jsx-no-useless-fragment
Do not use unnecessary fragments.
❌ 
```
<>foo</>
<div><>foo</></div>
```
✅ 
```
<>foo <div></div></>
<div>foo</div>
```

### react/jsx-pascal-case
Enforce PascalCase for user-defined JSX components.
❌ 
```
<Test_component />
<TEST_COMPONENT />
```
✅ 
```
<div />
<TestComponent />
<TestComponent>
    <div />
</TestComponent>
<CSSTransitionGroup />
```

### react/jsx-props-no-spread-multi
Enforce that any unique expression is only spread once.
❌ `<App {...props} myAttr="1" {...props} />`
✅ 
```
<App myAttr="1" {...props} />
<App {...props} myAttr="1" />
```

### react/jsx-props-no-spreading
Do not use JSX prop spreading.
❌ 
```
<App {...props} />
<MyCustomComponent {...props} some_other_prop={some_other_prop} />
<img {...props} />
```
✅ 
```
const {src, alt} = props;
const {one_prop, two_prop} = otherProps;
<MyCustomComponent one_prop={one_prop} two_prop={two_prop} />
<img src={src} alt={alt} />
```

### react/no-array-index-key
Warn if an element uses an Array index in its key.
❌ `things.map((thing, index) => <Hello key={index} />);`
✅ `things.map((thing, index) => <Hello key={thing.id} />);`

### react/no-children-prop
Ensure children are not passed using a prop.
❌ 
```
<div children='Children' />
<MyComponent children={<AnotherComponent />} />
<MyComponent children={['Child 1', 'Child 2']} />
React.createElement("div", { children: 'Children' })
```
✅ 
```
<div>Children</div>
<MyComponent>Children</MyComponent>
<MyComponent>
  <span>Child 1</span>
  <span>Child 2</span>
</MyComponent>
…
```

### react/no-clone-element
Prevent the usage of `React.cloneElement`, which is considered an anti-pattern in React.
❌ 
```
import { cloneElement } from "react";
function List({ children }) {
  const [selectedIndex, setSelectedIndex] = useState(0);
  return (
    <div className="List">
      {Children.map(children, (child, index) =>
…
```
✅ 
```
// Using a map with a `renderItem` function prop instead.
function List({ items, renderItem }) {
  const [selectedIndex, setSelectedIndex] = useState(0);
  return (
    <div className="List">
      {items.map((item, index) => {
…
```

### react/no-danger
This rule prevents the use of `dangerouslySetInnerHTML` prop.
❌ 
```
import React from "react";
const Hello = <div dangerouslySetInnerHTML={{ __html: "Hello World" }}></div>;
```
✅ 
```
import React from "react";
const Hello = <div>Hello World</div>;
```

### react/no-danger-with-children
Do not use when a DOM element is using both `children` and `dangerouslySetInnerHTML` properties.
❌ 
```
<div dangerouslySetInnerHTML={{ __html: "HTML" }}>Children</div>;
React.createElement("div", { dangerouslySetInnerHTML: { __html: "HTML" } }, "Children");
```
✅ 
```
<div>Children</div>
<div dangerouslySetInnerHTML={{ __html: "HTML" }} />
```

### react/no-did-mount-set-state
Do not use using `setState` in the `componentDidMount` lifecycle method.
❌ 
```
var Hello = createReactClass({
  componentDidMount: function () {
    this.setState({
      name: this.props.name.toUpperCase(),
    });
  },
…
```
✅ 
```
var Hello = createReactClass({
  componentDidMount: function () {
    this.onMount(function callback(newName) {
      this.setState({
        name: newName,
      });
…
```

### react/no-direct-mutation-state
This rule forbids the direct mutation of `this.state` in React components.
❌ 
```
var Hello = createReactClass({
  componentDidMount: function () {
    this.state.name = this.props.name.toUpperCase();
  },
  render: function () {
    return <div>Hello {this.state.name}</div>;
…
```
✅ 
```
var Hello = createReactClass({
  componentDidMount: function() {
    this.setState({
      name: this.props.name.toUpperCase();
    });
  },
…
```

### react/no-find-dom-node
This rule disallows the use of `findDOMNode`, which was deprecated in 2018 and removed in React 19.
❌ 
```
class MyComponent extends Component {
  componentDidMount() {
    findDOMNode(this).scrollIntoView();
  }
  render() {
    return <div />;
…
```

### react/no-is-mounted
This rule prevents using `isMounted` in class components.
❌ 
```
class Hello extends React.Component {
  someMethod() {
    if (!this.isMounted()) {
      return;
    }
  }
…
```

### react/no-multi-comp
Prevent multiple React components from being defined in the same file.
❌ 
```
function Foo({ name }) {
  return <div>Hello {name}</div>;
}
function Bar({ name }) {
  return <div>Hello again {name}</div>;
}
```
✅ 
```
function Foo({ name }) {
  return <div>Hello {name}</div>;
}
```

### react/no-namespace
Enforce that namespaces are not used in React elements.
❌ 
```
<ns:TestComponent />
<Ns:TestComponent />
```
✅ 
```
<TestComponent />
<testComponent />
```

### react/no-react-children
Do not use the usage of `React.Children`, as it is considered a bad practice.
❌ 
```
import { Children } from "react";
Children.toArray(children);
Children.map(children, (child) => <div>{child}</div>);
Children.only(children);
Children.count(children);
Children.forEach(children, (child, index) => {});
```
✅ 
```
function Card({ children }) {
  return <div className="card">{children}</div>;
}
```

### react/no-redundant-should-component-update
Do not use usage of `shouldComponentUpdate` when extending `React.PureComponent`.
❌ 
```
class Foo extends React.PureComponent {
  shouldComponentUpdate() {
    // do check
  }
  render() {
    return <div>Radical!</div>;
…
```
✅ 
```
class Foo extends React.Component {
  shouldComponentUpdate() {
    // do check
  }
  render() {
    return <div>Radical!</div>;
…
```

### react/no-render-return-value
This rule will warn you if you try to use the `ReactDOM.render()` return value.
❌ 
```
var inst = ReactDOM.render(<App />, document.body);
function render() {
  return ReactDOM.render(<App />, document.body);
}
```
✅ `ReactDOM.render(<App />, document.body);`

### react/no-set-state
Do not use the usage of `this.setState` in React components.
❌ 
```
var Hello = createReactClass({
  getInitialState: function () {
    return {
      name: this.props.name,
    };
  },
…
```

### react/no-string-refs
This rule prevents using the deprecated behavior of string literals in ref attributes.
❌ 
```
var Hello = createReactClass({
  render: function () {
    return <div ref="hello">Hello, world.</div>;
  },
});
var Hello = createReactClass({
…
```
✅ 
```
var Hello = createReactClass({
  componentDidMount: function () {
    var component = this.hello;
    // ...do something with component
  },
  render() {
…
```

### react/no-this-in-sfc
Prevent using `this` in stateless functional components.
❌ 
```
function Foo(props) {
  return <div>{this.props.bar}</div>;
}
function Foo(props) {
  const { bar } = this.props;
  return <div>{bar}</div>;
…
```
✅ 
```
function Foo(props) {
  return <div>{props.bar}</div>;
}
function Foo({ bar }) {
  return <div>{bar}</div>;
}
…
```

### react/no-unescaped-entities
This rule prevents characters that you may have meant as JSX escape characters from being accidentally injected as a text node in JSX statements.

### react/no-unknown-property
Do not use usage of unknown DOM properties.
❌ 
```
// Unknown properties
const Hello = <div class="hello">Hello World</div>;
const Alphabet = <div abc="something">Alphabet</div>;
// Invalid aria-* attribute
const IconButton = <div aria-foo="bar" />;
```
✅ 
```
// Unknown properties
const Hello = <div className="hello">Hello World</div>;
const Alphabet = <div>Alphabet</div>;
// Invalid aria-* attribute
const IconButton = <div aria-label="bar" />;
```

### react/no-unsafe
This rule identifies and restricts the use of unsafe React lifecycle methods.
❌ 
```
// By default, UNSAFE_ prefixed methods are flagged
class Foo extends React.Component {
  UNSAFE_componentWillMount() {}
  UNSAFE_componentWillReceiveProps() {}
  UNSAFE_componentWillUpdate() {}
}
…
```
✅ 
```
class Foo extends React.Component {
  componentDidMount() {}
  componentDidUpdate() {}
  render() {}
}
```

### react/no-will-update-set-state
Do not use using `setState` in the `componentWillUpdate` lifecycle method.
❌ 
```
var Hello = createReactClass({
  componentWillUpdate: function () {
    this.setState({
      name: this.props.name.toUpperCase(),
    });
  },
…
```
✅ 
```
var Hello = createReactClass({
  componentWillUpdate: function () {
    this.props.prepareHandler();
  },
  render: function () {
    return <div>Hello {this.state.name}</div>;
…
```

### react/only-export-components
Ensures that modules only **export React components (and related HMR-safe items)** so that Fast Refresh (a.k.a.
❌ 
```
// 1) Mixing util exports with components in unsupported ways
export const foo = () => {}; // util, not a component
export const Bar = () => <></>; // component
```
✅ 
```
// Named or default component exports are fine
export default function Foo() {
  return null;
}
```

### react/prefer-es6-class
React offers you two ways to create traditional components: using the `create-react-class` package or the newer ES2015 class system.
❌ 
```
var Hello = createReactClass({
  render: function () {
    return <div>Hello {this.props.name}</div>;
  },
});
```

### react/prefer-function-component
Enforce that React components are written as function components instead of class components.
❌ 
```
class Foo extends React.Component {
  render() {
    return <div>{this.props.foo}</div>;
  }
}
class Bar extends React.PureComponent {
…
```
✅ 
```
const Foo = function (props) {
  return <div>{props.foo}</div>;
};
const Bar = ({ bar }) => <div>{bar}</div>;
```

### react/react-in-jsx-scope
Enforce that React is imported and in-scope when using JSX syntax.
❌ `const a = <a />;`
✅ 
```
import React from "react";
const a = <a />;
```

### react/require-render-return
Enforce ES5 or ES2015 class for returning value in the `render` function.
❌ 
```
var Hello = createReactClass({
  render() {
    <div>Hello</div>;
  },
});
class Hello extends React.Component {
…
```
✅ 
```
var Hello = createReactClass({
  render() {
    return <div>Hello</div>;
  },
});
class Hello extends React.Component {
…
```

### react/rules-of-hooks
Enforce the Rules of Hooks, ensuring that React Hooks are only called in valid contexts and in the correct order.
❌ 
```
// Don't call Hooks inside loops, conditions, or nested functions
function BadComponent() {
  if (condition) {
    const [state, setState] = useState(); // ❌ Hook in condition
  }
  for (let i = 0; i < 10; i++) {
…
```
✅ 
```
// ✅ Call Hooks at the top level of a React component
function GoodComponent() {
  const [state, setState] = useState();
  useEffect(() => {
    // Effect logic here
  });
…
```

### react/self-closing-comp
Avoid components without children which can be self-closed to avoid unnecessary extra closing tags.
❌ 
```
const elem = <Component linter="oxlint"></Component>;
const dom_elem = <div id="oxlint"></div>;
const welem = <div id="oxlint"></div>;
```
✅ 
```
const elem = <Component linter="oxlint" />;
const welem = <Component linter="oxlint"> </Component>;
const dom_elem = <div id="oxlint" />;
```

### react/state-in-constructor
Enforce the state initialization style to be either in a constructor or with a class property.
❌ 
```
class Foo extends React.Component {
  state = { bar: 0 };
  render() {
    return <div>Foo</div>;
  }
}
```
✅ 
```
class Foo extends React.Component {
  constructor(props) {
    super(props);
    this.state = { bar: 0 };
  }
  render() {
…
```

### react/style-prop-object
Require that the value of the prop `style` be an object or a variable that is an object.
❌ 
```
<div style="color: 'red'" />
<div style={true} />
<Hello style={true} />
const styles = true;
<div style={styles} />
React.createElement("div", { style: "color: 'red'" });
…
```
✅ 
```
<div style={{ color: "red" }} />
<Hello style={{ color: "red" }} />
const styles = { color: "red" };
<div style={styles} />
React.createElement("div", { style: { color: 'red' }});
React.createElement("Hello", { style: { color: 'red' }});
…
```

### react/void-dom-elements-no-children
Do not use void DOM elements (e.g.
❌ 
```
<br>Children</br>
<br children='Children' />
<br dangerouslySetInnerHTML={{ __html: 'HTML' }} />
React.createElement('br', undefined, 'Children')
React.createElement('br', { children: 'Children' })
React.createElement('br', { dangerouslySetInnerHTML: { __html: 'HTML' } })
```
✅ 
```
<div>Children</div>
<div children='Children' />
<div dangerouslySetInnerHTML={{ __html: 'HTML' }} />
React.createElement('div', undefined, 'Children')
React.createElement('div', { children: 'Children' })
React.createElement('div', { dangerouslySetInnerHTML: { __html: 'HTML' } })
```

### react_perf/jsx-no-jsx-as-prop
Prevent JSX elements that are local to the current method from being used as values of JSX props.
❌ 
```
<Item jsx={<SubItem />} />
<Item jsx={this.props.jsx || <SubItem />} />
<Item jsx={this.props.jsx ? this.props.jsx : <SubItem />} />
```
✅ `<Item callback={this.props.jsx} />`

### react_perf/jsx-no-new-array-as-prop
Prevent Arrays that are local to the current method from being used as values of JSX props.
❌ 
```
<Item list={[]} />
<Item list={new Array()} />
<Item list={Array()} />
<Item list={this.props.list || []} />
<Item list={this.props.list ? this.props.list : []} />
```
✅ `<Item list={this.props.list} />`

### react_perf/jsx-no-new-function-as-prop
Prevent Functions that are local to the current method from being used as values of JSX props.
❌ 
```
<Item callback={new Function(...)} />
<Item callback={this.props.callback || function() {}} />
```
✅ `<Item callback={this.props.callback} />`

### react_perf/jsx-no-new-object-as-prop
Prevent Objects that are local to the current method from being used as values of JSX props.
❌ 
```
<Item config={{}} />
<Item config={new Object()} />
<Item config={Object()} />
<Item config={this.props.config || {}} />
<Item config={this.props.config ? this.props.config : {}} />
<div style={{display: 'none'}} />
```
✅ `<Item config={staticConfig} />`
