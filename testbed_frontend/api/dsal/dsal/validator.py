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
from os import path, sep

import jsonschema

from . import (SCHEMA_BASIC_TYPE, SCHEMA_DEFINE_DATA_READER,
               SCHEMA_DEFINE_DATA_WRITER, SCHEMA_DEFINE_QOS,
               SCHEMA_DEFINE_TOPIC, SCHEMA_DEVICES, SCHEMA_FOLDER, SCHEMA_ROOT)
from .exceptions import DsalSchemaError
from .resolver import resolve_schema_references


def create_uri(abs_dir_path: str, filename: str):
    p = path.join(abs_dir_path, filename)
    return 'file:{}{}{}'.format(sep, sep, p)

# extend validator to support default of properties


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(
            validator, properties, instance, schema,
        ):
            yield error

    return jsonschema.validators.extend(validator_class, {"properties": set_defaults})


class check_schema():
    def __init__(self, func):
        self._func = func

    def _get_schema_path(self):
        current_path = path.dirname(path.abspath(__file__))
        return path.join(current_path, SCHEMA_FOLDER)

    def _get_schema_uri(self):
        return create_uri(self._schema_path, "")

    def _load_schema(self):
        self._store = {}
        with open(path.join(self._schema_path, SCHEMA_BASIC_TYPE)) as f:
            self._store[SCHEMA_BASIC_TYPE] = json.load(f)
        with open(path.join(self._schema_path, SCHEMA_DEFINE_QOS)) as f:
            self._store[SCHEMA_DEFINE_QOS] = json.load(f)
        with open(path.join(self._schema_path, SCHEMA_DEFINE_TOPIC)) as f:
            self._store[SCHEMA_DEFINE_TOPIC] = json.load(f)
        with open(path.join(self._schema_path, SCHEMA_DEFINE_DATA_WRITER)) as f:
            self._store[SCHEMA_DEFINE_DATA_WRITER] = json.load(f)
        with open(path.join(self._schema_path, SCHEMA_DEFINE_DATA_READER)) as f:
            self._store[SCHEMA_DEFINE_DATA_READER] = json.load(f)
        with open(path.join(self._schema_path, SCHEMA_DEVICES)) as f:
            self._store[SCHEMA_DEVICES] = json.load(f)
        with open(path.join(self._schema_path, SCHEMA_ROOT)) as f:
            schema = json.load(f)
        return resolve_schema_references(schema, self._store)

    def _create_validator(self):
        validator = jsonschema.Draft7Validator(self._schema)
        self.validator = extend_with_default(validator)

    def __call__(self, *args, **kargs):
        self._schema_path = self._get_schema_path()
        self._schema_uri = self._get_schema_uri()
        self._schema = self._load_schema()
        self._create_validator()
        dsal = self._func(*args, **kargs)
        try:
            self.validator(self._schema).validate(dsal)
        except jsonschema.ValidationError as e:
            raise DsalSchemaError(e.message, e.absolute_path)
        return dsal
