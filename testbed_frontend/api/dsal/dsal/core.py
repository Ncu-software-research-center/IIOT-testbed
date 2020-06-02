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
import types
from copy import deepcopy

import yaml

from . import (DDS_ENTITY_DATA_READER, DDS_ENTITY_DATA_WRITER,
               DDS_ENTITY_TOPIC, DDS_QOS, DsalKey)
from .exceptions import (DsalBaseNotFoundError, DsalDataReaderNotFoundError,
                         DsalDataWriterNotFoundError,
                         DsalDstTopicNotFoundError, DsalDuplicatedNameError,
                         DsalNameEqualsBaseError, DsalQosNotFoundError,
                         DsalSchemaError, DsalSrcTopicNotFoundError)
from .qos import (QosKey, fix_nanosec_unlimit_value, set_default_qos,
                  set_default_reliability_qos)
from .qos_validator import (deadline_compatibility_validate,
                            destination_order_compatibility_validate,
                            durability_compatibility_validate,
                            durability_service_consistency_validate,
                            latency_budget_compatibility_validate,
                            lifespan_consistency_validate,
                            liveliness_compatibility_validate,
                            ownership_compatibility_validate,
                            presentation_compatibility_validate,
                            reliability_compatibility_validate,
                            resource_limits_history_consistency_validate,
                            resource_limits_consistency_validate,
                            time_based_filter_deadline_consistency_validate)
from .validator import check_schema


def _get_device_path(device):
    return 'devices={}'


def _get_dw_path(device, domain, partition, pub, dw):
    return 'devices={} -> domains[{}] -> partitions={} -> publishers[{}] -> data_writers[{}]'.format(device, domain, partition, pub, dw)


def _get_dr_path(device, domain, partition, sub, dr):
    return 'devices={} -> domains[{}] -> partitions={} -> subscribers[{}] -> data_readers[{}]'.format(device, domain, partition, sub, dr)


def _get_define_qos_path(qos):
    return 'define_qos="{}"'.format(qos)


def _get_define_topic_path(topic):
    return 'define_topic="{}"'.format(topic)


def _get_define_dw_path(dw):
    return 'define_data_writer="{}"'.format(dw)


def _get_define_dr_path(dr):
    return 'define_data_reader="{}"'.format(dr)


def _find_base(base: str, define: list, path: str) -> dict:
    for it in define:
        if it[DsalKey.base] == base:
            return it
    raise DsalBaseNotFoundError(base, path)


def _find_dw(devices: dict) -> list:
    data_writers = []
    for device in devices:
        domains = device[DsalKey.domains]
        for domain_index in range(len(domains)):
            for partition in domains[domain_index][DsalKey.partitions]:
                if DsalKey.publishers in partition:
                    publishers = partition[DsalKey.publishers]
                    for pub_index in range(len(publishers)):
                        dws = publishers[pub_index][DsalKey.data_writers]
                        for dw_index in range(len(dws)):
                            dw = deepcopy(dws[dw_index])
                            dw['key'] = '.'.join(
                                [str(domain_index), partition[DsalKey.name], dws[dw_index][DsalKey.dst_topic]])
                            dw['id'] = _get_dw_path(
                                device[DsalKey.name], domain_index, partition[DsalKey.name], pub_index, dw_index)
                            data_writers.append(dw)
    return data_writers


def _find_dr(devices: dict) -> list:
    data_readers = []
    for device in devices:
        domains = device[DsalKey.domains]
        for domain_index in range(len(domains)):
            for partition in domains[domain_index][DsalKey.partitions]:
                if DsalKey.subscribers in partition:
                    subscribers = partition[DsalKey.subscribers]
                    for sub_index in range(len(subscribers)):
                        drs = subscribers[sub_index][DsalKey.data_readers]
                        for dr_index in range(len(drs)):
                            dr = deepcopy(drs[dr_index])
                            dr['key'] = '.'.join(
                                [str(domain_index), partition[DsalKey.name], drs[dr_index][DsalKey.src_topic]])
                            dr['id'] = _get_dr_path(
                                device[DsalKey.name], domain_index, partition[DsalKey.name], sub_index, dr_index)
                            data_readers.append(dr)
    return data_readers


