from datetime import datetime
import unittest
from unittest.mock import patch, PropertyMock, Mock

import redis
from .mock_class import MockRedis
from api.emulation import EmulationStatus, WorkerStatus
from api.emulation.task_worker import TaskWorker
from api.emulation.emulation_interface import EmulationInterface


class TestTaskWorker(unittest.TestCase):
    def test_execute_task(self):
        task_worker = TaskWorker()
        task_id = datetime.now().strftime('%Y%m%d%Y%H%M%S')
        task = {
            'emulation_task_id': task_id,
            'emulation_time': 10,
            'dsal_filename': 'dsal1.yaml',
            'data_setting': '',
            'report_name': 'report1.json'
        }

        with patch.object(EmulationInterface, 'execute_emulation', return_value=None) as mock_method:
            task_worker.execute_task(task)

        mock_method.assert_called_once_with(task)

    def test_get_executing_task_id(self):
        task_worker = TaskWorker()
        task_id = datetime.now().strftime('%Y%m%d%Y%H%M%S')
        task = {
            'emulation_task_id': task_id,
            'emulation_time': 10,
            'dsal_filename': 'dsal1.yaml',
            'data_setting': '',
            'report_name': 'report1.json'
        }
        with patch.dict(task_worker.executing_task, task, clear=True):
            self.assertEqual(task_worker.get_executing_task_id(), task_id)

    @patch('time.sleep')
    @patch('api.emulation.emulation_interface.EmulationInterface.emulation_data', new_callable=PropertyMock)
    @patch('redis.StrictRedis')
    def test_abort_executing_task(self, mock_redis, mock_emulation_data, mock_sleep):
        MockRedis.hget = lambda _, x, y: WorkerStatus.WAIT
        mock_redis.side_effect = MockRedis
        mock_emulation_data.return_value = {'ip:10.52.52.6': ''}
        mock_sleep.side_effect = None

        task_worker = TaskWorker()
        task_id = datetime.now().strftime('%Y%m%d%Y%H%M%S')
        task = {
            'emulation_task_id': task_id,
            'emulation_time': 10,
            'dsal_filename': 'dsal1.yaml',
            'data_setting': '',
            'report_name': 'report1.json'
        }

        task_worker.executing_task = task
        aborted_task = task_worker.abort_executing_task()
        self.assertEqual(task_worker.redis_connection.get('emulation_status'), EmulationStatus.INIT)
        correct = {
            'emulation_task_id': '0',
            'emulation_time': 0,
            'dsal_filename': '',
            'data_setting': '',
            'report_name': ''
        }
        self.assertDictEqual(aborted_task, correct)

    @patch('redis.StrictRedis.get')
    def test_get_executing_task_status(self, mock_redis_get):

        data = {'emulation_status': EmulationStatus.START}

        def get(key):
            return data[key]
        mock_redis_get.side_effect = get

        task_worker = TaskWorker()
        self.assertEqual(task_worker.get_executing_task_status(), EmulationStatus.START)
