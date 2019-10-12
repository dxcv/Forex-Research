import numpy as np
import pandas as pd
from scipy.stats import norm, t
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
        self.__seed__     = 42
        self.__n_sample__ = 1000000
        self.rets         = rets
        self.nu           = None
        self.mu           = None
        self.sigma        = None

    def VaR_norm(self, alpha, h):
        self.mu, self.sigma = norm.fit(self.rets)
        mu_h, sigma_h = self.mu * (h/len(self.rets)), self.sigma * ((h/len(self.rets)) ** 0.5)
        VAR_param = self.VaR_Param(alpha, mu_h, sigma_h)
        VAR_hist  = self.VaR_Hist(alpha, h, self.rets)
        VAR_simu  = self.VaR_Simu(alpha, h, mu_h, sigma_h, self.__seed__, self.__n_sample__)

        VAR_table = pd.DataFrame({"Paremetric VAR": VAR_param,
                                  "Historical VAR": VAR_hist,
                                  "Simulated VAR": VAR_simu}, index = {"Confidence {0:.1f}%".format(100-alpha*100)})

        return VAR_table

    def VaR_t(self, alpha, h):
        """ h is number of days """
        self.nu, self.mu, self.sigma = t.fit(self.rets)
        mu_h, sigma_h = self.mu * (h/len(self.rets)), self.sigma * ((h/len(self.rets)) ** 0.5)
        VAR           = self.VaR_t_stats(alpha, h, self.nu, self.mu, sigma_h)
        VaR_table     = pd.DataFrame({"VaR (t-statistics)": VAR}, index = {"Confidence {0:.1f}%".format(100-alpha*100)})
        return VaR_table

    @classmethod
    def VaR_Param(cls, alpha, mu, sigma):
        return norm.ppf(1-alpha) * sigma - mu

    @classmethod
    def VaR_Hist(cls, alpha, h, rets):
        """ Estimation : VaR(h) = VaR(1) * sqrt(h) """
        return -np.percentile(rets, alpha*100) * ((h/len(rets)) ** 0.5)

    @classmethod
    def VaR_Simu(cls, alpha, h, mu, sigma, seed, n_sample):
        """ Generating n samples which has h days trading record """
        sim_returns = np.random.normal(mu, sigma, (h, n_sample))

        return -np.percentile(sim_returns, alpha * 100)

    @classmethod
    def VaR_t_stats(cls, alpha, h, nu, mu, sigma):
        return np.sqrt((nu-2)/nu) * t.ppf(1 - alpha, nu) * sigma - mu

class CVaR(VaR):
    def __init__(self, rets):
        super().__init__(rets)

    def CVaR_norm(self, alpha, h):
        self.mu, self.sigma = norm.fit(self.rets)
        mu_h, sigma_h = self.mu * (h/len(self.rets)), self.sigma * ((h/len(self.rets)) ** 0.5)
        CVAR = self.CVaR_Normal(alpha, mu_h, sigma_h)
        return pd.DataFrame({"CVaR (Normal)": CVAR}, index = {"Confidence {0:.1f}%".format(100-alpha*100)})

    def CVaR_t(self, alpha, h):
        """ h is number of days """
        self.nu, self.mu, self.sigma = t.fit(self.rets)
        mu_h, sigma_h = self.mu * (h/len(self.rets)), self.sigma * ((h/len(self.rets)) ** 0.5)
        self.nu = np.round(self.nu)
        xanu    = t.ppf(alpha, self.nu)
        CVAR    = self.CVaR_t_stats(alpha, 1, self.nu, xanu, mu_h, sigma_h)
        return pd.DataFrame({"CVaR (t-statistics)": CVAR}, index = {"Confidence {0:.1f}%".format(100-alpha*100)})

    @classmethod
    def CVaR_Normal(cls, alpha, mu, sigma):
        cvar = 1/alpha * norm.pdf(norm.ppf(alpha)) * sigma - mu
        return cvar

    @classmethod
    def CVaR_t_stats(cls, alpha, h, nu, xanu, mu, sigma):
        cvar = -1/alpha * 1/(1 - nu) * (nu - 2 + xanu**2) * t.pdf(xanu, nu) * sigma - h*mu
        return cvar

if __name__ == "__main__":
    import sys
    sys.path.insert(0, "../")
    df      = pd.read_csv("../Data/Forex_130603_191005.csv")
    df      = df.reindex(index = df.index[::-1])
    df      = df.rename(columns = {"index": "Time"}).set_index("Time")
    df_rets = df.apply(lambda x: Calculate_Return(x)).dropna()

    print(VaR(df_rets[["GBP_USD"]]).VaR_norm(0.01, 20))
    print(VaR(df_rets[["GBP_USD"]]).VaR_t(0.01, 20))
    print(CVaR(df_rets[["GBP_USD"]]).CVaR_norm(0.01, 20))
    print(CVaR(df_rets[["GBP_USD"]]).CVaR_t(0.01, 20))
