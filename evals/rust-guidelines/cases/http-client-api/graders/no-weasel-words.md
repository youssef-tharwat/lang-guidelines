---
type: regex
target: {source: file, path: client.rs}
pattern: '(struct|enum|trait) \w*(Manager|Service|Factory)\b'
match: not_contains
---

Rule `no-weasel-words`: no `Manager`/`Service`/`Factory` type names.
