"""

Example:
    python -m unittest tests.test_report_parser.ReportGeneratorTest

    python -m unittest tests.test_report_parser.PerformaceReportTest
"""
import json
import os
import unittest
from unittest.mock import patch

from api.emulation.utils import parser, json_resolver
from .mock_class import MockRedis

class ReportGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = 'tests/test-data/test_report_parser'

    @patch('redis.StrictRedis')
    def test_generate_performance_report(self, mock_redis):
        mock_redis.side_effect = MockRedis
        report_generator = parser.ReportGenerator()
        
        # set data into mock redis
        device_names = ['device1', 'device2']
        ip_collection = ['ip:10.52.52.106', 'ip:10.52.52.107']
        for i, ip in enumerate(ip_collection):
            report_path = os.path.join(self.test_data_dir, 'device_reports', 'device_report_{}.json'.format(i+1))
            device_report = json_resolver.read_json(report_path)
            report_generator.redis_connection.hset(ip, 'device_report', json.dumps(device_report))
            report_generator.redis_connection.hset(ip, 'device_name', device_names[i])
        
        # test if the function behavior is correct
        expected = report_generator.generate_performance_report(ip_collection)
        correct_test_report_path = os.path.join(self.test_data_dir, 'test_performance_report.json')
        correct = json_resolver.read_json(correct_test_report_path)
        self.assertEqual(expected, correct)


class PerformaceReportTest(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = 'tests/test-data/test_report_parser'

    @patch('api.emulation.utils.parser.PerformanceReport._set_report')
    def test_set_performance_report(self, mock__set_report):
        performance_report = parser.PerformanceReport()

        # read test data
        PARSED_REPORT_PATH = os.path.join(self.test_data_dir, 'parsed_report.json')
        PARSED_RESOURCE_USAGE_PATH = os.path.join(self.test_data_dir, 'parsed_resource_usage.json')
        parsed_report = json_resolver.read_json(PARSED_REPORT_PATH)
        parsed_resource_usage = json_resolver.read_json(PARSED_RESOURCE_USAGE_PATH)

        # test if the function behavior is correct
        performance_report.set_performance_report(parsed_report, parsed_resource_usage)
        self.assertEqual(mock__set_report.call_count, len(parsed_report.values()))

    def test__set_report(self):
        performance_report = parser.PerformanceReport()

        # read test data
        PARSED_REPORT_PATH = os.path.join(self.test_data_dir, 'parsed_report.json')
        PARSED_RESOURCE_USAGE_PATH = os.path.join(self.test_data_dir, 'parsed_resource_usage.json')
        parsed_report = json_resolver.read_json(PARSED_REPORT_PATH)
        parsed_resource_usage = json_resolver.read_json(PARSED_RESOURCE_USAGE_PATH)

        # test if the function behavior is correct
        performance_report.set_performance_report(parsed_report, parsed_resource_usage)

        CORRECT_PERFORMANCE_REPORT_PATH = os.path.join(self.test_data_dir, 'test__set_performance_report.json')
        correct = json_resolver.read_json(CORRECT_PERFORMANCE_REPORT_PATH)
        self.assertEqual(performance_report.performance_report, correct)

    def test_get_json(self):
        performance_report = parser.PerformanceReport()

        performance_report._performance_report = ['report1', 'report2']

        correct_report = {
            'report': ['report1', 'report2']
        }

        self.assertEqual(performance_report.get_json(), correct_report)
