import numpy as np
import pandas as pd

class Single_Currency(object):
    def __init__(self, data):
        self.data = data

    def Processing(self):
        price = pd.DataFrame(self.data["Time Series FX (Daily)"]).T.rename(columns = {"1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close"})
        return price

class Multi_Currency(object):
    def __init__(self, data_lyst):
        self.data_lyst = data_lyst
        self.price = None

    def Open(self):
        data = sorted(self.data_lyst.items(), key = lambda x: len(x))
        df = data[-1][1]["Open"].to_frame(name = data[-1][0]).reset_index()
        for x in data[:-1]:
            df = pd.merge(df, x[1]["Open"].to_frame(name = x[0]).reset_index(), how = "left", on = "index")
        self.price = df.interpolate(method='linear', limit_direction='forward', axis=0).set_index("index")

    def High(self):
        data = sorted(self.data_lyst.items(), key = lambda x: len(x))
        df = data[-1][1]["High"].to_frame(name = data[-1][0]).reset_index()
        for x in data[:-1]:
            df = pd.merge(df, x[1]["High"].to_frame(name = x[0]).reset_index(), how = "left", on = "index")
        self.price = df.interpolate(method='linear', limit_direction='forward', axis=0).set_index("index")

    def Low(self):
        data = sorted(self.data_lyst.items(), key = lambda x: len(x))
        df = data[-1][1]["Low"].to_frame(name = data[-1][0]).reset_index()
        for x in data[:-1]:
            df = pd.merge(df, x[1]["Low"].to_frame(name = x[0]).reset_index(), how = "left", on = "index")
        self.price = df.interpolate(method='linear', limit_direction='forward', axis=0).set_index("index")

    def Close(self):
        data = sorted(self.data_lyst.items(), key = lambda x: len(x))
        df = data[-1][1]["Close"].to_frame(name = data[-1][0]).reset_index()
        for x in data[:-1]:
            df = pd.merge(df, x[1]["Close"].to_frame(name = x[0]).reset_index(), how = "left", on = "index")
        self.price = df.interpolate(method='linear', limit_direction='forward', axis=0).set_index("index")

if __name__ == "__main__":
    import glob
    import sys
    sys.path.insert(0, "../")
    from UTILS import JSON_IO
    """ Loading File Name """
    file_name = [f for f in glob.glob("../Data/*.json", recursive = True)]
    """ Reading Data """
    currency_dyct = {}
    for f in file_name:
        data = Single_Currency(JSON_IO.load_from_json(f).data).Processing()
        key = f.split("/")[-1].split(".")[0]
        currency_dyct[key] = data.astype(float)

    Forex_rate = Multi_Currency(currency_dyct)
    Forex_rate.Open()
    Price = Forex_rate.price

    Price.loc["2019-10-05":"2013-06-01",:].to_csv("../Data/Forex_130603_191005.csv")
