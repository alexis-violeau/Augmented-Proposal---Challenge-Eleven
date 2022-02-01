import pandas as pd
import geopandas as gpd
import os

# Source : https://www.data.gouv.fr/fr/datasets/les-communes-d-ile-de-france-idf/
GEOMETRY_PATH = './data/decoupage_communal/communes-dile-de-france-au-01-janvier.shp'
COMMUNAL_PATH = './data/decoupage_idf.csv'

USE_COLS = ['anneemut', 'moismut', 'coddep', 'libnatmut', 'valeurfonc', 'nblot','nbcomm', 'l_codinsee', 'sterr', 
       'sapt1pp', 'sapt2pp', 'sapt3pp', 'sapt4pp', 'sapt5pp', 'sbatapt', 'libtypbien', 'latitude', 'longitude']


def load_data(path = 'data/'):
    df = pd.DataFrame()
    for file in os.listdir(path):
        print(file)

        if file[:9] == 'mutations':
            df = pd.concat([df,pd.read_csv(path + file,usecols = USE_COLS)])
    return df

def load_geodata(path=GEOMETRY_PATH):
    df = gpd.read_file(path)
    df.insee = df.insee.astype(int)
    return df[['insee','geometry']]

def load_communal_data(path=COMMUNAL_PATH):
    df = pd.read_csv(path, sep=';', header=None)
    return df
