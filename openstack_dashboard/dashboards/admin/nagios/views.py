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

from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView

from horizon import exceptions
from horizon import tabs
from horizon import tables

from openstack_dashboard.dashboards.admin.nagios \
        import tabs as nagios_tabs
from openstack_dashboard.dashboards.admin.nagios \
        import tables as nagios_tables
from openstack_dashboard.dashboards.admin.nagios \
        import api as nagios_api


class IndexView(tabs.TabbedTableView):
    tab_group_class = nagios_tabs.NagiosTabs
    template_name = 'admin/nagios/index.html'
    page_title = _("Nagios")

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context


class PNP4NagiosHostView(RedirectView):
    url = "/pnp4nagios/graph"

    def get_redirect_url(self, *args, **kwargs):
        self.url = self.url + "?host=%s" % kwargs["host"]
        
        return super(PNP4NagiosHostView, self).get_redirect_url(*args, **kwargs)


class PNP4NagiosServiceView(RedirectView):
    url = "/pnp4nagios/graph"

    def get_redirect_url(self, *args, **kwargs):
        host, service = kwargs["host_service"].split("+")
        self.url = self.url + "?host=%s" % host + "&srv=%s" % service
        
        return super(PNP4NagiosServiceView, self).get_redirect_url(*args, **kwargs)


class HostDetailView(tables.DataTableView):
    table_class = nagios_tables.NagiosServicesTable
    template_name = 'admin/nagios/detail.html'
    page_title = _("Services")

    def get_data(self):
        services = []

        try:
            host_name = self.kwargs['host']
            services = nagios_api.get_nagios_services_by_host(host_name)
        except Exception:
            exceptions.handle(self.request, _("Unable to get nagios service data"))

        return services

    def get_context_data(self, **kwargs):
        context = super(HostDetailView, self).get_context_data(**kwargs)
        host_name = self.kwargs['host']
        breadcrumb = [(host_name, None)]
        context['custom_breadcrumb'] = breadcrumb
        return context
