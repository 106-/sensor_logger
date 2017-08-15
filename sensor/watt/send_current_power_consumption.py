#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import json
import serial
import threading
import time
from influxdb import InfluxDBClient

settingfile = "../../setting.json"
serial_settingfile = "../../serial_setting.json"

class watt_poster(threading.Thread):
    def __init__(self, dbsetting, serialsetting):
        self.dbsetting = dbsetting
        self.serialsetting = serialsetting

    def run(self):
        s = json.load(open(self.dbsetting, "r"))
        c = InfluxDBClient(host=s["host"], port=s["port"], username=s["username"], password=s["password"], database=s["dbname"])
        ss = json.load(open(self.serialsetting, "r"))
        ser = serial.Serial(ss["devfile"], baudrate=ss["baudrate"], timeout=ss["timeout"])

        while True:
            ser.write("\n".encode("ascii"))
            while ser.in_waiting < ss["min_response_size"]:
                time.sleep(0.1)
            val = float(ser.read(ser.in_waiting))
            if val > ss["threshold"]:
                self._senddata(c, val, s["locate"])
            else:
                self._senddata(c, 0.0, s["locate"])
            time.sleep(ss["interval"])        

    def _senddata(self, c, val, locate):
        delta = datetime.timedelta(hours=9)
        tz = datetime.timezone(delta)
        now = datetime.datetime.now()
        now = now.astimezone(tz=tz)

        data = [
            {
                "measurement": "sensor",
                "time": now.isoformat(),
                "tags": {
                    "locate": locate
                },
                "fields": {
                    "power_consumption": val
                }
            }
        ]
        c.write_points(data)

def main():
    wp = watt_poster(settingfile, serial_settingfile)
    wp.run()

if __name__=='__main__':
    main()
