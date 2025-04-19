import unittest
from unittest.mock import patch, MagicMock
import requests
from github_project_manager.api_client import GitHubAPIClient


class TestGitHubAPIClient(unittest.TestCase):
    def setUp(self):
        self.token = "test_token"
        self.org = "test_org"
        self.client = GitHubAPIClient(self.token, self.org)

    def test_init(self):
        """Test initialization of the client."""
        self.assertEqual(self.client.token, "test_token")
        self.assertEqual(self.client.org, "test_org")
        self.assertEqual(
            self.client.headers,
            {
                "Authorization": "Bearer test_token",
                "Accept": "application/vnd.github+json",
            },
        )
        self.assertEqual(self.client.graphql_url, "https://api.github.com/graphql")
        self.assertEqual(self.client.rest_url, "https://api.github.com")

    @patch("github_project_manager.api_client.requests.post")
    def test_graphql_query_success(self, mock_post):
        """Test successful GraphQL query."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"test": "value"}}
        mock_post.return_value = mock_response

        # Call the method
        result = self.client.graphql_query("query { test }")

        # Verify
        self.assertEqual(result, {"test": "value"})
        mock_post.assert_called_once_with(
            "https://api.github.com/graphql",
            json={"query": "query { test }", "variables": None},
            headers=self.client.headers,
        )

    @patch("github_project_manager.api_client.requests.post")
    def test_graphql_query_with_variables(self, mock_post):
        """Test GraphQL query with variables."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": {"test": "value"}}
        mock_post.return_value = mock_response

        variables = {"name": "test_var"}

        # Call the method
        result = self.client.graphql_query("query($name: String!) { test }", variables)

        # Verify
        self.assertEqual(result, {"test": "value"})
        mock_post.assert_called_once_with(
            "https://api.github.com/graphql",
            json={"query": "query($name: String!) { test }", "variables": variables},
            headers=self.client.headers,
        )

    @patch("github_project_manager.api_client.requests.post")
    def test_graphql_query_with_errors(self, mock_post):
        """Test GraphQL query response with errors."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": None,
            "errors": [{"message": "Test error message"}],
        }
        mock_post.return_value = mock_response

        # Verify that exception is raised
        with self.assertRaises(RuntimeError) as context:
            self.client.graphql_query("query { test }")

        self.assertIn("GraphQL error: Test error message", str(context.exception))

    @patch("github_project_manager.api_client.requests.post")
    def test_graphql_query_request_exception(self, mock_post):
        """Test GraphQL query with request exception."""
        # Setup mock to raise an exception
        mock_post.side_effect = requests.RequestException("Connection error")

        # Verify that exception is raised
        with self.assertRaises(requests.RequestException):
            self.client.graphql_query("query { test }")

    @patch("github_project_manager.api_client.requests.get")
    def test_rest_request_get(self, mock_get):
        """Test REST GET request."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 123, "name": "test"}
        mock_response.content = b'{"id": 123, "name": "test"}'
        mock_get.return_value = mock_response

        # Call the method
        result = self.client.rest_request("GET", "/test/path")

        # Verify
        self.assertEqual(result, {"id": 123, "name": "test"})
        mock_get.assert_called_once_with(
            "https://api.github.com/test/path",
            json=None,
            headers=self.client.headers,
        )

    @patch("github_project_manager.api_client.requests.post")
    def test_rest_request_post(self, mock_post):
        """Test REST POST request with data."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 123, "name": "created"}
        mock_response.content = b'{"id": 123, "name": "created"}'
        mock_post.return_value = mock_response

        data = {"name": "test_data"}

        # Call the method
        result = self.client.rest_request("POST", "/test/create", data)

        # Verify
        self.assertEqual(result, {"id": 123, "name": "created"})
        mock_post.assert_called_once_with(
            "https://api.github.com/test/create",
            json=data,
            headers=self.client.headers,
        )

    @patch("github_project_manager.api_client.requests.put")
    def test_rest_request_empty_response(self, mock_put):
        """Test REST request with empty response."""
        # Setup mock response with empty content
        mock_response = MagicMock()
        mock_response.content = b""
        mock_put.return_value = mock_response

        # Call the method
        result = self.client.rest_request("PUT", "/test/update", {"status": "done"})

        # Verify empty dict is returned
        self.assertEqual(result, {})

    @patch("github_project_manager.api_client.requests.delete")
    def test_rest_request_exception(self, mock_delete):
        """Test REST request with exception."""
        # Setup mock to raise an exception
        mock_delete.side_effect = requests.RequestException("Connection error")

        # Verify that exception is raised
        with self.assertRaises(requests.RequestException):
            self.client.rest_request("DELETE", "/test/delete")


if __name__ == "__main__":
    unittest.main()
