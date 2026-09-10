---
description: Enforces PEP-8 standards, complete function signature type hints, and Google-style docstrings for Python files.
globs: ["**/*.py"]
alwaysApply: false
---

# Python Code Standards and Conventions

This rule applies automatically to all Python files (`**/*.py`) within the workspace. All Python code created, modified, or refactored must adhere to PEP-8 standards, include comprehensive type hints on all function and method signatures, and supply Google-style docstrings for every public function, method, class, and module.

---

## 1. PEP-8 Standards Compliance

All code must conform to [PEP 8 -- Style Guide for Python Code](https://peps.python.org/pep-0008/):

### 1.1 Indentation & Whitespace
- **Indentation**: Use exactly 4 spaces per indentation level. Never use tabs.
- **Line Length**: Limit all lines to a maximum of 79 characters for code, and 72 characters for docstrings and comments (or 88 characters if following Black-compatible formatting).
- **Line Breaks**: Break lines before binary operators, adhering to mathematical convention:
  ```python
  total_cost = (
      base_price
      + tax_amount
      - discount_applied
  )
  ```
- **Blank Lines**:
  - Separate top-level function and class definitions with 2 blank lines.
  - Separate method definitions inside a class with 1 blank line.
  - Use blank lines sparingly inside functions to separate logical sections.
- **Trailing Whitespace**: Do not leave trailing whitespace on any line. Ensure all files end with a single newline.

### 1.2 Naming Conventions
- **Modules & Packages**: Short, all-lowercase names with underscores if necessary (e.g., `data_loader.py`, `models/`).
- **Classes**: PascalCase (e.g., `HttpRequestHandler`, `UserProfile`).
- **Functions & Methods**: snake_case (e.g., `calculate_metrics()`, `get_user_by_id()`).
- **Variables & Attributes**: snake_case (e.g., `item_count`, `is_active`).
- **Constants**: UPPER_SNAKE_CASE (e.g., `MAX_RETRY_ATTEMPTS`, `DEFAULT_TIMEOUT`).
- **Non-Public / Internal Members**: Single leading underscore for protected members (e.g., `_internal_cache`, `_parse_raw_data()`).

### 1.3 Imports Organization
Group imports at the top of the file into three distinct blocks, separated by a single blank line, in this exact order:
1. **Standard library imports** (e.g., `import os`, `import sys`, `from typing import Any`)
2. **Related third-party imports** (e.g., `import numpy as np`, `import pydantic`)
3. **Local application / library-specific imports** (e.g., `from my_project.utils import format_date`)

Rules for imports:
- Put each import on a separate line (`import os` and `import sys`, not `import os, sys`).
- Avoid wildcard imports (`from module import *`).
- Prefer absolute imports over relative imports.

---

## 2. Type Hinting Requirements

Every function and method signature must have explicit, precise type annotations.

### 2.1 Function & Method Signatures
- **Parameters**: Every parameter (except `self` and `cls`) must have an explicit type hint:
  ```python
  def process_records(records: list[dict[str, Any]], batch_size: int = 100) -> int:
  ```
- **Return Types**: Every function and method must declare a return type annotation. Functions that do not explicitly return a value must declare `-> None`:
  ```python
  def log_status(message: str) -> None:
  ```
- **`*args` and `**kwargs`**: Annotate with the type of elements/values:
  ```python
  def execute_actions(*actions: Callable[[], bool], **metadata: str) -> bool:
  ```
- **Self & Cls**:
  - `self` in instance methods does not require an annotation unless returning the instance itself (use `from typing_extensions import Self` or `typing.Self` in Python 3.11+):
    ```python
    def set_name(self, name: str) -> Self:
        self.name = name
        return self
    ```

### 2.2 Typing Best Practices
- Prefer modern built-in generics (Python 3.9+) such as `list[str]`, `dict[str, Any]`, `tuple[int, ...]`, and `set[int]`.
- Use union syntax `T | None` (or `Optional[T]` for Python < 3.10) for nullable types.
- Avoid loose `Any` types whenever a more specific type, generic `TypeVar`, or `Protocol` can be expressed.

---

## 3. Google-Style Docstring Mandate

Every public module, class, public method, and public function must include a comprehensive Google-style docstring.

### 3.1 Structure & Sections
A Google-style docstring consists of:
1. **Summary line**: A concise, single-line imperative statement ending with a period.
2. **Extended description** (optional): Additional details, context, and usage notes separated by a blank line.
3. **`Args:`**: List each argument with its description. Explain preconditions, accepted ranges, or default behaviors.
4. **`Returns:`**: Detail the type and semantic meaning of the return value. (Omit if the function returns `None`).
5. **`Raises:`**: List all exceptions explicitly raised by the function and the conditions that trigger them.
6. **`Yields:`**: (For generators) Describe the type and meaning of yielded values.
7. **`Examples:`** (optional): Provide interactive doctest-style or clear markdown usage examples.

### 3.2 Standard Docstring Example
```python
def fetch_user_profile(user_id: int, include_deleted: bool = False) -> dict[str, Any]:
    """Retrieves the profile information for a specified user.

    Queries the backend database to fetch user details. If `include_deleted`
    is set to True, records marked as soft-deleted are also returned.

    Args:
        user_id: The unique integer identifier of the user.
        include_deleted: Whether to include soft-deleted user records.
            Defaults to False.

    Returns:
        A dictionary containing user profile attributes such as "username",
        "email", and "created_at".

    Raises:
        ValueError: If `user_id` is non-positive.
        UserNotFoundError: If no matching user record exists and `include_deleted`
            is False.

    Examples:
        >>> profile = fetch_user_profile(42)
        >>> print(profile["username"])
        'dinesh'
    """
```

### 3.3 Class Docstring Example
```python
class DataPipeline:
    """Manages extract, transform, and load (ETL) processing workflows.

    Attributes:
        source_uri: The connection URI for the data source.
        batch_size: The number of records to process per batch iteration.
    """

    def __init__(self, source_uri: str, batch_size: int = 500) -> None:
        """Initializes the DataPipeline with source connection and batch settings.

        Args:
            source_uri: The source connection string or URI.
            batch_size: The record batch size. Must be greater than 0.
                Defaults to 500.

        Raises:
            ValueError: If `batch_size` is less than or equal to 0.
        """
        if batch_size <= 0:
            raise ValueError("batch_size must be positive.")
        self.source_uri = source_uri
        self.batch_size = batch_size
```

---

## 4. Enforcement Checklist

Before completing any Python code generation or modification, verify:
- [ ] PEP-8 formatting: 4-space indentation, no lines exceeding length limit, proper blank line spacing.
- [ ] Clean import order: standard library, third-party, and local modules clearly separated.
- [ ] Strict type hints: Every parameter and return type explicitly annotated.
- [ ] Google-style docstrings: Present on all public functions, classes, and methods, including `Args:`, `Returns:`, and `Raises:` sections where applicable.
