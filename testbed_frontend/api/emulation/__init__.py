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
class Config:
    FRONTEND_IP = '{FRONTEND_IP}'
    REDIS_PORT = 6379
    REDIS_PASSWORD = 'redispass'

class EmulationStatus:
    INIT = '0'
    START = '1'
    END = '2'
    EXCEPTION = '3'
    ABORT = '4'


class WorkerStatus:
    WAIT = '0'
    PREPARE = '1'
    READY = '2'
    DONE = '3'
    EXCEPTION = '4'
