
import streamlit as st 
import folium
from folium import plugins
from folium.plugins import HeatMap
from streamlit_folium import folium_static


def communal_maps(communal_df, col, legend=''):
    communal_map = folium.Map(location=[48.868229, 2.347402],
                          zoom_start = 10,
                          tiles = 'cartodbpositron')

    myscale = (communal_df[col].quantile((0,0.2,0.75,0.9,0.98,1))).tolist()
    folium.Choropleth(
        geo_data = communal_df, #json
        name ='choropleth',                  
        data = communal_df,                     
        columns = ['insee',col], #columns to work on
        key_on ='feature.properties.insee',
        fill_color ='YlGnBu',     #I passed colors Yellow,Green,Blue
        threshold_scale=myscale,
        fill_opacity = 0.7,
        line_opacity = 0.2,
       legend_name = legend
    ).add_to(communal_map)

    folium.LayerControl().add_to(communal_map)

    return folium_static(communal_map)


def density_maps(df):
    map = folium.Map(location=[48.868229, 2.347402],
                    zoom_start = 12)
    coords = df[['latitude', 'longitude']]
    coords = coords.dropna(axis=0, subset=['latitude','longitude'])
    coords = [[row['latitude'],row['longitude']] for index, row in coords.iterrows()]
    HeatMap(coords).add_to(map)

    return folium_static(map)