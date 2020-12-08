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


"""
with open(listing_file, 'r') as f:
    f.readline();
    for line in f:
        num_of_listing += 1
        data = line.split(',')
        if(len(data) > 6) and (data[5].isdigit()) and (data[6].isdigit()):
            latitude = data[5]
            longitude = data[6]
            location.append(tuple((latitude, longitude)))
"""
# enter your api key here 
api_key = 'AIzaSyBCcZNt6ALOwNKpWB9P5r5e9Qykpj5yrQY'


# Get nearby places
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
        """
        elif category == "art_gallery":
            nearby_art.append(1)
        elif category == "shopping_mall":
            nearby_shop.append(1)
        elif category == "park":
            nearby_park.append(1)
        """
    else:
        if(category == "subway_station"):
            nearby_subway.append(0)
        elif category == "tourist_attraction":
            nearby_tour.append(0)
        """
        elif category == "art_gallery":
            nearby_art.append(0)
        elif category == "shopping_mall":
            nearby_shop.append(0)
        elif category == "park":
            nearby_park.append(0)
        """

    
    
    
    
    


def main():
    #search_nearby("40.87709,-73.85866999999998", api_key, "500", "subway_station", "20")
    #search_nearby("40.8584,-73.86969",  api_key, "500", "subway_station", "20")
    
    # Read from listing file.
    data = pd.read_csv(listing_file, sep = ',')
    print(data['lat'], data['lng'])
    
    
    location = [(row[0],row[1]) for row in zip(data['lat'], data['lng'])]
    print(len(location))
    
    for d in location:
        loc = str(d[0])+","+str(d[1])
        print(loc)
        search_nearby(loc,  api_key, "1000", "tourist_attraction", "20" )
        search_nearby(loc,  api_key, "500", "subway_station", "20" )
        #search_nearby(loc,  api_key, "1000", "art_gallery", "20" )
        #search_nearby(loc,  api_key, "1000", "shopping_mall", "20" )
        #search_nearby(loc,  api_key, "1000", "park", "20" )
    
    
    
    data['subway'] = nearby_subway
    data['tourist_attraction'] = nearby_tour
    data.to_csv('./listings_nearby.csv', index=False)
    
    
    #nearby_subway = []
    # Add nearby subway station back to listings.
    #data = [json.loads(line) for line in open("./nearby.json", 'r')]
    #for d in data:
        #print(d)











if __name__ == "__main__":
    # execute only if run as a script
    main()