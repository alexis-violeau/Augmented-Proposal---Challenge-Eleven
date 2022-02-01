import sys
import numpy as np
from model import X_COLS_BUY
import streamlit as st 
import folium
from folium import plugins
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import geopandas as gpd

sys.path.append('src/')

st.set_page_config(layout="wide")

import preprocessing
import loading
import visualization
import model

df = loading.load_data()
df_sell, df_buy = preprocessing.filter_dataset(df)

st.sidebar.title('Opportunities in the real estate landscape')

st.sidebar.header('Map')

type = st.sidebar.radio(
     "Type of mutation",
     ('Appartment', 'Raw land'))

if type == 'Appartment':
    df_selected = df_sell
else:
    df_selected = df_buy

col = st.sidebar.selectbox(
     'KPI',
     ('trade density','valm2', 'return', 'change in return'))

year_min,year_max = st.sidebar.slider('Select year range :',2014, 2020, (2016, 2018))

if col == 'trade density':
    df_selected = df_selected[['anneemut','insee']]
    df_agg = df_selected[(df_selected['anneemut'] >= year_min) & (df_selected['anneemut'] <= year_max)].groupby('insee').count().reset_index()
    df_geo = gpd.GeoDataFrame(preprocessing.add_geodata(df_agg).round())
    map = visualization.communal_maps(communal_df=df_geo,col='anneemut',legend='Number of trade')
    
if col == 'valm2':
    df_selected = df_selected[['anneemut','insee',col]]
    df_agg = df_selected[(df_selected['anneemut'] >= year_min) & (df_selected['anneemut'] <= year_max)].groupby('insee').mean().reset_index()
    df_geo = gpd.GeoDataFrame(preprocessing.add_geodata(df_agg).round())
    map = visualization.communal_maps(communal_df=df_geo,col=col,legend='Average square meter price')
    
st.sidebar.header('The Right Price')

map.add_child(folium.ClickForMarker(popup='Sell price (/m2) = '))



adresse = st.sidebar.text_input('Adress : ', '11 Rue Vieille du Temple, Paris')

lat,long = visualization.extract_logitude_latitude(adresse)

model_buy = model.load_buy_model()
model_sell = model.load_sell_model()

price_sell = model_sell.predict(np.array([[lat,long,1.0,0.0]]))
price_buy = model_buy.predict(np.array([[lat,long,0.0]]))


folium.Marker(
      location=[lat, long],
      popup=adresse +  ' \n sell price : ' + str(price_sell[0]) + ' \n buy price : ' + str(price_buy[0]),
   ).add_to(map)

folium_static(map)
