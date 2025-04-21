# GradeLib Usage Examples

This document provides comprehensive examples of how to use the GradeLib library for analyzing GitHub repositories. GradeLib is a high-performance library built with Rust and Python bindings, designed to facilitate repository analysis for grading and assessment purposes.

## Table of Contents

- [GradeLib Usage Examples](#gradelib-usage-examples)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
  - [Repository Management](#repository-management)
    - [Creating a RepoManager](#creating-a-repomanager)
    - [Cloning Repositories](#cloning-repositories)
    - [Monitoring Clone Status](#monitoring-clone-status)
  - [Repository Analysis](#repository-analysis)
    - [Commit Analysis](#commit-analysis)
    - [Blame Analysis](#blame-analysis)
    - [Branch Analysis](#branch-analysis)
    - [Collaborator Analysis](#collaborator-analysis)
    - [Pull Request Analysis](#pull-request-analysis)
    - [Issues Analysis](#issues-analysis)
  - [Advanced Usage](#advanced-usage)
    - [Parallel Processing](#parallel-processing)
    - [Error Handling](#error-handling)
  - [Full Example](#full-example)
- [Taiga Provider for gradelib](#taiga-provider-for-gradelib)
  - [Features](#features)
  - [Authentication](#authentication)
    - [Getting a Taiga Authentication Token](#getting-a-taiga-authentication-token)
      - [Option 1: Using the API (Recommended)](#option-1-using-the-api-recommended)
      - [Option 2: Using the Taiga Web Interface](#option-2-using-the-taiga-web-interface)
      - [Using cURL](#using-curl)
  - [Example Usage](#example-usage)
    - [Basic Usage](#basic-usage)
    - [Running the Example Script](#running-the-example-script)
  - [Data Structure](#data-structure)
  - [Dependencies](#dependencies)
  - [License](#license)
  - [This project is subject to the same license as the gradelib library.](#this-project-is-subject-to-the-same-license-as-the-gradelib-library)

---

## Setup

Before using GradeLib, ensure you have the necessary environment set up:

```python
import asyncio
import os
from gradelib.gradelib import setup_async, RepoManager

# Initialize the async runtime environment
setup_async()

# Set GitHub credentials (preferably from environment variables for security)
github_username = os.environ.get("GITHUB_USERNAME", "your_username")
github_token = os.environ.get("GITHUB_TOKEN", "your_personal_access_token")

# List of repositories to analyze
repo_urls = [
    "https://github.com/username/repo1",
    "https://github.com/username/repo2",
]
```

## Repository Management

### Creating a RepoManager

The `RepoManager` class is the central component for repository operations:

```python
# Create a repo manager with GitHub credentials
manager = RepoManager(
    urls=repo_urls,
    github_username=github_username,
    github_token=github_token
)
```

### Cloning Repositories

You can clone all repositories or a specific repository:

```python
# Clone all repositories
await manager.clone_all()

# Clone a specific repository
await manager.clone("https://github.com/username/specific-repo")
```

### Monitoring Clone Status

Monitor the progress of cloning operations with detailed status information:

```python
async def monitor_cloning(manager, repo_urls):
    """Monitor and display detailed clone progress for repositories."""
    completed = set()
    all_done = False

    while not all_done:
        tasks = await manager.fetch_clone_tasks()
        all_done = True  # Assume all are done until we find one that isn't

        for url in repo_urls:
            if url in tasks:
                task = tasks[url]
                status = task.status

                # Skip repositories we've already reported as complete
                if url in completed:
                    continue

                # Check status and provide appropriate information
                if status.status_type == "queued":
                    print(f"\r⏱️ {url}: Queued for cloning", end='', flush=True)
                    all_done = False

                elif status.status_type == "cloning":
                    all_done = False
                    progress = status.progress or 0
                    bar_length = 30
                    filled_length = int(bar_length * progress / 100)
                    bar = '█' * filled_length + '░' * (bar_length - filled_length)
                    print(f"\r⏳ {url}: [{bar}] {progress}%", end='', flush=True)

                elif status.status_type == "completed":
                    # Show details about the completed repository
                    print(f"\n✅ {url}: Clone completed successfully")
                    if task.temp_dir:
                        print(f"   📁 Local path: {task.temp_dir}")
                    completed.add(url)

                elif status.status_type == "failed":
                    # Show error details
                    print(f"\n❌ {url}: Clone failed")
                    if status.error:
                        print(f"   ⚠️ Error: {status.error}")
                    completed.add(url)

        if not all_done:
            await asyncio.sleep(0.5)  # Poll every half-second

    print("\nAll repository operations completed.")

# Usage
await monitor_cloning(manager, repo_urls)
```

This monitoring function provides complete details about:
- Queue status
- Cloning progress with visual progress bar
- Local paths for completed clones
- Detailed error information for failed operations

## Repository Analysis

### Commit Analysis

Analyze the commit history of a repository:

```python
# Analyze commits for a specific repository
commit_history = await manager.analyze_commits("https://github.com/username/repo")

# Process the commit data
for commit in commit_history:
    # Each commit is a dictionary with detailed information
    print(f"Commit: {commit['sha'][:8]}")
    print(f"Author: {commit['author_name']} <{commit['author_email']}>")
    print(f"Date: {commit['author_timestamp']}") # Unix timestamp
    print(f"Message: {commit['message']}")
    print(f"Changes: +{commit['additions']} -{commit['deletions']}")
    print(f"Is Merge: {commit['is_merge']}")
    print("---")

# Convert to pandas DataFrame for analysis
import pandas as pd
df = pd.DataFrame(commit_history)

# Example analysis: Most active contributors
author_counts = df['author_name'].value_counts()
print("Most active contributors:")
print(author_counts.head())

# Example analysis: Commit activity over time
df['date'] = pd.to_datetime(df['author_timestamp'], unit='s')
activity = df.set_index('date').resample('D').size()
print("Commit activity by day:")
print(activity)
```

### Blame Analysis

Perform Git blame on specific files to see who wrote each line:

```python
# Define the repository and files to blame
target_repo = "https://github.com/username/repo"
file_paths = [
    "src/main.py",
    "src/utils.py",
    "README.md"
]

# Perform blame analysis
blame_results = await manager.bulk_blame(target_repo, file_paths)

# Process the blame results
for file_path, result in blame_results.items():
    print(f"\nFile: {file_path}")

    if isinstance(result, str):
        # If result is a string, it's an error message
        print(f"Error: {result}")
        continue

    # Result is a list of line info dictionaries
    print(f"Lines analyzed: {len(result)}")

    # Group by author
    authors = {}
    for line in result:
        author = line['author_name']
        if author not in authors:
            authors[author] = 0
        authors[author] += 1

    # Print author contribution
    print("Author contribution:")
    for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(result)) * 100
        print(f"{author}: {count} lines ({percentage:.1f}%)")
```

### Branch Analysis

Analyze branch information for multiple repositories:

```python
# Analyze branches for repositories
branches = await manager.analyze_branches(repo_urls)

# Process the branch information
for repo_url, repo_branches in branches.items():
    if isinstance(repo_branches, str):
        # This is an error message
        print(f"Error analyzing branches for {repo_url}: {repo_branches}")
        continue

    print(f"\nRepository: {repo_url}")
    print(f"Found {len(repo_branches)} branches")

    # Count local vs remote branches
    local_branches = [b for b in repo_branches if not b['is_remote']]
    remote_branches = [b for b in repo_branches if b['is_remote']]
    print(f"Local branches: {len(local_branches)}")
    print(f"Remote branches: {len(remote_branches)}")

    # Find the default branch (usually HEAD)
    head_branches = [b for b in repo_branches if b['is_head']]
    if head_branches:
        print(f"Default branch: {head_branches[0]['name']}")

    # Get the most recent branches by commit time
    branches_by_time = sorted(repo_branches, key=lambda b: b['author_time'], reverse=True)
    print("\nMost recently updated branches:")
    for branch in branches_by_time[:5]:  # Top 5
        print(f"  - {branch['name']} (Last commit: {branch['commit_message'].split('\n')[0]})")
```

### Collaborator Analysis

Fetch and analyze collaborators information for repositories:

```python
# Fetch collaborator information
collaborators = await manager.fetch_collaborators(repo_urls)

# Process collaborator data
for repo_url, repo_collaborators in collaborators.items():
    print(f"\nRepository: {repo_url}")
    print(f"Found {len(repo_collaborators)} collaborators")

    # Print collaborator information
    for collab in repo_collaborators:
        print(f"  - {collab['login']}")

        # Display additional information if available
        if collab.get('full_name'):
            print(f"    Name: {collab['full_name']}")

        if collab.get('email'):
            print(f"    Email: {collab['email']}")

# Convert to pandas DataFrame for analysis
import pandas as pd

all_collaborators = []
for repo_url, repo_collaborators in collaborators.items():
    repo_name = '/'.join(repo_url.split('/')[-2:])

    for collab in repo_collaborators:
        collab_data = {
            'Repository': repo_name,
            'Login': collab['login'],
            'GitHub ID': collab['github_id'],
            'Name': collab.get('full_name', 'N/A'),
            'Email': collab.get('email', 'N/A'),
        }
        all_collaborators.append(collab_data)

# Create DataFrame
df = pd.DataFrame(all_collaborators)
print("\nCollaborator DataFrame:")
print(df)
```

### Pull Request Analysis

Fetch and analyze pull requests from repositories:

```python
# Fetch pull request information (default: all states - open, closed, merged)
pull_requests = await manager.fetch_pull_requests(repo_urls)

# Optionally specify state to fetch only certain pull requests
open_prs = await manager.fetch_pull_requests(repo_urls, state="open")
closed_prs = await manager.fetch_pull_requests(repo_urls, state="closed")

# Process pull request data
for repo_url, repo_prs in pull_requests.items():
    if isinstance(repo_prs, str):
        # This is an error message
        print(f"Error fetching pull requests for {repo_url}: {repo_prs}")
        continue

    print(f"\nRepository: {repo_url}")
    print(f"Found {len(repo_prs)} pull requests")

    # Count by state
    open_count = sum(1 for pr in repo_prs if pr['state'] == 'open')
    closed_count = sum(1 for pr in repo_prs if pr['state'] == 'closed')
    merged_count = sum(1 for pr in repo_prs if pr['merged'])
    draft_count = sum(1 for pr in repo_prs if pr['is_draft'])

    print(f"Open: {open_count}, Closed: {closed_count}, Merged: {merged_count}, Draft: {draft_count}")

    # Find the most active PR authors
    authors = {}
    for pr in repo_prs:
        author = pr['user_login']
        if author not in authors:
            authors[author] = 0
        authors[author] += 1

    print("\nMost active PR authors:")
    for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  - {author}: {count} PRs")

    # Show the most recent PRs
    recent_prs = sorted(repo_prs, key=lambda pr: pr['updated_at'], reverse=True)
    print("\nMost recently updated PRs:")
    for pr in recent_prs[:5]:
        print(f"  - #{pr['number']} {pr['title']} ({pr['state']})")
        print(f"    Updated: {pr['updated_at']}")
        print(f"    Author: {pr['user_login']}")
        print(f"    Changes: +{pr['additions']} -{pr['deletions']} in {pr['changed_files']} files")

# Convert to pandas DataFrame for analysis
import pandas as pd

all_prs = []
for repo_url, repo_prs in pull_requests.items():
    if isinstance(repo_prs, str):
        continue

    repo_name = '/'.join(repo_url.split('/')[-2:])

    for pr in repo_prs:
        # Extract common properties for analysis
        pr_data = {
            'Repository': repo_name,
            'Number': pr['number'],
            'Title': pr['title'],
            'State': pr['state'],
            'Author': pr['user_login'],
            'Created': pr['created_at'],
            'Updated': pr['updated_at'],
            'Closed': pr['closed_at'],
            'Merged': pr['merged_at'],
            'Is Merged': pr['merged'],
            'Comments': pr['comments'],
            'Commits': pr['commits'],
            'Additions': pr['additions'],
            'Deletions': pr['deletions'],
            'Changed Files': pr['changed_files'],
            'Is Draft': pr['is_draft'],
            'Labels': ', '.join(pr['labels'])
        }
        all_prs.append(pr_data)

# Create DataFrame
if all_prs:
    df = pd.DataFrame(all_prs)

    # Example analysis: PR size distribution
    df['Total Changes'] = df['Additions'] + df['Deletions']
    size_bins = [0, 10, 50, 100, 500, 1000, float('inf')]
    size_labels = ['XS (0-10)', 'S (11-50)', 'M (51-100)', 'L (101-500)', 'XL (501-1000)', 'XXL (1000+)']
    df['Size'] = pd.cut(df['Total Changes'], bins=size_bins, labels=size_labels)

    print("\nPR Size Distribution:")
    print(df['Size'].value_counts())

    # Example analysis: Average time to merge
    df['Created Date'] = pd.to_datetime(df['Created'])
    df['Merged Date'] = pd.to_datetime(df['Merged'])
    merged_prs = df[df['Is Merged'] == True].copy()
    if not merged_prs.empty:
        merged_prs['Days to Merge'] = (merged_prs['Merged Date'] - merged_prs['Created Date']).dt.total_seconds() / (60*60*24)
        print("\nAverage Days to Merge:", merged_prs['Days to Merge'].mean())
        print("Median Days to Merge:", merged_prs['Days to Merge'].median())
```

### Issues Analysis

Fetch and analyze GitHub issues from repositories:

```python
# Fetch issue information (default: all states - open, closed)
issues = await manager.fetch_issues(repo_urls)

# Optionally specify state to fetch only certain issues
open_issues = await manager.fetch_issues(repo_urls, state="open")
closed_issues = await manager.fetch_issues(repo_urls, state="closed")

# Process issue data
for repo_url, repo_result in issues.items():
    if isinstance(repo_result, str):
        # This is an error message
        print(f"Error fetching issues for {repo_url}: {repo_result}")
        continue

    print(f"\nRepository: {repo_url}")

    # Separate issues from pull requests (GitHub API returns both under issues endpoint)
    actual_issues = [issue for issue in repo_result if not issue['is_pull_request']]
    pull_requests = [issue for issue in repo_result if issue['is_pull_request']]

    print(f"Found {len(actual_issues)} issues and {len(pull_requests)} pull requests")

    # Count by state
    open_count = sum(1 for issue in actual_issues if issue['state'] == 'open')
    closed_count = sum(1 for issue in actual_issues if issue['state'] == 'closed')

    print(f"Issues: Open: {open_count}, Closed: {closed_count}")

    # Find the most common labels
    label_counts = {}
    for issue in actual_issues:
        for label in issue['labels']:
            if label not in label_counts:
                label_counts[label] = 0
            label_counts[label] += 1

    if label_counts:
        print("\nMost common labels:")
        for label, count in sorted(label_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  - {label}: {count} issues")

    # Show the most recent issues
    recent_issues = sorted(actual_issues, key=lambda i: i['updated_at'], reverse=True)
    print("\nMost recently updated issues:")
    for issue in recent_issues[:5]:
        print(f"  - #{issue['number']} {issue['title']} ({issue['state']})")
        print(f"    Updated: {issue['updated_at']}")
        print(f"    Author: {issue['user_login']}")
        print(f"    Comments: {issue['comments_count']}")

# Convert to pandas DataFrame for analysis
import pandas as pd
from datetime import datetime

all_issues = []
for repo_url, repo_result in issues.items():
    if isinstance(repo_result, str):
        continue

    repo_name = '/'.join(repo_url.split('/')[-2:])

    # Process only actual issues (not PRs)
    actual_issues = [issue for issue in repo_result if not issue['is_pull_request']]

    for issue in actual_issues:
        # Convert string dates to datetime objects
        created_at = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
        updated_at = datetime.fromisoformat(issue['updated_at'].replace('Z', '+00:00'))

        closed_at = None
        if issue['closed_at']:
            closed_at = datetime.fromisoformat(issue['closed_at'].replace('Z', '+00:00'))

        # Extract common properties for analysis
        issue_data = {
            'Repository': repo_name,
            'Number': issue['number'],
            'Title': issue['title'],
            'State': issue['state'],
            'Author': issue['user_login'],
            'Created': created_at,
            'Updated': updated_at,
            'Closed': closed_at,
            'Comments': issue['comments_count'],
            'Labels': ', '.join(issue['labels']) if issue['labels'] else '',
            'Assignees': ', '.join(issue['assignees']) if issue['assignees'] else '',
            'Milestone': issue['milestone'] if issue['milestone'] else '',
        }
        all_issues.append(issue_data)

# Create DataFrame
if all_issues:
    df = pd.DataFrame(all_issues)

    # Example analysis: Issue resolution time
    df['Created Date'] = pd.to_datetime(df['Created'])
    df['Closed Date'] = pd.to_datetime(df['Closed'])
    closed_issues = df[df['State'] == 'closed'].copy()
    if not closed_issues.empty:
        closed_issues['Days to Close'] = (closed_issues['Closed Date'] - closed_issues['Created Date']).dt.total_seconds() / (60*60*24)
        print("\nIssue Resolution Time:")
        print(f"Average Days to Close: {closed_issues['Days to Close'].mean():.2f}")
        print(f"Median Days to Close: {closed_issues['Days to Close'].median():.2f}")

    # Example analysis: Most productive issue resolvers
    if not closed_issues.empty and 'Assignees' in closed_issues.columns:
        # This is a simplified analysis since we only have comma-separated assignee names
        assignee_counts = {}
        for _, issue in closed_issues.iterrows():
            if issue['Assignees']:
                for assignee in issue['Assignees'].split(', '):
                    if assignee not in assignee_counts:
                        assignee_counts[assignee] = 0
                    assignee_counts[assignee] += 1

        if assignee_counts:
            print("\nMost Productive Issue Resolvers:")
            for assignee, count in sorted(assignee_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  - {assignee}: {count} issues closed")
```

## Advanced Usage

### Parallel Processing

GradeLib uses parallel processing for performance-intensive operations:

- `analyze_commits`: Uses Rayon for parallel commit analysis
- `bulk_blame`: Processes multiple files in parallel with Tokio tasks
- `analyze_branches`: Uses Rayon for parallel branch extraction
- `fetch_collaborators`: Fetches collaborator data concurrently
- `fetch_pull_requests`: Fetches pull request data concurrently

These operations automatically benefit from parallelism without additional configuration.

### Error Handling

GradeLib provides structured error handling. Here's an example of robust error handling:

```python
async def run_with_error_handling():
    try:
        # Try to analyze commits
        commits = await manager.analyze_commits("https://github.com/username/repo")
        print(f"Successfully analyzed {len(commits)} commits")
    except ValueError as e:
        # ValueErrors are raised for application-specific errors
        print(f"Application error: {e}")
    except Exception as e:
        # Other exceptions are unexpected errors
        print(f"Unexpected error: {e}")

    # For methods that return errors as strings instead of raising exceptions
    branches = await manager.analyze_branches(repo_urls)
    for repo_url, result in branches.items():
        if isinstance(result, str):
            print(f"Error analyzing branches for {repo_url}: {result}")
        else:
            print(f"Successfully analyzed {len(result)} branches for {repo_url}")

# Run the function
await run_with_error_handling()
```

---

## Full Example

Here's a complete example putting everything together:

```python
import asyncio
import os
import pandas as pd
from gradelib.gradelib import setup_async, RepoManager

async def analyze_repositories(repo_urls, github_username, github_token):
    # Initialize async runtime
    setup_async()

    # Create repo manager
    manager = RepoManager(repo_urls, github_username, github_token)

    # Clone repositories
    print("Cloning repositories...")
    await manager.clone_all()

    # Monitor cloning progress with detailed information
    completed = set()
    all_done = False
    while not all_done:
        tasks = await manager.fetch_clone_tasks()
        all_done = True

        for url in repo_urls:
            if url in tasks and url not in completed:
                task = tasks[url]
                status = task.status

                if status.status_type == "queued":
                    print(f"\r⏱️ {url}: Queued for cloning", end='', flush=True)
                    all_done = False

                elif status.status_type == "cloning":
                    all_done = False
                    progress = status.progress or 0
                    bar_length = 30
                    filled_length = int(bar_length * progress / 100)
                    bar = '█' * filled_length + '░' * (bar_length - filled_length)
                    print(f"\r⏳ {url}: [{bar}] {progress}%", end='', flush=True)

                elif status.status_type == "completed":
                    print(f"\n✅ {url}: Clone completed successfully")
                    if task.temp_dir:
                        print(f"   📁 Local path: {task.temp_dir}")
                    completed.add(url)

                elif status.status_type == "failed":
                    print(f"\n❌ {url}: Clone failed")
                    if status.error:
                        print(f"   ⚠️ Error: {status.error}")
                    completed.add(url)

        if not all_done:
            await asyncio.sleep(0.5)

    print("\nAll repository operations completed.")

    # Analyze commits
    print("\nAnalyzing commits...")
    all_commits = {}
    for url in repo_urls:
        try:
            commits = await manager.analyze_commits(url)
            all_commits[url] = commits
            print(f"Found {len(commits)} commits in {url}")
        except Exception as e:
            print(f"Error analyzing commits for {url}: {e}")

    # Analyze branches
    print("\nAnalyzing branches...")
    branches = await manager.analyze_branches(repo_urls)
    for url, branch_data in branches.items():
        if isinstance(branch_data, str):
            print(f"Error analyzing branches for {url}: {branch_data}")
        else:
            print(f"Found {len(branch_data)} branches in {url}")

    # Fetch collaborators
    print("\nFetching collaborators...")
    collaborators = await manager.fetch_collaborators(repo_urls)
    for url, collab_data in collaborators.items():
        if isinstance(collab_data, str):
            print(f"Error fetching collaborators for {url}: {collab_data}")
        else:
            print(f"Found {len(collab_data)} collaborators in {url}")

    # Fetch pull requests
    print("\nFetching pull requests...")
    pull_requests = await manager.fetch_pull_requests(repo_urls)
    for url, pr_data in pull_requests.items():
        if isinstance(pr_data, str):
            print(f"Error fetching pull requests for {url}: {pr_data}")
        else:
            print(f"Found {len(pr_data)} pull requests in {url}")

    # Fetch issues
    print("\nFetching issues...")
    issues = await manager.fetch_issues(repo_urls)
    for url, issue_data in issues.items():
        if isinstance(issue_data, str):
            print(f"Error fetching issues for {url}: {issue_data}")
        else:
            # Count actual issues (not PRs)
            actual_issues = [issue for issue in issue_data if not issue['is_pull_request']]
            print(f"Found {len(actual_issues)} issues in {url}")

    # Return all collected data
    return {
        "commits": all_commits,
        "branches": branches,
        "collaborators": collaborators,
        "pull_requests": pull_requests,
        "issues": issues
    }

# Run the analysis
if __name__ == "__main__":
    # Get GitHub credentials
    github_username = os.environ.get("GITHUB_USERNAME")
    github_token = os.environ.get("GITHUB_TOKEN")

    if not github_username or not github_token:
        print("Please set GITHUB_USERNAME and GITHUB_TOKEN environment variables")
        exit(1)

    # List of repositories to analyze
    repos = [
        "https://github.com/bmeddeb/gradelib",
        "https://github.com/PyO3/pyo3"
    ]

    # Run async analysis
    results = asyncio.run(analyze_repositories(repos, github_username, github_token))

    # Print summary
    print("\n===== ANALYSIS SUMMARY =====")
    for repo in repos:
        repo_name = repo.split('/')[-1]
        print(f"\nRepository: {repo_name}")

        # Commit stats
        if repo in results["commits"]:
            commits = results["commits"][repo]
            authors = set(c["author_name"] for c in commits)
            print(f"Total commits: {len(commits)}")
            print(f"Unique authors: {len(authors)}")

            # Find most recent commit
            if commits:
                recent = max(commits, key=lambda c: c["author_timestamp"])
                print(f"Most recent commit: {recent['message'].split('\n')[0]}")

        # Branch stats
        if repo in results["branches"] and isinstance(results["branches"][repo], list):
            branches = results["branches"][repo]
            local = sum(1 for b in branches if not b["is_remote"])
            remote = sum(1 for b in branches if b["is_remote"])
            print(f"Branches: {len(branches)} (Local: {local}, Remote: {remote})")

        # Collaborator stats
        if repo in results["collaborators"] and isinstance(results["collaborators"][repo], list):
            collabs = results["collaborators"][repo]
            print(f"Collaborators: {len(collabs)}")

        # Pull request stats
        if repo in results["pull_requests"] and isinstance(results["pull_requests"][repo], list):
            prs = results["pull_requests"][repo]
            open_prs = sum(1 for pr in prs if pr["state"] == "open")
            merged_prs = sum(1 for pr in prs if pr["merged"])
            print(f"Pull requests: {len(prs)} (Open: {open_prs}, Merged: {merged_prs})")

        # Issue stats
        if repo in results["issues"] and isinstance(results["issues"][repo], list):
            all_issues = results["issues"][repo]
            # Count actual issues (not PRs)
            actual_issues = [issue for issue in all_issues if not issue["is_pull_request"]]
            open_issues = sum(1 for issue in actual_issues if issue["state"] == "open")
            closed_issues = sum(1 for issue in actual_issues if issue["state"] == "closed")
            print(f"Issues: {len(actual_issues)} (Open: {open_issues}, Closed: {closed_issues})")
```
# Taiga Provider for gradelib

This README provides instructions for using the Taiga provider in the gradelib Python library. The Taiga provider enables you to fetch data from Taiga projects asynchronously and efficiently using Rust's performance benefits.

## Features

- Fetch comprehensive project data including:
  - Project details
  - Project members
  - Sprints/milestones (both open and closed)
  - User stories
  - Tasks
  - Task history
- Concurrent fetching for multiple projects
- Efficient async implementation with Tokio

## Authentication

To use the Taiga API, you need:

1. A Taiga account with access to the projects you want to fetch
2. An authentication token from Taiga

### Getting a Taiga Authentication Token

There are two ways to obtain a Taiga authentication token:

#### Option 1: Using the API (Recommended)

The most reliable way is to authenticate directly with the Taiga API using your username and password. Here's a Python function to help with that:

```python
async def get_auth_token(url, username, password):
    """Gets an authentication token from Taiga."""
    import aiohttp

    auth_url = f"{url.rstrip('/')}/auth"
    payload = {
        "type": "normal",
        "username": username,
        "password": password
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(auth_url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("auth_token")
            else:
                text = await response.text()
                raise Exception(f"Failed to get auth token: {response.status} - {text}")
```

You can use this function like this:

```python
token = await get_auth_token("https://api.taiga.io/api/v1/", "your_username", "your_password")
```

The response will contain the `auth_token` that you can use for subsequent API calls.

#### Option 2: Using the Taiga Web Interface

Alternatively, you can extract the token from the web interface:

1. Log into your Taiga account in a web browser
2. Open your browser's developer tools (F12 or Ctrl+Shift+I)
3. Go to the Network tab and filter for XHR/Fetch requests
4. Reload the page or perform an action that triggers an API call
5. Look for requests to the Taiga API and examine their headers
6. Find the `Authorization` header that contains `Bearer YOUR_TOKEN`
7. The token is the string after `Bearer `

#### Using cURL

You can also use cURL to get a token:

```bash
curl -X POST \
  https://api.taiga.io/api/v1/auth \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "normal",
    "username": "your_username",
    "password": "your_password"
}'
```

## Example Usage

### Basic Usage

```python
import asyncio
import aiohttp
from gradelib import TaigaClient

async def get_auth_token(url, username, password):
    """Gets an authentication token from Taiga."""
    auth_url = f"{url.rstrip('/')}/auth"
    payload = {
        "type": "normal",
        "username": username,
        "password": password
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(auth_url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("auth_token")
            else:
                text = await response.text()
                raise Exception(f"Failed to get auth token: {response.status} - {text}")

async def fetch_project():
    # Authenticate and get token
    token = await get_auth_token(
        "https://api.taiga.io/api/v1/",
        "your_username",
        "your_password"
    )

    # Create a client
    client = TaigaClient(
        base_url="https://api.taiga.io/api/v1/",
        auth_token=token,
        username="your_username"
    )

    # Fetch a single project
    project_data = await client.fetch_project_data("project-slug")

    # Access the data
    print(f"Project: {project_data['project']['name']}")
    print(f"Members: {len(project_data['members'])}")
    print(f"Sprints: {len(project_data['sprints'])}")

    # Fetch multiple projects concurrently
    results = await client.fetch_multiple_projects(["project1", "project2"])

    for slug, result in results.items():
        if result is True:
            print(f"{slug}: Successfully fetched")
        else:
            print(f"{slug}: {result}")

# Run the async function
asyncio.run(fetch_project())
```

### Running the Example Script

The repository includes an example script in `examples/taiga_example.py` that demonstrates all features of the Taiga provider. The script also includes a diagnostic function to check if the Taiga provider is properly installed in your environment.

To run it:

1. Set your Taiga credentials as environment variables:

```bash
export TAIGA_URL="https://api.taiga.io/api/v1/"
export TAIGA_USERNAME="your_taiga_username"
export TAIGA_PASSWORD="your_taiga_password"
```

Or, if you already have a token:

```bash
export TAIGA_URL="https://api.taiga.io/api/v1/"
export TAIGA_TOKEN="your_taiga_auth_token"
export TAIGA_USERNAME="your_taiga_username"
```

2. Run the example script:

```bash
python examples/taiga_example.py
```

Alternatively, you can edit the script and directly set your credentials in the code.

## Data Structure

The `fetch_project_data` method returns a dictionary with the following structure:

```
{
  "project": {
    "id": 123,
    "name": "Project Name",
    "slug": "project-slug",
    "description": "Project description",
    "created_date": "2023-01-01T00:00:00.000Z",
    "modified_date": "2023-01-02T00:00:00.000Z"
  },
  "members": [
    {
      "id": 456,
      "user": 789,
      "role": 1,
      "role_name": "Product Owner",
      "full_name": "John Doe"
    },
    ...
  ],
  "sprints": [
    {
      "id": 101,
      "name": "Sprint 1",
      "estimated_start": "2023-01-15",
      "estimated_finish": "2023-01-31",
      "created_date": "2023-01-10T00:00:00.000Z",
      "closed": false
    },
    ...
  ],
  "user_stories": {
    "101": [  # Sprint ID
      {
        "id": 201,
        "reference": 1,
        "subject": "User Story 1",
        "status": "In progress"
      },
      ...
    ],
    ...
  },
  "tasks": {
    "101": [  # Sprint ID
      {
        "id": 301,
        "reference": 1,
        "subject": "Task 1",
        "is_closed": false,
        "assigned_to": 789
      },
      ...
    ],
    ...
  },
  "task_histories": {
    "301": [  # Task ID
      {
        "id": 401,
        "created_at": "2023-01-20T00:00:00.000Z",
        "event_type": 1
      },
      ...
    ],
    ...
  }
}
```

## Dependencies

To run the example code with authentication, you need:

- Python 3.7+
- aiohttp (`pip install aiohttp`)
- gradelib (your Rust-based library)

## License

This project is subject to the same license as the gradelib library.
---

*This document is a living resource and will be updated as new functionality is added to GradeLib.*
