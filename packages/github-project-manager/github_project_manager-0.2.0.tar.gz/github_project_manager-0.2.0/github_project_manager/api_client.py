from typing import Any, Optional
import requests
import logging

logger = logging.getLogger("ghpm.api")


class GitHubAPIClient:
    """Handles HTTP communication with GitHub API."""

    def __init__(self, token: str, org: str):
        self.token = token
        self.org = org
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        }
        self.graphql_url = "https://api.github.com/graphql"
        self.rest_url = "https://api.github.com"

    def graphql_query(self, query: str, variables: Optional[dict] = None) -> dict:
        """Execute a GraphQL query against GitHub API."""
        try:
            response = requests.post(
                self.graphql_url,
                json={"query": query, "variables": variables},
                headers=self.headers,
            )
            response.raise_for_status()
            result = response.json()

            if "errors" in result:
                error_message = ", ".join(
                    [e.get("message", "Unknown error") for e in result["errors"]]
                )
                raise RuntimeError(f"GraphQL error: {error_message}")

            return result["data"]
        except requests.RequestException as e:
            logger.error(f"GraphQL request failed: {str(e)}")
            raise

    def rest_request(self, method: str, path: str, data: Optional[dict] = None) -> Any:
        """Make a REST API request to GitHub."""
        url = f"{self.rest_url}{path}"
        try:
            response = getattr(requests, method.lower())(
                url, json=data, headers=self.headers
            )
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.RequestException as e:
            logger.error(f"REST request failed: {method} {path} - {str(e)}")
            raise
