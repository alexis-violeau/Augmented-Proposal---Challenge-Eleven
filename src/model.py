from math import radians
import numpy as np
import os
from pickle import dump, load
import preprocessing
import metrics
import loading
import pandas as pd

from sklearn.model_selection import GridSearchCV,train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import make_scorer

#AVERAGE_RADIUS_OF_EARTH_KM = 6371

X_COLS_SELL = ['latitude', 'longitude', 'rooms','ts_date']
X_COLS_SELL_AUGM = ['latitude', 'longitude', 'rooms','ts_date','nb_educ','nb_sante','nb_hypermarche','median_rev']
X_COLS_BUY = ['latitude', 'longitude','ts_date']

Y_COLS = 'valm2'


PARAM_GRID = {'n_estimators' : [500],
               'max_samples' : [0.5]}


def produce_datasets(df,x_cols,y_col,add_external = False):

    if add_external :
        df_commerces = loading.load_commerces()
        df_filosofi = loading.load_filosofi()
        df = df.merge(df_commerces, on = 'insee')
        df = df.merge(df_filosofi, on = 'insee')

    df_train, df_test = train_test_split(df)
    df_train.reset_index(inplace=True,drop=True)
    df_test.reset_index(inplace=True,drop=True)

    X_train = df_train[x_cols]
    X_test = df_test[x_cols]

    y_train = df_train[y_col]
    y_test = df_test[y_col]

    return X_train, X_test, y_train, y_test


def fit_sell_model(df):
    X_train, X_test, y_train, y_test = produce_datasets(df,X_COLS_SELL,Y_COLS)

    scoring = make_scorer(metrics.mean_absolute_percentage_error,greater_is_better = False)
    gscv = GridSearchCV(estimator=RandomForestRegressor(), 
                        param_grid=PARAM_GRID,verbose=1,
                        scoring = scoring)
    gscv.fit(X_train,y_train)


    if not os.path.exists('saved_model'):
        os.mkdir('saved_model')

    y_pred = gscv.best_estimator_.predict(X_test)
    print("Mean absolute percentage error : {:.2f}".format(100*metrics.mean_absolute_percentage_error(y_test.values,y_pred)))
    print("Median absolute percentage error : {:.2f}".format(100*metrics.median_absolute_percentage_error(y_test.values,y_pred)))

    model = RandomForestRegressor(**gscv.best_params_)
    model.fit(pd.concat([X_train,X_test]),pd.concat([y_train,y_test]))

    dump(model, open('./saved_model/sell_model.pkl', 'wb'))



def fit_sell_model_augmented(df):
    X_train, X_test, y_train, y_test = produce_datasets(df,X_COLS_SELL_AUGM,Y_COLS,add_external=True)

    scoring = make_scorer(metrics.mean_absolute_percentage_error,greater_is_better = False)
    gscv = GridSearchCV(estimator=RandomForestRegressor(), 
                        param_grid=PARAM_GRID,verbose=1,
                        scoring = scoring)
    gscv.fit(X_train,y_train)


    if not os.path.exists('saved_model'):
        os.mkdir('saved_model')

    y_pred = gscv.best_estimator_.predict(X_test)
    print("Mean absolute percentage error : {:.2f}".format(100*metrics.mean_absolute_percentage_error(y_test.values,y_pred)))
    print("Median absolute percentage error : {:.2f}".format(100*metrics.median_absolute_percentage_error(y_test.values,y_pred)))

    model = RandomForestRegressor(**gscv.best_params_)
    model.fit(pd.concat([X_train,X_test]),pd.concat([y_train,y_test]))

    dump(model, open('./saved_model/sell_model_augmented.pkl', 'wb'))




def fit_buy_model(df):
    X_train, X_test, y_train, y_test = produce_datasets(df,X_COLS_BUY,Y_COLS)

    scoring = make_scorer(metrics.mean_absolute_percentage_error,greater_is_better = False)
    gscv = GridSearchCV(estimator=RandomForestRegressor(), 
                        param_grid=PARAM_GRID,verbose=1,
                        scoring = scoring)
    gscv.fit(X_train,y_train)


    if not os.path.exists('saved_model'):
        os.mkdir('saved_model')

    y_pred = gscv.best_estimator_.predict(X_test)
    print("Mean absolute percentage error : {:.2f}".format(100*metrics.mean_absolute_percentage_error(y_test.values,y_pred)))
    print("Median absolute percentage error : {:.2f}".format(100*metrics.median_absolute_percentage_error(y_test.values,y_pred)))

    model = RandomForestRegressor(**gscv.best_params_)
    model.fit(pd.concat([X_train,X_test]),pd.concat([y_train,y_test]))

    dump(model, open('./saved_model/buy_model.pkl', 'wb'))



def load_sell_model(augmented = False):
    try:
        if augmented :
            return load(open('./saved_model/sell_model.pkl', 'rb'))
        else :
            return load(open('./saved_model/sell_model_augmented.pkl', 'rb'))

    except :
        raise NameError('No model fitted yet. Please call model.fit_sell_model first.')



def load_buy_model():
    try:
        return load(open('./saved_model/buy_model.pkl', 'rb'))

    except :
        raise NameError('No model fitted yet. Please call model.fit_sell_model first.')