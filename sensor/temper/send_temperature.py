#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import subprocess
import datetime
import json
from influxdb import InfluxDBClient

settingfile = "../../setting.json"

def main():
    s = json.load(open(settingfile, "r"))
    c = InfluxDBClient(host=s["host"], port=s["port"], username=s["username"], password=s["password"], database=s["dbname"])

    result = subprocess.check_output(["temper"])
    result_lst = result.decode("utf-8").replace("\n","").split(",")

    delta = datetime.timedelta(hours=9)
    tz = datetime.timezone(delta)
    sensor_time = datetime.datetime.strptime(result_lst[0], "%Y-%m-%d %H:%M:%S")
    sensor_time = sensor_time.astimezone(tz=tz)

    sensor_temperature = float(result_lst[1])
    data = [
        {
            "measurement": "sensor",
            "time": sensor_time.isoformat(),
            "tags": {
                "locate": s["locate"]
            },
            "fields": {
                "temperature": sensor_temperature
            }
        }
    ]
    c.write_points(data)

if __name__=='__main__':
    main()