def _set_by_base(src: dict, base: dict):
    for k, v in base.items():
        if k not in src:
            src[k] = deepcopy(v)


def _check_name_duplicated(item: dict, base: dict, path: str):
    name = item[DsalKey.name]
    if name in base:
        raise DsalDuplicatedNameError(name, path, item, base[name])
    base[name] = item


def _check_name_equal_base(item: dict, path: str):
    if DsalKey.base in item:
        name = item[DsalKey.name]
        base = item[DsalKey.base]
        if name == base:
            raise DsalNameEqualsBaseError(name, path)


def _check_dst_topic(src, topics, path):
    if DsalKey.dst_topic in src:
        if src[DsalKey.dst_topic] not in topics:
            raise DsalDstTopicNotFoundError(src[DsalKey.dst_topic], path)


def _check_src_topic(src, topics, path):
    if DsalKey.src_topic in src:
        if src[DsalKey.src_topic] not in topics:
            raise DsalSrcTopicNotFoundError(src[DsalKey.src_topic], path)


def _resolve(src: dict, base_name: str, base: dict, define: list, set_by_default: types.FunctionType, get_path: types.FunctionType, key: str = None):
    path = get_path(src[DsalKey.name])
    if base_name == DsalKey.default:
        set_by_default(src)
    else:
        if base_name not in base:
            tmp = _find_base(base_name, define, path)
            _resolve(tmp, tmp.get(DsalKey.base, DsalKey.default),
                     base, define, get_path, set_by_default, key=key)
        _set_by_base(src.get(key, src), base[base_name])
    base[src[DsalKey.name]] = deepcopy(src.get(key, src))
    return {src[DsalKey.name]: deepcopy(src.get(key, src))}


def _resolve_qos(item: dict, resolved_qos: dict, path: str):
    qos = item[DsalKey.qos]
    if isinstance(qos, str):
        if qos in resolved_qos:
            item[DsalKey.qos] = deepcopy(resolved_qos[qos])
        else:
            raise DsalQosNotFoundError(qos, path)


def _resolve_define_entity(define_entity: list, resolved_topic: dict, resolved_qos: dict, get_path: types.FunctionType, key: str):
    resolved = {}
    base = {}
    for entity in define_entity:
        name = entity[DsalKey.name]
        tmp = _resolve(entity, entity.get(DsalKey.base, DsalKey.default),
                       base, define_entity, lambda x: x, get_path)
        _resolve_qos(tmp[name], resolved_qos,
                     get_path(tmp[name].get(key, key)))
        resolved.update(tmp)
    return resolved


def _resolve_device_qos(item, resolved_qos: dict, path: str, at: str):
    path = ' -> '.join([path, at])
    if isinstance(item, dict):
        for k, v in item.items():
            _resolve_device_qos(v, resolved_qos, path, k)
        if DsalKey.qos in item:
            _resolve_qos(item, resolved_qos, path)
            if DsalKey.dst_topic in item:
                set_default_reliability_qos(
                    item[DsalKey.qos], DDS_ENTITY_DATA_WRITER)
            elif DsalKey.src_topic in item:
                set_default_reliability_qos(
                    item[DsalKey.qos], DDS_ENTITY_DATA_READER)
            else:
                set_default_reliability_qos(
                    item[DsalKey.qos], DDS_ENTITY_TOPIC)
    elif isinstance(item, list):
        for x in item:
            _resolve_device_qos(x, resolved_qos, path, at)


def _resolve_device(src: dict, resolved: dict, resolved_topic: dict, path):
    name = src[DsalKey.name]
    if name in resolved:
        _set_by_base(src, resolved[name])
        _check_dst_topic(src, resolved_topic, path)
        _check_src_topic(src, resolved_topic, path)
    else:
        if DsalKey.dst_topic in src:
            raise DsalDataWriterNotFoundError(name, path)
        else:
            raise DsalDataReaderNotFoundError(name, path)


