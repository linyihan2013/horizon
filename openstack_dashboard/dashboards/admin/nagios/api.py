import urllib2
import json
import datetime

# settings
username = "nagiosadmin"
password = "niot_dbc_001*"
url = "http://127.0.0.1/nagios"

# install auth opener
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, url, username, password)

handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)


def get_nagios_hostlist():
    path = "/cgi-bin/statusjson.cgi?query=hostlist"
    request = urllib2.Request(url + path)

    # get HTTP response
    try:
        response = urllib2.urlopen(request)
    except urllib2.URLError, e:
        print e.reason

    content = response.read().decode()
    values = json.loads(content)

    # get host list
    hostlist = []
    if "data" in values:
        if "hostlist" in values["data"]:
            for host in values["data"]["hostlist"]:
                hostlist.append(host)
    hostlist.sort()

    return hostlist


def get_nagios_host_data(values):
    data = {}

    # parse host data
    if "result" in values and "data" in values:
        if "query_time" in values["result"] and "host" in values["data"] and "last_state_change" in values["data"]["host"]:
            query_time = values["result"]["query_time"]
            last_state_change = values["data"]["host"]["last_state_change"]
            duration = (query_time - last_state_change) / 1000
            
            seconds = duration % 60
            duration /= 60

            minutes = duration % 60
            duration /= 60

            hours = duration % 24
            days = duration / 24

            data["duration"] = "%sd %sh %sm %ss" % (days, hours, minutes, seconds)

    if "data" in values:
        if "host" in values["data"]:
            values = values["data"]["host"]

    if "name" in values:
        data["hostname"] = values["name"]

    if "status" in values:
        if values["status"] == 1:
            data["status"] = "PENDING"
        elif values["status"] == 2:
            data["status"] = "UP"
        elif values["status"] == 4:
            data["status"] = "DOWN"
        elif values["status"] == 8:
            data["status"] = "UNREACHABLE"

    if "last_check" in values:
        last_check = datetime.datetime.fromtimestamp(values["last_check"] / 1000)
        data["last_check"] = last_check.strftime("%m-%d-%Y %H:%M:%S")

    if "plugin_output" in values:
        data["status_info"] = values["plugin_output"]

    return data


def get_nagios_hosts():
    path = "/cgi-bin/statusjson.cgi?query=host&hostname=%s"
    
    hostlist = get_nagios_hostlist()
    hosts = []

    for host in hostlist:
        request = urllib2.Request(url + (path % host))

        # get HTTP response
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError, e:
            print e.reason

        content = response.read().decode()
        values = json.loads(content)
        hosts.append(get_nagios_host_data(values))

    return hosts
