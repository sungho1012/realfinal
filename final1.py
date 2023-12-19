#!/usr/bin/env python
# coding: utf-8

# In[3]:


#침수흔적도 최종

import geopandas as gpd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Gulim'

shp_file_path_emd = r"C:/Users/user/Desktop/seoul_emd/seoul_emd.shp"
gdf_emd = gpd.read_file(shp_file_path_emd)

shp_file_path_flood = "C:/Users/user/Desktop/침수흔적도/서울시_2022.shp"
gdf_flood = gpd.read_file(shp_file_path_flood)

fig, ax = plt.subplots(figsize=(10, 8))

gdf_emd.plot(ax=ax, color='skyblue', alpha=0.5, edgecolor='black')
gdf_flood.plot(ax=ax, color='red', alpha=1)

plt.title("서울시 2022년 침수흔적도", color='white')
plt.xlabel("경도(Longitude)", color='white')
plt.ylabel("위도(Latitude)", color='white')

ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

ax.set_facecolor('black')

fig.patch.set_facecolor('black')

plt.show()


# In[ ]:




