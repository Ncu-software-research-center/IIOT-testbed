import datetime
import os
import time
import unittest
from unittest.mock import patch, MagicMock

from api.emulation.utils import json_resolver
from api.emulation import Config


from api.emulation.utils import generator
from api.emulation.utils.transformer import transform_kind_qos


class GeneratorTest(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = 'tests/test-data/generator'
    
    def test__get_needed_topics(self):
        """
            Test the return value of _get_needed_topics which place in _get_avaliable_ip_address()
        """
        data_setting = json_resolver.read_json(os.path.join(self.test_data_dir, 'data_detting_2d_6t.json'))
        devices = data_setting['device']
        topics = data_setting['topic']

        for device in devices:
            expected_topics = generator._get_needed_topics(device, topics)

            path = os.path.join(self.test_data_dir, '{}_needed_topics.json'.format(device['name']))
            correct_topcis = json_resolver.read_json(path)

            self.assertEqual(expected_topics, correct_topcis)

    @patch('api.emulation.utils.generator._get_needed_topics')
    def test__get_computing_resource(self, mock__get_needed_topics):
        data_setting = json_resolver.read_json(os.path.join(self.test_data_dir, 'data_detting_2d_6t.json'))
        devices = data_setting['device']

        # Generate mock return value
        needed_topics = []
        for device in devices:
            path = os.path.join(self.test_data_dir, '{}_needed_topics.json'.format(device['name']))
            correct_topcis = json_resolver.read_json(path)
            needed_topics.append(correct_topcis)
        mock__get_needed_topics.side_effect = needed_topics

        expected = generator._get_computing_resource(data_setting)
        correct = json_resolver.read_json(os.path.join(self.test_data_dir, 'computing_resource.json'))
        self.assertEqual(expected, correct)

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

        expect = generator._get_avaliable_ip_address()
        correct = ['ip:10.52.52.106', 'ip:10.52.52.107']
        self.assertEqual(expect, correct)

    @patch('api.emulation.utils.generator._get_avaliable_ip_address')
    @patch('api.emulation.utils.generator._get_computing_resource')
    def test__distribute_computing_resource(self, mock__get_computing_resource, mock__get_avaliable_ip_address):
        path = os.path.join(self.test_data_dir, 'computing_resource.json')
        mock__get_computing_resource.return_value = json_resolver.read_json(path)
        mock__get_avaliable_ip_address.return_value = ['ip:10.52.52.106', 'ip:10.52.52.107']

        path = os.path.join(self.test_data_dir, 'data_setting.json')
        data_setting = json_resolver.read_json(path)
        expected_emulation_data = generator._distribute_computing_resource(data_setting)

        path = os.path.join(self.test_data_dir, 'distributed_computing_resource.json')
        correct = json_resolver.read_json(path)
        self.assertEqual(expected_emulation_data, correct)

    @patch('api.emulation.utils.generator._get_avaliable_ip_address')
    @patch('api.emulation.utils.generator._get_computing_resource')
    def test__distribute_computing_resource_raise_error(self, mock__get_computing_resource, mock__get_avaliable_ip_address):
        path = os.path.join(self.test_data_dir, 'computing_resource.json')
        mock__get_computing_resource.return_value = json_resolver.read_json(path)
        mock__get_avaliable_ip_address.return_value = ['ip:10.52.52.106']

        self.assertRaises(generator.DevicesNotEnoughException, generator._distribute_computing_resource, data_setting={})

    @patch('api.emulation.utils.generator._distribute_computing_resource')
    def test_generate_emulation_data(self, mock__distribute_computing_resource):
        path = os.path.join(self.test_data_dir, 'distributed_computing_resource.json')
        distributed_computing_resource = json_resolver.read_json(path)
        mock__distribute_computing_resource.return_value = distributed_computing_resource

        expected_emulation_data = generator.generate_emulation_data(data_setting={}, emulation_time=10)
        
        path = os.path.join(self.test_data_dir, 'emulation_data.json')
        correct = json_resolver.read_json(path)
        self.assertEqual(expected_emulation_data, correct)


class GeneratorExceptionTest(unittest.TestCase):

    @patch('api.emulation.utils.generator._get_avaliable_ip_address')
    @patch('api.emulation.utils.generator._get_computing_resource')
    def test__distribute_computing_resource(self, mock__get_computing_resource, mock__get_avaliable_ip_address):
        mock__get_computing_resource.return_value = ['ip:10.52.52.106', 'ip:10.52.52.107']
        mock__get_avaliable_ip_address.return_value = ['ip:10.52.52.106']

        with self.assertRaises(generator.DevicesNotEnoughException) as context:
            generator._distribute_computing_resource({})

        self.assertTrue("The number of devices aren't enough to do emulation. " \
                         "Which must be >= 2" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
