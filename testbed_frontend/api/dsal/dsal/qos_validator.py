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
from .exceptions import DsalQosConsistencyError, DsalQosCompatibilityError
from .qos import QosKey


def durability_service_consistency_validate(durability_service: dict, name: str):
    qos_name = QosKey.durability_service
    constraint = 'if kind="keep_last", max_samples_per_instance >= depth'
    kind = durability_service[QosKey._kind]
    depth = durability_service[QosKey._depth]
    max_samples_per_instance = durability_service[QosKey._max_samples_per_instance]
    if kind == 'keep_last':
        # unlimited
        if max_samples_per_instance != -1:
            if not (max_samples_per_instance >= depth):
                raise DsalQosConsistencyError(qos_name, constraint, name)


def lifespan_consistency_validate(lifespan: dict, name: str):
    qos_name = QosKey.lifespan
    constraint = 'duration.sec + duration.nanosec > 0'
    sec = lifespan[QosKey._duration][QosKey._sec]
    nanosec = lifespan[QosKey._duration][QosKey._nanosec]
    if not(sec + nanosec > 0):
        raise DsalQosConsistencyError(qos_name, constraint, name)


def resource_limits_consistency_validate(resource_limits: dict, name: str):
    qos_name = QosKey.resource_limits
    constraint = 'max_samples >= max_samples_per_instance'
    max_samples = resource_limits[QosKey._max_samples]
    max_samples_per_instance = resource_limits[QosKey._max_samples_per_instance]
    # unlimited
    if max_samples != -1:
        if not (max_samples >= max_samples_per_instance):
            raise DsalQosConsistencyError(qos_name, constraint, name)


def resource_limits_history_consistency_validate(resource_limits: dict, history: dict, name: str):
    qos_name = ', '.join([QosKey.resource_limits, QosKey.history])
    constraint = 'if history.kind="keep_last", resource_limits.max_samples_per_instance >= history.depth'
    depth = history[QosKey._depth]
    max_samples_per_instance = resource_limits[QosKey._max_samples_per_instance]
    # unlimited
    if max_samples_per_instance != -1:
        if not (max_samples_per_instance >= depth):
            raise DsalQosConsistencyError(qos_name, constraint, name)


def time_based_filter_deadline_consistency_validate(time_based_filter: dict, deadline: dict, name: str):
    qos_name = ', '.join([QosKey.time_based_filter, QosKey.deadline])
    constraint = 'deadline.period >= time_based_filter.minimum_separation'
    period = deadline[QosKey._period][QosKey._sec] + \
        deadline[QosKey._period][QosKey._nanosec]/(10**9)
    minimum_separation = time_based_filter[QosKey._minimum_separation][QosKey._sec] + \
        time_based_filter[QosKey._minimum_separation][QosKey._sec]/(10**9)
    if not (period >= minimum_separation):
        raise DsalQosConsistencyError(qos_name, constraint, name)


def deadline_compatibility_validate(requested: dict, offered: dict, dw_key: str, dr_key: str):
    qos_name = QosKey.deadline
    compatibility = 'offered period > requested period'
    r_period = requested[QosKey._period][QosKey._sec] + \
        requested[QosKey._period][QosKey._nanosec]/10**9
    o_period = offered[QosKey._period][QosKey._sec] + \
        offered[QosKey._period][QosKey._nanosec]/10**9
    if o_period > r_period:
        raise DsalQosCompatibilityError(
            qos_name, compatibility, dw_key, dr_key)


def destination_order_compatibility_validate(requested: dict, offered: dict, dw_key: str, dr_key: str):
    qos_name = QosKey.destination_order
    compatibility = 'offered kind == by_reception_timestamp, requested kind == by_source_time_stamp'
    r_kind = requested[QosKey._kind]
    o_kind = offered[QosKey._kind]
    if o_kind == 'by_reception_timestamp' and r_kind == 'by_source_time_stamp':
        raise DsalQosCompatibilityError(
            qos_name, compatibility, dw_key, dr_key)


