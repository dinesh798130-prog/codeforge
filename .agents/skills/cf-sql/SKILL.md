---
name: cf-sql
description: CodeForge SQL skill for diagnosing, repairing, and translating relational queries and schemas with dialect verification.
---

# CodeForge Skill: SQL

- **SKILL:** SQL
- **TRIGGERS:** `.sql`
- **TOOLCHAIN:** SQLite3 (portable local CLI) + PostgreSQL/MySQL dialect markers
- **STYLE_GUIDE:** Uppercase SQL keywords, snake_case table/column identifiers, explicit `JOIN ... ON`
- **LINT/FORMAT:** `sqlfluff`
- **COMMON_FAULTS:**
  - `SQL-001`: SQL injection vulnerabilities from unparameterized string concatenation
  - `SQL-002`: Comma-joins (`FROM A, B WHERE ...`) instead of explicit `INNER/LEFT JOIN`
  - `SQL-003`: Ambiguous column names in multi-table queries without table aliases
  - `SQL-004`: Wildcard `SELECT *` in production/analytic queries
  - `SQL-005`: Missing index references on primary join or filter predicates
  - `SQL-006`: Incorrect `NULL` handling (using `= NULL` instead of `IS NULL`)
- **IDIOM_RULES:**
  - Parameterized statements and prepared queries
  - Common Table Expressions (`WITH ... AS`) over deep nested subqueries
  - Explicit column projection lists and descriptive aliases
  - Window functions (`ROW_NUMBER()`, `RANK()`) for ranked aggregations
- **EXECUTION_SANDBOX:**
  - In-memory SQLite (`:memory:`) or ephemeral database seeded with test records.
