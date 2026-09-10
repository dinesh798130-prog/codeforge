---
name: cf-python
description: CodeForge Python skill for diagnosing, repairing, and translating Python code adhering to PEP-8 and PEP-484.
---

# CodeForge Skill: Python

- **SKILL:** Python
- **TRIGGERS:** `.py`, `.pyi`, `#!/usr/bin/env python`, `python3`
- **TOOLCHAIN:** CPython 3.11+, `python -X dev`
- **STYLE_GUIDE:** PEP 8 / PEP 257 (docstrings) / PEP 484 (type hints)
- **LINT/FORMAT:** `ruff`, `black`, `mypy --strict`
- **COMMON_FAULTS:**
  - `PY-001`: Indentation errors, tab/space mixing
  - `PY-002`: Mutable default arguments (`def f(x=[])`)
  - `PY-003`: Bare `except:` clauses swallowing system signals
  - `PY-004`: Off-by-one errors in `range()` or slice bounds
  - `PY-005`: Python 2 legacy syntax (`print x`, integer division `/`)
  - `PY-006`: Missing resource management (`with` context managers)
  - `PY-007`: Shadowing built-in names (`id`, `list`, `dict`, `str`)
- **IDIOM_RULES:**
  - List/dict/set comprehensions over manual loops where readable
  - Context managers (`with`) for file and network resource lifecycles
  - f-strings over `%` formatting or `.format()`
  - Explicit type annotations on function signatures
- **EXECUTION_SANDBOX:**
  - Isolated subprocess with timeout cap (10s), network access restricted unless required.
