import unittest

from filum_utils_dev.clients.filum import FilumClient
from filum_utils_dev.services.file import FileService


class TestCaseClass(unittest.TestCase):
    def test_replace(self):
        default_str = "automated_action"
        print(default_str.replace("_", " "))

    def test_decode(self):
        # Sample UTF-8 encoded string
        utf8_string = b'\xe5\xae\x89\xe5\xbe\xbdabc\xe6\xb5\x8b\xe8\xaf\x95'

        # Decode UTF-8 to Unicode (UTF-8)
        decoded_utf8 = utf8_string.decode('utf-8')
        print(decoded_utf8)

        # Encode Unicode (UTF-8) to UTF-16
        encoded_utf16 = decoded_utf8.encode('utf-16')

        # Decode UTF-16 to get the final string
        decoded_utf16 = encoded_utf16.decode('utf-16')

        print(decoded_utf16)

    def test_file(self):
        # file_name = "Relation NPS-e9a7ba9b-6210-48f3-bd66-a276e2fb0ecf.csv"
        file_name = "20230920 Amazing Co contacts-1bbad504-5ea4-4cf3-9235-72194b13e0e7.csv"
        # file_name = "Filum+example+-+Contacts 2-5f761cad-ee67-4996-b2c5-6b5efd327687.csv"
        filum_client = FilumClient()
        file_content_bytes = filum_client.get_uploaded_file(file_name)
        users = FileService.get_rows(
            file_name,
            file_content_bytes,
            current_index=0
        )

        for user in users:
            print(user)