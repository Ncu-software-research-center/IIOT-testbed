"""
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

Transform the kind value of qos setting to number.
"""

QUALITY_OF_SERVICE = {
    "durability": ["volatile", "transient_local", "transient", "persistent"],
    "presentation": ["instance", "topic", "group"],
    "ownership": ["shared", "exclusive"],
    "liveliness": ["automatic", "manual_by_participant", "manual_by_topic"],
    "reliability": ["best_effort", "reliable"],
    "destination_order": ["by_reception_timestamp", "by_source_timestamp"],
    "history": ["keep_last", "keep_all"],
    "reader_data_lifecycle": ["no_invalid_samples", "minimum_invalid_samples",
                              "all_invalid_samples"],
    "durability_service": ["keep_last", "keep_all"]
}


def resolve_kind_value(qos, value):
    return QUALITY_OF_SERVICE[qos].index(value['kind'])


def transform_kind_qos(properties: dict):
    for key, value in properties.items():
        if key in QUALITY_OF_SERVICE.keys():
            properties[key]['kind'] = resolve_kind_value(key, value)
        elif isinstance(value, dict):
            transform_kind_qos(value)
        elif isinstance(value, list):
            for val in value:
                transform_kind_qos(val)
    return properties
