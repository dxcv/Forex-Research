from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
import scipy.optimize as sco

from STATS.Risk import VaR, CVaR

class Parameters(ABC):
    def __init__(self, n_asset, time_length, risk_free_rate):
        self.n_asset        = n_asset
        self.time_length    = time_length
        self.risk_free_rate = risk_free_rate
        super().__init__()

    @abstractmethod
    def Execute_Optimization(self):
        pass

    def help(self):
        return None

class Mean_Variance_Optimizer(Parameters):
    def __init__(self, n_asset, time_length, risk_free_rate, mean_rets, cov_matrix):
        super()._init__(n_asset, time_length, risk_free_rate)
        self.mean_rets      = mean_rets
        self.cov_matrix     = cov_matrix

    def Execute_Optimization(self):

        return None

    @staticmethod
    def volatility(weights, time_length, cov_matrix):
        var = np.sqrt(np.dot(weights.T, np.dot(cov_mat, weights))) * np.sqrt(time_lengt)

        return var

    @classmethod
    def Minimize_volatility(n_asset, mean_returns, cov_matrix):
        args    = (mean_returns, cov_matrix)
        cons    = ({"type": "eq", "fun": lambda x: np.sum(x) - 1})
        bounds  = tuple((0.0, 1.0) for asset in range(n_asset))
        result  = sco.minimize(volatility, num_assets*[1./num_assets,], args = args, method = "SLSQP", bounds = bounds, constraints = cons)

        return result

    @staticmethod
    def neg_sharpe_ratio(weights, time_length, mean_rets, cov_matrix, risk_free_rate):
        p_ret = np.sum(mean_rets * weights) * time_length
        p_var = np.sqrt(np.dot(weights.T, np.dot(cov_mat, weights))) * np.sqrt(time_lengt)

        return -(p_ret - risk_free_rate)/p_var

    @classmethod
    def Maximize_sharpe_ratio(cls, num_assets, mean_returns, cov_matrix, risk_free_rate):
        args    = (mean_returns, cov_matrix, risk_free_rate)
        cons    = ({"type": "eq", "fun": lambda x: np.sum(x)-1})
        bounds  = tuple((0.0, 1.0) for asset in range(num_assets))
        result  = sco.minimize(neg_sharpe_ratio, num_assets*[1./num_assets,], args = args, method = "SLSQP", bounds = bounds, constraints = cons)

        return result

class Value_at_Risk_Optimizer(Parameters):
    def __init__(self, n_asset, time_length, all_returns):
        super().__init__(n_asset, time_length, None)
        self.all_returns = all_returns
        self.__alpha__   = 0.01

    def Execute_Optimization(self):
        res = self.Minimize_VaR(self.n_asset, self.__alpha__, self.time_length, self.all_returns)
        return res

    @staticmethod
    def Cal_VaR(weights, alpha, time_length, all_rets):
        res = VaR(np.dot(all_rets, weights)).VaR_t(alpha, time_length, False)

        return res

    @classmethod
    def Minimize_VaR(cls, n_asset, alpha, time_length, all_rets):
        args    = (alpha, time_length, all_rets)
        cons    = ({"type": "eq", "fun": lambda x: np.sum(x) - 1})
        bounds  = tuple((0.0, 1.0) for asset in range(n_asset))
        result  = sco.minimize(cls.Cal_VaR, n_asset * [1./n_asset,], args = args, method = "SLSQP", bounds = bounds, constraints = cons)

        return result
