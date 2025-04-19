# GitHub Project Manager

[![Tests](https://github.com/ezrahill/github-project-manager/actions/workflows/tests.yml/badge.svg)](https://github.com/ezrahill/github-project-manager/actions/workflows/tests.yml)
[![PyPI version](https://badge.fury.io/py/github-project-manager.svg)](https://badge.fury.io/py/github-project-manager)
[![Python Versions](https://img.shields.io/pypi/pyversions/github-project-manager.svg)](https://pypi.org/project/github-project-manager/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/ezrahill/github-project-manager/branch/main/graph/badge.svg)](https://codecov.io/gh/ezrahill/github-project-manager)

A Python library for managing GitHub Projects (v2), issues, labels, and milestones.

## Features

- Create and manage GitHub Projects (v2)
- Add issues to projects
- Automatically update issue descriptions when they change
- Manage project fields and status options
- Create and update labels across multiple repositories
- Create and update milestones across multiple repositories

## Installation

```bash
pip install github-project-manager
```

## Requirements

This library depends on:
- Python 3.10+
- requests >= 2.25.0
- python-dotenv >= 0.15.0

## Configuration

You need to set the following environment variables:

- `GITHUB_TOKEN`: Your GitHub personal access token with appropriate permissions
- `GITHUB_ORG`: Your GitHub organization name

You can also use a `.env` file:

```
GITHUB_TOKEN=your_github_token
GITHUB_ORG=your_org_name
```

## Usage Examples

### Initialize the Manager

```python
from github_project_manager import GitHubProjectManager

# Initialize the manager
manager = GitHubProjectManager()

# Initialize with an existing project
manager = GitHubProjectManager("My Existing Project")

# If you need to change the logging level
import logging
logging.getLogger("ghpm").setLevel(logging.DEBUG)
```

### Create a Project and Add Issues

```python
# Create a new project (or use an existing one with the same name)
project_id = manager.create_project("My Project")

# Create an issue (or use an existing one with the same title)
# Method 1: Create issue and add to project separately
issue_node_id = manager.create_issue("my-repo", "Issue Title", "Issue description")
manager.add_issue_to_project(issue_node_id)

# Method 2: Create issue and add to project in one step
issue_node_id = manager.create_issue(
    "my-repo",
    "Issue Title",
    "Issue description",
    add_to_project=True
)

# Method 3: Create issue with labels
issue_node_id = manager.create_issue(
    "my-repo",
    "Issue Title",
    "Issue description",
    add_to_project=True,
    labels=["bug", "high-priority"]
)
```

### Automatic Issue Description Updates

The library will automatically update the description of an existing issue if it has changed:

```python
# If an issue with this title already exists but with a different description,
# the description will be updated automatically
issue_node_id = manager.create_issue(
    "my-repo",
    "Existing Issue Title",
    "Updated description"
)
```

### Manage Project Status Options

```python
from github_project_manager import StatusOption

# Define status options
status_options = [
    StatusOption("To Do", "RED"),
    StatusOption("In Progress", "YELLOW"),
    StatusOption("Done", "GREEN", "Completed work"),
]

# Update the project's status field
manager.update_status_options(status_options)

# Replace all existing options with new ones
manager.update_status_options(status_options, preserve_existing=False)
```

### Manage Labels Across Repositories

```python
from github_project_manager import IssueLabel

# Create a single label
label = IssueLabel("bug", "FF0000", "Something isn't working")

# Create in a single repository
manager.create_labels("my-repo", label)

# Create in multiple repositories
manager.create_labels(["repo1", "repo2"], label)

# Create multiple labels in multiple repositories
labels = [
    IssueLabel("bug", "FF0000", "Something isn't working"),
    IssueLabel("enhancement", "0000FF", "New feature or request"),
]
manager.create_labels(["repo1", "repo2"], labels)
```

### Manage Milestones Across Repositories

```python
from github_project_manager import IssueMilestone

# Create a milestone with a due date
milestone = IssueMilestone(
    "v1.0",
    "First stable release",
    "2023-12-31T23:59:59Z"
)

# Create in multiple repositories
manager.create_milestones(
    ["repo1", "repo2"],
    milestone
)
```

## License

MIT

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to set up the development environment, run tests, and submit contributions.
