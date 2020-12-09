'''
title: listingcleaning.py
author: Chengyu Wu
date: 2-DEC-2020
'''

import numpy as np
import pandas as pd
from scipy import stats


def bayesian_average():
    """
    Calculate bayesian average rating using the mean and median of the existing rating data.
    """
    listings = pd.read_csv('listings_clean_copy.csv', header=0, index_col=0)
    print(listings.keys())

    print(listings['reviewsCount'].describe())
    listings['bysAvgRating'] = ((listings['avgRating'] * listings['reviewsCount']) + (
            np.mean(listings['avgRating']) * np.median(listings['reviewsCount']))) / (
                                       listings['reviewsCount'] + np.median(listings['reviewsCount']))

    print(listings['bysAvgRating'].describe)
    listings.to_csv('listings_clean_copy.csv')


def merge_host_response_data():
    """
    Merging host response information from dataset of insideairbnb.com.
    :return:
    """
    listings_master = pd.read_csv('listings_clean_copy.csv', header=0, index_col=0)
    listings_insidebnb = pd.read_csv('listings_insidebnb.csv', header=0)
    listings_insidebnb = listings_insidebnb[['id', 'host_response_time', 'host_response_rate', 'host_acceptance_rate']]
    listings_master = pd.merge(listings_master, listings_insidebnb, on='id', how='left')
    listings_master.to_csv('listings_clean_copy.csv')


def data_type_correction():
    """
    Correct data type of some columns, specifically striping the percentage mark in the host response info,
    and transform these columns into float64.
    :return:
    """
    listings = pd.read_csv('listings_clean_copy.csv', header=0, index_col=0)
    listings.info()
    listings['host_response_rate'] = listings['host_response_rate'].str[:-1]
    listings['host_response_rate'] = listings['host_response_rate'].astype('float64')
    listings['host_acceptance_rate'] = listings['host_acceptance_rate'].str[:-1]
    listings['host_acceptance_rate'] = listings['host_acceptance_rate'].astype('float64')
    listings.info()

