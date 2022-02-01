
import streamlit as st 
import folium
from folium import plugins
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim


def communal_maps(communal_df, col, legend = ''):
    communal_map = folium.Map(location=[48.868229, 2.347402],
                          zoom_start = 10,
                          tiles = 'cartodbpositron')
    myscale = (communal_df[col].quantile((0,0.2,0.75,0.9,0.98,1))).tolist()
    choropleth = folium.Choropleth(
                    geo_data = communal_df,                  #json
                    name ='choropleth',
                    data = communal_df,
                    columns = ['insee', col], #columns to work on
                    key_on ='feature.properties.insee',
                    fill_color = 'YlGnBu',     #I passed colors Yellow,Green,Blue
                    threshold_scale = myscale,
                    fill_opacity = 0.7,
                    line_opacity = 0.4,
                   legend_name = legend,
                    highlight = True)
    choropleth.add_to(communal_map)
    folium.LayerControl().add_to(communal_map)
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['insee', col], aliases=['Postal Code : ', legend + ' : '])
    )
    return communal_map

def extract_logitude_latitude(adresse):
    geolocator = Nominatim(user_agent = 'thomas_b')
    location = geolocator.geocode(adresse)
    print(location)
    if location is None :
        raise NameError("Erreur d'adresse")
    return location.latitude, location.longitude