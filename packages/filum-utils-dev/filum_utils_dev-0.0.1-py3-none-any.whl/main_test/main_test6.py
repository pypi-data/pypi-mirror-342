import random
import time
import unittest

from tenacity import wait_fixed, stop_after_attempt, retry, wait_exponential, wait_incrementing, stop_after_delay

from filum_utils_dev.errors import BaseError


_RETRY_PARAMS = {
    "reraise": True,
    "wait": wait_exponential(
        multiplier=2,
    ),
    "stop": stop_after_delay(60),
}


class TestCaseClass(unittest.TestCase):
    def test_split_func(self):
        default_str = "Hello World!!! "
        data_dict = {"key": default_str.strip()}
        print(data_dict)


    old_time = time.time()

    @retry(**_RETRY_PARAMS)
    def test_wait_exponential_1(self):
        run_at = time.time()
        print(run_at - self.old_time)
        self.old_time = run_at
        print("------------------------------")
        # print(
        #     "Wait 2^x * 2 second between each retry starting with 1 seconds, then up to 10 seconds, then 10 seconds afterwards"
        # )
        raise Exception

    def test_function(self):
        @retry(**_RETRY_PARAMS)
        def _random_raise_error():
            random_int = random.randint(1, 10)
            print(f"Random Int: {random_int}")
            if random_int != 1:
                print("You are so unlucky")
                raise BaseError(
                    message="You are so unlucky",
                )

        _random_raise_error()
