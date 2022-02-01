import pandas as pd
import loading
import numpy as np

def valm2_communal(df):
    return df.groupby(['l_codinsee', 'anneemut']).mean()[['valm2']].unstack().reset_index().T.reset_index().T.iloc[2:,:]


def fill_na(df, df_2):
    df_commune = loading.load_communal_data()
    df_commune.columns = ['l_codinsee', 'code_zone', 'no_need']  
    df_commune.drop(['no_need', 'code_zone'], axis=1, inplace=True)
    df_commune['l_codinsee'] = df_commune['l_codinsee'].astype(int)
    df_commune['coddep'] = df_commune['l_codinsee']//1000

    df.l_codinsee = df.l_codinsee.astype(int)  
     
    df = df.merge(df_commune,how='right',on='l_codinsee')
    
    df_3 = pd.DataFrame(df_2.groupby(['coddep']).mean()['valm2'].reset_index())
    df_3.coddep = df_3.coddep.astype(int)
    df.coddep = df.coddep.astype(int)

    df = df.merge( df_3, how='left', on='coddep')
    df.drop(['coddep'], axis=1, inplace=True)

    df_to_fill = df.iloc[:, 1:]
    df_to_fill = df_to_fill.ffill(axis=1).bfill(axis=1)
    df_to_fill.drop(['valm2'], axis=1, inplace=True)

    return pd.concat([ df.iloc[:,:1] , df_to_fill], axis=1).drop_duplicates()



def calculated_data(df_buy, df_sell):
    df = pd.DataFrame()

    df_buy_calcul = valm2_communal(df_buy)
    df_buy_calcul.columns = ['l_codinsee','b_14', 'b_15', 'b_16', 'b_17', 'b_18', 'b_19', 'b_20']
    df_buy_calcul = fill_na(df_buy_calcul, df_buy)
    df = pd.concat([df, df_buy_calcul])

    df_sell_calcul = valm2_communal(df_sell)
    df_sell_calcul.columns = ['l_codinsee','s_14', 's_15', 's_16', 's_17', 's_18', 's_19', 's_20']
    df_sell_calcul = fill_na(df_sell_calcul, df_sell)

    df = df.merge(df_sell_calcul, how='left', on='l_codinsee')
    df.drop_duplicates(inplace=True)

    array = df.iloc[:, 8:15].values / df.iloc[:, 1:8].values
    cols = ['ratio_2014', 'ratio_2015', 'ratio_2016', 'ratio_2017', 'ratio_2018', 'ratio_2019', 'ratio_2020']
    df = pd.concat([df,pd.DataFrame(array, columns=cols)], axis=1)

    for i in range (15,21):
        df = pd.concat([df, 100*(df.iloc[:, i+1] - df.iloc[:, i])/df.iloc[:, i] ], axis=1)
        col_name = 'evol_' + str(2000 + i)
        df.columns = [*df.columns[:-1], col_name]
        i+=1
    
    return(df)

def mean_absolute_percentage_error(y_true,y_pred):
    return np.mean(np.abs((y_pred - y_true)/y_true))
