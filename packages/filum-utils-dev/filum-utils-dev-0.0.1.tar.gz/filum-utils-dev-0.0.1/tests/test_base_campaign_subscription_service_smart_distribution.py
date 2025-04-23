import unittest
from unittest.mock import MagicMock, patch

from filum_utils_dev.services.subscription.base_campaign import BaseCampaignSubscriptionService


class DummyService(BaseCampaignSubscriptionService):
    """Dummy service class for testing BaseCampaignSubscriptionService"""

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


class TestBaseCampaignSubscriptionServiceSmartDistribution(unittest.TestCase):
    def setUp(self):
        # Sample subscription with smart distribution configuration
        self.subscription = {
            "id": "sub-1",
            "data": {
                "metadata_mapping": [{"property_name": "email"}, {"property_name": "province"}],
                "trigger_data": {
                    "segment_id": "seg-1",
                    "user_limit_per_trigger": 200
                },
                "distribution_id": "dist-1"
            },
            "smart_distribution": {
                "enabled": True,
                "config": {
                    "metadata_id": "province_metadata_id",
                    "property_name": "province",
                    "response_rate": 0.2,
                    "targets": {
                        "A": 100,
                        "B": 150,
                        "C": 50
                    }
                }
            }
        }
        self.action = {"id": "action-1"}
        self.organization = {"id": "org-1"}
        self.campaign_id = "camp-1"

        # Create service instance
        self.service = DummyService(
            self.subscription,
            self.action,
            self.organization,
            campaign_id=self.campaign_id
        )

        # Sample users for testing
        self.users = [
            {"id": "1", "email": "user1@example.com", "province": "A"},
            {"id": "2", "email": "user2@example.com", "province": "B"},
            {"id": "3", "email": "user3@example.com", "province": "A"},
            {"id": "4", "email": "user4@example.com", "province": "C"},
            {"id": "5", "email": "user5@example.com", "province": "B"},
        ]

    def test_get_metadata_groups_with_smart_distribution_enabled(self):
        """Test _get_metadata_groups when smart distribution is enabled"""
        # Mock FilumClient to return sample response data
        self.service.filum_client = MagicMock()
        self.service.filum_client.get_this_month_answered_response_counts_by_metadata.return_value = {
            "A": 50,
            "B": 100,
            "C": 40
        }

        # Mock SegmentUserUtil
        with patch('filum_utils_dev.services.subscription.base_campaign.SegmentUserUtil') as mock_segment_util_class:
            mock_segment_util = MagicMock()
            mock_segment_util_class.return_value = mock_segment_util
            mock_segment_util.count_grouped_users_by_metadata_value.return_value = {
                "A": 500,
                "B": 300,
                "C": 200
            }

            # Mock SmartDistributionUtil
            with patch(
                'filum_utils_dev.services.subscription.base_campaign.SmartDistributionUtil') as mock_smart_dist_class:
                mock_smart_dist = MagicMock()
                mock_smart_dist_class.return_value = mock_smart_dist
                mock_smart_dist.calculate_limit_per_metadata_value.return_value = {
                    "A": {"value": "A", "remaining_send": 91},
                    "B": {"value": "B", "remaining_send": 91},
                    "C": {"value": "C", "remaining_send": 18}
                }

                # Call the method
                result = self.service._get_metadata_groups(self.users)

                # Verify FilumClient was called correctly
                self.service.filum_client.get_this_month_answered_response_counts_by_metadata.assert_called_once_with(
                    "province_metadata_id", "org-1"
                )

                # Verify SegmentUserUtil was initialized and called correctly
                mock_segment_util_class.assert_called_once_with(self.users)
                mock_segment_util.count_grouped_users_by_metadata_value.assert_called_once_with("province")

                # Verify SmartDistributionUtil was initialized and called correctly
                mock_smart_dist_class.assert_called_once_with(
                    self.subscription["smart_distribution"]["config"],
                    {"A": 500, "B": 300, "C": 200},
                    200  # user_limit_per_trigger
                )
                mock_smart_dist.calculate_limit_per_metadata_value.assert_called_once_with(
                    {"A": 50, "B": 100, "C": 40}
                )

                # Verify the result
                self.assertEqual(result, {
                    "A": {"value": "A", "remaining_send": 91},
                    "B": {"value": "B", "remaining_send": 91},
                    "C": {"value": "C", "remaining_send": 18}
                })

    def test_get_metadata_groups_with_smart_distribution_disabled(self):
        """Test _get_metadata_groups when smart distribution is disabled"""
        # Create service with smart distribution disabled
        subscription_disabled = self.subscription.copy()
        subscription_disabled["smart_distribution"] = {"enabled": False}
        service = DummyService(subscription_disabled, self.action, self.organization)

        # Call the method
        result = service._get_metadata_groups(self.users)

        # Verify result is None when smart distribution is disabled
        self.assertIsNone(result)

    def test_get_metadata_groups_with_missing_config(self):
        """Test _get_metadata_groups when smart distribution config is missing"""
        # Create service with missing config
        subscription_no_config = self.subscription.copy()
        subscription_no_config["smart_distribution"] = {"enabled": True}  # No config
        service = DummyService(subscription_no_config, self.action, self.organization)

        # Call the method
        result = service._get_metadata_groups(self.users)

        # Verify result is None when config is missing
        self.assertIsNone(result)

    def test_get_metadata_groups_with_missing_metadata_id(self):
        """Test _get_metadata_groups when metadata_id is missing"""
        # Create service with missing metadata_id
        subscription_no_metadata_id = self.subscription.copy()
        subscription_no_metadata_id["smart_distribution"]["config"] = {
            "property_name": "province",
            "response_rate": 0.2,
            "targets": {"A": 100, "B": 150, "C": 50}
        }  # No metadata_id
        service = DummyService(subscription_no_metadata_id, self.action, self.organization)

        # Call the method
        result = service._get_metadata_groups(self.users)

        # Verify result is None when metadata_id is missing
        self.assertIsNone(result)

    def test_handle_segment_manual_trigger_initial_with_smart_distribution(self):
        """Test handle_segment_manual_trigger for initial trigger with smart distribution"""
        # Mock _handling_upload_segment_users_file to return filename and users
        with patch.object(self.service, '_handling_upload_segment_users_file',
                          return_value=('file.csv', self.users)) as mock_upload:
            # Mock _get_metadata_groups to return metadata groups
            with patch.object(self.service, '_get_metadata_groups') as mock_get_groups:
                metadata_groups = {
                    "A": {"value": "A", "remaining_send": 91},
                    "B": {"value": "B", "remaining_send": 91},
                    "C": {"value": "C", "remaining_send": 18}
                }
                mock_get_groups.return_value = metadata_groups

                # Mock _handle_publish_subscription
                with patch.object(self.service, '_handle_publish_subscription') as mock_publish:
                    mock_publish.return_value = None  # No error

                    # Call the method with initial parameters
                    callback = MagicMock()
                    result = self.service.handle_segment_manual_trigger(
                        callback,
                        ["email", "province"],
                        last_current_index=0,
                        last_success_count=0
                    )

                    # Verify _handling_upload_segment_users_file was called correctly
                    mock_upload.assert_called_once_with(["email", "province"])

                    # Verify _get_metadata_groups was called with users
                    mock_get_groups.assert_called_once_with(self.users)

                    # Verify _handle_publish_subscription was called with correct parameters
                    mock_publish.assert_called_once_with(
                        last_current_index=0,
                        last_success_count=0,
                        segment_user_file_name='file.csv',
                        metadata_group_mappings=metadata_groups,
                        user_metadata_property_name="province"
                    )

                    # Verify result
                    self.assertFalse(result['is_finished'])
                    self.assertEqual(result['success_count'], 0)
                    self.assertIsNone(result['error_message'])

    def test_handle_segment_manual_trigger_initial_without_smart_distribution(self):
        """Test handle_segment_manual_trigger for initial trigger without smart distribution"""
        # Create service with smart distribution disabled
        subscription_disabled = self.subscription.copy()
        subscription_disabled["smart_distribution"] = {"enabled": False}
        service = DummyService(subscription_disabled, self.action, self.organization)

        # Mock _handling_upload_segment_users_file to return filename and users
        with patch.object(service, '_handling_upload_segment_users_file',
                          return_value=('file.csv', self.users)) as mock_upload:
            # Mock _get_metadata_groups to return None (no smart distribution)
            with patch.object(service, '_get_metadata_groups') as mock_get_groups:
                mock_get_groups.return_value = None

                # Mock _handle_publish_subscription
                with patch.object(service, '_handle_publish_subscription') as mock_publish:
                    mock_publish.return_value = None  # No error

                    # Call the method with initial parameters
                    callback = MagicMock()
                    result = service.handle_segment_manual_trigger(
                        callback,
                        ["email", "province"],
                        last_current_index=0,
                        last_success_count=0
                    )

                    # Verify _handling_upload_segment_users_file was called correctly
                    mock_upload.assert_called_once_with(["email", "province"])

                    # Verify _get_metadata_groups was called with users
                    mock_get_groups.assert_called_once_with(self.users)

                    # Verify _handle_publish_subscription was called with correct parameters
                    # (without metadata_group_mappings and user_metadata_property_name)
                    mock_publish.assert_called_once_with(
                        last_current_index=0,
                        last_success_count=0,
                        segment_user_file_name='file.csv'
                    )

                    # Verify result
                    self.assertFalse(result['is_finished'])
                    self.assertEqual(result['success_count'], 0)
                    self.assertIsNone(result['error_message'])

    def test_handle_segment_manual_trigger_resumed(self):
        """Test handle_segment_manual_trigger for resumed trigger"""
        # Mock _get_users_in_csv_file to return users
        with patch.object(self.service, '_get_users_in_csv_file', return_value=self.users) as mock_get_users:
            # Mock _handle_manual_trigger
            with patch.object(self.service, '_handle_manual_trigger') as mock_handle_trigger:
                mock_handle_trigger.return_value = {
                    "is_finished": True,
                    "success_count": 5,
                    "error_message": None
                }

                # Call the method with resumed parameters
                callback = MagicMock()
                result = self.service.handle_segment_manual_trigger(
                    callback,
                    ["email", "province"],
                    last_current_index=10,
                    last_success_count=5,
                    segment_user_file_name='file.csv',
                    metadata_group_mappings={
                        "A": {"value": "A", "remaining_send": 91},
                        "B": {"value": "B", "remaining_send": 91},
                        "C": {"value": "C", "remaining_send": 18}
                    },
                    user_metadata_property_name="province"
                )

                # Verify _get_users_in_csv_file was called correctly
                mock_get_users.assert_called_once_with('file.csv')

                # Verify _handle_manual_trigger was called with correct parameters
                mock_handle_trigger.assert_called_once()

                # Verify result
                self.assertTrue(result['is_finished'])
                self.assertEqual(result['success_count'], 5)
                self.assertIsNone(result['error_message'])

    def test_handle_publish_subscription_with_smart_distribution(self):
        """Test _handle_publish_subscription with smart distribution parameters"""
        # Mock subscription client
        self.service.subscription_client = MagicMock()

        # Call the method with smart distribution parameters
        metadata_group_mappings = {
            "A": {"value": "A", "remaining_send": 91},
            "B": {"value": "B", "remaining_send": 91},
            "C": {"value": "C", "remaining_send": 18}
        }

        error = self.service._handle_publish_subscription(
            last_current_index=10,
            last_success_count=5,
            segment_user_file_name='file.csv',
            metadata_group_mappings=metadata_group_mappings,
            user_metadata_property_name="province"
        )

        # Verify no error was returned
        self.assertIsNone(error)

        # Verify subscription_client.update_data was called with correct parameters
        self.service.subscription_client.update_data.assert_called_once_with({
            "last_current_index": 10,
            "segment_user_file_name": 'file.csv',
            "metadata_group_mappings": metadata_group_mappings,
            "user_metadata_property_name": "province"
        })

        # Verify subscription_client.publish was called with correct parameters
        self.service.subscription_client.publish.assert_called_once_with({
            "last_current_index": 10,
            "last_success_count": 5,
            "segment_user_file_name": 'file.csv',
            "metadata_group_mappings": metadata_group_mappings,
            "user_metadata_property_name": "province"
        })


if __name__ == "__main__":
    unittest.main()
