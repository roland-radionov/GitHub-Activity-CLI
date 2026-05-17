import requests
import sys
import json
import time
from pathlib import Path

def fetch_user_events(username: str) -> list[dict]:
    cache_dir = Path.home() / ".cache_github_activity"
    cache_dir.mkdir(exist_ok=True)
    cache_file = cache_dir / f"{username}.json"
    cache_ttl = 300

    if cache_file.exists():
        file_age = time.time() - cache_file.stat().st_mtime
        if file_age < cache_ttl:
            with cache_file.open(encoding="utf-8") as f:
                data = json.load(f)
                print(f"Using cache from: {cache_file}")

            return data
        else:
            print("Cache expired: fetching fresh data")

    try:
        url = f"https://api.github.com/users/{username}/events"
        response = requests.get(url)
        response.raise_for_status()
        print("Successfully fetched GitHub activity")

        with cache_file.open('w', encoding="utf-8") as f:
            json.dump(response.json(), f, indent=2)
        print(f"Cached to {cache_file}")

        return response.json()

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            sys.exit(f"Error: User {username} not found")
        else:
            sys.exit(f"HTTP error: {e}")

    except requests.exceptions.ConnectionError:
        sys.exit("Error: No internet connection")

    except requests.exceptions.Timeout:
        sys.exit("Error: Request timeout")

    except requests.exceptions.RequestException as e:
        sys.exit(f"Error getting GitHub activity: {e}")