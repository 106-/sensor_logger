#!/usr/bin/env python
# -*- coding:utf-8 -*-

import subprocess
import datetime
from influxdb import InfluxDBClient

USERNAME = 'user'
PASSWORD = 'password'
DBNAME = 'sensor'
HOST = '192.168.0.11'
PORT = 6002
LOCATE = "shizuoka"

def main():
    c = InfluxDBClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD, database=DBNAME)

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
                "locate": LOCATE
            },
            "fields": {
                "temperature": sensor_temperature
            }
        }
    ]
    c.write_points(data)

if __name__=='__main__':
    main()
