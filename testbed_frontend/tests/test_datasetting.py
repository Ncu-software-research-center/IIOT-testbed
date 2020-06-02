"""
Test the data setting module in DSAL module - api/dsal/datasetting.py
"""
import os
import unittest

from api.dsal import convert_dsal_to_datasetting

CUR_PATH = os.path.dirname(os.path.abspath(__file__))


class DataSettingTestCase(unittest.TestCase):

    def test_convert_dsal_to_datasetting(self):
        test_data_path = os.path.join(CUR_PATH, 'test-data/datasetting')
        paths = [os.path.join(test_data_path, path) for path in os.listdir(test_data_path)]
        for path in paths:
            with open(path) as file:
                data = file.read()
            result = convert_dsal_to_datasetting(data)
