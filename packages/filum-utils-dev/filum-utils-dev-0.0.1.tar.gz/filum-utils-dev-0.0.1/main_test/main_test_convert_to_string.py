import unittest


def random_func(data: str):
    print(type(data))
    print(data)


class BaseTestClass(unittest.TestCase):
    def test_params_in_func(self):
        default_data = {
            "key 1": "value 1",
            "key 2": "value 2"
        }

        random_func(data=default_data)
