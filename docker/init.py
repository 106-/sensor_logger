#!/usr/bin/env python
# -*- conding:utf-8 -*-

import json
from influxdb import InfluxDBClient

settingfile = "../../setting.json"

def main():
    s = json.load(open(settingfile, "r"))
    client = InfluxDBClient(port='6002')
    client.create_user(s["username"], s["password"])
    client.create_database('sensor')
    client.grant_privilege('all', 'sensor', s["username"])
    client.grant_admin_privileges(s["username"])
    client.alter_retention_policy("autogen", duration="1w")

if __name__=='__main__':
    main()
