import unittest
from api.emulation.utils import transformer
from api.dsal.datasetting import convert_dsal_to_datasetting


class TransformerTest(unittest.TestCase):
    def test_transform_kind_qos(self):
        with open('tests/test-data/dsal/dsal.yaml') as inputfile:
            data = inputfile.read()
        data_setting = convert_dsal_to_datasetting(data)
        data_setting = transformer.transform_kind_qos(data_setting)

if __name__ == "__main__":
    unittest.main()
