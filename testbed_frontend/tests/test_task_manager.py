import datetime
import time
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from api.emulation import EmulationStatus
from api.emulation.task_manager import TaskManager
from api.emulation.task_queue import TaskQueue
from api.emulation.task_worker import TaskWorker


class TestTaskManager(unittest.TestCase):
    @patch('redis.StrictRedis')
    @patch('time.sleep')
    def test_get_available_device(self, mock_time_sleep, mock_redic_StrictRedis):
        # Remove sleep function
        mock_time_sleep.return_value = MagicMock()
        def scan_iter(ip):
            return ['ip:10.52.52.106', 'ip:10.52.52.107']
        mock_redic_StrictRedis.return_value.scan_iter.side_effect = scan_iter
        current_time = datetime.datetime.now()
        current_time_plus_one_second = current_time + datetime.timedelta(seconds=1)
        mock_redic_StrictRedis.return_value.time.return_value = [time.mktime(current_time.timetuple())]
        mock_redic_StrictRedis.return_value.hget.return_value = time.mktime(current_time_plus_one_second.timetuple())

        task_manager = TaskManager()

        expect = task_manager.get_available_device()
        correct = ['ip:10.52.52.106', 'ip:10.52.52.107']
        self.assertEqual(expect, correct)

    @patch('api.emulation.task_manager.TaskManager.get_executing_task_status')
    @patch('api.emulation.task_worker.TaskWorker.executing_task', new_callable=PropertyMock)
    @patch('api.emulation.task_queue.TaskQueue.get_all_tasks')
    def test_get_all_tasks(self, mock_get_all_tasks, mock_executing_task, mock_get_executing_task_status):
        task = {
            'emulation_task_id': datetime.datetime.now().strftime('%Y%m%d%Y%H%M%S'),
            'emulation_time': 11111,
            'dasl_filename': 'dsal1.yaml',
            'data_setting': '',
            'report_name': 'report1.json'
        }
        executing_task = {
            'emulation_task_id': datetime.datetime.now().strftime('%Y%m%d%Y%H%M%S'),
            'emulation_time': 10,
            'dasl_filename': 'dsal1.yaml',
            'data_setting': '',
            'report_name': 'report1.json'
        }
        mock_get_all_tasks.return_value = [task]
        mock_executing_task.return_value = executing_task
        mock_get_executing_task_status.return_value = EmulationStatus.INIT

        task_manager = TaskManager()
        executing_task.update({'emulation_status': EmulationStatus.INIT})
        correct = [executing_task, task]
        self.assertEqual(task_manager.get_all_tasks(), correct)

    def test_add_task_into_queue(self):
        task_manager = TaskManager()
        task = {
            'emulationTaskId': datetime.datetime.now().strftime('%Y%m%d%Y%H%M%S'),
            'emulationTime': 10,
            'daslFilename': 'dsal1.yaml',
            'dataSetting': '',
            'reportName': 'report1.json'
        }
        new_task = task_manager.add_task_into_queue(task)
        self.assertEqual(new_task, task)

    def test_get_task_size(self):
        task_manager = TaskManager()
        task = {
            'emulationTaskId': datetime.datetime.now().strftime('%Y%m%d%Y%H%M%S'),
            'emulationTime': 10,
            'daslFilename': 'dsal1.yaml',
            'dataSetting': '',
            'reportName': 'report1.json'
        }
        task_manager.task_queue.queue.put(task)
        self.assertEqual(task_manager.get_task_size(), 1)

    @patch('api.emulation.task_manager.TaskManager._cancel_task_from_queue')
    @patch('api.emulation.task_worker.TaskWorker.get_executing_task_id')
    def test_delete_task_that_is_pending(self, mock_get_executing_task_id, mock__cancel_task_from_queue):
        task_manager = TaskManager()
        task_id = 'test_task_id'
        mock_get_executing_task_id.return_value = 'test_task_id_123'
        task_manager.delete_task(task_id)
        mock__cancel_task_from_queue.assert_called_once()

    @patch('api.emulation.task_manager.TaskManager._abort_executing_task')
    @patch('api.emulation.task_worker.TaskWorker.get_executing_task_id')
    def test_delete_task_that_is_executing(self, mock_get_executing_task_id, mock__abort_executing_task):
        task_manager = TaskManager()
        task_id = 'test_task_id'
        mock_get_executing_task_id.return_value = 'test_task_id'
        task_manager.delete_task(task_id)
        mock__abort_executing_task.assert_called_once()

    @patch('time.sleep')
    @patch('api.emulation.task_worker.TaskWorker.execute_task')
    @patch('api.emulation.task_queue.TaskQueue.get_first_task')
    @patch('api.emulation.task_queue.TaskQueue.get_pending_task_size')
    @patch('api.emulation.task_manager.TaskManager._manager_is_running')
    @patch('api.emulation.task_manager.TaskManager.wait_task')
    def test__exectue_task(self, mock_wait_task, mock__manager_is_running, mock_get_pending_task_size, 
        mock_get_first_task, mock_execute_task, mock_sleep):
        mock_wait_task.side_effect = None
        mock__manager_is_running.side_effect = [True, False]
        mock_get_pending_task_size.return_value = 1
        mock_get_first_task.side_effect = None
        mock_execute_task.side_effect = None
        mock_sleep.side_effect = None

        task_manager = TaskManager()
        task_manager._exectue_task()

        mock_get_first_task.assert_called_once()
        mock_execute_task.assert_called_once()

    @patch('api.emulation.task_worker.TaskWorker.abort_executing_task')
    def test__abort_executing_task(self, mock_abort_executing_task):
        task_manager = TaskManager()
        task_manager._abort_executing_task()

        mock_abort_executing_task.assert_called_once()

    @patch('api.emulation.task_queue.TaskQueue.cancel_pending_task')
    def test__cancel_task_from_queue(self, mock_cancel_pending_task):
        task_manager = TaskManager()
        task_manager._cancel_task_from_queue(task_id='123')

        mock_cancel_pending_task.assert_called_once()

    @patch('api.emulation.task_worker.TaskWorker.executing_task', new_callable=PropertyMock)
    def test_get_executing_task(self, mock_executing_task):
        task_manager = TaskManager()
        task_manager.get_executing_task()

        mock_executing_task.assert_called_once()

    @patch('api.emulation.task_worker.TaskWorker.get_executing_task_status')
    def test_get_executing_task_status(self, mock_get_executing_task_status):
        task_manager = TaskManager()
        task_manager.get_executing_task_status()

        mock_get_executing_task_status.assert_called_once()

if __name__ == "__main__":
    unittest.main()
