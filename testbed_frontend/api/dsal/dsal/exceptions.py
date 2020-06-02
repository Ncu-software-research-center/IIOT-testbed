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
from . import DsalKey, DDS_QOS, DDS_ENTITY_TOPIC, DDS_ENTITY_DATA_WRITER, DDS_ENTITY_DATA_READER, DDS_ENTITY_PUBLISHERS, DDS_ENTITY_SUBSCRIBERS


class DsalError(Exception):
    def __init__(self, message, at):
        self.message = message
        self.at = at

    def _msg(self):
        return self.message

    def _at(self):
        return self.at

    def __str__(self):
        return self.__class__.__name__ + ": " + self._msg() + ", at: " + self._at()


class DsalSchemaError(DsalError):
    def _at(self):
        return 'dsal' or ' -> '.join([str(x) for x in list(self.at)])


class DsalQosConsistencyError(DsalError):
    def __init__(self, qos, constraint, at):
        self.qos = qos
        self.constraint = constraint
        super(DsalQosConsistencyError, self).__init__('', at)

    def _msg(self):
        return 'DDS QoS Policy: {}, Constraint: {}'.format(self.qos, self.constraint)

    def _at(self):
        return 'dsal -> define_qos: name="{}"'.format(self.at)


class DsalQosCompatibilityError(DsalError):
    def __init__(self, qos, consistency, dw_key, dr_key):
        self.qos = qos
        self.consistency = consistency
        self.dw_key = dw_key
        self.dr_key = dr_key

    def _msg(self):
        return 'DDS QoS QoS Policy RxO check: {}, Compatibility: {}'.format(self.qos, self.consistency)

    def _at(self):
        return 'data_writer:{}, data_reader:{}'.format(self.dw_key, self.dr_key)


class DsalDuplicatedNameError(DsalError):
    def __init__(self, name, path, item1, item2):
        self.name = name
        self.path = path
        self.item1 = item1
        self.item2 = item2

    def _msg(self):
        return 'found duplicated name="{}"'.format(self.name)

    def _at(self):
        return 'dsal -> {}: first={}, second={}'.format(self.path, self.item1, self.item2)


class DsalNameEqualsBaseError(DsalError):
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def _msg(self):
        return 'found name equals base="{}"'.format(self.name)

    def _at(self):
        return 'dsal -> {}'.format(self.path)


class DsalNotFoundError(DsalError):
    def __init__(self, key, value, path):
        self.key = key
        self.value = value
        self.path = path

    def _msg(self):
        return '{}="{}" not found'.format(self.key, self.value)

    def _at(self):
        return 'dsal -> {}'.format(self.path)


class DsalBaseNotFoundError(DsalNotFoundError):
    def __init__(self, base, path):
        super(DsalBaseNotFoundError, self).__init__(DsalKey.base, base, path)


class DsalQosNotFoundError(DsalNotFoundError):
    def __init__(self, qos, path):
        super(DsalQosNotFoundError, self).__init__(DsalKey.qos, qos, path)


class DsalSrcTopicNotFoundError(DsalNotFoundError):
    def __init__(self, topic, path):
        super(DsalSrcTopicNotFoundError, self).__init__(
            DsalKey.src_topic, topic, path)


class DsalDstTopicNotFoundError(DsalNotFoundError):
    def __init__(self, topic, path):
        super(DsalDstTopicNotFoundError, self).__init__(
            DsalKey.dst_topic, topic, path)


class DsalDataWriterNotFoundError(DsalNotFoundError):
    def __init__(self, dw, path):
        super(DsalDataWriterNotFoundError, self).__init__(
            DsalKey.define_data_writer, dw, path)


class DsalDataReaderNotFoundError(DsalNotFoundError):
    def __init__(self, dr, path):
        super(DsalDataReaderNotFoundError, self).__init__(
            DsalKey.define_data_reader, dr, path)
