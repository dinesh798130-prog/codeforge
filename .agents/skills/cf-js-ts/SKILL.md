---
name: cf-js-ts
description: CodeForge JavaScript/TypeScript skill for diagnosing, repairing, and translating modern ECMAScript/TypeScript code.
---

# CodeForge Skill: JavaScript & TypeScript

- **SKILL:** JavaScript / TypeScript
- **TRIGGERS:** `.js`, `.mjs`, `.cjs`, `.ts`, `.mts`, `.cts`, `.jsx`, `.tsx`
- **TOOLCHAIN:** Node.js LTS, `tsc --strict`
- **STYLE_GUIDE:** Airbnb JavaScript Style Guide / TypeScript ESLint Recommended
- **LINT/FORMAT:** `eslint`, `prettier`
- **COMMON_FAULTS:**
  - `JS-001`: Legacy `var` declarations instead of `let` or `const`
  - `JS-002`: Loose equality (`==`, `!=`) instead of strict equality (`===`, `!==`)
  - `JS-003`: Unhandled Promise rejections and omitted `await` keywords
  - `JS-004`: Implicit `any` in TypeScript or unsafe type assertions (`as unknown as T`)
  - `JS-005`: Asynchronous callback hell patterns
  - `JS-006`: Prototype mutations or unintended global variable leaking
- **IDIOM_RULES:**
  - `async`/`await` over chained `.then()`/`.catch()` calls
  - Object and array destructuring and spread syntax
  - Template literals over string concatenation
  - Strict TypeScript interface/type definitions with exhaustive type narrowing
- **EXECUTION_SANDBOX:**
  - Node.js isolated environment with execution timeout.
