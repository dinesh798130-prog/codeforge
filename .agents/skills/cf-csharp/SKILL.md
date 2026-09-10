---
name: cf-csharp
description: CodeForge C# skill for diagnosing, repairing, and translating C# code adhering to Microsoft C# Coding Conventions and .NET standards.
---

# CodeForge Skill: C#

- **SKILL:** C#
- **TRIGGERS:** `.cs`
- **TOOLCHAIN:** .NET SDK (Current LTS), `dotnet run`
- **STYLE_GUIDE:** Microsoft C# Coding Conventions
- **LINT/FORMAT:** `dotnet format`, Roslyn analyzers
- **COMMON_FAULTS:**
  - `CS-001`: Missing `using` or `await using` disposal of `IDisposable`/`IAsyncDisposable`
  - `CS-002`: Confusing reference equality (`ReferenceEquals` / `==`) with value equality
  - `CS-003`: Unhandled `NullReferenceException` risks (nullable reference types disregarded)
  - `CS-004`: Blocking on async tasks (`.Result` or `.Wait()`) causing deadlocks
  - `CS-005`: Misusing LINQ multiple enumeration on deferred queries
- **IDIOM_RULES:**
  - LINQ method syntax over manual nested loops where clear
  - Nullable reference types enabled (`#nullable enable`)
  - Target-typed `new()`, pattern matching (`switch` expressions)
  - `async`/`await` propagation with `CancellationToken` support
- **EXECUTION_SANDBOX:**
  - `dotnet run` in isolated project folder with memory caps.
