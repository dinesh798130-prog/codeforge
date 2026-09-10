---
name: cf-cpp
description: CodeForge C++ skill for diagnosing, repairing, and translating modern C++ code adhering to Google C++ Style Guide and RAII.
---

# CodeForge Skill: C++

- **SKILL:** C++
- **TRIGGERS:** `.cpp`, `.cc`, `.cxx`, `.hpp`, `.hxx`
- **TOOLCHAIN:** `g++ -std=c++20 -Wall -Wextra -Werror -fsanitize=address,undefined` (or `clang++`)
- **STYLE_GUIDE:** Google C++ Style Guide
- **LINT/FORMAT:** `clang-tidy`, `clang-format`
- **COMMON_FAULTS:**
  - `CPP-001`: Raw manual memory management (`new`/`delete`) without RAII
  - `CPP-002`: Dangling references, pointers, or iterator invalidation
  - `CPP-003`: Missing standard library includes (`<vector>`, `<string>`, `<memory>`, `<algorithm>`)
  - `CPP-004`: Implicit narrowing conversions or signed/unsigned comparison warnings
  - `CPP-005`: Polluting global namespace with `using namespace std;` in header files
  - `CPP-006`: Missing `virtual` destructor on polymorphic base classes
- **IDIOM_RULES:**
  - Smart pointers (`std::unique_ptr`, `std::shared_ptr`) over raw owning pointers
  - Standard library algorithms (`std::ranges`, `<algorithm>`) over manual indexing loops
  - Strict `const`-correctness and pass-by-const-reference for complex types
  - Move semantics (`std::move`) for efficient resource transfer
- **EXECUTION_SANDBOX:**
  - Compile with ASan/UBSan, add `-fsanitize=thread` for concurrent implementations.
