import numpy as np
import pandas as pd

class cal_returns(object):
    def __init__(self, data):
        self.data = data

    @staticmethod
    def ret(price):
        r = price/price.shift(1) - 1
        return r.dropna()

    @classmethod
    def multi_rets(cls, prices):
        return prices.apply(lambda x: cls.ret(x))
