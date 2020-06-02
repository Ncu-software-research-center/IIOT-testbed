import unittest
from unittest.mock import patch

from api.emulation import EmulationStatus
from api.emulation.emulation_handler import abort_handled


class MockRedis:
    def __init__(self, host, port, password, encoding, decode_responses):
        self.data = {}
    def get(self, name):
        return self.data.get(name, '')
    def hget(self, name, key):
        return self.data.get(name, '').get(key, '')
    def set(self, name, value):
        self.data[name] = value
    def hset(self, name, key, value):
        if name in self.data:
            self.data[name][key] = value
        else:
            self.data[name] = {}
            self.data[name][key] = value


class EmulationHandlerTest(unittest.TestCase):
    @patch('redis.StrictRedis')
    def test_abort_handled(self, mock_redis):
        mock_redis.side_effect = MockRedis

        @abort_handled
        def testing():
            return 'expected result'

        self.assertEqual(testing(), 'expected result')
