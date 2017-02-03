# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.conf.urls import url

from openstack_dashboard.dashboards.admin.nagios import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<host>[^/]+)/host$', views.PNP4NagiosHostView.as_view(), name='host'),
    url(r'^(?P<host_service>.+)/service$', views.PNP4NagiosServiceView.as_view(), name='service'),
    url(r'^(?P<host>[^/]+)/detail$', views.HostDetailView.as_view(), name='detail'),
]
