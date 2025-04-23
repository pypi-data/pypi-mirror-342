import unittest
from filum_utils_dev.utils.automated_action.string_formatter import AutomatedActionStringFormatter


class TestAutomatedActionStringFormatter(unittest.TestCase):
    def test_populate_data_with_empty_string(self):
        result = AutomatedActionStringFormatter.populate_data("")
        self.assertEqual(result, "")

    def test_populate_data_with_user_data(self):
        test_string = "Hello {{user.name}}"
        user_data = {"name": "John Doe"}
        result = AutomatedActionStringFormatter.populate_data(
            default_string=test_string,
            user=user_data
        )
        self.assertEqual(result, "Hello John Doe")

    def test_populate_data_with_multiple_variables(self):
        test_string = "User {{user.name}} from segment {{segment.name}}"
        user_data = {"name": "John Doe"}
        segment_data = {"name": "VIP Customers"}
        result = AutomatedActionStringFormatter.populate_data(
            default_string=test_string,
            user=user_data,
            segment=segment_data
        )
        self.assertEqual(result, "User John Doe from segment VIP Customers")

    def test_populate_data_with_missing_data(self):
        test_string = "Hello {{user.name}} from {{segment.name}}"
        user_data = {"name": "John Doe"}
        result = AutomatedActionStringFormatter.populate_data(
            default_string=test_string,
            user=user_data
        )
        self.assertEqual(result, "Hello John Doe from ")

    def test_populate_data_with_platform_url(self):
        test_string = "Check profile at {{user.link}}"
        user_data = {"email": "john@example.com"}
        platform_url = "https://platform.example.com"
        result = AutomatedActionStringFormatter.populate_data(
            default_string=test_string,
            user=user_data,
            platform_url=platform_url
        )
        expected_url = f"{platform_url}/customers/profile/redirect?Email=john@example.com"
        self.assertEqual(result, f"Check profile at {expected_url}")
