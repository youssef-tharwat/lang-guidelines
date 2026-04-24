# Nextjs Rules (TypeScript & JavaScript)

21 rules that apply when the project uses **nextjs**.
Load this file only if the project's manifest imports or depends on
`nextjs`.

---

### nextjs/google-font-display
Enforce font-display behavior with Google Fonts.
❌ 
```
import Head from "next/head";
export default Test = () => {
  return (
    <Head>
      <link href="https://fonts.googleapis.com/css2?family=Krona+One" rel="stylesheet" />
    </Head>
…
```
✅ 
```
import Head from "next/head";
export default Test = () => {
  return (
    <Head>
      <link
        href="https://fonts.googleapis.com/css2?family=Krona+One&display=optional"
…
```

### nextjs/google-font-preconnect
Enforce the presence of `rel="preconnect"` when using Google Fonts via `<link>` tags.
❌ 
```
<link href="https://fonts.gstatic.com" />
<link rel="preload" href="https://fonts.gstatic.com" />
```
✅ `<link rel="preconnect" href="https://fonts.gstatic.com" />`

### nextjs/inline-script-id
Enforce that all `next/script` components with inline content or `dangerouslySetInnerHTML` must have an `id` prop.
❌ 
```
import Script from 'next/script';
export default function Page() {
  return (
    <Script>
      {`console.log('Hello world');`}
    </Script>
…
```
✅ 
```
import Script from 'next/script';
export default function Page() {
  return (
    <Script id="my-script">
      {`console.log('Hello world');`}
    </Script>
…
```

### nextjs/next-script-for-ga
Enforce the use of the `next/script` component when implementing Google Analytics in Next.js applications, instead of using regular `<script>` tags.
❌ 
```
// Using regular script tag with GA source
<script src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
// Using inline script for GA initialization
<script dangerouslySetInnerHTML={{
  __html: `
    window.dataLayer = window.dataLayer || [];
…
```
✅ 
```
import Script from 'next/script'
// Using next/script for GA source
<Script
  src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"
  strategy="lazyOnload"
