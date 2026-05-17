# GitHub Activity CLI

CLI tool to fetch and display recent GitHub user activity

## Features

- Fetch recent events from any GitHub user
- Filter events by type (PushEvent, IssuesEvent, etc.)
- Cache responses to reduce API calls (5 minutes TTL)
- Install as global command

## Installation

```bash
git clone https://github.com/roland-radionov/GitHub-Activity-CLI.git
cd GitHub-Activity-CLI
pip install .
```

## Usage

```bash
# Show recent activity for user
github-activity octocat

# Filter by event type
github-activity octocat --type PushEvent

# Show last 5 events
github-activity octocat --limit 5
```

## Options

| Option | Description |
|--------|-------------|
| `user` | GitHub username (required) |
| `-l, --limit` | Number of events to display (default: 10) |
| `-t, --type` | Filter by event type |
| `-h, --help` | Show help message |

## Supported Event Types

- PushEvent - New commits
- WatchEvent - Starred repository
- IssuesEvent - Opened/closed issues
- PullRequestEvent - Pull request activity
- CreateEvent - New branch/tag/repo
- ForkEvent - Forked repository
- And 10+ more event types

## Requirements

- Python 3.8+
- `requests` library (installed automatically)

## License

MIT

## Credits

This project is based on the [GitHub User Activity](https://roadmap.sh/projects/github-user-activity) project from [roadmap.sh](https://roadmap.sh).

The original project specification includes:
- Fetching user events from GitHub API
- Displaying activity in human-readable format
- Adding optional filtering and caching features

## Author

Radionov Roland