import os

import pandas as pd
import time
from datetime import datetime

import config

from binance.BinanceApi import BinanceApi
from binance import DataProcessor

api_trade_limit = 1000
binance_api = BinanceApi(api_type="future")

def download_trade_id(url, symbol, last_id, n_trade, delay_time=1):
    os.makedirs(f"{config.trade_logs_id_binance_data_dir}{symbol}/", exist_ok=True)
    i = 1
    while(i * api_trade_limit <= n_trade):
        print(i * api_trade_limit)
        response = binance_api.send_public_request(url, payload={
            'symbol': symbol, "limit": api_trade_limit, "fromId": last_id - (i * api_trade_limit)
        })
        df = DataProcessor.convert_trade_response_to_dataframe(response)
        df = df.sort_index()
        df.to_csv(f"{config.trade_logs_id_binance_data_dir}{symbol}/{last_id - (i * api_trade_limit)}_{last_id - ((i - 1) * api_trade_limit)}.csv")
        i += 1
        time.sleep(delay_time)

def download_with_number_trade(url, symbol, last_id, n_trade, delay_time=1):
    i = 1
    all_df = pd.DataFrame()
    while(i * api_trade_limit <= n_trade):
        print(i * api_trade_limit)
        response = binance_api.send_public_request(url, payload={
            'symbol': symbol, "limit": api_trade_limit, "fromId": last_id - (i * api_trade_limit)
        })
        df = DataProcessor.convert_trade_response_to_dataframe(response)
        all_df = all_df.append(df)
        i += 1
        time.sleep(delay_time)
    all_df = all_df.sort_index()
    return all_df

def download_period(url, symbol, last_id, until_date, delay_time=1):
    os.makedirs(f"{config.trade_logs_binance_data_dir}{symbol}", exist_ok=True)
    all_df = pd.DataFrame()
    i = 1
    current_date = datetime.now()
    while(current_date >= until_date):
        response = binance_api.send_public_request(url, payload={
            'symbol': symbol, "limit": 1000, "fromId": last_id - (i * 1000)
        })
        df = DataProcessor.convert_trade_response_to_dataframe(response)
        current_date = df.index[0]
        last_date = df.index[-1]
        all_df = all_df.append(df) 
        print(current_date)
        if current_date.date() != last_date.date():
            all_df[ all_df.index.date == last_date.date() ].to_csv(f"""{config.trade_logs_binance_data_dir}{symbol}/{last_date.strftime("%Y%m%d")}.csv""")

        all_df = all_df[ all_df.index.date == current_date.date() ]
        i += 1
        time.sleep(delay_time)