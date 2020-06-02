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
import hashlib
from django.db import models


class Dsal(models.Model):
    dsal_filename = models.CharField(max_length=100, primary_key=True)
    dsal_content = models.TextField()
    dsal_updated = models.DateTimeField(auto_now=True)
    dsal_hash = models.CharField(max_length=64, unique=True, default=None)

    def save(self, *args, **kwargs):
        self.dsal_hash = hashlib.sha256(self.dsal_content.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)


class Report(models.Model):
    dsal = models.ForeignKey(Dsal, on_delete=models.CASCADE)
    report_name = models.CharField(max_length=100, primary_key=True)
    report_content = models.TextField()
    report_created = models.DateTimeField()

    class Meta:
        ordering = ['report_created']