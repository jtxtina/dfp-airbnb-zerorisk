#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 23:14:10 2020

@author: yanglingqin

Description: o	Read from the listings csv file and clean data that’s with NAN rating.
             o	Read from NYC borough shape file.
             o	Set coordinate system.
             o	Combine latitude and longitude into points.
             o	Create figure and axes, assign to subplot
             o	Geoplot with categorical/quantiles.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon
import mapclassify



def main():
    
    
    listing_nearby = "../data_collection/listings_nearby.csv"
    data = pd.read_csv(listing_nearby)
    data = data[data['bysAvgRating'].notna()]
    
    # Get NYC street map
    nyc_map = gpd.read_file("./BoroughBoundaries/geo_export_cfd5c472-30c8-4552-ad8a-34a29d6338f7.shp")
    nyc_map = nyc_map.dropna()
    
    # Set coordinate system
    coordinate = {'init'':''espc:4326'}
    
    # Combine latitude and longitude into points.
    points = [Point(xy) for xy in zip(data['lng'], data['lat'])]
    
    # Transform from dataframe to GeoDataframe.
    geo_points = gpd.GeoDataFrame(data, crs=coordinate, geometry = points)
           
    
    # create figure and axes, assign to subplot
    fig, ax = plt.subplots(figsize=(18,18))
    
    
    # add .shp mapfile to axes
    nyc_map.plot(ax=ax, alpha=0.35,color='grey')
    
    #geo_points.plot(column='bysAvgRating',cmap='OrRd', scheme='quantiles', ax=ax, alpha=0.5, legend = True, markersize = 15)
    #plt.title("Average Rating of Listings in NYC", fontsize = 20, fontweight = 'bold')
    
    #geo_points.plot(column='priceString', cmap='hot', scheme='quantiles', ax=ax, alpha=0.5, legend = True, markersize = 15)
    #plt.title("Prices of Listings in NYC", fontsize = 20, fontweight = 'bold')
    
    #geo_points.plot(column='tourist_attraction',  categorical = True, ax=ax, alpha=0.5, legend = True, markersize = 15)
    #plt.title("Listings with nearby subway in NYC", fontsize = 20, fontweight = 'bold')
    
    #geo_points.plot(column='subway',  categorical = True, ax=ax, alpha=0.5, legend = True, markersize = 12)
    #plt.title("Listings with nearby subway in NYC", fontsize = 20, fontweight = 'bold')
    
    
    plt.show()
    
    




if __name__ == "__main__":
    # execute only if run as a script
    main()

