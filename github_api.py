import requests
import sys

def fetch_user_events(username: str) -> list[dict]:
    try:
        url = f"https://api.github.com/users/{username}/events"
        response = requests.get(url)
        response.raise_for_status()
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