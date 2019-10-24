import numpy as np
import pandas as pd

from STATS.Risk import VaR, CVaR

class Generating_Portfolio(object):
    def __init__(self, rets, n_portfolio, time_length):
        self.rets        = rets
        self.n_asset     = rets.shape[1]
        self.mean        = self.rets.mean()
        self.cov_matrix  = self.rets.cov()

        self.__n_portfolio__ = 25000
        self.__time_length__ = 252        # Trading Days in ONE YEAR

    def Generator(self):
        return self.Portfolio(np.random.random(self.n_asset), self.rets.values, self.mean.values, self.cov_matrix, self.__time_length__)

    @staticmethod
    def Portfolio(weights, all_rets, mean_rets, cov_mat, time_length):
        """ All variable here is in numpy format """
        rets = np.sum(mean_rets * weights) * time_length
        std  = np.sqrt(np.dot(weights.T, np.dot(cov_mat, weights))) * np.sqrt(time_length)
        weighted_rets = np.dot(all_rets, weights)
        risk = VaR(weighted_rets).VaR_norm(0.01, time_length)

        return rets, std, risk
