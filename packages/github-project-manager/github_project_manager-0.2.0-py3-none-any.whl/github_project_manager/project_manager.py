from collections.abc import Iterable
import os
import logging
from typing import Any, Optional, Union

from dotenv import load_dotenv

from .api_client import GitHubAPIClient
from .models import StatusOption, IssueLabel, IssueMilestone

# Load environment variables
load_dotenv()

# Set up logger with shorter namespace
logger = logging.getLogger("ghpm")


class GitHubProjectManager:
    """
    Manages GitHub Projects (v2), issues, labels, and milestones for GitHub repositories.

    This class provides functionality to:
    - Create and manage GitHub Projects (v2)
    - Add and configure project fields
    - Create and update issues
    - Manage labels and milestones across repositories
    """

    def __init__(self, project_name: Optional[str] = None):
        self.token = os.getenv("GITHUB_TOKEN")
        self.org = os.getenv("GITHUB_ORG")
        if not self.token or not self.org:
            raise ValueError(
                "GITHUB_TOKEN and GITHUB_ORG environment variables must be set"
            )

        self.api = GitHubAPIClient(self.token, self.org)
        self.project_id = None
        self.project_name = project_name

        if project_name:
            if not self.project_exists(project_name):
                raise ValueError(f"Project '{project_name}' does not exist")

    def _lower_names(self, items: Iterable) -> set[str]:
        """Helper: set of names (case‑insensitive) for any items with a name attribute."""
        return {o.name.lower() for o in items}

    def get_org_id(self) -> str:
        """Get the GitHub organization node ID."""
        query = """
        query($login: String!) {
          organization(login: $login) {
            id
          }
        }
        """
        result = self.api.graphql_query(query, {"login": self.org})
        return result["organization"]["id"]

    def project_exists(self, title: str) -> bool:
        """Check if a project exists and set project_id if found."""
        query = """
        query($login: String!) {
          organization(login: $login) {
            projectsV2(first: 100) {
              nodes {
                title
                id
              }
            }
          }
        }
        """
        result = self.api.graphql_query(query, {"login": self.org})
        for project in result["organization"]["projectsV2"]["nodes"]:
            if project["title"].lower() == title.lower():
                self.project_id = project["id"]
                return True
        return False

    def create_project(self, title: str) -> str:
        """Create a new GitHub project or use existing one."""
        self.project_name = title

        if self.project_exists(title):
            logger.info(f"Project '{title}' already exists. Using existing project.")
            return self.project_id

        org_id = self.get_org_id()
        mutation = """
        mutation($orgId: ID!, $title: String!) {
          createProjectV2(input: {ownerId: $orgId, title: $title}) {
            projectV2 {
              id
              title
            }
          }
        }
        """
        result = self.api.graphql_query(mutation, {"orgId": org_id, "title": title})
        self.project_id = result["createProjectV2"]["projectV2"]["id"]
        logger.info(f"Project '{title}' created with ID: {self.project_id}")
        return self.project_id

    def issue_exists(self, repo: str, title: str) -> Optional[dict]:
        """
        Check if an issue exists in a repository.

        Returns:
            Optional[dict]: Dictionary with issue data if found, None otherwise
        """
        # More efficient to search by title than to list all issues
        issues = self.api.rest_request(
            "GET", f"/repos/{self.org}/{repo}/issues?state=all&per_page=100"
        )
        for issue in issues:
            if issue["title"].strip().lower() == title.strip().lower():
                logger.info(
                    f"Issue '{title}' already exists with ID {issue['node_id']} in {repo}."
                )
                return issue
        return None

    def update_issue(self, repo: str, issue_number: int, body: str) -> None:
        """Update an issue's body/description."""
        self.api.rest_request(
            "PATCH", f"/repos/{self.org}/{repo}/issues/{issue_number}", {"body": body}
        )
        logger.info(f"Issue #{issue_number} updated in {repo}.")

    def create_issue(
        self,
        repo: str,
        title: str,
        body: str,
        add_to_project: bool = False,
        labels: Optional[list[str]] = None,
    ) -> str:
        """Create a new issue or use existing one."""
        existing_issue = self.issue_exists(repo, title)

        if existing_issue:
            # Check if body has changed
            if existing_issue["body"] != body:
                logger.info(
                    f"Issue {title} {existing_issue['node_id']} description has changed. Updating..."
                )
                self.update_issue(repo, existing_issue["number"], body)

            # Update labels if provided
            if labels:
                self.api.rest_request(
                    "PUT",
                    f"/repos/{self.org}/{repo}/issues/{existing_issue['number']}/labels",
                    {"labels": labels},
                )
                logger.info(f"Labels updated for issue '{title}' in {repo}.")

            # Add to project if requested
            if add_to_project and self.project_id:
                self.add_issue_to_project(existing_issue["node_id"])

            return existing_issue["node_id"]

        # Create new issue if not found
        issue_data = {"title": title, "body": body}
        if labels:
            issue_data["labels"] = labels

        result = self.api.rest_request(
            "POST", f"/repos/{self.org}/{repo}/issues", issue_data
        )
        logger.info(f"Issue '{title}' {result['node_id']} created in {repo}.")

        if add_to_project and self.project_id:
            self.add_issue_to_project(result["node_id"])

        return result["node_id"]

    def add_issue_to_project(self, issue_node_id: str) -> None:
        """Add an issue to the current project."""
        if not self.project_id:
            raise ValueError("Project ID not set. Call create_project() first.")

        # Check if issue is already in the project
        query = """
        query($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              items(first: 100) {
                nodes {
                  content {
                    ... on Issue {
                      id
                    }
                  }
                }
              }
            }
          }
        }
        """
        result = self.api.graphql_query(query, {"projectId": self.project_id})

        # Extract content IDs from project items
        project_items = result["node"]["items"]["nodes"]
        issue_ids = [
            item["content"]["id"]
            for item in project_items
            if item["content"] and "id" in item["content"]
        ]

        # If issue is already in project, don't add it again
        if issue_node_id in issue_ids:
            logger.info(f"Issue {issue_node_id} already in project {self.project_name}")
            return

        # Add issue to project
        mutation = """
        mutation($projectId: ID!, $contentId: ID!) {
          addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
            item {
              id
            }
          }
        }
        """
        self.api.graphql_query(
            mutation, {"projectId": self.project_id, "contentId": issue_node_id}
        )
        logger.info(f"Issue {issue_node_id} added to project {self.project_name}")

    def delete_project(self, title: str) -> None:
        """Delete a project by title."""
        if not self.project_exists(title):
            logger.info(f"No project titled '{title}' found.")
            return

        mutation = """
        mutation($projectId: ID!) {
        deleteProjectV2(input: {projectId: $projectId}) {
            clientMutationId
        }
        }
        """
        self.api.graphql_query(mutation, {"projectId": self.project_id})
        logger.info(f"Project '{title}' deleted.")
        self.project_id = None

    def update_status_options(
        self, custom_options: list[StatusOption], preserve_existing: bool = True
    ) -> Optional[str]:
        """
        Update status options for a project.

        Args:
            custom_options: List of StatusOption objects to add
            preserve_existing: Whether to keep existing options (True) or replace all (False)

        Returns:
            The field ID of the status field or None on error
        """
        if not self.project_id:
            raise ValueError("Project ID not set. Call create_project() first.")

        # Get current fields
        query = """
        query ($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              fields(first: 50) {
                nodes {
                  ... on ProjectV2SingleSelectField {
                    id
                    name
                    options { id name color description }
                  }
                }
              }
            }
          }
        }"""

        fields = self.api.graphql_query(query, {"projectId": self.project_id})
        fields = fields["node"]["fields"]["nodes"]

        # Find status field
        status = next(
            (f for f in fields if f.get("name", "").lower() == "status"),
            None,
        )

        if not status:
            logger.warning("Status field not found in project")
            return None

        # Convert existing options to StatusOption objects
        existing_opts = [StatusOption.from_dict(o) for o in status.get("options", [])]
        existing_names = self._lower_names(existing_opts)

        # Check which options are missing
        missing = [o for o in custom_options if o.name.lower() not in existing_names]

        # If preserving existing and nothing is missing, we're done
        if preserve_existing and not missing:
            logger.info("Status options already up to date")
            return status["id"]

        # Determine final list of options
        if not preserve_existing:
            final_options = custom_options
        else:
            # Create lookup of existing options by name
            existing_by_name = {o.name.lower(): o for o in existing_opts}

            # Merge existing and new options
            final_options = []
            seen_names = set()

            # Process all options (existing first, then missing)
            for option in (*existing_opts, *missing):
                name_key = option.name.lower()
                if name_key in seen_names:
                    continue

                # Use existing option details when available
                source = existing_by_name.get(name_key, option)
                final_options.append(
                    StatusOption(
                        name=option.name,  # Keep original casing
                        color=source.color,
                        description=source.description,
                    )
                )
                seen_names.add(name_key)

        # Update field options
        mutation = """
        mutation ($fieldId: ID!, $opts: [ProjectV2SingleSelectFieldOptionInput!]!) {
            updateProjectV2Field(input: {
            fieldId: $fieldId,
            singleSelectOptions: $opts
            }) { projectV2Field { ... on ProjectV2SingleSelectField { id } } }
        }"""

        opts_dicts = [o.to_dict() for o in final_options]
        self.api.graphql_query(mutation, {"fieldId": status["id"], "opts": opts_dicts})
        logger.info(f"Status options updated for project {self.project_name}")
        return status["id"]

    def _update_or_create_label(self, repo: str, label: IssueLabel) -> None:
        """Update or create a label in a repository."""
        existing_labels = self.api.rest_request(
            "GET", f"/repos/{self.org}/{repo}/labels"
        )
        for existing in existing_labels:
            if existing["name"].lower() == label.name.lower():
                # Check if update needed
                if (
                    existing["color"].lower() != label.color.lower()
                    or existing["description"] != label.description
                ):

                    # Update label
                    self.api.rest_request(
                        "PATCH",
                        f"/repos/{self.org}/{repo}/labels/{existing['name']}",
                        label.to_dict(),
                    )
                    logger.info(f"Label '{label.name}' updated in {repo}.")
                else:
                    logger.info(
                        f"Label '{label.name}' already exists in {repo} with correct properties."
                    )
                return

        # Create new label
        self.api.rest_request(
            "POST", f"/repos/{self.org}/{repo}/labels", label.to_dict()
        )
        logger.info(f"Label '{label.name}' created in {repo}.")

    def create_labels(
        self, repos: Union[str, list[str]], labels: Union[IssueLabel, list[IssueLabel]]
    ) -> None:
        """
        Create labels in one or more repositories.

        Args:
            repos: Repository name or list of repository names
            labels: IssueLabel object or list of IssueLabel objects
        """
        # Convert single items to lists
        if isinstance(repos, str):
            repos = [repos]
        if not isinstance(labels, list):
            labels = [labels]

        for repo in repos:
            for label in labels:
                self._update_or_create_label(repo, label)

    def _update_or_create_milestone(self, repo: str, milestone: IssueMilestone) -> int:
        """Update or create a milestone in a repository."""
        existing_milestones = self.api.rest_request(
            "GET", f"/repos/{self.org}/{repo}/milestones?state=all"
        )

        # Check if milestone exists
        for existing in existing_milestones:
            if existing["title"].lower() == milestone.title.lower():
                # Check if update needed
                needs_update = existing["description"] != milestone.description or (
                    milestone.due_on and existing["due_on"] != milestone.due_on
                )

                if needs_update:
                    # Update milestone
                    self.api.rest_request(
                        "PATCH",
                        f"/repos/{self.org}/{repo}/milestones/{existing['number']}",
                        milestone.to_dict(),
                    )
                    logger.info(f"Milestone '{milestone.title}' updated in {repo}")
                else:
                    logger.info(
                        f"Milestone '{milestone.title}' already exists in {repo} with correct properties"
                    )
                return existing["number"]

        # Create new milestone
        result = self.api.rest_request(
            "POST", f"/repos/{self.org}/{repo}/milestones", milestone.to_dict()
        )
        logger.info(f"Milestone '{milestone.title}' created in {repo}")
        return result["number"]

    def create_milestones(
        self,
        repos: Union[str, list[str]],
        milestones: Union[IssueMilestone, list[IssueMilestone]],
    ) -> None:
        """
        Create milestones in one or more repositories.

        Args:
            repos: Repository name or list of repository names
            milestones: IssueMilestone object or list of IssueMilestone objects
        """
        # Convert single items to lists
        if isinstance(repos, str):
            repos = [repos]
        if not isinstance(milestones, list):
            milestones = [milestones]

        for repo in repos:
            for milestone in milestones:
                self._update_or_create_milestone(repo, milestone)
