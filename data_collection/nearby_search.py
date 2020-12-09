#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 00:45:09 2020

@author: yanglingqin
"""

import requests
from urllib.parse import urlencode
import pandas as pd
import numpy as np


nearby_subway = []
nearby_tour = []
nearby_art = []
nearby_shop = []
nearby_park = []
listing_file = "./listings_clean_copy.csv"


# enter your api key here 
api_key = 'AIzaSyBCcZNt6ALOwNKpWB9P5r5e9Qykpj5yrQY'


"""
Input: location string("latitude,longitude"), search radius, category of places, how many results.

Description: Construct the request url using inputs. Get the JSON response. If the response's 
status is "ZERO_RESULTS", meaning no subway/toursit attractions nearby, set the corresponding 
item in list to 0, otherwise 1.

Output: A list recording whether there is subway/tourist attractions nearby for each listing.
"""
def search_nearby(loc, api_key, radius, category, pagetoken):
    # nearby search url
    nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    response = requests.get(
        nearby_url + urlencode(
            {'location': loc, 'radius': radius, 'type': category, 'key': api_key}
            ))
    nearby_response = response.json()
    if nearby_response['status']!= "ZERO_RESULTS":
        if(category == "subway_station"):
            nearby_subway.append(1)
        elif category == "tourist_attraction":
            nearby_tour.append(1) 
    else:
        if(category == "subway_station"):
            nearby_subway.append(0)
        elif category == "tourist_attraction":
            nearby_tour.append(0)
        

    
    
    


def main():

    # Read from listing file.
    data = pd.read_csv(listing_file, sep = ',')
    
    location = [(row[0],row[1]) for row in zip(data['lat'], data['lng'])]
    
    for d in location:
        loc = str(d[0])+","+str(d[1])
        search_nearby(loc,  api_key, "1000", "tourist_attraction", "20" )
        search_nearby(loc,  api_key, "500", "subway_station", "20" )
   
    
    
    data['subway'] = nearby_subway
    data['tourist_attraction'] = nearby_tour
    data.to_csv('./listings_nearby.csv', index=False)
    
    





if __name__ == "__main__":
    # execute only if run as a script
    main()