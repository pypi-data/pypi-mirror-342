import unittest

from filum_utils_dev import CampaignSubscriptionService
from filum_utils_dev.types.common import MessagePayload
from filum_utils_dev.types.organization import Organization


def trigger_function(action, campaign, data, subscription_data, organization):
    for user in data:
        print(user)

    return {
        "success_count": 0
    }


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
                # "file_name": "Users_1000_Rows.xlsx",
                "file_name": "users_1000_rows.csv",
                # "file_name": "danh_sach_nhan_vien.csv"
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
        "service_account_info": {
            "type": "service_account",
            "project_id": "filum-bdp-dev",
            "private_key_id": "2cbd4ee010ea0a11be3dfea8c7f9e33ba478c09e",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC6sIO+KBS3v8oO\ngB0E9b1XElVzzLwlDTT2+QMw6lsxXPntQbdL3tQphfnZLpLxXnT86R6kM0rEuhGC\n8y87eHVTCB2QlmB7RrGdTbzoPuSjoiQGZfSwozDzI1Z4bmvMzz5QQd+LEGPQHgTV\njk7s8UJXpIxVxLXnd33hBWgXVvHt0P9+LFPHH/PMSzUmXQVElENZM3w8E1IxFAO6\n5XUDLLQBeuKjFysVJijvsk77waxtNSggmYBDyG6IvcMcb+YVy/hfdhV7dbW+Yn+h\nDxFVSd4bUYVV2R0JsicKwqS3O2PREs0+aWaw0I3XfXsJC7+HqYiF2Sj4lNim3I8G\nuGvJeH0jAgMBAAECggEALp4XN6uwiLXGkdph5LQsZIq6deEg9iuXFzjVGCjdPrVV\n323yhGqPFhNTcW0U2lrY4bKgqSX5vKgt6UIqgDIzMdmr8EfsrbvYbExWKLRTyZya\nXFKnSFhnx78CP65rEsiJaecZGBOuqPBmCqGvibEw/MulE2G8fqEy+Lat6G4YmWaS\nr6Xt3+vViebj086/WS5pHl0+UBmJ7Lf3qGDZqouqSa+16lhYRRyQaQ6qwc6M5CEl\nEaoac6QbYEc+xf5swuPaca0YRamuUAbyQ9alvpTTJ6kr7g8FeKQPkXbXtnGvs2fM\nTg4bfa8qQ3+CmpYKRA7So9y8LASRb6NtjAzTTiEs8QKBgQDj4dgCK/tLw1cduA5+\nUouKztoCoN/frgiKJMpRyKptwmXhFLbToWvnSBdw312hNTzy1KCZ8DMx0KYr2L9N\nWYhb3lwhmP7Xg7fH9jHJvNuG6hCW0mZOKII/rq+/MTQOzD7i3DXUwFpUazFQMRwv\nxlRm4vVv+K+j62nt7WtQIs4HOwKBgQDRuYKFOxFMctHOVdD1CwEZE+jdd3lvMQeO\n6w5TPy5V/lnLkiBqA2mTnXOLLeABOkjAagkiroYAIJAe1vuH9gZM917okBKYjybD\nUy+Zs+Q3PdNbnusofSQTAu7KGL1KdVNRXVx75sC3vyWrAZlawTS9OlcvI/Tzl0hv\n1MNFTzaTOQKBgQCimF0Qx6LpHvrEqLQmq+0G4KqrH3A9YCaVssRs8DmyUPdyTt5Y\nSB/+iPC4x5c91Ael19Kzo7BTheVa+a8dmJlzu0ePbWPAECqMUXyazdbw/4dQpdT7\nRWoR2ClryMa1HERuh+Mc5xZMj6NC7ZeH+wHz21J2T0G7Oth9PF7KcdsBSwKBgG6S\nqS8HUnqE+vsXocDgWWbYaWkCicLHDd4bLgVUBWEPZlZ/J5ndTLeoRvf1auoayaqw\n/ToM29eLU5D+9cTcQLwpnB9vfm5y4xQOcsVN5B//98SRiBhjyjY/0Jg67Oop65C1\ncYJdyfPW0sxTXoBL5ztxW/AdvBMGCwnzGjUbq4F5AoGBANJK3llW2T0qlL0RD6VB\nLCIr6bC8ogGKkzF/aQnyqTv5Ndle//hwOOqrdhT4fpPmi2tLemf926/RpkTaLL44\nTPzD424+/rX2kelykkCt1WyW2U/yEiyzUirXJEB7bvcrs6IzAyuuV+uIZpVrMwdC\nOkvzBiXuKoCV3ns+ecOQZRIR\n-----END PRIVATE KEY-----\n",
            "client_email": "super-admin@filum-bdp-dev.iam.gserviceaccount.com",
            "client_id": "110959741530660797756",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/super-admin%40filum-bdp-dev.iam.gserviceaccount.com"
        }
    },
    "data": {}
}


class TestManualCampaignByFile(unittest.TestCase):
    organization = Organization(
        id=message_payload.get("organization_id", ""),
        slug=message_payload.get("organization_slug", "")
    )

    def test_trigger(self):
        campaign_service = CampaignSubscriptionService(
            campaign=message_payload.get("campaign"),
            subscription=message_payload.get("subscription"),
            action=message_payload.get("action"),
            organization=self.organization
        )

        campaign_service.handle_file_manual_trigger(
            trigger_function, 3
        )
