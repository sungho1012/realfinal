#!/usr/bin/env python
# coding: utf-8

# In[1]:


import geopandas as gpd
import pandas as pd
import pydeck as pdk

df = pd.read_excel("C:/Users/user/Desktop/10월 이동인구 정리3.xlsx")
sgg = gpd.read_file("C:/Users/user/Desktop/서울 행정동/서울 행정동/서울 행정동.shp", encoding='utf-8').set_crs(5179)

sgg_wgs84 = sgg.to_crs(4326)
sgg_wgs84['lon'] = sgg_wgs84['geometry'].centroid.x
sgg_wgs84['lat'] = sgg_wgs84['geometry'].centroid.y

df['ocode'] = df['ocode'].astype(str)
df['dcode'] = df['dcode'].astype(str)
data = df.merge(sgg_wgs84[['ADM_CD', 'lon', 'lat']], how = 'left' , left_on = 'ocode', right_on = 'ADM_CD')
data = data.merge(sgg_wgs84[['ADM_CD', 'lon', 'lat']], how = 'left' , left_on = 'dcode', right_on = 'ADM_CD')


GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]

# Specify a deck.gl ArcLayer
arc_layer = pdk.Layer(
    "ArcLayer",
    data=data,
    get_width="value/300",
    get_source_position=["lon_x", "lat_x"],
    get_target_position=["lon_y", "lat_y"],
    get_tilt=15,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(latitude=38, longitude=127, bearing=0, pitch=70, zoom=8,)


TOOLTIP_TEXT = {"html": "migration {value} <br /> source in red; target in green"}
r = pdk.Deck(arc_layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT)
r.to_html("arc_layer.html")


# In[2]:


get_ipython().system(' pip install pydeck')


# In[3]:


import geopandas as gpd
import pandas as pd
import pydeck as pdk

df = pd.read_excel("C:/Users/user/Desktop/10월 이동인구 정리3.xlsx")
sgg = gpd.read_file("C:/Users/user/Desktop/서울 행정동/서울 행정동/서울 행정동.shp", encoding='utf-8').set_crs(5179)

sgg_wgs84 = sgg.to_crs(4326)
sgg_wgs84['lon'] = sgg_wgs84['geometry'].centroid.x
sgg_wgs84['lat'] = sgg_wgs84['geometry'].centroid.y

df['ocode'] = df['ocode'].astype(str)
df['dcode'] = df['dcode'].astype(str)
data = df.merge(sgg_wgs84[['ADM_CD', 'lon', 'lat']], how = 'left' , left_on = 'ocode', right_on = 'ADM_CD')
data = data.merge(sgg_wgs84[['ADM_CD', 'lon', 'lat']], how = 'left' , left_on = 'dcode', right_on = 'ADM_CD')


GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]

# Specify a deck.gl ArcLayer
arc_layer = pdk.Layer(
    "ArcLayer",
    data=data,
    get_width="value/300",
    get_source_position=["lon_x", "lat_x"],
    get_target_position=["lon_y", "lat_y"],
    get_tilt=15,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(latitude=38, longitude=127, bearing=0, pitch=70, zoom=8,)


TOOLTIP_TEXT = {"html": "migration {value} <br /> source in red; target in green"}
r = pdk.Deck(arc_layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT)
r.to_html("arc_layer.html")


# In[ ]:




