#!/usr/bin/env python
# -*- conding:utf-8 -*-

from influxdb import InfluxDBClient

USERNAME = 'user'
PASSWORD = 'password'

def main():
    client = InfluxDBClient(port='6002')
    client.create_user(USERNAME, PASSWORD)
    client.create_database('sensor')
    client.grant_privilege('all', 'sensor', USERNAME)
    client grant_admin_privileges(USERNAME)
    c.alter_retention_policy("autogen", duration="1w")

if __name__=='__main__':
    main()
