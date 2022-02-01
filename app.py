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

st.write('Hello World !')


map_sell = folium.Map(location=[48.868229, 2.347402],
                    zoom_start = 12)

folium_static(map_sell)



#st.map(df_sell[['latitude','longitude','valm2']])