def durability_compatibility_validate(requested: dict, offered: dict, dw_key: str, dr_key: str):
    qos_name = QosKey.durability
    compatibility = '''
        1. offered kind == volatile, requested kind != volatile
        2. offered kind == transient_local, requested kind == transient or persistent
        3. offered kind == transient, requested kind == persistent
        '''
    r_kind = requested[QosKey._kind]
    o_kind = offered[QosKey._kind]
    if o_kind == 'volatile' and r_kind != 'volatile':
        raise DsalQosCompatibilityError(
            qos_name, compatibility, dw_key, dr_key)
    if o_kind == 'transient_local' and (r_kind == 'transient' or r_kind == 'persistent'):
        raise DsalQosCompatibilityError(
            qos_name, compatibility, dw_key, dr_key)
    if o_kind == 'transient' and r_kind != 'persistent':
        raise DsalQosCompatibilityError(
            qos_name, compatibility, dw_key, dr_key)


def latency_budget_compatibility_validate(requested: dict, offered: dict, dw_key: str, dr_key: str):
    qos_name = QosKey.latency_budget
    compatibility = 'offered duration > requested duration'
    r_duration = requested[QosKey._duration][QosKey._sec] + \
        requested[QosKey._duration][QosKey._nanosec]/10**9
    o_duration = offered[QosKey._duration][QosKey._sec] + \
        offered[QosKey._duration][QosKey._nanosec]/10**9
    if o_duration > r_duration:
        raise DsalQosCompatibilityError(
            qos_name, compatibility, dw_key, dr_key)


def liveliness_compatibility_validate(requested: dict, offered: dict, dw_key: str, dr_key: str):
    qos_name = QosKey.liveliness
    compatibility = '''
        1. offered kind == automatic, requested kind != automatic
        2. offered kind == manual_by_participant, requested kind == manual_by_topic
        '''
    r_kind = requested[QosKey._kind]
    o_kind = offered[QosKey._kind]
    if o_kind == 'automatic' and r_kind != 'automatic':
        raise DsalQosCompatibilityError(
            qos_name, compatibility, dw_key, dr_key)
    if o_kind == 'manual_by_participant' and r_kind == 'manual_by_topic':
        raise DsalQosCompatibilityError(
            qos_name, compatibility, dw_key, dr_key)


def ownership_compatibility_validate(requested: dict, offered: dict, dw_key: str, dr_key: str):
    qos_name = QosKey.ownership
    compatibility = 'offered kind != requested kind'
    r_kind = requested[QosKey._kind]
    o_kind = offered[QosKey._kind]
    if r_kind != o_kind:
        raise DsalQosCompatibilityError(
            qos_name, compatibility, dw_key, dr_key)


def presentation_compatibility_validate(requested: dict, offered: dict, dw_key: str, dr_key: str):
    qos_name = QosKey.presentation
    compatibility = '''
        1. offered kind == instance, requested kind != instance
        2. offered kind == topic, requested kind == group
        '''
    r_kind = requested[QosKey._kind]
    o_kind = offered[QosKey._kind]
    if o_kind == 'instance' and r_kind != 'instance':
        raise DsalQosCompatibilityError(
            qos_name, compatibility, dw_key, dr_key)
    if o_kind == 'topic' and r_kind == 'group':
        raise DsalQosCompatibilityError(
            qos_name, compatibility, dw_key, dr_key)


def reliability_compatibility_validate(requested: dict, offered: dict, dw_key: str, dr_key: str):
    qos_name = QosKey.reliability
    compatibility = 'offered kind == best_effort, requested kind == reliabile'
    r_kind = requested[QosKey._kind]
    o_kind = offered[QosKey._kind]
    if o_kind == 'best_effort' and r_kind == 'reliabile':
        raise DsalQosCompatibilityError(
            qos_name, compatibility, dw_key, dr_key)
