---
type: regex
target: {source: file, path: ffi.rs}
pattern: 'CStr::from_ptr'
match: contains
---

Rule `ffi-boundary`: the incoming string is borrowed as `CStr`.
