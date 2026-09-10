---
name: cf-go
description: CodeForge Go skill for diagnosing, repairing, and translating idiomatic Go code adhering to Effective Go.
---

# CodeForge Skill: Go

- **SKILL:** Go
- **TRIGGERS:** `.go`
- **TOOLCHAIN:** `go build`, `go vet`, stable Go (1.22+)
- **STYLE_GUIDE:** Effective Go + `gofmt`
- **LINT/FORMAT:** `gofmt`, `golangci-lint`
- **COMMON_FAULTS:**
  - `GO-001`: Silently unhandled `error` return values (`_ = doSomething()`)
  - `GO-002`: Goroutine leaks and unbuffered channel blocking
  - `GO-003`: Shadowed variables in short variable declarations (`:=`)
  - `GO-004`: Nil pointer dereference on pointers, maps, or slices
  - `GO-005`: Misuse of loop variables inside closures (pre-Go 1.22 behavior)
- **IDIOM_RULES:**
  - Explicit error handling pattern: `if err != nil { return ..., fmt.Errorf(...) }`
  - Small, focused interfaces defined by consumers
  - Slices and map idiom initialization (`make()`)
  - `defer` for resource cleanup (mutex unlock, file/connection close)
- **EXECUTION_SANDBOX:**
  - `go run` with `-race` detection enabled when concurrency primitives are used.
