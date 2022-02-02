import pandas as pd
import geopandas as gpd
import os

# Source : https://www.data.gouv.fr/fr/datasets/les-communes-d-ile-de-france-idf/
GEOMETRY_PATH = './data/decoupage_communal/communes-dile-de-france-au-01-janvier.shp'
COMMUNAL_PATH = './data/decoupage_idf.csv'
COMMERCES_PATH = './data/données_nb_commerces_commune.csv'
FILOSOFI_PATH  = './data/filosofi.xlsx'

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


def load_commerces(path = COMMERCES_PATH):
    df = pd.read_csv(path, sep=';')
    df['nb_educ'] = df['École maternelle 2019'] + df['École élémentaire 2019'] + df['Collège 2019'] + df['Lycée 2019']
    df['nb_sante'] = df["Service d'urgences 2019"] + df['Médecin généraliste 2019'] + df['Infirmier 2019']
    df['nb_hypermarche'] = df['Hypermarché - Supermarché 2019'] + df['Supérette - Épicerie 2019']

    df.rename(columns = {'Code' : 'insee'},inplace=True)
    return df[['insee','nb_educ','nb_sante','nb_hypermarche']]

def load_filosofi(path = FILOSOFI_PATH):
    df = pd.read_excel(path)
    df.rename(columns = {'CODGEO' : 'insee', 'MED18' : 'median_rev'},inplace=True)
    df.insee = df.insee.apply(lambda x : int(x) if str(x).isdigit() else -1)
    return df[['insee','median_rev']]


