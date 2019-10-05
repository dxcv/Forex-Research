import json
import numpy as np
import scipy as sp
import pandas as pd

class ComplexEncoder(json.JSONEncoder):
    def default(self, var):
        """ Adding pandas datatype """
        if isinstance(var, pd.Series):
            return var.to_dict()
        elif isinstance(var, pd.DataFrame):
            return var.to_dict(orient = "dict")
        """ Adding numpy datatype """
        if isinstance(var, np.ndarray):
            return list(var)
        elif isinstance(var, (np.int8, np.int16, np.int32, np.int64)):
            return int(var)
        elif isinstance(var, np.bool_):
            return bool(var)
        """ Adding Class datatype """
        if hasattr(var, "__dict__"):
            return var.__dict__

        else:
            return super().default(var)

class save_to_json(object):
    def __init__(self, data, name):
        with open(name + ".json", "w") as file:
            json.dump(data, file, cls = ComplexEncoder)

class load_from_json(object):
    def __init__(self, name):
        assert ".json" in name, " Please Correct File Name "
        with open(name, "r") as file:
            self.data = json.loads(file.read())
