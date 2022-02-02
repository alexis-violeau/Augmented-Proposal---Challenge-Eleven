from sklearn.inspection import partial_dependence
import model
import matplotlib.pyplot as plt
from PyALE import ale
from tqdm import tqdm
import pandas as pd

def plot_pdp(df_sell,col='ts_date',augmented = False):


    rf = model.load_sell_model(augmented)

    plt.figure(figsize=(4,2))

    if augmented:
        X_train,X_test,_,_ = model.produce_datasets(df_sell,model.X_COLS_SELL_AUGM,model.Y_COLS,augmented)
    else :
        X_train,X_test,_,_ = model.produce_datasets(df_sell,model.X_COLS_SELL,model.Y_COLS,augmented)

    x_train = pd.concat([X_train,X_test])
    pdp = partial_dependence(rf, x_train, col, kind = 'average')
    plt.plot(pdp['values'][0],pdp['average'][0])
    plt.ylabel('Partial Dependence')
    plt.show()


def plot_ale(df_sell,col='ts_date',augmented=False):

    rf = model.load_sell_model(augmented)

    plt.figure(figsize=(4,2))

    if augmented:
        X_train,X_test,_,_ = model.produce_datasets(df_sell,model.X_COLS_SELL_AUGM,model.Y_COLS,augmented)
    else :
        X_train,X_test,_,_ = model.produce_datasets(df_sell,model.X_COLS_SELL,model.Y_COLS,augmented)

    x_train = pd.concat([X_train,X_test])
    pdp = ale(X=x_train, model=rf, feature=[col], grid_size=50, predictors = col,feature_type = 'continuous')
    
    plt.show()
   

