import requests as req

headers = {
    ":authority": "bin.bnbstatic.com",
    ":method": "GET",
    ":path": "/static/images/coin/dodo.svg",
    ":scheme": "https",
    "referer": "https://launchpad.binance.com/",
    
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
}

url = "https://bin.bnbstatic.com/static/images/coin/dodo.svg"
response = req.get(url)
print(response.text)