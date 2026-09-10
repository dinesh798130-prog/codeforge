---
name: cf-java
description: CodeForge Java skill for diagnosing, repairing, and translating Java code adhering to Google Java Style Guide.
---

# CodeForge Skill: Java

- **SKILL:** Java
- **TRIGGERS:** `.java`
- **TOOLCHAIN:** OpenJDK 21+, `javac` + `java`
- **STYLE_GUIDE:** Google Java Style Guide
- **LINT/FORMAT:** `google-java-format`, `checkstyle`
- **COMMON_FAULTS:**
  - `JAVA-001`: Class name mismatch with filename for `public class`
  - `JAVA-002`: Unhandled checked exceptions
  - `JAVA-003`: Reference equality (`==`) instead of `.equals()` on `String` or object types
  - `JAVA-004`: Resource leak (omitting try-with-resources on `AutoCloseable` streams/connections)
  - `JAVA-005`: NullPointer risks without null checking or `Optional`
  - `JAVA-006`: Raw generic types without type parameters (`List` instead of `List<String>`)
- **IDIOM_RULES:**
  - Streams and lambda expressions (`map`, `filter`, `collect`) over manual iteration where readable
  - Try-with-resources statement for all `AutoCloseable` types
  - `Optional<T>` for potentially missing return values rather than returning `null`
  - Immutable collections (`List.of`, `Set.of`, `Map.of`) where appropriate
- **EXECUTION_SANDBOX:**
  - Memory-capped JVM (`-Xmx256m`), no `Runtime.getRuntime().exec()`.
