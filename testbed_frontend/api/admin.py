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
from django.contrib import admin

from .models import Dsal, Report


class DsalAdmin(admin.ModelAdmin):
    list_display = ('dsal_filename', 'dsal_content')


class ReportAdmin(admin.ModelAdmin):
    list_display = ('dsal', 'report_name', 'report_content')


admin.site.register(Dsal, DsalAdmin)
admin.site.register(Report, ReportAdmin)
