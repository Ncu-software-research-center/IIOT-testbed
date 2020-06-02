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
import json
import time

import redis

from api.emulation import (
    Config,
    EmulationStatus,
    WorkerStatus
)
from .emulation_handler import abort_handled
from .utils import parser


class EmulationManager:
    def __init__(self):
        self.ip_collection = None
        self.redis_connection = redis.StrictRedis(
            host=Config.FRONTEND_IP, port=Config.REDIS_PORT, password=Config.REDIS_PASSWORD,
            encoding="utf-8", decode_responses=True)

    @abort_handled
    def init(self, emulation_data: dict):
        """
            Initialize the redis using the specific emualtion data, then set
            emulation status to `init`.

            Args:
                emulation_data (dict): Emulation data.
        """
        print('emulation initialization.')
        self.redis_connection.set('emulation_status', EmulationStatus.INIT)
        self.redis_connection.set('emulation_time', emulation_data['emulation_time'])
        self.ip_collection = [key for key in emulation_data.keys() if 'ip' in key]
        for ip in self.ip_collection:
            self.redis_connection.hset(ip, 'device_name', emulation_data[ip]['device_name'])
            self.redis_connection.hset(ip, 'device_settings', json.dumps(emulation_data[ip]['device_setting']))
            self.redis_connection.hset(ip, 'worker_status', WorkerStatus.PREPARE)

    @abort_handled
    def ready(self):
        """
            Waiting for all device is ready to run emulation. If all device is ready,
            set the emulation status to `start`.
        """
        while not self.check_worker_status(WorkerStatus.READY):
            print("Waiting for all of worker is ready.")
            if self.redis_connection.get('emulation_status') == EmulationStatus.ABORT:
                break
            else:
                time.sleep(1)

    @abort_handled
    def start(self):
        self.redis_connection.set("emulation_status", EmulationStatus.START)
        while not self.check_worker_status(WorkerStatus.DONE):
            print("Waiting for emulation finish.")
            if self.redis_connection.get('emulation_status') == EmulationStatus.ABORT:
                break
            else:
                time.sleep(1)

    @abort_handled
    def finish(self):
        """
            Waiting for the emulation in each device are finished. After every device finish
            the emulations, re-initialize redis table, then set emulation status to `end`.
        """
        self.redis_connection.set("emulation_status", EmulationStatus.END)
        print("done")

    def check_worker_status(self, status):
        print(status, end=": ")
        worker_status_count = 0
        for ip in self.ip_collection:
            if self.redis_connection.hget(ip, "worker_status") == status:
                worker_status_count += 1
                print("{}.".format(ip), end=" ")
            else:
                print("{}.".format(ip), end=" ")

        return worker_status_count == len(self.ip_collection)




