"""Unit test suite for user_processor module using pytest."""

from typing import Any
from unittest.mock import MagicMock, patch
import pytest
import requests

from user_processor import fetch_users, main, process_data


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_user_records() -> list[dict[str, Any]]:
    """Provides a realistic dataset containing mixed valid and invalid users.

    Returns:
        A list of dictionary records simulating API user responses.
    """
    return [
        {"name": "ALICE", "age": 25, "status": "active"},
        {"name": "Bob", "age": 17, "status": "active"},
        {"name": "Charlie", "age": 18, "status": "active"},
        {"name": "Diana", "age": 30, "status": "inactive"},
        {"name": "Evan", "age": 19, "status": "pending"},
        {"name": None, "age": 22, "status": "active"},
        {"age": 40, "status": "active"},
        {"name": "Frank"},
    ]


# ---------------------------------------------------------------------------
# Tests for process_data
# ---------------------------------------------------------------------------

class TestProcessData:
    """Test group for the process_data function."""

    def test_process_data_with_sample_records(
        self, sample_user_records: list[dict[str, Any]]
    ) -> None:
        """Verifies filtering of active adults from a mixed dataset.

        Args:
            sample_user_records: Fixture supplying valid and invalid records.
        """
        result = process_data(sample_user_records)
        assert result == ["alice", "charlie"]

    @pytest.mark.parametrize(
        "user,expected",
        [
            ({"name": "JOHN", "age": 18, "status": "active"}, ["john"]),
            ({"name": "JANE", "age": 17.9, "status": "active"}, []),
            ({"name": "DOE", "age": 19, "status": "inactive"}, []),
            ({"name": "SMITH", "age": 65, "status": "ACTIVE"}, []),
            ({"name": "KATE", "age": 20, "status": "active"}, ["kate"]),
            ({"name": "LEO", "age": "twenty", "status": "active"}, []),
            ({"name": "MIA", "age": None, "status": "active"}, []),
        ],
    )
    def test_process_data_individual_cases(
        self, user: dict[str, Any], expected: list[str]
    ) -> None:
        """Tests individual boundary conditions, status matches, and types.

        Args:
            user: Dictionary containing individual test user properties.
            expected: Expected list of filtered names.
        """
        assert process_data([user]) == expected

    def test_process_data_empty_input(self) -> None:
        """Verifies that an empty input list produces an empty result list."""
        assert process_data([]) == []

    def test_process_data_handles_malformed_elements(self) -> None:
        """Ensures non-dictionary items are safely ignored without crashing."""
        malformed_data: list[Any] = [
            None,
            "invalid_string",
            42,
            [],
            {"name": "Zoe", "age": 20, "status": "active"},
        ]
        assert process_data(malformed_data) == ["zoe"]


# ---------------------------------------------------------------------------
# Tests for fetch_users
# ---------------------------------------------------------------------------

class TestFetchUsers:
    """Test group for the fetch_users function."""

    @patch("requests.get")
    def test_fetch_users_success(self, mock_get: MagicMock) -> None:
        """Verifies successful retrieval of user records from API.

        Args:
            mock_get: Mocked requests.get function.
        """
        expected_users = [{"name": "Alice", "age": 25, "status": "active"}]
        mock_response = MagicMock()
        mock_response.json.return_value = expected_users
        mock_get.return_value = mock_response

        users = fetch_users("https://api.example.com/users", timeout=5.0)

        mock_get.assert_called_once_with(
            "https://api.example.com/users", timeout=5.0
        )
        mock_response.raise_for_status.assert_called_once()
        assert users == expected_users

    @patch("requests.get")
    def test_fetch_users_non_list_response(self, mock_get: MagicMock) -> None:
        """Verifies that fetch_users returns None if response JSON is not a list.

        Args:
            mock_get: Mocked requests.get function.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": "unexpected structure"}
        mock_get.return_value = mock_response

        users = fetch_users("https://api.example.com/users")
        assert users is None

    @pytest.mark.parametrize(
        "raised_exception",
        [
            requests.exceptions.ConnectionError("Failed to connect"),
            requests.exceptions.Timeout("Request timed out"),
            requests.exceptions.HTTPError("404 Not Found"),
            ValueError("Invalid JSON"),
        ],
    )
    @patch("requests.get")
    def test_fetch_users_network_and_parse_errors(
        self, mock_get: MagicMock, raised_exception: Exception
    ) -> None:
        """Verifies that network exceptions and JSON parsing errors return None.

        Args:
            mock_get: Mocked requests.get function.
            raised_exception: Exception type to be simulated.
        """
        mock_get.side_effect = raised_exception
        result = fetch_users("https://api.example.com/users")
        assert result is None


# ---------------------------------------------------------------------------
# Tests for main
# ---------------------------------------------------------------------------

class TestMain:
    """Test group for the orchestrator main function."""

    @patch("user_processor.fetch_users")
    @patch("user_processor.process_data")
    def test_main_success_flow(
        self,
        mock_process: MagicMock,
        mock_fetch: MagicMock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Verifies full execution pipeline when users are successfully fetched.

        Args:
            mock_process: Mocked process_data function.
            mock_fetch: Mocked fetch_users function.
            capsys: Pytest fixture to capture stdout and stderr.
        """
        raw_users = [{"name": "Alice", "age": 25, "status": "active"}]
        mock_fetch.return_value = raw_users
        mock_process.return_value = ["alice"]

        result = main("https://api.example.com/users")

        mock_fetch.assert_called_once_with("https://api.example.com/users")
        mock_process.assert_called_once_with(raw_users)
        assert result == ["alice"]

        captured = capsys.readouterr()
        assert "active adults: ['alice']" in captured.out

    @patch("user_processor.fetch_users")
    def test_main_fetch_failure(self, mock_fetch: MagicMock) -> None:
        """Verifies that main returns an empty list when fetch_users fails.

        Args:
            mock_fetch: Mocked fetch_users function.
        """
        mock_fetch.return_value = None

        result = main("https://api.example.com/users")
        assert result == []
