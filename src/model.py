from math import radians
import numpy as np
from scipy.spatial import distance_matrix
from sklearn.neighbors import BallTree

AVERAGE_RADIUS_OF_EARTH_KM = 6371
X_COLS = ['latitude', 'longitude', 'rooms','ts_date','neighborhood_price','mean_distance_neigh']
Y_COLS = ['valm2']




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
            break
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

        Neigh_price.append(np.mean(np.array(clean_values)[new_dist<dist_max]))


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

