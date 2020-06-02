from datetime import datetime
import queue
import unittest

from api.emulation.task_queue import TaskQueue


class TestTaskQueue(unittest.TestCase):

    def test_add_task(self):
        task_queue = TaskQueue()
        task = {
            'emulation_time': 10,
            'dasl_filename': 'dsal1.yaml',
            'data_setting': '',
            'report_name': 'report1.json'
        }
        response = task_queue.add_task(task)
        self.assertTrue('emulation_task_id' in response)
        self.assertEqual(response['emulation_time'], task['emulation_time'])
        self.assertEqual(response['dasl_filename'], task['dasl_filename'])
        self.assertEqual(response['data_setting'], task['data_setting'])
        self.assertEqual(response['report_name'], task['report_name'])

    def test_get_all_tasks(self):
        task_queue = TaskQueue()
        task1 = {
            'emulation_time': 10,
            'dasl_filename': 'dsal1.yaml',
            'data_setting': '',
            'report_name': 'report1.json'
        }
        task2 = {
            'emulation_time': 10,
            'dasl_filename': 'dsal1.yaml',
            'data_setting': '',
            'report_name': 'report1.json'
        }
        task_queue.queue.put(task1)
        task_queue.queue.put(task2)
        
        expected_tasks = task_queue.get_all_tasks()
        correct_tasks = [task1, task2]
        self.assertEqual(expected_tasks, correct_tasks)

    def test_get_first_task(self):
        task_queue = TaskQueue()
        task = {
            'emulation_time': 10,
            'dasl_filename': 'dsal2.yaml',
            'data_setting': '',
            'report_name': 'report3.json'
        }
        task_queue.queue.put(task)
        first_task = task_queue.get_first_task()
        self.assertEqual(first_task['emulation_time'], task['emulation_time'])
        self.assertEqual(first_task['dasl_filename'], task['dasl_filename'])
        self.assertEqual(first_task['data_setting'], task['data_setting'])
        self.assertEqual(first_task['report_name'], task['report_name'])

    def test_get_pending_task_size(self):
        task_queue = TaskQueue()
        task = {
            'emulation_time': 10,
            'dasl_filename': 'dsal2.yaml',
            'data_setting': '',
            'report_name': 'report3.json'
        }
        task_queue.queue.put(task)
        task_queue.queue.put(task)
        self.assertEqual(task_queue.get_pending_task_size(), 2)

    def test_cancel_pending_task(self):
        task_queue = TaskQueue()
        task1 = {
            'emulation_task_id': '1',
            'emulation_time': 10,
            'dasl_filename': 'dsal1.yaml',
            'data_setting': '',
            'report_name': 'report1.json'
        }
        task2 = {
            'emulation_task_id': '2',
            'emulation_time': 10,
            'dasl_filename': 'dsal2.yaml',
            'data_setting': '',
            'report_name': 'report3.json'
        }
        task_queue.queue.put(task1)
        task_queue.queue.put(task2)
        response = task_queue.cancel_pending_task(task2['emulation_task_id'])
        self.assertEqual(response, task2)
        self.assertEqual(task_queue.queue.qsize(), 1)

if __name__ == "__main__":
    unittest.main()
