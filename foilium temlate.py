# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 20:55:11 2021

@author: tanakanc
"""

import folium
#from folium.features import DivIcon 
from folium.plugins import Fullscreen
#from folium.plugins import FeatureGroupSubGroup


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
# any plot on layer 1 will not show at the beginning because of show= False
layer1 = folium.FeatureGroup(name= '<u><b>layer1</b></u>',show= False)
m.add_child(layer1)

layer2 = folium.FeatureGroup(name= '<u><b>layer2</b></u>',show= True)
m.add_child(layer2)


# marker 1 #draw marker with corlor you want (default is blue)
# and if you not specific icon , it shows (!)
# put it at base layer
folium.Marker(
        location=[13.82868065256, 100.3621470],
        title = 'marker1 at base',
        popup = 'marker1 at base',
        icon= folium.Icon(color='red')).add_to(m)
        
# marker 2 #draw marker with default marker
# put it to layer1 which will not show at the beginning
folium.Marker(
        location=[13.72868065256, 100.6621470],
        title = 'marker2 at layer1',
        popup = 'marker2 at layer1').add_to(layer1)

# marker 3 #draw marker with corlor you want and assigned icon
# and if you not specific icon , it shows (!)
# put it at layer2
folium.Marker(
        location=[13.718685256, 100.3621470],
        title = 'marker1 at layer2',
        popup = 'marker1 at layer2',
        icon= folium.Icon(color='green',icon='ok-sign')).add_to(layer2)


# marker 4 #draw marker with symbol you want at base
#First, you have to create CSS class in order to relate with our marker class
# in the code below I created class called  fa-mysymbol
my_symbol_css_class= """ <style>
.fa-mysymbol:before {
    font-family: Arial; 
    font-weight: bold;
    font-size: 12px;
    color: white;
    background-color:black;
    border-radius: 10px; 
    white-space: pre;
    content: ' M4 ';
    }
</style>    
        """
# the below is just add above  CSS class to folium root map      
m.get_root().html.add_child(folium.Element(my_symbol_css_class))
# then we just create marker and specific your css class in icon like below
folium.Marker(
        location=[13.318685256, 100.321470],
        title = 'marker4 at base',
        popup = 'marker4 at base',
        icon= folium.Icon(color='red', icon='fa-mysymbol', prefix='fa')).add_to(m)

folium.Circle(
            radius= 10000, # this is metre unit
            location=[13.318685256, 100.321470],
            title = 'area marker4 at base',
            popup = 'area marker4 at base',
            color="salmon",
            fill= True,
            fill_opacity=0.4,
            opacity=0.3,
            weight= 1
        ).add_to(m)    


# marker5 Popup with deep information of the marker
# we have to create html page to put it into our popup
# ALERT! you may have to know about HTML and CSS
def fancy_html():

    html = """<!DOCTYPE html>
<html>

<head>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</head>

<body>
<h5> Header </h5>
<div class= "row"> 

<div class= "col-sm-12" > 
<table class="table table-striped">
<thead>
<tr>
<th>head1</th>
<th>head2</th>
</thead>
<tbody>
<tr>
<td> 1 </td>
<td> 2 </td>
</tr>
<tr>
<td> 3 </td>
<td> 4 </td>
</tr>
</tbody>
</table>
</div>

</div>
<img src="https://images.unsplash.com/photo-1560221328-12fe60f83ab8?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1506&q=80" alt="just for example" width="400" >

        </body>
        </html>
        """
    return html

# import more library to create iframe for popup
import branca  
  
# finally , bring them all together.
html = fancy_html()
iframe_deep = branca.element.IFrame(html=html,width=450,height=400)
popup_deep = folium.Popup(iframe_deep,parse_html=True)
folium.Marker(
        location=[13.718685256, 100.321570],
        title = 'marker5 at base wtih deep details',
        popup= popup_deep ,
        icon= folium.Icon(color='black')).add_to(m)




# to let the map have full screen button
Fullscreen(
    position='topright',
    title='Expand me',
    title_cancel='Exit me',

).add_to(m)

# to let the map have selectd layer1 layer2 you created
folium.LayerControl(collapsed=True,position= 'bottomright').add_to(m)

# save it to html then we can send the file to our colleagues
m.save('mymap.html')   