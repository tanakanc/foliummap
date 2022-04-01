# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 21:29:01 2022

@author: tanakanc
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from sklearn.cluster import KMeans
import folium

df_map = pd.read_excel('input_clustering.xlsx')

# 1. Clustering your data into KMeans clustering one of the unsupervise clsutering method
#1.1 data preparation
X = df_map .iloc[:, 1:3].values
# Using the elbow method to find the optimal number of clusters
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# 1.2 Training the K-Means model regarding to your elbow method or business logic groups
kmeans = KMeans(n_clusters = 4, init = 'k-means++', random_state = 42)
y_kmeans = kmeans.fit_predict(X)
# 1.3 map data back to df
df_map['cluster'] = y_kmeans +1 # to step up to group 1 to 4
 

#%%
#2.plot data to map

# Create the map object called m which is the base layer of the map
m = folium.Map(location=[df_map['lat'].mean(), df_map['lon'].mean()],
               tiles='CartoDB positron',
               zoom_start=7)

# create layers based on your clustering groups
layer1 = folium.FeatureGroup(name= '<u><b>group1</b></u>',show= True)
m.add_child(layer1)

layer2 = folium.FeatureGroup(name= '<u><b>group2</b></u>',show= True)
m.add_child(layer2)

layer3 = folium.FeatureGroup(name= '<u><b>group3</b></u>',show= True)
m.add_child(layer3)

layer4 = folium.FeatureGroup(name= '<u><b>group4</b></u>',show= True)
m.add_child(layer4)


#draw marker class for each group by adding CSS class
my_symbol_css_class= """ <style>
.fa-g1:before {
    font-family: Arial; 
    font-weight: bold;
    font-size: 12px;
    color: black;
    background-color:white;
    border-radius: 10px; 
    white-space: pre;
    content: ' g1 ';
    }
  

.fa-g2:before {
    font-family: Arial; 
    font-weight: bold;
    font-size: 12px;
    color: black;
    background-color:white;
    border-radius: 10px; 
    white-space: pre;
    content: ' g2 ';
    }

.fa-g3:before {
    font-family: Arial; 
    font-weight: bold;
    font-size: 12px;
    color: black;
    background-color:white;
    border-radius: 10px; 
    white-space: pre;
    content: ' g3 ';
    }

.fa-g4:before {
    font-family: Arial; 
    font-weight: bold;
    font-size: 12px;
    color: black;
    background-color:white;
    border-radius: 10px; 
    white-space: pre;
    content: ' g4 ';
    }

.fa-g1bad:before {
    font-family: Arial; 
    font-weight: bold;
    font-size: 12px;
    color: white;
    background-color:red;
    border-radius: 10px; 
    white-space: pre;
    content: ' g1 ';
    }
  

.fa-g2bad:before {
    font-family: Arial; 
    font-weight: bold;
    font-size: 12px;
    color: white;
    background-color:red;
    border-radius: 10px; 
    white-space: pre;
    content: ' g2 ';
    }

.fa-g3bad:before {
    font-family: Arial; 
    font-weight: bold;
    font-size: 12px;
    color: white;
    background-color:red;
    border-radius: 10px; 
    white-space: pre;
    content: ' g3 ';
    }

.fa-g4bad:before {
    font-family: Arial; 
    font-weight: bold;
    font-size: 12px;
    color: white;
    background-color:red;
    border-radius: 10px; 
    white-space: pre;
    content: ' g4 ';
    }
</style>    


        """
# the below is just add above  CSS class to folium root map      
m.get_root().html.add_child(folium.Element(my_symbol_css_class))


# then we just create marker and specific your css class in icon like below
for index, row in df_map.iterrows():
    if row['cluster'] == 1 and row['business_condition1'] < 500 :
        color='black'
        fa_symbol = 'fa-g1'
        lay = layer1
    elif row['cluster'] == 1 and row['business_condition1'] >= 500 :
        color='black'
        fa_symbol = 'fa-g1bad'
        lay = layer1
    elif row['cluster'] == 2 and row['business_condition1'] < 500:
        color='purple'
        fa_symbol = 'fa-g2'
        lay = layer2
    elif row['cluster'] == 2 and row['business_condition1'] >= 500:
        color='purple'
        fa_symbol = 'fa-g2bad'
        lay = layer2        
    elif row['cluster'] == 3 and row['business_condition1'] < 500:
        color='orange'
        fa_symbol = 'fa-g3'
        lay = layer3
    elif row['cluster'] == 3 and row['business_condition1'] >= 500:
        color='orange'
        fa_symbol = 'fa-g3bad'
        lay = layer3
    elif row['cluster'] == 4 and row['business_condition1'] < 500:
        color='blue'
        fa_symbol = 'fa-g4'
        lay = layer4
    else:
        color='blue'
        fa_symbol = 'fa-g4bad'
        lay = layer4
        
    folium.Marker(
        location=[row['lat'], row['lon']],
        title = row['name']+ 'group:{}'.format(str(row['name'])),
        popup = row['name']+ 'group:{}'.format(str(row['name'])),
        icon= folium.Icon(color=color, icon=fa_symbol, prefix='fa')).add_to(lay)

#draw cluster each group
#flat line to group path
#prepare layer and color for each group
layer_list = [layer1,layer2,layer3,layer4]
color_list = ['black','purple','orange','blue']
for g in df_map['cluster'].unique():

    # this part we apply ConvexHull theory to find the boundary of each group
    # first, we have to cut the lat lon in each group 
    latlon_cut =df_map[df_map['cluster']==g].iloc[:, 1:3]
    # second, scipy already provides  the great function for ConvexHull
    # we just throw our dataframe with lat lon in this function
    hull = ConvexHull(latlon_cut.values)
    # and with magic, we can have new lat lon boundary of each group
    Lat = latlon_cut.values[hull.vertices,0]
    Long = latlon_cut.values[hull.vertices,1] 
    # the we create dataframe boundary and convert it to list of lat lon 
    # for plotting polygon in folium
    cluster = pd.DataFrame({'lat':Lat,'lon':Long })       
    area = list(zip(cluster['lat'],cluster['lon']))
    # plot polygon
    list_index = g-1 # minus 1 to get the same index 
    lay_cluster = layer_list[list_index ] 
    folium.Polygon(locations=area,
        color=color_list[list_index],
        weight=2,
        fill=True,
        fill_opacity=0.1,
        opacity=0.8).add_to(lay_cluster) 
            
# to let the map have selectd layer1 layer2 you created
folium.LayerControl(collapsed=False,position= 'bottomright').add_to(m)

# save it to html then we can send the file to our colleagues
m.save('mymap_clustering.html')   