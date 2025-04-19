import unittest
from github_project_manager.models import StatusOption, IssueLabel, IssueMilestone


class TestModels(unittest.TestCase):
    def test_status_option(self):
        # Test creation
        option = StatusOption("To Do", "RED", "Items to be done")
        self.assertEqual(option.name, "To Do")
        self.assertEqual(option.color, "RED")
        self.assertEqual(option.description, "Items to be done")

        # Test to_dict
        option_dict = option.to_dict()
        self.assertEqual(option_dict["name"], "To Do")
        self.assertEqual(option_dict["color"], "RED")
        self.assertEqual(option_dict["description"], "Items to be done")

        # Test from_dict
        new_option = StatusOption.from_dict(option_dict)
        self.assertEqual(new_option.name, option.name)
        self.assertEqual(new_option.color, option.color)
        self.assertEqual(new_option.description, option.description)

    def test_issue_label(self):
        # Test creation
        label = IssueLabel("bug", "FF0000", "Something isn't working")
        self.assertEqual(label.name, "bug")
        self.assertEqual(label.color, "FF0000")
        self.assertEqual(label.description, "Something isn't working")

        # Test to_dict
        label_dict = label.to_dict()
        self.assertEqual(label_dict["name"], "bug")
        self.assertEqual(label_dict["color"], "FF0000")
        self.assertEqual(label_dict["description"], "Something isn't working")

        # Test from_dict
        new_label = IssueLabel.from_dict(label_dict)
        self.assertEqual(new_label.name, label.name)
        self.assertEqual(new_label.color, label.color)
        self.assertEqual(new_label.description, label.description)

    def test_issue_milestone(self):
        # Test creation
        milestone = IssueMilestone(
            "v1.0", "First stable release", "2023-12-31T23:59:59Z"
        )
        self.assertEqual(milestone.title, "v1.0")
        self.assertEqual(milestone.description, "First stable release")
        self.assertEqual(milestone.due_on, "2023-12-31T23:59:59Z")

        # Test to_dict
        milestone_dict = milestone.to_dict()
        self.assertEqual(milestone_dict["title"], "v1.0")
        self.assertEqual(milestone_dict["description"], "First stable release")
        self.assertEqual(milestone_dict["due_on"], "2023-12-31T23:59:59Z")

        # Test from_dict
        new_milestone = IssueMilestone.from_dict(milestone_dict)
        self.assertEqual(new_milestone.title, milestone.title)
        self.assertEqual(new_milestone.description, milestone.description)
        self.assertEqual(new_milestone.due_on, milestone.due_on)

    def test_from_dicts(self):
        # Test the from_dicts classmethod
        dicts = [
            {"name": "Todo", "color": "RED", "description": "To do items"},
            {"name": "Done", "color": "GREEN", "description": "Completed items"},
        ]

        options = StatusOption.from_dicts(dicts)
        self.assertEqual(len(options), 2)
        self.assertEqual(options[0].name, "Todo")
        self.assertEqual(options[1].name, "Done")


if __name__ == "__main__":
    unittest.main()
