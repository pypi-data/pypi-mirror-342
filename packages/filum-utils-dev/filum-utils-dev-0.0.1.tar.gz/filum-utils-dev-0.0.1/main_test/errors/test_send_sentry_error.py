import unittest

from sentry_sdk import capture_exception, capture_message

from filum_utils_dev import DateTimeFormatter
from filum_utils_dev.sentry import SentryClient


class TestSendSentryError(unittest.TestCase):
    def test_catch_exception(self):
        sentry_client = SentryClient()
        sentry_client.setup()
        try:
            current_datetime_str = DateTimeFormatter.get_current_datetime_str()
            error_message = f"Test error at {current_datetime_str}"
            print(error_message)
            raise Exception(error_message)
        except Exception as e:
            capture_exception(e)
        sentry_client.close_connection()

    def test_catch_error_message(self):
        sentry_client = SentryClient()
        sentry_client.setup()

        current_datetime_str = DateTimeFormatter.get_current_datetime_str()
        error_message = f"This is test message at {current_datetime_str}"
        print(error_message)
        capture_message(error_message, level="error")
        # sentry_client.close_connection()
