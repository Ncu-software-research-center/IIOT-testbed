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
from django.urls import path, re_path
from api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tokenrefresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('users', views.UserViewSet.as_view()),
    path('dsals', views.DsalList.as_view()),
    path('dsals/<str:pk>', views.DsalItem.as_view()),
    path('dsals/<dsal_filename>/data-setting', views.DataSetting.as_view()),
    path('data-setting', views.DataSettings.as_view()),
    path('emulations', views.EmulationList.as_view()),
    path('emulations/<emulation_task_id>', views.EmulationItem.as_view()),
    path('reports', views.ReportList.as_view()),
    path('reports/<str:pk>', views.ReportItem.as_view()),
    path('reports/file/<report_file>', views.ReportDownload.as_view()),
    path('available-device', views.AvailableDeviceList.as_view())
]
