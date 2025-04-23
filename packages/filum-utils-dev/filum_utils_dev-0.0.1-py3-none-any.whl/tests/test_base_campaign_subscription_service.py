import csv
import datetime
import io
import unittest
from unittest.mock import patch

import filum_utils_dev.services.subscription.base_campaign as base_mod
from filum_utils_dev import CampaignSubscriptionService
from filum_utils_dev.config import config
from filum_utils_dev.errors import BaseError, ErrorMessage
from filum_utils_dev.services.subscription.base_campaign import BaseCampaignSubscriptionService


class DummyService(BaseCampaignSubscriptionService):
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


class TestBaseCampaignSubscriptionService(unittest.TestCase):
    def setUp(self):
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

    def test_handling_upload_segment_users_file(self):
        """Test the basic functionality of _handling_upload_segment_users_file"""
        service = DummyService(self.subscription, self.action, self.organization, campaign_id="camp-1")
        users = [{"email": "a@b", "name": "Name"}]
        fixed_date = datetime.datetime(2021, 1, 2)
        upload_calls = []

        class DummyStorageClient:
            def upload_file(self, filename, buffer):
                upload_calls.append((filename, buffer.getvalue()))

        with unittest.mock.patch.object(DummyService, '_fetch_segment_users', return_value=users), \
            unittest.mock.patch.object(base_mod.DateTimeFormatter, 'get_current_datetime', return_value=fixed_date), \
            unittest.mock.patch.object(base_mod, 'GoogleCloudStorageClient', new=DummyStorageClient):
            filename = service._handling_upload_segment_users_file(users, ["email", "name", "age"])
            
        # Test file name format
        self.assertEqual(filename, "org-1/camp-1/dist-1/20210102.csv")
        self.assertEqual(len(upload_calls), 1)
        uploaded_fname, data_bytes = upload_calls[0]
        self.assertEqual(uploaded_fname, filename)
        
        # Test CSV content
        text = data_bytes.decode('utf-8')
        reader = csv.DictReader(io.StringIO(text))
        self.assertEqual(reader.fieldnames, ["email", "name", "age"])
        rows = list(reader)
        self.assertTrue(rows and rows[0]["email"] == "a@b")
        
    def test_handling_upload_segment_users_file_without_distribution_id(self):
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
        
        service = DummyService(subscription_without_dist, self.action, self.organization, campaign_id="camp-1")
        users = [{"email": "user1@example.com", "name": "User One"}]
        properties = ["email", "name"]
        fixed_date = datetime.datetime(2021, 1, 2)
        upload_calls = []
        
        class DummyStorageClient:
            def upload_file(self, filename, buffer):
                upload_calls.append((filename, buffer.getvalue()))
        
        with unittest.mock.patch.object(base_mod.DateTimeFormatter, 'get_current_datetime', return_value=fixed_date), \
             unittest.mock.patch.object(base_mod, 'GoogleCloudStorageClient', new=DummyStorageClient):
            
            # Call the method
            file_name = service._handling_upload_segment_users_file(users, properties)
            
            # Verify the file name format without distribution_id
            expected_file_name = f"org-1/camp-1/20210102.csv"
            self.assertEqual(file_name, expected_file_name)
            
    def test_handling_upload_segment_users_file_with_missing_properties(self):
        """Test that CSV content handles missing properties correctly"""
        service = DummyService(self.subscription, self.action, self.organization, campaign_id="camp-1")
        
        # Test with multiple users and properties, including missing values
        users = [
            {"email": "user1@example.com", "name": "User One", "age": "25"},
            {"email": "user2@example.com", "name": "User Two", "age": "30"},
            {"email": "user3@example.com", "name": "User Three"} # Missing age property
        ]
        properties = ["email", "name", "age"]
        fixed_date = datetime.datetime(2021, 1, 2)
        upload_calls = []
        
        class DummyStorageClient:
            def upload_file(self, filename, buffer):
                upload_calls.append((filename, buffer.getvalue()))
        
        with unittest.mock.patch.object(base_mod.DateTimeFormatter, 'get_current_datetime', return_value=fixed_date), \
             unittest.mock.patch.object(base_mod, 'GoogleCloudStorageClient', new=DummyStorageClient):
            
            # Call the method
            service._handling_upload_segment_users_file(users, properties)
            
            # Verify CSV content
            _, data_bytes = upload_calls[0]
            csv_content = data_bytes.decode('utf-8')
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
            
    def test_handling_upload_segment_users_file_empty_users(self):
        """Test handling of an empty users list"""
        service = DummyService(self.subscription, self.action, self.organization, campaign_id="camp-1")
        users = []
        properties = ["email", "name"]
        fixed_date = datetime.datetime(2021, 1, 2)
        upload_calls = []
        
        class DummyStorageClient:
            def upload_file(self, filename, buffer):
                upload_calls.append((filename, buffer.getvalue()))
        
        with unittest.mock.patch.object(base_mod.DateTimeFormatter, 'get_current_datetime', return_value=fixed_date), \
             unittest.mock.patch.object(base_mod, 'GoogleCloudStorageClient', new=DummyStorageClient):
            
            # Call the method
            file_name = service._handling_upload_segment_users_file(users, properties)
            
            # Verify the file name is still generated correctly
            expected_file_name = f"org-1/camp-1/dist-1/20210102.csv"
            self.assertEqual(file_name, expected_file_name)
            
            # Verify that upload_file was called with a CSV containing only headers
            self.assertEqual(len(upload_calls), 1)
            
            # Check CSV content has only headers
            _, data_bytes = upload_calls[0]
            csv_content = data_bytes.decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(csv_content))
            self.assertEqual(csv_reader.fieldnames, properties)
            self.assertEqual(list(csv_reader), [])

    def test_fetch_segment_users_pagination(self):
        service = DummyService(self.subscription, self.action, self.organization)

        class DummyClient:
            def __init__(self):
                self.call_args = []

            def get_user_csv_reader(self, custom_properties, segment_id, organization, offset, limit):
                self.call_args.append((custom_properties, segment_id, offset, limit))
                if offset == 0:
                    return list(range(config.SEGMENT_RECORD_LIMIT))
                return [1, 2]

        service.filum_client = DummyClient()
        result = service._fetch_segment_users(["p"], "seg")
        self.assertEqual(len(service.filum_client.call_args), 2)
        self.assertEqual(service.filum_client.call_args[0][2], 0)
        self.assertEqual(service.filum_client.call_args[1][2], config.SEGMENT_RECORD_LIMIT)
        self.assertEqual(len(result), config.SEGMENT_RECORD_LIMIT + 2)

    def test_handle_segment_manual_trigger_initial(self):
        service = DummyService(self.subscription, self.action, self.organization)
        with patch.object(service, '_handling_upload_segment_users_file', return_value='file.csv'), \
            patch.object(service, '_handle_publish_subscription') as mock_pub:
            res = service.handle_segment_manual_trigger(lambda **kwargs: None, ["email"], 0, 0)
        self.assertFalse(res['is_finished'])
        self.assertEqual(res['success_count'], 0)
        self.assertIsNone(res['error_message'])
        mock_pub.assert_called_once_with(last_current_index=0, last_success_count=0, segment_user_file_name='file.csv')

    def test_handle_segment_manual_trigger_missing_segment_id(self):
        sub = {
            "id": "sub-1",
            "data": {
                "metadata_mapping": [{"property_name": "email"}],
                "trigger_data": {},
                "distribution_id": "dist-1"
            }
        }
        service = DummyService(sub, self.action, self.organization)
        with self.assertRaises(BaseError) as cm:
            service.handle_segment_manual_trigger(lambda **kwargs: None, ["email"])
        self.assertEqual(cm.exception.message, ErrorMessage.MISSING_SEGMENT_ID)

    def test_handle_segment_manual_trigger_resumed(self):
        service = DummyService(self.subscription, self.action, self.organization)
        with unittest.mock.patch.object(service, '_get_users_in_csv_file', return_value=[{"u": 1}]), \
            unittest.mock.patch.object(service, '_handle_manual_trigger',
                                       return_value={"is_finished": True, "success_count": 1, "error_message": "err"}):
            res = service.handle_segment_manual_trigger(lambda **kwargs: None, ["email"], last_current_index=5,
                                                        last_success_count=2, channel_name="ch",
                                                        segment_user_file_name="file.csv")
        self.assertDictEqual(res, {"is_finished": True, "success_count": 1, "error_message": "err"})

    def test_handle_publish_subscription(self):
        service = DummyService(self.subscription, self.action, self.organization)

        class SubClient:
            def __init__(self):
                self.calls = []

            def update_data(self, data):
                self.calls.append(("update", data))

            def publish(self, request_data):
                self.calls.append(("publish", request_data))

        client = SubClient()
        service.subscription_client = client
        err = service._handle_publish_subscription(10, 3)
        self.assertIsNone(err)
        self.assertIn(("update", {"last_current_index": 10}), client.calls)
        self.assertIn(("publish", {"last_current_index": 10, "last_success_count": 3}), client.calls)
        client.calls.clear()
        err2 = service._handle_publish_subscription(7, 4, "file.csv")
        self.assertIsNone(err2)
        self.assertIn(("update", {"last_current_index": 7, "segment_user_file_name": "file.csv"}), client.calls)
        self.assertIn(
            (
                "publish",
                {"last_current_index": 7, "last_success_count": 4, "segment_user_file_name": "file.csv"}
            ),
            client.calls
        )

        class ErrClient:
            def update_data(self, data): pass

            def publish(self, request_data):
                raise BaseError("fail")

        service.subscription_client = ErrClient()
        err3 = service._handle_publish_subscription(1, 2)
        self.assertIn("Publish Subscription: fail", err3)


if __name__ == '__main__':
    unittest.main()
