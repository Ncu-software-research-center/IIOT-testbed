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
from copy import deepcopy

from .dsal import DsalKey, loads


def dsal_modify_keys(dsal: dict) -> dict:
    cp = deepcopy(dsal)
    for topic in cp[DsalKey.define_topic]:
        topic['topic_qos'] = topic.pop(DsalKey.qos)
    for device in cp[DsalKey.devices]:
        device['domain'] = device.pop(DsalKey.domains)
        domains = device['domain']
        for domain_index in range(len(domains)):
            domain = domains[domain_index]
            domain['id'] = domain_index
            domain['domain_qos'] = domain.pop(DsalKey.qos)
            domain['partition'] = domain.pop(DsalKey.partitions)
            for partition in domain['partition']:
                partition['publisher'] = partition.pop(DsalKey.publishers, dict())
                partition['subscriber'] = partition.pop(DsalKey.subscribers, dict())
                pubs = partition.get('publisher')
                subs = partition.get('subscriber')
                for pub_index in range(len(pubs)):
                    pub = pubs[pub_index]
                    pub['id'] = pub_index+1
                    pub['pub_qos'] = pub.pop(DsalKey.qos)
                    pub['data_writer'] = pub.pop(DsalKey.data_writers)
                    dws = pub['data_writer']
                    for dw_index in range(len(dws)):
                        dw = dws[dw_index]
                        dw['id'] = dw_index
                        dw['dw_qos'] = dw.pop(DsalKey.qos)
                        dw['size'] = dw.pop(DsalKey.msg_size)
                        dw['cycletime'] = dw.pop(DsalKey.msg_cycletime)
                        dw.pop(DsalKey.name)
                for sub_index in range(len(subs)):
                    sub = subs[sub_index]
                    sub['id'] = sub_index+1
                    sub['sub_qos'] = sub.pop(DsalKey.qos)
                    sub['data_reader'] = sub.pop(DsalKey.data_readers)
                    drs = sub['data_reader']
                    for dr_index in range(len(drs)):
                        dr = drs[dr_index]
                        dr['id'] = dr_index
                        dr['dr_qos'] = dr.pop(DsalKey.qos)
                        dr.pop(DsalKey.name)
    return cp


def dsal_append_devices(dsal: dict) -> dict:
    cp = deepcopy(dsal)
    devices = []
    for device in cp[DsalKey.devices]:
        number = device.pop(DsalKey.number) - 1
        for i in range(number):
            copy_device = deepcopy(device)
            copy_device[DsalKey.name] = '{}_{}'.format(
                device[DsalKey.name], i+1)
            devices.append(copy_device)
    cp[DsalKey.devices].extend(devices)
    return cp


def dsal_to_datasetting(dsal: dict) -> dict:
    datasetting = {
        'device': [],
        'topic': []
    }
    datasetting['topic'] = dsal[DsalKey.define_topic]
    datasetting['device'] = dsal[DsalKey.devices]
    return datasetting


def convert_dsal_to_datasetting(src: str) -> dict:
    dsal = loads(src)
    dsal = dsal_modify_keys(dsal)
    dsal = dsal_append_devices(dsal)
    datasetting = dsal_to_datasetting(dsal)
    return datasetting
