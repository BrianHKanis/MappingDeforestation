from api.adapters.client import Client
from api.adapters.country_builder import CountryBuilder
import streamlit as st
from streamlit_folium import st_folium, folium_static
from folium.plugins import Fullscreen
import folium
# st.set_page_config(layout="wide")

can = Client('Canada')
us = Client('United_States')
mex = Client('Mexico')

canada = CountryBuilder(can)
usa = CountryBuilder(us)
mexico = CountryBuilder(mex).run()



# map = folium.Map(location=(50.5260, -105.2551), zoom_start=2.2)
# st_folium(map) 