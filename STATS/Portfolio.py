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
        results = np.zeros((3, self.__n_portfolio__))
        weights_record = []
        for i in range(self.__n_portfolio__):
            weights  = np.random.random(self.n_asset)
            weights /= np.sum(weights)
            weights_record.append(weights)
            rets, std, risk = self.Portfolio(weights, self.rets.values, self.mean.values, self.cov_matrix, self.__time_length__)
            results[0, i] = std
            results[1, i] = rets
            results[2, i] = risk

        return results, weights_record

    @staticmethod
    def Portfolio(weights, all_rets, mean_rets, cov_mat, time_length):
        """ All variable here is in numpy format """
        rets = np.sum(mean_rets * weights) * time_length
        std  = np.sqrt(np.dot(weights.T, np.dot(cov_mat, weights))) * np.sqrt(time_length)
        weighted_rets = np.dot(all_rets, weights)
        risk = VaR(weighted_rets).VaR_t(0.01, time_length, False)

        return rets, std, risk
