from typing import Callable

def _format_time(data: dict) -> str:
    created_at = data.get('created_at', '')
    if not created_at:
        return 'unknown time'

    date_part, time_part = created_at.split('T')
    time_part = time_part.replace('Z', '')

    return f"{date_part} {time_part[:5]}"

class EventFormatter:
    _registry = {}

    @classmethod
    def register(cls, event_type: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            cls._registry[event_type] = func
            return func
        return decorator

    @classmethod
    def format(cls, event_type: str, data: dict) -> str:
        formatter = cls._registry.get(event_type)
        if not formatter:
            print(f"[WARNING] Unknown event type: {event_type}")
            return f'Unknown event: {event_type}'
        return formatter(data)


@EventFormatter.register("PushEvent")
def handle_push(data: dict) -> str:
    size = data.get('payload', {}).get('size', 0)
    return f"[{_format_time(data)}] Pushed {size} commit(s) to {data['repo']['name']}"


@EventFormatter.register("CreateEvent")
def handle_create(data: dict) -> str:
    return f"[{_format_time(data)}] Created {data['payload']['ref_type']} {data['payload']['ref']} in {data['repo']['name']}"


@EventFormatter.register("DeleteEvent")
def handle_delete(data: dict) -> str:
    return f"[{_format_time(data)}] Deleted {data['payload']['ref_type']} {data['payload']['ref']} in {data['repo']['name']}"


@EventFormatter.register("WatchEvent")
def handle_watch(data: dict) -> str:
    return f"[{_format_time(data)}] Starred {data['repo']['name']}"


@EventFormatter.register("ForkEvent")
def handle_fork(data: dict) -> str:
    forkee = data.get('payload', {}).get('forkee', {})
    target_repo = forkee.get('full_name', 'unknown')
    return f"[{_format_time(data)}] Forked {data['repo']['name']} to {target_repo}"


@EventFormatter.register("IssuesEvent")
def handle_issues(data: dict) -> str:
    action = data['payload']['action']
    issue_number = data['payload']['issue']['number']
    return f"[{_format_time(data)}] {action.capitalize()} issue #{issue_number} in {data['repo']['name']}"


@EventFormatter.register("IssueCommentEvent")
def handle_issue_comment(data: dict) -> str:
    issue_number = data['payload']['issue']['number']
    return f"[{_format_time(data)}] Commented on issue #{issue_number} in {data['repo']['name']}"


@EventFormatter.register("PullRequestEvent")
def handle_pr(data: dict) -> str:
    action = data['payload']['action']
    pr_number = data['payload']['pull_request']['number']
    return f"[{_format_time(data)}] {action.capitalize()} PR #{pr_number} in {data['repo']['name']}"


@EventFormatter.register("PullRequestReviewEvent")
def handle_pr_review(data: dict) -> str:
    pr_number = data['payload']['pull_request']['number']
    return f"[{_format_time(data)}] Reviewed PR #{pr_number} in {data['repo']['name']}"


@EventFormatter.register("PullRequestReviewCommentEvent")
def handle_pr_review_comment(data: dict) -> str:
    return f"[{_format_time(data)}] Commented on PR review in {data['repo']['name']}"


@EventFormatter.register("CommitCommentEvent")
def handle_commit_comment(data: dict) -> str:
    return f"[{_format_time(data)}] Commented on commit in {data['repo']['name']}"


@EventFormatter.register("GollumEvent")
def handle_gollum(data: dict) -> str:
    pages = data['payload']['pages']
    if pages:
        page_name = pages[0]['page_name']
        return f"Edited the wiki page '{page_name}' in {data['repo']['name']}"
    return f"[{_format_time(data)}] Edited a wiki page in {data['repo']['name']}"


@EventFormatter.register("ReleaseEvent")
def handle_release(data: dict) -> str:
    release_name = data['payload']['release']['name']
    return f"[{_format_time(data)}] Published release '{release_name}' in {data['repo']['name']}"


@EventFormatter.register("PublicEvent")
def handle_public(data: dict) -> str:
    return f"[{_format_time(data)}] Made public {data['repo']['name']}"


@EventFormatter.register("MemberEvent")
def handle_member(data: dict) -> str:
    member_login = data['payload']['member']['login']
    return f"[{_format_time(data)}] Added user {member_login} to {data['repo']['name']}"


@EventFormatter.register("ForkApplyEvent")
def handle_fork_apply(data: dict) -> str:
    return f"[{_format_time(data)}] Applied fork to {data['repo']['name']}"


@EventFormatter.register("SponsorshipEvent")
def handle_sponsorship(data: dict) -> str:
    return f"[{_format_time(data)}] Sponsorship action in {data['repo']['name']}"


@EventFormatter.register("BranchProtectionRuleEvent")
def handle_branch_protection_rule(data: dict) -> str:
    return f"[{_format_time(data)}] Updated branch rules in {data['repo']['name']}"
