import unittest
from typing import List, Any, Dict
from uuid import uuid4

from filum_utils_dev import StringFormatter


def count_items_in_list(default_mappings_list: List[Dict[str, Any]], limit_number_of_item: int = None):
    total_counted_items = 0

    count_item_mappings_list = []
    for idx, item in enumerate(default_mappings_list):
        total_counted_items += 1
        count_item_mappings_list.append(item)
        if is_exceeded_limit(total_counted_items, limit_number_of_item):
            break

    # print(f"Total Items: {total_counted_items} item(s)")
    print(count_item_mappings_list)


def is_exceeded_limit(current_number: int, limit_number_of_item: int = None) -> bool:
    if limit_number_of_item is None:
        return False

    return current_number >= limit_number_of_item


class TestValidateLimitClass(unittest.TestCase):
    def test_data(self):
        response_id = "rid_preview"
        response_id = str(uuid4())
        formatted_str = StringFormatter.encode_str_in_url(response_id)
        print(formatted_str)

    def test_validate_limit_class(self):
        item_mappings_list = []
        for i in range(0, 10):
            item_mappings = {f"item_{i}": f"value_{i}"}
            item_mappings_list.append(item_mappings)

        limit_number_of_item = 5
        count_items_in_list(item_mappings_list, limit_number_of_item)
