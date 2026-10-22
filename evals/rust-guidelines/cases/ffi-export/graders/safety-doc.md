---
type: regex
target: {source: file, path: ffi.rs}
pattern: '# Safety'
match: contains
---

Rule `sound-only`: the unsafe export documents caller obligations under `# Safety`.
