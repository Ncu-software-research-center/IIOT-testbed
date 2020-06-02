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
# constant value, do not modify them in runtime
SCHEMA_FOLDER             = 'schema'
SCHEMA_ROOT               = 'dsal.json'
SCHEMA_BASIC_TYPE         = 'basic_type.json'
SCHEMA_DEFINE_QOS         = 'define_qos.json'
SCHEMA_DEFINE_TOPIC       = 'define_topic.json'
SCHEMA_DEFINE_DATA_WRITER = 'define_data_writer.json'
SCHEMA_DEFINE_DATA_READER = 'define_data_reader.json'
SCHEMA_DEVICES            = 'devices.json'

DDS_QOS                = 'qos'
DDS_ENTITY_TOPIC       = 'topic'
DDS_ENTITY_DATA_WRITER = 'data_writer'
DDS_ENTITY_DATA_READER = 'data_reader'
DDS_ENTITY_PUBLISHERS  = 'publishers'
DDS_ENTITY_SUBSCRIBERS = 'subscribers'

class DsalKey():
    dsal               = 'dsal'
    define_qos         = 'define_qos'
    define_topic       = 'define_topic'
    define_data_writer = 'define_data_writer'
    define_data_reader = 'define_data_reader'
    devices            = 'devices'
    domains            = 'domains'
    partitions         = 'partitions'
    publishers         = 'publishers'
    data_writers       = 'data_writers'
    subscribers        = 'subscribers'
    data_readers       = 'data_readers'
    version            = 'version'
    profile_name       = 'profile_name'
    name               = 'name'
    number             = 'number'
    base               = 'base'
    qos                = 'qos'
    default            = 'default'
    src_topic          = 'src_topic'
    dst_topic          = 'dst_topic'
    msg_size           = 'msg_size'
    msg_cycletime      = 'msg_cycletime'

from .exceptions import *
from .core import loads
