import pandas as pd
import time
from datetime import datetime

import config

from api.BinanceApi import BinanceApi
from utils import DataProcessor, DataDownloader

binance_api = BinanceApi(api_type="future")

# symbol = "BNBUSDT"
# symbol = "DOGEUSDT"
symbol = "TLMUSDT"

# response = binance_api.send_public_request('/fapi/v1/trades', payload={'symbol': symbol, "limit": 1000})
# df = DataProcessor.convert_trade_response_to_dataframe(response)
# print(df)

DataDownloader.download_trade_id('/fapi/v1/historicalTrades', symbol=symbol, last_id=34379109, n_trade=10000000, delay_time=3.0)

# df = DataDownloader.download_with_number_trade('/fapi/v1/historicalTrades', symbol=symbol, last_id=174000000, n_trade=100000, delay_time=2)
# df.to_csv(f"{config.trade_logs_binance_data_dir}{symbol}.csv")

# df = DataDownloader.download_with_number_trade('/fapi/v1/historicalTrades', symbol=symbol, last_id=174000000, n_trade=100000, delay_time=2)
# df.to_csv(f"{config.trade_logs_binance_data_dir}{symbol}.csv")
# DataDownloader.download_period('/api/v3/historicalTrades', symbol=symbol, id=224114000)
# DataDownloader.download_period('/fapi/v1/historicalTrades', symbol=symbol, last_id=174000000, until_date=datetime(2021, 4, 1), delay_time=1.2)