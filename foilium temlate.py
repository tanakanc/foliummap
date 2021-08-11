# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 20:55:11 2021

@author: tanakanc
"""

import folium
from folium.features import DivIcon 
from folium.plugins import Fullscreen
from folium.plugins import FeatureGroupSubGroup


# Create the map object called m which is the base layer of the map
# Center at specific lcation 
# tiles is background layer of the map which you can select from below as well.
# Zoom level = the level you want to zoom at the beginning
m = folium.Map(location=[13.728680652566823, 100.362147071618],
               tiles='CartoDB positron',
               zoom_start=8)

#if you need option that user can select background layer of the map
folium.TileLayer('openstreetmap').add_to(m)
folium.TileLayer('Stamen Toner').add_to(m)
folium.TileLayer('Stamen Terrain').add_to(m)
folium.TileLayer('Stamen Watercolor').add_to(m)
folium.TileLayer('CartoDB positron').add_to(m)


# We can create other layers to separate our marker or any area we want to draw.
#name= layername that you want to show to user  '<u><b>layer1</b></u>'
# from above <u><b> are just CSS tag which to underline and bold respectively
layer1 = folium.FeatureGroup(name= '<u><b>layer1</b></u>',show= False)
m.add_child(layer1)

layer2 = folium.FeatureGroup(name= '<u><b>layer2</b></u>',show= True)
m.add_child(layer2)


# marker 1
folium.Marker(
        location=[13.82868065256, 100.3621470],
        title = 'marker1 at base',
        popup = 'marker1 at base',
        icon= folium.Icon(color='red')).add_to(m)
        
# marker 2
folium.Marker(
        location=[13.72868065256, 100.6621470],
        title = 'marker1 at base',
        popup = 'marker1 at base').add_to(layer1)

# marker 3
folium.Marker(
        location=[13.718685256, 100.3621470],
        title = 'marker1 at base',
        popup = 'marker1 at base',
        icon= folium.Icon(color='green',icon='ok-sign')).add_to(layer2)

Fullscreen(
    position='topright',
    title='Expand me',
    title_cancel='Exit me',
    #force_separate_button=True,
    style={'background-color':'red'}
).add_to(m)

# to selectd layer1 layer2 you created
folium.LayerControl(collapsed=True,position= 'bottomright').add_to(m)
m.save('mymap.html')   