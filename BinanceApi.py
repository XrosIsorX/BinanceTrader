import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode

""" This is a very simple script working on Binance API
- work with USER_DATA endpoint with no third party dependency
- work with testnet
Provide the API key and secret, and it's ready to go
Because USER_DATA endpoints require signature:
- call `send_signed_request` for USER_DATA endpoints
- call `send_public_request` for public endpoints
```python
python spot.py
```
"""

class BinanceApi:
    
    def __init__(self, api_type, is_production=True):
        if is_production:
            key_file = open('KEY.txt', 'r')
        else:
            key_file = open('KEY_TESTNET.txt', 'r')

        self.key, self.secret = key_file.read().split('\n')
        key_file.close()

        if api_type == "spot":
            if is_production:
                self.base_url = 'https://api.binance.com' # production base url
            else:
                self.base_url = 'https://testnet.binance.vision' # testnet base url
        elif api_type == "future":
            if is_production:
                self.base_url = 'https://fapi.binance.com' # future
            else:
                self.base_url = 'https://testnet.binancefuture.com' # future testnet base url

    ''' ======  begin of functions, you don't need to touch ====== '''
    def hashing(self, query_string):
        return hmac.new(self.secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def get_timestamp(self, ):
        return int(time.time() * 1000)

    def dispatch_request(self, http_method):
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json;charset=utf-8',
            'X-MBX-APIKEY': self.key
        })
        return {
            'GET': session.get,
            'DELETE': session.delete,
            'PUT': session.put,
            'POST': session.post,
        }.get(http_method, 'GET')

    # used for sending request requires the signature
    def send_signed_request(self, http_method, url_path, payload={}):
        query_string = urlencode(payload, True)
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())

        url = self.base_url + url_path + '?' + query_string + '&signature=' + self.hashing(query_string)
        print("{} {}".format(http_method, url))
        params = {'url': url, 'params': {}}
        response = self.dispatch_request(http_method)(**params)
        return response.json()

    # used for sending public data request
    def send_public_request(self, url_path, payload={}):
        query_string = urlencode(payload, True)
        url = self.base_url + url_path
        if query_string:
            url = url + '?' + query_string
        # print("{}".format(url))
        response = self.dispatch_request('GET')(url=url)
        return response.json()