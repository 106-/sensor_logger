import math
from gpiozero import MCP3008

resist = 460 # CTセンサに付けている負荷抵抗
rate = 3000 # CTセンサの変換比
max_voltage = 5.00 # 回路の最大電圧
num_sampling = 100 # サンプリング数
effective_voltage = 100 # 交流電源の実効電圧

# `pot.value`の値は0から1の範囲
pot = MCP3008(channel=0, max_voltage=max_voltage)

# 2.5Vに分圧しているので`pot.value`の平均は0.5になるはずだが, 実際には少しずれている.
# その差がこの変数である.
bias = 0.49690356619443293

# クランプ内に流れる電力を返す(交流なので負の値もありえる)
def current():
    return (pot.value - bias) * max_voltage / resist * rate * effective_voltage

while True:
    sum_ = 0
    for i in range(num_sampling):
        sum_ += current() ** 2
    print("%g"%(math.sqrt(sum_/num_sampling)))