def resolve_define_qos(define_qos: list) -> dict:
    resolved = {}
    base = {}
    name_base = {}
    for qos in define_qos:
        _check_name_duplicated(
            qos, name_base, _get_define_qos_path(qos[DsalKey.name]))
        _check_name_equal_base(qos, _get_define_qos_path(qos[DsalKey.name]))
    for qos in define_qos:
        resolved.update(_resolve(qos, qos[DsalKey.base], base, define_qos,
                                 set_default_qos, _get_define_qos_path, key=DsalKey.qos))
    return resolved


def resolve_define_topic(define_topic: list, resolved_qos: dict) -> dict:
    resolved = {}
    name_base = {}
    for topic in define_topic:
        _check_name_duplicated(
            topic, name_base, _get_define_topic_path(topic[DsalKey.name]))
    for topic in define_topic:
        _resolve_qos(topic, resolved_qos,
                     _get_define_topic_path(topic[DsalKey.name]))
        resolved.update({topic[DsalKey.name]: topic})
    return resolved


def resolve_define_data_writer(define_dw: list, resolved_topic: dict, resolved_qos: dict):
    name_base = {}
    for dw in define_dw:
        _check_name_duplicated(
            dw, name_base, _get_define_dw_path(dw[DsalKey.name]))
        _check_name_equal_base(dw, _get_define_dw_path(dw[DsalKey.name]))
    for dw in define_dw:
        _check_dst_topic(dw, resolved_topic,
                         _get_define_dw_path(dw[DsalKey.name]))
    return _resolve_define_entity(define_dw, resolved_topic, resolved_qos, _get_define_dw_path, key=DsalKey.name)


def resolve_define_data_reader(define_dr: list, resolved_topic: dict, resolved_qos: dict):
    name_base = {}
    for dr in define_dr:
        _check_name_duplicated(
            dr, name_base, _get_define_dr_path(dr[DsalKey.name]))
        _check_name_equal_base(dr, _get_define_dr_path(dr[DsalKey.name]))
    for dr in define_dr:
        _check_src_topic(dr, resolved_topic,
                         _get_define_dr_path(dr[DsalKey.name]))
    return _resolve_define_entity(define_dr, resolved_topic, resolved_qos, _get_define_dw_path, key=DsalKey.name)


def resolve_devices(devices: list, resolved_dw: dict, resolved_dr: dict, resolved_topic: dict, resolved_qos):
    name_base = {}
    for device in devices:
        _check_name_duplicated(
            device, name_base, _get_device_path(device[DsalKey.name]))
    for device in devices:
        domains = device[DsalKey.domains]
        for domain_index in range(len(domains)):
            partitions = domains[domain_index][DsalKey.partitions]
            for partition in partitions:
                publishers = partition.get(DsalKey.publishers, list())
                subscribers = partition.get(DsalKey.subscribers, list())
                for pub_index in range(len(publishers)):
                    dws = publishers[pub_index][DsalKey.data_writers]
                    for dw_index in range(len(dws)):
                        _resolve_device(dws[dw_index], resolved_dw, resolved_topic, _get_dw_path(
                            device[DsalKey.name], domain_index, partition[DsalKey.name], pub_index, dw_index))
                for sub_index in range(len(subscribers)):
                    drs = subscribers[sub_index][DsalKey.data_readers]
                    for dr_index in range(len(drs)):
                        _resolve_device(drs[dr_index], resolved_dr, resolved_topic, _get_dr_path(
                            device[DsalKey.name], domain_index, partition[DsalKey.name], sub_index, dr_index))
    _resolve_device_qos(devices, resolved_qos, DsalKey.devices, '')
    return devices


