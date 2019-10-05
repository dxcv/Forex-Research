import pandas as pd

class Single_Currency(object):
    def __init__(self, data):
        self.data = data

    def Processing(self):
        price = pd.DataFrame(self.data["Time Series FX (Daily)"]).T.rename(columns = {"1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close"})
        return price

class Multi_Currency(object):
    def __init__(self, currencies):
        self.currencies = currencies
        

    def Open(self):
        open_dyct = {}
        for i in self.currencies.keys():
            open_dyct[i] = self.currencies[i]["Open"].values

        df =


if __name__ == "__main__":
    import glob
    import sys
    sys.path.insert(0, "../")
    from UTILS import JSON_IO

    file_name = [f for f in glob.glob("../Data/*.json", recursive = True)]
    currency_dyct = {}

    for f in file_name:
        data = Single_Currency(JSON_IO.load_from_json(f).data).Processing()
        currency_dyct[f] = data

    Multi_Currency(currency_dyct).Open()
