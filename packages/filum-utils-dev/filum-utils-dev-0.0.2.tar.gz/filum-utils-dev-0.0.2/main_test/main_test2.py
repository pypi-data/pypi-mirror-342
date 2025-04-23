import unittest
from typing import Callable, Dict, Any

from filum_utils_dev.clients.filum import FilumClient


def my_new_func(param_1: str, random_func: Callable, **kwargs):
    print(param_1)
    print(kwargs)
    random_func(param_1=param_1, **kwargs)


def find_value(data: Dict[str, Any], selected_key: str):
    if not isinstance(data, dict):
        return None

    for key, value in data.items():
        if isinstance(value, dict):
            selected_value = find_value(value, selected_key)
            if selected_value is None:
                continue

            return selected_value

        if key != selected_key:
            continue

        return value


class TestCaseClass(unittest.TestCase):
    def test_get_key_in_child_dictionary(self):
        default_dict = {
            "zalo_auth_data": {
                "identifier1": "zalo_id",
                "identifier2": "zalo_id",
                "identifier3": "zalo_id",
                "identifier4": "zalo_id",
                "identifier5": "zalo_id",
                "identifier6": "zalo_id",
                "identifier7": "zalo_id",
                "identifier8": "zalo_id",
                "identifier": "zalo_id"
            },
            "identifier1": "zalo_id",
            "identifier2": "zalo_id",
            "identifier3": "zalo_id",
            "identifier4": "zalo_id",
            "identifier5": "zalo_id",
            "identifier6": "zalo_id",
            "identifier7": "zalo_id",
            "identifier8": "zalo_id",
            "identifier9": "zalo_id",
            "identifier10": "zalo_id",
            "identifier20": "zalo_id",
            "identifier30": "zalo_id",
            "identifier40": "zalo_id",
            "identifier50": "zalo_id",
            "identifier60": "zalo_id",
            "identifier70": "zalo_id",
            "identifier80": "zalo_id",
            "identifier90": "zalo_id"
        }
        default_dict = None
        value = find_value(default_dict, "identifier")
        print(value)

    def test_error_timeout(self):
        filum_client = FilumClient()
        filum_client.create_survey_responses()

    def test_some_random_func(self):
        def my_inside_func(param_1: str, param_2: str, param_3: str):
            print(param_1)
            print(param_2)
            print(param_3)

        my_new_func(
            param_1="Hey 1",
            random_func=my_inside_func,
            param_2="Hey 2",
            param_3="Hey 3"
        )

    def test_function(self):
        n = 5
        m = 4

        tasks = [1, 2, 3, 4, 5]

        task_process_rule = {
            "task_1": ["task_2", "task_3", "task_5"],
            # "task_2": ["task_5"],
            "task_3": ["task_4"],
            "task_5": ["task_3"],
            "task_4": ["task_2"]
        }

        list_task = []
        prefix_task_name = f"task_"
        for i in range(1, n + 1):
            list_task.append(f"{prefix_task_name}{i}")

        task_order = []
        completed_tasks = []

        self.process_task(list_task, task_process_rule, completed_tasks)

    def process_task(self, list_task, task_process_rule, completed_tasks):

        left_over_tasks = []
        for task_name in list_task:
            can_proceed = False
            for primary_task, sub_tasks in task_process_rule.items():
                if task_name not in sub_tasks:
                    can_proceed = True
                    continue

                # check if dependent task can be process
                if task_name in sub_tasks and primary_task not in completed_tasks:
                    can_proceed = False
                    break

                if task_name in sub_tasks and primary_task in completed_tasks:
                    can_proceed = True

            if not can_proceed:
                left_over_tasks.append(task_name)
                continue

            completed_tasks.append(task_name)
            print(task_name)

        if left_over_tasks:
            self.process_task(left_over_tasks, task_process_rule, completed_tasks)
