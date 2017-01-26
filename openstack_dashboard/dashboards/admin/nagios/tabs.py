from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard.dashboards.admin.nagios import tables

import api

class NagiosHostTab(tabs.TableTab):
    table_classes = (tables.NagiosHostsTable,)
    name = _("Hosts")
    slug = "hosts"
    template_name = "horizon/common/_detail_table.html"

    def get_hosts_data(self):
        hosts = []

        try:
            hosts = api.get_nagios_hosts()
            hosts.sort(key=lambda x : x["hostname"])
        except Exception:
            exceptions.handle(self.request, _("Unable to get nagios host data"))

        return hosts


class NagiosServiceTab(tabs.TableTab):
    table_classes = (tables.NagiosServicesTable,)
    name = _("Services")
    slug = "services"
    template_name = "horizon/common/_detail_table.html"

    def get_services_data(self):
        services = []
        return services


class NagiosTabs(tabs.TabGroup):
    slug = "nagios_tabs"
    tabs = (NagiosHostTab, NagiosServiceTab)
    sticky = True
