import unittest
from unittest.mock import patch, MagicMock
import os
from github_project_manager.project_manager import GitHubProjectManager
from github_project_manager.models import StatusOption, IssueLabel, IssueMilestone


class TestGitHubProjectManager(unittest.TestCase):
    def setUp(self):
        # Set environment variables for testing
        os.environ["GITHUB_TOKEN"] = "test_token"
        os.environ["GITHUB_ORG"] = "test_org"

        # Create patcher for the API client
        self.api_patcher = patch(
            "github_project_manager.project_manager.GitHubAPIClient"
        )
        self.mock_api_class = self.api_patcher.start()
        self.mock_api = MagicMock()
        self.mock_api_class.return_value = self.mock_api

        # Initialize the project manager
        self.manager = GitHubProjectManager()

        # Set the project_id for testing
        self.manager.project_id = "test_project_id"
        self.manager.project_name = "Test Project"

    def tearDown(self):
        self.api_patcher.stop()

    def test_init_with_non_existing_project(self):
        """Test initialization with non-existing project name"""
        # Mock project_exists to return False
        with patch.object(GitHubProjectManager, "project_exists", return_value=False):
            with self.assertRaises(ValueError) as context:
                GitHubProjectManager("Non-Existent Project")

            self.assertIn("does not exist", str(context.exception))

    def test_init_missing_env_vars(self):
        """Test initialization with missing environment variables"""
        # Save current env vars
        token = os.environ.get("GITHUB_TOKEN")
        org = os.environ.get("GITHUB_ORG")

        try:
            # Remove env vars
            os.environ.pop("GITHUB_TOKEN", None)

            with self.assertRaises(ValueError) as context:
                GitHubProjectManager()

            self.assertIn("environment variables must be set", str(context.exception))

            # Reset token and test missing org
            os.environ["GITHUB_TOKEN"] = "test_token"
            os.environ.pop("GITHUB_ORG", None)

            with self.assertRaises(ValueError) as context:
                GitHubProjectManager()

            self.assertIn("environment variables must be set", str(context.exception))

        finally:
            # Restore env vars
            if token:
                os.environ["GITHUB_TOKEN"] = token
            if org:
                os.environ["GITHUB_ORG"] = org

    def test_lower_names(self):
        """Test the _lower_names helper method"""

        # Create test objects with name attribute
        class TestObj:
            def __init__(self, name):
                self.name = name

        items = [TestObj("Test"), TestObj("test"), TestObj("TEST")]

        # Call the method
        result = self.manager._lower_names(items)

        # Verify result
        self.assertEqual(result, {"test"})

    def test_get_org_id(self):
        """Test getting organization ID"""
        # Mock API response
        self.mock_api.graphql_query.return_value = {
            "organization": {"id": "test_org_id"}
        }

        # Call the method
        result = self.manager.get_org_id()

        # Verify result
        self.assertEqual(result, "test_org_id")

        # Verify API was called correctly
        self.mock_api.graphql_query.assert_called_once()
        args = self.mock_api.graphql_query.call_args[0]
        self.assertIn("organization(login: $login)", args[0])
        self.assertEqual(args[1], {"login": "test_org"})

    def test_delete_project(self):
        """Test deleting a project"""
        # Mock project_exists to return True and set project_id
        with patch.object(GitHubProjectManager, "project_exists", return_value=True):
            # Set up mock for graphql_query
            self.mock_api.graphql_query.return_value = {
                "deleteProjectV2": {"clientMutationId": "test_id"}
            }

            # Call the method
            self.manager.delete_project("Test Project")

            # Verify API was called correctly
            self.mock_api.graphql_query.assert_called_once()
            args = self.mock_api.graphql_query.call_args[0]
            self.assertIn("deleteProjectV2", args[0])
            self.assertEqual(args[1], {"projectId": "test_project_id"})

    def test_update_status_options(self):
        """Test updating project status options"""
        # Mock project field ID query
        field_id = "test_field_id"
        self.mock_api.graphql_query.side_effect = [
            # First call - get project fields
            {
                "node": {
                    "fields": {
                        "nodes": [
                            {
                                "name": "Status",
                                "id": field_id,
                                "options": [
                                    {"id": "opt1", "name": "Todo"},
                                    {"id": "opt2", "name": "In Progress"},
                                ],
                            }
                        ]
                    }
                }
            },
            # Second call - update field with options
            {"updateProjectV2Field": {"clientMutationId": "test_id"}},
        ]

        # Create custom options
        custom_options = [
            StatusOption("Todo", "RED", "To do items"),
            StatusOption("Done", "GREEN", "Completed items"),
        ]

        # Call the method
        result = self.manager.update_status_options(custom_options)

        # Verify result
        self.assertEqual(result, field_id)

        # Verify API calls
        self.assertEqual(self.mock_api.graphql_query.call_count, 2)

        # Check first call
        first_call = self.mock_api.graphql_query.call_args_list[0]
        self.assertIn("node(id: $projectId)", first_call[0][0])
        self.assertIn("on ProjectV2", first_call[0][0])

        # Check second call
        second_call = self.mock_api.graphql_query.call_args_list[1]
        self.assertIn("updateProjectV2Field", second_call[0][0])
        self.assertEqual(second_call[0][1]["fieldId"], field_id)
        self.assertIn("opts", second_call[0][1])

    def test_create_issue_with_add_to_project(self):
        """Test creating an issue with add_to_project=True"""
        # Mock API responses
        self.mock_api.rest_request.side_effect = [
            # First call - check if issue exists
            [],
            # Second call - create issue
            {"node_id": "test_issue_id", "title": "Test Issue"},
        ]

        # Mock GraphQL query for adding to project
        project_items_response = {"node": {"items": {"nodes": []}}}
        self.mock_api.graphql_query.side_effect = [
            project_items_response,  # First call - check if already in project
            {
                "addProjectV2ItemById": {"item": {"id": "new_item_id"}}
            },  # Second call - add to project
        ]

        # Test creating a new issue with add_to_project=True
        result = self.manager.create_issue(
            "test-repo", "Test Issue", "Test description", add_to_project=True
        )

        # Verify issue was created
        self.assertEqual(result, "test_issue_id")

        # Verify issue was added to project
        self.assertEqual(self.mock_api.graphql_query.call_count, 2)

        # Check second call (the mutation)
        mutation_call = self.mock_api.graphql_query.call_args_list[1]
        self.assertIn("addProjectV2ItemById", mutation_call[0][0])

        # Verify the variables were passed correctly
        variables = mutation_call[0][1]
        self.assertEqual(variables["projectId"], "test_project_id")
        self.assertEqual(variables["contentId"], "test_issue_id")

    def test_create_issue_update_description(self):
        """Test updating an issue's description when it changes"""
        # Mock API responses
        existing_issue = {
            "node_id": "test_issue_id",
            "title": "Test Issue",
            "body": "Old description",
            "number": 42,
        }

        self.mock_api.rest_request.side_effect = [
            # First call - check if issue exists
            [existing_issue],
            # Second call - update issue (add this mock response)
            {"node_id": "test_issue_id", "body": "New description"},
        ]

        # Test updating an existing issue's description
        result = self.manager.create_issue("test-repo", "Test Issue", "New description")

        # Verify correct issue ID is returned
        self.assertEqual(result, "test_issue_id")

        # Verify description was updated
        self.assertEqual(self.mock_api.rest_request.call_count, 2)
        patch_call_args = self.mock_api.rest_request.call_args_list[1]
        self.assertEqual(patch_call_args[0][0], "PATCH")
        self.assertEqual(patch_call_args[0][1], "/repos/test_org/test-repo/issues/42")
        self.assertEqual(patch_call_args[0][2], {"body": "New description"})

    def test_add_issue_to_project_already_exists(self):
        """Test adding an issue that's already in the project"""
        # Mock API responses for checking project items
        project_items_response = {
            "node": {
                "items": {
                    "nodes": [
                        {"content": {"id": "issue_1"}},
                        {"content": {"id": "test_issue_id"}},
                    ]
                }
            }
        }

        self.mock_api.graphql_query.return_value = project_items_response

        # Try to add an issue that's already in the project
        self.manager.add_issue_to_project("test_issue_id")

        # Verify the API wasn't called to add the issue
        self.assertEqual(self.mock_api.graphql_query.call_count, 1)

    def test_add_issue_to_project_new_issue(self):
        """Test adding an issue that's not already in the project"""
        # Mock API responses for checking project items
        project_items_response = {
            "node": {"items": {"nodes": [{"content": {"id": "issue_1"}}]}}
        }

        # First call returns existing items, second call is the mutation
        self.mock_api.graphql_query.side_effect = [
            project_items_response,
            {"addProjectV2ItemById": {"item": {"id": "new_item_id"}}},
        ]

        # Add a new issue to the project
        self.manager.add_issue_to_project("test_issue_id")

        # Verify the API was called to add the issue
        self.assertEqual(self.mock_api.graphql_query.call_count, 2)
        mutation_call = self.mock_api.graphql_query.call_args_list[1]

        # Check that a mutation with addProjectV2ItemById was called
        self.assertIn("addProjectV2ItemById", mutation_call[0][0])

        # Verify the variables were passed correctly
        variables = mutation_call[0][1]
        self.assertEqual(variables["projectId"], "test_project_id")
        self.assertEqual(variables["contentId"], "test_issue_id")

    def test_create_labels(self):
        """Test creating labels in repositories"""
        # Mock the _update_or_create_label method
        with patch.object(
            GitHubProjectManager, "_update_or_create_label"
        ) as mock_update:
            # Create test label
            label = IssueLabel("bug", "FF0000", "Bug description")

            # Test with a single repo and label
            self.manager.create_labels("test-repo", label)

            # Verify _update_or_create_label was called correctly
            mock_update.assert_called_once_with("test-repo", label)

            # Reset mock
            mock_update.reset_mock()

            # Test with multiple repos and labels
            repos = ["repo1", "repo2"]
            labels = [
                IssueLabel("bug", "FF0000", "Bug description"),
                IssueLabel("feature", "00FF00", "Feature description"),
            ]

            self.manager.create_labels(repos, labels)

            # Verify _update_or_create_label was called correctly 4 times (2 repos * 2 labels)
            self.assertEqual(mock_update.call_count, 4)
            # Check first call
            mock_update.assert_any_call("repo1", labels[0])
            # Check last call
            mock_update.assert_any_call("repo2", labels[1])

    def test_update_or_create_label(self):
        """Test updating or creating a label"""
        # Create test label
        label = IssueLabel("bug", "FF0000", "Bug description")

        # Mock API responses for existing label case
        self.mock_api.rest_request.side_effect = [
            # First call - get existing labels
            [{"name": "bug", "color": "cc0000", "description": "Old description"}],
            # Second call - update existing label
            {"name": "bug", "color": "FF0000", "description": "Bug description"},
        ]

        # Call the method for existing label case
        self.manager._update_or_create_label("test-repo", label)

        # Verify API calls
        self.assertEqual(self.mock_api.rest_request.call_count, 2)

        # Check first call (GET labels)
        first_call = self.mock_api.rest_request.call_args_list[0]
        self.assertEqual(first_call[0][0], "GET")
        self.assertEqual(first_call[0][1], "/repos/test_org/test-repo/labels")

        # Check second call (PATCH label)
        second_call = self.mock_api.rest_request.call_args_list[1]
        self.assertEqual(second_call[0][0], "PATCH")
        self.assertEqual(second_call[0][1], "/repos/test_org/test-repo/labels/bug")
        self.assertEqual(second_call[0][2], label.to_dict())

        # Reset mock
        self.mock_api.rest_request.reset_mock()

        # Mock API responses for new label case
        self.mock_api.rest_request.side_effect = [
            # First call - get existing labels (empty)
            [],
            # Second call - create new label
            {
                "name": "feature",
                "color": "00FF00",
                "description": "Feature description",
            },
        ]

        # Create a new test label
        new_label = IssueLabel("feature", "00FF00", "Feature description")

        # Call the method for new label case
        self.manager._update_or_create_label("test-repo", new_label)

        # Verify API calls
        self.assertEqual(self.mock_api.rest_request.call_count, 2)

        # Check second call (POST label)
        second_call = self.mock_api.rest_request.call_args_list[1]
        self.assertEqual(second_call[0][0], "POST")
        self.assertEqual(second_call[0][1], "/repos/test_org/test-repo/labels")
        self.assertEqual(second_call[0][2], new_label.to_dict())

    def test_create_milestones(self):
        """Test creating milestones in repositories"""
        # Mock the _update_or_create_milestone method
        with patch.object(
            GitHubProjectManager, "_update_or_create_milestone", return_value=1
        ) as mock_update:
            # Create test milestone
            milestone = IssueMilestone("v1.0", "First release", "2023-12-31")

            # Test with a single repo and milestone
            self.manager.create_milestones("test-repo", milestone)

            # Verify _update_or_create_milestone was called correctly
            mock_update.assert_called_once_with("test-repo", milestone)

            # Reset mock
            mock_update.reset_mock()

            # Test with multiple repos and milestones
            repos = ["repo1", "repo2"]
            milestones = [
                IssueMilestone("v1.0", "First release", "2023-12-31"),
                IssueMilestone("v2.0", "Second release", "2024-06-30"),
            ]

            self.manager.create_milestones(repos, milestones)

            # Verify _update_or_create_milestone was called correctly 4 times (2 repos * 2 milestones)
            self.assertEqual(mock_update.call_count, 4)
            # Check first call
            mock_update.assert_any_call("repo1", milestones[0])
            # Check last call
            mock_update.assert_any_call("repo2", milestones[1])

    def test_update_or_create_milestone(self):
        """Test updating or creating a milestone"""
        # Create test milestone
        milestone = IssueMilestone("v1.0", "First release", "2023-12-31")

        # Mock API responses for existing milestone case
        self.mock_api.rest_request.side_effect = [
            # First call - get existing milestones
            [{"title": "v1.0", "description": "Old description", "number": 1}],
            # Second call - update existing milestone
            {"title": "v1.0", "description": "First release", "number": 1},
        ]

        # Call the method for existing milestone case
        result = self.manager._update_or_create_milestone("test-repo", milestone)

        # Verify result is the milestone number
        self.assertEqual(result, 1)

        # Verify API calls
        self.assertEqual(self.mock_api.rest_request.call_count, 2)

        # Check first call (GET milestones)
        first_call = self.mock_api.rest_request.call_args_list[0]
        self.assertEqual(first_call[0][0], "GET")
        self.assertEqual(
            first_call[0][1], "/repos/test_org/test-repo/milestones?state=all"
        )

        # Check second call (PATCH milestone)
        second_call = self.mock_api.rest_request.call_args_list[1]
        self.assertEqual(second_call[0][0], "PATCH")
        self.assertEqual(second_call[0][1], "/repos/test_org/test-repo/milestones/1")
        self.assertEqual(second_call[0][2], milestone.to_dict())

        # Reset mock
        self.mock_api.rest_request.reset_mock()

        # Mock API responses for new milestone case
        self.mock_api.rest_request.side_effect = [
            # First call - get existing milestones (none match)
            [{"title": "v0.5", "description": "Beta release", "number": 1}],
            # Second call - create new milestone
            {"title": "v2.0", "description": "Second release", "number": 2},
        ]

        # Create a new test milestone
        new_milestone = IssueMilestone("v2.0", "Second release", "2024-06-30")

        # Call the method for new milestone case
        result = self.manager._update_or_create_milestone("test-repo", new_milestone)

        # Verify result is the milestone number
        self.assertEqual(result, 2)

        # Verify API calls
        self.assertEqual(self.mock_api.rest_request.call_count, 2)

        # Check second call (POST milestone)
        second_call = self.mock_api.rest_request.call_args_list[1]
        self.assertEqual(second_call[0][0], "POST")
        self.assertEqual(second_call[0][1], "/repos/test_org/test-repo/milestones")
        self.assertEqual(second_call[0][2], new_milestone.to_dict())


if __name__ == "__main__":
    unittest.main()
