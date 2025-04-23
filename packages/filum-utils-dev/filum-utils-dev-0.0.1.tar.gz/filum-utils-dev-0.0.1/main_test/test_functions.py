import unittest
from unittest.mock import Mock, patch
from uuid import uuid4

from filum_utils_dev.services.subscription.campaign import CampaignSubscriptionService  # Replace with the actual class name

class TestCampaign(unittest.TestCase):

    def setUp(self):
        self.user_limit_per_trigger = 13
        self.subscription_service = CampaignSubscriptionService(
            campaign={
                "id": "1",
                "name": "Campaign Name"
            },
            subscription={
                "id": "11",
                "data": {
                    "user_limit_per_trigger": self.user_limit_per_trigger
                }
            },
            organization={
                "id": str(uuid4()),
                "slug": "test-organization-slug"
            },
            action={},
        )  # Replace with the actual class name

    @patch('filum_utils_dev.services.subscription.campaign.CampaignSubscriptionService._handle_trigger')
    @patch(
        'filum_utils_dev.services.subscription.campaign.CampaignSubscriptionService._handle_trigger_function_with_try_except'
    )
    @patch('filum_utils_dev.services.subscription.campaign.CampaignSubscriptionService._handle_publish_subscription')
    def test_handle_manual_trigger(
        self,
        mock_publish,
        mock_handle_trigger_with_try_except,
        mock_handle_trigger
    ):
        # Setup
        process_fn = Mock()
        last_current_index = 0
        last_success_count = 0
        channel_name = 'test_channel'

        object_record_limit = 10
        # number_of_user = 17
        users = []
        for i in range(0, object_record_limit):
            users.append({"id": f"User_ID_{i}"})

        mock_success_count = (
            object_record_limit
            if object_record_limit < self.user_limit_per_trigger
            else self.user_limit_per_trigger
        )

        mock_handle_trigger.return_value = {'success_count': mock_success_count}
        mock_handle_trigger_with_try_except.return_value = None
        mock_publish.return_value = None

        # Execute
        result = self.subscription_service._handle_manual_trigger(
            process_fn, users, object_record_limit, last_current_index, last_success_count, channel_name
        )

        # Assert
        self.assertFalse(result['is_finished'])
        # self.assertTrue(result['is_finished'])
        self.assertEqual(result['success_count'], mock_success_count)
        self.assertIsNone(result['error_message'])

        mock_handle_trigger.assert_called_once_with(process_fn=process_fn, data=users)
        # mock_exceeded_user_limit.assert_called_once_with(3)
        mock_publish.assert_called_once_with(last_current_index=object_record_limit, last_success_count=mock_success_count)

    # Add more test cases to cover different scenarios
    # For example, test when user limit is exceeded, when there are no more users, etc.

if __name__ == '__main__':
    unittest.main()