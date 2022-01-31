import pandas as pd
import os

col = ['idmutation', 'idmutinvar', 'idopendata',
       'idnatmut', 'codservch', 'refdoc', 'datemut', 'anneemut', 'moismut',
       'coddep', 'libnatmut', 'vefa', 'valeurfonc', 'nbdispo', 'nblot',
       'nbcomm', 'l_codinsee', 'nbsection', 'l_section', 'nbpar', 'l_idpar',
       'nbparmut', 'l_idparmut', 'nbsuf', 'sterr', 'nbvolmut', 'nblocmut',
       'l_idlocmut', 'nblocmai', 'nblocapt', 'nblocdep', 'nblocact',
       'nbapt1pp', 'nbapt2pp', 'nbapt3pp', 'nbapt4pp', 'nbapt5pp', 'nbmai1pp',
       'nbmai2pp', 'nbmai3pp', 'nbmai4pp', 'nbmai5pp', 'sbati', 'sbatmai',
       'sbatapt', 'sbatact', 'sapt1pp', 'sapt2pp', 'sapt3pp', 'sapt4pp',
       'sapt5pp', 'smai1pp', 'smai2pp', 'smai3pp', 'smai4pp', 'smai5pp',
       'codtypbien', 'libtypbien', 'latitude', 'longitude']


def load_data(path = 'data/'):
    df = pd.DataFrame()
    for file in os.listdir(path):
        print(file)

        if file[:9] == 'mutations':
            df = pd.concat([df,pd.read_csv(path + file,usecols = col)])
    return df