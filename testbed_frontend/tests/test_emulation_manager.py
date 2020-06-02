import os
import unittest
from unittest.mock import patch
import time

from api.emulation.emulation_manager import EmulationManager
from api.emulation.utils import json_resolver
from .mock_class import MockRedis


class EmulationManagerTest(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = 'tests/test-data/emulation_manager'

    @patch('redis.StrictRedis', MockRedis)
    def test_init(self):
        emulation_manager = EmulationManager()
        emulation_data = json_resolver.read_json(os.path.join(self.test_data_dir, 'emulation_data.json'))

        emulation_manager.init(emulation_data=emulation_data)
        expected = emulation_manager.redis_connection.data
        correct = json_resolver.read_json(os.path.join(self.test_data_dir, 'redis_init.json'))
        self.assertEqual(expected, correct)

    @patch('redis.StrictRedis', MockRedis)
    @patch('api.emulation.emulation_manager.EmulationManager.check_worker_status')
    def test_ready(self, mock_check_worker_status):
        mock_check_worker_status.side_effect = [False, True]
      
        emulation_manager = EmulationManager()
        emulation_manager.ready()

        self.assertEqual(mock_check_worker_status.call_count, 2)

    @patch('redis.StrictRedis')
    @patch('api.emulation.emulation_manager.EmulationManager.check_worker_status')
    @patch('api.emulation.emulation_handler.abort_handled')
    def test_start(self, mock_abort_handled, mock_check_worker_status, mock_redis):
        mock_abort_handled.side_effect = None
        mock_redis.side_effect = MockRedis

        mock_check_worker_status.side_effect = [False, True]

        emulation_manager = EmulationManager()
        emulation_manager.start()

        self.assertEqual(mock_redis.call_count, 1)
        self.assertEqual(mock_check_worker_status.call_count, 2)

    @patch('redis.StrictRedis')
    def test_finish(self, mock_redis):
        emulation_manager = EmulationManager()
        emulation_manager.finish()

        self.assertEqual(mock_redis.return_value.set.call_count, 1)

    @patch('redis.StrictRedis')
    def test_check_worker_status(self, mock_redis):
        mock_redis.side_effect = MockRedis

        emulation_manager = EmulationManager()
        emulation_manager.ip_collection = ['10.52.52.106', '10.52.52.107']
        emulation_manager.redis_connection.hset('10.52.52.106', 'worker_status', '2')
        emulation_manager.redis_connection.hset('10.52.52.107', 'worker_status', '1')
        expected = emulation_manager.check_worker_status('2')
        self.assertEqual(expected, False)


if __name__ == '__main__':
    unittest.main()
