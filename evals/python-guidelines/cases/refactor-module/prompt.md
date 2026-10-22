---
description: Refactor a module full of common Python mistakes.
tags: [functions, features, strings]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

Refactor this Python module into idiomatic, well-designed Python. Keep its behavior.

```python
import logging, os
from utils import *

log = logging.getLogger(__name__)
CACHE = {}

class Report:
    def __init__(self, rows):
        self._rows = rows

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value

    @staticmethod
    def header(title):
        return "== " + title + " =="

def add_row(row, rows=[]):
    rows.append(row)
    return rows

def render(report, title):
    out = ""
    out += Report.header(title) + "\n"
    if len(report.rows) == 0:
        log.info(f"empty report {title}")
    for key in CACHE.keys():
        out += key + ": " + str(CACHE[key]) + "\n"
    for row in report.rows:
        out = out + str(row) + "\n"
    return out

def save(report, path):
    assert path, "path required"
    f = open(path, "w")
    try:
        f.write(render(report, os.path.basename(path)))
    except:
        pass
    f.close()
```

Write the complete refactored module to `report.py` in the current directory, then reply with a short list of what you changed.
