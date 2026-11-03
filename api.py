import os
import time
import requests

# os.environ.get allows for safely fetching the website, and provides a default if the website cannot be found, which is better than hard coding the website URL.
BASE_URL = os.environ.get("DEADLOCK_API", "https://api.deadlock-api.com")

# Seconds of timeout for API requests, and max retries for failed requests.
TIMEOUT = 15
MAX_RETRIES = 3

class ApiErrorException(Exception):
    """General API failure."""

class PlayerNotFoundException(ApiErrorException):
    """API returned 404 or empty result for this player."""

class RateLimitedException(ApiErrorException):
    """After all retries, still getting code 429."""

# This function retrieves data from the API based on provided path and params.
def _get_data(path, params=None, apiKey=None):
    headers = {"Accept": "application/json"}
    if apiKey:
        headers["X-API-KEY"] = apiKey

    # Retry loop.
    for attempt in range (1, MAX_RETRIES + 1):
        try:
            # This line actually requests certain things from the API server.
            resp = requests.get(f"{BASE_URL}{path}", params=params, headers=headers, timeout=TIMEOUT)
        except requests.RequestException as e:
            raise ApiErrorException(f"Network Error: {e}") from e

        # Rate limited error code.
        if resp.status_code == 429:
            if attempt == MAX_RETRIES:
                raise RateLimitedException("Rate limited, try again in a moment.")
            # Sleeps longer per attempt, avoids sending too many requests too quickly to a busy server.
            time.sleep(2 * attempt)
            continue
        if resp.status_code == 404:
            raise PlayerNotFoundException("Player not found.")
        if not resp.ok:
            raise ApiErrorException(f"API returned HTTP {resp.status_code}")

        try:
            data = resp.json()
        except ValueError as e:
            raise ApiErrorException("API returned invalid JSON.") from e
        if data in ([], {}, None):
            raise PlayerNotFoundException("No available data for that player.")
        return data


# When a function has =None in a parameter, it means the parameter is optional when calling the function.
def get_profile(accountID, apiKey=None):
    return _get_data("/v1/players/steam", {"account_ids": accountID}, apiKey)

def get_mmr(accountID, apiKey=None):
    return _get_data("/v1/players/mmr", {"account_ids": accountID}, apiKey)

def get_hero_stats(accountID, apiKey=None):
    return _get_data("/v1/players/hero-stats", {"account_ids": accountID}, apiKey)


# Code for a quick terminal test
if __name__ == "__main__":
    import json
    import sys

    # Puts together command line arguments
    acct = int(sys.argv[1]) if len(sys.argv) > 1 else int(input ("Account ID: "))
    for name, fn in [("profile", get_profile), ("mmr", get_mmr), ("hero stats", get_hero_stats)]:
        print(f"--- {name} ---")
        try:
            # Prints the fetched data values, limits it to 3000 characters.
            print(json.dumps(fn(acct), indent = 2)[:3000])
        except ApiErrorException as e:
            print("Error: ", e)