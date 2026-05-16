import argparse
from github_api import fetch_user_events
from event_formatter import EventFormatter

def main():
    parser = argparse.ArgumentParser(
        description="Display GitHub user activity"
    )
    parser.add_argument("user", type=str, help="GitHub username")
    parser.add_argument("-l", "--limit", type=int, default=5, help="Number of events to display")
    args = parser.parse_args()

    data = fetch_user_events(args.user)

    limit = args.limit
    for event in data[:limit]:
        print('-', EventFormatter.format(event['type'], event))

if __name__ == "__main__":
    main()