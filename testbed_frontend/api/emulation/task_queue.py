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
from datetime import datetime
import queue
import threading


class TaskQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.mutex = threading.Lock()

    def get_all_tasks(self) -> list:
        return list(self.queue.queue)

    def get_pending_task_size(self) -> int:
        return self.queue.qsize()

    def add_task(self, task: dict):
        self.mutex.acquire()
        task['emulation_task_id'] = datetime.now().strftime('%Y%m%d%H%M%S%f')
        self.queue.put(task)
        self.mutex.release()

        return task

    def get_first_task(self):
        self.mutex.acquire()
        task = self.queue.get()
        self.mutex.release()

        return task

    def cancel_pending_task(self, task_id):
        qsize = self.queue.qsize()

        self.mutex.acquire()
        for _ in range(qsize):
            task = self.queue.get()
            print(task)
            if task_id == task['emulation_task_id']:
                print('delete')
                delete_task = task
            else:
                print('put')
                self.queue.put(task)
        self.mutex.release()

        return delete_task
