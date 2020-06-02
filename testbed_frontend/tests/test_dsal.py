"""
Test the whole dsal module including core.py, qos.py and qos_validator.py
"""
import json
import os
import unittest

import yaml

from api.dsal import (DsalBaseNotFoundError, DsalQosCompatibilityError, DsalError,
                     DsalQosConsistencyError, DsalSchemaError, dsal)
from api.dsal.dsal.core import (_loads, resolve_define_data_reader,
                               resolve_define_data_writer, resolve_define_qos,
                               resolve_define_topic, resolve_devices)
from api.dsal.dsal.qos import fix_nanosec_unlimit_value
from api.dsal.dsal.qos_validator import (
    deadline_compatibility_validate, destination_order_compatibility_validate,
    durability_compatibility_validate, durability_service_consistency_validate,
    latency_budget_compatibility_validate, lifespan_consistency_validate,
    liveliness_compatibility_validate, ownership_compatibility_validate,
    presentation_compatibility_validate, reliability_compatibility_validate,
    resource_limits_history_consistency_validate, resource_limits_consistency_validate,
    time_based_filter_deadline_consistency_validate)

CUR_PATH = os.path.dirname(os.path.abspath(__file__))

class DsalTestCase(unittest.TestCase):

    def test_fix_nanosec_unlimit_value_one_layer(self):
        data = {"nanosec":-1}
        fix_nanosec_unlimit_value(data)
        self.assertEqual(2147483647, data['nanosec'])
    
    def test_fix_nanosec_unlimit_value_multiple_layer(self):
        data = {"k":{"k":{"k":{"k":{"k":{"nanosec":-1}}}}}}
        fix_nanosec_unlimit_value(data)
        self.assertEqual(2147483647, data['k']['k']['k']['k']['k']['nanosec'])
    
    def test_dsal_base_not_found(self):
        e = DsalBaseNotFoundError("base", "test")
        self.assertEqual('DsalBaseNotFoundError: base="base" not found, at: dsal -> test',e.__str__())

    def test_resolve_define_qos_zero_layer(self):
        data = [{'name':'1','base':'default','qos':{}}]
        resolved = resolve_define_qos(data)
        result = {'1': {'deadline': {'period': {'sec': 2147483647, 'nanosec': 2147483647}}, 'destination_order': {'kind': 'by_reception_timestamp'}, 'durability': {'kind': 'volatile'}, 'history': {'kind': 'keep_last', 'depth': 1}, 'latency_budget': {'duration': {'sec': 0, 'nanosec': 0}}, 'liveliness': {'kind': 'automatic', 'lease_duration': {'sec': 2147483647, 'nanosec': 2147483647}}, 'ownership': {'kind': 'shared'}, 'resource_limits': {'max_samples': -1, 'max_instances': -1, 'max_samples_per_instance': -1}}}
        self.assertEqual(result, resolved)

    def test_resolve_define_qos_multiple_layer(self):
        data = [{'name':'1','base':'default','qos':{}}, {'name':'2','base':'1','qos':{'deadline':{'period':{'sec':0, 'nanosec':0}}, 'user_data':{'value':"123"}}}, {'name':'3','base':'2','qos':{'deadline':{'period':{'sec':1, 'nanosec':1}}, 'topic_data':{'value':"123"}}}]
        resolved = resolve_define_qos(data)
        result = {'1': {'deadline': {'period': {'sec': 2147483647, 'nanosec': 2147483647}}, 'destination_order': {'kind': 'by_reception_timestamp'}, 'durability': {'kind': 'volatile'}, 'history': {'kind': 'keep_last', 'depth': 1}, 'latency_budget': {'duration': {'sec': 0, 'nanosec': 0}}, 'liveliness': {'kind': 'automatic', 'lease_duration': {'sec': 2147483647, 'nanosec': 2147483647}}, 'ownership': {'kind': 'shared'}, 'resource_limits': {'max_samples': -1, 'max_instances': -1, 'max_samples_per_instance': -1}}, '2': {'deadline': {'period': {'sec': 0, 'nanosec': 0}}, 'user_data': {'value': '123'}, 'destination_order': {'kind': 'by_reception_timestamp'}, 'durability': {'kind': 'volatile'}, 'history': {'kind': 'keep_last', 'depth': 1}, 'latency_budget': {'duration': {'sec': 0, 'nanosec': 0}}, 'liveliness': {'kind': 'automatic', 'lease_duration': {'sec': 2147483647, 'nanosec': 2147483647}}, 'ownership': {'kind': 'shared'}, 'resource_limits': {'max_samples': -1, 'max_instances': -1, 'max_samples_per_instance': -1}}, '3': {'deadline': {'period': {'sec': 1, 'nanosec': 1}}, 'topic_data': {'value': '123'}, 'user_data': {'value': '123'}, 'destination_order': {'kind': 'by_reception_timestamp'}, 'durability': {'kind': 'volatile'}, 'history': {'kind': 'keep_last', 'depth': 1}, 'latency_budget': {'duration': {'sec': 0, 'nanosec': 0}}, 'liveliness': {'kind': 'automatic', 'lease_duration': {'sec': 2147483647, 'nanosec': 2147483647}}, 'ownership': {'kind': 'shared'}, 'resource_limits': {'max_samples': -1, 'max_instances': -1, 'max_samples_per_instance': -1}}}
        self.assertEqual(result, resolved)
    
    def test_resolve_define_topic(self):
        qos = {'1':{'user_data':'123'}, '2':{'user_data':{'value':'456'}}}
        topic = [{'name':'1','qos':'1'}]
        resolved = resolve_define_topic(topic, qos)
        result = {'1': {'name': '1', 'qos': {'user_data': '123'}}}
        self.assertEqual(result, resolved)
    
    def test_resolve_define_data_writer_zero_layer(self):
        qos = {'1':{'user_data':'123'}, '2':{'user_data':{'value':'456'}}}
        topic = {'1':{'name': '1', 'qos': {'user_data': '123'}}, '2':{'name': '2', 'qos': {'user_data': {'value': '456'}}}}
        data = [{'name':'1','qos':'1','dst_topic':'1','msg_size':12,'msg_cycletime':1}]
        resolved = resolve_define_data_writer(data, topic, qos)
        result = {'1': {'name': '1', 'qos': {'user_data': '123'}, 'dst_topic': '1', 'msg_size': 12, 'msg_cycletime': 1}} 
        self.assertEqual(result, resolved)

    def test_resolve_define_data_writer_multiple_layer(self):
        qos = {'1':{'user_data':'123'}, '2':{'user_data':{'value':'456'}}}
        topic = {'1':{'name': '1', 'qos': {'user_data': '123'}}, '2':{'name': '2', 'qos': {'user_data': {'value': '456'}}}}
        data = [{'name':'1','qos':'1','dst_topic':'1','msg_size':12,'msg_cycletime':1},{'name':'2','base':'1','msg_size':13},{'name':'3','base':'2','qos':'2','msg_cycletime':2}]
        resolved = resolve_define_data_writer(data, topic, qos)
        result = {'1': {'name': '1', 'qos': {'user_data': '123'}, 'dst_topic': '1', 'msg_size': 12, 'msg_cycletime': 1}, '2': {'name': '2', 'base': '1', 'msg_size': 13, 'qos': {'user_data': '123'}, 'dst_topic': '1', 'msg_cycletime': 1}, '3': {'name': '3', 'base': '2', 'qos': {'user_data': {'value': '456'}}, 'msg_cycletime': 2, 'msg_size': 13, 'dst_topic': '1'}}
        self.assertEqual(result, resolved)

    def test_resolve_define_data_reader_zero_layer(self):
        qos = {'1':{'user_data':'123'}, '2':{'user_data':{'value':'456'}}}
        topic = {'1':{'name': '1', 'qos': {'user_data': '123'}}, '2':{'name': '2', 'qos': {'user_data': {'value': '456'}}}}
        data = [{'name':'1','qos':'1','src_topic':'1'}]
        resolved = resolve_define_data_reader(data, topic, qos)
        result = {'1': {'name': '1', 'qos': {'user_data': '123'}, 'src_topic': '1'}}
        self.assertEqual(result, resolved)
   
    def test_resolve_define_data_reader_multiple_layer(self):
        qos = {'1':{'user_data':'123'}, '2':{'user_data':{'value':'456'}}}
        topic = {'1':{'name': '1', 'qos': {'user_data': '123'}}, '2':{'name': '2', 'qos': {'user_data': {'value': '456'}}}}
        data = [{'name':'1','qos':'1','src_topic':'1'},{'name':'2','base':'1', 'src_topic':'2'},{'name':'3','base':'2','qos':'2'}]
        resolved = resolve_define_data_reader(data, topic, qos)
        result = {'1': {'name': '1', 'qos': {'user_data': '123'}, 'src_topic': '1'}, '2': {'name': '2', 'base': '1', 'qos': {'user_data': '123'}, 'src_topic': '2'}, '3': {'name': '3', 'base': '2', 'qos': {'user_data': {'value': '456'}}, 'src_topic': '2'}}
        self.assertEqual(result, resolved)
    
    def test_resolve_devices(self):
        qos = {'1':{'user_data':'123'}, '2':{'user_data':{'value':'456'}}}
        topic = {'1':{'name': '1', 'qos': {'user_data': '123'}}, '2':{'name': '2', 'qos': {'user_data': {'value': '456'}}}}
        dw = {'1': {'name': '1', 'qos': {'user_data': '123'}, 'dst_topic': '1', 'msg_size': 12, 'msg_cycletime': 1}, '2': {'name': '2', 'base': '1', 'msg_size': 13, 'qos': {'user_data': '123'}, 'dst_topic': '1', 'msg_cycletime': 1}, '3': {'name': '3', 'base': '2', 'qos': {'user_data': {'value': '456'}}, 'msg_cycletime': 2, 'msg_size': 13, 'dst_topic': '1'}}
        dr = {'1': {'name': '1', 'qos': {'user_data': '123'}, 'src_topic': '1'}, '2': {'name': '2', 'base': '1', 'qos': {'user_data': '123'}, 'src_topic': '2'}, '3': {'name': '3', 'base': '2', 'qos': {'user_data': {'value': '456'}}, 'src_topic': '2'}}
        data = [{'name':'1','number':1,'domains':[{'qos':'1','partitions':[{'name':'part1','publishers':[{'qos':'1','data_writers':[{'name':'1'},{'name':'1', 'qos':'1'},{'name':'1','msg_cycletime':3}]}],'subscribers':[{'qos':'1', 'data_readers':[{'name':'1'}, {'name':'1','qos':'2'}, {'name':'1','src_topic':'2'}]}]}]}]}]
        resolved = resolve_devices(data, dw, dr, topic, qos)
        result =  [{'name': '1', 'number': 1, 'domains': [{'qos': {'user_data': '123', 'reliability': {'kind': 'best_effort', 'max_block_time': {'sec': 0, 'nanosec': 100000000}}}, 'partitions': [{'name': 'part1', 'publishers': [{'qos': {'user_data': '123', 'reliability': {'kind': 'best_effort', 'max_block_time': {'sec': 0, 'nanosec': 100000000}}}, 'data_writers': [{'name': '1', 'qos': {'user_data': '123', 'reliability': {'kind': 'reliable', 'max_block_time': {'sec': 0, 'nanosec': 100000000}}}, 'dst_topic': '1', 'msg_size': 12, 'msg_cycletime': 1}, {'name': '1', 'qos': {'user_data': '123', 'reliability': {'kind': 'reliable', 'max_block_time': {'sec': 0, 'nanosec': 100000000}}}, 'dst_topic': '1', 'msg_size': 12, 'msg_cycletime': 1}, {'name': '1', 'msg_cycletime': 3, 'qos': {'user_data': '123', 'reliability': {'kind': 'reliable', 'max_block_time': {'sec': 0, 'nanosec': 100000000}}}, 'dst_topic': '1', 'msg_size': 12}]}], 'subscribers': [{'qos': {'user_data': '123', 'reliability': {'kind': 'best_effort', 'max_block_time': {'sec': 0, 'nanosec': 100000000}}}, 'data_readers': [{'name': '1', 'qos': {'user_data': '123', 'reliability': {'kind': 'best_effort', 'max_block_time': {'sec': 0, 'nanosec': 100000000}}}, 'src_topic': '1'}, {'name': '1', 'qos': {'user_data': {'value': '456'}, 'reliability': {'kind': 'best_effort', 'max_block_time': {'sec': 0, 'nanosec': 100000000}}}, 'src_topic': '1'}, {'name': '1', 'src_topic': '2', 'qos': {'user_data': '123', 'reliability': {'kind': 'best_effort', 'max_block_time': {'sec': 0, 'nanosec': 100000000}}}}]}]}]}]}]
        self.assertEqual(result, resolved)
    
    def test_durability_service_consistency_validate_valid(self):
        data = {'kind':'keep_last', 'depth':1, 'max_samples_per_instance':-1}
        durability_service_consistency_validate(data, 'test')

    def test_durability_service_consistency_validate_invalid(self):
        data = {'kind':'keep_last', 'depth':1, 'max_samples_per_instance':0}
        self.assertRaises(DsalQosConsistencyError, durability_service_consistency_validate, data, 'test')
    
    def test_lifespan_consistency_validate_valid(self):
        data = {'duration':{'sec':1,'nanosec':1}}
        lifespan_consistency_validate(data, 'test')

    def test_lifespan_consistency_validate_invalid(self):
        data = {'duration':{'sec':0,'nanosec':0}}
        self.assertRaises(DsalQosConsistencyError, lifespan_consistency_validate, data, 'test')
    
    def test_resource_limits_consistency_validate_valid(self):
        data = {'max_samples':-1, 'max_samples_per_instance':1}
        resource_limits_consistency_validate(data, 'test')

    def test_resource_limits_consistency_validate_invalid(self):
        data = {'max_samples':0, 'max_samples_per_instance':1}
        self.assertRaises(DsalQosConsistencyError, resource_limits_consistency_validate, data, 'test')

    def test_resource_limits_history_consistency_validate_valid(self):
        data1 = {'max_samples':-1, 'max_samples_per_instance':-1}
        data2 = {'kind':'keep_last','depth':1}
        resource_limits_history_consistency_validate(data1, data2, 'test')

    def test_resource_limits_history_consistency_validate_invalid(self):
        data1 = {'max_samples':-1, 'max_samples_per_instance':0}
        data2 = {'kind':'keep_last','depth':1}
        self.assertRaises(DsalQosConsistencyError, resource_limits_history_consistency_validate, data1, data2, 'test')

    def test_time_based_filter_deadline_consistency_validate_valid(self):
        data1 = {'minimum_separation':{'sec':1,'nanosec':100000}}
        data2 = {'period':{'sec':10, 'nanosec':10}}
        time_based_filter_deadline_consistency_validate(data1, data2, 'test')

    def test_time_based_filter_deadline_consistency_validate_invalid(self):
        data1 = {'minimum_separation':{'sec':10,'nanosec':10}}
        data2 = {'period':{'sec':1, 'nanosec':1000000}}
        self.assertRaises(DsalQosConsistencyError, time_based_filter_deadline_consistency_validate, data1, data2, 'test')

    def test_deadline_compatibility_validate_valid(self):
        r = {'period':{'sec':1, 'nanosec':0}}
        o = {'period':{'sec':0, 'nanosec':0}}
        deadline_compatibility_validate(r, o, 'dw', 'dr')

    def test_deadline_compatibility_validate_invalid(self):
        r = {'period':{'sec':0, 'nanosec':0}}
        o = {'period':{'sec':1, 'nanosec':0}}
        self.assertRaises(DsalQosCompatibilityError, deadline_compatibility_validate, r, o, 'dw', 'dr')
    
    def test_destination_order_compatibility_validate_valid(self):
        r = {'kind':'by_reception_timestamp'}
        o = {'kind':'by_reception_timestamp'}
        destination_order_compatibility_validate(r, o, 'dw', 'dr')

    def test_destination_order_compatibility_validate_invalid(self):
        r = {'kind':'by_source_time_stamp'}
        o = {'kind':'by_reception_timestamp'}
        self.assertRaises(DsalQosCompatibilityError, destination_order_compatibility_validate, r, o, 'dw', 'dr')
    
    def test_durability_compatibility_validate_valid(self):
        r = {'kind':'volatile'}
        o = {'kind':'volatile'}
        durability_compatibility_validate(r, o, 'dw', 'dr')

    def test_durability_compatibility_validate_invalid(self):
        r = {'kind':'transient_local'}
        o = {'kind':'volatile'}
        self.assertRaises(DsalQosCompatibilityError, durability_compatibility_validate, r, o, 'dw', 'dr')
    
    def test_latency_budget_compatibility_validate_valid(self):
        r = {'duration':{'sec':1, 'nanosec':0}}
        o = {'duration':{'sec':0, 'nanosec':0}}
        latency_budget_compatibility_validate(r, o, 'dw', 'dr')

    def test_latency_budget_compatibility_validate_invalid(self):
        r = {'duration':{'sec':0, 'nanosec':0}}
        o = {'duration':{'sec':1, 'nanosec':0}}
        self.assertRaises(DsalQosCompatibilityError, latency_budget_compatibility_validate, r, o, 'dw', 'dr')

    def test_liveliness_compatibility_validate_valid(self):
        r = {'kind':'automatic'}
        o = {'kind':'automatic'}
        liveliness_compatibility_validate(r, o, 'dw', 'dr')

    def test_liveliness_compatibility_validate_invalid(self):
        r = {'kind':'manual_by_participant'}
        o = {'kind':'automatic'}
        self.assertRaises(DsalQosCompatibilityError, liveliness_compatibility_validate, r, o, 'dw', 'dr')
    
    def test_ownership_compatibility_validate_valid(self):
        r = {'kind':'shared'}
        o = {'kind':'shared'}
        ownership_compatibility_validate(r, o, 'dw', 'dr')

    def test_ownership_compatibility_validate_invalid(self):
        r = {'kind':'shared'}
        o = {'kind':'exclusive'}
        self.assertRaises(DsalQosCompatibilityError, ownership_compatibility_validate, r, o, 'dw', 'dr')

    def test_presentation_compatibility_validate_valid(self):
        r = {'kind':'instance'}
        o = {'kind':'instance'}
        ownership_compatibility_validate(r, o, 'dw', 'dr')

    def test_presentation_compatibility_validate_invalid(self):
        r = {'kind':'topic'}
        o = {'kind':'instance'}
        self.assertRaises(DsalQosCompatibilityError, ownership_compatibility_validate, r, o, 'dw', 'dr')

    def test_reliability_compatibility_validate_valid(self):
        r = {'kind':'best_effort'}
        o = {'kind':'best_effort'}
        reliability_compatibility_validate(r, o, 'dw', 'dr')

    def test_reliability_compatibility_validate_invalid(self):
        r = {'kind':'reliabile'}
        o = {'kind':'best_effort'}
        self.assertRaises(DsalQosCompatibilityError, reliability_compatibility_validate, r, o, 'dw', 'dr')

    def test_loads_exception(self):
        self.assertRaises(DsalSchemaError, dsal.loads, src="{}")
    
    def test_loads(self):
        test_data_path = os.path.join(CUR_PATH, 'test-data/dsal/dsal.yaml')
        test_resolved_path = os.path.join(CUR_PATH, 'test-data/dsal/dsal.json')
        with open(test_data_path) as file:
            data = file.read()
        with open(test_resolved_path) as file:
            resolved = json.load(file)

        result = dsal.loads(data)
        self.assertEqual(result, resolved)
    
    def test_loads_fail(self):
        test_validate_value_path = os.path.join(CUR_PATH, 'test-data/dsal/validate/consistency')
        test_validate_consistency_path = os.path.join(CUR_PATH, 'test-data/dsal/validate/compatibility')
        paths = [os.path.join(test_validate_value_path, path) for path in os.listdir(test_validate_value_path)]
        paths.extend([os.path.join(test_validate_consistency_path, path) for path in os.listdir(test_validate_consistency_path)])
        for path in paths:
            with open(path) as file:
                data = file.read()
            self.assertRaises(DsalError, dsal.loads, data)
    
    def test_loads_success(self):
        data = ""
        test_correct_path = os.path.join(CUR_PATH, 'test-data/dsal/correct')
        paths = [os.path.join(test_correct_path, path) for path in os.listdir(test_correct_path)]
        for path in paths:
            with open(path) as file:
                data = file.read()

    def test_load_default_qos(self):
        test_data_path = os.path.join(CUR_PATH, 'test-data/dsal/dsal_default.yaml')
        with open(test_data_path) as file:
            data = file.read()
        d = _loads(data)
        self.assertEqual(d["dsal"]["version"], "1.0.0")
        self.assertTrue("base" in d["dsal"]["define_qos"][0])
        self.assertTrue("qos" in d["dsal"]["define_qos"][0])
        self.assertTrue("user_data" in d["dsal"]["define_qos"][0]["qos"])
        self.assertEqual("", d["dsal"]["define_qos"][0]
                         ["qos"]["user_data"]["value"])
        self.assertTrue("topic_data" in d["dsal"]["define_qos"][0]["qos"])
        self.assertEqual("", d["dsal"]["define_qos"][0]
                         ["qos"]["topic_data"]["value"])
        self.assertTrue("group_data" in d["dsal"]["define_qos"][0]["qos"])
        self.assertEqual("", d["dsal"]["define_qos"][0]
                         ["qos"]["group_data"]["value"])
        self.assertTrue(
            "transport_priority" in d["dsal"]["define_qos"][0]["qos"])
        self.assertEqual(0, d["dsal"]["define_qos"][0]
                         ["qos"]["transport_priority"]["value"])
        self.assertTrue("lifespan" in d["dsal"]["define_qos"][0]["qos"])
        self.assertEqual(
            2147483647, d["dsal"]["define_qos"][0]["qos"]["lifespan"]["duration"]["sec"])
        self.assertEqual(-1, d["dsal"]["define_qos"][0]
                         ["qos"]["lifespan"]["duration"]["nanosec"])
        self.assertTrue("presentation" in d["dsal"]["define_qos"][0]["qos"])
        self.assertEqual("instance", d["dsal"]["define_qos"][0]
                         ["qos"]["presentation"]["kind"])
        self.assertFalse(d["dsal"]["define_qos"][0]["qos"]
                         ["presentation"]["coherent_access"])
        self.assertFalse(d["dsal"]["define_qos"][0]["qos"]
                         ["presentation"]["ordered_access"])
        self.assertTrue(
            "ownership_strength" in d["dsal"]["define_qos"][0]["qos"])
        self.assertEqual(0, d["dsal"]["define_qos"][0]
                         ["qos"]["ownership_strength"]["value"])
        self.assertTrue(
            "time_based_filter" in d["dsal"]["define_qos"][0]["qos"])
        self.assertEqual(0, d["dsal"]["define_qos"][0]
                         ["qos"]["time_based_filter"]["minimum_separation"]["sec"])
        self.assertEqual(0, d["dsal"]["define_qos"][0]["qos"]
                         ["time_based_filter"]["minimum_separation"]["nanosec"])
        self.assertTrue("entity_factory" in d["dsal"]["define_qos"][0]["qos"])
        self.assertTrue(d["dsal"]["define_qos"][0]["qos"]
                        ["entity_factory"]["autoenable_created_entities"])
        self.assertTrue(
            "writer_data_lifecycle" in d["dsal"]["define_qos"][0]["qos"])
        self.assertTrue(d["dsal"]["define_qos"][0]["qos"]
                        ["writer_data_lifecycle"]["autodispose_unregistered_instances"])
        self.assertEqual(2147483647, d["dsal"]["define_qos"][0]["qos"]
                         ["writer_data_lifecycle"]["autopurge_suspended_samples_delay"]["sec"])
        self.assertEqual(-1, d["dsal"]["define_qos"][0]["qos"]
                         ["writer_data_lifecycle"]["autopurge_suspended_samples_delay"]["nanosec"])
        self.assertEqual(2147483647, d["dsal"]["define_qos"][0]["qos"]
                         ["writer_data_lifecycle"]["autounregister_instance_delay"]["sec"])
        self.assertEqual(-1, d["dsal"]["define_qos"][0]["qos"]
                         ["writer_data_lifecycle"]["autounregister_instance_delay"]["nanosec"])
        self.assertTrue(
            "reader_data_lifecycle" in d["dsal"]["define_qos"][0]["qos"])
        self.assertEqual("minimum_invalid_samples", d["dsal"]["define_qos"][0]
                         ["qos"]["reader_data_lifecycle"]["kind"])
        self.assertEqual(2147483647, d["dsal"]["define_qos"][0]["qos"]
                         ["reader_data_lifecycle"]["autopurge_nowriter_samples_delay"]["sec"])
        self.assertEqual(-1, d["dsal"]["define_qos"][0]["qos"]
                         ["reader_data_lifecycle"]["autopurge_nowriter_samples_delay"]["nanosec"])
        self.assertEqual(2147483647, d["dsal"]["define_qos"][0]["qos"]
                         ["reader_data_lifecycle"]["autopurge_disposed_samples_delay"]["sec"])
        self.assertEqual(-1, d["dsal"]["define_qos"][0]["qos"]
                         ["reader_data_lifecycle"]["autopurge_disposed_samples_delay"]["nanosec"])
        self.assertTrue(
            "durability_service" in d["dsal"]["define_qos"][0]["qos"])
        self.assertEqual(
            "keep_last", d["dsal"]["define_qos"][0]["qos"]["durability_service"]["kind"])
        self.assertEqual(1, d["dsal"]["define_qos"][0]["qos"]
                         ["durability_service"]["depth"])
        self.assertEqual(-1, d["dsal"]["define_qos"][0]["qos"]
                         ["durability_service"]["max_samples"])
        self.assertEqual(-1, d["dsal"]["define_qos"][0]["qos"]
                         ["durability_service"]["max_instances"])
        self.assertEqual(-1, d["dsal"]["define_qos"][0]["qos"]
                         ["durability_service"]["max_samples_per_instance"])


if __name__ == '__main__':
    unittest.main()
