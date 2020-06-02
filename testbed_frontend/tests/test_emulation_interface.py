"""
Test the emulation interface in api/emulation/emulation_interface.py
"""
from functools import wraps
import os
import unittest
from unittest.mock import patch, PropertyMock
import redis
from .mock_class import MockRedis

def mock_decorator(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        return fun(*args, **kwargs)
    return wrapper

patch('api.emulation.emulation_handler.abort_handled', mock_decorator).start()

from api.emulation import Config
from api.emulation.emulation_interface import EmulationInterface


class TestEmulationInterface(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = 'tests/test-data/emulation-interface'

    @patch('api.emulation.utils.generator.generate_emulation_data')
    @patch('api.emulation.utils.transformer.transform_kind_qos')
    def test__generate_emultaion_data(self, mock_transform_kind_qos, mock_generate_emulation_data):
        mock_task = {
            'data_setting': {},
            'emulation_time': {}
        }
        emulation_interface = EmulationInterface()
        emulation_interface._generate_emultaion_data(emulation_task=mock_task)
        mock_transform_kind_qos.assert_called_once()
        mock_generate_emulation_data.assert_called_once()

    @patch('api.emulation.emulation_manager.EmulationManager.finish')
    @patch('api.emulation.emulation_manager.EmulationManager.start')
    @patch('api.emulation.emulation_manager.EmulationManager.ready')
    @patch('api.emulation.emulation_manager.EmulationManager.init')
    def test__start_emulation(self, mock_init, mock_ready, mock_start, mock_finish):
        # mock functions
        def do_nothing(something=None):
            return None
        mock_init.side_effect = do_nothing
        mock_ready.side_effect = do_nothing
        mock_start.side_effect = do_nothing
        mock_finish.side_effect = do_nothing

        # test function
        emulation_interface = EmulationInterface()
        emulation_interface._start_emulation()
        mock_init.assert_called_once()
        mock_ready.assert_called_once()
        mock_start.assert_called_once()
        mock_finish.assert_called_once()


    @patch('api.emulation.utils.parser.ReportGenerator')
    def test__parse_device_report(self, mock_report_generator):
        mock_report_generator.return_value.generate_performance_report.return_value = {}
        mock_report_generator.return_value.save_performance_report.return_value = {}

        emulation_interface = EmulationInterface()
        emulation_interface.emulation_data = {'ip:10.52.52.106': {}, 'ip:10.52.52.107': {}}
        emulation_interface._parse_device_report(dsal_filename='dasl.yaml', report_name='report')
        mock_report_generator.assert_called_once()
        mock_report_generator.return_value.generate_performance_report.assert_called_once()
        mock_report_generator.return_value.save_performance_report.assert_called_once()

    @patch('api.emulation.emulation_interface.EmulationInterface._init_redis_table')
    @patch('api.emulation.emulation_interface.EmulationInterface._parse_device_report')
    @patch('api.emulation.emulation_interface.EmulationInterface._start_emulation')
    @patch('api.emulation.emulation_interface.EmulationInterface._generate_emultaion_data')
    @patch('redis.StrictRedis')
    def test_execute_emulation(self, mock_redis, mock__generate_emultaion_data, mock__start_emulation,
                               mock__parse_device_report, mock__init_redis_table):
        mock_redis.side_effect = MockRedis
        mock__generate_emultaion_data.side_effect = None
        mock__start_emulation.side_effect = None
        mock__parse_device_report.side_effect = None
        mock__init_redis_table.side_effect = None

        emulation_interface = EmulationInterface()
        emulation_task = {'dsal_filename': 'dsal1.yaml', 'report_name': 'report'}
        emulation_interface.execute_emulation(emulation_task)

        mock__generate_emultaion_data.assert_called_once()
        mock__start_emulation.assert_called_once()
        mock__parse_device_report.assert_called_once()
