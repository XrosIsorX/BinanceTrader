import pandas as pd

from utils import Utils

def read_trade(filepath):
    df = pd.read_csv(filepath)
    df = df.set_index("time")
    df.index = pd.to_datetime(df.index)
    return df

def read_trade_from_directory(dirpath):
    df = Utils.read_csv_from_directory(dirpath)
    df = df.set_index("time")
    df.index = pd.to_datetime(df.index)
    return df