#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 23:14:10 2020

@author: yanglingqin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon
import mapclassify


listing_file = "./listings_clean_copy.csv"
data = pd.read_csv(listing_file)

# Get NYC street map
nyc_map = gpd.read_file("./BoroughBoundaries/geo_export_cfd5c472-30c8-4552-ad8a-34a29d6338f7.shp")
nyc_map = nyc_map.dropna()
# designate coordinate system
crs = {'init'':''espc:4326'}

# Combine lat and lng into points.
points = [Point(xy) for xy in zip(data['lng'], data['lat'])]

# Transform from dataframe to GeoDataframe.
geo_points = gpd.GeoDataFrame(data, crs=crs, geometry = points)
       

# create figure and axes, assign to subplot
fig, ax = plt.subplots(figsize=(20,20))


# add .shp mapfile to axes
nyc_map.plot(ax=ax, alpha=0.4,color='grey')

#geo_points.plot(column='avgRating', scheme='quantiles', ax=ax, alpha=0.5, legend = True, markersize = 15)
#plt.title("Average Rating of Listings in NYC", fontsize = 20, fontweight = 'bold')

geo_points.plot(column='isSuperhost',  cmap='OrRd', categorical = True,  ax=ax, alpha=0.5, legend = True, markersize = 15)
plt.title("Superhost of Listings in NYC", fontsize = 20, fontweight = 'bold')


plt.show()