/>
…
```

### nextjs/no-assign-module-variable
Prevent the assignment or declaration of variables named `module` in Next.js applications.
❌ 
```
// Declaring module variable
let module = {};
// Using module in variable declaration
const module = {
  exports: {},
};
…
```
✅ 
```
// Use a different variable name
let myModule = {};
// Use a more descriptive name
const customModule = {
  exports: {},
};
…
```

### nextjs/no-async-client-component
Prevent the use of async functions for client components in Next.js applications.
❌ 
```
"use client"
// Async component with default export
export default async function MyComponent() {
  return <></>
}
// Async component with named export
…
```
✅ 
```
"use client"
// Regular synchronous component
export default function MyComponent() {
  return <></>
}
// Handling async operations in effects
…
```

### nextjs/no-before-interactive-script-outside-document
Prevent the usage of `next/script`'s `beforeInteractive` strategy outside of `pages/_document.js`.
❌ 
```
// pages/index.js
import Script from "next/script";
export default function HomePage() {
  return (
    <div>
      <Script
…
```
✅ 
```
// pages/_document.js
import Document, { Html, Head, Main, NextScript } from "next/document";
import Script from "next/script";
class MyDocument extends Document {
  render() {
    return (
…
```

### nextjs/no-css-tags
Prevent manual inclusion of stylesheets using `<link>` tags in Next.js applications.
❌ 
```
// Manually including local CSS file
<link href="/_next/static/css/styles.css" rel="stylesheet" />
// In pages/_document.js
<Head>
  <link href="css/my-styles.css" rel="stylesheet" />
</Head>
```
✅ 
```
// Importing CSS file directly
import '../styles/global.css'
// Using CSS Modules
import styles from './Button.module.css'
// Using external stylesheets (allowed)
<link
…
```

### nextjs/no-document-import-in-page
Prevent importing `next/document` outside of `pages/_document.js`.
❌ 
```
// `components/MyDocument.jsx`
import Document from "next/document";
class MyDocument extends Document {
  //...
}
export default MyDocument;
```
✅ 
```
// `pages/_document.jsx`
import Document from "next/document";
class MyDocument extends Document {
  //...
}
export default MyDocument;
```

### nextjs/no-duplicate-head
Prevent duplicate usage of `<Head>` in `pages/_document.js`.
❌ 
```
import Document, { Html, Head, Main, NextScript } from "next/document";
class MyDocument extends Document {
  static async getInitialProps(ctx) {}
  render() {
    return (
      <Html>
…
```
✅ 
```
import Document, { Html, Head, Main, NextScript } from "next/document";
class MyDocument extends Document {
  static async getInitialProps(ctx) {}
  render() {
    return (
      <Html>
…
```

### nextjs/no-head-element
Prevent the usage of the native `<head>` element inside a Next.js application.
❌ 
```
function Index() {
  return (
    <>
      <head>
        <title>My page title</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
…
```
✅ 
```
import Head from "next/head";
function Index() {
  return (
    <>
      <Head>
        <title>My page title</title>
…
```

### nextjs/no-head-import-in-document
Prevent the usage of `next/head` inside a Next.js document.
❌ 
```
import Document, { Html, Main, NextScript } from "next/document";
import Head from "next/head";
class MyDocument extends Document {
  static async getInitialProps(ctx) {
    //...
  }
…
```
✅ 
```
import Document, { Html, Head, Main, NextScript } from "next/document";
class MyDocument extends Document {
  static async getInitialProps(ctx) {
    //...
  }
  render() {
…
```

### nextjs/no-html-link-for-pages
Prevent the usage of `<a>` elements to navigate between Next.js pages.
❌ 
```
function HomePage() {
  return (
    <div>
      <a href="/about">About Us</a>
      <a href="/contact">Contact</a>
    </div>
…
```
✅ 
```
import Link from "next/link";
function HomePage() {
  return (
    <div>
      <Link href="/about">About Us</Link>
      <Link href="/contact">Contact</Link>
…
```

### nextjs/no-img-element
Prevent the usage of `<img>` element due to slower LCP and higher bandwidth.
❌ 
```
export function MyComponent() {
  return (
    <div>
      <img src="/test.png" alt="Test picture" />
    </div>
  );
…
```
✅ 
```
import Image from "next/image";
import testImage from "./test.png";
export function MyComponent() {
  return (
    <div>
      <Image src={testImage} alt="Test picture" />
…
```

### nextjs/no-page-custom-font
Prevent page-only custom fonts.
❌ 
```
// pages/index.jsx
import Head from "next/head";
function IndexPage() {
  return (
    <Head>
      <link
…
```
✅ 
```
// pages/_document.jsx
import NextDocument, { Html, Head } from "next/document";
class Document extends NextDocument {
  render() {
    return (
      <Html>
…
```

### nextjs/no-script-component-in-head
Prevent usage of `next/script` in `next/head` component.
❌ 
```
import Script from "next/script";
import Head from "next/head";
export default function Index() {
  return (
    <Head>
      <title>Next.js</title>
…
```
✅ 
```
import Script from "next/script";
import Head from "next/head";
export default function Index() {
  return (
    <>
      <Head>
…
```

### nextjs/no-styled-jsx-in-document
Prevent usage of styled-jsx in `pages/_document.js`.
❌ 
```
// pages/_document.js
import Document, { Html, Head, Main, NextScript } from "next/document";
class MyDocument extends Document {
  render() {
    return (
      <Html>
…
```
✅ 
```
// pages/_document.js
import Document, { Html, Head, Main, NextScript } from "next/document";
class MyDocument extends Document {
  render() {
    return (
      <Html>
…
```

### nextjs/no-sync-scripts
This rule prevents the use of synchronous `<script>` tags in Next.js applications.
❌ 
```
// Synchronous script without async/defer
<script src="https://example.com/script.js"></script>
// Dynamic src without async/defer
<script src={dynamicSrc}></script>
```
✅ 
```
// Script with async attribute
<script src="https://example.com/script.js" async></script>
// Script with defer attribute
<script src="https://example.com/script.js" defer></script>
// Script with spread props (allowed as it might include async/defer)
<script {...props}></script>
```

### nextjs/no-title-in-document-head
Prevent usage of `<title>` with `Head` component from `next/document`.
❌ 
```
import { Head } from "next/document";
export function Home() {
  return (
    <div>
      <Head>
        <title>My page title</title>
…
```
✅ 
```
import Head from "next/head";
export function Home() {
  return (
    <div>
      <Head>
        <title>My page title</title>
…
```

### nextjs/no-typos
Avoid common typos in Next.js data fetching function names.
❌ 
```
export default function Page() {
  return <div></div>;
}
export async function getServurSideProps() {}
```
✅ 
```
export default function Page() {
  return <div></div>;
}
export async function getServerSideProps() {}
```

### nextjs/no-unwanted-polyfillio
Prevent use of unsafe polyfill.io domains and duplicate polyfills.
❌ 
```
// Security risk - compromised domain
<script src='https://cdn.polyfill.io/v2/polyfill.min.js'></script>
<script src='https://polyfill.io/v3/polyfill.min.js'></script>
// Duplicate polyfills
<script src='https://cdnjs.cloudflare.com/polyfill/v3/polyfill.min.js?features=Array.prototype.copyWithin'></script>
<script src='https://cdnjs.cloudflare.com/polyfill/v3/polyfill.min.js?features=WeakSet%2CPromise'></script>
```
