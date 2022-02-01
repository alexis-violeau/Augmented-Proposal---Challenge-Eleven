import sys
import streamlit as st 
import folium
from folium import plugins
from folium.plugins import HeatMap
from streamlit_folium import folium_static

sys.path.append('src/')

import preprocessing
import loading

df = loading.load_data()
df_sell, df_buy = preprocessing.filter_dataset(df)

st.title('Opportunities in the real estate landscape')

type = st.radio(
     "Type of mutation",
     ('Appartment', 'Raw land'))

if type == 'Appartment':
    map_sell = folium.Map(location=[48.868229, 2.347402],
                    zoom_start = 12)
    coords_sell = df_sell[['latitude', 'longitude']]
    coords_sell = coords_sell.dropna(axis=0, subset=['latitude','longitude'])
    coords_sell = [[row['latitude'],row['longitude']] for index, row in coords_sell.iterrows()]
    HeatMap(coords_sell).add_to(map_sell)

    folium_static(map_sell)
else:
    map_buy = folium.Map(location=[48.868229, 2.347402],
                    zoom_start = 12)
    coords_buy = df_buy[['latitude', 'longitude']]
    coords_buy = coords_buy.dropna(axis=0, subset=['latitude','longitude'])
    coords_buy = [[row['latitude'],row['longitude']] for index, row in coords_buy.iterrows()]
    HeatMap(coords_buy).add_to(map_buy)
    
    folium_static(map_buy)