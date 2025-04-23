import csv
import datetime
import io
import unittest
from unittest.mock import MagicMock, Mock, patch

import filum_utils_dev.services.subscription.base_campaign as base_mod
from filum_utils_dev.services.subscription.base_campaign import BaseCampaignSubscriptionService
from filum_utils_dev.utils.datetime_formatter import DateTimeFormatter


class DummyService(BaseCampaignSubscriptionService):
    """Dummy implementation of BaseCampaignSubscriptionService for testing"""

    def __init__(self, subscription, action, organization, campaign_id=None):
        super().__init__(subscription, action, organization, campaign_id)

    @property
    def parent(self):
        return {"id": "parent-id", "name": "Parent Campaign"}

    @property
    def member_account_id(self):
        return "member-id"

    @property
    def run_type(self):
        return "manual"

    @property
    def _parent_id(self):
        return self.parent["id"]

    @property
    def _parent_name(self):
        return self.parent["name"]

    @property
    def _parent_type(self):
        return "campaign"

    @property
    def _notification_route(self):
        return {
            "path": "path",
            "params": {
                "key": "value"
            }
        }

    def update_status(self, updated_status):
        pass

    def _get_trigger_completed_notification_subtitle(self, channel_name, success_count):
        return f"Completed {success_count}"


class TestHandlingUploadSegmentUsersFile(unittest.TestCase):
    """Test cases for the _handling_upload_segment_users_file method"""

    def setUp(self):
        """Set up test fixtures"""
        self.subscription = {
            "id": "sub-1",
            "data": {
                "metadata_mapping": [{"property_name": "email"}, {"property_name": "name"}],
                "trigger_data": {"segment_id": "seg-1"},
                "distribution_id": "dist-1"
            }
        }
        self.action = {"id": "action-1"}
        self.organization = {"id": "org-1"}
        self.campaign_id = "camp-1"

        # Create a fixed datetime for consistent testing
        self.fixed_datetime = datetime.datetime(2023, 4, 15, 10, 30)

        # Create a service instance for testing
        self.service = DummyService(
            self.subscription,
            self.action,
            self.organization,
            campaign_id=self.campaign_id
        )

    def test_file_name_generation_with_distribution_id(self):
        """Test file name generation when distribution_id is present"""
        users = [{"email": "user1@example.com", "name": "User One"}]
        properties = ["email", "name"]

        # Mock dependencies
        storage_client_mock = MagicMock()

        with patch.object(DateTimeFormatter, 'get_current_datetime', return_value=self.fixed_datetime), \
            patch.object(base_mod, 'GoogleCloudStorageClient', return_value=storage_client_mock):
            # Call the method
            file_name = self.service._handling_upload_segment_users_file(users, properties)

            # Verify the file name format with distribution_id
            expected_file_name = f"org-1/camp-1/dist-1/202304151030.csv"
            self.assertEqual(file_name, expected_file_name)

    def test_file_name_generation_without_distribution_id(self):
        """Test file name generation when distribution_id is not present"""
        # Create a subscription without distribution_id
        subscription_without_dist = {
            "id": "sub-1",
            "data": {
                "metadata_mapping": [{"property_name": "email"}, {"property_name": "name"}],
                "trigger_data": {"segment_id": "seg-1"}
                # No distribution_id
            }
        }

        service = DummyService(
            subscription_without_dist,
            self.action,
            self.organization,
            campaign_id=self.campaign_id
        )

        users = [{"email": "user1@example.com", "name": "User One"}]
        properties = ["email", "name"]

        # Mock dependencies
        storage_client_mock = MagicMock()

        with patch.object(DateTimeFormatter, 'get_current_datetime', return_value=self.fixed_datetime), \
            patch.object(base_mod, 'GoogleCloudStorageClient', return_value=storage_client_mock):
            # Call the method
            file_name = service._handling_upload_segment_users_file(users, properties)

            # Verify the file name format without distribution_id
            expected_file_name = f"org-1/camp-1/202304151030.csv"
            self.assertEqual(file_name, expected_file_name)

    def test_csv_content_generation(self):
        """Test that CSV content is correctly generated from user data"""
        # Test with multiple users and properties
        users = [
            {"email": "user1@example.com", "name": "User One", "age": "25"},
            {"email": "user2@example.com", "name": "User Two", "age": "30"},
            {"email": "user3@example.com", "name": "User Three"}  # Missing age property
        ]
        properties = ["email", "name", "age"]

        # Create a mock for the storage client
        class MockStorageClient:
            def __init__(self):
                self.uploaded_file = None
                self.uploaded_content = None

            def upload_file(self, file_name, file_obj):
                self.uploaded_file = file_name
                self.uploaded_content = file_obj.getvalue()

        mock_client = MockStorageClient()

        with patch.object(DateTimeFormatter, 'get_current_datetime', return_value=self.fixed_datetime), \
            patch.object(base_mod, 'GoogleCloudStorageClient', return_value=mock_client):
            # Call the method
            self.service._handling_upload_segment_users_file(users, properties)

            # Verify CSV content
            csv_content = mock_client.uploaded_content.decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(csv_content))

            # Check headers
            self.assertEqual(csv_reader.fieldnames, properties)

            # Check rows
            rows = list(csv_reader)
            self.assertEqual(len(rows), 3)

            # Check first user data
            self.assertEqual(rows[0]["email"], "user1@example.com")
            self.assertEqual(rows[0]["name"], "User One")
            self.assertEqual(rows[0]["age"], "25")

            # Check third user with missing property (should be empty string)
            self.assertEqual(rows[2]["email"], "user3@example.com")
            self.assertEqual(rows[2]["name"], "User Three")
            self.assertEqual(rows[2]["age"], "")  # Missing property should be empty string

    def test_upload_to_storage(self):
        """Test that the file is correctly uploaded to Google Cloud Storage"""
        users = [{"email": "user1@example.com", "name": "User One"}]
        properties = ["email", "name"]

        # Create a mock for the storage client
        mock_storage_client = MagicMock()

        with patch.object(DateTimeFormatter, 'get_current_datetime', return_value=self.fixed_datetime), \
            patch.object(base_mod, 'GoogleCloudStorageClient', return_value=mock_storage_client):
            # Call the method
            file_name = self.service._handling_upload_segment_users_file(users, properties)

            # Verify that upload_file was called with the correct file name
            mock_storage_client.upload_file.assert_called_once()
            args, _ = mock_storage_client.upload_file.call_args
            self.assertEqual(args[0], file_name)

            # Verify that the second argument is a BytesIO object
            self.assertIsInstance(args[1], io.BytesIO)

    def test_empty_users_list(self):
        """Test handling of an empty users list"""
        users = []
        properties = ["email", "name"]

        # Mock dependencies
        storage_client_mock = MagicMock()

        with patch.object(DateTimeFormatter, 'get_current_datetime', return_value=self.fixed_datetime), \
            patch.object(base_mod, 'GoogleCloudStorageClient', return_value=storage_client_mock):
            # Call the method
            file_name = self.service._handling_upload_segment_users_file(users, properties)

            # Verify the file name is still generated correctly
            expected_file_name = f"org-1/camp-1/dist-1/202304151030.csv"
            self.assertEqual(file_name, expected_file_name)

            # Verify that upload_file was called with a CSV containing only headers
            storage_client_mock.upload_file.assert_called_once()

            # Get the BytesIO object passed to upload_file
            _, kwargs = storage_client_mock.upload_file.call_args
            file_obj = kwargs.get('file_obj', None)
            if file_obj is None:
                args, _ = storage_client_mock.upload_file.call_args
                file_obj = args[1]

            # Check CSV content has only headers
            csv_content = file_obj.getvalue().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(csv_content))
            self.assertEqual(csv_reader.fieldnames, properties)
            self.assertEqual(list(csv_reader), [])

    # def test_buffer_is_closed(self):
    #     """Test that the StringIO buffer is properly closed after use"""
    #     users = [{"email": "user1@example.com", "name": "User One"}]
    #     properties = ["email", "name"]

    #     # Mock dependencies
    #     storage_client_mock = MagicMock()
    #     io_mock = MagicMock(spec=io.StringIO)

    #     with patch.object(DateTimeFormatter, 'get_current_datetime', return_value=self.fixed_datetime), \
    #         patch.object(base_mod, 'GoogleCloudStorageClient', return_value=storage_client_mock), \
    #         patch.object(base_mod, 'io.StringIO', return_value=io_mock):
    #         # Call the method
    #         print("io_mock")
    #         print(io_mock)
    #         self.service._handling_upload_segment_users_file(users, properties)

    #         # Verify that close was called on the StringIO buffer
    #         io_mock.assert_called_once()
    #         io_mock.StringIO.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
