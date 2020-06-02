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
import os
import re
from statistics import mean

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testbed.settings")
django.setup()
from django.utils import timezone
import redis

from . import json_resolver
from api.models import Dsal, Report
from api.emulation import Config


class PerformanceReport:
    def __init__(self):
        self._performance_report = []

    @property
    def performance_report(self):
        return self._performance_report

    def set_performance_report(self, device_report: dict, resource_usage: dict):
        for report in device_report.values():
            self._set_report(report, resource_usage)

    def _set_report(self, report: dict, resource_usage: dict):
        pattern = re.compile(r'(?P<device_name>\w+)-(?P<publisher_id>\w+)-(?P<data_reader_or_writer>\w+)')
        pub_device_name = pattern.match(report['src_device']).group('device_name')
        sub_device_name = pattern.match(report['dst_device']).group('device_name')
        pub_resource_usage = resource_usage[pub_device_name]
        sub_resource_usage = resource_usage[sub_device_name]
        _report = {
            'partition': report['partition'],
            'publisher': pub_device_name,
            'pub_cpu_usgae': pub_resource_usage['cpu_usage'],
            'pub_memory_usgae': pub_resource_usage['memory_usage'],
            'pub_bandwidth_receive': pub_resource_usage['bandwidth_receive'],
            'pub_bandwidth_transmit': pub_resource_usage['bandwidth_transmit'],
            'topic': report['dst_topic'],
            'letency': mean(report['latency']),
            'loss_rate': (1 - report['sub_msg_count']/report['pub_msg_count']),
            'subscriber': sub_device_name,
            'sub_cpu_usgae': sub_resource_usage['cpu_usage'],
            'sub_memory_usgae': sub_resource_usage['memory_usage'],
            'sub_bandwidth_receive': sub_resource_usage['bandwidth_receive'],
            'sub_bandwidth_transmit': sub_resource_usage['bandwidth_transmit'],
        }
        self._performance_report.append(_report)

    def get_json(self):
        return {'report': self._performance_report}


class DeviceReportParser:
    def __init__(self):
        self.device_name = None
        self.device_report = None
        self._parsed_report = {}
        self._parsed_resource_usage = {}

    @property
    def parsed_report(self):
        return self._parsed_report

    @property
    def parsed_resource_usage(self):
        return self._parsed_resource_usage

    def parse_device_report(self, device_name: str, device_report: dict):
        self.device_name = device_name
        self.device_report = device_report
        self._parse_report()

    def _parse_report(self):
        self._parse_and_set_data_readers_report()
        self._parse_and_set_data_writers_report()
        self._parse_and_set_resource_usage_report()

    def _parse_and_set_data_readers_report(self):
        """
            Build key-value of each report in data readers.
        """
        data_readers_report = self.device_report['data_readers'] or list()
        for data_reader_report in data_readers_report:
            # key: <partition>-<pub_device>-<pub_id>-<dw_id>-<topic>-<sub_device>-<sub_id>-<dr_id>
            key = '{}-{}-{}-{}-{}-{}'.format(
                data_reader_report['partition'],
                data_reader_report['src_device'],
                data_reader_report['src_topic'],
                self.device_name,
                data_reader_report['sub_id'],
                data_reader_report['id']
                )
            self._set_parsed_report(key, data_reader_report)

    def _parse_and_set_data_writers_report(self):
        """
            Build key-value of each report in data writers.
        """
        data_writers_report = self.device_report['data_writers'] or list()
        for data_writer_report in data_writers_report:
            # key: <partition>-<pub_device>-<pub_id>-<dw_id>-<topic>-<sub_device>-<sub_id>-<dr_id>
            key = '{}-{}-{}-{}-{}-{}'.format(
                data_writer_report['partition'],
                self.device_name,
                data_writer_report['pub_id'],
                data_writer_report['id'],
                data_writer_report['dst_topic'],
                data_writer_report['dst_device'])
            self._set_parsed_report(key, data_writer_report)

    def _set_parsed_report(self, key: str, report: dict):
        if key in self._parsed_report:
            self._parsed_report[key].update(**report)
        else:
            self._parsed_report[key] = report

    def _parse_and_set_resource_usage_report(self):
        self._parsed_resource_usage[self.device_name] = {
            'cpu_usage': mean(self.device_report['resource']['cpu']),
            'memory_usage': mean(self.device_report['resource']['memory']),
            'bandwidth_receive': mean(self.device_report['resource']['rx']),
            'bandwidth_transmit': mean(self.device_report['resource']['tx'])
        }


class ReportGenerator:
    def __init__(self):
        self.performance_report = PerformanceReport()
        self.report_parser = DeviceReportParser()
        self.redis_connection = redis.StrictRedis(
            host=Config.FRONTEND_IP, port=Config.REDIS_PORT, password=Config.REDIS_PASSWORD,
            encoding="utf-8", decode_responses=True)

    def generate_performance_report(self, ip_collection: list) -> dict:
        """
            Generate performance report by given device report
        """
        # Read and parse device report
        for ip in ip_collection:
            device_name = self.redis_connection.hget(ip, 'device_name')
            device_report = self.redis_connection.hget(ip, 'device_report')
            self.report_parser.parse_device_report(device_name, json.loads(device_report))

        self.performance_report.set_performance_report(self.report_parser.parsed_report,
                                                       self.report_parser.parsed_resource_usage)

        return self.performance_report.get_json()

    def save_performance_report(self, dsal_filename: str, report_name: str, report: dict):
        """
            Save perfromance report into database
        """
        dsal = Dsal.objects.get(dsal_filename=dsal_filename)
        report_instance = Report(
            dsal=dsal,
            report_name=report_name,
            report_content=report,
            report_created=timezone.now()
        )
        report_instance.save()
        return report_instance
