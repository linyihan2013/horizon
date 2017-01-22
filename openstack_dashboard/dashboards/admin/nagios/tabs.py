from django.utils.translation import ugettext_lazy as _

from horizon import tabs

from openstack_dashboard.dashboards.admin.nagios import tables


class NagiosHostTab(tabs.TableTab):
    table_classes = (tables.NagiosHostsTable,)
    name = _("Hosts")
    slug = "hosts"
    template_name = "horizon/common/_detail_table.html"

    def get_hosts_data(self):
        hosts = []
        return hosts


class NagiosTabs(tabs.TabGroup):
    slug = "nagios_tabs"
    tabs = (NagiosHostTab,)
    sticky = True
