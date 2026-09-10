"""Unit and integration test suite for CodeForge autonomous engine and API."""

import pytest
from fastapi.testclient import TestClient

from app.engine.analyzer import detect_language, diagnose_code, get_dsa_complexity_summary
from app.engine.repairer import repair_code
from app.engine.sandbox import execute_in_sandbox
from app.engine.translator import translate_all
from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Provides test client for FastAPI endpoints."""
    return TestClient(app)


# ---------------------------------------------------------------------------
# Analyzer Tests
# ---------------------------------------------------------------------------

class TestAnalyzer:
    """Tests language detection and rule-based diagnosis."""

    @pytest.mark.parametrize(
        "filename,code,expected_lang",
        [
            ("script.py", "print('hello')", "python"),
            ("main.c", "#include <stdio.h>\nint main(){}", "c"),
            ("main.cpp", "#include <iostream>\nint main(){}", "cpp"),
            ("App.java", "public class App { public static void main(String[] args){} }", "java"),
            ("index.js", "const x = 10; console.log(x);", "javascript"),
            ("types.ts", "const x: number = 10;", "typescript"),
            ("main.go", "package main\nimport \"fmt\"\nfunc main(){}", "go"),
            ("main.rs", "fn main() { println!(\"Hi\"); }", "rust"),
            ("query.sql", "SELECT id, name FROM users WHERE active = 1;", "sql"),
        ],
    )
    def test_detect_language(self, filename: str, code: str, expected_lang: str) -> None:
        lang, confidence = detect_language(filename, code)
        assert lang == expected_lang
        assert confidence >= 0.85

    def test_diagnose_python_bare_except_and_range_loop(self) -> None:
        broken_code = "try:\n    pass\nexcept:\n    pass\nfor i in range(len(arr)):\n    pass"
        diagnoses = diagnose_code(broken_code, "python")
        rule_ids = [d["rule_id"] for d in diagnoses]
        assert "PY-003" in rule_ids
        assert "PY-004" in rule_ids

    def test_diagnose_dsa_binary_search(self) -> None:
        broken_bs = "def binary_search(arr, target):\n    low, high = 0, len(arr)-1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: low = mid + 1\n        else: high = mid"
        diagnoses = diagnose_code(broken_bs, "python")
        rule_ids = [d["rule_id"] for d in diagnoses]
        assert "DSA-003" in rule_ids
        assert "DSA-002" in rule_ids

        dsa_summary = get_dsa_complexity_summary(broken_bs)
        assert dsa_summary["time_complexity"] == "O(log N)"
        assert dsa_summary["space_complexity"] == "O(1)"


# ---------------------------------------------------------------------------
# Repairer Tests
# ---------------------------------------------------------------------------

class TestRepairer:
    """Tests minimal-diff repairs."""

    def test_repair_python_bare_except(self) -> None:
        broken = "try:\n    x = 1\nexcept:\n    pass"
        fixed = repair_code(broken, "python")
        assert "except Exception as e:" in fixed

    def test_repair_python_none_comparison(self) -> None:
        broken = "if val != None:\n    print(val)"
        fixed = repair_code(broken, "python")
        assert "val is not None" in fixed


# ---------------------------------------------------------------------------
# Sandbox Tests
# ---------------------------------------------------------------------------

class TestSandbox:
    """Tests execution sandboxing and security safeguards."""

    def test_sandbox_python_success(self) -> None:
        code = "print('Hello from CodeForge sandbox!')"
        res = execute_in_sandbox("python", code)
        assert res.exit_code == 0
        assert "Hello from CodeForge sandbox!" in res.stdout
        assert res.status == "success"

    def test_sandbox_blocks_unsafe_code(self) -> None:
        code = "import os\nos.system('rm -rf /')"
        res = execute_in_sandbox("python", code)
        assert res.status == "unsafe_blocked"
        assert res.exit_code != 0


# ---------------------------------------------------------------------------
# API Integration Tests
# ---------------------------------------------------------------------------

class TestApiEndpoints:
    """Tests FastAPI routes and end-to-end processing pipeline."""

    def test_health_check(self, client: TestClient) -> None:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_get_presets(self, client: TestClient) -> None:
        response = client.get("/api/presets")
        assert response.status_code == 200
        presets = response.json()
        assert len(presets) >= 4

    def test_api_process_pipeline(self, client: TestClient) -> None:
        payload = {
            "filename": "sample.py",
            "code": "print 'Python 2'\nif x != None:\n    pass",
        }
        response = client.post("/api/process", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["detected_language"] == "python"
        assert len(data["diagnoses"]) > 0
        assert "print('Python 2')" in data["fixed_code"] or "is not None" in data["fixed_code"]
        assert len(data["polyglot_grid"]) > 0
