from abc import ABC, abstractmethod
import requests
import sys

class Forex_D(ABC):
    def __init__(self):
        self.main_URL   = "https://www.alphavantage.co/query?"
        self.function   = "FX_DAILY"
        self.apikey     = "{HT1VSGJMRN19BN4W}"

    @abstractmethod
    def Execute(self):
        pass

class Forex_W(ABC):
    def __init__(self):
        self.main_URL   = "https://www.alphavantage.co/query?"
        self.function   = "FX_WEEKLY"
        self.apikey     = "{HT1VSGJMRN19BN4W}"

    @abstractmethod
    def Execute(self):
        pass

class Forex_M(ABC):
    def __init__(self   ):
        self.main_URL   = "https://www.alphavantage.co/query?"
        self.function   = "FX_MONTHLY"
        self.apikey     = "{HT1VSGJMRN19BN4W}"

    @abstractmethod
    def Execute(self):
        pass

class GBP_USD(Forex_D):
    def __init__(self):
        super().__init__()
        self.URL = self.main_URL + "function=" + self.function + "&"

    def Execute(self):
        self.URL = self.URL + self.URL + "from_symbol=GBP&to_symbol=USD" + "&" + \
                   "outputsize=full" + "&apikey=" + self.apikey

        res  = requests.get(self.URL)
        data = res.json()
        return data

class GBP_CAD(Forex_D):
    def __init__(self):
        super().__init__()
        self.URL = self.main_URL + "function=" + self.function + "&"

    def Execute(self):
        self.URL = self.URL + self.URL + "from_symbol=GBP&to_symbol=CAD" + "&" + \
                   "outputsize=full" + "&apikey=" + self.apikey

        res  = requests.get(self.URL)
        data = res.json()
        return data

class GBP_AUD(Forex_D):
    def __init__(self):
        super().__init__()
        self.URL = self.main_URL + "function=" + self.function + "&"

    def Execute(self):
        self.URL = self.URL + self.URL + "from_symbol=GBP&to_symbol=AUD" + "&" + \
                   "outputsize=full" + "&apikey=" + self.apikey

        res  = requests.get(self.URL)
        data = res.json()
        return data

class GBP_EUR(Forex_D):
    def __init__(self):
        super().__init__()
        self.URL = self.main_URL + "function=" + self.function + "&"

    def Execute(self):
        self.URL = self.URL + self.URL + "from_symbol=GBP&to_symbol=EUR" + "&" + \
                   "outputsize=full" + "&apikey=" + self.apikey

        res  = requests.get(self.URL)
        data = res.json()
        return data

class GBP_JPY(Forex_D):
    def __init__(self):
        super().__init__()
        self.URL = self.main_URL + "function=" + self.function + "&"

    def Execute(self):
        self.URL = self.URL + self.URL + "from_symbol=GBP&to_symbol=JPY" + "&" + \
                   "outputsize=full" + "&apikey=" + self.apikey

        res  = requests.get(self.URL)
        data = res.json()
        return data

class GBP_CNY(Forex_D):
    def __init__(self):
        super().__init__()
        self.URL = self.main_URL + "function=" + self.function + "&"

    def Execute(self):
        self.URL = self.URL + self.URL + "from_symbol=GBP&to_symbol=CNY" + "&" + \
                   "outputsize=full" + "&apikey=" + self.apikey

        res  = requests.get(self.URL)
        data = res.json()
        return data

if __name__ == "__main__":
    sys.path.insert(0, "../")
    saving_path = "../Data/"
    from UTILS import JSON_IO
    forex_loader = [GBP_USD(), GBP_CAD(), GBP_AUD(), GBP_EUR(), GBP_JPY(), GBP_CNY()]
    for loader in forex_loader:
        data = loader.Execute()
        file_name = loader.__class__.__name__
        JSON_IO.save_to_json(data, saving_path + file_name)