def resolve_dsal(name: str, version: str, qos: dict, topic: dict, dw: dict, dr: dict, devices: dict):
    resolved = {
        'profile_name': name,
        'version': version,
        'define_qos': qos,
        'define_topic': list(topic.values()),
        'define_data_writer': list(dw.values()),
        'define_data_reader': list(dr.values()),
        'devices': devices
    }
    return resolved


def check_qos_consistency(resolved_qos: dict):
    for k, v in resolved_qos.items():
        durability_service_consistency_validate(
            v[QosKey.durability_service], k)
        lifespan_consistency_validate(v[QosKey.lifespan], k)
        resource_limits_consistency_validate(v[QosKey.resource_limits], k)
        resource_limits_history_consistency_validate(
            v[QosKey.resource_limits], v[QosKey.history], k)
        time_based_filter_deadline_consistency_validate(
            v[QosKey.time_based_filter], v[QosKey.deadline], k)


def check_qos_compatibility(resolved_devices: dict):
    data_writers = _find_dw(resolved_devices)
    data_readers = _find_dr(resolved_devices)
    for dw in data_writers:
        for dr in data_readers:
            if dw['key'] == dr['key']:
                deadline_compatibility_validate(
                    dr[DsalKey.qos][QosKey.deadline], dw[DsalKey.qos][QosKey.deadline], dw['id'], dr['id'])
                destination_order_compatibility_validate(
                    dr[DsalKey.qos][QosKey.destination_order], dw[DsalKey.qos][QosKey.destination_order], dw['id'], dr['id'])
                durability_compatibility_validate(
                    dr[DsalKey.qos][QosKey.durability], dw[DsalKey.qos][QosKey.durability], dw['id'], dr['id'])
                latency_budget_compatibility_validate(
                    dr[DsalKey.qos][QosKey.latency_budget], dw[DsalKey.qos][QosKey.latency_budget], dw['id'], dr['id'])
                liveliness_compatibility_validate(
                    dr[DsalKey.qos][QosKey.liveliness], dw[DsalKey.qos][QosKey.liveliness], dw['id'], dr['id'])
                ownership_compatibility_validate(
                    dr[DsalKey.qos][QosKey.ownership], dw[DsalKey.qos][QosKey.ownership], dw['id'], dr['id'])
                presentation_compatibility_validate(
                    dr[DsalKey.qos][QosKey.presentation], dw[DsalKey.qos][QosKey.presentation], dw['id'], dr['id'])
                reliability_compatibility_validate(
                    dr[DsalKey.qos][QosKey.reliability], dw[DsalKey.qos][QosKey.reliability], dw['id'], dr['id'])


@check_schema
def _loads(src: str) -> dict:
    dsal = yaml.safe_load(src)
    return dsal


def loads(src: str) -> dict:
    src_dsal = _loads(src)
    fix_nanosec_unlimit_value(src_dsal)
    resolved_qos = resolve_define_qos(
        src_dsal[DsalKey.dsal][DsalKey.define_qos])
    resolved_topic = resolve_define_topic(
        src_dsal[DsalKey.dsal][DsalKey.define_topic], resolved_qos)
    resolved_dw = resolve_define_data_writer(
        src_dsal[DsalKey.dsal][DsalKey.define_data_writer], resolved_topic, resolved_qos)
    resolved_dr = resolve_define_data_reader(
        src_dsal[DsalKey.dsal][DsalKey.define_data_reader], resolved_topic, resolved_qos)
    resolved_devices = resolve_devices(
        src_dsal[DsalKey.dsal][DsalKey.devices], resolved_dw, resolved_dr, resolved_topic, resolved_qos)
    for topic in resolved_topic.values():
        set_default_reliability_qos(topic[DsalKey.qos], DDS_ENTITY_TOPIC)
    check_qos_consistency(resolved_qos)
    check_qos_compatibility(resolved_devices)
    return resolve_dsal(src_dsal[DsalKey.dsal][DsalKey.profile_name], src_dsal[DsalKey.dsal][DsalKey.version], resolved_qos, resolved_topic, resolved_dw, resolved_dr, resolved_devices)
