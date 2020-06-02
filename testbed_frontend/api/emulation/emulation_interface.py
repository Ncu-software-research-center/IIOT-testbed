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
import os
import re
import time

import redis

from api.emulation import Config, WorkerStatus, EmulationStatus
from .emulation_handler import abort_handled
from .emulation_manager import EmulationManager
from .utils import generator, parser, transformer


class EmulationInterface:
    def __init__(self):
        self._emulation_data = None
        self.redis_connection = redis.StrictRedis(
            host=Config.FRONTEND_IP, port=Config.REDIS_PORT, password=Config.REDIS_PASSWORD,
            encoding="utf-8", decode_responses=True)
        self.ip_collection = []

    @property
    def emulation_data(self):
        return self._emulation_data

    @emulation_data.setter
    def emulation_data(self, emulation_data):
        self._emulation_data = emulation_data

    @abort_handled
    def _generate_emultaion_data(self, emulation_task: dict):
        data_setting = transformer.transform_kind_qos(emulation_task['data_setting'])
        self.emulation_data = generator.generate_emulation_data(data_setting, emulation_task['emulation_time'])

    @abort_handled
    def _start_emulation(self):
        print("Start emulation")
        manager = EmulationManager()
        manager.init(self.emulation_data)
        manager.ready()
        manager.start()
        manager.finish()
        print('Finish emulation')

    def _get_device_ip(self):
        pattern = re.compile("ip:.+")
        if self.ip_collection:
            return self.ip_collection

        self.ip_collection = [key for key in self.emulation_data.keys() if pattern.match(key)]
        return self.ip_collection

    @abort_handled
    def _parse_device_report(self, dsal_filename: str, report_name: str):
        # prase report after emulation finished
        report_generator = parser.ReportGenerator()
        ip_collection = self._get_device_ip()
        report = report_generator.generate_performance_report(ip_collection)
        report_generator.save_performance_report(dsal_filename, report_name, report)

    def _handle_abort_task(self):
        ip_collection = self._get_device_ip()
        tasks_are_aborting = True
        while tasks_are_aborting:
            print('task are aborting')
            aborting_devices = 0
            for ip in ip_collection:
                if self.redis_connection.hget(ip, 'worker_status') != WorkerStatus.WAIT:
                    aborting_devices += 1

            tasks_are_aborting = (aborting_devices > 0)
            time.sleep(1)

    def _init_redis_table(self):
        """
            Initialize redis table by given ip address.
        """
        try:
            ip_collection = self._get_device_ip()

            for ip in ip_collection:
                self.redis_connection.set("stop_agentworker", "")
                self.redis_connection.hset(ip, "device_name", "")
                self.redis_connection.hset(ip, "device_settings", "")
                self.redis_connection.hset(ip, "device_report", "")
                self.redis_connection.hset(ip, "worker_status", WorkerStatus.WAIT)
        except Exception as e:
            print("_init_redis_table error", e)
            return False

        return True

    def execute_emulation(self, emulation_task: dict):
        self._generate_emultaion_data(emulation_task)
        self._start_emulation()
        self._parse_device_report(emulation_task['dsal_filename'], emulation_task['report_name'])
        if self.redis_connection.get('emulation_status') == EmulationStatus.ABORT:
            self._handle_abort_task()                
        self._init_redis_table()
