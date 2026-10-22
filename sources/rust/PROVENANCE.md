# Rust sources: provenance

`build/compile.py rust` reads the three files below. Refresh a file, record the new
provenance here, then map any new upstream sections in `build/rust/manifest.toml`.

| File | Origin | Retrieved | sha256 |
| --- | --- | --- | --- |
| `microsoft-pragmatic-rust-guidelines.md` | `src/agents/all.txt` of [microsoft/rust-guidelines](https://github.com/microsoft/rust-guidelines) at commit `19723b30aadf1854fef6a56c2da2395dc03255c1` (a Git LFS object; its oid equals the sha256), byte for byte | 2026-10-22 | `5cf536f19c53ecd003897c2065c044b1abaf17612e0838f69a7fe0ce547ad650` |
| `google-rust-style-guide.md` | [Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html), page published 2026-10-21, converted from HTML to Markdown; the file header lists the omitted Chromium/Fuchsia/Android-only rules and the corrected upstream typos | 2026-10-22 | `8bcf2ddae1cf0c5392baa9f93e4d31ff068932f1792233131a83f85ed54fb0f4` |
| `rust-patterns.md` | [rust-unofficial/patterns](https://rust-unofficial.github.io/patterns/) and [refactoring.guru Rust examples](https://refactoring.guru/design-patterns/rust), extracted page by page; each page starts with a `<!-- source: url -->` marker | 2026-04-24 (commit `58deb6e`) | `f6cdd1d0656ebd48bf9e46a8d45cba5fa341d39a13086c6869b9112bfb2b6424` |

Known upstream defects the parser handles:

- **`M-FAST-HASHER` (Microsoft, commit `19723b3`):** its code example is never closed. The
  parser starts a new section at every guideline heading and closes a fence left open at
  a section's end. It also fails the build if any guideline the file declares goes
  unparsed.
- **refactoring.guru pages:** their example code arrived unfenced. The parser re-fences it
  under each `**file.rs**` heading.
