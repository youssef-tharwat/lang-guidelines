# TypeScript sources: provenance

`build/compile.py typescript` reads the files below. Refresh a file, record the new
provenance here, then map any new upstream sections in `build/typescript/manifest.toml`.

| File | Origin | Retrieved | sha256 |
| --- | --- | --- | --- |
| `google-typescript-style-guide.md` | [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) HTML (sha256 `3ab5ef4a659559bafeced5ad971f0805b5b8bb755decc6d0c195bd6a4a1c57a3`), converted by `build/fetch/google_styleguide.py` with no hand edits | 2026-10-22 | `8bd9991206c376d2f75f12bfbb21858dedc1977b2c47d9b30810aaa374892b65` |
| `typescript-patterns.md` | [Systemic TypeScript](https://valand.dev/systemic-ts) and [refactoring.guru TypeScript examples](https://refactoring.guru/design-patterns/typescript), extracted page by page; each page starts with a `<!-- source: url -->` marker; carried over from `typescript-guidelines/patterns.md` | 2026-04-24 (commit `24273ab`, last edit `f65ebca`) | `2ab1cdda5b957dd57ea3231d83b402931d644cd37d202259c9510ee2bc6cd2dc` |
| `oxlint-rules.md` | Tier 1 and Tier 2 digest of the [Oxlint rule documentation](https://oxc.rs/docs/guide/usage/linter/rules); carried over from `typescript-guidelines/guidelines.txt` | 2026-04-24 (commit `1a013d9`) | `0e0d61c2c2194aa658d3db4b0f344057fad01f5888521b3ea7a348c71209ef29` |
| `oxlint-inventory.json` | `oxlint --rules --format json` from Oxlint 1.89.0 (`bunx oxlint@1.89.0`), reduced to each rule's plugin, name and type-awareness | 2026-10-22 | `db313b09d0866fab33c15749da5db3f47662443139f9b34d9ee3757d0d229521` |

The vendored files in `typescript-guidelines/` (`lint/<plugin>/<rule>/index.md`,
`style.md`, `frameworks/*.md`) come from the same Oxlint documentation digest (commit
`1a013d9`). The compiler checks that every Tier 1–2 rule in `oxlint-rules.md` has its
`lint/` doc.

The Google guide replaced an April 2026 page extraction that had flattened every code
example onto one line and merged good and bad examples. The converter keeps the page's
own good/bad markers (`✅ Good:` / `❌ Bad:`) and section anchors.

Known gaps the build handles:

- **Systemic TypeScript pages carry no title heading.** The parser names each page from
  its URL slug.
- **refactoring.guru pages:** their example code arrived unfenced. The parser re-fences
  it under each `**file.ts**` heading.
