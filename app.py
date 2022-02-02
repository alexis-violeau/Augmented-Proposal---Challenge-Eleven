import sys
import numpy as np
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
     "What are you looking for ?",
     ('Sell appartment', 'Buy raw land'))

if type == 'Appartment':
    df_selected = df_sell
else:
    df_selected = df_buy

col = st.sidebar.selectbox(
     'Indicator',
     ('Trade density','Value per square meter', 'Return', 'Change in return'))

year_min,year_max = st.sidebar.slider('Year range :',2014, 2020, (2016, 2018))

if col == 'Trade density':
    df_selected = df_selected[['anneemut','insee']]
    df_agg = df_selected[(df_selected['anneemut'] >= year_min) & (df_selected['anneemut'] <= year_max)].groupby('insee').count().reset_index()
    df_geo = gpd.GeoDataFrame(preprocessing.add_geodata(df_agg).round())
    map = visualization.communal_maps(communal_df=df_geo,col='anneemut',legend='Number of trade')
    
if col == 'Value per square meter':
    df_selected = df_selected[['anneemut','insee','valm2']]
    df_agg = df_selected[(df_selected['anneemut'] >= year_min) & (df_selected['anneemut'] <= year_max)].groupby('insee').mean().reset_index()
    df_geo = gpd.GeoDataFrame(preprocessing.add_geodata(df_agg).round())
    map = visualization.communal_maps(communal_df=df_geo,col='valm2',legend='Average square meter price')
    
st.sidebar.header('The Right Price')

map.add_child(folium.ClickForMarker(popup='Sell price'))


adresse = st.sidebar.text_input('Adress : ', 'Rue de la libération Jouy en Josas')

lat,long = visualization.extract_logitude_latitude(adresse)

model_sell = model.load_sell_model()
model_buy = model.load_buy_model()

sell_price = round(model_sell.predict(np.array([[lat,long,1,0]]))[0])
buy_price = round(model_buy.predict(np.array([[lat,long,0]]))[0])

st.sidebar.caption('Sell price : ' + str(sell_price))
st.sidebar.caption('Buy price : ' + str(buy_price))


folium.Marker(
      location=[lat, long],
      popup=adresse,
   ).add_to(map)

folium_static(map)
