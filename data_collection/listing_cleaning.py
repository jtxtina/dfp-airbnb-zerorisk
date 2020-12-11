#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: listing_cleaning.py
Description: Split the previewAmenityNames into four seperate amenity,
calculate Bayesian average rating from original rating data,
merge response rate data from CSV downloaded from insideairbnb.com,
and correct data type of the master dataset.
"""

import numpy as np
import pandas as pd

def amenity():
    # to separate four amenities
    listings = pd.read_csv('../data_collection/listings_clean_copy.csv', header=0, index_col=0)
    
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
    
    listings.to_csv('../data_collection/listings_clean_copy.csv', index = False)
    

def bayesian_average():
    """
    Calculate bayesian average rating using the mean and median of the existing rating data.
    """
    listings = pd.read_csv('../data_collection/listings_clean_copy.csv', header=0, index_col=0)
    print(listings.keys())

    print(listings['reviewsCount'].describe())
    listings['bysAvgRating'] = ((listings['avgRating'] * listings['reviewsCount']) + (
            np.mean(listings['avgRating']) * np.median(listings['reviewsCount']))) / (
                                       listings['reviewsCount'] + np.median(listings['reviewsCount']))

    print(listings['bysAvgRating'].describe)
    listings.to_csv('../data_collection/listings_clean_copy.csv')


def merge_host_response_data():
    """
    Merging host response information from dataset of insideairbnb.com.
    :return:
    """
    listings_master = pd.read_csv('../data_collection/listings_clean_copy.csv', header=0, index_col=0)
    listings_insidebnb = pd.read_csv('../data_collection/listings_insidebnb.csv', header=0)
    listings_insidebnb = listings_insidebnb[['id', 'host_response_time', 'host_response_rate', 'host_acceptance_rate']]
    listings_master = pd.merge(listings_master, listings_insidebnb, on='id', how='left')
    listings_master.to_csv('../data_collection/listings_clean_copy.csv')


def data_type_correction():
    """
    Correct data type of some columns, specifically striping the percentage mark in the host response info,
    and transform these columns into float64.
    :return:
    """
    listings = pd.read_csv('../data_collection/listings_clean_copy.csv', header=0, index_col=0)
    listings.info()
    listings['host_response_rate'] = listings['host_response_rate'].str[:-1]
    listings['host_response_rate'] = listings['host_response_rate'].astype('float64')
    listings['host_acceptance_rate'] = listings['host_acceptance_rate'].str[:-1]
    listings['host_acceptance_rate'] = listings['host_acceptance_rate'].astype('float64')
    listings.info()
    listings.to_csv('../data_collection/listings_clean_copy.csv')


if __name__ == '__main__':
    amenity()
    bayesian_average()
    merge_host_response_data()
    data_type_correction()
