import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode

import collections

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from utils import DataProcessor
from api.BinanceApi import BinanceApi

max_lenth = 200
x_deque = collections.deque(maxlen=max_lenth)
sum_volume_deque = collections.deque(maxlen=max_lenth)
zero_deque = collections.deque(maxlen=max_lenth)
last_sum_volume_deque = collections.deque(maxlen=20)
diff_price_deque = collections.deque(maxlen=max_lenth)

last_sum_volume = 0
last_price = 0
symbol = "DOGEUSDT"

binance_api = BinanceApi(api_type="future")
def calculate(i):
    global last_sum_volume, last_price
    # response = binance_api.send_public_request('/api/v3/trades', payload={'symbol': symbol, "limit": 1000})
    response = binance_api.send_public_request('/fapi/v1/trades', payload={'symbol': symbol, "limit": 1000})

    df = DataProcessor.convert_trade_response_to_dataframe(response)
    # df["volume_buy"] = df[ df["isBuyerMaker"] == False ]["qty"].sum()
    # df["volume_sell"] = df[ df["isBuyerMaker"] == True ]["qty"].sum()
    # df["count_buy"] = df[ df["isBuyerMaker"] == False ].shape[0]
    # df["count_sell"] = df[ df["isBuyerMaker"] == True ].shape[0]
    # df["isBuyerMaker"][ df["isBuyerMaker"] == False ] = "buy"
    # df["isBuyerMaker"][ df["isBuyerMaker"] == True ] = "sell"
    # df.to_csv("current_trade_logs.csv")

    sum_volume = df[ df["isBuyerMaker"] == False ]["qty"].sum() - df[ df["isBuyerMaker"] == True ]["qty"].sum()
    sum_volume_deque.append(sum_volume)
    diff_price = df["price"].iloc[-1] - last_price
    last_price = df["price"].iloc[-1]
    diff_price_deque.append(diff_price)
    zero_deque.append(0)
    if i < max_lenth:
        x_deque.append(i)

    diff_volume = sum_volume - last_sum_volume
    last_sum_volume = sum_volume
    last_sum_volume_deque.append(str(int(diff_volume)))
    ax.set_title(int(sum_volume), loc="left", fontsize=20)
    ax.set_title(int(diff_volume), loc="right", fontsize=20)
    ax.xaxis.set_label_position('top')
    ax.xaxis.tick_top()
    ax.set_xlabel("    ".join(last_sum_volume_deque))
    line1.set_data(x_deque, sum_volume_deque)
    line2.set_data(x_deque, diff_price_deque)
    return [line1, line2]
    # plt.plot(sum_volume_deque)
    # plt.plot(zero_deque)

figure, ax = plt.subplots(figsize=(4,3))
ax2 = ax.twinx()
line1, = ax.plot(x_deque, sum_volume_deque, color="red")
line2, = ax2.plot(x_deque, diff_price_deque, color="blue")
lines = [line1, line2]
ax.axis([0, max_lenth, -3000000, 3000000])
ax2.axis([0, max_lenth, -0.005, 0.005])

ani = FuncAnimation(figure, calculate, interval=200)
plt.show()