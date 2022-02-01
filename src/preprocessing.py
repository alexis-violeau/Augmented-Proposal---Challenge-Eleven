import loading
import numpy as np


SELL_COLS = ['anneemut','moismut', 'coddep','insee','latitude','longitude','nblot','valm2','rooms','ts_date']
BUY_COLS = ['anneemut','moismut', 'coddep','insee','latitude','longitude','valm2','ts_date']
AVERAGE_RADIUS_OF_EARTH_KM = 6371


def subset_valm2_by_iqr(df, width=1.5):
    # Calculate Q1, Q2 and IQR
    q1 = df['valm2'].quantile(0.25)
    q3 = df['valm2'].quantile(0.75)
    iqr = q3 - q1
    # Apply filter with respect to IQR, including optional whiskers
    filter = (df['valm2'] >= q1 - width*iqr) & (df['valm2'] <= q3 + width*iqr)
    return df.loc[filter]


def delete_low_valm2(df, value_min):
    return df[df['valm2'] >= value_min]


def compute_number_of_rooms(row):
    if row.sapt5pp > 0 : return 5
    elif row.sapt4pp > 0 : return 4
    elif row.sapt3pp > 0 : return 3
    elif row.sapt2pp > 0 : return 2
    elif row.sapt1pp > 0 : return 1
    else : return 0

def filter_dataset(df):

    # preprocessing the date
    df = preprocess_date(df)

    # Select only 'new appartments' + 'one appartment' deals
    df_sell = df[(df.libnatmut == "Vente en l'état futur d'achèvement") & (df.libtypbien == 'UN APPARTEMENT')]
    # Compute the value per m2
    df_sell['valm2'] = df_sell.valeurfonc/df_sell.sbatapt
    # Filter outliers + anomalies (should be only one comune + no land with an appartment)
    df_sell=df_sell[(df_sell.valm2 < 2e4) & (df_sell.nbcomm == 1) & (df_sell.sterr == 0 )]
    # Compute number of rooms
    df_sell['rooms'] = df_sell.apply(compute_number_of_rooms,axis=1)    
    # Convert list of INSEE code to single value
    df_sell['insee'] = df_sell['l_codinsee'].apply(lambda x : x[2:-2]).astype(int)
    # Set right types
    df_sell.coddep = df_sell.coddep.astype(int)
    df_sell.anneemut = df_sell.anneemut.astype(int)
    df_sell.moismut = df_sell.moismut.astype(int)
    df_sell.nblot = df_sell.nblot.astype(int)
    
    # Remove clear outliers
    df_sell = subset_valm2_by_iqr(df_sell)
    df_sell = delete_low_valm2(df_sell, 1000)

    # Filter only TAB
    df_buy = df[df.libtypbien == 'TERRAIN DE TYPE TAB']
    # Filter only one comm
    df_buy = df_buy[(df_buy.nbcomm == 1)]
    # Compute value per surface
    df_buy['valm2'] = df_buy.valeurfonc/df_buy.sterr
    
    
    # Convert list of INSEE code to single value
    df_buy['insee'] = df_buy['l_codinsee'].apply(lambda x : x[2:-2]).astype(int)
    

    df_buy.coddep = df_buy.coddep.astype(int)
    df_buy.anneemut = df_buy.anneemut.astype(int)
    df_buy.moismut = df_buy.moismut.astype(int)
    df_buy.nblot = df_buy.nblot.astype(int)

    # Remove clear outliers
    df_buy = subset_valm2_by_iqr(df_buy)
    df_buy = delete_low_valm2(df_buy, 20)

    return df_sell[SELL_COLS].reset_index(drop=True), df_buy[BUY_COLS].reset_index(drop=True)


def add_geodata(df):
    df_geo = loading.load_geodata()
    return df.merge(df_geo,how='left',left_on='insee',right_on='insee')


def add_communal_div(df):
    df_commune = loading.load_communal_data()
    df_commune.columns = ['insee', 'code_zone', 'no_need']
    df_commune.drop(['no_need'], axis=1, inplace=True)
    df_commune['insee'] = df_commune['insee'].astype(int)

    df = df.merge(df_commune,how='left',left_on='insee',right_on='insee')
    df.drop(['insee'], axis=1, inplace=True)

    # Adding code_zone for Paris
    df['code_zone'].replace({np.NaN : "Abis"}, inplace=True)
    return df

def preprocess_date(df):
    df['ts_date'] = df.anneemut + (df.moismut-1)/12 
    df['ts_date'] = df['ts_date'] - np.max(df['ts_date'])
    return df



