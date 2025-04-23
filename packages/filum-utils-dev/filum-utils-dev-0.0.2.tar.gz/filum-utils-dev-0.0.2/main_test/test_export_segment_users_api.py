import unittest

from filum_utils_dev.clients.filum import FilumClient
from filum_utils_dev.types.organization import Organization


class TestExportSegmentUserClass(unittest.TestCase):
    def test_export_segment_users(self):
        filum_client = FilumClient()
        custom_properties = [
            "Latest Transaction Timestamp",
            "Number of Transactions",
            "Average Review Rating",
        ]
        segment_id = "44135c81-425d-4fdc-a40f-6750602d2fb2"
        organization = Organization(
            id="8706c5ac-c255-43ea-bf01-58d238e8c086",
            slug="workspace-account-1068"
        )
        rows = filum_client.get_user_csv_reader(
            custom_properties=custom_properties,
            segment_id=segment_id,
            organization=organization,
            limit=100,
            offset=0,
        )

        print(rows)

        for row in rows:
            print(row)
