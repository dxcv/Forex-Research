import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

def Calculate_Return(data):
    rets = (data/data.shift(1)) - 1
    return rets

class VaR(object):
    def __init__(self, rets):
        """
            Variance-Covariance calculation of daily VaR using confidence level c,
            with mean of returns mu and standard deviation of returns sigma,
            on a portfolio of value P.
            P is price of
            c is confidence level in percentage
            mu is mean value
            sigma is variance
        """
        self.rets         = rets
        self.mu           = rets.mean()
        self.sigma        = rets.std()
        self.__seed__     = 42
        self.__n_sample__ = 1000000

    def Calculate_VaR(self, P, c):
        VAR_param = self.VaR_Param(P, c, self.mu, self.sigma)
        VAR_hist  = self.VaR_Hist(P, c, self.rets)
        VAR_simu  = self.VaR_Simu(P, c, self.mu, self.sigma, self.__seed__, self.__n_sample__)

        VAR_table = pd.DataFrame({"Paremetric VAR": VAR_param,
                                  "Historical VAR": VAR_hist,
                                  "Simulated VAR": VAR_simu}, index = {"Confidence {0:.1f}%".format(c)})

        return VAR_table

    @classmethod
    def VaR_Param(cls, P, c, mu, sigma):
        return P * sp.stats.norm.ppf(1 - c/100, mu, sigma)

    @classmethod
    def VaR_Hist(cls, P, c, rets):
        return P * np.percentile(rets, 100 - c)

    @classmethod
    def VaR_Simu(cls, P, c, mu, sigma, seed, n_sample):
        np.random.seed(seed)
        n_sims   = n_sample
        rets_sim = np.random.normal(mu, sigma, n_sims)
        return P * np.percentile(rets_sim, 100 - c)

class CVaR(VaR):
    def __init__(self, rets):
        super().__init__(rets)
        self.VaR = self.Calculate_VaR(1000, 99)

        print(self.CVaR_Param(0.01, self.mu, self.sigma))

    @classmethod
    def CVaR_Param(cls, alpha, mu, sigma):
        cvar = sp.stats.norm.pdf(sp.stats.norm.ppf(alpha)) * 1/alpha * sigma - mu
        return cvar


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "../")
    df      = pd.read_csv("../Data/Forex_130603_191005.csv")
    df      = df.reindex(index = df.index[::-1])
    df      = df.rename(columns = {"index": "Time"}).set_index("Time")
    df_rets = df.apply(lambda x: Calculate_Return(x)).dropna()

    # print(VaR(df_rets[["GBP_USD"]]).Calculate_VaR(1000, 99))
    print(CVaR(df_rets[["GBP_USD"]]))
