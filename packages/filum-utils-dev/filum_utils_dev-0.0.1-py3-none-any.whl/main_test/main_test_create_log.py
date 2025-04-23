import unittest

from filum_utils_dev.clients.log import LogClient, LogType, StatusCode
from filum_utils_dev.enums import ObjectType, ParentType


class TestCreateLogClass(unittest.TestCase):
    def test_create_log(self):
        log_client = LogClient()

        default_log_data = {
            # "object_type": ObjectType.INSTALLED_SOURCE,
            # "object_id": 3188,
            "object_type": ObjectType.ACTION,
            "object_id": 3026,
            "parent_type": ParentType.AUTOMATED_ACTION,
            "parent_id": 885,
            "type": LogType.ERROR,
            "code": StatusCode.SYNC_ERROR,
            "title": "Test Log",
            "subtitle": "This log is for testing purpose",
            "error_data": {
                "random key": "random error"
            },
            "trigger_data": {
                "subscription": {
                    "id": 1,
                    "data": {
                        "distribution_id": 123,
                        "trigger_data": {
                            "key 1": "value 1"
                        },
                        "triggered_source": {
                            "source data": "source value"
                        }
                    }
                },
                "automated_action": {
                    "id": 885,
                    "name": "Test Automated Action"
                }
            },
            "member_account_id": None,
            "member_organization_id": "e3375f64-88b8-48af-877b-2e5e03d3ca07"
        }

        log_client.create_log(**default_log_data)
