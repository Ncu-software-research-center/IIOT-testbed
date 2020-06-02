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
import threading
import time
import redis

from api.emulation import Config, EmulationStatus
from api.emulation.task_queue import TaskQueue
from api.emulation.task_worker import TaskWorker


class TaskManager:
    def __init__(self):
        self.task_queue = TaskQueue()
        self.task_worker = TaskWorker()
        self.redis_connection = redis.StrictRedis(
            host=Config.FRONTEND_IP, port=Config.REDIS_PORT, password=Config.REDIS_PASSWORD,
            encoding="utf-8", decode_responses=True)
        self.wait_task()

    def wait_task(self):
        self.execution_thread = threading.Thread(target=self._exectue_task, name='execution_thread', args=())
        self.execution_thread.daemon = True
        self.execution_thread.start()

    def get_available_device(self):
        def check_heartbeat(ip_address):
            TIME_LIMIT = 2
            current_time = float(self.redis_connection.time()[0])
            worker_time = float(self.redis_connection.hget(ip_address, "time"))
            return current_time - worker_time < TIME_LIMIT

        time.sleep(1)
        avaliable_ip_address = []
        for ip in self.redis_connection.scan_iter("ip:*"):
            if check_heartbeat(ip):
                avaliable_ip_address.append(ip)

        return avaliable_ip_address

    def get_all_tasks(self):
        pending_tasks = self.task_queue.get_all_tasks()
        executing_task = self.task_worker.executing_task
        executing_task['emulation_status'] = self.get_executing_task_status()
        return [executing_task] + pending_tasks

    def get_task_size(self):
        return self.task_queue.get_pending_task_size() + int(self.task_worker.get_executing_task_id() != '0')

    def add_task_into_queue(self, task: dict):
        new_task = self.task_queue.add_task(task)
        return new_task

    def _manager_is_running(self):
        """
        This function is used to testting.
        """
        return True

    def _exectue_task(self):
        while self._manager_is_running():
            if self.task_queue.get_pending_task_size() > 0:
                print('execute task')
                task = self.task_queue.get_first_task()
                self.task_worker.execute_task(task)
                print('finish task')
            time.sleep(1)

    def _abort_executing_task(self):
        aborted_task = self.task_worker.abort_executing_task()
        return aborted_task

    def _cancel_task_from_queue(self, task_id):
        canceled_task = self.task_queue.cancel_pending_task(task_id)
        return canceled_task

    def delete_task(self, task_id):
        if self.task_worker.get_executing_task_id() == task_id:
            print('abort')
            deleted_task = self._abort_executing_task()
        else:
            deleted_task = self._cancel_task_from_queue(task_id)

        return deleted_task

    def get_executing_task(self):
        return self.task_worker.executing_task

    def get_executing_task_status(self):
        return self.task_worker.get_executing_task_status()
