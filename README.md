# sensor_logger
センサーの値を入れるサーバとそれに値を送るスクリプト

※あらかじめ[temper](https://github.com/106-/temper)をいれておく
```
$ git clone https://github.com/106-/sensor_logger.git
$ cd sensor_logger
$ pip install -r requirements.txt
$ cd docker
$ docker-compose up -d
$ ./init.py
```
あとは適当にsend_temperature.pyを実行する