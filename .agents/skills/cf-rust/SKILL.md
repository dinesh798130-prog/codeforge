---
name: cf-rust
description: CodeForge Rust skill for diagnosing, repairing, and translating memory-safe idiomatic Rust code adhering to Rust API Guidelines.
---

# CodeForge Skill: Rust

- **SKILL:** Rust
- **TRIGGERS:** `.rs`
- **TOOLCHAIN:** Stable `rustc` / `cargo`
- **STYLE_GUIDE:** Rust API Guidelines
- **LINT/FORMAT:** `cargo clippy`, `rustfmt`
- **COMMON_FAULTS:**
  - `RS-001`: Excessive, unnecessary `.clone()` or `.to_owned()` calls
  - `RS-002`: Unsafe panicking methods (`.unwrap()`, `.expect()`) on fallible code paths
  - `RS-003`: Borrow-checker conflicts (multiple mutable references, lifetime issues)
  - `RS-004`: Unjustified or undocumented `unsafe` blocks
  - `RS-005`: Misuse of `String` vs `&str`, or `Vec<T>` vs `&[T]` in function parameters
- **IDIOM_RULES:**
  - Ownership, borrowing, and RAII-first design patterns
  - `?` operator for clean error propagation with `Result<T, E>`
  - Iterator combinators (`map`, `filter`, `fold`) over manual index loops
  - Exhaustive pattern matching (`match`, `if let`)
- **EXECUTION_SANDBOX:**
  - `cargo run` in container; explicit scrutiny on `unsafe` blocks.
