---
name: pytest-generator
description: Writes comprehensive unit tests for Python code using pytest, parameterized tests for edge cases, and mocks for external dependencies.
---

# Pytest Generator Skill

This skill guides the agent in generating robust, production-grade test suites using `pytest` for any Python source file.

## Workflow Instructions

### Step 1: Analyze the Target Code
1. Inspect the source file to identify:
   - All public functions, classes, and method signatures.
   - Core business logic, expected happy-path workflows, and return types.
   - Branching conditions, boundary limits, and edge cases (e.g., empty collections, `None` values, zero division, off-by-one bounds).
   - Expected exceptions and error scenarios.
   - External dependencies requiring isolation (e.g., filesystem I/O, database connections, third-party APIs, network calls, environment variables).

### Step 2: Formulate the Test Strategy
1. **Fixtures (`@pytest.fixture`)**:
   - Create reusable fixtures for setup and teardown of state, sample data, and mock objects.
2. **Parameterized Tests (`@pytest.mark.parametrize`)**:
   - Use parametrization to test multiple inputs, boundary conditions, and expected outputs concisely.
3. **Mocking External Dependencies**:
   - Use `unittest.mock` (`patch`, `MagicMock`, `AsyncMock`) or `pytest-mock` (`mocker` fixture) to intercept external calls, API endpoints, and I/O.
4. **Exception Handling Tests**:
   - Use `pytest.raises(<ExpectedException>)` to verify that invalid inputs or system errors raise the proper exceptions.

### Step 3: Write Companion Test File (`test_{filename}.py`)
1. Determine the target path:
   - Name the file `test_{filename}.py` (e.g., for `calculator.py`, write `test_calculator.py`).
   - Place it alongside the source file or inside the project's dedicated `tests/` directory if one exists.
2. Structure the test file:
   - Import necessary modules (`pytest`, `unittest.mock`, etc.).
   - Import the units under test from the target module.
   - Group related tests into classes (e.g., `Test<TargetClass>`) or clearly named test functions (`test_<function_name>_<scenario>_<expected_outcome>`).
   - Write assertions using idiomatic pytest syntax (`assert actual == expected`).

### Step 4: Output and Deliver the Final Test Script
1. Save the test file using the appropriate file writing tool.
2. Output the complete, runnable test script to the user along with:
   - A summary of all covered test scenarios (happy path, edge cases, error cases).
   - Details on mocked dependencies.
   - The CLI command to execute the test suite (e.g., `pytest test_{filename}.py -v`).
