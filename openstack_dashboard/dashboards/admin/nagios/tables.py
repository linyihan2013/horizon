from django.utils.translation import ugettext_lazy as _

from horizon import tables


class NagiosHostsTable(tables.DataTable):
    hostname = tables.Column("hostname",
                                    verbose_name=_("Hostname"))

    status = tables.Column("status",
                                    verbose_name=_("Status"))

    last_check = tables.Column("last_check",
                               verbose_name=_("Last Check"))

    duration = tables.Column("duration",
                          verbose_name=_("Duration"))

    status_info = tables.Column('status_info',
                                verbose_name=_("Status Information"))

    class Meta(object):
        name = "hosts"
        verbose_name = _("Hosts")
