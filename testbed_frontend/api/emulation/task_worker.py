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
import re
import time
import redis
from api.emulation import Config, EmulationStatus, WorkerStatus
from api.emulation.emulation_interface import EmulationInterface
from .emulation_handler import abort_handled


class TaskWorker:
    def __init__(self):
        self.emulation_interface = EmulationInterface()
        self._executing_task = {}
        self.reset_executing_task()
        self.redis_connection = redis.StrictRedis(
            host=Config.FRONTEND_IP, port=Config.REDIS_PORT, password=Config.REDIS_PASSWORD,
            encoding="utf-8", decode_responses=True)

    @property
    def executing_task(self):
        return self._executing_task

    @executing_task.setter
    def executing_task(self, task):
        self._executing_task = task

    def get_executing_task_id(self):
        return self._executing_task['emulation_task_id']

    @abort_handled
    def reset_executing_task(self):
        print('reset_executing_task')
        self._executing_task = {
            'emulation_task_id': '0',
            'emulation_time': 0,
            'dsal_filename': '',
            'data_setting': '',
            'report_name': ''
        }

    def execute_task(self, task):
        print('Execute Emulation')
        self._executing_task = task
        self.emulation_interface.execute_emulation(task)
        self.reset_executing_task()

    def abort_executing_task(self):
        self.redis_connection.set('emulation_status', EmulationStatus.ABORT)

        # Wait for all devices are abort the task.
        pattern = re.compile("ip:.+")
        ip_collection = [key for key in self.emulation_interface.emulation_data.keys() if pattern.match(key)]
        tasks_are_aborting = True
        while tasks_are_aborting:
            print('task are aborting')
            aborting_devices = 0
            for ip in ip_collection:
                if self.redis_connection.hget(ip, 'worker_status') != WorkerStatus.WAIT:
                    aborting_devices += 1

            tasks_are_aborting = (aborting_devices > 0)
            time.sleep(1)

        self.redis_connection.set('emulation_status', EmulationStatus.INIT)
        self.reset_executing_task()
        return self._executing_task

    def get_executing_task_status(self):
        return self.redis_connection.get('emulation_status')
