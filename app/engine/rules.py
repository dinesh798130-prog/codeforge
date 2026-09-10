"""Rule definitions and catalog for the CodeForge engine."""

from typing import Any

RULES_CATALOG: dict[str, dict[str, Any]] = {
    # Python Rules
    "PY-001": {
        "language": "python",
        "severity": "blocks_compilation",
        "title": "Indentation / Syntax Error",
        "description": "Inconsistent indentation, mixed tabs/spaces, or malformed syntax.",
    },
    "PY-002": {
        "language": "python",
        "severity": "logic_risk",
        "title": "Mutable Default Argument",
        "description": "Default parameter value is mutable (list/dict/set), causing cross-call state pollution.",
    },
    "PY-003": {
        "language": "python",
        "severity": "logic_risk",
        "title": "Bare Except Clause",
        "description": "Bare 'except:' intercepts system exit, keyboard interrupt, and masks critical bugs.",
    },
    "PY-004": {
        "language": "python",
        "severity": "logic_risk",
        "title": "Off-by-One / Range Boundary Error",
        "description": "Index out of range or incorrect range() boundary logic.",
    },
    "PY-005": {
        "language": "python",
        "severity": "blocks_compilation",
        "title": "Legacy Python 2 Syntax",
        "description": "Use of print statement without parentheses or obsolete syntax.",
    },
    "PY-006": {
        "language": "python",
        "severity": "style_only",
        "title": "Missing Resource Management Context",
        "description": "File or socket opened without 'with' statement context manager.",
    },
    "PY-007": {
        "language": "python",
        "severity": "style_only",
        "title": "Missing Type Hints / PEP-8 Violation",
        "description": "Function missing parameter/return type hints or violates PEP-8 spacing/naming.",
    },

    # C Rules
    "C-001": {
        "language": "c",
        "severity": "blocks_compilation",
        "title": "Missing Header Include",
        "description": "Missing required header inclusion (<stdio.h>, <stdlib.h>, <string.h>, etc.).",
    },
    "C-002": {
        "language": "c",
        "severity": "logic_risk",
        "title": "Buffer Overflow / Out of Bounds",
        "description": "Array indexing or string copy beyond allocated buffer capacity.",
    },
    "C-003": {
        "language": "c",
        "severity": "logic_risk",
        "title": "Memory Leak / Unfreed Heap Allocation",
        "description": "Dynamically allocated memory (malloc/calloc) without corresponding free().",
    },
    "C-004": {
        "language": "c",
        "severity": "logic_risk",
        "title": "Uninitialized Variable / Pointer",
        "description": "Read from uninitialized local variable or wild pointer dereference.",
    },
    "C-005": {
        "language": "c",
        "severity": "blocks_compilation",
        "title": "Printf Format Specifier Mismatch",
        "description": "Format specifier type in printf/scanf does not match argument type.",
    },
    "C-006": {
        "language": "c",
        "severity": "blocks_compilation",
        "title": "Missing Return in Non-Void Function",
        "description": "Non-void function reaches end of body without returning a value.",
    },
    "C-007": {
        "language": "c",
        "severity": "logic_risk",
        "title": "Unsafe Function Call",
        "description": "Use of inherently unsafe functions (gets, strcpy) instead of bounded alternatives.",
    },

    # C++ Rules
    "CPP-001": {
        "language": "cpp",
        "severity": "logic_risk",
        "title": "Raw Owning Pointer / Non-RAII Resource",
        "description": "Manual new/delete instead of std::unique_ptr, std::shared_ptr, or RAII container.",
    },
    "CPP-002": {
        "language": "cpp",
        "severity": "logic_risk",
        "title": "Dangling Reference / Iterator Invalidation",
        "description": "Reference or pointer to local variable or iterator after container modification.",
    },
    "CPP-003": {
        "language": "cpp",
        "severity": "blocks_compilation",
        "title": "Missing Standard Include",
        "description": "Missing #include <vector>, <string>, <memory>, <algorithm>, or <iostream>.",
    },
    "CPP-004": {
        "language": "cpp",
        "severity": "style_only",
        "title": "Missing Const Correctness",
        "description": "Parameter passed by value or non-const reference when const reference is preferred.",
    },
    "CPP-005": {
        "language": "cpp",
        "severity": "style_only",
        "title": "Namespace Pollution",
        "description": "'using namespace std;' used in headers or global scope.",
    },

    # Java Rules
    "JAVA-001": {
        "language": "java",
        "severity": "blocks_compilation",
        "title": "Class Name / Filename Mismatch",
        "description": "Public class name does not match file naming conventions.",
    },
    "JAVA-002": {
        "language": "java",
        "severity": "blocks_compilation",
        "title": "Unhandled Checked Exception",
        "description": "Method does not declare throws or catch checked exceptions.",
    },
    "JAVA-003": {
        "language": "java",
        "severity": "logic_risk",
        "title": "Reference Equality on Strings/Objects",
        "description": "Using '==' instead of '.equals()' for String or object content comparison.",
    },
    "JAVA-004": {
        "language": "java",
        "severity": "logic_risk",
        "title": "Resource Leak / Missing Try-with-Resources",
        "description": "AutoCloseable stream or connection not managed in try-with-resources.",
    },
    "JAVA-005": {
        "language": "java",
        "severity": "logic_risk",
        "title": "NullPointer Risk",
        "description": "Dereference of potentially null reference without null check or Optional.",
    },
    "JAVA-006": {
        "language": "java",
        "severity": "style_only",
        "title": "Raw Generic Types",
        "description": "Use of raw collection types without generic type parameters.",
    },

    # JavaScript / TypeScript Rules
    "JS-001": {
        "language": "javascript",
        "severity": "style_only",
        "title": "Var Declaration Instead of Let/Const",
        "description": "Use of function-scoped 'var' instead of block-scoped 'let' or 'const'.",
    },
    "JS-002": {
        "language": "javascript",
        "severity": "logic_risk",
        "title": "Loose Equality Operator",
        "description": "Use of '==' or '!=' instead of strict '===' or '!=='.",
    },
    "JS-003": {
        "language": "javascript",
        "severity": "logic_risk",
        "title": "Unhandled Promise / Missing Await",
        "description": "Promise returned by async function called synchronously without await or .catch().",
    },
    "JS-004": {
        "language": "typescript",
        "severity": "style_only",
        "title": "Implicit Any Type",
        "description": "Variable or function parameter lacks explicit TypeScript type annotation.",
    },
    "JS-005": {
        "language": "javascript",
        "severity": "blocks_compilation",
        "title": "Syntax Error / Undefined Symbol",
        "description": "Unterminated string, missing parenthesis/bracket, or reference to undefined variable.",
    },

    # Go Rules
    "GO-001": {
        "language": "go",
        "severity": "logic_risk",
        "title": "Unhandled Error Return",
        "description": "Error return value discarded or ignored without checking if err != nil.",
    },
    "GO-002": {
        "language": "go",
        "severity": "logic_risk",
        "title": "Goroutine / Resource Leak",
        "description": "Goroutine launched without termination channel or deferred resource cleanup.",
    },
    "GO-003": {
        "language": "go",
        "severity": "logic_risk",
        "title": "Shadowed Variable in := Assignment",
        "description": "Short variable declaration shadows outer scope variable unintentionally.",
    },
    "GO-004": {
        "language": "go",
        "severity": "blocks_compilation",
        "title": "Unused Import or Variable",
        "description": "Imported package or declared local variable is never referenced.",
    },

    # Rust Rules
    "RS-001": {
        "language": "rust",
        "severity": "logic_risk",
        "title": "Unsafe Unwrap on Fallible Path",
        "description": "Direct .unwrap() or .expect() on Result/Option without fallback handling.",
    },
    "RS-002": {
        "language": "rust",
        "severity": "logic_risk",
        "title": "Borrow Checker Violation",
        "description": "Simultaneous mutable and immutable borrows, or use after move.",
    },
    "RS-003": {
        "language": "rust",
        "severity": "style_only",
        "title": "Redundant Clone / Allocation",
        "description": "Unnecessary .clone() call where reference borrowing would suffice.",
    },

    # C# Rules
    "CS-001": {
        "language": "csharp",
        "severity": "logic_risk",
        "title": "Missing IDisposable Using Statement",
        "description": "Disposable resource instantiated without 'using' statement or declaration.",
    },
    "CS-002": {
        "language": "csharp",
        "severity": "logic_risk",
        "title": "NullReference Risk",
        "description": "Nullable reference dereferenced without null propagation (?.) or check.",
    },
    "CS-003": {
        "language": "csharp",
        "severity": "logic_risk",
        "title": "Sync-over-Async Blocking",
        "description": "Calling .Result or .Wait() on Task causes thread pool starvation/deadlock.",
    },

    # SQL Rules
    "SQL-001": {
        "language": "sql",
        "severity": "logic_risk",
        "title": "SQL Injection Risk / Unparameterized Query",
        "description": "Dynamic string concatenation in query predicates instead of parameter binding.",
    },
    "SQL-002": {
        "language": "sql",
        "severity": "style_only",
        "title": "Implicit Comma Join",
        "description": "Use of comma-separated table list instead of explicit INNER/LEFT JOIN ... ON.",
    },
    "SQL-003": {
        "language": "sql",
        "severity": "logic_risk",
        "title": "Incorrect NULL Comparison",
        "description": "Comparing column with '= NULL' or '!= NULL' instead of 'IS NULL' / 'IS NOT NULL'.",
    },
    "SQL-004": {
        "language": "sql",
        "severity": "style_only",
        "title": "Wildcard SELECT * Usage",
        "description": "SELECT * used instead of explicit column projection list.",
    },

    # Cross-Cutting DSA Rules
    "DSA-001": {
        "language": "dsa",
        "severity": "logic_risk",
        "title": "Unhandled Empty Input / Base Case",
        "description": "Algorithm does not guard against empty collections, size-0 arrays, or None/null.",
    },
    "DSA-002": {
        "language": "dsa",
        "severity": "logic_risk",
        "title": "Boundary / Off-by-One Condition",
        "description": "Loop index, binary search midpoint, or slice bounds off by one.",
    },
    "DSA-003": {
        "language": "dsa",
        "severity": "logic_risk",
        "title": "Integer Overflow / Arithmetic Bounds",
        "description": "Potential integer overflow in sum calculation or binary search (low + high) // 2.",
    },
    "DSA-004": {
        "language": "dsa",
        "severity": "logic_risk",
        "title": "Suboptimal Complexity Gap",
        "description": "Algorithm operates in O(N^2) time complexity where standard O(N log N) or O(N) exists.",
    },
}
