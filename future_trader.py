import hmac
import time
import hashlib
import requests
import json
from urllib.parse import urlencode

import pandas as pd

import DataProcessor
from BinanceApi import BinanceApi

binance_api = BinanceApi(api_type="future", is_production=False)

response = binance_api.send_signed_request('GET', '/fapi/v2/account')

response = binance_api.send_public_request("/fapi/v1/trades", payload={'symbol': "DOGEUSDT", "limit": 1000})
print(response)

#df = DataProcessor.convert_trade_response_to_dataframe(response)
#print(df)

# ### USER_DATA endpoints, call send_signed_request #####
# # place an order
# # if you see order response, then the parameters setting is correct
# # if it has response from server saying some parameter error, please adjust the parameters according the market.
# params = {
#     "symbol": "BNBUSDT",
#     "side": "BUY",
#     "type": "LIMIT",
#     "timeInForce": "GTC",
#     "quantity": 1,
#     "price": "15"
# }
# response = binance_api.send_signed_request('POST', '/fapi/v1/order', params)
# print(response)

# # place batch orders
# # if you see order response, then the parameters setting is correct
# # if it has response from server saying some parameter error, please adjust the parameters according the market.
# params = {
#     "batchOrders": [
#         {
#             "symbol":"BNBUSDT",
#             "side": "BUY",
#             "type": "STOP",
#             "quantity": "1",
#             "price": "9000",
#             "timeInForce": "GTC",
#             "stopPrice": "9100"
#         },
#         {
#             "symbol":"BNBUSDT",
#             "side": "BUY",
#             "type": "LIMIT",
#             "quantity": "1",
#             "price": "15",
#             "timeInForce": "GTC"
#         },
#     ]
# }
# response = binance_api.send_signed_request('POST', '/fapi/v1/batchOrders', params)
# print(response)