"""
Copyright © 2017 Stitch
Distributed under the Apache License Version 2.0

Reference from:
https://github.com/singer-io/singer-python

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
"""

from jsonschema import RefResolver


class SchemaKey:
    ref = "$ref"
    items = "items"
    properties = "properties"
    pattern_properties = "patternProperties"
    any_of = 'anyOf'
    _if = "if"
    _then = 'then'
    _else = 'else'


def resolve_schema_references(schema, refs=None):
    refs = refs or {}
    return _resolve_schema_references(schema, RefResolver("", schema, store=refs))


def _resolve_schema_references(schema, resolver):
    if SchemaKey.ref in schema:
        reference_path = schema.pop(SchemaKey.ref, None)
        resolved = resolver.resolve(reference_path)[1]
        schema.update(resolved)
        return _resolve_schema_references(schema, resolver)

    if SchemaKey.properties in schema:
        for k, val in schema[SchemaKey.properties].items():
            schema[SchemaKey.properties][k] = _resolve_schema_references(
                val, resolver)

    if SchemaKey.pattern_properties in schema:
        for k, val in schema[SchemaKey.pattern_properties].items():
            schema[SchemaKey.pattern_properties][k] = _resolve_schema_references(
                val, resolver)

    if SchemaKey.items in schema:
        schema[SchemaKey.items] = _resolve_schema_references(
            schema[SchemaKey.items], resolver)

    if SchemaKey.any_of in schema:
        for i, element in enumerate(schema[SchemaKey.any_of]):
            schema[SchemaKey.any_of][i] = _resolve_schema_references(
                element, resolver)

    if SchemaKey._if in schema:
        schema[SchemaKey._if] = _resolve_schema_references(
            schema[SchemaKey._if], resolver)

    if SchemaKey._then in schema:
        schema[SchemaKey._then] = _resolve_schema_references(
            schema[SchemaKey._then], resolver)

    if SchemaKey._else in schema:
        schema[SchemaKey._else] = _resolve_schema_references(
            schema[SchemaKey._else], resolver)

    return schema
