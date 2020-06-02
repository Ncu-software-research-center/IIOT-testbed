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
from functools import wraps
import redis
from api.emulation import (
    Config,
    EmulationStatus
)


def abort_handled(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        redis_connection = redis.StrictRedis(
            host=Config.FRONTEND_IP, port=Config.REDIS_PORT, password=Config.REDIS_PASSWORD,
            encoding="utf-8", decode_responses=True)
        if redis_connection.get('emulation_status') == EmulationStatus.ABORT:
            return

        return fun(*args, **kwargs)
    return wrapper
