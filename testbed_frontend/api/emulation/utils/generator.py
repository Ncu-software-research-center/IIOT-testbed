"""
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

This module used to generate emulation file.

Example:
    python generate_emulation_file.py -i data-setting.json -o emulation.json
"""
from collections import deque
import json
import time

import redis

from . import json_resolver
from api.emulation import Config


class DevicesNotEnoughException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "DevicesNotEnoughException: {}".format(self.message)


def _get_needed_topics(device: dict, topics: dict) -> list:
    """
        Get the all of destination topic sent by data writer in publisher and read by data reader in subscriber
    """
    dst_topic, src_topic = [], []
    for domain in device["domain"]:
        for partition in domain["partition"]:
            for publisher in partition["publisher"]:
                dst_topic += [dw["dst_topic"] for dw in publisher["data_writer"]]

            for subscriber in partition["subscriber"]:
                src_topic += [dr["src_topic"] for dr in subscriber["data_reader"]]

    needed_topic = []
    for topic in topics:
        if topic['name'] in dst_topic+src_topic:
            needed_topic.append(topic)
    return needed_topic


def _get_computing_resource(data_setting: dict) -> list:
    computing_resource = []
    devices = data_setting["device"]
    topics = data_setting["topic"]

    for device in devices:
        needed_topic = _get_needed_topics(device, topics)
        resource = {}
        resource["device_name"] = device["name"]
        resource["device_setting"] = {"domain": device["domain"][0]}
        resource["device_setting"]["domain"]["topic"] = needed_topic
        computing_resource.append(resource)


    return computing_resource


def _get_avaliable_ip_address():
    """
        This function used to get avaliable ip address that already connected to redis.
    """
    def check_heartbeat(ip_address):
        TIME_LIMIT = 2
        current_time = float(client.time()[0])
        worker_time = float(client.hget(ip_address, "time"))
        return current_time - worker_time < TIME_LIMIT

    client = redis.StrictRedis(
        host=Config.FRONTEND_IP, port=Config.REDIS_PORT, password=Config.REDIS_PASSWORD, 
        encoding="utf-8", decode_responses=True)
    time.sleep(1)
    avaliable_ip_address = []
    for ip in client.scan_iter("ip:*"):
        if check_heartbeat(ip):
            avaliable_ip_address.append(ip)

    return avaliable_ip_address


def _distribute_computing_resource(data_setting: dict) -> dict:
    """
        Distribute the device to each device setting.

        Args:
            data_setting: data setting.

        Return:
            Emulation data
    """
    computing_resource = _get_computing_resource(data_setting)
    ip_address = deque(_get_avaliable_ip_address())
    if len(ip_address) >= len(computing_resource):
        distributed_computing_resource = {}
        for resource in computing_resource:
            backend_ip = ip_address.popleft()
            distributed_computing_resource[backend_ip] = resource

        return distributed_computing_resource
    else:
        raise DevicesNotEnoughException("The number of devices aren't enough to do emulation. " \
                                        "Which must be >= {}".format(len(computing_resource)))


def generate_emulation_data(data_setting: dict, emulation_time: int) -> dict:
    """
        Intsert the Generate emulation file.

        Args:
            data_setting (dict): The settings of each topic and device.
         emulation_time (int): emulation time.

        Return:
            Emulation data.
    """
    emulation_data = _distribute_computing_resource(data_setting)
    emulation_data['emulation_time'] = emulation_time

    return emulation_data
