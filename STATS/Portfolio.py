import numpy as np
import pandas as pd

class Generating_Portfolio(object):
    def __init__(self, rets, num, time_length):
        self.rets        = rets
        self.num         = num
        self.time_length = time_length
        self.mean        = self.rets.mean()
        self.cov_matrix  = self.rets.cov()

    @staticmethod
    def Performance(weights, mean_rets, cov_mat):
        print(weights, mean_rets, cov_mat)
