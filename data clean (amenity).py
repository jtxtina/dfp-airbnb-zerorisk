#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 17:27:54 2020

@author: HuZhexin
"""

import pandas as pd
listings = pd.read_csv('/Users/HuZhexin/Desktop/Data Focused Python/project/listings_clean(a).csv', encoding='latin1')

# to separate four amenities
amenity = listings['previewAmenityNames']

wifi = []
kitchen = []
heating = []
air_conditioning = []

for index in amenity.index:
    if 'Wifi' in amenity.iloc[index]:
        wifi.append('1')
    else:
        wifi.append('0')
    if 'Kitchen' in amenity.iloc[index]:
        kitchen.append('1')
    else:
        kitchen.append('0')        
    if 'Heating' in amenity.iloc[index]:
        heating.append('1')
    else:
        heating.append('0')       
    if 'Air conditioning' in amenity.iloc[index]:
        air_conditioning.append('1')
    else:
        air_conditioning.append('0')        
        
listings['Wifi'] = wifi
listings['Kitchen'] = kitchen
listings['Heating'] = heating
listings['Air conditioning'] =air_conditioning

listings.to_csv('/Users/HuZhexin/Desktop/Data Focused Python/project/listings_clean(a).csv', index = False)
