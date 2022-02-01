import sys
import streamlit as st 
import folium
from folium import plugins
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import geopandas as gpd

sys.path.append('src/')

import preprocessing
import loading
import visualization

df = loading.load_data()
df_sell, df_buy = preprocessing.filter_dataset(df)

st.title('Opportunities in the real estate landscape')

type = st.radio(
     "Type of mutation",
     ('Appartment', 'Raw land'))

if type == 'Appartment':
    visualization.density_maps(df_sell)
else:
    visualization.density_maps(df_buy)
    
df_sell_agg = preprocessing.add_geodata(df_sell.groupby('l_codinsee').mean().reset_index())
df_sell_agg = gpd.GeoDataFrame(df_sell_agg.round())


visualization.communal_maps(df_sell_agg,'valm2')
    
    