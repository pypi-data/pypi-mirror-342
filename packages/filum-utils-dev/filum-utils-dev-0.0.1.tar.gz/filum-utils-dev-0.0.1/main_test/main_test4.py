import datetime
import unittest

from dateutil.tz import gettz

from filum_utils_dev import CampaignSubscriptionService
from filum_utils_dev.clients.filum import FilumClient
from filum_utils_dev.types.common import MessagePayload

message_payload: MessagePayload = {
    "organization_id": "random_org_id",
    "organization_slug": "random_org_slug",
    "subscription": {
        "id": "subscription_id",
        "data": {
            "last_current_row": 3,
            "input_data": {
                "sender_name": "Long Nguyen",
                "reply_to_email": "long@filum.ai"
            },
            "trigger_data": {
                # "file_name": "users_1000_rows.xlsx",
                "file_name": "users_1000_rows.csv",
            }
        }
    },
    "campaign": {
        "id": "campaign_id",
        "name": "My Campaign",
        "account": {
            "id": "account_id",
            "full_name": "My Name from account",
            "email": "nhlong@filum.ai"
        },
        "survey": {
            "input_data": {
                "company": "From Filum with love",
                "target": "Our Customer"
            },
            "questions": [
                {
                    "id": "question_1",
                    "name": "Question 1"
                },
                {
                    "id": "question_2",
                    "name": "Question 2"
                }
            ]
        },
        "data": {}
    },
    "action": {
        "id": 1,
        "data": {
            "data_key": "data_value"
        },
        "action_type": {
            "id": 1,
            "internal_data": {
                "internal_key": "internal_value"
            }
        },
        "service_account_info": None
    },
    "data": {}
}


def trigger_fn_for_test(action, campaign, data, subscription_data, organization):
    print("Total Users")
    print(len(data))
    print("===========")
    return {
        "success_count": 1
    }


class TestManualCampaignByFile(unittest.TestCase):
    def test_get_expiration_time(self):
        expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)
        print(expiration_time.timestamp())

    def test_download_file(self):
        filum_client = FilumClient()

        # file_name = "aaa2a81b652341c09f2dbb54f83a31ec.xls"
        start_time = datetime.datetime.now()
        file_name = "Users_1000_Rows.xlsx"
        # file_name = "danh_sach_don_hang_theo_san_pham_15.09.2022_09ca93ccf12f4505dee931b30be79e4d.xlsx"
        # file_name = "don_hang.xlsx"
        filum_client.get_uploaded_file(file_name)
        end_time = datetime.datetime.now()

        print(end_time - start_time)

    def test_handle_manual_by_file(self):
        campaign = message_payload.get("campaign") or {}
        subscription = message_payload.get("subscription") or {}
        action = message_payload.get("action") or {}
        organization = {
            "id": message_payload["organization_id"],
            "slug": message_payload["organization_slug"]
        }
        campaign_service = CampaignSubscriptionService(
            campaign, subscription, action, organization
        )

        campaign_service.handle_file_manual_trigger(
            process_file_manual_fn=trigger_fn_for_test,
            last_current_index=0
        )
