# short-names

Keep identifiers short: at most two short words (`AppConfig`), no module or crate name baked in (`foo::Id`, not `foo::FooId`), and widely known abbreviations welcome (`CallbackFn`); never abbreviations outsiders can't decode or words with letters dropped. Microsoft's preference for short forms overrides Google's general advice against abbreviations.

**Why:** Paths already carry context; names shouldn't repeat it.

**Sources:** M-SHORT-NAMES, G:avoid-abbreviations

---

## Names of items are short (M-SHORT-NAMES)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

The Rust convention that item identifiers are short should be followed:

- identifiers should not compound more than 2 short words (`AppConfig` over `GlobalApplicationConfig`),
- module or crate information shouldn't be baked into prefixes (`foo::Id` over `foo::FooId`), in particular when the direct 'super' item is sufficiently descriptive - in these cases users are expected to disambiguate items locally via qualifiers where needed (`fn convert(foo::Id) -> bar::Id`).
- abbreviations are preferred (`CallbackFn` over `CallbackFunction`),

Any of these rules can be broken where it makes local sense, but on a per-crate bases these exceptions should be _exceptional_ and well motivated.


## Avoid abbreviations (G:avoid-abbreviations)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#avoid-abbreviations), CC BY 3.0.

Don’t use abbreviations (especially acronyms and initialisms) that someone outside your project is unlikely to know. Don’t abbreviate by deleting letters within a word.

See also the [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html#General_Naming_Rules).

Exceptions:

*   Common abbreviations found in Wikipedia.

*   Abbreviations that are unlikely to be confusing to people outside of your project, for example `IpAddr`. You and your reviewer should make this determination. In general, the preference should still be not to abbreviate.
