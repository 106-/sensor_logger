import math
import os
import influxdb_client
from gpiozero import MCP3008
from influxdb_client.client.write_api import SYNCHRONOUS

resist = 460 # CTセンサに付けている負荷抵抗
rate = 3000 # CTセンサの変換比
max_voltage = 5.00 # 回路の最大電圧
num_sampling = 100 # サンプリング数
effective_voltage = 100 # 交流電源の実効電圧

# `pot.value`の値は0から1の範囲
pot = MCP3008(channel=0, max_voltage=max_voltage)

# 2.5Vに分圧しているので`pot.value`の平均は0.5になるはずだが, 実際には少しずれている.
# それがこの変数である.
bias = 0.492533

# influxdbの設定を読み込んでいく
bucket = os.environ["INFLUXDB_BUCKET"]
org = os.environ["INFLUXDB_ORGANIZATION"]
token = os.environ["INFLUXDB_TOKEN"]
url = os.environ["INFLUXDB_URL"]

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# クランプ内に流れる電力を返す(交流なので負の値もありえる)
def current():
    # `pot.value`の取る値[0, +1]を[-0.5, +0.5]の範囲にしたあと,
    # 最大電圧(5.0V)をかけて電圧に変換する.
    voltage = (pot.value - bias) * max_voltage
    # オームの法則から, センサーに流れている電流を計算する.
    ampere = voltage / resist
    # CTセンサに流れている電流から, 観測対象の回路の電流を計算する.
    ampere_observe = ampere * rate
    # 電流*実効電圧で電力量を計算する.
    watt = ampere_observe * effective_voltage
    return watt

while True:
    sum_ = 0
    for i in range(num_sampling):
        sum_ += current() ** 2
    watt = math.sqrt(sum_/num_sampling)
    p = influxdb_client.Point("watt").tag("location", "somewhere").field("watt", watt)
    write_api.write(bucket=bucket, org=org, record=p)
