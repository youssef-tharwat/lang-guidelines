# Python sources: provenance

`build/compile.py python` reads the files below. Refresh a file, record the new
provenance here, then map any new upstream sections in `build/python/manifest.toml`.

| File | Origin | Retrieved | sha256 |
| --- | --- | --- | --- |
| `google-python-style-guide.md` | [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html), page-to-Markdown extraction; carried over from `python-guidelines/design.md` | 2026-04-24 (commit `37414d1`, last edit `6a4706e`) | `2b07390dda018991375a5b25af70ffdd80b86cfbedea79e258615e8a98f1622d` |
| `python-patterns.md` | [python-patterns.guide](https://python-patterns.guide/) by Brandon Rhodes, extracted page by page; each page starts with a `<!-- source: url -->` marker; carried over from `python-guidelines/patterns.md` | 2026-04-24 (commit `37414d1`, last edit `f65ebca`) | `206c9050fb71666e36808ca0be47ba44951269bf8521db2bdaf4edf1bc4e4bc4` |
| `ruff-rules.md` | Tier 1 and Tier 2 digest of the [Ruff rule documentation](https://docs.astral.sh/ruff/rules/); carried over from `python-guidelines/guidelines.txt` | 2026-04-24 (commit `1a013d9`) | `9f51d059350bea589e0b7905d722949df104568473e34071f1df701de3a2f17a` |
| `ruff-inventory.json` | `ruff rule --all --output-format json` from Ruff 0.17.1 (`uvx ruff@0.17.1`), reduced to each rule's code, name and status | 2026-10-22 | `47eb61e25733dce4dd9c8f18dda2c9e0a7aed621b5577f6a55046f10ec3b5958` |

The vendored files in `python-guidelines/` (`lint/<rule>/index.md`, `style.md`,
`frameworks/*.md`) come from the same Ruff documentation digest (commit `1a013d9`).
The compiler checks that every Tier 1–2 rule in `ruff-rules.md` has its `lint/` doc.

Known gaps the build handles:

- **`ruff-rules.md` predates Ruff 0.17.1.** Eleven of its rules no longer exist in Ruff.
  `ruff.toml` selects only rules the pinned inventory can select, and names the omitted
  ones in its header.
- **python-patterns.guide pages carry no title heading.** The parser names each page
  from its URL path.
