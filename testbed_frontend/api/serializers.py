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
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Dsal, Report


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class DsalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dsal
        fields = ('dsal_filename', 'dsal_content', 'dsal_updated', 'dsal_hash')


class EmulationSerializer(serializers.Serializer):
    emulation_task_id = serializers.CharField()
    emulation_time = serializers.IntegerField()
    emulation_status = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    dsal_filename = serializers.CharField(max_length=100)
    data_setting = serializers.CharField()
    report_name = serializers.CharField(max_length=100)


class JSONSerializerField(serializers.Field):
    """Serializer for JSONField -- required to make field writable"""

    def to_representation(self, value):
        json_data = {}
        try:
            json_data = json.loads(value.replace("'", '"'))
        except ValueError as e:
            print(e)
            raise e
        finally:
            return json_data

    def to_internal_value(self, data):
        return json.dumps(data)


class ReportSerializer(serializers.ModelSerializer):
    report_content = JSONSerializerField()

    class Meta:
        model = Report
        fields = ('dsal', 'report_name', 'report_content', 'report_created')
