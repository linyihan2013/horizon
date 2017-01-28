import urllib2
import json
import datetime

# settings
username = "nagiosadmin"
password = "niot_dbc_001*"
nagios_url = "http://127.0.0.1/nagios"

# install auth opener
password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
password_mgr.add_password(None, nagios_url, username, password)

handler = urllib2.HTTPBasicAuthHandler(password_mgr)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)


def get_nagios_host_list():
    path = "/cgi-bin/statusjson.cgi?query=hostlist"
    request = urllib2.Request(nagios_url + path)

    # get HTTP response
    try:
        response = urllib2.urlopen(request)
    except urllib2.URLError, e:
        print e.reason

    content = response.read().decode()
    values = json.loads(content)

    # get host list
    host_list = []
    if "data" in values:
        if "hostlist" in values["data"]:
            for host in values["data"]["hostlist"]:
                host_list.append(host)
    host_list.sort()

    return host_list


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
    
    host_list = get_nagios_host_list()
    hosts = []

    for host in host_list:
        request = urllib2.Request(nagios_url + (path % host))

        # get HTTP response
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError, e:
            print e.reason

        content = response.read().decode()
        values = json.loads(content)
        hosts.append(get_nagios_host_data(values))

    return hosts


def get_nagios_service_list():
    path = "/cgi-bin/statusjson.cgi?query=servicelist"
    request = urllib2.Request(nagios_url + path)

    # get HTTP response
    try:
        response = urllib2.urlopen(request)
    except urllib2.URLError, e:
        print e.reason

    content = response.read().decode()
    values = json.loads(content)

    # get service list
    service_list = []
    if "data" in values:
        if "servicelist" in values["data"]:
            for host in values["data"]["servicelist"]:
                for service in values["data"]["servicelist"][host]:
                    service_list.append((host, service))
    service_list.sort()

    return service_list


def get_nagios_service_data(values):
    data = {}

    # parse service data
    if "result" in values and "data" in values:
        if "query_time" in values["result"] and "service" in values["data"] and "last_state_change" in values["data"]["service"]:
            query_time = values["result"]["query_time"]
            last_state_change = values["data"]["service"]["last_state_change"]
            duration = (query_time - last_state_change) / 1000
            
            seconds = duration % 60
            duration /= 60

            minutes = duration % 60
            duration /= 60

            hours = duration % 24
            days = duration / 24

            data["duration"] = "%sd %sh %sm %ss" % (days, hours, minutes, seconds)

    if "data" in values:
        if "service" in values["data"]:
            values = values["data"]["service"]

    if "host_name" in values:
        data["hostname"] = values["host_name"]

    if "description" in values:
        data["service"] = values["description"]

    if "status" in values:
        if values["status"] == 1:
            data["status"] = "PENDING"
        elif values["status"] == 2:
            data["status"] = "OK"
        elif values["status"] == 4:
            data["status"] = "WARNING"
        elif values["status"] == 8:
            data["status"] = "UNKNOWN"
        elif values["status"] == 16:
            values["status"] = "CRITICAL"

    if "last_check" in values:
        last_check = datetime.datetime.fromtimestamp(values["last_check"] / 1000)
        data["last_check"] = last_check.strftime("%m-%d-%Y %H:%M:%S")

    if "plugin_output" in values:
        data["status_info"] = values["plugin_output"]

    if "current_attempt" in values and "max_attemps" in values:
        data["attempt"] = str(values["current_attempt"]) + "/" + str(values["max_attemps"])

    return data


def get_nagios_services():
    path = "/cgi-bin/statusjson.cgi?query=service&hostname=%s&servicedescription=%s"
    
    service_list = get_nagios_service_list()
    services = []

    for host, service in service_list:
        request = urllib2.Request(nagios_url + (path % (host, service.replace(' ', '+'))))

        # get HTTP response
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError, e:
            print e.reason

        content = response.read().decode()
        values = json.loads(content)
        services.append(get_nagios_service_data(values))

    return services


