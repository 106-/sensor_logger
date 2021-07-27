# sensor_logger
influxdbに電力消費量を送信し続けるスクリプト
influxdb-clientを使うのでPython3.6以上が必須環境

## 初期設定
```
$ git clone https://github.com/106-/sensor_logger.git
$ cd sensor_logger
$ pip install -r requirements.txt
```

## daemon化
influxDBを起動し、その設定を`send_watt.env`に書き込む
`send_watt.service`にスクリプトのあるディレクトリ, `send_watt.env`ファイルのある位置を書き込み`/etc/systemd/system`にコピーする.
