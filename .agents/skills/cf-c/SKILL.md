---
name: cf-c
description: CodeForge C skill for diagnosing, repairing, and translating C code with strict memory safety and bounds checking.
---

# CodeForge Skill: C

- **SKILL:** C
- **TRIGGERS:** `.c`, `.h`
- **TOOLCHAIN:** `gcc -std=c17 -Wall -Wextra -Werror -fsanitize=address,undefined` (or `clang`)
- **STYLE_GUIDE:** K&R / Linux Kernel style with consistent 4-space indentation
- **LINT/FORMAT:** `clang-tidy`, `clang-format`
- **COMMON_FAULTS:**
  - `C-001`: Missing header `#include` statements
  - `C-002`: Buffer overflows and out-of-bounds array access
  - `C-003`: Memory leaks (unpaired `malloc`/`calloc` without `free`)
  - `C-004`: Use of uninitialized variables or pointer references
  - `C-005`: Format-string specifier mismatches in `printf`/`scanf`
  - `C-006`: Missing `return` value in non-void function
  - `C-007`: Use of unsafe functions (`gets`, `strcpy` instead of bounded alternatives)
- **IDIOM_RULES:**
  - Explicit memory ownership documentation and lifecycle management
  - Avoid variable length arrays (VLAs) in portable code
  - Strict bounds-checked iterations and array indexing
  - Use `size_t` for indexing and memory sizes; `int32_t`/`int64_t` from `<stdint.h>`
- **EXECUTION_SANDBOX:**
  - Compile with AddressSanitizer (ASan) and UndefinedBehaviorSanitizer (UBSan). Terminate execution on sanitizer faults and report as defects.
