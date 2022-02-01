import numpy as np

def mean_absolute_percentage_error(y_true,y_pred):
    return np.mean(np.abs((y_pred - y_true)/y_true))