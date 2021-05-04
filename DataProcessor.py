from datetime import datetime

import pandas as pd

def convert_trade_response_to_dataframe(response):
    df = pd.DataFrame(response)
    df["price"] = df["price"].astype(float)
    df["qty"] = df["qty"].astype(float)
    df["quoteQty"] = df["quoteQty"].astype(float)
    df["time"] = df["time"].apply(lambda v: datetime.fromtimestamp(v / 1000))
    df = df.set_index("time")
    return df
