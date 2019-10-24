import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

if __name__ == "__main__":
    import sys
    sys.path.insert(0, "../")
    from STATS.Basic import cal_returns
    from STATS.Risk import VaR, CVaR
    from STATS.Portfolio import Generating_Portfolio as GP
    df      = pd.read_csv("../Data/Forex_130603_191005.csv")
    df      = df.reindex(index = df.index[::-1])
    df      = df.rename(columns = {"index": "Time"}).set_index("Time")
    df_rets = cal_returns(None).multi_rets(df)

    print(GP(df_rets, 3, 10).Generator())

    # print(VaR(df_rets[["GBP_USD"]]).VaR_norm(0.01, 20))
    # print(VaR(df_rets[["GBP_USD"]]).VaR_t(0.01, 20))
    # print(CVaR(df_rets[["GBP_USD"]]).CVaR_norm(0.01, 20))
    # print(CVaR(df_rets[["GBP_USD"]]).CVaR_t(0.01, 20))
