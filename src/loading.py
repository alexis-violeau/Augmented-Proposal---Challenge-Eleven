import pandas as pd
import os

USE_COLS = ['anneemut', 'moismut', 'coddep', 'libnatmut', 'valeurfonc', 'nblot','nbcomm', 'l_codinsee', 'sterr', 
       'sapt1pp', 'sapt2pp', 'sapt3pp', 'sapt4pp', 'sapt5pp', 'sbatapt', 'libtypbien', 'latitude', 'longitude']


def load_data(path = 'data/'):
    df = pd.DataFrame()
    for file in os.listdir(path):
        print(file)

        if file[:9] == 'mutations':
            df = pd.concat([df,pd.read_csv(path + file,usecols = USE_COLS)])
    return df


