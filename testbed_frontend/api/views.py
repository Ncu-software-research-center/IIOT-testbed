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
import codecs
import csv
import json
import os

from django.contrib.auth.models import User
from django.http import HttpResponse
import redis
from redis.exceptions import ConnectionError

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Dsal, Report
from .serializers import (
    UserSerializer,
    DsalSerializer,
    EmulationSerializer,
    ReportSerializer
)
from api.emulation.task_manager import TaskManager
from .dsal import convert_dsal_to_datasetting

task_manager = TaskManager()


class UserViewSet(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated,)


class DsalList(generics.ListCreateAPIView):
    queryset = Dsal.objects.all()
    serializer_class = DsalSerializer
    permission_classes = (IsAuthenticated,)


class DsalItem(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dsal.objects.all()
    serializer_class = DsalSerializer
    permission_classes = (IsAuthenticated,)


class DataSettings(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            data_setting = convert_dsal_to_datasetting(request.data['dsal_content'])
            return Response({'data_setting': data_setting})
        except Exception as e:
            return Response({'error': str(e)})


class DataSetting(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, dsal_filename):
        return Dsal.objects.get(dsal_filename=dsal_filename)

    def retrieve(self, request, dsal_filename):
        queryset = self.get_object(dsal_filename)
        serializer = DsalSerializer(queryset)
        dsal_content = codecs.decode(serializer.data['dsal_content'], 'unicode_escape')
        data_setting = convert_dsal_to_datasetting(dsal_content)

        return Response(data_setting)


class EmulationList(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)

    def list(self, request):
        try:
            emulation_tasks = task_manager.get_all_tasks()
            serializer = EmulationSerializer(emulation_tasks, many=True)
            return Response(serializer.data)
        except ConnectionError as e:
            return Response({'error': 'Redis failed to connect.'})

    def create(self, request):
        import json
        with open('data_setting.json', 'w') as outputflie:
            json.dump(request.data['task']['data_setting'], outputflie)
        new_task = task_manager.add_task_into_queue(request.data['task'])
        serializer = EmulationSerializer(new_task)
        return Response(serializer.data)


class EmulationItem(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, emulation_task_id):
        try:
            executing_task = task_manager.get_executing_task()
            executing_task['emulationStatus'] = task_manager.get_executing_task_status()
            serializer = EmulationSerializer(executing_task)
            return Response(serializer.data)
        except ConnectionError:
            return Response({'error': 'Redis failed to connect.'})

    def destroy(self, request, emulation_task_id):
        deleted_task = task_manager.delete_task(emulation_task_id)
        serializer = EmulationSerializer(deleted_task)
        return Response(serializer.data)


class ReportList(generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)


class ReportItem(generics.RetrieveDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)


class ReportDownload(generics.RetrieveAPIView):
    queryset = Report.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self, report_name):
        report_name = report_name.split('.')[0]
        return Report.objects.filter(report_name=report_name)

    def retrieve(self, request, report_file):
        report_name = report_file.split('.')[0]
        report = self.get_object(report_name)[0]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}'.format(report_file)

        csv_columns = ['partition',
                       'publisher',
                       'pub_cpu_usgae',
                       'pub_memory_usgae',
                       'pub_bandwidth_receive',
                       'pub_bandwidth_transmit',
                       'topic',
                       'letency',
                       'loss_rate',
                       'subscriber',
                       'sub_cpu_usgae',
                       'sub_memory_usgae',
                       'sub_bandwidth_receive',
                       'sub_bandwidth_transmit',]
        writer = csv.DictWriter(response, fieldnames=csv_columns)
        writer.writeheader()
        for row in eval(report.report_content)['report']:
            writer.writerow(row)
        return response


class AvailableDeviceList(generics.RetrieveAPIView):
    # permission_classes = (IsAuthenticated,)

    def retrieve(self, request):
        try:
            available_device = task_manager.get_available_device()
            return Response({'availableDevice' :available_device})
        except ConnectionError:
            return Response({'error': 'Redis failed to connect.'})
