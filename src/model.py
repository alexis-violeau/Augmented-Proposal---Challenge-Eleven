from math import radians
import numpy as np
import os
from pickle import dump, load
import preprocessing
import metrics
import pandas as pd

from sklearn.model_selection import GridSearchCV,train_test_split
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import make_scorer

#AVERAGE_RADIUS_OF_EARTH_KM = 6371

X_COLS_SELL = ['latitude', 'longitude', 'rooms','ts_date']
X_COLS_BUY = ['latitude', 'longitude','ts_date']

Y_COLS = 'valm2'


def produce_datasets(df,x_cols,y_col,n_neigh_max = 100,dist_max = 350):


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
    param_grid = {'n_estimators' : [500],
                  'max_samples' : [0.5]}

    scoring = make_scorer(metrics.mean_absolute_percentage_error,greater_is_better = False)
    gscv = GridSearchCV(estimator=RandomForestRegressor(), 
                        param_grid=param_grid,verbose=1,
                        scoring = scoring)
    gscv.fit(X_train,y_train)


    if not os.path.exists('saved_model'):
        os.mkdir('saved_model')

    y_pred = gscv.best_estimator_.predict(X_test)
    print("Mean absolute percentage error : {:.2f}".format(100*metrics.mean_absolute_percentage_error(y_test.values,y_pred)))

    model = RandomForestRegressor(**gscv.best_params_)
    model.fit(pd.concat([X_train,X_test]),pd.concat([y_train,y_test]))

    dump(model, open('./saved_model/sell_model.pkl', 'wb'))




def fit_buy_model(df):
    X_train, X_test, y_train, y_test = produce_datasets(df,X_COLS_BUY,Y_COLS)
    param_grid = {'n_estimators' : [500],
                  'max_samples' : [0.5]}

    scoring = make_scorer(metrics.mean_absolute_percentage_error,greater_is_better = False)
    gscv = GridSearchCV(estimator=RandomForestRegressor(), 
                        param_grid=param_grid,verbose=1,
                        scoring = scoring)
    gscv.fit(X_train,y_train)


    if not os.path.exists('saved_model'):
        os.mkdir('saved_model')

    y_pred = gscv.best_estimator_.predict(X_test)
    print("Mean absolute percentage error : {:.2f}".format(100*metrics.mean_absolute_percentage_error(y_test.values,y_pred)))

    model = RandomForestRegressor(**gscv.best_params_)
    model.fit(pd.concat([X_train,X_test]),pd.concat([y_train,y_test]))

    dump(model, open('./saved_model/buy_model.pkl', 'wb'))



def load_sell_model():
    try:
        return load(open('./saved_model/sell_model.pkl', 'rb'))

    except :
        raise NameError('No model fitted yet. Please call model.fit_sell_model first.')



def load_buy_model():
    try:
        return load(open('./saved_model/buy_model.pkl', 'rb'))

    except :
        raise NameError('No model fitted yet. Please call model.fit_sell_model first.')



""""

def compute_neighborhood_price_train(df,n_neigh_max = 50,dist_max = 500,clean = True):

    df['radian_longitude'] = df.longitude.apply(radians)
    df['radian_latitude'] = df.latitude.apply(radians)

    model = BallTree(df[['radian_latitude', 'radian_longitude']].values, metric='haversine')
    dist, indices = model.query(df[['radian_latitude', 'radian_longitude']].values,n_neigh_max+1)

    # remove the one :
    nb_query = len(dist)

    new_dist = np.zeros((nb_query,n_neigh_max))
    new_indices = np.zeros((nb_query,n_neigh_max))

    Neigh_price = []
    mean_distance = []
    indices_to_delete = []

    for i in range(nb_query):
        try :
            to_remove = np.where(dist[i]==0)[0]
            new_dist = np.delete(dist[i], to_remove)
            new_indices = np.delete(indices[i], to_remove)
        except :
            new_dist = dist[i]
            new_indices = indices[i]


        values = df.valm2.values[new_indices.astype(int)]
        mean_values = np.mean(values)

        clean_values = []
        clean_indices = []

        for ind,m2values in enumerate(values) :
            if np.abs(m2values-mean_values)/m2values < 1:
                clean_values.append(m2values)
                clean_indices.append(ind)
            else :
                indices_to_delete.append(new_indices[ind])

        new_dist = new_dist[clean_indices] * AVERAGE_RADIUS_OF_EARTH_KM *1000
        mean_distance.append(np.mean(new_dist))
        clean_values = np.array(clean_values)

        if len(clean_values[new_dist<dist_max]):
            Neigh_price.append(np.mean(clean_values[new_dist<dist_max]))
        else :
            try :
                Neigh_price.append(clean_values[0])
            except :
                print('Increase number of neighbors, nan values.')
                Neigh_price.append(np.nan)


    df['neighborhood_price'] = Neigh_price
    df['mean_distance_neigh'] = mean_distance

    if clean :
        return df.drop(list(set(indices_to_delete))).reset_index()
    else :
        return df



def compute_neighborhood_price_test(df_train,df_test,n_neigh_max = 10,dist_max = 500):

    model = BallTree(df_train[['latitude', 'longitude']].values, metric='haversine')
    dist, indices = model.query(df_test[['latitude', 'longitude']].values,n_neigh_max)
    nb_query = len(dist) 

    Neigh_price = []
    mean_distance = []

    for i in range(nb_query):
        distances = dist[i] * AVERAGE_RADIUS_OF_EARTH_KM *1000
        mean_distance.append(np.mean(distances))
        new_indices = indices[i][distances<dist_max]
        if len(new_indices) == 0:
            new_indices = np.array(indices[i][0])
        Neigh_price.append(np.mean(df_train.valm2.values[new_indices.astype(int)]))
    
    df_test['neighborhood_price'] = Neigh_price
    df_test['mean_distance_neigh'] = mean_distance

    return df_test

"""