"""Module for retrieving and processing user records from an external API."""

from typing import Any
import requests


def fetch_users(url: str, timeout: float = 10.0) -> list[dict[str, Any]] | None:
    """Fetches user records from a remote API endpoint.

    Args:
        url: The HTTP or HTTPS URL to retrieve user data from.
        timeout: The request timeout in seconds. Defaults to 10.0.

    Returns:
        A list of user dictionaries if the request succeeded and returned
        valid JSON, or None if a network, HTTP, or parsing error occurred.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return data
        return None
    except (requests.RequestException, ValueError):
        return None


def process_data(users: list[dict[str, Any]]) -> list[str]:
    """Filters active adult users and extracts their lowercase names.

    Args:
        users: A list of dictionaries representing user records.

    Returns:
        A list of lowercase names of active users who are 18 or older.
    """
    active_adults: list[str] = []
    for user in users:
        if not isinstance(user, dict):
            continue
        age = user.get("age")
        status = user.get("status")
        name = user.get("name")
        if (
            isinstance(age, (int, float))
            and age >= 18
            and status == "active"
            and name is not None
        ):
            active_adults.append(str(name).lower())
    return active_adults


def main(url: str) -> list[str]:
    """Coordinates fetching and processing active adult users from a URL.

    Args:
        url: The endpoint URL to fetch users from.

    Returns:
        A list of lowercase names of active adult users, or an empty list if
        retrieval failed or no users matched.
    """
    data = fetch_users(url)
    if data is not None:
        results = process_data(data)
        print("active adults:", results)
        return results
    return []


if __name__ == "__main__":
    main("https://api.example.com/users")
