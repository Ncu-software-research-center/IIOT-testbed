'''
                      Vortex OpenSplice

This software and documentation are Copyright 2006 to TO_YEAR ADLINK
Technology Limited, its affiliated companies and licensors. All rights
reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from . import (DsalKey, DDS_ENTITY_DATA_READER, DDS_ENTITY_DATA_WRITER,
               DDS_ENTITY_TOPIC)


class QosDefaultValue():
    duration_min = 0
    duration_unlimit = 2147483647
    duration_max_block_time_ns = 100000000
    value = 0
    value_unlimit = -1
    destination_order_kind = 'by_reception_timestamp'
    durability_kind = 'volatile'
    history_kind = 'keep_last'
    history_depth = 1
    liveliness_kind = 'automatic'
    ownership_kind = 'shared'
    reliability_kind_topic = 'best_effort'
    reliability_kind_dw = 'reliable'
    reliability_kind_dr = 'best_effort'


class QosKey():
    user_data = 'user_data'
    topic_data = 'topic_data'
    group_data = 'group_data'
    entity_factory = 'entity_factory'
    transport_priority = 'transport_priority'
    lifespan = 'lifespan'
    durability = 'durability'
    deadline = 'deadline'
    latency_budget = 'latency_budget'
    ownership = 'ownership'
    ownership_strength = 'ownership_strength'
    liveliness = 'liveliness'
    reliability = 'reliability'
    destination_order = 'destination_order'
    history = 'history'
    resource_limits = 'resource_limits'
    durability_service = 'durability_service'
    presentation = 'presentation'
    writer_data_lifecycle = 'writer_data_lifecycle'
    time_based_filter = 'time_based_filter'
    reader_data_lifecycl = 'reader_data_lifecycle'
    _kind = 'kind'
    _duration = 'duration'
    _period = 'period'
    _lease_duration = 'lease_duration'
    _minimum_separation = 'minimum_separation'
    _max_block_time = 'max_block_time'
    _sec = 'sec'
    _nanosec = 'nanosec'
    _depth = 'depth'
    _max_samples = 'max_samples'
    _max_instances = 'max_instances'
    _max_samples_per_instance = 'max_samples_per_instance'


def set_default_deadline_qos(qos: dict):
    if QosKey.deadline not in qos:
        qos[QosKey.deadline] = {
            QosKey._period: {
                QosKey._sec: QosDefaultValue.duration_unlimit,
                QosKey._nanosec: QosDefaultValue.duration_unlimit
            }
        }


def set_default_destination_order_qos(qos: dict):
    if QosKey.destination_order not in qos:
        qos[QosKey.destination_order] = {
            QosKey._kind: QosDefaultValue.destination_order_kind
        }


def set_default_durability_qos(qos: dict):
    if QosKey.durability not in qos:
        qos[QosKey.durability] = {
            QosKey._kind: QosDefaultValue.durability_kind
        }


def set_default_history_qos(qos: dict):
    if QosKey.history not in qos:
        qos[QosKey.history] = {
            QosKey._kind: QosDefaultValue.history_kind,
            QosKey._depth: QosDefaultValue.history_depth
        }


def set_default_latency_budget_qos(qos: dict):
    if QosKey.latency_budget not in qos:
        qos[QosKey.latency_budget] = {
            QosKey._duration: {
                QosKey._sec: QosDefaultValue.duration_min,
                QosKey._nanosec: QosDefaultValue.duration_min
            }
        }


def set_default_liveliness_qos(qos: dict):
    if QosKey.liveliness not in qos:
        qos[QosKey.liveliness] = {
            QosKey._kind: QosDefaultValue.liveliness_kind,
            QosKey._lease_duration: {
                QosKey._sec: QosDefaultValue.duration_unlimit,
                QosKey._nanosec: QosDefaultValue.duration_unlimit
            }
        }


def set_default_ownership_qos(qos: dict):
    if QosKey.ownership not in qos:
        qos[QosKey.ownership] = {
            QosKey._kind: QosDefaultValue.ownership_kind
        }


def set_default_resource_limits_qos(qos: dict):
    if QosKey.resource_limits not in qos:
        qos[QosKey.resource_limits] = {
            QosKey._max_samples: QosDefaultValue.value_unlimit,
            QosKey._max_instances: QosDefaultValue.value_unlimit,
            QosKey._max_samples_per_instance: QosDefaultValue.value_unlimit
        }


def set_default_reliability_qos(qos: dict, entity: str):
    if QosKey.reliability not in qos:
        qos[QosKey.reliability] = {}
        if entity == DDS_ENTITY_DATA_WRITER:
            qos[QosKey.reliability][QosKey._kind] = QosDefaultValue.reliability_kind_dw
        else:
            qos[QosKey.reliability][QosKey._kind] = QosDefaultValue.reliability_kind_topic
        qos[QosKey.reliability][QosKey._max_block_time] = {}
        qos[QosKey.reliability][QosKey._max_block_time][QosKey._sec] = QosDefaultValue.duration_min
        qos[QosKey.reliability][QosKey._max_block_time][QosKey._nanosec] = QosDefaultValue.duration_max_block_time_ns


def set_default_qos(qos: dict):
    set_default_deadline_qos(qos[DsalKey.qos])
    set_default_destination_order_qos(qos[DsalKey.qos])
    set_default_durability_qos(qos[DsalKey.qos])
    set_default_history_qos(qos[DsalKey.qos])
    set_default_latency_budget_qos(qos[DsalKey.qos])
    set_default_liveliness_qos(qos[DsalKey.qos])
    set_default_ownership_qos(qos[DsalKey.qos])
    set_default_resource_limits_qos(qos[DsalKey.qos])


def fix_nanosec_unlimit_value(qos: dict):
    if isinstance(qos, dict):
        if qos.get(QosKey._nanosec, -2) == -1:
            qos[QosKey._nanosec] = QosDefaultValue.duration_unlimit
        else:
            for _, v in qos.items():
                fix_nanosec_unlimit_value(v)
    elif isinstance(qos, list):
        for q in qos:
            fix_nanosec_unlimit_value(q)
